from backend.services.llm_service import LLMService

llm_service = LLMService()

SUMMARY_PROMPT = """Summarize the following conversation between a user and an AI assistant.
Keep it concise (3-5 sentences), capturing key facts, decisions, and open questions.
Do not include pleasantries.

Conversation:
{conversation}
"""


def summarize_conversation(messages: list[dict]) -> str:
    conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    prompt = SUMMARY_PROMPT.format(conversation=conversation_text)
    return llm_service.simple_ask(prompt)