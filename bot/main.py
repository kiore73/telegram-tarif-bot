"""Entry point — Dispatcher, middlewares, routers."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.settings import settings
from bot.middlewares import DbSessionMiddleware
from bot.handlers import start, payment, intake, questionnaire, photos, slots, admin
from bot.handlers import gender


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
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

    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
