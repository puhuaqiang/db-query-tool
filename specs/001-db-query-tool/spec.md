# Feature Specification: 数据库查询工具

**Feature Branch**: `001-db-query-tool`
**Created**: 2026-01-08
**Status**: Draft
**Input**: 用户描述: 数据库查询工具，支持添加数据库连接、查看元数据、SQL 查询和自然语言生成 SQL

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 数据库连接管理 (Priority: P1)

用户需要能够添加和管理数据库连接。用户输入数据库连接字符串（URL），系统连接到数据库并自动获取数据库的元数据信息（表、视图、字段等），将这些信息存储到本地 SQLite 数据库中以便后续使用。

**Why this priority**: 数据库连接是所有后续功能的基础，没有数据库连接就无法进行任何查询操作。

**Independent Test**: 可以通过添加一个数据库连接，验证系统是否成功连接并显示数据库的表和视图列表。

**Acceptance Scenarios**:

1. **Given** 用户在界面上, **When** 输入有效的 PostgreSQL 连接字符串并提交, **Then** 系统成功连接并显示该数据库的所有表和视图
2. **Given** 用户在界面上, **When** 输入有效的 MySQL 连接字符串并提交, **Then** 系统成功连接并显示该数据库的所有表和视图
3. **Given** 用户输入无效的连接字符串, **When** 提交连接请求, **Then** 系统显示明确的错误信息说明连接失败原因
4. **Given** 用户已添加多个数据库连接, **When** 查看连接列表, **Then** 可以看到所有已保存的数据库连接

---

### User Story 2 - SQL 查询执行 (Priority: P1)

用户需要能够直接输入 SQL 查询语句并执行。系统对 SQL 进行语法验证，确保只允许 SELECT 语句，执行查询后将结果以表格形式展示，并支持导出。

**Why this priority**: SQL 查询是工具的核心功能，用户需要能够快速执行查询并查看结果。

**Independent Test**: 可以通过输入一条 SELECT 语句，验证系统是否正确执行并以表格形式显示结果。

**Acceptance Scenarios**:

1. **Given** 用户已连接到数据库, **When** 输入有效的 SELECT 语句并执行, **Then** 系统显示查询结果表格
2. **Given** 用户输入不包含 LIMIT 的 SELECT 语句, **When** 执行查询, **Then** 系统自动添加 LIMIT 1000 并执行
3. **Given** 用户输入非 SELECT 语句（如 INSERT、UPDATE、DELETE）, **When** 尝试执行, **Then** 系统拒绝执行并提示只允许 SELECT 语句
4. **Given** 用户输入语法错误的 SQL, **When** 尝试执行, **Then** 系统显示具体的语法错误信息
5. **Given** 查询结果已显示, **When** 用户选择导出为 CSV, **Then** 系统生成并下载 CSV 文件
6. **Given** 查询结果已显示, **When** 用户选择导出为 JSON, **Then** 系统生成并下载 JSON 文件

---

### User Story 3 - 自然语言生成 SQL (Priority: P2)

用户可以使用自然语言描述查询需求，系统利用 LLM 将自然语言转换为 SQL 查询语句。用户可以查看生成的 SQL，确认后执行查询。

**Why this priority**: 自然语言查询降低了使用门槛，但需要在基础 SQL 查询功能完成后实现。

**Independent Test**: 可以通过输入自然语言描述（如"查询所有用户"），验证系统是否生成正确的 SQL 并执行。

**Acceptance Scenarios**:

1. **Given** 用户已连接到数据库, **When** 输入自然语言描述（如"查询用户表的所有信息"）, **Then** 系统生成对应的 SELECT SQL 语句
2. **Given** 系统生成了 SQL 语句, **When** 用户查看并确认, **Then** 可以直接执行该 SQL
3. **Given** 系统生成了 SQL 语句, **When** 用户想要修改, **Then** 可以在 SQL 编辑器中编辑后再执行
4. **Given** 用户选择不同的 LLM 模型, **When** 提交自然语言查询, **Then** 系统使用选定的模型生成 SQL

