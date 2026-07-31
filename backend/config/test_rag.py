from rag.indexing import index_document
from rag.retrieval import search_documents

sample_text = """
The Enterprise AI Knowledge Assistant is a multi-agent system built on Azure.
It uses retrieval-augmented generation to answer questions from internal documents.
"""

print("Indexing sample document...")
index_document(sample_text, "sample.txt")

print("\nSearching...")
results = search_documents("What does the assistant use for answering questions?")
for r in results:
    print(f"[{r['score']:.3f}] {r['filename']}: {r['content'][:100]}...")