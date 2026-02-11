"""/start handler — tariff selection."""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot import texts, keyboards
from bot.states.user_states import BookingFSM
from bot.services.yookassa_service import YooKassaService
from config.settings import settings
from db.models import User, Payment, PaymentStatus, TariffType

router = Router()

TARIFF_PRICES = {
    "basic": settings.TARIFF_BASIC_PRICE,
    "extended": settings.TARIFF_EXTENDED_PRICE,
    "repeat": settings.TARIFF_REPEAT_PRICE,
    "lite": settings.TARIFF_LITE_PRICE,
}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    welcome = texts.WELCOME.format(
        basic_price=f"{settings.TARIFF_BASIC_PRICE:,}".replace(",", " "),
        extended_price=f"{settings.TARIFF_EXTENDED_PRICE:,}".replace(",", " "),
        repeat_price=f"{settings.TARIFF_REPEAT_PRICE:,}".replace(",", " "),
        lite_price=f"{settings.TARIFF_LITE_PRICE:,}".replace(",", " "),
    )
    await message.answer(welcome, parse_mode="HTML", reply_markup=keyboards.tariff_keyboard())


@router.callback_query(F.data.startswith("tariff:"))
async def on_tariff_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    tariff_key = callback.data.split(":")[1]
    price = TARIFF_PRICES.get(tariff_key)
    if not price:
        await callback.answer("Неизвестный тариф")
        return

    # Ensure user exists in DB
    tg_id = callback.from_user.id
    result = await session.execute(select(User).where(User.telegram_id == tg_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=tg_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    # Create pending payment record
    payment = Payment(
        user_id=user.id,
        tariff=TariffType(tariff_key),
        amount=price,
        currency="RUB",
        status=PaymentStatus.pending,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    # Create YooKassa payment
    yk = YooKassaService(settings)
    tariff_label = texts.TARIFF_LABELS.get(tariff_key, tariff_key)
    yk_result = await yk.create_payment(
        amount=float(price),
        currency="RUB",
        description=f"Консультация «{tariff_label}»",
        metadata={"payment_id": str(payment.id), "user_id": str(user.id), "tariff": tariff_key},
    )

    if not yk_result or not yk_result.get("confirmation_url"):
        await callback.message.edit_text(texts.PAYMENT_ERROR, parse_mode="HTML")
        await callback.answer()
        return

    payment.yookassa_payment_id = yk_result["id"]
    await session.commit()

    await state.update_data(
        tariff=tariff_key,
        payment_id=payment.id,
        user_db_id=user.id,
        yookassa_payment_id=yk_result["id"],
    )
    await state.set_state(BookingFSM.awaiting_payment)

    tariff_text = texts.TARIFF_SELECTED.format(tariff=tariff_label, price=f"{price:,}".replace(",", " "))
    consent_text = (
        '⚠️ Нажимая кнопку «Оплатить», я подтверждаю, что ознакомлен(а) '
        'и согласен(на) с <b>Договором-офертой</b> и <b>Согласием на обработку '
        'моих персональных данных</b>, включая данные о здоровье и пищевых привычках.'
    )
    await callback.message.edit_text(
        f"{tariff_text}\n\n{consent_text}\n\n{texts.PAYMENT_CHECK}",
        parse_mode="HTML",
        reply_markup=keyboards.payment_check_keyboard(yk_result["confirmation_url"]),
    )
    await callback.answer()
