from fastapi import APIRouter

from src.cards.router.v1.cards import router as users_router

router = APIRouter(prefix="/directories")

router.include_router(users_router, tags=["Directories"])
