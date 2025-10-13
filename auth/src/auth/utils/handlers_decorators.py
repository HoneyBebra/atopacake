import time
from functools import wraps
from typing import Any, Callable, Literal

from pydantic import ValidationError
from fastapi import HTTPException, status, Depends

from src.auth.schemas.v1.users import UserJwtSchema
from src.auth.services.users import UsersService


class CheckJWT:
    def __init__(self, credentials_type: Literal["all", "refresh"]) -> None:
        self.credentials_type = credentials_type
        
        self.user_service: UsersService = Depends()

    def __call__(self, function) -> Callable[..., Any]:
        @wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Callable:
            # TODO: Check if secret key works

            raw_credentials = kwargs.get("jwt_credentials")
            if raw_credentials is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid credentials",
                )

            try:
                user_jwt_schema = UserJwtSchema(**raw_credentials.subject)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid credentials",
                ) from e

            if user_jwt_schema.iat + user_jwt_schema.exp < time.time():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token is outdated",
                )

            if await self.user_service.jwt_token_repository.is_token_in_blacklist(
                    jti=raw_credentials.subject.jti,
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token is outdated",
                )

            return await function(*args, **kwargs)

        return wrapper
