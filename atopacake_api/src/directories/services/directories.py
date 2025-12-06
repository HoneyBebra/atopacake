from uuid import UUID

from fastapi import Depends

from src.directories.models.directories import Directories
from src.directories.schemas.v1.directories import CreateDirectorySchema
from src.directories.services.repositories.directories import DirectoriesRepository


class DirectoriesService:
    def __init__(
            self,
            directories_repository: DirectoriesRepository = Depends(),
    ) -> None:
        self.directories_repository = directories_repository

    async def create(
            self,
            directory_data: CreateDirectorySchema,
            user_id: UUID,
    ) -> Directories:
        return await self.directories_repository.create(
            user_id=user_id,
            name=directory_data.name,
        )

    async def read(
            self,
            user_id: UUID,
            page_num: int,
            elements_count: int,
    ) -> list[Directories]:
        return await self.directories_repository.read(
            user_id=user_id,
            limit=elements_count,
            offset=page_num * elements_count - elements_count,
        )

    async def get_total_elements(self, user_id: UUID) -> int:
        return await self.directories_repository.get_total_elements(user_id=user_id)
