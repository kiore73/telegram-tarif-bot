"""Entry point — Dispatcher, middlewares, routers + webhook server."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

from config.settings import settings
from bot.middlewares import DbSessionMiddleware
from bot.handlers import start, payment, intake, questionnaire, photos, slots, admin
from bot.handlers import gender
from bot.webhook_server import create_webhook_app, set_bot_and_dp


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # Auto-create database tables if they don't exist
    from db.base import engine, Base
    from db import models  # noqa: F401 — register all models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Middlewares
    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())

    # Routers
    dp.include_router(admin.router)    # admin first (higher priority)
    dp.include_router(start.router)
    dp.include_router(payment.router)
    dp.include_router(intake.router)
    dp.include_router(gender.router)
    dp.include_router(questionnaire.router)
    dp.include_router(photos.router)
    dp.include_router(slots.router)

    # Share bot and dispatcher with webhook handler
    set_bot_and_dp(bot, dp)

    # Start webhook server for YooKassa notifications
    webhook_app = create_webhook_app()
    webhook_port = int(getattr(settings, "WEBHOOK_PORT", 8080))
    runner = web.AppRunner(webhook_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", webhook_port)
    await site.start()
    logger.info(f"YooKassa webhook server started on port {webhook_port}")

    # Start bot polling
    logger.info("Bot starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
