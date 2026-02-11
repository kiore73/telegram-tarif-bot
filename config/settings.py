from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str
    ADMIN_IDS: List[int] = []

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://botuser:botpassword@localhost:5432/tarif_bot"

    # YooKassa
    YOOKASSA_SHOP_ID: str = ""
    YOOKASSA_SECRET_KEY: str = ""
    YOOKASSA_RETURN_URL: str = ""
    YOOKASSA_DEFAULT_RECEIPT_EMAIL: str = ""
    YOOKASSA_VAT_CODE: int = 1
    YOOKASSA_PAYMENT_MODE: str = "full_payment"
    YOOKASSA_PAYMENT_SUBJECT: str = "service"
    YOOKASSA_ENABLED: bool = True

    # Tariff prices
    TARIFF_BASIC_PRICE: int = 8000
    TARIFF_EXTENDED_PRICE: int = 20000
    TARIFF_REPEAT_PRICE: int = 5000
    TARIFF_LITE_PRICE: int = 3000

    # Webhook
    WEBHOOK_PORT: int = 8080
    YOOKASSA_WEBHOOK_SECRET: str = ""

    # Other
    TIMEZONE: str = "Europe/Moscow"
    UPLOAD_DIR: str = "./uploads"
    PHOTO_RETENTION_DAYS: int = 30

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()  # type: ignore[call-arg]
