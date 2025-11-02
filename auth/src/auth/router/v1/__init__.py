from fastapi import APIRouter

from src.auth.router.v1.users import router as users_router

router = APIRouter(prefix="/auth")

router.include_router(users_router, tags=["Auth"])
