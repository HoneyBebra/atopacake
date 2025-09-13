import re
from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr, Field


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    return password


class UserLogin(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: Annotated[str, AfterValidator(validate_password)]


class UserRegister(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: Annotated[str, AfterValidator(validate_password)]
    confirm_password: Annotated[str, AfterValidator(validate_password)]
    phone_number: str | None = Field(default=None, pattern=r"^\+?1?\d{9,15}$")

    # TODO: make passwords match check


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: Annotated[str, AfterValidator(validate_password)]
    confirm_password: Annotated[str, AfterValidator(validate_password)]

    # TODO: make passwords match check
