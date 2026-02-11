# Telegram Tarif Bot

Бот для записи на онлайн-консультации с оплатой через ЮKassa, опросниками и админ-панелью.

## Тарифы

| Тариф | Цена | Особенности |
|-------|------|-------------|
| Базовый | 8 000 ₽ | Полный опросник + аюрвед + фото + слот |
| Сопровождение | 20 000 ₽ | Расширенная консультация |
| Повторная | 5 000 ₽ | Без опросников, фото опционально |
| Лайт | 3 000 ₽ | Только аюрвед-опросник |

## Быстрый старт

### 1. Клонирование
```bash
git clone <repo-url>
cd telegram-tarif-bot
```

### 2. Настройка окружения
```bash
cp .env.example .env
# Заполните .env своими данными
```

### 3. Запуск через Docker
```bash
docker-compose up -d
```

### 4. Миграции БД
```bash
docker-compose exec bot alembic revision --autogenerate -m "initial"
docker-compose exec bot alembic upgrade head
```

### 5. Проверка
- Отправьте `/start` боту в Telegram
- `/admin` для панели администратора (только для ADMIN_IDS)

## Структура проекта

```
bot/
├── main.py              # Точка входа
├── keyboards.py         # Inline-клавиатуры
├── texts.py             # Текстовые константы
├── middlewares.py        # DB session middleware
├── handlers/            # Обработчики команд
│   ├── start.py         # /start + выбор тарифа
│   ├── payment.py       # Проверка оплаты
│   ├── intake.py        # Ввод данных (имя, возраст, вес)
│   ├── questionnaire.py # Движок опросников
│   ├── photos.py        # Загрузка фото
│   ├── slots.py         # Выбор слота + бронирование
│   ├── gender.py        # Выбор пола (лайт)
│   └── admin.py         # Админ-панель
├── services/            # Бизнес-логика
│   ├── yookassa_service.py
│   ├── questionnaire_engine.py
│   ├── slot_service.py
│   ├── booking_service.py
│   ├── photo_service.py
│   └── notification_service.py
└── states/
    └── user_states.py   # FSM-состояния

db/
├── base.py              # SQLAlchemy Base + engine
├── models.py            # Модели данных
└── migrations/          # Alembic

config/
└── settings.py          # Pydantic Settings

questionnaires/          # .md файлы опросников
```

## Технологии

- Python 3.11+
- aiogram 3.x
- SQLAlchemy 2.0 (async)
- PostgreSQL + asyncpg
- ЮKassa SDK
- Docker + Docker Compose
