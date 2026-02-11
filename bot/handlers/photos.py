"""Photo upload handler."""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.photo_service import PhotoService
from bot.services.slot_service import SlotService

router = Router()

MAX_PHOTOS = 20


@router.message(BookingFSM.uploading_photos, F.photo)
async def on_photo(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    booking_id = data.get("booking_id")
    user_db_id = data.get("user_db_id")
    photo_count = data.get("photo_count", 0)

    if photo_count >= MAX_PHOTOS:
        await message.answer(texts.PHOTO_LIMIT, parse_mode="HTML")
        return

    # Get the largest photo
    photo = message.photo[-1]

    # Download file
    bot = message.bot
    file = await bot.get_file(photo.file_id)
    file_data = await bot.download_file(file.file_path)

    svc = PhotoService(session)
    # We may not have booking_id yet; store temporarily
    temp_booking_id = booking_id or 0
    await svc.save_photo(
        booking_id=temp_booking_id,
        user_id=user_db_id or 0,
        file_data=file_data.read(),
        filename=f"photo_{photo_count + 1}.jpg",
        telegram_file_id=photo.file_id,
    )

    photo_count += 1
    await state.update_data(photo_count=photo_count)
    await message.answer(
        texts.PHOTO_RECEIVED.format(num=photo_count),
        reply_markup=keyboards.photos_keyboard(),
    )


@router.callback_query(F.data == "photos_done", BookingFSM.uploading_photos)
async def on_photos_done(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    await _go_to_slots(callback.message, state, session)


@router.callback_query(F.data == "photos_skip", BookingFSM.uploading_photos)
async def on_photos_skip(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    await _go_to_slots(callback.message, state, session)


async def _go_to_slots(message: Message, state: FSMContext, session: AsyncSession):
    slot_svc = SlotService(session)
    available = await slot_svc.get_available_slots()

    if not available:
        await message.answer(texts.NO_SLOTS, parse_mode="HTML")
        return

    await state.set_state(BookingFSM.choosing_slot)
    await message.answer(
        texts.CHOOSE_SLOT,
        parse_mode="HTML",
        reply_markup=keyboards.slot_keyboard(available),
    )
