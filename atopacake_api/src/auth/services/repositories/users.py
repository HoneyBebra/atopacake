# Maybe this will be moved to the auth service

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.auth.utils.encryption import hash_password
from src.db.postgres import get_session
from src.auth.models.users import Users
from src.auth.services.repositories.base.users import BaseUsersRepository


class UsersRepository(BaseUsersRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def create(
            self,
            login: str | None = None,
            password: str | None = None,
            phone_number: str = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
    ) -> Users:
        user = Users()

        user.login = login
        user.password = hash_password(password)
        user.email = email
        user.tg_id = tg_id
        user.tg_username = tg_username
        user.phone_number = phone_number

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def read(
            self,
            login: str | None = None,
            phone_number: str | None = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            order_by: str | None = None,
    ) -> list[Users]:
        query = select(Users)

        if login is not None:
            query = query.where(Users.login == login)
        if phone_number is not None:
            query = query.where(Users.phone_number == phone_number)
        if email is not None:
            query = query.where(Users.email == email)
        if tg_id is not None:
            query = query.where(Users.tg_id == tg_id)
        if tg_username is not None:
            query = query.where(Users.tg_username == tg_username)

        if order_by is not None:
            query = query.order_by(order_by)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(
            self,
            user_id: UUID,
            login: str | None = None,
            password: str | None = None,
            phone_number: str = None,
            email: str | None = None,
            tg_id: int | None = None,
            tg_username: str | None = None,
    ) -> Users:
        ...

    async def delete(self, user_id: UUID) -> None:
        ...
