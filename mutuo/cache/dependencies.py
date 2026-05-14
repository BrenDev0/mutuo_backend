from fastapi import Request
from .protocols import CacheStore

def get_cache_store(request: Request) -> CacheStore:
    cache_store = getattr(request.app.state, "cache_store", None)
    if not cache_store:
        raise ValueError("Cache store not initialized in app")
    
    return cache_store