from aiogram import Router
from aiogram.types import ChatMemberUpdated

from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_active_member_status

logger = get_logger(__name__)


def build_my_chat_member_router(subscription_service: SubscriptionService) -> Router:
    router = Router()

    @router.my_chat_member()
    async def my_chat_member_handler(event: ChatMemberUpdated) -> None:
        if event.chat.type != "private":
            return

        user_id = int(event.chat.id)
        is_active = is_active_member_status(event.new_chat_member.status)

        subscriber = await subscription_service.find_by_user_id(user_id)
        if subscriber is None:
            return

        logger.info(
            "Private chat state changed for user_id=%s, is_active=%s (no delivery state updated)",
            user_id,
            is_active,
        )

    return router
