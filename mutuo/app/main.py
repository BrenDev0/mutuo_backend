from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from .api import router as api_router

app = FastAPI()

ALLOWED_ORIGINS = []

app.add_middleware(
    CORSMiddleware,
    allowed_methods="*",
    allowed_origins=ALLOWED_ORIGINS,
    allow_headers=["*"]
)


@app.exception_handler(Exception)
def exception_handler(
    request: Request,
    exc: Union[Exception]
):
    pass

app.include_router(api_router, prefix="/api/v1")







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


