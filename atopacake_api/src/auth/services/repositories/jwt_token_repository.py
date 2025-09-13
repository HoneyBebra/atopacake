from datetime import datetime

from src.auth.services.repositories.base.jwt_token_repository import BaseJwtTokenRepository
from src.db.redis import get_session


class RedisTokenStorage(BaseJwtTokenRepository):
    async def store_refresh_token(self, token: str, user_id: str, expires_in: int) -> None:
        async with get_session() as session:
            data = {
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
            await session.hset(token, mapping=data)
            await session.expire(token, expires_in)

    async def get_refresh_token(self, token: str) -> dict | None:
        async with get_session() as session:
            data = await session.hgetall(token)
            return {k.decode(): v.decode() for k, v in data.items()} if data else None

    async def delete_refresh_token(self, token: str) -> None:
        async with get_session() as session:
            await session.delete(token)

    async def delete_all_user_tokens(self, user_id: str) -> None:
        # TODO: Check this func performance

        async with get_session() as session:
            async for key in session.scan_iter(match="*"):
                data = await session.hgetall(key)
                if data.get(b"user_id") == user_id.encode():
                    await session.delete(key)
