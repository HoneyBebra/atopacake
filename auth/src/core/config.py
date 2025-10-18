from functools import lru_cache
from logging import config as logging_config
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi_jwt import JwtAccessCookie, JwtRefreshCookie
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError

from src.core.logger import LOGGING

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    postgres_echo: bool

    api_v1_prefix: str = "/auth/api/v1"

    app_name: str
    app_description: str
    app_version: str

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    password_min_length: int = 8

    redis_host: str
    redis_port: str
    redis_db: int

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    @property
    def access_security(self) -> JwtAccessCookie:
        return JwtAccessCookie(secret_key=self.jwt_secret_key, auto_error=False)

    @property
    def refresh_security(self) -> JwtRefreshCookie:
        return JwtRefreshCookie(secret_key=self.jwt_secret_key, auto_error=False)

    @property
    def redis_settings(self) -> dict[str, Any]:
        # TODO: Add redis password

        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "socket_keepalive": True,
            "retry": Retry(ExponentialBackoff(), 3),
            "retry_on_error": [TimeoutError, ConnectionError],
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()

logging_config.dictConfig(LOGGING)
