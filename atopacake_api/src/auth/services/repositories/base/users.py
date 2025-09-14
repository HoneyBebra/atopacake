# Maybe this will be moved to the auth service

from abc import ABC, abstractmethod
from uuid import UUID

from src.auth.models.users import Users
from src.auth.schemas.v1.users import UserRegisterSchema


class BaseUsersRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(self, user_data: UserRegisterSchema) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def read(self, user_id: UUID) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_data: UserRegisterSchema) -> Users:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError
