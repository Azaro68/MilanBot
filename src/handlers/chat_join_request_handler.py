from aiogram import Bot, Router
from aiogram.types import ChatJoinRequest

from src.config.settings import settings
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_chat_join_request_router(
    bot: Bot,
    subscription_service: SubscriptionService,
    messaging_service: MessagingService,
) -> Router:
    router = Router()

    @router.chat_join_request()
    async def chat_join_request_handler(join_request: ChatJoinRequest) -> None:
        logger.info(
            "Join request received: request_chat_id=%s expected_channel_id=%s user_id=%s user_chat_id=%s username=%s",
            join_request.chat.id,
            settings.channel_id,
            join_request.from_user.id,
            join_request.user_chat_id,
            join_request.from_user.username,
        )

        if join_request.chat.id != settings.channel_id:
            logger.info(
                "Join request ignored because chat_id does not match target channel: request_chat_id=%s expected_channel_id=%s",
                join_request.chat.id,
                settings.channel_id,
            )
            return

        user = join_request.from_user

        try:
            await subscription_service.upsert_private_user(
                user_id=user.id,
                chat_id=join_request.user_chat_id,
                username=user.username,
                first_name=user.first_name,
            )

            await subscription_service.activate_subscription(user.id)

            logger.info(
                "Subscriber saved from join request: user_id=%s chat_id=%s",
                user.id,
                join_request.user_chat_id,
            )
        except Exception:
            logger.exception(
                "Failed to save subscriber from join request for user_id=%s",
                user.id,
            )
            return

        sent = await messaging_service.send_join_request_message(
            user_id=user.id,
            chat_id=join_request.user_chat_id,
        )

        if not sent:
            return

        try:
            await bot.approve_chat_join_request(
                chat_id=join_request.chat.id,
                user_id=user.id,
            )
            logger.info(
                "Join request approved successfully: user_id=%s channel_id=%s",
                user.id,
                join_request.chat.id,
            )
        except Exception:
            logger.exception(
                "Failed to approve join request for user_id=%s channel_id=%s",
                user.id,
                join_request.chat.id,
            )

    return router
