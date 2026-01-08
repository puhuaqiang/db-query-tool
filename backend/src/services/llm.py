"""LLM service for natural language to SQL generation."""

import re
import json
from typing import Any
import httpx
from openai import AsyncOpenAI

from src.config import get_settings
from src.models.llm import LlmModel, NaturalQueryRequest, NaturalQueryResult
from src.models.database import DatabaseConnectionDetail, TableMetadata


# Available LLM models
AVAILABLE_MODELS: list[LlmModel] = [
    LlmModel(
        id="qwen-coder-plus",
        name="通义千问-Coder-Plus",
        provider="dashscope",
    ),
    LlmModel(
        id="kimi-k2-0711-preview",
        name="Kimi K2 Preview",
        provider="moonshot",
    ),
]


def _build_metadata_context(database: DatabaseConnectionDetail) -> str:
    """Build metadata context string for LLM prompt."""
    lines = [f"数据库类型: {database.db_type}"]
    lines.append(f"数据库名: {database.name}")
    lines.append("")
    lines.append("表结构:")

    for table in database.tables:
        table_type = "视图" if table.table_type == "view" else "表"
        lines.append(f"\n{table_type}: {table.table_name}")
        lines.append("字段:")
        for field in table.fields:
            nullable = "可空" if field.is_nullable else "非空"
            chinese = f" ({field.chinese_name})" if field.chinese_name else ""
            lines.append(f"  - {field.field_name}: {field.data_type} [{nullable}]{chinese}")

    return "\n".join(lines)


def _build_prompt(user_query: str, metadata_context: str) -> str:
    """Build the full prompt for SQL generation."""
    return f"""你是一个专业的数据库查询助手。根据用户的自然语言描述，生成对应的 SQL 查询语句。

数据库元数据信息:
{metadata_context}

用户需求: {user_query}

请生成一个有效的 SELECT 查询语句来满足用户需求。

要求:
1. 只生成 SELECT 查询，不要生成任何修改数据的语句
2. 确保查询语法正确且高效
3. 如有需要，使用 JOIN 连接相关表
4. 只返回用户需要的字段

请按以下格式返回:
```sql
你的SQL查询语句
```

解释: 简短说明这个查询的作用"""


def _extract_sql_from_response(response: str) -> tuple[str, str | None]:
    """Extract SQL and explanation from LLM response."""
    # Try to extract SQL from code block
    sql_match = re.search(r"```sql\s*([\s\S]*?)\s*```", response, re.IGNORECASE)
    if sql_match:
        sql = sql_match.group(1).strip()
    else:
        # Try to find raw SQL
        sql_match = re.search(r"(SELECT\s+[\s\S]+?)(?:;|\n\n|$)", response, re.IGNORECASE)
        if sql_match:
            sql = sql_match.group(1).strip()
        else:
            sql = response.strip()

    # Remove trailing semicolon
    sql = sql.rstrip(";").strip()

    # Extract explanation
    explanation = None
    explanation_match = re.search(r"解释[：:]\s*(.+?)(?:\n|$)", response)
    if explanation_match:
        explanation = explanation_match.group(1).strip()

    return sql, explanation


class LlmService:
    """Service for LLM-based SQL generation."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def get_available_models(self) -> list[LlmModel]:
        """Get list of available LLM models."""
        models = []
        # Only include models with configured API keys
        if self.settings.dashscope_api_key:
            models.extend([m for m in AVAILABLE_MODELS if m.provider == "dashscope"])
        if self.settings.moonshot_api_key:
            models.extend([m for m in AVAILABLE_MODELS if m.provider == "moonshot"])
        return models

    async def generate_sql(
        self,
        request: NaturalQueryRequest,
        database: DatabaseConnectionDetail,
    ) -> NaturalQueryResult:
        """Generate SQL from natural language query."""
        # Find the model
        model = next((m for m in AVAILABLE_MODELS if m.id == request.model_id), None)
        if model is None:
            raise ValueError(f"未知的模型: {request.model_id}")

        # Build prompt
        metadata_context = _build_metadata_context(database)
        prompt = _build_prompt(request.prompt, metadata_context)

        # Call LLM
        if model.provider == "dashscope":
            response = await self._call_dashscope(model.id, prompt)
        elif model.provider == "moonshot":
            response = await self._call_moonshot(model.id, prompt)
        else:
            raise ValueError(f"未支持的 LLM 提供商: {model.provider}")

        # Extract SQL
        sql, explanation = _extract_sql_from_response(response)

        return NaturalQueryResult(
            sql=sql,
            explanation=explanation,
            model_id=request.model_id,
        )

    async def _call_dashscope(self, model_id: str, prompt: str) -> str:
        """Call Dashscope (通义千问) API."""
        if not self.settings.dashscope_api_key:
            raise ValueError("未配置 DASHSCOPE_API_KEY")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.settings.dashscope_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_moonshot(self, model_id: str, prompt: str) -> str:
        """Call Moonshot (Kimi) API using OpenAI SDK."""
        if not self.settings.moonshot_api_key:
            raise ValueError("未配置 MOONSHOT_API_KEY")

        client = AsyncOpenAI(
            api_key=self.settings.moonshot_api_key,
            base_url="https://api.moonshot.cn/v1",
        )

        response = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        return response.choices[0].message.content or ""


# Global service instance
_llm_service: LlmService | None = None


def get_llm_service() -> LlmService:
    """Get LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LlmService()
    return _llm_service
