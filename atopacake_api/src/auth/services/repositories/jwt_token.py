from fastapi import Depends
from redis.asyncio import Redis

from src.auth.services.repositories.base.jwt_token import BaseJwtTokenRepository
from src.db.redis import get_session


class JwtTokenRepository(BaseJwtTokenRepository):
    def __init__(self, session: Redis = Depends(get_session)) -> None:
        self.session = session

    async def create_refresh_token(self, token: str, user_id: str, expires_in: int) -> None:
        async with self.session as session:
            await session.set(user_id, token)
            await session.expire(user_id, expires_in)

    async def get_refresh_token(self, user_id: str) -> str | None:
        async with self.session as session:
            return await session.get(user_id)

    async def delete_refresh_token(self, user_id: str) -> None:
        async with self.session as session:
            await session.delete(user_id)
