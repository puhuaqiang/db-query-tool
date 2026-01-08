"""LLM API endpoints."""

from fastapi import APIRouter

from src.models.llm import LlmModel
from src.services.llm import get_llm_service

router = APIRouter()


@router.get(
    "/models",
    response_model=list[LlmModel],
    summary="获取可用的 LLM 模型列表",
)
async def get_llm_models() -> list[LlmModel]:
    """Get list of available LLM models."""
    service = get_llm_service()
    return service.get_available_models()
