from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from mutuo.cache.protocols import CacheStore


class RateLimiter(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        limit: int,
        window_seconds: int
    ):
        super().__init__(app)
        
        self._limit = limit
        self._window = window_seconds

    async def dispatch(
        self, 
        request: Request, 
        call_next: RequestResponseEndpoint
    ) -> Response:
        cache_store: CacheStore = request.app.state.cache_store

        ip = self._get_client_ip(request)

        request_count_key = f"ratelimit:count:{ip}"
        blocked_ip_key = f"ratelimit:block:{ip}"
        
        is_blocked = await cache_store.get(
            key=blocked_ip_key
        )

        if is_blocked:
            return JSONResponse(content="Request limit reached", status_code=429) 

        count = await cache_store.increment(key=request_count_key)

        if count == 1:
            await cache_store.expire(key=request_count_key, expire_seconds=self._window)


        if count > self._limit:
            await cache_store.set(
                key=blocked_ip_key,
                value=1,
                expire_seconds=60*10 # 10mins
            )

            return JSONResponse(
                content="Request limit reached",
                status_code=429
            )
        
        return await call_next(request)
    
    
    def _get_client_ip(self, request: Request) -> str:
        ip = "unknown"
        forwarded = request.headers.get("x-forwarded-for")

        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            client = request.client
            ip = client.host if client else "unknown"

        return ip

