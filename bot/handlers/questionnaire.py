"""Questionnaire handler — drives Q&A using QuestionnaireEngine."""

from __future__ import annotations

import os
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.questionnaire_engine import QuestionnaireEngine

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


async def send_question(target: Message | CallbackQuery, state: FSMContext) -> None:
    """Send the current question to the user."""
    data = await state.get_data()
    phase = data.get("questionnaire_phase", "basic")
    q_id = data.get("current_question_id")
    answers = data.get("questionnaire_answers", {})

    engine = _get_engine(QUESTIONNAIRE_MAP[phase])

    if not q_id:
        q = engine.get_first_question()
    else:
        q = engine.questions.get(q_id)

    if not q:
        await _finish_phase(target, state)
        return

    await state.update_data(current_question_id=q.id)

    msg_target = target if isinstance(target, Message) else target.message

    if q.q_type == "single":
        await msg_target.answer(
            f"❓ {q.text}",
            reply_markup=keyboards.single_option_keyboard(q.options),
        )
    elif q.q_type == "multi":
        await state.update_data(multi_selected=[])
        await msg_target.answer(
            f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_MULTI_HINT}",
            reply_markup=keyboards.multi_option_keyboard(q.options),
        )
    elif q.q_type == "text":
        await msg_target.answer(f"❓ {q.text}\n\n{texts.QUESTIONNAIRE_TEXT_HINT}")
    elif q.q_type == "info":
        await msg_target.answer(f"ℹ️ {q.text}", reply_markup=keyboards.info_keyboard())


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

    answers = data.get("questionnaire_answers", {})
    answers[q_id] = answer_value
    await state.update_data(questionnaire_answers=answers)

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

    q_id = data.get("current_question_id")
    phase = data.get("questionnaire_phase", "basic")
    engine = _get_engine(QUESTIONNAIRE_MAP[phase])
    q = engine.questions.get(q_id)
    if q:
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.multi_option_keyboard(q.options, selected)
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
    await state.update_data(questionnaire_answers=answers, multi_selected=[])

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
    await state.update_data(questionnaire_answers=answers)

    await _advance(message, state, answer_value)


# --- Info screen ---
@router.callback_query(F.data == "info_next", BookingFSM.answering_questionnaire)
async def on_info_next(callback: CallbackQuery, state: FSMContext):
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

    if next_q and next_q.q_type != "info":
        await state.update_data(current_question_id=next_q.id)
        await send_question(target, state)
    elif next_q and next_q.q_type == "info":
        # Show info and finish
        msg_target = target if isinstance(target, Message) else target.message
        await msg_target.answer(f"ℹ️ {next_q.text}", reply_markup=keyboards.info_keyboard())
        await state.update_data(current_question_id=next_q.id)
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
        )
        await msg_target.answer(f"📝 Переходим к аюрвед-опроснику...")
        await send_question(msg_target, state)
    else:
        # All questionnaires done -> photos
        await msg_target.answer(texts.QUESTIONNAIRE_DONE, parse_mode="HTML")
        await state.set_state(BookingFSM.uploading_photos)
        await msg_target.answer(
            texts.UPLOAD_PHOTOS,
            parse_mode="HTML",
            reply_markup=keyboards.photos_keyboard(),
        )
