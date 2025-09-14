from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel, EmailStr, Field, model_validator

from src.auth.schemas.v1.base import validate_password


class UserRegisterSchema(BaseModel):
    # Web registration
    login: str | None = Field(default=None, min_length=3, max_length=50)
    password: Annotated[str | None, AfterValidator(validate_password)] = Field(default=None)
    confirm_password: Annotated[str | None, AfterValidator(validate_password)] = Field(default=None)
    email: EmailStr | None = Field(default=None)

    # TG registration
    tg_id: int | None = Field(default=None)
    tg_username: str | None = Field(default=None)

    phone_number: str | None = Field(default=None, pattern=r"^\+?1?\d{9,15}$")

    is_registration_from_tg: bool = Field(default=False)

    @model_validator(mode="after")  # type: ignore[arg-type]
    def check_fields_fullness(self, values: dict[str, Any]) -> dict[str, Any]:
        if values["is_registration_from_tg"]:
            if (
                values["tg_id"] is None or
                values["tg_username"] is None
            ):
                raise ValueError("tg_id and tg_username must be provided")
        else:
            if (
                values["login"] is None or
                values["password"] is None or
                values["confirm_password"] is None or
                values["email"] is None
            ):
                raise ValueError("login, password, confirm_password and email must be provided")

        return values

    @model_validator(mode="after")  # type: ignore[arg-type]
    def check_passwords_match(self, values: dict[str, Any]) -> dict[str, Any]:
        if values["password"] != values["confirm_password"]:
            raise ValueError("passwords do not match")
        return values
