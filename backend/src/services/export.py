"""Export service for query results."""

import csv
import json
import io
from typing import Any

from src.models.query import QueryResult


class ExportService:
    """Service for exporting query results."""

    def export_csv(self, result: QueryResult) -> str:
        """Export query result to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([col.name for col in result.columns])

        # Write data rows
        for row in result.rows:
            writer.writerow([self._format_csv_value(val) for val in row])

        return output.getvalue()

    def export_json(self, result: QueryResult) -> str:
        """Export query result to JSON format."""
        # Convert to list of dictionaries
        data = []
        column_names = [col.name for col in result.columns]

        for row in result.rows:
            record = {}
            for i, value in enumerate(row):
                record[column_names[i]] = value
            data.append(record)

        return json.dumps(data, ensure_ascii=False, indent=2, default=str)

    def _format_csv_value(self, value: Any) -> str:
        """Format a value for CSV output."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


# Global service instance
_export_service: ExportService | None = None


def get_export_service() -> ExportService:
    """Get export service instance."""
    global _export_service
    if _export_service is None:
        _export_service = ExportService()
    return _export_service
