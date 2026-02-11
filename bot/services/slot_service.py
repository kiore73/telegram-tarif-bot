"""Slot CRUD service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Slot


class SlotService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_slot(
        self, dt_utc: datetime, duration: int, admin_id: int
    ) -> Slot:
        slot = Slot(
            datetime_utc=dt_utc,
            duration_minutes=duration,
            created_by_admin_id=admin_id,
        )
        self.session.add(slot)
        await self.session.commit()
        await self.session.refresh(slot)
        return slot

    async def get_available_slots(self) -> List[Slot]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stmt = (
            select(Slot)
            .where(
                Slot.is_booked.is_(False),
                Slot.is_deleted.is_(False),
                Slot.datetime_utc > now,
            )
            .order_by(Slot.datetime_utc)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_slot_by_id(self, slot_id: int) -> Optional[Slot]:
        return await self.session.get(Slot, slot_id)

    async def book_slot(self, slot_id: int) -> Optional[Slot]:
        slot = await self.get_slot_by_id(slot_id)
        if slot and not slot.is_booked and not slot.is_deleted:
            slot.is_booked = True
            await self.session.commit()
            return slot
        return None

    async def soft_delete_slot(self, slot_id: int) -> bool:
        slot = await self.get_slot_by_id(slot_id)
        if slot and not slot.is_booked:
            slot.is_deleted = True
            await self.session.commit()
            return True
        return False

    async def get_future_slots(self) -> List[Slot]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stmt = (
            select(Slot)
            .where(Slot.is_deleted.is_(False), Slot.datetime_utc > now)
            .order_by(Slot.datetime_utc)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_slots_for_date(self, date) -> List[Slot]:
        """Get all non-deleted slots for a specific date."""
        from datetime import time as dt_time
        day_start = datetime.combine(date, dt_time.min)
        day_end = datetime.combine(date, dt_time.max)
        stmt = (
            select(Slot)
            .where(
                Slot.is_deleted.is_(False),
                Slot.datetime_utc >= day_start,
                Slot.datetime_utc <= day_end,
            )
            .order_by(Slot.datetime_utc)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
