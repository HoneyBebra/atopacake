from datetime import timedelta
from typing import Any

from fastapi import Depends, Response

from src.auth.exceptions.users import InvalidCredentials, UserAlreadyExists
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

    async def __get_already_used_field(self, **params_to_search: Any) -> Any:
        for field, value in params_to_search.items():
            if await self.users_repository.read(**{field: value}):
                return field
        return None

    async def add_token_to_blacklist(self, token: str) -> None:
        await self.jwt_token_repository.set_token_to_blacklist(
            token=token,
            expires_in=settings.refresh_token_expire,
        )

    @staticmethod
    async def refresh_token(
            refresh_payload: dict[str, Any],
            response: Response,
    ) -> Response:
        user_jwt_schema = UserJwtSchema(**refresh_payload)

        access_token = await create_token(
            sub=user_jwt_schema.id,
            email=user_jwt_schema.email,
            phone_number=user_jwt_schema.phone_number,
            token_type="access",
        )

        settings.access_security.set_access_cookie(
            response=response,
            access_token=access_token,
            expires_delta=timedelta(seconds=settings.access_token_expire),
        )
        return response

    @staticmethod
    async def login(
            user: Users,
            response: Response,
    ) -> Response:
        access_token = await create_token(
            sub=user.id,
            email=user.email,
            phone_number=user.phone_number,
            token_type="access",
        )
        refresh_token = await create_token(
            sub=user.id,
            email=user.email,
            phone_number=user.phone_number,
            token_type="refresh",
        )

        response.set_cookie(
            key=settings.access_token_key_in_cookie,
            value=access_token,
            httponly=True,
        )
        response.set_cookie(
            key=settings.refresh_token_key_in_cookie,
            value=refresh_token,
            httponly=True,
        )

        return response
