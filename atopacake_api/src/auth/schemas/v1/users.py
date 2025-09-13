from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    user_id: UUID | None = Field(default=None)
    login: str | None = Field(default=None)
    password: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
