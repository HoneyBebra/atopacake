from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry

from src.core.config import settings
from src.db.postgres import get_session
from src.directories.models.directories import Directories
from src.directories.services.repositories.base.directories import BaseDirectoriesRepository


class DirectoriesRepository(BaseDirectoriesRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    @retry(**settings.backoff_decorator_sqlalchemy_settings)
    async def create(self, user_id: UUID, name: str) -> Directories:
        directory = Directories()

        directory.user_id = user_id
        directory.name = name

        self.session.add(directory)
        await self.session.commit()
        await self.session.refresh(directory)

        return directory

    @retry(**settings.backoff_decorator_sqlalchemy_settings)
    async def read(
            self,
            user_id: UUID,
            offset: int,
            limit: int,
    ) -> list[Directories]:
        query = select(Directories)

        query = query.where(Directories.user_id == user_id)
        query = query.limit(limit)
        query = query.offset(offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    @retry(**settings.backoff_decorator_sqlalchemy_settings)
    async def update(self, user_id: UUID, name: str) -> Directories:
        ...

    @retry(**settings.backoff_decorator_sqlalchemy_settings)
    async def delete(self, directory_id: UUID) -> None:
        ...

    @retry(**settings.backoff_decorator_sqlalchemy_settings)
    async def get_total_elements(self, user_id: UUID) -> int:
        query = select(func.count()).where(Directories.user_id == user_id)

        result = await self.session.execute(query)

        return result.scalar()  # type: ignore[return-value]
