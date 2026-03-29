from fastapi import Request
from .protocols import CryptographyService

def get_cryptography_service(request: Request) -> CryptographyService:
    service = request.app.state.get("cryptography")
    if not service:
        raise ValueError("Cryptography service not initialized in app")
    
    return service