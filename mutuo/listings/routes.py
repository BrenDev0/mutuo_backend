from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.dependencies import get_db_session
from mutuo.auth.dependencies import user_is_owner

from mutuo.users.schemas import UserPublic

from .schemas import CreateListingRequest, ListingPublic
from .usecases import handle_create_listing
from .repository import create

router = APIRouter(
    tags=["Listings"]
)

@router.post("", status_code=201, response_model=ListingPublic)
async def listings_create(
    data: CreateListingRequest,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(user_is_owner)
):
    return await handle_create_listing(
        db=db,
        user_id=user.user_id,
        listing_in=data,
        create_listing=create
    )

