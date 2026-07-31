import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from functools import lru_cache
import hashlib

_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutes

def _cache_key(query: str, top: int) -> str:
    return hashlib.sha256(f"{query}:{top}".encode()).hexdigest()

def search_documents(query: str, top: int = 5) -> dict:
    import time
    key = _cache_key(query, top)
    now = time.time()

    if key in _cache:
        cached_result, cached_time = _cache[key]
        if now - cached_time < CACHE_TTL_SECONDS:
            return cached_result

    results = _search_with_retry(query, top)  # your existing retry-wrapped search call

    context_chunks = []
    sources = []
    for r in results:
        content = r.get("content", "")
        if content:
            context_chunks.append(content)
        source = r.get("filename") or r.get("source")
        if source and source not in sources:
            sources.append(source)

    result = {"context": "\n\n".join(context_chunks), "sources": sources}
    _cache[key] = (result, now)
    return result