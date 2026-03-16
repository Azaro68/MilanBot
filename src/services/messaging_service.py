from __future__ import annotations

from datetime import datetime, timezone

from aiogram import Bot
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

from src.config.messages import FIXED_MESSAGE, FIXED_MESSAGE_IMAGE_PATH, JOIN_REQUEST_MESSAGE, RANDOM_MESSAGES
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.message_picker import MessagePicker
from src.types.subscriber import Subscriber
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_blocked_bot_error

logger = get_logger(__name__)


class MessagingService:
    def __init__(
        self,
        bot: Bot,
        subscriber_repository: SubscriberRepository,
        message_picker: MessagePicker,
    ):
        self.bot = bot
        self.subscriber_repository = subscriber_repository
        self.message_picker = message_picker

    async def send_welcome_random_message(self, subscriber: Subscriber) -> bool:
        if subscriber.welcome_sent_at is not None:
            return False

        sent_at = datetime.now(tz=timezone.utc)
        message_data = self.message_picker.pick_random(RANDOM_MESSAGES)

        try:
            await self._send_random_message(
                chat_id=subscriber.chat_id,
                message_data=message_data,
            )
            await self.subscriber_repository.mark_welcome_sent(subscriber.user_id, sent_at)
            logger.info("Welcome random message sent to user_id=%s", subscriber.user_id)
            return True
        except Exception as error:
            await self._handle_send_error(subscriber.user_id, error)
            logger.exception("Failed to send welcome random message to user_id=%s", subscriber.user_id)
            return False

    async def send_daily_random_message(self, subscriber: Subscriber) -> bool:
        sent_at = datetime.now(tz=timezone.utc)
        message_data = self.message_picker.pick_random(RANDOM_MESSAGES)

        try:
            await self._send_random_message(
                chat_id=subscriber.chat_id,
                message_data=message_data,
            )
            await self.subscriber_repository.mark_random_sent(subscriber.user_id, sent_at)
            logger.info("Daily random message sent to user_id=%s", subscriber.user_id)
            return True
        except Exception as error:
            await self._handle_send_error(subscriber.user_id, error)
            logger.exception("Failed to send daily random message to user_id=%s", subscriber.user_id)
            return False

    async def send_daily_fixed_message(self, subscriber: Subscriber) -> bool:
        sent_at = datetime.now(tz=timezone.utc)

        try:
            photo = FSInputFile(FIXED_MESSAGE_IMAGE_PATH)
            await self.bot.send_photo(
                subscriber.chat_id,
                photo=photo,
                caption=FIXED_MESSAGE,
            )
            await self.subscriber_repository.mark_fixed_sent(subscriber.user_id, sent_at)
            logger.info("Daily fixed message sent to user_id=%s", subscriber.user_id)
            return True
        except Exception as error:
            await self._handle_send_error(subscriber.user_id, error)
            logger.exception("Failed to send daily fixed message to user_id=%s", subscriber.user_id)
            return False

    async def send_join_request_message(
        self,
        user_id: int,
        chat_id: int,
    ) -> bool:
        sent_at = datetime.now(tz=timezone.utc)

        try:
            await self._send_random_message(
                chat_id=chat_id,
                message_data=JOIN_REQUEST_MESSAGE,
            )
            await self.subscriber_repository.mark_welcome_sent(user_id, sent_at)
            logger.info("Join request message sent to user_id=%s", user_id)
            return True
        except Exception as error:
            await self._handle_send_error(user_id, error)
            logger.exception("Failed to send join request message to user_id=%s", user_id)
            return False

    async def _send_random_message(
        self,
        chat_id: int,
        message_data: dict,
    ) -> None:
        buttons = message_data.get("buttons")
        if buttons is None:
            buttons = [
                {
                    "text": message_data["button_text"],
                    "url": message_data["button_url"],
                }
            ]

        keyboard_rows = [
            [InlineKeyboardButton(text=button["text"], url=button["url"])]
            for button in buttons
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

        image_path = message_data.get("image_path")
        caption = message_data.get("caption", "")

        if image_path:
            photo = FSInputFile(image_path)
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                reply_markup=keyboard,
            )
            return

        await self.bot.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=keyboard,
        )

    async def send_text(self, chat_id: int, text: str) -> None:
        await self.bot.send_message(chat_id, text)

    async def _handle_send_error(self, user_id: int, error: Exception) -> None:
        if is_blocked_bot_error(error):
            await self.subscriber_repository.set_bot_chat_active(user_id, False)
