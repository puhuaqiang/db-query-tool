# 设计摘要

## 架构概述

采用前后端分离架构：
- **后端**: Python FastAPI REST API
- **前端**: Vue 3 SPA
- **存储**: SQLite (元数据) + MySQL/PostgreSQL (用户数据库)

## 技术栈

### 后端

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| 框架 | FastAPI | 异步 Python Web 框架 |
| 数据验证 | Pydantic | 类型安全的数据模型 |
| SQL 解析 | sqlglot | 多方言 SQL 解析器 |
| 数据库驱动 | asyncpg + aiomysql | 异步数据库驱动 |
| 本地存储 | aiosqlite | 异步 SQLite |
| LLM | dashscope + openai | LLM API 客户端 |

### 前端

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| 框架 | Vue 3 | 渐进式 JavaScript 框架 |
| 语言 | TypeScript | 类型安全的 JavaScript |
| UI 组件 | Element Plus | Vue 3 UI 组件库 |
| 样式 | Tailwind CSS | 原子化 CSS |
| SQL 编辑器 | Monaco Editor | VSCode 同款编辑器 |
| 状态管理 | Pinia | Vue 3 状态管理 |
| HTTP 客户端 | Axios | HTTP 请求库 |

## 项目结构

```
db-query-tool/
├── backend/
│   ├── src/
│   │   ├── models/      # Pydantic 数据模型
│   │   │   ├── database.py   # 数据库连接和元数据模型
│   │   │   ├── query.py      # 查询请求和结果模型
│   │   │   ├── llm.py        # LLM 相关模型
│   │   │   └── errors.py     # 错误响应模型
│   │   ├── services/    # 业务逻辑
│   │   │   ├── database.py   # 数据库连接管理
│   │   │   ├── metadata.py   # 元数据提取
│   │   │   ├── query.py      # SQL 查询执行和验证
│   │   │   ├── export.py     # CSV/JSON 导出
│   │   │   └── llm.py        # LLM 自然语言转 SQL
│   │   ├── api/         # REST API 端点
│   │   │   └── v1/
│   │   │       ├── dbs.py    # 数据库和查询 API
│   │   │       └── llm.py    # LLM 模型 API
│   │   ├── storage/     # SQLite 存储
│   │   │   └── sqlite.py     # SQLite 操作
│   │   ├── config.py    # 应用配置
│   │   └── main.py      # FastAPI 入口
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/  # Vue 组件
│   │   │   ├── DatabaseList.vue      # 数据库列表
│   │   │   ├── AddDatabaseDialog.vue # 添加数据库对话框
│   │   │   ├── TableList.vue         # 表结构树
│   │   │   ├── FieldEditor.vue       # 字段中文名编辑
│   │   │   ├── SqlEditor.vue         # Monaco SQL 编辑器
│   │   │   ├── QueryResult.vue       # 查询结果表格
│   │   │   ├── ExportDialog.vue      # 导出下拉菜单
│   │   │   ├── NaturalQueryInput.vue # 自然语言输入
│   │   │   └── LlmModelSelector.vue  # LLM 模型选择
│   │   ├── pages/       # 页面组件
│   │   │   └── HomePage.vue
│   │   ├── services/    # API 客户端
│   │   │   ├── api.ts        # Axios API 封装
│   │   │   └── types.ts      # TypeScript 类型定义
│   │   └── stores/      # Pinia 状态
│   │       └── database.ts   # 数据库和查询状态
│   └── tests/
└── docs/
```

## API 设计

### 数据库管理

- `GET /api/v1/dbs` - 获取所有数据库连接
- `PUT /api/v1/dbs/{name}` - 添加数据库连接
- `GET /api/v1/dbs/{name}` - 获取数据库详情
- `DELETE /api/v1/dbs/{name}` - 删除数据库连接

### 查询

- `POST /api/v1/dbs/{name}/query` - 执行 SQL 查询
- `POST /api/v1/dbs/{name}/query/natural` - 自然语言查询
- `POST /api/v1/dbs/{name}/query/export` - 导出查询结果

### 元数据

- `POST /api/v1/dbs/{name}/refresh` - 刷新元数据
- `PATCH /api/v1/dbs/{name}/tables/{table}/fields/{field}` - 更新字段备注

### LLM

- `GET /api/v1/llm/models` - 获取可用 LLM 模型列表

## 设计原则

1. **类型安全**: 后端 Python 类型注解，前端 TypeScript strict 模式
2. **数据格式**: 后端 JSON 使用 camelCase
3. **无认证**: 所有 API 公开访问
4. **安全限制**: 仅允许 SELECT 语句，自动添加 LIMIT

## 实现功能

### 用户故事 1: 数据库连接管理
- 支持 PostgreSQL 和 MySQL 数据库连接
- 自动提取数据库元数据（表、视图、字段）
- 连接信息持久化存储

### 用户故事 2: SQL 查询执行
- Monaco Editor SQL 编辑器（语法高亮、自动完成）
- SQL 语法验证（仅允许 SELECT）
- 自动添加 LIMIT 1000 限制
- 查询结果表格展示
- CSV/JSON 导出

### 用户故事 3: 自然语言生成 SQL
- 支持通义千问-Coder-Plus
- 支持 Kimi K2
- 基于数据库元数据生成 SQL
- 生成结果预览和编辑

### 用户故事 4: 元数据管理
- 表结构树形展示
- 字段中文名称编辑
- 元数据刷新

## 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-01-08 | 1.0.0 | 初始架构设计 | - |
| 2026-01-08 | 1.0.0 | 完成全部用户故事实现 | - |
