"""Photo saving and cleanup service."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import aiofiles

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from db.models import Photo


class PhotoService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.upload_dir = Path(settings.UPLOAD_DIR)

    async def save_photo(
        self,
        booking_id: int,
        user_id: int,
        file_data: bytes,
        filename: str,
        telegram_file_id: Optional[str] = None,
    ) -> Photo:
        folder = self.upload_dir / str(user_id) / str(booking_id)
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_data)

        photo = Photo(
            booking_id=booking_id,
            file_path=str(file_path),
            telegram_file_id=telegram_file_id,
        )
        self.session.add(photo)
        await self.session.commit()
        await self.session.refresh(photo)
        return photo

    async def get_photos_for_booking(self, booking_id: int) -> list[Photo]:
        stmt = select(Photo).where(Photo.booking_id == booking_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_photos(self, booking_id: int) -> int:
        photos = await self.get_photos_for_booking(booking_id)
        return len(photos)

    @staticmethod
    def cleanup_old_photos(retention_days: int | None = None) -> int:
        """Synchronous cleanup for cron usage."""
        days = retention_days or settings.PHOTO_RETENTION_DAYS
        upload_dir = Path(settings.UPLOAD_DIR)
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        removed = 0
        if not upload_dir.exists():
            return 0
        for f in upload_dir.rglob("*"):
            if f.is_file():
                mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
                if mtime < cutoff:
                    try:
                        f.unlink()
                        removed += 1
                    except OSError as e:
                        logging.warning(f"Cannot remove {f}: {e}")
        return removed
