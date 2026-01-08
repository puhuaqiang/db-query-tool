# Research: 数据库查询工具

**Branch**: `001-db-query-tool` | **Date**: 2026-01-08

## 技术决策摘要

| 领域 | 决策 | 理由 |
|------|------|------|
| SQL 解析 | sqlglot | 支持 MySQL/PostgreSQL 方言，纯 Python 实现，无外部依赖 |
| 数据库驱动 | asyncpg + aiomysql | 异步驱动，与 FastAPI 异步架构匹配 |
| LLM 集成 | dashscope SDK + OpenAI SDK | 官方 SDK，支持流式响应 |
| 前端 SQL 编辑器 | Monaco Editor | 语法高亮，自动补全，VSCode 同款 |
| 状态管理 | Pinia | Vue 3 官方推荐，TypeScript 支持良好 |

---

## 1. SQL 解析与验证 (sqlglot)

### 决策
使用 sqlglot 进行 SQL 解析、验证和转换。

### 理由
- **多方言支持**: 原生支持 MySQL 和 PostgreSQL 方言
- **纯 Python**: 无需编译，易于部署
- **AST 操作**: 可以精确检测语句类型（SELECT/INSERT/UPDATE/DELETE）
- **LIMIT 注入**: 可以在 AST 层面添加 LIMIT 子句

### 替代方案评估
| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| sqlparse | 简单，流行 | 不支持方言差异，无法修改 AST | ❌ 不选择 |
| pyparsing | 灵活 | 需要自己定义 SQL 语法 | ❌ 不选择 |
| sqlglot | 功能全面，方言支持 | 学习曲线稍高 | ✅ 选择 |

### 关键用法

```python
import sqlglot
from sqlglot import exp

# 解析 SQL
ast = sqlglot.parse_one("SELECT * FROM users", dialect="postgres")

# 检查是否为 SELECT 语句
is_select = isinstance(ast, exp.Select)

# 检查是否有 LIMIT
has_limit = ast.find(exp.Limit) is not None

# 添加 LIMIT
if not has_limit:
    ast = ast.limit(1000)

# 转回 SQL 字符串
sql = ast.sql(dialect="postgres")
```

---

## 2. 数据库连接管理

### 决策
使用 asyncpg (PostgreSQL) 和 aiomysql (MySQL) 异步驱动。

### 理由
- **异步支持**: 与 FastAPI 的异步架构完美匹配
- **连接池**: 内置连接池管理
- **性能**: 异步 I/O 提高并发处理能力

### 替代方案评估
| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| psycopg2 + pymysql | 成熟稳定 | 同步阻塞 | ❌ 不选择 |
| SQLAlchemy async | ORM 功能 | 本项目不需要 ORM | ❌ 不选择 |
| asyncpg + aiomysql | 轻量，异步原生 | 需要分别处理两种数据库 | ✅ 选择 |

### 连接字符串解析

```python
from urllib.parse import urlparse

def parse_db_url(url: str) -> dict:
    parsed = urlparse(url)
    return {
        "type": parsed.scheme,  # postgres or mysql
        "host": parsed.hostname,
        "port": parsed.port,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip("/")
    }
```

---

## 3. 元数据提取

### 决策
使用数据库系统表查询元数据，通过 LLM 辅助生成结构化 JSON。

### PostgreSQL 元数据查询

```sql
-- 获取所有表和视图
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public';

-- 获取表的字段信息
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'table_name' AND table_schema = 'public';
```

### MySQL 元数据查询

```sql
-- 获取所有表和视图
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = DATABASE();

-- 获取表的字段信息
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'table_name' AND table_schema = DATABASE();
```

---

## 4. LLM 集成

### 决策
支持两种 LLM：dashscope (通义千问) 和 Kimi (kimi-k2-thinking-turbo)。

### dashscope SDK 用法

```python
import dashscope
from dashscope import Generation

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

response = Generation.call(
    model="qwen-coder-plus",
    messages=[
        {"role": "system", "content": "你是一个 SQL 专家..."},
        {"role": "user", "content": prompt}
    ]
)
```

### Kimi API 用法 (OpenAI 兼容)

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="kimi-k2-thinking-turbo",
    messages=[
        {"role": "system", "content": "你是一个 SQL 专家..."},
        {"role": "user", "content": prompt}
    ]
)
```

### LLM Prompt 设计

```text
你是一个数据库 SQL 专家。根据以下数据库结构和用户的自然语言描述，生成对应的 SELECT SQL 语句。

数据库类型: {db_type}
数据库结构:
{metadata_json}

用户请求: {user_prompt}

要求:
1. 只生成 SELECT 语句
2. 使用正确的表名和字段名
3. 如果用户提到中文字段备注，对应到实际字段名
4. 只返回 SQL 语句，不要解释

SQL:
```

---

## 5. 前端技术栈

### Monaco Editor 集成

```typescript
// 安装: npm install monaco-editor @monaco-editor/react
// Vue 3 使用: npm install monaco-editor-vue3

import { MonacoEditor } from 'monaco-editor-vue3'

// 配置 SQL 语法高亮
const editorOptions = {
  language: 'sql',
  theme: 'vs-dark',
  minimap: { enabled: false },
  automaticLayout: true
}
```

### Element Plus 组件选择

| 功能 | 组件 |
|------|------|
| 数据库列表 | ElMenu + ElMenuItem |
| 添加数据库对话框 | ElDialog + ElForm |
| 表格列表 | ElTree |
| 字段编辑 | ElTable + ElInput |
| 查询结果 | ElTable + ElPagination |
| 导出 | ElDropdown + ElButton |
| LLM 选择 | ElSelect |

### Pinia Store 设计

```typescript
import { defineStore } from 'pinia'

export const useDatabaseStore = defineStore('database', {
  state: () => ({
    databases: [] as Database[],
    currentDatabase: null as Database | null,
    queryResult: null as QueryResult | null,
    llmModel: 'qwen-coder-plus' as string
  }),
  actions: {
    async fetchDatabases() { /* ... */ },
    async addDatabase(name: string, url: string) { /* ... */ },
    async executeQuery(sql: string) { /* ... */ },
    async executeNaturalQuery(prompt: string) { /* ... */ }
  }
})
```

---

## 6. SQLite 本地存储

### 决策
使用 aiosqlite 进行异步 SQLite 操作。

### 数据库 Schema

```sql
-- 数据库连接
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    db_type TEXT NOT NULL,  -- 'postgres' or 'mysql'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据库元数据
CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    connection_id INTEGER NOT NULL,
    table_name TEXT NOT NULL,
    table_type TEXT NOT NULL,  -- 'TABLE' or 'VIEW'
    FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE
);

-- 字段信息
CREATE TABLE IF NOT EXISTS fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metadata_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    is_nullable BOOLEAN DEFAULT TRUE,
    column_default TEXT,
    chinese_name TEXT,  -- 用户添加的中文备注
    FOREIGN KEY (metadata_id) REFERENCES metadata(id) ON DELETE CASCADE
);
```

---

## 7. API 设计最佳实践

### CORS 配置

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Pydantic camelCase 配置

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
```

---

## 8. 未解决问题

无。所有技术决策已确定。
