from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from mutuo.database.dependencies import get_db_session

from .repository import create, get_by_user_id
from ..models import Listing
from ..types import GetByUserIdFn, CreateListingFn, UserListingQuery


def provide_create_listing(db: AsyncSession = Depends(get_db_session)) -> CreateListingFn:
    async def create_listing(listing_in: Listing) -> Listing:
        return  await create(db=db, listing_in=listing_in)
    
    return create_listing


def provide_get_by_user_id(db: AsyncSession = Depends(get_db_session)) -> GetByUserIdFn:
    async def get_listing_by_user_id(query: UserListingQuery) -> list[Listing]:
        return await get_by_user_id(
            db=db,
            user_id=query.user_id,
            offset=query.offset,
            limit=query.limit,
            filters=query.filters
        )
    
    return get_listing_by_user_id
        

