from typing import Protocol, Dict, Any


class CacheStore(Protocol):
    async def set(
        self,
        key: str,
        value: Dict[str, Any],
        expire_seconds: int
    ) -> None:
        ...


    async def delete(
        self,
        key: str
    ) -> bool:
        ...



    async def get(
        self,
        key: str
    ) -> Dict[str, Any] | None:
        ...


    async def increment(
        self,
        key: str 
    ) -> int:
        ...

    async def expire(
        self,
        key: str,
        expire_seconds: int
    ) -> None:
        ...  

