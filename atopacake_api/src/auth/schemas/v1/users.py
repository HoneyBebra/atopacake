from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel, EmailStr, Field, model_validator

from src.auth.schemas.v1.base import validate_password


class UserRegisterBase(BaseModel):
    phone_number: str = Field(pattern=r"^\+?1?\d{9,15}$")


class UserRegisterSchema(UserRegisterBase):
    login: str = Field(min_length=3, max_length=50)
    password: Annotated[str, AfterValidator(validate_password)]
    confirm_password: Annotated[str, AfterValidator(validate_password)]
    email: EmailStr

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterSchema":
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


class UserRegisterTgSchema(UserRegisterBase):
    tg_id: int
    tg_username: str
