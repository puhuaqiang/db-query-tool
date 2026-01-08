<!--
============================================================================
SYNC IMPACT REPORT
============================================================================
Version change: N/A → 1.0.0 (Initial constitution)
Modified principles: N/A (Initial creation)

Added sections:
- Core Principles (5 principles)
- 技术栈约束 (Technology Stack Constraints)
- 开发工作流 (Development Workflow)
- Governance

Removed sections: N/A

Templates requiring updates:
- .specify/templates/plan-template.md ✅ (No changes needed - generic template)
- .specify/templates/spec-template.md ✅ (No changes needed - generic template)
- .specify/templates/tasks-template.md ✅ (No changes needed - generic template)

Follow-up TODOs: None
============================================================================
-->

# DB-Query-Tool Constitution

## Core Principles

### I. 类型安全 (Type Safety)

所有代码必须具有严格的类型标注。

- 后端 Python 代码必须使用完整的类型注解（type hints）
- 前端 TypeScript 代码必须启用 strict 模式
- 禁止使用 `Any` 类型，除非有明确的技术理由并添加注释说明
- 数据模型必须使用 Pydantic 进行定义和验证

**理由**: 严格的类型系统能在编译/运行时捕获错误，提高代码可维护性和开发效率。

### II. 数据格式一致性 (Data Format Consistency)

后端与前端之间的数据交换必须遵循统一格式。

- 所有后端生成的 JSON 数据必须使用 camelCase 命名格式
- Pydantic 模型必须配置 `alias_generator` 或 `by_alias=True` 以确保 JSON 输出为 camelCase
- API 响应结构必须保持一致性

**理由**: 统一的数据格式减少前后端转换逻辑，降低出错概率。

### III. 代码风格规范 (Code Style Standards)

代码必须遵循特定的语言风格规范。

- 后端：使用 Ergonomic Python 风格（简洁、Pythonic、可读性优先）
- 前端：使用 TypeScript 进行开发
- 遵循各语言社区的最佳实践和代码规范

**理由**: 一致的代码风格提高团队协作效率和代码可读性。

### IV. 开放访问 (Open Access)

系统不实现用户认证机制。

- 不需要用户登录或身份验证
- 所有 API 端点对任何用户开放
- 不存储用户个人身份信息

**理由**: 简化系统架构，专注于核心数据库查询功能。

### V. 文档规范 (Documentation Standards)

项目文档必须遵循统一的标准。

- 文档默认使用中文输出
- 所有文档存放在 `./docs` 目录下
- 需求变更记录在 `./docs/requirements_summary.md`
- 设计变更记录在 `./docs/design_summary.md`
- BUG 修复记录在 `./docs/bugfixes_summary.md`

**理由**: 统一的文档管理便于团队协作和知识传承。

## 技术栈约束

本项目的技术栈选择具有约束力：

**后端**:
- 语言：Python（使用 uv 进行包管理）
- 框架：FastAPI
- SQL 解析：sqlglot
- 数据验证：Pydantic
- LLM 支持：dashscope (通义千问-Coder-Plus)、kimi-k2-thinking-turbo

**前端**:
- 框架：Vue 3
- 语言：TypeScript
- 样式：Tailwind CSS
- UI 组件库：Element Plus
- SQL 编辑器：Monaco Editor

**数据库**:
- 元数据存储：SQLite（位置：`~/.db_query/db_query.db`）
- 支持连接的数据库：MySQL、PostgreSQL

## 开发工作流

### 代码质量要求

- 所有代码提交前必须通过 lint 检查
- 所有代码提交前必须通过测试
- 使用 rebase 而非 merge 进行分支合并

### 提交规范

遵循 Conventional Commits:
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 重构

### API 设计规范

- 后端 API 必须支持 CORS，允许所有 origin
- API 版本前缀：`/api/v1/`
- SQL 查询必须经过 sqlglot 解析验证
- 仅允许 SELECT 语句执行
- 查询如不包含 LIMIT 子句，默认添加 `LIMIT 1000`

## Governance

本 Constitution 是项目开发的最高指导原则，所有开发实践必须遵循本文档规定。

### 修订流程

1. 修订提案必须以文档形式提交
2. 重大变更需要团队评审
3. 所有修订必须更新版本号和修订日期

### 版本管理

- MAJOR：不兼容的治理/原则变更
- MINOR：新增原则或章节
- PATCH：澄清说明、措辞修正

### 合规检查

- 所有 PR 必须验证是否符合本 Constitution
- 代码复杂性必须有正当理由
- 架构决策必须符合技术栈约束

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
