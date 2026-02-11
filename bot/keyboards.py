"""All inline keyboards for the bot."""

from __future__ import annotations

from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def tariff_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💚 Базовый — 8 000 ₽", callback_data="tariff:basic")],
        [InlineKeyboardButton(text="💎 Сопровождение — 20 000 ₽", callback_data="tariff:extended")],
        [InlineKeyboardButton(text="🔄 Повторная — 5 000 ₽", callback_data="tariff:repeat")],
        [InlineKeyboardButton(text="🌿 Лайт — 3 000 ₽", callback_data="tariff:lite")],
    ])


def payment_check_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
        [InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_payment")],
    ])


def gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужчина", callback_data="gender:Мужчина")],
        [InlineKeyboardButton(text="Женщина", callback_data="gender:Женщина")],
    ])


def single_option_keyboard(options: List[str], prefix: str = "answer", show_back: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"{prefix}:{i}")]
        for i, opt in enumerate(options)
    ]
    if show_back:
        buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="q_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def multi_option_keyboard(
    options: List[str],
    selected: set[str] | None = None,
    prefix: str = "multi",
    show_back: bool = False,
) -> InlineKeyboardMarkup:
    selected = selected or set()
    buttons = []
    for i, opt in enumerate(options):
        mark = "☑" if opt in selected else "☐"
        buttons.append(
            [InlineKeyboardButton(text=f"{mark} {opt}", callback_data=f"{prefix}:{i}")]
        )
    buttons.append([InlineKeyboardButton(text="✅ Готово", callback_data="multi_done")])
    if show_back:
        buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="q_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def info_keyboard(show_back: bool = False) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="➡️ Далее", callback_data="info_next")]]
    if show_back:
        buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="q_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def photos_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Готово", callback_data="photos_done")],
        [InlineKeyboardButton(text="⏩ Пропустить", callback_data="photos_skip")],
    ])


def slot_keyboard(slots) -> InlineKeyboardMarkup:
    buttons = []
    for slot in slots:
        label = slot.datetime_utc.strftime("%d.%m.%Y %H:%M") + f" ({slot.duration_minutes} мин)"
        buttons.append(
            [InlineKeyboardButton(text=label, callback_data=f"slot:{slot.id}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_booking_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")],
    ])


# Admin keyboards

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Создать слот", callback_data="admin:create_slot")],
        [InlineKeyboardButton(text="🗑 Удалить слот", callback_data="admin:delete_slot")],
        [InlineKeyboardButton(text="📋 Свободные слоты", callback_data="admin:list_slots")],
        [InlineKeyboardButton(text="📊 История записей", callback_data="admin:history")],
    ])


def admin_slot_delete_keyboard(slots) -> InlineKeyboardMarkup:
    buttons = []
    for slot in slots:
        status = "🟢" if not slot.is_booked else "🔴"
        label = f"{status} {slot.datetime_utc.strftime('%d.%m.%Y %H:%M')}"
        buttons.append(
            [InlineKeyboardButton(text=label, callback_data=f"admin_del_slot:{slot.id}")]
        )
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
