from typing import Any

from fastapi import Depends, Response

from src.auth.exceptions.users import InvalidCredentials, UserAlreadyExists
from src.auth.models.users import Users
from src.auth.schemas.v1.users import UserLoginSchema, UserRegisterSchema
from src.auth.services.repositories.jwt_token import JwtTokenRepository
from src.auth.services.repositories.users import UsersRepository
from src.auth.utils.encryption import verify_password, hash_user_data, hash_password, encrypt_data
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
        email_hash = hash_user_data(user_data.email)
        phone_number_hash = hash_user_data(user_data.phone_number)
        password_hash = hash_password(password=user_data.password)
        encrypted_email = encrypt_data(user_data.email)
        encrypt_phone_number = encrypt_data(user_data.phone_number)

        already_used_field = await self.__get_already_used_field(
            email_hash=email_hash,
            phone_number_hash=phone_number_hash,
        )
        if already_used_field is not None:
            raise UserAlreadyExists(already_used_field)

        user = await self.users_repository.create(
            login=user_data.login,
            password_hash=password_hash,
            encrypted_email=encrypted_email,
            encrypted_phone_number=encrypt_phone_number,
            email_hash=email_hash,
            phone_number_hash=phone_number_hash,
        )
        return user

    async def authenticate(self, user_data: UserLoginSchema) -> Users:
        if user_data.email is not None:
            users = await self.users_repository.read(email_hash=hash_user_data(user_data.email))
        elif user_data.phone_number is not None:
            users = await self.users_repository.read(
                phone_number_hash=hash_user_data(user_data.phone_number),
            )
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

    async def add_token_to_blacklist(
            self,
            token: str,
            expires_in: int,
    ) -> None:
        await self.jwt_token_repository.set_token_to_blacklist(
            token=token,
            expires_in=expires_in,
        )

    @staticmethod
    async def add_tokens_to_response(
            user_id: str,
            response: Response,
    ) -> Response:
        access_token = await create_token(
            sub=user_id,
            token_type="access",
        )
        refresh_token = await create_token(
            sub=user_id,
            token_type="refresh",
        )

        response.set_cookie(
            key=settings.access_token_key_in_cookie,
            value=access_token,
            httponly=True,
            secure=True,
        )
        response.set_cookie(
            key=settings.refresh_token_key_in_cookie,
            value=refresh_token,
            httponly=True,
            secure=True,
        )

        return response
