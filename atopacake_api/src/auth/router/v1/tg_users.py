from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.schemas.v1.tg_users import CreateTgUserSchema, CreatingTgUserResponseSchema
from src.auth.services.repositories.tg_users_repository import TgUsersRepository

router = APIRouter(prefix="/tg-users")


@router.post("/signup", status_code=status.HTTP_200_OK)
async def create_user(
    user_data: CreateTgUserSchema,
    user_repository: TgUsersRepository = Depends()
) -> CreatingTgUserResponseSchema:
    user_exist = await user_repository.read(user_data.tg_id)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already created")
    user = await user_repository.create(user_data)
    return CreatingTgUserResponseSchema(tg_id=user.tg_user.tg_id)
