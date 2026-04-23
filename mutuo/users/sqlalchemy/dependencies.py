from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 

from mutuo.database.dependencies import get_db_session

from .repository import create, update_by_id, get_by_id, get_by_email_hash, delete_by_id
from ..types import CreateUserFn, UpdateUserFn, GetByIdFn, GetByEmailHashFn, DeleteByIdFn
from ..models import User, UserPartial

def provide_create_user(db: AsyncSession = Depends(get_db_session)) -> CreateUserFn:
    async def create_user(user_in: UserPartial) -> User:
        return await create(db=db, user_in=user_in)
    
    return create_user


def provide_update_user(db: AsyncSession = Depends(get_db_session)) -> UpdateUserFn:
    async def update_user(user_id: UUID, changes: dict[str, Any]) -> User:
        return await update_by_id(db=db, user_id=user_id, changes=changes)
    
    return update_user


def provide_get_by_id(db: AsyncSession = Depends(get_db_session)) -> GetByIdFn:
    async def get_user_by_id(user_id: UUID) -> User | None:
        return await get_by_id(db=db, user_id=user_id)
    
    return get_user_by_id


def provide_get_by_email_hash(db: AsyncSession = Depends(get_db_session)) -> GetByEmailHashFn:
    async def get_user_by_email_hash(email_hash: str) -> User | None:
        return await get_by_email_hash(db=db, email_hash=email_hash)
    
    return get_user_by_email_hash


def provide_delete_by_id(db: AsyncSession = Depends(get_db_session)) -> DeleteByIdFn:
    async def delete_user_by_id(user_id: UUID) -> User | None:
        return await delete_by_id(db=db, user_id=user_id)
    
    return delete_user_by_id