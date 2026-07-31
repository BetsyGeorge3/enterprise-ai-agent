from memory.cosmos import ConversationMemory

memory = ConversationMemory()
session_id = "test-session-001"

memory.add_message(session_id, "user", "What is the Enterprise AI Assistant?")
memory.add_message(session_id, "assistant", "It's a multi-agent system built on Azure.")

history = memory.get_history(session_id)
print("HISTORY:")
for msg in history:
    print(f"  [{msg['role']}] {msg['content']}")