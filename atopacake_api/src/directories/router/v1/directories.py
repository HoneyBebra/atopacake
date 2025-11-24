from fastapi import APIRouter, Depends, Response, status

from src.core.dependencies.jwt import get_user_info_by_token
from src.core.schemas import UserInfoByTokenSchema

router = APIRouter(prefix="/directories")


@router.post(
    "",
    description="Create directory",
    summary="Create directory with cards",
    responses={
        status.HTTP_201_CREATED: {
            "model": None,
            "description": "Directory had been created"
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": None,
            "description": "Validation error",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        }
    },
)
async def create_directory(
        user_data: UserInfoByTokenSchema = Depends(get_user_info_by_token),
) -> Response:
    return user_data
