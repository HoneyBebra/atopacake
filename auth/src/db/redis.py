from typing import AsyncGenerator

from redis.asyncio import Redis

from src.core.config import settings


async def get_refresh_tokens_session() -> AsyncGenerator:
    async with Redis(
            **settings.redis_settings,
            db=settings.redis_refresh_tokens_db,
    ) as session:
        try:
            yield session
        finally:
            await session.close()


async def get_blacklist_tokens_session() -> AsyncGenerator:
    async with Redis(
            **settings.redis_settings,
            db=settings.redis_blacklist_tokens_db,
    ) as session:
        try:
            yield session
        finally:
            await session.close()
