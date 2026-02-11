"""Questionnaire handler — drives Q&A using QuestionnaireEngine.

Features:
  - Edits the same message instead of sending new ones
  - ⬅️ Back button to return to previous question
  - Question history stack for navigation
"""

from __future__ import annotations

import os
import logging
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.questionnaire_engine import QuestionnaireEngine

logger = logging.getLogger(__name__)
router = Router()

# Base directory for questionnaire .md files
QUESTIONNAIRES_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

# Cache loaded engines
_engines: dict[str, QuestionnaireEngine] = {}


def _get_engine(name: str) -> QuestionnaireEngine:
    if name not in _engines:
        engine = QuestionnaireEngine()
        engine.load(str(QUESTIONNAIRES_DIR / f"{name}.md"))
        _engines[name] = engine
    return _engines[name]


QUESTIONNAIRE_MAP = {
    "basic": "basic_questionnaire",
    "ayurved_m": "ayurved_m_questionnaire",
    "ayurved_j": "ayurved_j_questionnaire",
}


async def _show_question(target: Message | CallbackQuery, state: FSMContext, edit: bool = False) -> None:
    """Display the current question — either edit existing message or send new one."""
    data = await state.get_data()
    phase = data.get("questionnaire_phase", "basic")
    q_id = data.get("current_question_id")
    history: list = data.get("question_history", [])

    engine = _get_engine(QUESTIONNAIRE_MAP[phase])

    if not q_id:
        q = engine.get_first_question()
    else:
        q = engine.questions.get(q_id)

    if not q:
        await _finish_phase(target, state)
        return

    await state.update_data(current_question_id=q.id)

    show_back = len(history) > 0

    # Determine whether to edit or send a new message
    if edit and isinstance(target, CallbackQuery) and target.message:
        msg = target.message
        try:
            if q.q_type == "single":
                await msg.edit_text(
                    f"❓ {q.text}",
                    reply_markup=keyboards.single_option_keyboard(q.options, show_back=show_back),
                )
            elif q.q_type == "multi":
                await state.update_data(multi_selected=[])
                await msg.edit_text(
                    f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_MULTI_HINT}",
                    reply_markup=keyboards.multi_option_keyboard(q.options, show_back=show_back),
                )
            elif q.q_type == "text":
                await msg.edit_text(f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_TEXT_HINT}")
            elif q.q_type == "info":
                await msg.edit_text(
                    f"ℹ️ {q.text}",
                    reply_markup=keyboards.info_keyboard(show_back=show_back),
                )
            return
        except Exception:
            # If edit fails (e.g. message too old), fall through to send new
            pass

    # Send new message
    msg_target = target if isinstance(target, Message) else target.message

    if q.q_type == "single":
        await msg_target.answer(
            f"❓ {q.text}",
            reply_markup=keyboards.single_option_keyboard(q.options, show_back=show_back),
        )
    elif q.q_type == "multi":
        await state.update_data(multi_selected=[])
        await msg_target.answer(
            f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_MULTI_HINT}",
            reply_markup=keyboards.multi_option_keyboard(q.options, show_back=show_back),
        )
    elif q.q_type == "text":
        await msg_target.answer(f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_TEXT_HINT}")
    elif q.q_type == "info":
        await msg_target.answer(
            f"ℹ️ {q.text}",
            reply_markup=keyboards.info_keyboard(show_back=show_back),
        )


# --- Back button ---
@router.callback_query(F.data == "q_back", BookingFSM.answering_questionnaire)
async def on_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    history: list = data.get("question_history", [])

    if not history:
        await callback.answer("Это первый вопрос")
        return

    # Pop previous question from history
    prev_q_id = history.pop()
    answers: dict = data.get("questionnaire_answers", {})
    answers.pop(prev_q_id, None)  # Remove the answer for that question

    await state.update_data(
        current_question_id=prev_q_id,
        question_history=history,
        questionnaire_answers=answers,
        multi_selected=[],
    )

    await callback.answer()
    await _show_question(callback, state, edit=True)


