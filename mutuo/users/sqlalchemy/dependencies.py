from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 

from mutuo.database.dependencies import get_db_session

from .repository import create
from ..types import CreateUserFn 
from ..models import User 

def provide_create_user(db: AsyncSession = Depends(get_db_session)) -> CreateUserFn:
    async def create_user(user_in: User) -> User:
        return await create(db=db, user_in=user_in)
    
    return create_user