# Maybe this will be moved to the auth service

from abc import ABC, abstractmethod

from src.auth.models.users import Users
from src.auth.schemas.v1.tg_users import TgUserSchema


class BaseTgUsersRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(self, user_data: TgUserSchema) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def read(self, tg_id: int) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_data: TgUserSchema) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, tg_id: int) -> None:
        raise NotImplementedError
