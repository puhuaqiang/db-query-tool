"""API v1 router."""

from fastapi import APIRouter

from src.api.v1.dbs import router as dbs_router
from src.api.v1.llm import router as llm_router

api_router = APIRouter()

# Include sub-routers
api_router.include_router(dbs_router, prefix="/dbs", tags=["databases"])
api_router.include_router(llm_router, prefix="/llm", tags=["llm"])
