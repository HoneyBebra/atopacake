from uuid import UUID

from pydantic import BaseModel, Field


class TgUserSchema(BaseModel):
    user_id: UUID | None = Field(default=None)
    tg_id: UUID
    username: str


class TgUserResponseSchema(BaseModel):
    tg_id: UUID
