"""Gender selection handler (for lite tariff)."""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.user_states import BookingFSM
from db.models import User

router = Router()


@router.callback_query(F.data.startswith("gender:"), BookingFSM.choosing_gender)
async def on_gender_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    gender = callback.data.split(":", 1)[1]
    data = await state.get_data()

    # Save gender
    user = await session.get(User, data.get("user_db_id"))
    if user:
        user.gender = gender
        await session.commit()

    # For lite tariff: go to ayurved questionnaire based on gender
    if gender == "Мужчина":
        phase = "ayurved_m"
    else:
        phase = "ayurved_j"

    await state.update_data(
        gender=gender,
        questionnaire_phase=phase,
        current_question_id=None,
        questionnaire_answers={"q_gender": gender},
        multi_selected=[],
        question_history=[],
    )
    await state.set_state(BookingFSM.answering_questionnaire)

    await callback.message.edit_text(f"Пол: <b>{gender}</b>", parse_mode="HTML")
    await callback.answer()

    from bot.handlers.questionnaire import _show_question
    await _show_question(callback, state)
