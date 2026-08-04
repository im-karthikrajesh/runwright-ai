from fastapi import APIRouter

from runwright.api.routes.analysis import router as analysis_router
from runwright.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(analysis_router, tags=["Analysis"])