---

### User Story 4 - 数据库元数据管理 (Priority: P2)

用户可以查看数据库的详细元数据信息，包括表结构、字段类型等。用户还可以为字段添加中文备注，便于自然语言查询时的理解。

**Why this priority**: 元数据备注功能增强了自然语言生成 SQL 的准确性，但不是核心功能。

**Independent Test**: 可以通过选择一个表，查看其字段列表，并为字段添加中文备注。

**Acceptance Scenarios**:

1. **Given** 用户已连接到数据库, **When** 选择查看某个表的详情, **Then** 系统显示该表的所有字段、类型和约束信息
2. **Given** 用户查看表的字段列表, **When** 为某个字段添加中文备注, **Then** 备注被保存并在后续显示
3. **Given** 用户已为字段添加中文备注, **When** 使用自然语言查询, **Then** LLM 能够利用这些备注生成更准确的 SQL
4. **Given** 用户修改字段的中文备注, **When** 保存修改, **Then** 新的备注覆盖旧的备注

---

### Edge Cases

- 当数据库连接超时或断开时，系统应提示用户重新连接
- 当查询结果为空时，系统应显示"无数据"而非错误
- 当查询结果数据量过大时，系统应分页显示或提示用户添加筛选条件
- 当 LLM 服务不可用时，系统应提示用户使用直接 SQL 查询
- 当数据库元数据发生变化时，用户应能手动刷新元数据

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统必须支持 MySQL 和 PostgreSQL 数据库的连接
- **FR-002**: 系统必须能够获取并存储数据库的元数据（表、视图、字段、类型、约束）
- **FR-003**: 系统必须使用 SQL 解析器验证所有输入的 SQL 语句语法
- **FR-004**: 系统必须仅允许执行 SELECT 语句，拒绝其他类型的 SQL 操作
- **FR-005**: 系统必须为不包含 LIMIT 子句的查询自动添加 LIMIT 1000
- **FR-006**: 系统必须将查询结果以 JSON 格式返回，前端以表格形式展示
- **FR-007**: 系统必须支持将查询结果导出为 CSV 和 JSON 格式
- **FR-008**: 系统必须支持通过自然语言生成 SQL 查询
- **FR-009**: 系统必须支持多种 LLM 模型切换（通义千问、Kimi）
- **FR-010**: 系统必须支持用户为数据库字段添加中文备注
- **FR-011**: 系统必须将数据库连接信息和元数据持久化存储
- **FR-012**: 系统必须提供语法高亮的 SQL 编辑器

### Key Entities

- **DatabaseConnection**: 数据库连接信息，包括名称、连接字符串、数据库类型（MySQL/PostgreSQL）
- **DatabaseMetadata**: 数据库元数据，包括表列表、视图列表、每个表/视图的字段信息
- **TableField**: 字段信息，包括字段名、数据类型、约束、中文备注
- **QueryResult**: 查询结果，包括列定义和数据行
- **LLMConfig**: LLM 配置，包括模型选择和相关参数

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 用户能够在 30 秒内完成数据库连接的添加
- **SC-002**: SQL 查询从提交到显示结果的时间不超过 5 秒（在正常数据量下）
- **SC-003**: 自然语言生成的 SQL 对于简单查询（单表、基本条件）的准确率达到 80% 以上
- **SC-004**: 系统能够处理返回最多 10000 行数据的查询结果
- **SC-005**: 用户能够成功导出查询结果到 CSV 或 JSON 文件
- **SC-006**: 数据库元数据（包括字段中文备注）在系统重启后保持不变

## Assumptions

- 用户具备基本的 SQL 知识或能够用自然语言描述查询需求
- 目标数据库允许来自本应用的连接
- LLM API 服务可用且响应时间合理
- 单次查询的数据量在合理范围内（通过 LIMIT 1000 默认限制）
- 用户的数据库连接字符串包含所有必要的认证信息
