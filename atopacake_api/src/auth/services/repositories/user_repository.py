# Maybe this will be moved to the auth service

from uuid import UUID

from src.auth.models.users import Users
from src.auth.services.repositories.base.base_users_repository import BaseUsersRepository
from src.auth.schemas.v1.users import UserSchema


class UsersRepository(BaseUsersRepository):
    async def create(self, user_data: UserSchema) -> Users:
        ...

    async def read(self, user_id: UUID) -> Users:
        ...

    async def update(self, user_data: UserSchema) -> Users:
        ...

    async def delete(self, user_id: UUID) -> None:
        ...
