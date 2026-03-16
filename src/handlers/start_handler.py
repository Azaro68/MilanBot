from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.config.settings import settings
from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_start_router(subscription_service: SubscriptionService) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        if message.chat.type != "private" or message.from_user is None:
            return

        user = message.from_user

        await subscription_service.upsert_private_user(
            user_id=user.id,
            chat_id=message.chat.id,
            username=user.username,
            first_name=user.first_name,
        )

        is_subscribed = await subscription_service.ensure_active_subscription_state(user.id)

        if not is_subscribed:
            await message.answer(
                "Я пока не вижу у вас активную подписку на канал.\n"
                f"Подпишитесь на канал: {settings.channel_link}"
            )
            return

        await subscription_service.mark_bot_chat_active(user.id, True)

        await message.answer(
            "Готово ✅\n"
            "Ежедневные уведомления активированы.\n"
            "Теперь я буду присылать:\n"
            "1) одно случайное сообщение из 4\n"
            "2) затем одно фиксированное сообщение"
        )

        logger.info("Notifications activated in private chat for user_id=%s", user.id)

    return router