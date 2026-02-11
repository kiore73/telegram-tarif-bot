"""Admin panel handler."""

from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from bot import texts, keyboards
from bot.states.user_states import AdminFSM
from bot.services.slot_service import SlotService
from config.settings import settings
from db.models import Booking, User

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа.")
        return
    await state.set_state(AdminFSM.main_menu)
    await message.answer(texts.ADMIN_MENU, parse_mode="HTML", reply_markup=keyboards.admin_menu_keyboard())


# --- Menu navigation ---

@router.callback_query(F.data == "admin:menu")
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminFSM.main_menu)
    await callback.message.edit_text(texts.ADMIN_MENU, parse_mode="HTML", reply_markup=keyboards.admin_menu_keyboard())
    await callback.answer()


# --- Create slot flow ---

@router.callback_query(F.data == "admin:create_slot")
async def start_create_slot(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminFSM.entering_slot_date)
    await callback.message.edit_text(texts.ADMIN_ENTER_DATE, parse_mode="HTML")
    await callback.answer()


@router.message(AdminFSM.entering_slot_date)
async def enter_slot_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        await message.answer(texts.ADMIN_INVALID_DATE, parse_mode="HTML")
        return
    await state.update_data(slot_date=str(date))
    await state.set_state(AdminFSM.entering_slot_time)
    await message.answer(texts.ADMIN_ENTER_TIME, parse_mode="HTML")


@router.message(AdminFSM.entering_slot_time)
async def enter_slot_time(message: Message, state: FSMContext):
    try:
        time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except (ValueError, AttributeError):
        await message.answer(texts.ADMIN_INVALID_TIME, parse_mode="HTML")
        return
    await state.update_data(slot_time=str(time))
    await state.set_state(AdminFSM.entering_slot_duration)
    await message.answer(texts.ADMIN_ENTER_DURATION, parse_mode="HTML")


@router.message(AdminFSM.entering_slot_duration)
async def enter_slot_duration(message: Message, state: FSMContext, session: AsyncSession):
    try:
        duration = int(message.text.strip())
        if not 30 <= duration <= 60:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        await message.answer(texts.ADMIN_INVALID_DURATION, parse_mode="HTML")
        return

    data = await state.get_data()
    date = datetime.strptime(data["slot_date"], "%Y-%m-%d").date()
    time = datetime.strptime(data["slot_time"], "%H:%M:%S").time()
    dt = datetime.combine(date, time)

    # Check not in past (UTC)
    if dt < datetime.now(timezone.utc).replace(tzinfo=None):
        await message.answer(texts.ADMIN_PAST_SLOT, parse_mode="HTML")
        return

    slot_svc = SlotService(session)
    slot = await slot_svc.create_slot(dt, duration, message.from_user.id)

    await message.answer(
        texts.ADMIN_SLOT_CREATED.format(
            date=date.strftime("%d.%m.%Y"),
            time=time.strftime("%H:%M"),
            duration=duration,
        ),
        parse_mode="HTML",
    )
    await state.set_state(AdminFSM.main_menu)
    await message.answer(texts.ADMIN_MENU, parse_mode="HTML", reply_markup=keyboards.admin_menu_keyboard())


# --- Delete slot ---

@router.callback_query(F.data == "admin:delete_slot")
async def start_delete_slot(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not _is_admin(callback.from_user.id):
        return
    slot_svc = SlotService(session)
    slots = await slot_svc.get_future_slots()
    if not slots:
        await callback.answer(texts.ADMIN_NO_SLOTS, show_alert=True)
        return
    await callback.message.edit_text(
        "Выберите слот для удаления:",
        reply_markup=keyboards.admin_slot_delete_keyboard(slots),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_del_slot:"))
async def confirm_delete_slot(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not _is_admin(callback.from_user.id):
        return
    slot_id = int(callback.data.split(":")[1])
    slot_svc = SlotService(session)
    ok = await slot_svc.soft_delete_slot(slot_id)
    if ok:
        await callback.answer(texts.ADMIN_SLOT_DELETED, show_alert=True)
    else:
        await callback.answer("Не удалось удалить слот (уже забронирован).", show_alert=True)
    # Refresh slot list
    await start_delete_slot(callback, state, session)


# --- List slots ---

@router.callback_query(F.data == "admin:list_slots")
async def list_slots(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not _is_admin(callback.from_user.id):
        return
    slot_svc = SlotService(session)
    slots = await slot_svc.get_available_slots()
    if not slots:
        await callback.answer("Нет свободных слотов.", show_alert=True)
        return
    lines = ["📋 <b>Свободные слоты:</b>\n"]
    for s in slots:
        lines.append(f"  • {s.datetime_utc.strftime('%d.%m.%Y %H:%M')} — {s.duration_minutes} мин")
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=keyboards.admin_menu_keyboard())
    await callback.answer()


# --- History ---

@router.callback_query(F.data == "admin:history")
async def booking_history(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not _is_admin(callback.from_user.id):
        return
    result = await session.execute(
        select(Booking).order_by(desc(Booking.created_at)).limit(20)
    )
    bookings = list(result.scalars().all())
    if not bookings:
        await callback.answer("Записей пока нет.", show_alert=True)
        return

    lines = ["📊 <b>Последние записи:</b>\n"]
    for b in bookings:
        user = await session.get(User, b.user_id)
        name = f"{user.first_name} {user.last_name}" if user else "—"
        lines.append(
            f"  • {b.created_at.strftime('%d.%m.%Y')} | {name} | {b.tariff.value} | {b.status.value}"
        )
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=keyboards.admin_menu_keyboard())
    await callback.answer()
