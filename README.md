# 数据库查询工具

一个现代化的数据库查询工具，支持 SQL 查询和基于 LLM 的自然语言生成 SQL 功能。

## 功能特性

- **多数据库支持**: 支持 PostgreSQL 和 MySQL 数据库连接
- **自然语言查询**: 使用 LLM（通义千问、Kimi）将自然语言转换为 SQL 查询
- **SQL 编辑器**: 基于 Monaco Editor 的智能 SQL 编辑器，支持语法高亮
- **表结构浏览**: 可视化展示数据库表结构，支持中文字段备注
- **查询结果导出**: 支持导出查询结果为 CSV、JSON、Excel 格式
- **响应式界面**: 基于 Vue 3 + Element Plus 的现代化 UI

## 界面预览

### 主界面
![主界面](docs/images/main-interface.png)

### 自然语言查询
通过自然语言描述查询需求，LLM 自动生成对应的 SQL 语句：

![自然语言输入](docs/images/natural-query-input.png)

### SQL 生成与执行
LLM 生成 SQL 后，可以查看解释说明，然后一键应用到编辑器执行：

![生成的SQL](docs/images/generated-sql.png)

### 查询结果展示
查询结果以表格形式展示，支持分页和导出：

![查询结果](docs/images/query-results.png)

### 更多查询示例
![查询示例2](docs/images/query-example-2.png)

## 技术栈

### 后端
- **Python 3.11+**
- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy** - 数据库 ORM
- **asyncpg / aiomysql** - 异步数据库驱动
- **httpx / openai** - LLM API 调用

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 下一代前端构建工具
- **Element Plus** - Vue 3 组件库
- **Monaco Editor** - VS Code 同款编辑器
- **Pinia** - Vue 状态管理
- **TailwindCSS** - 原子化 CSS 框架

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 或 MySQL 数据库

### 后端安装

```bash
cd backend

# 使用 uv 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库和 LLM API 密钥

# 启动后端服务
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 环境变量配置

在 `backend/.env` 文件中配置：

```env
# LLM API 密钥
DASHSCOPE_API_KEY=your_dashscope_api_key
MOONSHOT_API_KEY=your_moonshot_api_key

# 数据目录（可选）
DATA_DIR=~/.db_query
```

## 使用说明

1. **添加数据库连接**: 点击左侧「添加」按钮，输入数据库连接 URL
   - PostgreSQL: `postgresql://user:password@host:port/database`
   - MySQL: `mysql://user:password@host:port/database`

2. **浏览表结构**: 选择数据库后，左侧会显示所有表和字段信息

3. **自然语言查询**:
   - 选择 LLM 模型
   - 输入自然语言描述（如"查询所有用户"）
   - 点击「生成 SQL」
   - 查看生成的 SQL 和解释
   - 点击「应用到编辑器」

4. **执行查询**: 在 SQL 编辑器中编辑或直接执行查询

5. **导出结果**: 点击「导出」按钮，选择导出格式

## 项目结构

```
db-query-tool/
├── backend/                 # 后端代码
│   ├── src/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 入口文件
│   └── pyproject.toml
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API 服务
│   │   └── stores/         # Pinia 状态
│   └── package.json
└── docs/                    # 文档
    └── images/             # 截图
```

## 开发

### 运行测试

```bash
# 后端测试
cd backend
uv run pytest

# 前端 E2E 测试
cd frontend
npx playwright test
```

### 代码风格

- 后端: 使用 ruff 进行代码检查和格式化
- 前端: 使用 ESLint + Prettier

## License

MIT License
