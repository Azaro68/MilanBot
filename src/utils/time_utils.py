from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class TimeUtils:
    def __init__(self, time_zone: str):
        self.zone = ZoneInfo(time_zone)

    def now_local(self) -> datetime:
        return datetime.now(tz=self.zone)

    def to_local(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=self.zone)
        return value.astimezone(self.zone)

    def local_date_key(self, value: datetime) -> str:
        return self.to_local(value).strftime("%Y-%m-%d")

    def local_time_key(self, value: datetime) -> str:
        return self.to_local(value).strftime("%H:%M")

    def local_minute_key(self, value: datetime) -> str:
        return self.to_local(value).strftime("%Y-%m-%d %H:%M")

    def has_local_date(self, value: datetime | None, expected_date_key: str) -> bool:
        if value is None:
            return False
        return self.local_date_key(value) == expected_date_key

    def has_local_minute(self, value: datetime | None, expected_minute_key: str) -> bool:
        if value is None:
            return False
        return self.local_minute_key(value) == expected_minute_key

    def add_minutes(self, value: datetime, minutes: int) -> datetime:
        return value + timedelta(minutes=minutes)
