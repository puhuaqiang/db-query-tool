# Implementation Plan: 数据库查询工具

**Branch**: `001-db-query-tool` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-db-query-tool/spec.md`

## Summary

构建一个数据库查询工具，用户可以添加数据库连接（MySQL/PostgreSQL），系统自动获取并存储数据库元数据。支持直接 SQL 查询（仅 SELECT，自动添加 LIMIT 1000）和自然语言生成 SQL（通过 LLM）。前端使用 Monaco Editor 提供 SQL 编辑，结果以表格展示并支持导出 CSV/JSON。

## Technical Context

**Language/Version**: Python 3.11+ (后端), TypeScript 5.x (前端)
**Primary Dependencies**:
- 后端: FastAPI, sqlglot, Pydantic, dashscope SDK, openai SDK (for Kimi), asyncpg, aiomysql, aiosqlite
- 前端: Vue 3, Element Plus, Tailwind CSS, Monaco Editor, Axios
**Storage**: SQLite (元数据存储: ~/.db_query/db_query.db), MySQL/PostgreSQL (用户连接的数据库)
**Testing**: pytest + pytest-asyncio (后端), Vitest (前端)
**Target Platform**: Web 应用 (跨平台浏览器)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 查询响应 < 5秒, 支持 10000 行结果展示
**Constraints**: 仅允许 SELECT 语句, 默认 LIMIT 1000, 无需认证
**Scale/Scope**: 单用户本地工具, 支持多个数据库连接

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原则 | 要求 | 状态 |
|------|------|------|
| I. 类型安全 | Python 使用完整类型注解, TypeScript 启用 strict 模式, 使用 Pydantic 数据模型 | ✅ 符合 |
| II. 数据格式一致性 | 后端 JSON 使用 camelCase, Pydantic 配置 alias_generator | ✅ 符合 |
| III. 代码风格规范 | 后端 Ergonomic Python, 前端 TypeScript | ✅ 符合 |
| IV. 开放访问 | 无需认证, 所有 API 开放 | ✅ 符合 |
| V. 文档规范 | 中文文档存放于 ./docs | ✅ 符合 |

**技术栈约束检查**:
- 后端: Python + FastAPI + sqlglot + Pydantic ✅
- 前端: Vue 3 + TypeScript + Tailwind + Element Plus + Monaco Editor ✅
- 数据库: SQLite (元数据) + MySQL/PostgreSQL (用户数据库) ✅
- LLM: dashscope + Kimi ✅

## Project Structure

### Documentation (this feature)

```text
specs/001-db-query-tool/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # Pydantic models
│   │   ├── __init__.py
│   │   ├── database.py  # DatabaseConnection, DatabaseMetadata
│   │   ├── query.py     # QueryRequest, QueryResult
│   │   └── llm.py       # LLMConfig, NaturalQueryRequest
│   ├── services/        # Business logic
│   │   ├── __init__.py
│   │   ├── database.py  # Database connection management
│   │   ├── metadata.py  # Metadata extraction
│   │   ├── query.py     # SQL validation and execution
│   │   └── llm.py       # LLM integration
│   ├── api/             # FastAPI routers
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── dbs.py   # /api/v1/dbs endpoints
│   ├── storage/         # SQLite operations
│   │   ├── __init__.py
│   │   └── sqlite.py    # Local storage operations
│   ├── config.py        # Configuration
│   └── main.py          # FastAPI app entry
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pyproject.toml
└── requirements.txt

frontend/
├── src/
│   ├── components/      # Vue components
│   │   ├── DatabaseList.vue
│   │   ├── AddDatabaseDialog.vue
│   │   ├── TableList.vue
│   │   ├── FieldEditor.vue
│   │   ├── SqlEditor.vue
│   │   ├── NaturalQueryInput.vue
│   │   ├── QueryResult.vue
│   │   └── ExportDialog.vue
│   ├── pages/           # Page components
│   │   └── HomePage.vue
│   ├── services/        # API clients
│   │   ├── api.ts
│   │   └── types.ts
│   ├── stores/          # Pinia stores
│   │   └── database.ts
│   ├── App.vue
│   └── main.ts
├── tests/
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts

docs/
├── requirements_summary.md
├── design_summary.md
└── bugfixes_summary.md
```

**Structure Decision**: 采用 Web application 结构 (Option 2)，分离 backend 和 frontend 目录。后端使用 FastAPI 提供 REST API，前端使用 Vue 3 SPA。

## Complexity Tracking

> 本项目无 Constitution 违规，无需复杂性追踪。
