from datetime import timedelta
from typing import Any

from fastapi import Depends, Response

from src.auth.exceptions.user import UserAlreadyExists
from src.auth.schemas.v1.users import UserRegisterSchema, UserRegisterTgSchema
from src.auth.services.repositories.jwt_token import JwtTokenRepository
from src.auth.services.repositories.users import UsersRepository
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

    async def register(self, user_data: UserRegisterSchema, response: Response) -> Response:
        # TODO: make register all actions rollback when any errors raised

        already_used_field = await self.__get_already_used_field(
            email=user_data.email,
            phone_number=user_data.phone_number,
        )
        if already_used_field is not None:
            raise UserAlreadyExists(already_used_field)

        del user_data.confirm_password
        return await self.__base_create_user(user_data, response)

    async def register_tg(self, user_data: UserRegisterTgSchema, response: Response) -> Response:
        # TODO: make register all actions rollback when any errors raised

        already_used_field = await self.__get_already_used_field(
            tg_id=user_data.tg_id,
            tg_username=user_data.tg_username,
        )
        if already_used_field is not None:
            raise UserAlreadyExists(already_used_field)

        return await self.__base_create_user(user_data, response)

    async def __base_create_user(
            self,
            user_data: UserRegisterSchema | UserRegisterTgSchema,  # TODO: Make it through polymorphism or make it in view
            response: Response,
    ) -> Response:
        user = await self.users_repository.create(**dict(user_data))

        access_token = create_token(data={"sub": str(user.id)}, token_type="access")
        refresh_token = create_token(data={"sub": str(user.id)}, token_type="refresh")

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
