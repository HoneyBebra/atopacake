from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.auth.exceptions.user import UserAlreadyExists
from src.auth.schemas.v1.users import UserRegisterSchema
from src.auth.services.users import UsersService

router = APIRouter(prefix="/users")


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(
        user_data: UserRegisterSchema,
        user_service: UsersService = Depends(),
) -> Response:
    response = Response()
    try:
        return await user_service.register(user_data, response)
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already created",
        ) from e
