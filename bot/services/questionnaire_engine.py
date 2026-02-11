"""Questionnaire Engine — parses .md questionnaire files and drives the Q&A flow."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class Trigger:
    """Action to take when an answer matches a condition."""
    condition_op: str      # '==' or '!=' or 'in' (for multi matches?)
    condition_value: str   # Value to check against
    flag_name: str         # Flag to set in context
    flag_value: bool = True


@dataclass
class Question:
    id: str
    text: str
    q_type: str  # single | multi | text | info | scale
    options: List[str] = field(default_factory=list)
    triggers: List[Trigger] = field(default_factory=list)


@dataclass
class LogicRule:
    from_q: str
    to_q: str
    condition_answer: Optional[str] = None  # None = any answer (unless flag set)
    condition_flag: Optional[str] = None    # Name of flag to check
    condition_flag_value: bool = True       # Value expected for the flag


class QuestionnaireEngine:
    """Loads a questionnaire from a .md file, provides navigation."""

    def __init__(self) -> None:
        self.questions: Dict[str, Question] = {}
        self.question_order: List[str] = []
        self.rules: List[LogicRule] = []
        self._loaded = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, md_file_path: str) -> None:
        text = Path(md_file_path).read_text(encoding="utf-8")
        self._parse_questions(text)
        self._parse_rules(text)
        self._loaded = True

    def get_first_question(self) -> Optional[Question]:
        if not self.question_order:
            return None
        return self.questions[self.question_order[0]]

    def execute_triggers(self, q_id: str, answer: str, context: Dict[str, Any]) -> None:
        """Evaluate triggers for the given question and answer, updating context flags."""
        q = self.questions.get(q_id)
        if not q or not q.triggers:
            return

        # Prepare selected values for multi-choice logic
        # Multi answers often stored as "Val1, Val2" string
        if q.q_type == "multi":
            selected_set = {x.strip() for x in answer.split(",")}
        else:
            selected_set = {answer.strip()}

        for trig in q.triggers:
            match = False
            
            # Logic for '=='
            if trig.condition_op == "==":
                # If single: exact match
                # If multi: trigger if THIS value is present in selection? 
                # Usually triggers on "If answer is X"
                if q.q_type == "multi":
                    match = trig.condition_value in selected_set
                else:
                    match = (answer.strip() == trig.condition_value)

            # Logic for '!='
            elif trig.condition_op == "!=":
                # If single: answer is NOT X
                # If multi: "If selection is NOT X" usually means X is NOT in set 
                # OR "Selection is anything except X" (e.g. "None" is option, checking if something else selected)
                if q.q_type == "multi":
                    # Special handling: if condition is "No", and user selected "Pain", 
                    # then "No" is NOT in set -> True.
                    match = trig.condition_value not in selected_set
                else:
                    match = (answer.strip() != trig.condition_value)

            if match:
                context[trig.flag_name] = trig.flag_value

    def get_next_question(
        self,
        current_q_id: str,
        answer: str,
        context: Dict[str, Any] | None = None,
    ) -> Optional[Question]:
        """Return next question based on logic rules (flags and answers)."""
        context = context or {}

        # 1. Evaluate triggers first (to ensure context is up-to-date locally if not done yet)
        # Note: In a real app, triggers should ideally be executed ONCE when saving answer.
        # But doing it here ensures logic consistency if caller didn't. 
        # (Be careful not to duplicate side effects if they were external, but here it's just dict update)
        self.execute_triggers(current_q_id, answer, context)

        # 2. Check Logic Rules in order
        for rule in self.rules:
            if rule.from_q != current_q_id:
                continue

            # Check Flag condition
            if rule.condition_flag:
                flag_val = context.get(rule.condition_flag, False)
                if flag_val != rule.condition_flag_value:
                    continue  # Flag mismatch, skip rule

            # Check Answer condition
            if rule.condition_answer is not None:
                # For basic compat, check against "q_gender" in context for router questions
                # OR check against current 'answer' if it matches? 
                # Usually rules are "From Q1 to Q2".
                # Legacy special case: branching based on PREVIOUS question answer stored in context
                # (like gender).
                
                # If rule depends on specific answer string:
                # We check if context[current_q_id] matches, or 'answer' matches.
                # But 'answer' is the *current* answer being submitted.
                if rule.condition_answer == answer:
                     pass # Match
                elif context.get("q_gender") == rule.condition_answer:
                     pass # Match (legacy gender hack)
                else:
                     continue # Mismatch

            # If we got here, all conditions passed
            return self.questions.get(rule.to_q)

        # 3. Fallback: Sequential order
        if current_q_id in self.question_order:
            try:
                idx = self.question_order.index(current_q_id)
                if idx + 1 < len(self.question_order):
                    return self.questions[self.question_order[idx + 1]]
            except ValueError:
                pass

        return None

    def is_finished(self, q_id: str) -> bool:
        q = self.questions.get(q_id)
        if q and q.q_type == "info":
            return True
        # Naive check: if next is None. 
        # But next depends on answer/context. 
        # We assume if it's info, it's end.
        return False

    # ------------------------------------------------------------------
    # Parsers
    # ------------------------------------------------------------------

    # Regex for Question block
    _QUESTION_HEADER_RE = re.compile(r"^###\s+\d+\.\s+`(\w+)`\s*$", re.MULTILINE)
    _FIELD_RE = re.compile(r"^\*\s+\*\*(\w+):\*\*\s*(.+)$", re.MULTILINE)
    
    # Regex for Triggers: "*   If answer == "Val" set flag"
    _TRIGGER_RE = re.compile(r"^\*\s+If answer\s*(==|!=)\s*\"(.+?)\"\s*set\s+(\w+)\s*$", re.MULTILINE)

    # Regex for Rules
    # From `q1` to `q2`
    # From `q1` (flag: fname) to `q2`
    # From `q1` (flag: !fname) to `q2`
    # From `q1` (answer: Val) to `q2`
    _RULE_RE = re.compile(
        r"^\*\s+\*\*From\s+`(\w+)`\s*(?:\((.+?)\))?\s+to\s+`(\w+)`\*\*",
        re.MULTILINE
    )

    def _parse_questions(self, text: str) -> None:
        # Split by "### " to isolate blocks (simple approach)
        blocks = re.split(r"^###\s+", text, flags=re.MULTILINE)
        
        for block in blocks:
            if not block.strip():
                continue
            
            # Re-add ### for regex if needed, or just parse body
            # block starts with "1. `id`"
            header_match = re.match(r"^(\d+)\.\s+`(\w+)`", block)
            if not header_match:
                continue
            
            q_id = header_match.group(2)
            
            # Extract fields
            q_text = ""
            q_type = "text"
            options = []
            triggers = []

            for field_match in self._FIELD_RE.finditer(block):
                key = field_match.group(1)
                val = field_match.group(2).strip()
                
                if key == "Text":
                    q_text = val
                elif key == "Type":
                    q_type = val
                elif key == "Options":
                    # Use dot split per recent update
                    options = [o.strip() for o in val.split(".") if o.strip()]

            # Extract Triggers (look for lines starting with * If answer ...)
            # Need to scan the block text specifically
            trigger_lines = self._TRIGGER_RE.findall(block)
            for op, val, flag in trigger_lines:
                triggers.append(Trigger(
                    condition_op=op,
                    condition_value=val,
                    flag_name=flag,
                    flag_value=True
                ))

            q = Question(
                id=q_id, 
                text=q_text, 
                q_type=q_type, 
                options=options,
                triggers=triggers
            )
            self.questions[q_id] = q
            self.question_order.append(q_id)

    def _parse_rules(self, text: str) -> None:
        # Scan for Logic Rules section? Or just scan whole file for rule pattern
        for m in self._RULE_RE.finditer(text):
            from_q = m.group(1)
            params = m.group(2) # e.g. "flag: fname" or "answer: Val" or None
            to_q = m.group(3)

            cond_flag = None
            cond_flag_val = True
            cond_ans = None

            if params:
                params = params.strip()
                if params.startswith("flag:"):
                    # "flag: name" or "flag: !name"
                    raw = params.split(":", 1)[1].strip()
                    if raw.startswith("!"):
                        cond_flag = raw[1:]
                        cond_flag_val = False
                    else:
                        cond_flag = raw
                elif params.startswith("answer:"):
                    cond_ans = params.split(":", 1)[1].strip()
                elif params == "any answer":
                    pass

            self.rules.append(LogicRule(
                from_q=from_q, 
                to_q=to_q, 
                condition_answer=cond_ans,
                condition_flag=cond_flag,
                condition_flag_value=cond_flag_val
            ))
