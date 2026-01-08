# Tasks: 数据库查询工具

**Input**: Design documents from `/specs/001-db-query-tool/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project root directories: `backend/`, `frontend/`, `docs/`
- [x] T002 [P] Initialize Python project with uv in `backend/pyproject.toml`
- [x] T003 [P] Initialize Vue 3 + TypeScript project with Vite in `frontend/`
- [x] T004 [P] Configure Tailwind CSS in `frontend/tailwind.config.js`
- [x] T005 [P] Install Element Plus in `frontend/` and configure in `frontend/src/main.ts`
- [x] T006 [P] Install Monaco Editor package in `frontend/`
- [x] T007 [P] Configure TypeScript strict mode in `frontend/tsconfig.json`
- [x] T008 [P] Install backend dependencies (FastAPI, sqlglot, Pydantic, asyncpg, aiomysql, aiosqlite, dashscope, openai) in `backend/pyproject.toml`
- [x] T009 [P] Create `.gitignore` with Python and Node.js patterns
- [x] T010 [P] Create `docs/requirements_summary.md` with initial requirements
- [x] T011 [P] Create `docs/design_summary.md` with architecture overview

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T012 Create base Pydantic model with camelCase configuration in `backend/src/models/__init__.py`
- [x] T013 [P] Create configuration module with environment variables in `backend/src/config.py`
- [x] T014 [P] Create SQLite database schema and initialization in `backend/src/storage/sqlite.py`
- [x] T015 [P] Create FastAPI app entry with CORS middleware in `backend/src/main.py`
- [x] T016 [P] Create API router structure in `backend/src/api/__init__.py` and `backend/src/api/v1/__init__.py`
- [x] T017 [P] Create error response models in `backend/src/models/errors.py`
- [x] T018 [P] Create Axios API client base in `frontend/src/services/api.ts`
- [x] T019 [P] Create TypeScript type definitions in `frontend/src/services/types.ts`
- [x] T020 [P] Create Pinia store structure in `frontend/src/stores/database.ts`
- [x] T021 [P] Create main App.vue layout in `frontend/src/App.vue`
- [x] T022 Create HomePage.vue with basic layout in `frontend/src/pages/HomePage.vue`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - 数据库连接管理 (Priority: P1) 🎯 MVP

**Goal**: 用户能够添加、查看和管理数据库连接，系统自动获取数据库元数据

**Independent Test**: 添加一个 PostgreSQL 或 MySQL 连接，验证系统成功连接并显示表和视图列表

### Backend Implementation for US1

- [x] T023 [P] [US1] Create DatabaseConnection model in `backend/src/models/database.py`
- [x] T024 [P] [US1] Create TableMetadata model in `backend/src/models/database.py`
- [x] T025 [P] [US1] Create FieldMetadata model in `backend/src/models/database.py`
- [x] T026 [P] [US1] Create AddDatabaseRequest model in `backend/src/models/database.py`
- [x] T027 [US1] Implement SQLite storage operations for connections in `backend/src/storage/sqlite.py`
- [x] T028 [US1] Implement database URL parser in `backend/src/services/database.py`
- [x] T029 [US1] Implement PostgreSQL metadata extraction in `backend/src/services/metadata.py`
- [x] T030 [US1] Implement MySQL metadata extraction in `backend/src/services/metadata.py`
- [x] T031 [US1] Implement DatabaseService with connect/disconnect logic in `backend/src/services/database.py`
- [x] T032 [US1] Implement GET /dbs endpoint in `backend/src/api/v1/dbs.py`
- [x] T033 [US1] Implement PUT /dbs/{name} endpoint in `backend/src/api/v1/dbs.py`
- [x] T034 [US1] Implement GET /dbs/{name} endpoint in `backend/src/api/v1/dbs.py`
- [x] T035 [US1] Implement DELETE /dbs/{name} endpoint in `backend/src/api/v1/dbs.py`

### Frontend Implementation for US1

- [x] T036 [P] [US1] Create DatabaseList.vue component in `frontend/src/components/DatabaseList.vue`
- [x] T037 [P] [US1] Create AddDatabaseDialog.vue component in `frontend/src/components/AddDatabaseDialog.vue`
- [x] T038 [P] [US1] Create TableList.vue component in `frontend/src/components/TableList.vue`
- [x] T039 [US1] Implement database API client methods in `frontend/src/services/api.ts`
- [x] T040 [US1] Implement database store actions (fetchDatabases, addDatabase, deleteDatabase) in `frontend/src/stores/database.ts`
- [x] T041 [US1] Integrate DatabaseList and AddDatabaseDialog into HomePage.vue in `frontend/src/pages/HomePage.vue`
- [x] T042 [US1] Add error handling and loading states for database operations in `frontend/src/pages/HomePage.vue`

**Checkpoint**: User Story 1 complete - can add databases and view metadata

---

## Phase 4: User Story 2 - SQL 查询执行 (Priority: P1)

**Goal**: 用户能够输入 SQL 查询语句并执行，系统验证语法、限制为 SELECT、自动添加 LIMIT，结果以表格展示并支持导出

**Independent Test**: 输入 SELECT 语句，验证系统正确执行并以表格形式显示结果，支持 CSV/JSON 导出

### Backend Implementation for US2

- [x] T043 [P] [US2] Create QueryRequest model in `backend/src/models/query.py`
- [x] T044 [P] [US2] Create QueryResult model in `backend/src/models/query.py`
- [x] T045 [P] [US2] Create Column model in `backend/src/models/query.py`
- [x] T046 [US2] Implement SQL validation with sqlglot (SELECT only check) in `backend/src/services/query.py`
- [x] T047 [US2] Implement automatic LIMIT injection with sqlglot in `backend/src/services/query.py`
- [x] T048 [US2] Implement query execution for PostgreSQL in `backend/src/services/query.py`
- [x] T049 [US2] Implement query execution for MySQL in `backend/src/services/query.py`
- [x] T050 [US2] Implement CSV export formatter in `backend/src/services/export.py`
- [x] T051 [US2] Implement JSON export formatter in `backend/src/services/export.py`
- [x] T052 [US2] Implement POST /dbs/{name}/query endpoint in `backend/src/api/v1/dbs.py`
- [x] T053 [US2] Implement POST /dbs/{name}/query/export endpoint in `backend/src/api/v1/dbs.py`

### Frontend Implementation for US2

- [x] T054 [P] [US2] Create SqlEditor.vue component with Monaco Editor in `frontend/src/components/SqlEditor.vue`
- [x] T055 [P] [US2] Create QueryResult.vue component with ElTable in `frontend/src/components/QueryResult.vue`
- [x] T056 [P] [US2] Create ExportDialog.vue component in `frontend/src/components/ExportDialog.vue`
- [x] T057 [US2] Implement query API client methods in `frontend/src/services/api.ts`
- [x] T058 [US2] Implement query store actions (executeQuery, exportResult) in `frontend/src/stores/database.ts`
- [x] T059 [US2] Integrate SqlEditor, QueryResult, ExportDialog into HomePage.vue in `frontend/src/pages/HomePage.vue`
- [x] T060 [US2] Add SQL syntax error display in SqlEditor.vue in `frontend/src/components/SqlEditor.vue`
- [x] T061 [US2] Add execution time and row count display in QueryResult.vue in `frontend/src/components/QueryResult.vue`

**Checkpoint**: User Story 2 complete - can execute SQL queries and export results

---

## Phase 5: User Story 3 - 自然语言生成 SQL (Priority: P2)

**Goal**: 用户可以使用自然语言描述查询需求，系统利用 LLM 生成 SQL 语句

**Independent Test**: 输入自然语言描述（如"查询所有用户"），验证系统生成正确的 SQL 并可执行

### Backend Implementation for US3

- [x] T062 [P] [US3] Create NaturalQueryRequest model in `backend/src/models/llm.py`
- [x] T063 [P] [US3] Create NaturalQueryResult model in `backend/src/models/llm.py`
- [x] T064 [P] [US3] Create LlmModel model in `backend/src/models/llm.py`
- [x] T065 [US3] Implement dashscope (通义千问) LLM client in `backend/src/services/llm.py`
- [x] T066 [US3] Implement Kimi LLM client (OpenAI compatible) in `backend/src/services/llm.py`
- [x] T067 [US3] Implement LLM prompt template with metadata context in `backend/src/services/llm.py`
- [x] T068 [US3] Implement LLM response parsing and SQL extraction in `backend/src/services/llm.py`
- [x] T069 [US3] Implement POST /dbs/{name}/query/natural endpoint in `backend/src/api/v1/dbs.py`
- [x] T070 [US3] Implement GET /llm/models endpoint in `backend/src/api/v1/llm.py`

### Frontend Implementation for US3

- [x] T071 [P] [US3] Create NaturalQueryInput.vue component in `frontend/src/components/NaturalQueryInput.vue`
- [x] T072 [P] [US3] Create LlmModelSelector.vue component in `frontend/src/components/LlmModelSelector.vue`
- [x] T073 [US3] Implement natural query API client methods in `frontend/src/services/api.ts`
- [x] T074 [US3] Implement LLM store actions (fetchModels, executeNaturalQuery) in `frontend/src/stores/database.ts`
- [x] T075 [US3] Integrate NaturalQueryInput and LlmModelSelector into HomePage.vue in `frontend/src/pages/HomePage.vue`
- [x] T076 [US3] Add generated SQL preview and edit capability in `frontend/src/components/NaturalQueryInput.vue`
- [x] T077 [US3] Add LLM loading state and error handling in `frontend/src/components/NaturalQueryInput.vue`

**Checkpoint**: User Story 3 complete - can generate SQL from natural language

---

## Phase 6: User Story 4 - 数据库元数据管理 (Priority: P2)

**Goal**: 用户可以查看数据库的详细元数据信息，并为字段添加中文备注

**Independent Test**: 选择一个表，查看其字段列表，并为字段添加中文备注

### Backend Implementation for US4

- [x] T078 [P] [US4] Create UpdateFieldRequest model in `backend/src/models/database.py`
- [x] T079 [US4] Implement field chinese name update in SQLite storage in `backend/src/storage/sqlite.py`
- [x] T080 [US4] Implement POST /dbs/{name}/refresh endpoint in `backend/src/api/v1/dbs.py`
- [x] T081 [US4] Implement PATCH /dbs/{name}/tables/{tableName}/fields/{fieldName} endpoint in `backend/src/api/v1/dbs.py`

### Frontend Implementation for US4

- [x] T082 [P] [US4] Create FieldEditor.vue component with inline editing in `frontend/src/components/FieldEditor.vue`
- [x] T083 [US4] Implement metadata API client methods (refreshMetadata, updateFieldChineseName) in `frontend/src/services/api.ts`
- [x] T084 [US4] Implement metadata store actions in `frontend/src/stores/database.ts`
- [x] T085 [US4] Integrate FieldEditor into TableList.vue in `frontend/src/components/TableList.vue`
- [x] T086 [US4] Add refresh metadata button in DatabaseList.vue in `frontend/src/components/DatabaseList.vue`

**Checkpoint**: User Story 4 complete - can manage metadata and add Chinese annotations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T087 [P] Add comprehensive error handling middleware in `backend/src/main.py`
- [x] T088 [P] Add request logging middleware in `backend/src/main.py`
- [x] T089 [P] Add connection pool management for database connections in `backend/src/services/database.py`
- [x] T090 [P] Add frontend global error boundary in `frontend/src/App.vue`
- [x] T091 [P] Add responsive design adjustments in `frontend/src/App.vue`
- [x] T092 [P] Update `docs/design_summary.md` with final implementation details
- [x] T093 Run quickstart.md validation checklist
- [x] T094 Create backend startup script in `backend/run.py` or update `backend/pyproject.toml` scripts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 and US2 can proceed in parallel (both P1)
  - US3 depends on US1 (needs metadata context for LLM)
  - US4 depends on US1 (needs database connections)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

```text
Setup (Phase 1)
     ↓
