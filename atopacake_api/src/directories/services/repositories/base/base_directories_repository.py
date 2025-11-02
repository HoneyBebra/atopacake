from abc import ABC, abstractmethod
from uuid import UUID

from src.directories.schemas.v1.directories import DirectorySchema


class BaseDirectoriesRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(self, user_id: UUID, name: str) -> DirectorySchema:
        raise NotImplementedError

    @abstractmethod
    async def read_all(self, user_id: UUID) -> list[DirectorySchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: UUID, name: str) -> DirectorySchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, directory_id: UUID) -> None:
        raise NotImplementedError
