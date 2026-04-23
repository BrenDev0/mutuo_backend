from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from mutuo.database.dependencies import get_db_session

from .repository import create, get_by_user_id
from ..models import Listing
from ..types import GetByUserIdFn, CreateListingFn


def provide_create_listing(db: AsyncSession = Depends(get_db_session)) -> CreateListingFn:
    async def create_listing(listing_in: Listing) -> Listing:
        return  await create(db=db, listing_in=listing_in)
    
    return create_listing


def provide_get_by_user_id(db: AsyncSession = Depends(get_db_session)) -> GetByUserIdFn:
    async def get_listing_by_user_id(user_id: UUID, offset: int, limit: int, filters: dict[str, Any] | None = None):
        return await get_by_user_id(
            db=db,
            user_id=user_id,
            offset=offset,
            limit=limit,
            filters=filters
        )
    
    return get_listing_by_user_id
        

