"""Booking orchestration — creates the final booking record."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Booking, BookingStatus, TariffType


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
        # Generate a placeholder conference link
        conference_link = f"https://telemost.yandex.ru/placeholder-{uuid.uuid4().hex[:8]}"

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
