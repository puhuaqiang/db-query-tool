# 数据库查询工具 - 后端

Python FastAPI 后端服务，支持数据库连接管理、SQL 查询执行和自然语言生成 SQL。

## 功能

- 数据库连接管理 (PostgreSQL / MySQL)
- SQL 查询执行（仅限 SELECT，自动添加 LIMIT）
- 自然语言转 SQL（通义千问、Kimi）
- 查询结果导出（CSV / JSON）
- 元数据管理和中文字段备注

## 快速开始

```bash
# 安装依赖
uv sync

# 启动服务
uv run python -m src.main
```

## 环境变量

- `DASHSCOPE_API_KEY` - 通义千问 API Key
- `MOONSHOT_API_KEY` - Kimi API Key

## API 文档

启动服务后访问 http://localhost:8000/docs
