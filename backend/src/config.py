"""Application configuration."""

import os
from pathlib import Path
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables."""

    # Database paths
    db_query_dir: Path = Path.home() / ".db_query"
    sqlite_db_path: Path = db_query_dir / "db_query.db"

    # LLM API Keys
    dashscope_api_key: str = os.environ.get("DASHSCOPE_API_KEY", "")
    moonshot_api_key: str = os.environ.get("MOONSHOT_API_KEY", "")

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

    # Query settings
    default_limit: int = 1000
    max_rows: int = 10000

    def __init__(self) -> None:
        """Ensure db_query_dir exists."""
        self.db_query_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
