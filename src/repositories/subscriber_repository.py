from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import asyncpg

from src.types.subscriber import Subscriber


class SubscriberRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    def _map_row(self, row: asyncpg.Record) -> Subscriber:
        return Subscriber(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            chat_id=int(row["chat_id"]),
            username=row["username"],
            first_name=row["first_name"],
            subscribed_at=row["subscribed_at"],
            is_subscription_active=row["is_subscription_active"],
            is_bot_chat_active=row["is_bot_chat_active"],
            welcome_sent_at=row["welcome_sent_at"],
            last_random_sent_at=row["last_random_sent_at"],
            last_fixed_sent_at=row["last_fixed_sent_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def upsert_user(
        self,
        user_id: int,
        chat_id: int,
        username: Optional[str],
        first_name: Optional[str],
    ) -> Subscriber:
        query = """
            INSERT INTO subscribers (
                user_id,
                chat_id,
                username,
                first_name,
                updated_at
            )
            VALUES ($1, $2, $3, $4, NOW())
            ON CONFLICT (user_id)
            DO UPDATE SET
                chat_id = EXCLUDED.chat_id,
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                is_bot_chat_active = TRUE,
                updated_at = NOW()
            RETURNING *
        """
        row = await self.pool.fetchrow(query, user_id, chat_id, username, first_name)
        return self._map_row(row)

    async def find_by_user_id(self, user_id: int) -> Subscriber | None:
        row = await self.pool.fetchrow("SELECT * FROM subscribers WHERE user_id = $1", user_id)
        if row is None:
            return None
        return self._map_row(row)

    async def activate_subscription(self, user_id: int, subscribed_at: datetime | None = None) -> None:
        current_time = subscribed_at or datetime.now(tz=timezone.utc)
        query = """
            UPDATE subscribers
            SET
                is_subscription_active = TRUE,
                subscribed_at = CASE
                    WHEN is_subscription_active = FALSE OR subscribed_at IS NULL THEN $2
                    ELSE subscribed_at
                END,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id, current_time)

    async def deactivate_subscription(self, user_id: int) -> None:
        query = """
            UPDATE subscribers
            SET
                is_subscription_active = FALSE,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id)

    async def reset_delivery_state(self, user_id: int) -> None:
        query = """
            UPDATE subscribers
            SET
                subscribed_at = NULL,
                welcome_sent_at = NULL,
                last_random_sent_at = NULL,
                last_fixed_sent_at = NULL,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id)

    async def set_bot_chat_active(self, user_id: int, is_active: bool) -> None:
        query = """
            UPDATE subscribers
            SET
                is_bot_chat_active = $2,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id, is_active)

    async def mark_welcome_sent(self, user_id: int, sent_at: datetime) -> None:
        query = """
            UPDATE subscribers
            SET
                welcome_sent_at = COALESCE(welcome_sent_at, $2),
                last_random_sent_at = $2,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id, sent_at)

    async def mark_random_sent(self, user_id: int, sent_at: datetime) -> None:
        query = """
            UPDATE subscribers
            SET
                last_random_sent_at = $2,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id, sent_at)

    async def mark_fixed_sent(self, user_id: int, sent_at: datetime) -> None:
        query = """
            UPDATE subscribers
            SET
                last_fixed_sent_at = $2,
                updated_at = NOW()
            WHERE user_id = $1
        """
        await self.pool.execute(query, user_id, sent_at)

    async def list_active_subscribers(self) -> list[Subscriber]:
        rows = await self.pool.fetch(
            """
            SELECT *
            FROM subscribers
            WHERE is_subscription_active = TRUE
            ORDER BY id ASC
            """
        )
        return [self._map_row(row) for row in rows]

    async def try_acquire_scheduler_lock(self, lock_id: int) -> asyncpg.Connection | None:
        connection = await self.pool.acquire()
        try:
            acquired = await connection.fetchval("SELECT pg_try_advisory_lock($1)", lock_id)
            if not acquired:
                await self.pool.release(connection)
                return None
            return connection
        except Exception:
            await self.pool.release(connection)
            raise

    async def release_scheduler_lock(self, connection: asyncpg.Connection, lock_id: int) -> None:
        try:
            await connection.execute("SELECT pg_advisory_unlock($1)", lock_id)
        finally:
            await self.pool.release(connection)
