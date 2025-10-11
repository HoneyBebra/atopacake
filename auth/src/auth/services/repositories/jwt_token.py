from uuid import UUID

from fastapi import Depends
from redis.asyncio import Redis

from src.auth.services.repositories.base.jwt_token import BaseJwtTokenRepository
from src.db.redis import get_blacklist_tokens_session, get_refresh_tokens_session


class JwtTokenRepository(BaseJwtTokenRepository):
    def __init__(
            self,
            refresh_tokens_session: Redis = Depends(get_refresh_tokens_session),
            blacklist_tokens_session: Redis = Depends(get_blacklist_tokens_session)
    ) -> None:
        self.refresh_tokens_session = refresh_tokens_session
        self.blacklist_tokens_session = blacklist_tokens_session

    async def set_refresh_token(self, token: str, user_id: UUID, expires_in: int) -> None:
        async with self.refresh_tokens_session as session:
            await session.setex(
                name=str(user_id),
                time=expires_in,
                value=token,
            )

    async def get_refresh_token(self, user_id: UUID) -> str | None:
        async with self.refresh_tokens_session as session:
            return await session.get(name=str(user_id))

    async def delete_refresh_token(self, user_id: UUID) -> None:
        async with self.refresh_tokens_session as session:
            await session.delete(str(user_id))

    async def set_token_to_blacklist(self, jti: UUID, user_id: UUID, expires_in: int) -> None:
        async with self.blacklist_tokens_session as session:
            await session.setex(
                name=str(jti),
                time=expires_in,
                value=str(user_id),
            )

    async def is_token_in_blacklist(self, jti: UUID) -> bool:
        async with self.blacklist_tokens_session as session:
            return bool(await session.exists(str(jti)))
