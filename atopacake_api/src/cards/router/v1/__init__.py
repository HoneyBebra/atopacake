from fastapi import APIRouter

from src.cards.router.v1.users import router as users_router

router = APIRouter(prefix="/cards")

router.include_router(users_router, tags=["Cards"])
