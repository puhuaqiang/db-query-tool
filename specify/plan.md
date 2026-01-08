后端使用 Python (uv) / FastAPI / sqlglot 来实现。
LLM 支持 2 种：dashscope(通义千问-Coder-Plus) sdk 和 kimi-k2-thinking-turbo
后端要根据连接的数据库不同，支持 MYSQL 和 PostgreSQL 的处理
支持对数据库的 metadata，每个表的字段输入中文名，便于在 LLM 生成 SQL 时，中文名和表的字段进行对应,字段的中文备注可以和 metadata 数据存储在 sqlite 数据库

dashscope(通义千问-Coder) API key 在环境变量 DASHSCOPE_API_KEY 中。
kimi-k2-thinking-turbo API key 在环境变量 MOONSHOT_API_KEY 中。

前端使用 Vue / tailwind / Element Plus(https://element-plus.org/) 来实现。sql editor 使用 monaco editor 来实现。
前端支持对数据库的 metadata，每个表的字段输入中文名进行备注，支持添加和修改.

数据库连接和 metadata 存储在 sqlite 数据库中，放在 ~/.db_query/db_query.db 中。

后端 API 需要支持 cors，允许所有 origin。大致 API 如下：

前端要支持选择不同 LLM 模型，支持导出多种方式。

```bash
# 获取所有已存储的数据库
GET /api/v1/dbs
# 添加一个数据库
PUT /api/v1/dbs/{name}

{
  "url": "postgres://postgres:postgres@localhost:5432/postgres"
}

# 获取一个数据库的 metadata
GET /api/v1/dbs/{name}

# 查询某个数据库的信息
POST /api/v1/dbs/{name}/query

{
  "sql": "SELECT * FROM users"
}

# 根据自然语言生成 sql
POST /api/v1/dbs/{name}/query/natural

{
  "prompt": "查询用户表的所有信息"
}
```
