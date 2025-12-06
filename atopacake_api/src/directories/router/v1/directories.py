from fastapi import APIRouter, Depends, Query, status

from src.core.dependencies.jwt import get_user_info_by_token
from src.core.schemas import UserInfoByTokenSchema
from src.directories.schemas.v1.directories import (
    CreatedDirectorySchema,
    CreateDirectorySchema,
    DirectoriesWithPaginationSchema,
)
from src.directories.services.directories import DirectoriesService

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
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Can not validating",
        },
    },
)
async def create_directory(
        directory_data: CreateDirectorySchema,
        directories_service: DirectoriesService = Depends(),
        user_data: UserInfoByTokenSchema = Depends(get_user_info_by_token),
) -> CreatedDirectorySchema:
    directory = await directories_service.create(
        directory_data=directory_data,
        user_id=user_data.id,
    )
    return {"id": directory.id}


@router.get(
    "",
    description="Read directories",
    summary="Read directories (all or by query)",
    responses={
        status.HTTP_200_OK: {
            "model": DirectoriesWithPaginationSchema,
            "description": "List of directories",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Wrong args",
        }
    },
)
async def read_directories(
        directories_service: DirectoriesService = Depends(),
        user_data: UserInfoByTokenSchema = Depends(get_user_info_by_token),
        page: int = Query(1, ge=1, description="Page number"),
        count: int = Query(10, ge=1, le=100, description="Elements count on the page")
) -> DirectoriesWithPaginationSchema:
    directories = await directories_service.read(
        user_id=user_data.id,
        page_num=page,
        elements_count=count,
    )
    total_count = await directories_service.get_total_elements(user_id=user_data.id)
    return {
        "directories": [
            {
                "id": directory.id,
                "name": directory.name,
            }
            for directory in directories
        ],
        "pagination": {
            "page": page,
            "count": count,
            "total_count": total_count,
        }
    }
