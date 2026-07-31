from backend.services.llm_service import LLMService

llm = LLMService()

SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer the user's question "
    "using ONLY the provided context below. If the answer isn't in the context, "
    "say you don't have that information. Be concise and clear."
)


def answer_node(state: dict) -> dict:
    """
    Takes the retrieved context from state and generates a grounded answer
    using the LLM. Updates state with the final answer.
    """
    question = state["question"]
    context = state.get("context", "")

    if not context.strip():
        state["answer"] = "I couldn't find any relevant information in the knowledge base for that question."
        return state

    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    llm_result = llm.chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ])

    # LLMService.chat returns both the generated text and usage metadata.
    # Only the text belongs in the user-facing answer; retaining the whole
    # dictionary here causes it to be rendered verbatim in chat responses.
    state["answer"] = llm_result["text"]
    state["tokens_used"] = llm_result["tokens_used"]
    return state
