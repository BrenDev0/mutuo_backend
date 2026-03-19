import os 
from .protocols import CacheStore
from .redis import RedisCacheStore

def get_external_cache_store() -> CacheStore:
    redis_url = os.getenv("REDIS_URL")
    return RedisCacheStore(connection_url=redis_url)
    