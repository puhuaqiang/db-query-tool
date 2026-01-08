# Data Model: 数据库查询工具

**Branch**: `001-db-query-tool` | **Date**: 2026-01-08

## 概述

本文档定义了数据库查询工具的数据模型，包括实体、关系和验证规则。

---

## 实体定义

### 1. DatabaseConnection (数据库连接)

存储用户添加的数据库连接信息。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 主键，自增 |
| name | string | 是 | 连接名称，唯一 |
| url | string | 是 | 数据库连接字符串 |
| dbType | enum | 是 | 数据库类型: `postgres` \| `mysql` |
| createdAt | datetime | 是 | 创建时间 |
| updatedAt | datetime | 是 | 更新时间 |

**验证规则**:
- `name`: 长度 1-100，仅允许字母、数字、下划线、中划线
- `url`: 必须是有效的数据库连接字符串格式
- `dbType`: 必须从连接字符串中解析得到

**关系**:
- 一个 DatabaseConnection 有多个 TableMetadata

---

### 2. TableMetadata (表元数据)

存储数据库中的表和视图信息。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 主键，自增 |
| connectionId | integer | 是 | 外键，关联 DatabaseConnection |
| tableName | string | 是 | 表名 |
| tableType | enum | 是 | 类型: `TABLE` \| `VIEW` |
| chineseName | string | 否 | 表的中文名称 |

**验证规则**:
- `tableName`: 长度 1-255
- 同一 connectionId 下 tableName 唯一

**关系**:
- 属于一个 DatabaseConnection
- 一个 TableMetadata 有多个 FieldMetadata

---

### 3. FieldMetadata (字段元数据)

存储表的字段信息。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 主键，自增 |
| tableId | integer | 是 | 外键，关联 TableMetadata |
| fieldName | string | 是 | 字段名 |
| dataType | string | 是 | 数据类型 |
| isNullable | boolean | 是 | 是否可为空 |
| columnDefault | string | 否 | 默认值 |
| maxLength | integer | 否 | 最大长度 |
| chineseName | string | 否 | 字段的中文备注 |

**验证规则**:
- `fieldName`: 长度 1-255
- `chineseName`: 长度 0-100

**关系**:
- 属于一个 TableMetadata

---

### 4. QueryRequest (查询请求)

表示用户发起的 SQL 查询请求。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sql | string | 是 | SQL 查询语句 |

**验证规则**:
- `sql`: 非空，长度 1-10000
- 解析后必须是 SELECT 语句

---

### 5. NaturalQueryRequest (自然语言查询请求)

表示用户发起的自然语言查询请求。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 自然语言描述 |
| model | string | 否 | LLM 模型，默认 qwen-coder-plus |

**验证规则**:
- `prompt`: 非空，长度 1-2000
- `model`: 可选值 `qwen-coder-plus` \| `kimi-k2-thinking-turbo`

---

### 6. QueryResult (查询结果)

表示 SQL 查询的结果。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| columns | Column[] | 是 | 列定义数组 |
| rows | any[][] | 是 | 数据行数组 |
| rowCount | integer | 是 | 返回行数 |
| executionTime | number | 是 | 执行时间(毫秒) |

---

### 7. Column (列定义)

查询结果的列定义。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 列名 |
| type | string | 是 | 数据类型 |

---

### 8. NaturalQueryResult (自然语言查询结果)

表示自然语言生成 SQL 的结果。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| generatedSql | string | 是 | 生成的 SQL 语句 |
| result | QueryResult | 否 | 如果执行了查询，返回结果 |

---

## 实体关系图

```text
┌─────────────────────┐
│ DatabaseConnection  │
├─────────────────────┤
│ id (PK)             │
│ name (unique)       │
│ url                 │
│ dbType              │
│ createdAt           │
│ updatedAt           │
└─────────┬───────────┘
          │ 1
          │
          │ *
┌─────────▼───────────┐
│ TableMetadata       │
├─────────────────────┤
│ id (PK)             │
│ connectionId (FK)   │
│ tableName           │
│ tableType           │
│ chineseName         │
└─────────┬───────────┘
          │ 1
          │
          │ *
┌─────────▼───────────┐
│ FieldMetadata       │
├─────────────────────┤
│ id (PK)             │
│ tableId (FK)        │
│ fieldName           │
│ dataType            │
│ isNullable          │
│ columnDefault       │
│ maxLength           │
│ chineseName         │
└─────────────────────┘
```

---

## 状态转换

### 数据库连接状态

```text
[初始] --> [连接中] --> [已连接] --> [已断开]
                   \--> [连接失败]
```

| 状态 | 说明 |
|------|------|
| 初始 | 连接信息已保存，未尝试连接 |
| 连接中 | 正在尝试连接数据库 |
| 已连接 | 连接成功，可以执行查询 |
| 已断开 | 连接已关闭 |
| 连接失败 | 连接尝试失败 |

---

## SQLite 存储 Schema

```sql
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
```
