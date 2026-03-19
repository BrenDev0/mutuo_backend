import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from contextlib import asynccontextmanager
from mutuo.persistence.redis import RedisCacheStore

from .rate_limiter import RateLimiter
from .exception_handler import ExceptionHandler
from .api import router as api_router
from .logging import configure_logger

configure_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection_url = os.getenv("REDIS_URL")
    cache_store = RedisCacheStore(connection_url)
    app.state.cache_store = cache_store
    
    try:
        yield
    finally:
        await cache_store.close_connection()

app = FastAPI(lifespan=lifespan)

ALLOWED_ORIGINS = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_methods="*",
    allow_origins=ALLOWED_ORIGINS,
    allow_headers=["*"]
)

app.add_middleware(ExceptionHandler)

app.add_middleware(
    RateLimiter,
    limit=50,
    window_seconds=60
)


app.include_router(api_router, prefix="/api/v1")


@app.get("/health", status_code=200)
def health_check():
    return {
        "status": "Mutuo ok"
    }




if __name__ == "__main__":
    ### Dev entry ###
    from dotenv import load_dotenv
    load_dotenv()
    import uvicorn

    uvicorn.run(
        app="mutuo.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


