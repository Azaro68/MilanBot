from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.config.settings import settings
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService


def build_check_router(
    subscription_service: SubscriptionService,
    messaging_service: MessagingService,
) -> Router:
    router = Router()

    @router.message(Command("check"))
    async def check_handler(message: Message) -> None:
        if message.from_user is None or message.chat is None or message.chat.type != "private":
            return

        await subscription_service.upsert_private_user(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

        is_subscribed = await subscription_service.ensure_active_subscription_state(message.from_user.id)
        if not is_subscribed:
            await message.answer(f"Я пока не вижу активную подписку на канал: {settings.channel_link}")
            return

        subscriber = await subscription_service.find_by_user_id(message.from_user.id)
        if subscriber is None:
            return

        if subscriber.welcome_sent_at is None:
            await messaging_service.send_welcome_random_message(subscriber)
            return

        await message.answer("Подписка подтверждена ✅ Ежедневные сообщения уже активны.")

    return router
