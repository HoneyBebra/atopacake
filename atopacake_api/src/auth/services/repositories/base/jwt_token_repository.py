from abc import ABC, abstractmethod


class BaseJwtTokenRepository(ABC):
    @abstractmethod
    async def store_refresh_token(self, token: str, user_id: str, expires_in: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_refresh_token(self, token: str) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_refresh_token(self, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_user_tokens(self, user_id: str) -> None:
        raise NotImplementedError
