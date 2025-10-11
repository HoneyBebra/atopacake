import time
from datetime import timedelta
from typing import Any

from fastapi import Depends, Response
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import ValidationError

from src.auth.exceptions.users import (
    InvalidCredentials,
    NoCredentialsData,
    TokenInBlackList,
    TokenIsOutdated,
    UserAlreadyExists,
)
from src.auth.models.users import Users
from src.auth.schemas.v1.users import UserJwtSchema, UserLoginSchema, UserRegisterSchema
from src.auth.services.repositories.jwt_token import JwtTokenRepository
from src.auth.services.repositories.users import UsersRepository
from src.auth.utils.encryption import verify_password
from src.auth.utils.jwt import create_token
from src.core.config import settings


class UsersService:
    def __init__(
            self,
            users_repository: UsersRepository = Depends(),
            jwt_token_repository: JwtTokenRepository = Depends(),
    ) -> None:
        self.users_repository = users_repository
        self.jwt_token_repository = jwt_token_repository

    async def create(self, user_data: UserRegisterSchema) -> Users:
        already_used_field = await self.__get_already_used_field(
            email=user_data.email,
            phone_number=user_data.phone_number,
        )
        if already_used_field is not None:
            raise UserAlreadyExists(already_used_field)

        del user_data.confirm_password
        user = await self.users_repository.create(**dict(user_data))
        return user

    async def login(
            self,
            user: Users,
            response: Response,
    ) -> Response:
        access_token = create_token(
            data=UserJwtSchema(
                sub=user.id,
                email=user.email,
                phone_number=user.phone_number,
                iat=time.time(),
                exp=timedelta(minutes=settings.refresh_token_expire_days),
            ),
            token_type="access",
        )
        refresh_token = create_token(
            data=UserJwtSchema(
                sub=user.id,
                email=user.email,
                phone_number=user.phone_number,
                iat=time.time(),
                exp=timedelta(days=settings.refresh_token_expire_days),
            ),
            token_type="refresh",
        )

        await self.jwt_token_repository.set_refresh_token(
            token=refresh_token,
            user_id=str(user.id),
            expires_in=timedelta(days=settings.refresh_token_expire_days)
        )

        settings.access_security.set_access_cookie(response, access_token)
        settings.refresh_security.set_refresh_cookie(response, refresh_token)

        return response

    async def __get_already_used_field(self, **params_to_search: Any) -> Any:
        for field, value in params_to_search.items():
            if await self.users_repository.read(**{field: value}):
                return field
        return None

    async def authenticate(self, user_data: UserLoginSchema) -> Users:
        if user_data.email is not None:
            users = await self.users_repository.read(email=user_data.email)
        elif user_data.phone_number is not None:
            users = await self.users_repository.read(phone_number=user_data.phone_number)
        else:
            raise InvalidCredentials("email or phone number is required")

        if not users or not verify_password(user_data.password, users[0].password):
            raise InvalidCredentials

        return users[0]

    async def verify_jwt(self, jwt_credentials: JwtAuthorizationCredentials) -> UserJwtSchema:
        # TODO: Maybe move in decorator
        # TODO: Check if secret key works

        try:
            user_jwt_schema = UserJwtSchema(**jwt_credentials.subject)
        except ValidationError as e:
            raise InvalidCredentials from e

        if user_jwt_schema.iat + user_jwt_schema.exp < time.time():
            raise TokenIsOutdated

        if not jwt_credentials:
            raise NoCredentialsData

        if await self.jwt_token_repository.is_token_in_blacklist(jti=jwt_credentials.jti):
            raise TokenInBlackList

        return user_jwt_schema
