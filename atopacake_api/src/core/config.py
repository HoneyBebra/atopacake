from functools import lru_cache
from logging import config as logging_config
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.exc import DisconnectionError, OperationalError
from tenacity import retry_if_exception_type, stop_after_attempt, wait_exponential

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

    api_v1_prefix: str = "/api/v1"

    app_name: str
    app_description: str
    app_version: str

    access_token_key_in_cookie: str = "access_token"

    grpc_user_service_url: str = "auth:50051"

    backoff_retries_count: int = 10

    @property
    def backoff_decorator_sqlalchemy_settings(self) -> dict[str, Any]:
        return {
            "stop": stop_after_attempt(self.backoff_retries_count),
            "wait": wait_exponential(multiplier=1, min=2, max=60),
            "retry": retry_if_exception_type((OperationalError, DisconnectionError)),
            "reraise": True,
        }

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


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()

logging_config.dictConfig(LOGGING)
