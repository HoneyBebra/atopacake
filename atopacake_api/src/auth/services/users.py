from datetime import timedelta

from fastapi import Depends, Response

from src.auth.exceptions.user import UserAlreadyExists
from src.auth.schemas.v1.users import UserRegisterSchema
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
        if await self.users_repository.read(user_data.id):
            raise UserAlreadyExists

        user = await self.users_repository.create(user_data)

        access_token = create_token(data={"sub": str(user.id)}, token_type="access")
        refresh_token = create_token(data={"sub": str(user.id)}, token_type="refresh")

        await self.jwt_token_repository.create_refresh_token(
            token=refresh_token,
            user_id=user.id,
            expires_in=timedelta(days=settings.refresh_token_expire_days)
        )

        settings.access_security.set_access_cookie(response, access_token)
        settings.refresh_security.set_refresh_cookie(response, refresh_token)

        return response
