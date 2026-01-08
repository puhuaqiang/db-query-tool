"""Query models for SQL execution."""

from src.models import CamelModel


class QueryRequest(CamelModel):
    """Request to execute a SQL query."""

    sql: str


class Column(CamelModel):
    """Column definition in query result."""

    name: str
    type: str


class QueryResult(CamelModel):
    """Result of a SQL query execution."""

    columns: list[Column]
    rows: list[list]
    row_count: int
    execution_time: float  # milliseconds
