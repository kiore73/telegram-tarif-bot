"""Photo upload handler.

Photos are saved to disk immediately but DB records are deferred
until the booking is created (to avoid FK violations).
File IDs are stored in FSM state.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.slot_service import SlotService
from config.settings import settings

import aiofiles
from pathlib import Path

router = Router()

MAX_PHOTOS = 20


@router.message(BookingFSM.uploading_photos, F.photo)
async def on_photo(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_db_id = data.get("user_db_id", 0)
    photo_count = data.get("photo_count", 0)
    saved_photos: list = data.get("saved_photos", [])

    if photo_count >= MAX_PHOTOS:
        await message.answer(texts.PHOTO_LIMIT, parse_mode="HTML")
        return

    # Get the largest photo
    photo = message.photo[-1]

    # Download file to disk
    bot = message.bot
    file = await bot.get_file(photo.file_id)
    file_data = await bot.download_file(file.file_path)

    filename = f"photo_{photo_count + 1}.jpg"
    folder = Path(settings.UPLOAD_DIR) / str(user_db_id) / "pending"
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file_data.read())

    # Track in FSM state (NOT in DB yet)
    saved_photos.append({
        "file_path": str(file_path),
        "telegram_file_id": photo.file_id,
    })

    photo_count += 1
    await state.update_data(photo_count=photo_count, saved_photos=saved_photos)
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
