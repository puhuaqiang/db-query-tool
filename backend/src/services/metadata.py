"""Metadata extraction service."""

from typing import Any
import asyncpg
import aiomysql

from src.services.database import parse_db_url


class MetadataService:
    """Service for extracting database metadata."""

    async def fetch_metadata(self, url: str, db_type: str) -> list[dict[str, Any]]:
        """Fetch metadata from a database."""
        if db_type == "postgres":
            return await self._fetch_postgres_metadata(url)
        else:
            return await self._fetch_mysql_metadata(url)

    async def _fetch_postgres_metadata(self, url: str) -> list[dict[str, Any]]:
        """Fetch metadata from PostgreSQL database."""
        conn = await asyncpg.connect(url)
        try:
            # Get tables and views
            tables_query = """
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
            table_rows = await conn.fetch(tables_query)

            tables = []
            for table_row in table_rows:
                table_name = table_row["table_name"]
                table_type = "TABLE" if table_row["table_type"] == "BASE TABLE" else "VIEW"

                # Get columns for this table
                columns_query = """
                    SELECT
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        character_maximum_length
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = $1
                    ORDER BY ordinal_position
                """
                column_rows = await conn.fetch(columns_query, table_name)

                fields = [
                    {
                        "field_name": col["column_name"],
                        "data_type": col["data_type"],
                        "is_nullable": col["is_nullable"] == "YES",
                        "column_default": col["column_default"],
                        "max_length": col["character_maximum_length"],
                    }
                    for col in column_rows
                ]

                tables.append({
                    "table_name": table_name,
                    "table_type": table_type,
                    "fields": fields,
                })

            return tables
        finally:
            await conn.close()

    async def _fetch_mysql_metadata(self, url: str) -> list[dict[str, Any]]:
        """Fetch metadata from MySQL database."""
        parsed = parse_db_url(url)

        conn = await aiomysql.connect(
            host=parsed["host"],
            port=parsed["port"],
            user=parsed["user"],
            password=parsed["password"],
            db=parsed["database"],
        )
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Get tables and views
                await cursor.execute("""
                    SELECT table_name, table_type
                    FROM information_schema.tables
                    WHERE table_schema = DATABASE()
                    ORDER BY table_name
                """)
                table_rows = await cursor.fetchall()

                tables = []
                for table_row in table_rows:
                    table_name = table_row["TABLE_NAME"]
                    table_type = "TABLE" if table_row["TABLE_TYPE"] == "BASE TABLE" else "VIEW"

                    # Get columns for this table
                    await cursor.execute("""
                        SELECT
                            column_name,
                            data_type,
                            is_nullable,
                            column_default,
                            character_maximum_length
                        FROM information_schema.columns
                        WHERE table_schema = DATABASE() AND table_name = %s
                        ORDER BY ordinal_position
                    """, (table_name,))
                    column_rows = await cursor.fetchall()

                    fields = [
                        {
                            "field_name": col["COLUMN_NAME"],
                            "data_type": col["DATA_TYPE"],
                            "is_nullable": col["IS_NULLABLE"] == "YES",
                            "column_default": col["COLUMN_DEFAULT"],
                            "max_length": col["CHARACTER_MAXIMUM_LENGTH"],
                        }
                        for col in column_rows
                    ]

                    tables.append({
                        "table_name": table_name,
                        "table_type": table_type,
                        "fields": fields,
                    })

                return tables
        finally:
            conn.close()
