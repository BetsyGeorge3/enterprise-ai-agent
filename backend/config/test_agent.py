from agents.graph import run_agent

result = run_agent("what is the purpose of legal document")

print("ANSWER:", result["answer"])
print("SOURCES:", result["sources"])