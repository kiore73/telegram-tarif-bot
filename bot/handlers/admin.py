"""Admin panel handler — calendar-based slot management."""

from datetime import datetime, timezone, date as dt_date

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

DEFAULT_SLOT_DURATION = 60  # minutes


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


# ═══════════════════════════════════════════════════
#  CREATE SLOT — Calendar → Time Grid → Auto-create
# ═══════════════════════════════════════════════════

@router.callback_query(F.data == "admin:create_slot")
async def start_create_slot(callback: CallbackQuery, state: FSMContext):
    """Show inline calendar for current month."""
    if not _is_admin(callback.from_user.id):
        return
    now = datetime.now()
    await state.set_state(AdminFSM.entering_slot_date)
    await callback.message.edit_text(
        "Выберите дату для добавления слота:",
        reply_markup=keyboards.calendar_keyboard(now.year, now.month),
    )
    await callback.answer()


# Calendar navigation (< and >)
@router.callback_query(F.data.startswith("cal:"), AdminFSM.entering_slot_date)
async def calendar_nav(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    if len(parts) < 3 or parts[1] == "ignore":
        await callback.answer()
        return
    year, month = int(parts[1]), int(parts[2])
    await callback.message.edit_text(
        "Выберите дату для добавления слота:",
        reply_markup=keyboards.calendar_keyboard(year, month),
    )
    await callback.answer()


# Day selected → show time grid
@router.callback_query(F.data.startswith("cal_day:"), AdminFSM.entering_slot_date)
async def on_day_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    _, year, month, day = callback.data.split(":")
    year, month, day = int(year), int(month), int(day)
    selected_date = dt_date(year, month, day)

    # Check not in the past
    today = datetime.now().date()
    if selected_date < today:
        await callback.answer("❌ Нельзя выбрать прошедшую дату", show_alert=True)
        return

    # Find existing slots for this date to mark taken hours
    slot_svc = SlotService(session)
    existing_slots = await slot_svc.get_slots_for_date(selected_date)
    taken_hours = {s.datetime_utc.hour for s in existing_slots}

    date_str = selected_date.strftime("%Y-%m-%d")
    await state.update_data(slot_date=date_str)
    await state.set_state(AdminFSM.entering_slot_time)

    # Format the date nicely for the header
    display_date = selected_date.strftime("%d %B %Y")
    await callback.message.edit_text(
        f"Выбрана дата: <b>{display_date}</b>. Теперь выберите время:",
        parse_mode="HTML",
        reply_markup=keyboards.time_grid_keyboard(date_str, taken_hours),
    )
    await callback.answer()


# Time selected → create slot immediately
@router.callback_query(F.data.startswith("cal_time:"), AdminFSM.entering_slot_time)
async def on_time_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    parts = callback.data.split(":")
    date_str = parts[1]
    hour = int(parts[2])

    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    from datetime import time as dt_time
    dt = datetime.combine(selected_date, dt_time(hour, 0))

    # Check not in past
    if dt < datetime.now():
        await callback.answer("❌ Это время уже прошло", show_alert=True)
        return

    # Create slot
    slot_svc = SlotService(session)
    slot = await slot_svc.create_slot(dt, DEFAULT_SLOT_DURATION, callback.from_user.id)

    await callback.answer(
        f"✅ Слот создан: {selected_date.strftime('%d.%m.%Y')} {hour:02d}:00 ({DEFAULT_SLOT_DURATION} мин)",
        show_alert=True,
    )

    # Refresh time grid — show updated taken hours
    existing_slots = await slot_svc.get_slots_for_date(selected_date)
    taken_hours = {s.datetime_utc.hour for s in existing_slots}

    display_date = selected_date.strftime("%d %B %Y")
    await callback.message.edit_text(
        f"Выбрана дата: <b>{display_date}</b>. Теперь выберите время:",
        parse_mode="HTML",
        reply_markup=keyboards.time_grid_keyboard(date_str, taken_hours),
    )


# Ignore clicks on empty/header cells
@router.callback_query(F.data == "cal:ignore")
async def ignore_calendar_click(callback: CallbackQuery):
    await callback.answer()


# ═══════════════════════════════════════════════════
#  DELETE SLOT
# ═══════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════
#  LIST SLOTS
# ═══════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════
#  BOOKING HISTORY
# ═══════════════════════════════════════════════════

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
