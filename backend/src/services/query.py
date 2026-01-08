"""Query service for SQL validation and execution."""

import time
from typing import Any
import sqlglot
from sqlglot import exp
import asyncpg
import aiomysql

from src.config import get_settings
from src.models.query import QueryRequest, QueryResult, Column
from src.services.database import parse_db_url
from src.storage.sqlite import get_storage


class QueryService:
    """Service for SQL query validation and execution."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def validate_sql(self, sql: str, dialect: str = "postgres") -> tuple[bool, str]:
        """
        Validate SQL query.
        Returns (is_valid, error_message).
        Only SELECT statements are allowed.
        """
        try:
            # Parse the SQL
            statements = sqlglot.parse(sql, dialect=dialect)

            if not statements:
                return False, "无法解析 SQL 语句"

            if len(statements) > 1:
                return False, "只允许执行单条 SQL 语句"

            statement = statements[0]

            if statement is None:
                return False, "无法解析 SQL 语句"

            # Check if it's a SELECT statement
            if not isinstance(statement, exp.Select):
                return False, "只允许执行 SELECT 语句"

            return True, ""

        except sqlglot.errors.ParseError as e:
            return False, f"SQL 语法错误: {str(e)}"
        except Exception as e:
            return False, f"SQL 验证失败: {str(e)}"

    def inject_limit(self, sql: str, dialect: str = "postgres", limit: int | None = None) -> str:
        """
        Inject LIMIT clause if not present.
        Returns the modified SQL.
        """
        if limit is None:
            limit = self.settings.default_limit

        try:
            statements = sqlglot.parse(sql, dialect=dialect)
            if not statements or statements[0] is None:
                return sql

            statement = statements[0]

            # Check if LIMIT already exists
            if statement.find(exp.Limit) is not None:
                return sql

            # Add LIMIT
            statement = statement.limit(limit)
            return statement.sql(dialect=dialect)

        except Exception:
            # If parsing fails, return original SQL
            return sql

    async def execute_query(
        self,
        db_name: str,
        request: QueryRequest,
    ) -> QueryResult:
        """Execute a SQL query against a database."""
        # Get connection URL
        storage = await get_storage()
        url = await storage.get_connection_url(db_name)
        if url is None:
            raise ValueError(f"数据库连接 '{db_name}' 不存在")

        parsed = parse_db_url(url)
        dialect = parsed["db_type"]

        # Validate SQL
        is_valid, error = self.validate_sql(request.sql, dialect)
        if not is_valid:
            raise ValueError(error)

        # Inject LIMIT if needed
        sql = self.inject_limit(request.sql, dialect)

        # Execute query
        start_time = time.time()

        if dialect == "postgres":
            result = await self._execute_postgres(url, sql)
        else:
            result = await self._execute_mysql(url, sql, parsed)

        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return QueryResult(
            columns=result["columns"],
            rows=result["rows"],
            row_count=len(result["rows"]),
            execution_time=round(execution_time, 2),
        )

    async def _execute_postgres(self, url: str, sql: str) -> dict[str, Any]:
        """Execute query on PostgreSQL."""
        conn = await asyncpg.connect(url)
        try:
            # Execute query
            records = await conn.fetch(sql)

            if not records:
                return {"columns": [], "rows": []}

            # Get column info from first record
            columns = [
                Column(name=key, type=self._get_type_name(records[0][key]))
                for key in records[0].keys()
            ]

            # Convert records to rows
            rows = [[self._serialize_value(record[col.name]) for col in columns] for record in records]

            return {"columns": columns, "rows": rows}

        finally:
            await conn.close()

    async def _execute_mysql(self, url: str, sql: str, parsed: dict) -> dict[str, Any]:
        """Execute query on MySQL."""
        conn = await aiomysql.connect(
            host=parsed["host"],
            port=parsed["port"],
            user=parsed["user"],
            password=parsed["password"],
            db=parsed["database"],
        )
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql)
                records = await cursor.fetchall()

                if not records:
                    return {"columns": [], "rows": []}

                # Get columns from first record
                first_record = records[0]
                columns = [
                    Column(name=key, type=self._get_type_name(first_record[key]))
                    for key in first_record.keys()
                ]

                # Convert records to rows
                rows = [
                    [self._serialize_value(record[col.name]) for col in columns]
                    for record in records
                ]

                return {"columns": columns, "rows": rows}

        finally:
            conn.close()

    def _get_type_name(self, value: Any) -> str:
        """Get type name for a value."""
        if value is None:
            return "null"
        type_name = type(value).__name__
        type_map = {
            "int": "integer",
            "float": "number",
            "str": "string",
            "bool": "boolean",
            "datetime": "datetime",
            "date": "date",
            "time": "time",
            "Decimal": "decimal",
            "bytes": "binary",
        }
        return type_map.get(type_name, type_name)

    def _serialize_value(self, value: Any) -> Any:
        """Serialize value for JSON response."""
        if value is None:
            return None
        if isinstance(value, (int, float, str, bool)):
            return value
        if hasattr(value, "isoformat"):
            return value.isoformat()
        if isinstance(value, bytes):
            return value.hex()
        return str(value)


# Global service instance
_query_service: QueryService | None = None


def get_query_service() -> QueryService:
    """Get query service instance."""
    global _query_service
    if _query_service is None:
        _query_service = QueryService()
    return _query_service
