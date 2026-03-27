from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker

from mutuo.cache.redis import RedisCacheStore
from mutuo.settings import settings
from mutuo.database.core import engine

from .rate_limiter import RateLimiter
from .exception_handler import ExceptionHandler
from .api import router as api_router
from .logging import configure_logger


configure_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache_store = RedisCacheStore(settings.REDIS_URL)
    db_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    app.state.cache_store = cache_store
    app.state.db_session_maker = db_session_maker
    
    try:
        yield
    finally:
        await cache_store.close_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_methods="*",
    allow_origins=settings.ALLOW_ORIGINS,
    allow_headers=["*"]
)

app.add_middleware(ExceptionHandler)

app.add_middleware(
    RateLimiter,
    limit=settings.RATELIMIT,
    window_seconds=settings.RATE_LIMIT_WINDOW
)

@app.middleware("http")
async def db_session_middleware(
    request: Request,
    call_next
):
    if "/api/v1" not in str(request.url):
            return await call_next(request)
    
    try:
        session = request.app.state.db_session_maker()
        request.state.db = session

        response = await call_next(request)

        if hasattr(request.state, "db") and request.state.db.is_active:
            await request.state.db.commit()

        return response

    except Exception:
        await request.state.db.close()
        raise
    
    finally:
        await request.state.db.close()


    


app.include_router(api_router, prefix="/api/v1")


@app.get("/health", status_code=200)
def health_check():
    return {
        "status": "Mutuo ok"
    }




if __name__ == "__main__":
    ### Dev entry ###
    import uvicorn

    uvicorn.run(
        app="mutuo.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


