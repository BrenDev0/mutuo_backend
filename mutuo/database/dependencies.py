from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

def get_db_session(request: Request) -> AsyncSession:
    db = request.state.get("db")
    if not db:
        raise ValueError("Error getting db session")
    
    return db