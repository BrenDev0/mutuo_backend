import logging
from typing import Dict
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from mutuo.exceptions import ErrorSlug, MutuoException
logger = logging.getLogger(__name__)

ERROR_STATUS_MAP: Dict[ErrorSlug, int] = {
    ErrorSlug.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorSlug.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    ErrorSlug.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED
}

class ExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)

        except MutuoException as e:
            response = JSONResponse(
                status_code=ERROR_STATUS_MAP[e.slug],
                content={"detail": [{"msg": e.detail}]}
            )
        
        except Exception:
            error =  {
                "endpoint": request.url,
                "method": request.method
            }
            
            logger.error(str(error))
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                content={"detail": [{"msg": "Unable to process request at this time"}]}
            )
        

        return response

