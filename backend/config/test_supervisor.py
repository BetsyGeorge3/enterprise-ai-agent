# backend/config/test_supervisor.py
from agents.graph import run_agent


tests = [
    "What does the leave policy say about public holidays?",
    "Show me total sales for Q1",
    "Generate a report on segment performance",
    "Email the summary to the team",
]

for t in tests:
    result = run_agent(t)
    print(f"Q: {t}\nA: {result['answer']}\n")