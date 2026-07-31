# backend/config/test_sql_agent.py
from agents.graph import run_agent

tests = [
    "Show me total sales for Q1",
    "What was the revenue for Widget A in Europe?",
    "Compare Q1 and Q2 revenue by region",
]

for t in tests:
    result = run_agent(t)
    print(f"Q: {t}\nA: {result['answer']}\nSources: {result['sources']}\n")