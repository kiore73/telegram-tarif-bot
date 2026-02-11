"""Intake handler — collects name, surname, age, weight."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from db.models import User

router = Router()


@router.message(BookingFSM.entering_first_name)
async def enter_first_name(message: Message, state: FSMContext, session: AsyncSession):
    name = message.text.strip() if message.text else ""
    if not name or len(name) > 100:
        await message.answer("Введите корректное имя (до 100 символов).")
        return
    await state.update_data(first_name=name)
    await state.set_state(BookingFSM.entering_last_name)
    await message.answer(texts.ENTER_LAST_NAME, parse_mode="HTML")


@router.message(BookingFSM.entering_last_name)
async def enter_last_name(message: Message, state: FSMContext, session: AsyncSession):
    name = message.text.strip() if message.text else ""
    if not name or len(name) > 100:
        await message.answer("Введите корректную фамилию (до 100 символов).")
        return
    await state.update_data(last_name=name)
    await state.set_state(BookingFSM.entering_age)
    await message.answer(texts.ENTER_AGE, parse_mode="HTML")


@router.message(BookingFSM.entering_age)
async def enter_age(message: Message, state: FSMContext, session: AsyncSession):
    try:
        age = int(message.text.strip())
        if not 1 <= age <= 120:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        await message.answer(texts.INVALID_AGE, parse_mode="HTML")
        return

    await state.update_data(age=age)

    data = await state.get_data()
    tariff = data.get("tariff")

    if tariff == "repeat":
        # Repeat tariff: skip weight, go directly to photos
        await _save_user_data(session, data, age=age)
        await state.set_state(BookingFSM.uploading_photos)
        await message.answer(texts.UPLOAD_PHOTOS, parse_mode="HTML", reply_markup=keyboards.photos_keyboard())
    else:
        # basic, extended, lite: ask for weight
        await state.set_state(BookingFSM.entering_weight)
        await message.answer(texts.ENTER_WEIGHT, parse_mode="HTML")


@router.message(BookingFSM.entering_weight)
async def enter_weight(message: Message, state: FSMContext, session: AsyncSession):
    try:
        weight = float(message.text.strip().replace(",", "."))
        if not 20 <= weight <= 300:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        await message.answer(texts.INVALID_WEIGHT, parse_mode="HTML")
        return

    await state.update_data(weight=weight)
    data = await state.get_data()
    await _save_user_data(session, data, weight=weight)

    tariff = data.get("tariff")

    if tariff == "lite":
        # Lite: choose gender -> ayurved questionnaire
        await state.set_state(BookingFSM.choosing_gender)
        await message.answer(texts.CHOOSE_GENDER, parse_mode="HTML", reply_markup=keyboards.gender_keyboard())
    else:
        # Basic / Extended: start questionnaires
        await state.set_state(BookingFSM.answering_questionnaire)
        await state.update_data(
            questionnaire_phase="basic",
            questionnaire_index=0,
            questionnaire_answers={},
            multi_selected=[],
            question_history=[],
        )
        # Import here to avoid circular
        from bot.handlers.questionnaire import _show_question
        await _show_question(message, state)


async def _save_user_data(session: AsyncSession, data: dict, age: int = 0, weight: float = 0):
    user_db_id = data.get("user_db_id")
    user = await session.get(User, user_db_id)
    if user:
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.age = data.get("age", age)
        if weight:
            user.weight = weight
        elif data.get("weight"):
            user.weight = data["weight"]
        await session.commit()
