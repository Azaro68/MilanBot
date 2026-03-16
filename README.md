# Telegram Channel Subscription Bot (Python)

Python-версия Telegram-бота для канала.

## Что делает бот

- при join request отправляет отдельное welcome-сообщение
- затем отправляет одно случайное сообщение из 4 каждые 5 часов
- один раз в день отправляет фиксированное сообщение в 20:00 по Москве
- защищается от дублей
- останавливает ежедневные отправки после отписки
- помнит блокировку бота пользователем

## Рекомендуемый Telegram-сценарий

Лучший вариант — включить в канале join requests и сделать бота администратором.
Тогда бот сможет:

1. получить `chat_join_request`
2. одобрить заявку
3. записать пользователя в БД
4. отправить welcome-сообщение в личку

Fallback-сценарий тоже есть:

- пользователь открывает бота и пишет `/start`
- бот проверяет подписку на канал
- пользователь может отправить `/check`

## Стек

- Python 3.11+
- aiogram
- asyncpg
- APScheduler
- PostgreSQL

## Структура проекта

```text
telegram-channel-bot-python/
├─ .env.example
├─ requirements.txt
├─ README.md
├─ sql/
│  └─ 001_init.sql
└─ src/
   ├─ main.py
   ├─ bot_factory.py
   ├─ config/
   │  ├─ settings.py
   │  └─ messages.py
   ├─ db/
   │  └─ pool.py
   ├─ handlers/
   │  ├─ start_handler.py
   │  ├─ check_handler.py
   │  ├─ chat_join_request_handler.py
   │  ├─ chat_member_handler.py
   │  └─ my_chat_member_handler.py
   ├─ repositories/
   │  └─ subscriber_repository.py
   ├─ services/
   │  ├─ message_picker.py
   │  ├─ messaging_service.py
   │  ├─ subscription_service.py
   │  └─ scheduler_service.py
   ├─ types/
   │  └─ subscriber.py
   └─ utils/
      ├─ logger.py
      ├─ time_utils.py
      └─ telegram_utils.py
```

## Настройка

### 1. Создайте и заполните `.env`

```bash
cp .env.example .env
```

### 2. Создайте виртуальное окружение и установите зависимости

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Создайте БД и примените SQL

```bash
createdb telegram_bot
psql "$DATABASE_URL" -f sql/001_init.sql
```

### 4. Запустите бота

```bash
python -m src.main
```

## Деплой

Самый простой вариант для такого бота — Railway: там удобно поднять и сам Python-процесс, и PostgreSQL рядом.

Что уже подготовлено в проекте:

- `Dockerfile` для запуска бота как long-running worker
- `.dockerignore`
- `.env.example`

### Вариант: Railway

1. Залейте проект в GitHub.
2. В Railway создайте проект и подключите репозиторий.
3. Добавьте в проект PostgreSQL.
4. Railway автоматически подхватит `Dockerfile`.
5. В Variables задайте:
   - `BOT_TOKEN`
   - `DATABASE_URL`
   - `CHANNEL_ID`
   - `CHANNEL_LINK`
   - `TELEGRAM_BOT_USERNAME`
   - `TIME_ZONE`
   - `SCHEDULER_TICK_CRON`
   - `RANDOM_SEND_INTERVAL_HOURS`
   - `FIXED_SEND_TIME`
   - `LOG_LEVEL`
6. После первого запуска примените SQL из `sql/001_init.sql` к базе Railway.

Для продакшна рекомендую вернуть обычный режим:

- `SCHEDULER_TICK_CRON=*/5 * * * *`
- `TIME_ZONE=Europe/Moscow`
- `RANDOM_SEND_INTERVAL_HOURS=5`
- `FIXED_SEND_TIME=20:00`

### Как применить SQL в Railway

Откройте PostgreSQL в Railway и выполните содержимое файла `sql/001_init.sql`.

После этого бот сможет работать постоянно как фоновый сервис.

## Важные настройки Telegram

- бот должен быть администратором канала
- для join requests у бота должно быть право одобрять заявки
- бот должен получать `chat_member` и `chat_join_request`
- если пользователь никогда не писал боту, обычная подписка без join requests может не позволить отправить ему личное сообщение

## Где задаются тексты

Файл:

- `src/config/messages.py`

Там находятся:

- `RANDOM_MESSAGES` — 4 случайных сообщения
- `FIXED_MESSAGE` — 1 фиксированное сообщение

## Антидубли

Используются поля:

- `welcome_sent_at`
- `last_random_sent_at`
- `last_fixed_sent_at`

Также scheduler использует PostgreSQL advisory lock, чтобы несколько инстансов не запустили один и тот же daily tick одновременно.
