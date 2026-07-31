from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from agents.graph import run_agent
from memory.cosmos import ConversationMemory
from backend.api.deps import get_current_user
from backend.config.rate_limiter import limiter
import uuid

router = APIRouter()
memory = ConversationMemory()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    sources: list[str] = []


@router.post("", response_model=ChatResponse)
@limiter.limit("20/minute")
def chat(request: Request, chat_request: ChatRequest, user_id: str = Depends(get_current_user)):
    session_id = chat_request.session_id or str(uuid.uuid4())

    memory.add_message(session_id, "user", chat_request.message, user_id=user_id)

    result = run_agent(chat_request.message)

    memory.add_message(session_id, "assistant", result["answer"], result.get("sources", []), user_id=user_id)

    return ChatResponse(
        reply=result["answer"],
        session_id=session_id,
        sources=result.get("sources", [])
    )