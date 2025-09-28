# Maybe this will be moved to the auth service

from abc import ABC, abstractmethod
from uuid import UUID

from src.auth.models.users import Users
from src.auth.schemas.v1.users import UserRegisterSchema


class BaseUsersRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(
            self,
            login: str | None = None,
            password: str | None = None,
            phone_number: str = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
    ) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def read(
            self,
            login: str | None = None,
            phone_number: str | None = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            order_by: str | None = None,
    ) -> list[Users]:
        raise NotImplementedError

    @abstractmethod
    async def update(
            self,
            user_id: UUID,
            login: str | None = None,
            password: str | None = None,
            phone_number: str = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
    ) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError
