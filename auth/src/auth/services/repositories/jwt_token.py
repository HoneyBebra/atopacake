from fastapi import Depends
from redis.asyncio import Redis

from src.auth.services.repositories.base.jwt_token import BaseJwtTokenRepository
from src.db.redis import get_redis_session


class JwtTokenRepository(BaseJwtTokenRepository):
    def __init__(
            self,
            redis_session: Redis = Depends(get_redis_session),
    ) -> None:
        self.redis_session = redis_session

    async def set_token_to_blacklist(self, token: str, expires_in: int) -> None:
        async with self.redis_session as session:
            await session.setex(
                name=token,
                time=expires_in,
                value="none",
            )

    async def is_token_in_blacklist(self, token: str) -> bool:
        async with self.redis_session as session:
            return bool(await session.exists(token))
