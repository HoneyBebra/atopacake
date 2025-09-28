from abc import ABC, abstractmethod


class BaseJwtTokenRepository(ABC):
    @abstractmethod
    async def set_refresh_token(self, token: str, user_id: str, expires_in: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_refresh_token(self, user_id: str) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_refresh_token(self, token: str) -> None:
        raise NotImplementedError
