import time
from functools import wraps
from typing import Any, Callable, Literal

from fastapi import Depends, HTTPException, status

# TODO: jose is deprecated
from jose import JWTError, jwt
from pydantic import ValidationError

from src.auth.exceptions.inner import CredentialsAreNotProvided
from src.auth.schemas.v1.users import UserJwtSchema
from src.auth.services.users import UsersService
from src.core.config import settings


# TODO: Convert to DI to avoid duplicating payload calculations
class CheckJWT:
    def __init__(
            self,
            jwt_format: Literal["all", "access", "refresh"],
            user_service: UsersService = Depends()
    ) -> None:
        self.user_service = user_service

        self.jwt_format = jwt_format

        self.jwt_format_to_creds_name: dict = {
            "all": ["access_credentials", "refresh_credentials"],
            "access": ["access_credentials"],
            "refresh": ["refresh_credentials"],
        }

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Callable:
            for credentials_name in self.jwt_format_to_creds_name[self.jwt_format]:
                await self.__check_jwt_credentials(
                    credentials_name=credentials_name,
                    **kwargs,
                )

            return await function(*args, **kwargs)

        return wrapper

    async def __check_jwt_credentials(self, credentials_name: str, **kwargs: Any) -> None:
        raw_credentials = await self.__get_raw_credentials(
            credentials_name=credentials_name,
            **kwargs,
        )
        await self.__raise_if_jwt_in_blacklist(raw_credentials)
        payload = await self.__get_payload(raw_credentials)
        jwt_schema = await self.__get_jwt_schema(payload)
        await self.__raise_if_jwt_is_outdated(jwt_schema)

    async def __raise_if_jwt_in_blacklist(self, raw_credentials: str) -> None:
        if await self.user_service.jwt_token_repository.is_token_in_blacklist(raw_credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is outdated",
            )

    @staticmethod
    async def __get_payload(raw_credentials: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token=raw_credentials,
                key=settings.jwt_secret_key,
                algorithms=settings.jwt_algorithm,
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token validation error",
            ) from e

    @staticmethod
    async def __raise_if_jwt_is_outdated(user_jwt_schema: UserJwtSchema) -> None:
        if user_jwt_schema.iat + user_jwt_schema.exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is outdated",
            )

    @staticmethod
    async def __get_jwt_schema(payload: dict[str, Any]) -> None:
        try:
            return UserJwtSchema(**payload)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            ) from e

    @staticmethod
    async def __get_raw_credentials(credentials_name: str, **kwargs: Any) -> str:
        raw_credentials = kwargs.get(credentials_name)
        if raw_credentials is None:
            raise CredentialsAreNotProvided(credentials_name)
        return raw_credentials
