from typing import Any
from uuid import UUID

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    status: bool
    msg: str
    detail: dict[str, Any]


class UserInfoByTokenSchema(BaseModel):
    id: UUID


class Pagination(BaseModel):
    page: int
    count: int
    total_count: int
