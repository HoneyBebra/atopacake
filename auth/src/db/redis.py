from typing import AsyncGenerator

from redis.asyncio import Redis

from src.core.config import settings


async def get_redis_session() -> AsyncGenerator:
    async with Redis(**settings.redis_settings) as session:
        try:
            yield session
        finally:
            await session.close()
