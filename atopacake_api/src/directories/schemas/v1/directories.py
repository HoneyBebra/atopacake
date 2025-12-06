from uuid import UUID

from pydantic import BaseModel, Field

from src.core.schemas import Pagination


class CreateDirectorySchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class CreatedDirectorySchema(BaseModel):
    id: UUID


class Directories(BaseModel):
    id: UUID
    name: str = Field(min_length=3, max_length=50)


class DirectoriesWithPaginationSchema(BaseModel):
    directories: list[Directories]
    pagination: Pagination
