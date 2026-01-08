"""Error response models."""

from src.models import CamelModel


class ErrorResponse(CamelModel):
    """Standard error response."""

    error: str
    message: str
    detail: str | None = None
