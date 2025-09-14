from fastapi import APIRouter

from src.auth.router.v1.users import router as tg_users_router

router = APIRouter(prefix="/auth")

router.include_router(tg_users_router, tags=["Users"])
