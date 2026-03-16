from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Subscriber:
    id: int
    user_id: int
    chat_id: int
    username: Optional[str]
    first_name: Optional[str]
    subscribed_at: Optional[datetime]
    is_subscription_active: bool
    is_bot_chat_active: bool
    welcome_sent_at: Optional[datetime]
    last_random_sent_at: Optional[datetime]
    last_fixed_sent_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
