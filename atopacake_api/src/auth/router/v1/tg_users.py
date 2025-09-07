from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.schemas.v1.tg_users import TgUserSchema, TgUserResponseSchema
from src.auth.schemas.v1.users import UserSchema
from src.auth.services.repositories.tg_users_repository import TgUsersRepository
from src.auth.services.repositories.user_repository import UsersRepository

router = APIRouter(prefix="/tg-users")


@router.post("/signup", status_code=status.HTTP_200_OK)
async def create_user(
    user_data: TgUserSchema,
    tg_user_repository: TgUsersRepository = Depends(),
    user_repository: UsersRepository = Depends(),
) -> TgUserResponseSchema:
    if await tg_user_repository.read(user_data.tg_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already created")

    if user_data.user_id is None:
        user = await user_repository.create(
            UserSchema(user_id=None, login=None, password=None, phone_number=None)
        )
        user_data.user_id = user.id

    tg_user = await tg_user_repository.create(user_data)
    return TgUserResponseSchema(tg_id=tg_user.tg_user.tg_id)
