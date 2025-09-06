from uuid import UUID

from pydantic import BaseModel, Field


class CreateTgUserSchema(BaseModel):
    user_id: UUID | None = Field(default=None)
    tg_id: UUID
    username: str


class CreatingTgUserResponseSchema(BaseModel):
    tg_id: UUID
