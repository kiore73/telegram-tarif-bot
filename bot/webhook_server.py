"""YooKassa webhook receiver — aiohttp server for payment notifications."""

import hashlib
import hmac
import json
import logging
from typing import Optional

from aiohttp import web
from sqlalchemy import select

from config.settings import settings
from db.base import async_session
from db.models import Payment, PaymentStatus

logger = logging.getLogger(__name__)

# Will be set from main.py
_bot = None
_dp = None


def set_bot_and_dp(bot, dp):
    global _bot, _dp
    _bot = bot
    _dp = dp


async def handle_yookassa_webhook(request: web.Request) -> web.Response:
    """Handle incoming webhook notifications from YooKassa."""
    try:
        body = await request.read()
        data = json.loads(body)
    except Exception:
        logger.warning("Invalid webhook body")
        return web.Response(status=400)

    event_type = data.get("event")
    obj = data.get("object", {})
    yk_payment_id = obj.get("id")
    status = obj.get("status")

    logger.info(f"YooKassa webhook: event={event_type}, payment_id={yk_payment_id}, status={status}")

    if event_type == "payment.succeeded" and status == "succeeded":
        await _handle_payment_succeeded(yk_payment_id, obj)
    elif event_type == "payment.canceled":
        await _handle_payment_cancelled(yk_payment_id)

    # Always respond 200 to acknowledge receipt
    return web.Response(status=200, text="OK")


async def _handle_payment_succeeded(yk_payment_id: str, payment_obj: dict):
    """Payment confirmed — update DB and notify user to continue."""
    if not _bot:
        logger.error("Bot not initialized for webhook handler")
        return

    async with async_session() as session:
        # Find payment by YooKassa ID
        result = await session.execute(
            select(Payment).where(Payment.yookassa_payment_id == yk_payment_id)
        )
        payment = result.scalar_one_or_none()

        if not payment:
            logger.warning(f"Payment not found in DB for YooKassa ID: {yk_payment_id}")
            return

        if payment.status == PaymentStatus.succeeded:
            logger.info(f"Payment {yk_payment_id} already marked as succeeded")
            return

        # Update payment status
        payment.status = PaymentStatus.succeeded
        payment_method = payment_obj.get("payment_method", {})
        payment.payment_method_type = payment_method.get("type", "unknown")
        await session.commit()

        # Get user's telegram_id
        from db.models import User
        user = await session.get(User, payment.user_id)
        if not user:
            logger.error(f"User not found for payment {payment.id}")
            return

        telegram_id = user.telegram_id

    # Notify user that payment succeeded
    try:
        from bot import texts
        await _bot.send_message(
            telegram_id,
            f"{texts.PAYMENT_SUCCESS}\n\n{texts.ENTER_FIRST_NAME}",
            parse_mode="HTML",
        )

        # Update FSM state for this user
        from aiogram.fsm.storage.memory import MemoryStorage
        storage = _dp.storage
        from aiogram.fsm.storage.base import StorageKey
        key = StorageKey(bot_id=_bot.id, chat_id=telegram_id, user_id=telegram_id)

        # Set FSM state to entering_first_name
        from bot.states.user_states import BookingFSM
        await storage.set_state(key, BookingFSM.entering_first_name)

        logger.info(f"User {telegram_id} notified about successful payment")
    except Exception as e:
        logger.error(f"Failed to notify user {telegram_id}: {e}", exc_info=True)


async def _handle_payment_cancelled(yk_payment_id: str):
    """Payment cancelled — update DB."""
    async with async_session() as session:
        result = await session.execute(
            select(Payment).where(Payment.yookassa_payment_id == yk_payment_id)
        )
        payment = result.scalar_one_or_none()

        if payment and payment.status == PaymentStatus.pending:
            payment.status = PaymentStatus.cancelled
            await session.commit()

            from db.models import User
            user = await session.get(User, payment.user_id)
            if user and _bot:
                try:
                    await _bot.send_message(
                        user.telegram_id,
                        "❌ Оплата отменена. Используйте /start чтобы начать заново.",
                    )
                except Exception as e:
                    logger.error(f"Failed to notify user about cancellation: {e}")

    logger.info(f"Payment {yk_payment_id} cancelled")


def create_webhook_app() -> web.Application:
    """Create aiohttp application for YooKassa webhooks."""
    app = web.Application()
    app.router.add_post("/webhook/yookassa", handle_yookassa_webhook)
    # Health check endpoint
    app.router.add_get("/health", lambda r: web.Response(text="OK"))
    return app
