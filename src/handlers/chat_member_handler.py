from aiogram import Router
from aiogram.types import ChatMemberUpdated

from src.config.settings import settings
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_active_member_status

logger = get_logger(__name__)


def build_chat_member_router(
    subscription_service: SubscriptionService,
    messaging_service: MessagingService,
) -> Router:
    router = Router()

    @router.chat_member()
    async def chat_member_handler(event: ChatMemberUpdated) -> None:
        if event.chat.id != settings.channel_id:
            return

        user = event.new_chat_member.user
        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status

        was_active = is_active_member_status(old_status)
        is_active = is_active_member_status(new_status)

        if not was_active and is_active:
            await subscription_service.upsert_private_user(
                user_id=user.id,
                chat_id=user.id,
                username=user.username,
                first_name=user.first_name,
            )
            await subscription_service.activate_subscription(user.id)

            subscriber = await subscription_service.find_by_user_id(user.id)
            if subscriber is not None:
                await messaging_service.send_welcome_random_message(subscriber)

            logger.info("Channel subscription detected via chat_member for user_id=%s", user.id)
            return

        if was_active and not is_active:
            await subscription_service.deactivate_subscription(user.id)
            await subscription_service.reset_delivery_state(user.id)
            logger.info("Channel unsubscribe detected via chat_member for user_id=%s", user.id)

    return router
