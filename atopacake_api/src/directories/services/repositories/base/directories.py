from abc import ABC, abstractmethod
from uuid import UUID

from src.directories.models.directories import Directories


class BaseDirectoriesRepository(ABC):
    """Abstract class describing working with database."""

    @abstractmethod
    async def create(self, user_id: UUID, name: str) -> Directories:
        raise NotImplementedError

    @abstractmethod
    async def read(
            self,
            user_id: UUID,
            offset: int,
            limit: int,
    ) -> list[Directories]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: UUID, name: str) -> Directories:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, directory_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_total_elements(self, user_id: UUID) -> int:
        raise NotImplementedError
