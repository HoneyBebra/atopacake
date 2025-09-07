# Maybe this will be moved to the auth service

from src.auth.models.users import Users
from src.auth.schemas.v1.tg_users import TgUserSchema
from src.auth.services.repositories.base.base_tg_users_repository import BaseTgUsersRepository
from src.db.postgres import get_session


class TgUsersRepository(BaseTgUsersRepository):
    async def create(self, user_data: TgUserSchema) -> Users:
        async with get_session() as session:
            pass

    async def read(self, tg_id: int) -> Users:
        ...

    async def update(self, user_data: TgUserSchema) -> Users:
        ...

    async def delete(self, tg_id: int) -> None:
        ...
