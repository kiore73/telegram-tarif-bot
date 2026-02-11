"""YooKassa payment service — adapted from yookassa_service.example.py."""

import uuid
import logging
import asyncio
from typing import Optional, Dict, Any, List

from yookassa import Configuration, Payment as YooKassaPayment
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from yookassa.domain.common.confirmation_type import ConfirmationType

from config.settings import Settings


class YooKassaService:
    def __init__(self, settings_obj: Settings) -> None:
        self.settings = settings_obj

        if not self.settings.YOOKASSA_ENABLED:
            logging.warning("YooKassa is disabled via YOOKASSA_ENABLED flag.")
            self.configured = False
        elif not self.settings.YOOKASSA_SHOP_ID or not self.settings.YOOKASSA_SECRET_KEY:
            logging.warning("YooKassa SHOP_ID or SECRET_KEY not configured.")
            self.configured = False
        else:
            try:
                Configuration.configure(
                    self.settings.YOOKASSA_SHOP_ID,
                    self.settings.YOOKASSA_SECRET_KEY,
                )
                self.configured = True
                logging.info("YooKassa SDK configured.")
            except Exception as e:
                logging.error(f"Failed to configure YooKassa: {e}", exc_info=True)
                self.configured = False

        self.return_url = self.settings.YOOKASSA_RETURN_URL or "https://t.me/bot"

    # ------------------------------------------------------------------

    async def create_payment(
        self,
        amount: float,
        currency: str,
        description: str,
        metadata: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        if not self.configured:
            logging.error("YooKassa not configured. Cannot create payment.")
            return None

        customer_contact: Dict[str, str] = {}
        if self.settings.YOOKASSA_DEFAULT_RECEIPT_EMAIL:
            customer_contact["email"] = self.settings.YOOKASSA_DEFAULT_RECEIPT_EMAIL
        else:
            logging.error("No receipt email configured.")
            return None

        try:
            builder = PaymentRequestBuilder()
            builder.set_amount({"value": str(round(amount, 2)), "currency": currency.upper()})
            builder.set_capture(True)
            builder.set_confirmation({
                "type": ConfirmationType.REDIRECT,
                "return_url": self.return_url,
            })
            builder.set_description(description)
            builder.set_metadata(metadata)

            receipt_items: List[Dict[str, Any]] = [{
                "description": description[:128],
                "quantity": "1.00",
                "amount": {"value": str(round(amount, 2)), "currency": currency.upper()},
                "vat_code": str(self.settings.YOOKASSA_VAT_CODE),
                "payment_mode": self.settings.YOOKASSA_PAYMENT_MODE,
                "payment_subject": self.settings.YOOKASSA_PAYMENT_SUBJECT,
            }]
            builder.set_receipt({"customer": customer_contact, "items": receipt_items})

            idempotence_key = str(uuid.uuid4())
            request = builder.build()

            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, lambda: YooKassaPayment.create(request, idempotence_key)
            )

            return {
                "id": response.id,
                "confirmation_url": (
                    response.confirmation.confirmation_url if response.confirmation else None
                ),
                "status": response.status,
                "paid": response.paid,
            }
        except Exception as e:
            logging.error(f"YooKassa payment creation failed: {e}", exc_info=True)
            return None

    async def get_payment_info(self, payment_id: str) -> Optional[Dict[str, Any]]:
        if not self.configured:
            return None
        try:
            loop = asyncio.get_running_loop()
            info = await loop.run_in_executor(
                None, lambda: YooKassaPayment.find_one(payment_id)
            )
            if not info:
                return None
            return {
                "id": info.id,
                "status": info.status,
                "paid": info.paid,
            }
        except Exception as e:
            logging.error(f"YooKassa get info failed: {e}", exc_info=True)
            return None

    async def cancel_payment(self, payment_id: str) -> bool:
        if not self.configured:
            return False
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: YooKassaPayment.cancel(payment_id))
            return True
        except Exception as e:
            logging.error(f"YooKassa cancel failed: {e}", exc_info=True)
            return False
