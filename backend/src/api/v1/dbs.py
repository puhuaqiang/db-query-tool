"""Database API endpoints."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from src.models.database import (
    AddDatabaseRequest,
    DatabaseConnection,
    DatabaseConnectionDetail,
    UpdateFieldRequest,
    FieldMetadata,
)
from src.models.query import QueryRequest, QueryResult
from src.models.llm import NaturalQueryRequest, NaturalQueryResult
from src.models.errors import ErrorResponse
from src.services.database import get_database_service
from src.services.query import get_query_service
from src.services.export import get_export_service
from src.services.llm import get_llm_service
from src.storage.sqlite import get_storage

router = APIRouter()


@router.get(
    "",
    response_model=list[DatabaseConnection],
    summary="获取所有数据库连接",
)
async def get_databases() -> list[DatabaseConnection]:
    """Get all database connections."""
    service = get_database_service()
    return await service.get_all_connections()


@router.put(
    "/{name}",
    response_model=DatabaseConnectionDetail,
    responses={400: {"model": ErrorResponse}},
    summary="添加或更新数据库连接",
)
async def add_database(name: str, request: AddDatabaseRequest) -> DatabaseConnectionDetail:
    """Add or update a database connection."""
    try:
        service = get_database_service()
        return await service.add_connection(name, request.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"连接失败: {str(e)}")


@router.get(
    "/{name}",
    response_model=DatabaseConnectionDetail,
    responses={404: {"model": ErrorResponse}},
    summary="获取数据库详细信息",
)
async def get_database(name: str) -> DatabaseConnectionDetail:
    """Get database connection with metadata."""
    service = get_database_service()
    result = await service.get_connection(name)
    if result is None:
        raise HTTPException(status_code=404, detail=f"数据库连接 '{name}' 不存在")
    return result


@router.delete(
    "/{name}",
    status_code=204,
    responses={404: {"model": ErrorResponse}},
    summary="删除数据库连接",
)
async def delete_database(name: str) -> None:
    """Delete a database connection."""
    service = get_database_service()
    deleted = await service.delete_connection(name)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"数据库连接 '{name}' 不存在")


@router.post(
    "/{name}/refresh",
    response_model=DatabaseConnectionDetail,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="刷新数据库元数据",
)
async def refresh_metadata(name: str) -> DatabaseConnectionDetail:
    """Refresh metadata for a database connection."""
    service = get_database_service()
    result = await service.refresh_metadata(name)
    if result is None:
        raise HTTPException(status_code=404, detail=f"数据库连接 '{name}' 不存在")
    return result


@router.patch(
    "/{name}/tables/{table_name}/fields/{field_name}",
    response_model=FieldMetadata,
    responses={404: {"model": ErrorResponse}},
    summary="更新字段中文备注",
)
async def update_field_chinese_name(
    name: str, table_name: str, field_name: str, request: UpdateFieldRequest
) -> FieldMetadata:
    """Update the chinese name for a field."""
    storage = await get_storage()
    updated = await storage.update_field_chinese_name(
        name, table_name, field_name, request.chinese_name
    )
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"字段 '{field_name}' 在表 '{table_name}' 中不存在",
        )

    # Get the updated field
    conn = await storage.get_connection_with_metadata(name)
    if conn is None:
        raise HTTPException(status_code=404, detail=f"数据库连接 '{name}' 不存在")

    for table in conn.tables:
        if table.table_name == table_name:
            for field in table.fields:
                if field.field_name == field_name:
                    return field

    raise HTTPException(status_code=404, detail="字段未找到")


@router.post(
    "/{name}/query",
    response_model=QueryResult,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="执行 SQL 查询",
)
async def execute_query(name: str, request: QueryRequest) -> QueryResult:
    """Execute a SQL query against the database."""
    try:
        service = get_query_service()
        return await service.execute_query(name, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询执行失败: {str(e)}")


@router.post(
    "/{name}/query/export",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="导出查询结果",
)
async def export_query_result(
    name: str,
    request: QueryRequest,
    format: str = Query(..., description="导出格式: csv 或 json"),
) -> Response:
    """Execute a query and export results."""
    if format not in ("csv", "json"):
        raise HTTPException(status_code=400, detail="导出格式必须是 csv 或 json")

    try:
        # Execute query
        query_service = get_query_service()
        result = await query_service.execute_query(name, request)

        # Export
        export_service = get_export_service()
        if format == "csv":
            content = export_service.export_csv(result)
            return Response(
                content=content,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=query_result.csv"},
            )
        else:
            content = export_service.export_json(result)
            return Response(
                content=content,
                media_type="application/json",
                headers={"Content-Disposition": "attachment; filename=query_result.json"},
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post(
    "/{name}/query/natural",
    response_model=NaturalQueryResult,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="自然语言生成 SQL",
)
async def natural_query(name: str, request: NaturalQueryRequest) -> NaturalQueryResult:
    """Generate SQL from natural language query."""
    try:
        # Get database info
        db_service = get_database_service()
        database = await db_service.get_connection(name)
        if database is None:
            raise HTTPException(status_code=404, detail=f"数据库连接 '{name}' 不存在")

        # Generate SQL
        llm_service = get_llm_service()
        return await llm_service.generate_sql(request, database)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL 生成失败: {str(e)}")
