# 快速开始: 数据库查询工具

**Branch**: `001-db-query-tool` | **Date**: 2026-01-08

## 环境要求

### 后端
- Python 3.11+
- uv (Python 包管理器)

### 前端
- Node.js 18+
- npm 或 pnpm

### 数据库
- MySQL 8.0+ 或 PostgreSQL 14+ (用于连接)
- SQLite (自动创建，用于本地存储)

### LLM API Keys
- `DASHSCOPE_API_KEY`: 通义千问 API 密钥
- `MOONSHOT_API_KEY`: Kimi API 密钥

---

## 安装步骤

### 1. 克隆仓库

```bash
git clone <repository-url>
cd db-query-tool
```

### 2. 配置环境变量

```bash
# Linux/macOS
export DASHSCOPE_API_KEY="your-dashscope-api-key"
export MOONSHOT_API_KEY="your-moonshot-api-key"

# Windows PowerShell
$env:DASHSCOPE_API_KEY="your-dashscope-api-key"
$env:MOONSHOT_API_KEY="your-moonshot-api-key"
```

### 3. 启动后端

```bash
cd backend

# 使用 uv 安装依赖
uv sync

# 启动开发服务器
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 http://localhost:8000 启动。

### 4. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:5173 启动。

---

## 使用指南

### 1. 添加数据库连接

1. 打开浏览器访问 http://localhost:5173
2. 点击"添加数据库"按钮
3. 输入连接名称（如 `my-postgres`）
4. 输入连接字符串：
   - PostgreSQL: `postgres://user:password@host:5432/database`
   - MySQL: `mysql://user:password@host:3306/database`
5. 点击"连接"

系统将自动获取数据库的表和字段信息。

### 2. 查看数据库结构

1. 在左侧选择已添加的数据库
2. 展开查看所有表和视图
3. 点击表名查看字段详情
4. 可以为字段添加中文备注

### 3. 执行 SQL 查询

1. 在 SQL 编辑器中输入查询语句
2. 点击"执行"按钮
3. 查看结果表格
4. 可选：导出为 CSV 或 JSON

**注意**：
- 仅支持 SELECT 语句
- 如果没有 LIMIT，系统会自动添加 LIMIT 1000

### 4. 自然语言查询

1. 选择 LLM 模型（通义千问或 Kimi）
2. 在输入框中用自然语言描述查询需求
3. 点击"生成 SQL"
4. 查看生成的 SQL，可以编辑
5. 点击"执行"运行查询

**示例**：
- "查询所有用户"
- "查询订单金额大于 100 的记录"
- "统计每个分类的商品数量"

---

## API 示例

### 获取所有数据库

```bash
curl http://localhost:8000/api/v1/dbs
```

### 添加数据库

```bash
curl -X PUT http://localhost:8000/api/v1/dbs/my-postgres \
  -H "Content-Type: application/json" \
  -d '{"url": "postgres://user:pass@localhost:5432/mydb"}'
```

### 执行查询

```bash
curl -X POST http://localhost:8000/api/v1/dbs/my-postgres/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM users LIMIT 10"}'
```

### 自然语言查询

```bash
curl -X POST http://localhost:8000/api/v1/dbs/my-postgres/query/natural \
  -H "Content-Type: application/json" \
  -d '{"prompt": "查询所有用户", "model": "qwen-coder-plus"}'
```

---

## 常见问题

### Q: 连接失败怎么办？

1. 检查连接字符串格式是否正确
2. 确认数据库服务正在运行
3. 检查防火墙设置
4. 验证用户名和密码

### Q: LLM 生成的 SQL 不准确？

1. 为表字段添加中文备注
2. 使用更具体的描述
3. 尝试切换不同的 LLM 模型

### Q: 查询超时？

1. 添加 LIMIT 限制返回行数
2. 添加 WHERE 条件筛选数据
3. 检查数据库连接状态

---

## 验证清单

- [ ] 后端服务启动成功 (http://localhost:8000/docs)
- [ ] 前端服务启动成功 (http://localhost:5173)
- [ ] 可以添加数据库连接
- [ ] 可以查看数据库表结构
- [ ] 可以执行 SQL 查询
- [ ] 可以使用自然语言生成 SQL
- [ ] 可以导出查询结果
