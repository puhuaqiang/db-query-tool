"""SQLite database storage operations."""

import aiosqlite
from pathlib import Path
from datetime import datetime
from src.config import get_settings
from src.models.database import (
    DatabaseConnection,
    DatabaseConnectionDetail,
    TableMetadata,
    FieldMetadata,
)

SCHEMA = """
-- 数据库连接
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    db_type TEXT NOT NULL CHECK (db_type IN ('postgres', 'mysql')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 表元数据
CREATE TABLE IF NOT EXISTS table_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    connection_id INTEGER NOT NULL,
    table_name TEXT NOT NULL,
    table_type TEXT NOT NULL CHECK (table_type IN ('TABLE', 'VIEW')),
    chinese_name TEXT,
    FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE,
    UNIQUE (connection_id, table_name)
);

-- 字段元数据
CREATE TABLE IF NOT EXISTS field_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    is_nullable BOOLEAN DEFAULT TRUE,
    column_default TEXT,
    max_length INTEGER,
    chinese_name TEXT,
    FOREIGN KEY (table_id) REFERENCES table_metadata(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_table_metadata_connection ON table_metadata(connection_id);
CREATE INDEX IF NOT EXISTS idx_field_metadata_table ON field_metadata(table_id);
"""


class SQLiteStorage:
    """SQLite storage for connections and metadata."""

    def __init__(self, db_path: Path | None = None) -> None:
        """Initialize storage with database path."""
        self.db_path = db_path or get_settings().sqlite_db_path

    async def initialize(self) -> None:
        """Initialize database schema."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(SCHEMA)
            await db.commit()

    async def _get_connection(self) -> aiosqlite.Connection:
        """Get database connection."""
        db = await aiosqlite.connect(self.db_path)
        db.row_factory = aiosqlite.Row
        return db

    # Connection operations
    async def get_all_connections(self) -> list[DatabaseConnection]:
        """Get all database connections."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT id, name, db_type, created_at, updated_at FROM connections ORDER BY name"
            )
            rows = await cursor.fetchall()
            return [
                DatabaseConnection(
                    id=row["id"],
                    name=row["name"],
                    db_type=row["db_type"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
                for row in rows
            ]

    async def get_connection_by_name(self, name: str) -> DatabaseConnection | None:
        """Get a database connection by name."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT id, name, url, db_type, created_at, updated_at FROM connections WHERE name = ?",
                (name,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return DatabaseConnection(
                id=row["id"],
                name=row["name"],
                db_type=row["db_type"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )

    async def get_connection_url(self, name: str) -> str | None:
        """Get the connection URL for a database."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT url FROM connections WHERE name = ?", (name,)
            )
            row = await cursor.fetchone()
            return row["url"] if row else None

    async def add_connection(
        self, name: str, url: str, db_type: str
    ) -> DatabaseConnection:
        """Add or update a database connection."""
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Try to update existing
            cursor = await db.execute(
                "UPDATE connections SET url = ?, db_type = ?, updated_at = ? WHERE name = ?",
                (url, db_type, now, name),
            )
            if cursor.rowcount == 0:
                # Insert new
                cursor = await db.execute(
                    "INSERT INTO connections (name, url, db_type, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (name, url, db_type, now, now),
                )
            await db.commit()

            # Get the connection
            cursor = await db.execute(
                "SELECT id, name, db_type, created_at, updated_at FROM connections WHERE name = ?",
                (name,),
            )
            row = await cursor.fetchone()
            return DatabaseConnection(
                id=row["id"],
                name=row["name"],
                db_type=row["db_type"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )

    async def delete_connection(self, name: str) -> bool:
        """Delete a database connection."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM connections WHERE name = ?", (name,)
            )
            await db.commit()
            return cursor.rowcount > 0

    # Metadata operations
    async def save_metadata(
        self,
        connection_name: str,
        tables: list[dict],
    ) -> None:
        """Save metadata for a connection."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Get connection ID
            cursor = await db.execute(
                "SELECT id FROM connections WHERE name = ?", (connection_name,)
            )
            row = await cursor.fetchone()
            if row is None:
                raise ValueError(f"Connection {connection_name} not found")
            connection_id = row["id"]

            # Delete existing metadata
            await db.execute(
                "DELETE FROM table_metadata WHERE connection_id = ?", (connection_id,)
            )

            # Insert new metadata
            for table in tables:
                cursor = await db.execute(
                    "INSERT INTO table_metadata (connection_id, table_name, table_type) VALUES (?, ?, ?)",
                    (connection_id, table["table_name"], table["table_type"]),
                )
                table_id = cursor.lastrowid

                for field in table.get("fields", []):
                    await db.execute(
                        """INSERT INTO field_metadata
                           (table_id, field_name, data_type, is_nullable, column_default, max_length)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (
                            table_id,
                            field["field_name"],
                            field["data_type"],
                            field.get("is_nullable", True),
                            field.get("column_default"),
                            field.get("max_length"),
                        ),
                    )

            await db.commit()

    async def get_connection_with_metadata(
        self, name: str
    ) -> DatabaseConnectionDetail | None:
        """Get a connection with its metadata."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Get connection
            cursor = await db.execute(
                "SELECT id, name, db_type, created_at, updated_at FROM connections WHERE name = ?",
                (name,),
            )
            conn_row = await cursor.fetchone()
            if conn_row is None:
                return None

            # Get tables
            cursor = await db.execute(
                """SELECT id, table_name, table_type, chinese_name
                   FROM table_metadata WHERE connection_id = ? ORDER BY table_name""",
                (conn_row["id"],),
            )
            table_rows = await cursor.fetchall()

            tables = []
            for table_row in table_rows:
                # Get fields for this table
                cursor = await db.execute(
                    """SELECT id, field_name, data_type, is_nullable, column_default, max_length, chinese_name
                       FROM field_metadata WHERE table_id = ? ORDER BY id""",
                    (table_row["id"],),
                )
                field_rows = await cursor.fetchall()

                fields = [
                    FieldMetadata(
                        id=f["id"],
                        field_name=f["field_name"],
                        data_type=f["data_type"],
                        is_nullable=bool(f["is_nullable"]),
                        column_default=f["column_default"],
                        max_length=f["max_length"],
                        chinese_name=f["chinese_name"],
                    )
                    for f in field_rows
                ]

                tables.append(
                    TableMetadata(
                        id=table_row["id"],
                        table_name=table_row["table_name"],
                        table_type=table_row["table_type"],
                        chinese_name=table_row["chinese_name"],
                        fields=fields,
                    )
                )

            return DatabaseConnectionDetail(
                id=conn_row["id"],
                name=conn_row["name"],
                db_type=conn_row["db_type"],
                created_at=datetime.fromisoformat(conn_row["created_at"]),
                updated_at=datetime.fromisoformat(conn_row["updated_at"]),
                tables=tables,
            )

    async def update_field_chinese_name(
        self, connection_name: str, table_name: str, field_name: str, chinese_name: str
    ) -> bool:
        """Update the chinese name for a field."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Get connection and table IDs
            cursor = await db.execute(
                """SELECT fm.id FROM field_metadata fm
                   JOIN table_metadata tm ON fm.table_id = tm.id
                   JOIN connections c ON tm.connection_id = c.id
                   WHERE c.name = ? AND tm.table_name = ? AND fm.field_name = ?""",
                (connection_name, table_name, field_name),
            )
            row = await cursor.fetchone()
            if row is None:
                return False

            await db.execute(
                "UPDATE field_metadata SET chinese_name = ? WHERE id = ?",
                (chinese_name, row["id"]),
            )
            await db.commit()
            return True


# Global storage instance
_storage: SQLiteStorage | None = None


async def get_storage() -> SQLiteStorage:
    """Get or create storage instance."""
    global _storage
    if _storage is None:
        _storage = SQLiteStorage()
        await _storage.initialize()
    return _storage
