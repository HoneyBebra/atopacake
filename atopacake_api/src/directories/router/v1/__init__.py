from fastapi import APIRouter

from src.directories.router.v1.directories import router as directories_router

router = APIRouter(prefix="/directories")

router.include_router(directories_router, tags=["Directories"])
