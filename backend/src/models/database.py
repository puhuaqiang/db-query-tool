"""Database models for connections and metadata."""

from datetime import datetime
from src.models import CamelModel


class FieldMetadata(CamelModel):
    """Field metadata model."""

    id: int
    field_name: str
    data_type: str
    is_nullable: bool = True
    column_default: str | None = None
    max_length: int | None = None
    chinese_name: str | None = None


class TableMetadata(CamelModel):
    """Table metadata model."""

    id: int
    table_name: str
    table_type: str  # 'TABLE' or 'VIEW'
    chinese_name: str | None = None
    fields: list[FieldMetadata] = []


class DatabaseConnection(CamelModel):
    """Database connection model."""

    id: int
    name: str
    db_type: str  # 'postgres' or 'mysql'
    created_at: datetime
    updated_at: datetime


class DatabaseConnectionDetail(DatabaseConnection):
    """Database connection with metadata."""

    tables: list[TableMetadata] = []


class AddDatabaseRequest(CamelModel):
    """Request to add a database connection."""

    url: str


class UpdateFieldRequest(CamelModel):
    """Request to update field chinese name."""

    chinese_name: str
