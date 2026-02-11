"""Cron script for cleaning up old uploaded photos."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot.services.photo_service import PhotoService


if __name__ == "__main__":
    removed = PhotoService.cleanup_old_photos()
    print(f"Removed {removed} old photo(s).")