# --- Single answer ---
@router.callback_query(F.data.startswith("answer:"), BookingFSM.answering_questionnaire)
async def on_single_answer(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":", 1)[1])
    data = await state.get_data()
    q_id = data.get("current_question_id")
    phase = data.get("questionnaire_phase", "basic")
    engine = _get_engine(QUESTIONNAIRE_MAP[phase])
    q = engine.questions.get(q_id)
    answer_value = q.options[idx] if q and idx < len(q.options) else str(idx)

    # Save answer and push current question to history
    answers = data.get("questionnaire_answers", {})
    answers[q_id] = answer_value
    history: list = data.get("question_history", [])
    history.append(q_id)
    await state.update_data(questionnaire_answers=answers, question_history=history)

    await callback.answer()
    await _advance(callback, state, answer_value)


# --- Multi answer ---
@router.callback_query(F.data.startswith("multi:"), BookingFSM.answering_questionnaire)
async def on_multi_toggle(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":", 1)[1])
    data = await state.get_data()
    q_id = data.get("current_question_id")
    phase = data.get("questionnaire_phase", "basic")
    engine = _get_engine(QUESTIONNAIRE_MAP[phase])
    q = engine.questions.get(q_id)
    option = q.options[idx] if q and idx < len(q.options) else str(idx)

    selected = set(data.get("multi_selected", []))
    if option in selected:
        selected.discard(option)
    else:
        selected.add(option)
    await state.update_data(multi_selected=list(selected))

    history: list = data.get("question_history", [])
    show_back = len(history) > 0

    if q:
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.multi_option_keyboard(q.options, selected, show_back=show_back)
        )
    await callback.answer()


@router.callback_query(F.data == "multi_done", BookingFSM.answering_questionnaire)
async def on_multi_done(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    q_id = data.get("current_question_id")
    selected = data.get("multi_selected", [])
    answer_value = ", ".join(selected) if selected else "—"

    answers = data.get("questionnaire_answers", {})
    answers[q_id] = answer_value
    history: list = data.get("question_history", [])
    history.append(q_id)
    await state.update_data(questionnaire_answers=answers, multi_selected=[], question_history=history)

    await callback.answer()
    await _advance(callback, state, answer_value)


# --- Text answer ---
@router.message(BookingFSM.answering_questionnaire)
async def on_text_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    q_id = data.get("current_question_id")
    answer_value = message.text.strip() if message.text else "—"

    answers = data.get("questionnaire_answers", {})
    answers[q_id] = answer_value
    history: list = data.get("question_history", [])
    history.append(q_id)
    await state.update_data(questionnaire_answers=answers, question_history=history)

    # Text answers can't be edited (user typed a message), send new
    await _advance(message, state, answer_value)


# --- Info screen ---
@router.callback_query(F.data == "info_next", BookingFSM.answering_questionnaire)
async def on_info_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    q_id = data.get("current_question_id")
    history: list = data.get("question_history", [])
    history.append(q_id)
    await state.update_data(question_history=history)

    await callback.answer()
    await _finish_phase(callback, state)


# --- Navigation helpers ---

async def _advance(target: Message | CallbackQuery, state: FSMContext, answer: str):
    data = await state.get_data()
    phase = data.get("questionnaire_phase", "basic")
    q_id = data.get("current_question_id")
    answers = data.get("questionnaire_answers", {})

    engine = _get_engine(QUESTIONNAIRE_MAP[phase])
    next_q = engine.get_next_question(q_id, answer, answers)

    if next_q:
        await state.update_data(current_question_id=next_q.id)
        # Use edit for callback-based navigation
        edit = isinstance(target, CallbackQuery)
        await _show_question(target, state, edit=edit)
    else:
        await _finish_phase(target, state)


async def _finish_phase(target: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phase = data.get("questionnaire_phase", "basic")
    gender = data.get("questionnaire_answers", {}).get("q_gender", "")

    msg_target = target if isinstance(target, Message) else target.message

    if phase == "basic":
        # After basic questionnaire, start ayurved based on gender
        if gender == "Мужчина":
            next_phase = "ayurved_m"
        else:
            next_phase = "ayurved_j"
        await state.update_data(
            questionnaire_phase=next_phase,
            current_question_id=None,
            question_history=[],  # Reset history for new phase
        )
        await msg_target.answer(f"📝 Переходим к аюрвед-опроснику...")
        await _show_question(msg_target, state, edit=False)
    else:
        # All questionnaires done -> photos
        await msg_target.answer(texts.QUESTIONNAIRE_DONE, parse_mode="HTML")
        await state.set_state(BookingFSM.uploading_photos)
        await msg_target.answer(
            texts.UPLOAD_PHOTOS,
            parse_mode="HTML",
            reply_markup=keyboards.photos_keyboard(),
        )
