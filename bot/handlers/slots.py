"""Slot selection + booking confirmation handler."""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.slot_service import SlotService
from bot.services.booking_service import BookingService
from bot.services.notification_service import NotificationService
from db.models import User, QuestionnaireAnswer, Photo, TariffType

router = Router()


@router.callback_query(F.data.startswith("slot:"), BookingFSM.choosing_slot)
async def on_slot_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    slot_id = int(callback.data.split(":")[1])
    data = await state.get_data()

    slot_svc = SlotService(session)
    slot = await slot_svc.get_slot_by_id(slot_id)

    if not slot or slot.is_booked or slot.is_deleted:
        await callback.answer("Этот слот уже занят. Выберите другой.", show_alert=True)
        return

    await state.update_data(selected_slot_id=slot_id)

    dt = slot.datetime_utc
    await callback.message.edit_text(
        f"Вы выбрали:\n📅 {dt.strftime('%d.%m.%Y')}\n⏰ {dt.strftime('%H:%M')}\n⏱ {slot.duration_minutes} мин\n\nПодтвердить?",
        reply_markup=keyboards.confirm_booking_keyboard(),
    )
    await state.set_state(BookingFSM.confirming_booking)
    await callback.answer()


@router.callback_query(F.data == "confirm_booking", BookingFSM.confirming_booking)
async def on_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    slot_id = data.get("selected_slot_id")
    payment_id = data.get("payment_id")
    user_db_id = data.get("user_db_id")
    tariff = data.get("tariff")

    # Book the slot
    slot_svc = SlotService(session)
    slot = await slot_svc.book_slot(slot_id)
    if not slot:
        await callback.answer("Слот уже занят!", show_alert=True)
        return

    # Create booking
    booking_svc = BookingService(session)
    booking = await booking_svc.create_booking(
        user_id=user_db_id,
        payment_id=payment_id,
        slot_id=slot_id,
        tariff=TariffType(tariff),
    )

    await state.update_data(booking_id=booking.id)

    # Save questionnaire answers to DB
    answers_dict = data.get("questionnaire_answers", {})
    phase = data.get("questionnaire_phase", "basic")
    from bot.services.questionnaire_engine import QuestionnaireEngine
    from bot.handlers.questionnaire import QUESTIONNAIRE_MAP, _get_engine

    for q_id, answer_text in answers_dict.items():
        # Determine questionnaire type
        q_type = "basic"
        for key, md_name in QUESTIONNAIRE_MAP.items():
            engine = _get_engine(md_name)
            if q_id in engine.questions:
                q_type = key
                q = engine.questions[q_id]
                break
        else:
            q = None

        qa = QuestionnaireAnswer(
            booking_id=booking.id,
            questionnaire_type=q_type,
            question_id=q_id,
            question_text=q.text if q else q_id,
            answer=answer_text,
        )
        session.add(qa)

    await session.commit()

    # Save photos to DB now that booking exists
    saved_photos = data.get("saved_photos", [])
    for p in saved_photos:
        photo_record = Photo(
            booking_id=booking.id,
            file_path=p["file_path"],
            telegram_file_id=p.get("telegram_file_id"),
        )
        session.add(photo_record)
    if saved_photos:
        await session.commit()

    # Load answers and photos for notification
    user = await session.get(User, user_db_id)
    answers_result = await session.execute(
        select(QuestionnaireAnswer).where(QuestionnaireAnswer.booking_id == booking.id)
    )
    answers_list = list(answers_result.scalars().all())

    photos_result = await session.execute(
        select(Photo).where(Photo.booking_id == booking.id)
    )
    photos_list = list(photos_result.scalars().all())

    # Notify admins
    notifier = NotificationService(callback.bot)
    await notifier.notify_new_booking(user, booking, answers_list, photos_list)

    # Confirm to user
    dt = slot.datetime_utc
    await callback.message.edit_text(
        texts.BOOKING_CONFIRMED.format(
            date=dt.strftime("%d.%m.%Y"),
            time=dt.strftime("%H:%M"),
            duration=slot.duration_minutes,
            link=booking.conference_link or "будет отправлена позже",
        ),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer("Запись подтверждена! ✅")


@router.callback_query(F.data == "cancel_booking", BookingFSM.confirming_booking)
async def on_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Запись отменена. Используйте /start чтобы начать заново.")
    await callback.answer()
