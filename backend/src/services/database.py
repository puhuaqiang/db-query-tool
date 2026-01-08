"""Database connection service."""

from urllib.parse import urlparse
from typing import Any
import asyncpg
import aiomysql

from src.storage.sqlite import get_storage
from src.models.database import DatabaseConnection, DatabaseConnectionDetail


def parse_db_url(url: str) -> dict[str, Any]:
    """Parse a database URL into components."""
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    # Normalize scheme
    if scheme in ("postgres", "postgresql"):
        db_type = "postgres"
    elif scheme == "mysql":
        db_type = "mysql"
    else:
        raise ValueError(f"Unsupported database type: {scheme}")

    return {
        "db_type": db_type,
        "host": parsed.hostname or "localhost",
        "port": parsed.port or (5432 if db_type == "postgres" else 3306),
        "user": parsed.username or "",
        "password": parsed.password or "",
        "database": parsed.path.lstrip("/") if parsed.path else "",
    }


class DatabaseService:
    """Service for database connection management."""

    async def get_all_connections(self) -> list[DatabaseConnection]:
        """Get all database connections."""
        storage = await get_storage()
        return await storage.get_all_connections()

    async def get_connection(self, name: str) -> DatabaseConnectionDetail | None:
        """Get a database connection with metadata."""
        storage = await get_storage()
        return await storage.get_connection_with_metadata(name)

    async def add_connection(self, name: str, url: str) -> DatabaseConnectionDetail:
        """Add a database connection and fetch metadata."""
        from src.services.metadata import MetadataService

        # Parse URL to get db_type
        parsed = parse_db_url(url)
        db_type = parsed["db_type"]

        # Save connection
        storage = await get_storage()
        await storage.add_connection(name, url, db_type)

        # Fetch and save metadata
        metadata_service = MetadataService()
        tables = await metadata_service.fetch_metadata(url, db_type)
        await storage.save_metadata(name, tables)

        # Return connection with metadata
        result = await storage.get_connection_with_metadata(name)
        if result is None:
            raise RuntimeError("Failed to retrieve saved connection")
        return result

    async def delete_connection(self, name: str) -> bool:
        """Delete a database connection."""
        storage = await get_storage()
        return await storage.delete_connection(name)

    async def refresh_metadata(self, name: str) -> DatabaseConnectionDetail | None:
        """Refresh metadata for a connection."""
        from src.services.metadata import MetadataService

        storage = await get_storage()
        url = await storage.get_connection_url(name)
        if url is None:
            return None

        # Parse URL and fetch metadata
        parsed = parse_db_url(url)
        metadata_service = MetadataService()
        tables = await metadata_service.fetch_metadata(url, parsed["db_type"])
        await storage.save_metadata(name, tables)

        return await storage.get_connection_with_metadata(name)

    async def test_connection(self, url: str) -> bool:
        """Test if a database connection is valid."""
        parsed = parse_db_url(url)

        try:
            if parsed["db_type"] == "postgres":
                conn = await asyncpg.connect(url)
                await conn.close()
            else:  # mysql
                conn = await aiomysql.connect(
                    host=parsed["host"],
                    port=parsed["port"],
                    user=parsed["user"],
                    password=parsed["password"],
                    db=parsed["database"],
                )
                conn.close()
            return True
        except Exception:
            return False


# Global service instance
_db_service: DatabaseService | None = None


def get_database_service() -> DatabaseService:
    """Get database service instance."""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service
