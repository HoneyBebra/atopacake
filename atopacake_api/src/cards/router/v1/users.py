from fastapi import APIRouter, Depends, Response

from src.core.dependencies.jwt import get_user_info_by_token
from src.core.schemas import UserInfoByTokenSchema

router = APIRouter(prefix="/cards")


@router.get("/test")
async def test_handler(
        user_data: UserInfoByTokenSchema = Depends(get_user_info_by_token),
) -> Response:
    return user_data
