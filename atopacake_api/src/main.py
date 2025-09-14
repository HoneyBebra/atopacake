import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from src.auth.router.v1 import router as auth_router
from src.core.config import settings
from src.core.logger import LOGGING

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=f"{settings.api_prefix}/openapi",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    default_response_class=ORJSONResponse
)

router = APIRouter(prefix=settings.api_prefix)
router.include_router(auth_router)
app.include_router(router)

if __name__ == "__main__":

    # TODO: migrate new PSQL schema

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=settings.log_level,
    )
