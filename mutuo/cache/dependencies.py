from fastapi import Request
from .protocols import CacheStore

def get_cache_store(request: Request) -> CacheStore:
    cache_store = request.app.state.get("cache_store")
    if not cache_store:
        raise ValueError("Cache store not initialized in app")
    
    return cache_store