from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(alias="DATABASE_URL")
    channel_id: int = Field(alias="CHANNEL_ID")
    channel_link: str = Field(alias="CHANNEL_LINK")
    telegram_bot_username: str = Field(alias="TELEGRAM_BOT_USERNAME")
    time_zone: str = Field(default="Europe/Moscow", alias="TIME_ZONE")
    scheduler_tick_cron: str = Field(default="*/5 * * * *", alias="SCHEDULER_TICK_CRON")
    random_send_interval_hours: int = Field(default=5, alias="RANDOM_SEND_INTERVAL_HOURS")
    fixed_send_time: str = Field(default="20:00", alias="FIXED_SEND_TIME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
