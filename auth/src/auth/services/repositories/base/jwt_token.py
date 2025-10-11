from abc import ABC, abstractmethod
from uuid import UUID


class BaseJwtTokenRepository(ABC):
    @abstractmethod
    async def set_refresh_token(self, token: str, user_id: UUID, expires_in: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_refresh_token(self, user_id: UUID) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_refresh_token(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_token_to_blacklist(self, jti: UUID, user_id: UUID, expires_in: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_token_blacklisted(self, jti: UUID) -> bool:
        raise NotImplementedError
