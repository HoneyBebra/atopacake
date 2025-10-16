import time
from functools import wraps
from typing import Any, Callable, Literal

from pydantic import ValidationError
from fastapi import HTTPException, status, Depends
from fastapi_jwt import JwtAuthorizationCredentials

from src.auth.schemas.v1.users import UserJwtSchema
from src.auth.services.users import UsersService


class CheckJWT:
    def __init__(self) -> None:
        self.user_service: UsersService = Depends()

    def __call__(self, function) -> Callable[..., Any]:
        @wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Callable:
            # TODO: Check if secret key works

            await self.__check_jwt_credentials(**kwargs)

            return await function(*args, **kwargs)

        return wrapper

    async def __check_jwt_credentials(self, **kwargs: Any) -> None:
        raw_credentials = await self.__get_raw_credentials(**kwargs)

        user_jwt_schema = await self.__get_user_jwt_schema(raw_credentials)

        await self.__raise_if_jwt_is_outdated(user_jwt_schema)

        await self.__raise_if_jwt_in_blacklist(user_jwt_schema)

    async def __raise_if_jwt_in_blacklist(
            self,
            raw_credentials: JwtAuthorizationCredentials,
    ) -> None:
        if await self.user_service.jwt_token_repository.is_token_in_blacklist(
                jti=raw_credentials.jti,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is outdated",
            )

    @staticmethod
    async def __raise_if_jwt_is_outdated(user_jwt_schema: UserJwtSchema) -> None:
        if user_jwt_schema.iat + user_jwt_schema.exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is outdated",
            )

    @staticmethod
    async def __get_user_jwt_schema(raw_credentials: JwtAuthorizationCredentials) -> UserJwtSchema:
        try:
            return UserJwtSchema(**raw_credentials.subject)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            ) from e

    @staticmethod
    async def __get_raw_credentials(**kwargs: Any) -> JwtAuthorizationCredentials:
        raw_credentials = kwargs.get("credentials")
        if raw_credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            )
        return raw_credentials
