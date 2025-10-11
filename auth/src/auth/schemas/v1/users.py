from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, EmailStr, Field, model_validator

from src.auth.schemas.v1.base import validate_password


class UserRequestedDataBaseSchema(BaseModel):
    email: EmailStr | None
    phone_number: str | None = Field(pattern=r"^\+?1?\d{9,15}$")
    password: Annotated[str, AfterValidator(validate_password)]

    @model_validator(mode="before")
    def check_email_or_phone_number_exists(self) -> "UserRequestedDataBaseSchema":
        if not self.get("email") and self.get("phone_number") is not None:
            raise ValueError("email or phone number is required")
        return self


class UserRegisterSchema(UserRequestedDataBaseSchema):
    login: str = Field(min_length=3, max_length=50)
    confirm_password: Annotated[str, AfterValidator(validate_password)]

    @model_validator(mode="before")
    def check_passwords_match(self) -> "UserRegisterSchema":
        if self.get("password") != self.get("confirm_password"):
            raise ValueError("passwords do not match")
        return self


class UserLoginSchema(UserRequestedDataBaseSchema):
    pass


class UserJwtSchema(BaseModel):
    sub: UUID
    email: EmailStr | None
    phone_number: str | None = Field(pattern=r"^\+?1?\d{9,15}$")
    iat: int
    exp: int
