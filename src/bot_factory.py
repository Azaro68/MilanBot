from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config.settings import settings
from src.handlers.chat_join_request_handler import build_chat_join_request_router
from src.handlers.chat_member_handler import build_chat_member_router
from src.handlers.check_handler import build_check_router
from src.handlers.my_chat_member_handler import build_my_chat_member_router
from src.handlers.start_handler import build_start_router
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.message_picker import MessagePicker
from src.services.messaging_service import MessagingService
from src.services.scheduler_service import SchedulerService
from src.services.subscription_service import SubscriptionService
from src.utils.time_utils import TimeUtils


def create_application(subscriber_repository: SubscriberRepository):
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()

    subscription_service = SubscriptionService(
        bot=bot,
        subscriber_repository=subscriber_repository,
    )

    messaging_service = MessagingService(
        bot=bot,
        subscriber_repository=subscriber_repository,
        message_picker=MessagePicker(),
    )

    time_utils = TimeUtils(settings.time_zone)

    scheduler_service = SchedulerService(
        subscriber_repository=subscriber_repository,
        subscription_service=subscription_service,
        messaging_service=messaging_service,
        time_utils=time_utils,
    )

    dispatcher.include_router(build_start_router(subscription_service))
    dispatcher.include_router(build_check_router(subscription_service, messaging_service))
    dispatcher.include_router(build_chat_join_request_router(bot, subscription_service, messaging_service))
    dispatcher.include_router(build_chat_member_router(subscription_service, messaging_service))
    dispatcher.include_router(build_my_chat_member_router(subscription_service))

    return bot, dispatcher, scheduler_service
