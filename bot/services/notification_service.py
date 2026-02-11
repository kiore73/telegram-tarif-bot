"""Send notifications to admin(s) about new bookings."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram import Bot

from config.settings import settings

if TYPE_CHECKING:
    from db.models import Booking, Photo, QuestionnaireAnswer, User


class NotificationService:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def notify_new_booking(
        self,
        user: User,
        booking: Booking,
        answers: list[QuestionnaireAnswer],
        photos: list[Photo],
    ) -> None:
        tariff_labels = {
            "basic": "Базовый",
            "extended": "Сопровождение",
            "repeat": "Повторная",
            "lite": "Лайт",
        }

        text_parts = [
            "📋 <b>Новая запись на консультацию</b>\n",
            f"👤 {user.first_name} {user.last_name}",
            f"🎂 Возраст: {user.age}",
        ]
        if user.weight:
            text_parts.append(f"⚖️ Вес: {user.weight} кг")
        text_parts.append(
            f"📦 Тариф: {tariff_labels.get(booking.tariff.value, booking.tariff.value)}"
        )
        text_parts.append(
            f"💳 Оплата: подтверждена (Payment #{booking.payment_id})"
        )
        if booking.slot:
            text_parts.append(
                f"📅 Слот: {booking.slot.datetime_utc.strftime('%d.%m.%Y %H:%M')} UTC"
            )
        if booking.conference_link:
            text_parts.append(f"🔗 Конференция: {booking.conference_link}")

        # Questionnaire summary
        if answers:
            text_parts.append("\n📝 <b>Ответы на опросник:</b>")
            for a in answers:
                text_parts.append(f"  • {a.question_text}: <i>{a.answer}</i>")

        message = "\n".join(text_parts)

        # Send to each admin; truncate if too long
        for admin_id in settings.ADMIN_IDS:
            try:
                # Telegram max message 4096 chars
                for chunk_start in range(0, len(message), 4000):
                    await self.bot.send_message(
                        admin_id,
                        message[chunk_start: chunk_start + 4000],
                        parse_mode="HTML",
                    )
                # Forward photos
                for photo in photos:
                    if photo.telegram_file_id:
                        await self.bot.send_photo(admin_id, photo.telegram_file_id)
            except Exception as e:
                logging.error(f"Failed to notify admin {admin_id}: {e}")
