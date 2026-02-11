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
        [InlineKeyboardButton(
            text="📄 Договор-оферта",
            url="https://telegra.ph/Dogovor-oferta-na-okazanie-uslug-nutriciologii-02-11",
        )],
        [InlineKeyboardButton(
            text="🔒 Согласие на обработку персональных данных",
            url="https://telegra.ph/SOGLASIE-NA-OBRABOTKU-PERSONALNYH-DANNYH-02-11-19",
        )],
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


def calendar_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    """Inline calendar for a given month — looks like a real calendar grid."""
    import calendar

    MONTH_NAMES = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    buttons = []

    # Month/year header with < > navigation
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year -= 1
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1

    buttons.append([
        InlineKeyboardButton(text="<", callback_data=f"cal:{prev_year}:{prev_month}"),
        InlineKeyboardButton(text=f"{MONTH_NAMES[month]} {year}", callback_data="cal:ignore"),
        InlineKeyboardButton(text=">", callback_data=f"cal:{next_year}:{next_month}"),
    ])

    # Day-of-week headers
    buttons.append([
        InlineKeyboardButton(text=d, callback_data="cal:ignore")
        for d in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    ])

    # Day cells
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="cal:ignore"))
            else:
                row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=f"cal_day:{year}:{month}:{day}",
                ))
        buttons.append(row)

    # Back to admin
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def time_grid_keyboard(
    date_str: str,
    taken_hours: set[int] | None = None,
) -> InlineKeyboardMarkup:
    """Time selection grid from 09:00 to 18:00. Taken hours marked with ❌."""
    taken_hours = taken_hours or set()

    hours = list(range(9, 19))  # 09:00 .. 18:00
    buttons = []
    row = []
    for h in hours:
        label = f"{h:02d}:00"
        if h in taken_hours:
            label = f"❌ {label}"
            cb = "cal:ignore"
        else:
            cb = f"cal_time:{date_str}:{h}"
        row.append(InlineKeyboardButton(text=label, callback_data=cb))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ Назад к выбору даты", callback_data="admin:create_slot")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin:menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
