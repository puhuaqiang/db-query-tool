"""LLM models for natural language SQL generation."""

from src.models import CamelModel


class LlmModel(CamelModel):
    """Available LLM model information."""

    id: str
    name: str
    provider: str


class NaturalQueryRequest(CamelModel):
    """Request for natural language to SQL conversion."""

    prompt: str
    model_id: str = "qwen-coder-plus"


class NaturalQueryResult(CamelModel):
    """Result of natural language SQL generation."""

    sql: str
    explanation: str | None = None
    model_id: str
