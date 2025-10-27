from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.users import Users
from src.auth.services.repositories.base.users import BaseUsersRepository
from src.db.postgres import get_session


class UsersRepository(BaseUsersRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def create(
            self,
            login: str,
            password_hash: str,
            encrypted_email: str | None = None,
            encrypted_phone_number: str | None = None,
            email_hash: str | None = None,
            phone_number_hash: str | None = None,
    ) -> Users:
        user = Users()

        user.login = login
        user.password = password_hash
        user.encrypted_email = encrypted_email
        user.encrypted_phone_number = encrypted_phone_number
        user.email_hash = email_hash
        user.phone_number_hash = phone_number_hash

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def read(
            self,
            login: str | None = None,
            phone_number_hash: str | None = None,
            email_hash: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            order_by: str | None = None,
    ) -> list[Users]:
        query = select(Users)

        if login is not None:
            query = query.where(Users.login == login)
        if phone_number_hash is not None:
            query = query.where(Users.phone_number_hash == phone_number_hash)
        if email_hash is not None:
            query = query.where(Users.email_hash == email_hash)
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
            phone_number: str | None = None,
            email: str | None = None,
    ) -> Users:
        ...

    async def delete(self, user_id: UUID) -> None:
        ...
