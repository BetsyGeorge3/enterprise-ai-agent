import json
from backend.services.llm_service import LLMService

llm_service = LLMService()

PLANNER_PROMPT = """...
Each step must specify:
- "agent": one of "rag", "sql", "report", "email", "mcp"
- "instruction": for rag/sql/report/email, a natural language instruction.
  For "mcp", instead provide "tool" (the MCP tool name) and "args" (a JSON object of arguments).
...
"""



def create_plan(request: str) -> list[dict]:
    raw = llm_service.simple_ask(PLANNER_PROMPT.format(request=request))
    raw = raw.strip()
    # strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        raw = raw.replace("json", "", 1).strip()

    try:
        plan = json.loads(raw)
        if not isinstance(plan, list):
            raise ValueError("Plan is not a list")
        return plan
    except (json.JSONDecodeError, ValueError):
        # Fallback: treat the whole request as a single rag step
        return [{"agent": "rag", "instruction": request}]