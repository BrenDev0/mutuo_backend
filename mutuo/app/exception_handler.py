import logging
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
logger = logging.getLogger(__name__)

class ExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
        
        except Exception:
            error =  {
                "endpoint": request.url,
                "method": request.method
            }
            
            logger.error(str(error))
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                content={
                    "detail": [
                        {
                            "msg": "Unable to process request at this time"
                        }   
                    ] 
                }
            )
        

        return response

