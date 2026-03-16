from __future__ import annotations

from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config.settings import settings
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService
from src.types.subscriber import Subscriber
from src.utils.logger import get_logger
from src.utils.time_utils import TimeUtils

logger = get_logger(__name__)

SCHEDULER_LOCK_ID = 910001


class SchedulerService:
    def __init__(
        self,
        subscriber_repository: SubscriberRepository,
        subscription_service: SubscriptionService,
        messaging_service: MessagingService,
        time_utils: TimeUtils,
    ):
        self.subscriber_repository = subscriber_repository
        self.subscription_service = subscription_service
        self.messaging_service = messaging_service
        self.time_utils = time_utils
        self.scheduler = AsyncIOScheduler(timezone=settings.time_zone)

    def start(self) -> None:
        trigger = CronTrigger.from_crontab(settings.scheduler_tick_cron, timezone=settings.time_zone)
        self.scheduler.add_job(self.process_tick, trigger=trigger, id="daily_messages_tick", replace_existing=True)
        self.scheduler.start()
        logger.info(
            "Scheduler started: cron=%s timezone=%s random_interval_hours=%s fixed=%s",
            settings.scheduler_tick_cron,
            settings.time_zone,
            settings.random_send_interval_hours,
            settings.fixed_send_time,
        )

    async def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    async def process_tick(self) -> None:
        connection = await self.subscriber_repository.try_acquire_scheduler_lock(SCHEDULER_LOCK_ID)
        if connection is None:
            logger.warning("Scheduler tick skipped because another instance holds the advisory lock")
            return

        try:
            subscribers = await self.subscriber_repository.list_active_subscribers()
            for subscriber in subscribers:
                await self.process_subscriber(subscriber)
        except Exception:
            logger.exception("Scheduler tick failed")
        finally:
            await self.subscriber_repository.release_scheduler_lock(connection, SCHEDULER_LOCK_ID)

    async def process_subscriber(self, subscriber: Subscriber) -> None:
        if not subscriber.is_bot_chat_active:
            return

        still_subscribed = await self.subscription_service.ensure_active_subscription_state(subscriber.user_id)
        if not still_subscribed:
            logger.info("User user_id=%s is no longer subscribed, daily sends stopped", subscriber.user_id)
            return

        fresh_subscriber = await self.subscription_service.find_by_user_id(subscriber.user_id)
        if fresh_subscriber is None:
            return

        now_local = self.time_utils.now_local()

        if self.should_send_random(fresh_subscriber, now_local):
            await self.messaging_service.send_daily_random_message(fresh_subscriber)

        if self.should_send_daily_fixed(fresh_subscriber, now_local):
            await self.messaging_service.send_daily_fixed_message(fresh_subscriber)

    def should_send_random(self, subscriber: Subscriber, now_local) -> bool:
        if subscriber.welcome_sent_at is None or subscriber.subscribed_at is None:
            return False

        last_random_sent_at = subscriber.last_random_sent_at or subscriber.welcome_sent_at
        next_random_at = self.time_utils.to_local(last_random_sent_at) + timedelta(
            hours=settings.random_send_interval_hours
        )
        return now_local >= next_random_at

    def should_send_daily_fixed(self, subscriber: Subscriber, now_local) -> bool:
        if subscriber.welcome_sent_at is None or subscriber.subscribed_at is None:
            return False

        today_key = self.time_utils.local_date_key(now_local)

        if self.time_utils.has_local_date(subscriber.last_fixed_sent_at, today_key):
            return False

        current_time = self.time_utils.local_time_key(now_local)
        return current_time >= settings.fixed_send_time
