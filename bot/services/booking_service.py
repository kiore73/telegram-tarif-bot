"""Booking orchestration — creates the final booking record."""

from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Booking, BookingStatus, TariffType, Slot
from bot.services.google_meet import GoogleMeetService

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_booking(
        self,
        user_id: int,
        payment_id: int,
        slot_id: int,
        tariff: TariffType,
    ) -> Booking:
        # 1. Get slot info for meeting details
        slot = await self.session.get(Slot, slot_id)
        if not slot:
            raise ValueError(f"Slot {slot_id} not found")

        # 2. Try to generate Google Meet link
        conference_link = None
        try:
            meet_service = GoogleMeetService()
            # Summary: "Consultation - [Tariff]" or similar
            summary = f"Консультация ({tariff.value})"
            description = f"Онлайн-консультация. Тариф: {tariff.value}"
            
            link_obj = meet_service.create_meeting(
                summary=summary,
                description=description,
                start_time=slot.datetime_utc,
                duration_minutes=slot.duration_minutes
            )
            if link_obj:
                conference_link = link_obj.url
        except Exception as e:
            logger.error(f"Failed to generate Google Meet link: {e}")

        # Fallback if generation failed
        if not conference_link:
            conference_link = "Ссылка будет отправлена администратором вручную"

        booking = Booking(
            user_id=user_id,
            payment_id=payment_id,
            slot_id=slot_id,
            tariff=tariff,
            status=BookingStatus.active,
            conference_link=conference_link,
        )
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def get_booking(self, booking_id: int) -> Optional[Booking]:
        return await self.session.get(Booking, booking_id)
