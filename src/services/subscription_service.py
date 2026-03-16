from __future__ import annotations

from datetime import datetime, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from src.config.settings import settings
from src.repositories.subscriber_repository import SubscriberRepository
from src.types.subscriber import Subscriber
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_active_member_status

logger = get_logger(__name__)


class SubscriptionService:
    def __init__(self, bot: Bot, subscriber_repository: SubscriberRepository):
        self.bot = bot
        self.subscriber_repository = subscriber_repository

    async def upsert_private_user(
        self,
        user_id: int,
        chat_id: int,
        username: str | None,
        first_name: str | None,
    ) -> Subscriber:
        return await self.subscriber_repository.upsert_user(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
            first_name=first_name,
        )

    async def activate_subscription(self, user_id: int) -> None:
        await self.subscriber_repository.activate_subscription(
            user_id=user_id,
            subscribed_at=datetime.now(tz=timezone.utc),
        )

    async def deactivate_subscription(self, user_id: int) -> None:
        await self.subscriber_repository.deactivate_subscription(user_id)

    async def reset_delivery_state(self, user_id: int) -> None:
        await self.subscriber_repository.reset_delivery_state(user_id)

    async def mark_bot_chat_active(self, user_id: int, is_active: bool) -> None:
        await self.subscriber_repository.set_bot_chat_active(user_id, is_active)

    async def find_by_user_id(self, user_id: int) -> Subscriber | None:
        return await self.subscriber_repository.find_by_user_id(user_id)

    async def verify_channel_membership(self, user_id: int) -> bool:
        try:
            member = await self.bot.get_chat_member(settings.channel_id, user_id)
            return is_active_member_status(member.status)
        except TelegramAPIError as error:
            logger.exception("Failed to verify channel membership for user_id=%s", user_id)
            return False

    async def ensure_active_subscription_state(self, user_id: int) -> bool:
        is_subscribed = await self.verify_channel_membership(user_id)
        if is_subscribed:
            await self.activate_subscription(user_id)
            return True

        await self.deactivate_subscription(user_id)
        return False
