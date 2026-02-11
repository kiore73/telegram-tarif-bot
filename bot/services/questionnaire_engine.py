"""Questionnaire Engine — parses .md questionnaire files and drives the Q&A flow."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Question:
    id: str
    text: str
    q_type: str  # single | multi | text | info
    options: List[str] = field(default_factory=list)


@dataclass
class LogicRule:
    from_q: str
    to_q: str
    condition_answer: Optional[str] = None  # None = any answer


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

    def get_next_question(
        self,
        current_q_id: str,
        answer: str,
        context: Dict[str, str] | None = None,
    ) -> Optional[Question]:
        """Return next question based on logic rules.

        ``context`` is a dict of {question_id: chosen_answer} collected so far.
        It is used for branching that depends on earlier answers (e.g. gender).
        """
        context = context or {}

        # 1) Look for a conditional rule first
        for rule in self.rules:
            if rule.from_q == current_q_id and rule.condition_answer is not None:
                # For the gender branch the condition is stored on the
                # *router* question (q_oda_doctor) but must be matched
                # against q_gender answer stored in context.
                ctx_gender = context.get("q_gender", "")
                if rule.condition_answer == ctx_gender:
                    return self.questions.get(rule.to_q)

        # 2) Fallback to generic (any answer) rule
        for rule in self.rules:
            if rule.from_q == current_q_id and rule.condition_answer is None:
                return self.questions.get(rule.to_q)

        # 3) Fallback to positional order
        if current_q_id in self.question_order:
            idx = self.question_order.index(current_q_id)
            if idx + 1 < len(self.question_order):
                return self.questions[self.question_order[idx + 1]]

        return None

    def is_finished(self, q_id: str) -> bool:
        q = self.questions.get(q_id)
        if q and q.q_type == "info":
            return True
        return self.get_next_question(q_id, "", {}) is None

    # ------------------------------------------------------------------
    # Parsers
    # ------------------------------------------------------------------

    _QUESTION_RE = re.compile(
        r"###\s+\d+\.\s+`(\w+)`\s*\n"
        r"\*\s+\*\*Text:\*\*\s*(.+)\n"
        r"\*\s+\*\*Type:\*\*\s*(\w+)\n"
        r"(?:\*\s+\*\*Options:\*\*\s*(.+)\n)?",
        re.MULTILINE,
    )

    _RULE_RE = re.compile(
        r"\*\s+\*\*From\s+`(\w+)`\s+\((?:any answer|answer:\s*(.+?))\)\s+to\s+`(\w+)`\*\*",
    )

    def _parse_questions(self, text: str) -> None:
        for m in self._QUESTION_RE.finditer(text):
            q_id = m.group(1)
            q_text = m.group(2).strip()
            q_type = m.group(3).strip()
            raw_opts = m.group(4)
            options = [o.strip() for o in raw_opts.split(",")] if raw_opts else []
            q = Question(id=q_id, text=q_text, q_type=q_type, options=options)
            self.questions[q_id] = q
            self.question_order.append(q_id)

    def _parse_rules(self, text: str) -> None:
        for m in self._RULE_RE.finditer(text):
            from_q = m.group(1)
            cond = m.group(2)  # None when "any answer"
            to_q = m.group(3)
            self.rules.append(LogicRule(from_q=from_q, to_q=to_q, condition_answer=cond))
