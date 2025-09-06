# Maybe this will be moved to the auth service

from abc import ABC, abstractmethod
from uuid import UUID

from src.auth.models.users import Users


class BaseUsersRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(
            self,
            login: str,
            password: str,
            phone_number: str | None = None,
    ) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def read(
            self,
            user_id: UUID,
    ) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def update(
            self,
            user_id: UUID,
            login: str | None = None,
            password: str | None = None,
            phone_number: str | None = None,
    ) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def delete(
            self,
            user_id: UUID,
    ) -> None:
        raise NotImplementedError
