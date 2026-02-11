"""Payment status checking handler."""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import texts
from bot.states.user_states import BookingFSM
from bot.services.yookassa_service import YooKassaService
from config.settings import settings
from db.models import Payment, PaymentStatus

router = Router()


@router.callback_query(F.data == "check_payment", BookingFSM.awaiting_payment)
async def check_payment(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    yk_payment_id = data.get("yookassa_payment_id")
    payment_db_id = data.get("payment_id")

    if not yk_payment_id:
        await callback.answer("Ошибка: платёж не найден", show_alert=True)
        return

    yk = YooKassaService(settings)
    info = await yk.get_payment_info(yk_payment_id)

    if not info:
        await callback.answer("Не удалось проверить статус оплаты. Попробуйте позже.", show_alert=True)
        return

    if info.get("status") == "succeeded" and info.get("paid"):
        # Update payment in DB
        payment = await session.get(Payment, payment_db_id)
        if payment:
            payment.status = PaymentStatus.succeeded
            await session.commit()

        await callback.message.edit_text(texts.PAYMENT_SUCCESS, parse_mode="HTML")

        tariff = data.get("tariff")
        # Next step: intake (name)
        await state.set_state(BookingFSM.entering_first_name)
        await callback.message.answer(texts.ENTER_FIRST_NAME, parse_mode="HTML")
    else:
        await callback.answer(texts.PAYMENT_PENDING, show_alert=True)
