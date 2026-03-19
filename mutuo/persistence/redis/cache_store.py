from redis import asyncio as aioredis
import json
from typing import Any, Dict
from ..protocols import CacheStore


class RedisCacheStore(CacheStore):
    def __init__(self, connection_url: str):
        self._redis = aioredis.from_url(connection_url)


    async def set(self, key: str, value: Dict[str,Any], expire_seconds: int) -> None:
        await self._redis.set(key, json.dumps(value), ex=expire_seconds)


    async def get(self, key: str) -> Dict[str, Any] | None:
        data = await self._redis.get(key)
        if data is None:
            return None
        return json.loads(data)


    async def delete(self, key: str) -> bool:
        return await self._redis.delete(key) > 0
    

    async def increment(self, key: str) -> int:
        return await self._redis.incr(key)

    async def expire(self, key: str, seconds: int) -> None:
        await self._redis.expire(key, seconds)