Foundational (Phase 2)
     ↓
┌────┴────┐
↓         ↓
US1 (P1)  US2 (P1)  ← Can run in parallel
↓    ↘    ↓
↓     ↘   ↓
US4 (P2)  US3 (P2)  ← US3 needs US1 metadata, US4 needs US1 connections
     ↓
Polish (Phase 7)
```

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend (API must exist for frontend to call)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Backend and frontend model/component creation marked [P] can run in parallel
- US1 and US2 can be implemented in parallel after Foundational phase

---

## Parallel Execution Examples

### Setup Phase Parallel Tasks

```bash
# Launch all setup tasks in parallel:
T002: Initialize Python project
T003: Initialize Vue 3 project
T004: Configure Tailwind CSS
T005: Install Element Plus
T006: Install Monaco Editor
T007: Configure TypeScript strict
T008: Install backend dependencies
T009: Create .gitignore
T010: Create requirements_summary.md
T011: Create design_summary.md
```

### User Story 1 Backend Parallel Tasks

```bash
# Launch model creation in parallel:
T023: Create DatabaseConnection model
T024: Create TableMetadata model
T025: Create FieldMetadata model
T026: Create AddDatabaseRequest model
```

### User Story 1 Frontend Parallel Tasks

```bash
# Launch component creation in parallel:
T036: Create DatabaseList.vue
T037: Create AddDatabaseDialog.vue
T038: Create TableList.vue
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (数据库连接管理)
4. Complete Phase 4: User Story 2 (SQL 查询执行)
5. **STOP and VALIDATE**: Test database connection + SQL query end-to-end
6. Deploy/demo if ready - this is a working MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Can connect to databases
3. Add User Story 2 → Test independently → Can execute SQL queries (MVP!)
4. Add User Story 3 → Test independently → Can use natural language
5. Add User Story 4 → Test independently → Can manage metadata
6. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend uses camelCase JSON output per Constitution requirement
- Frontend TypeScript strict mode per Constitution requirement
