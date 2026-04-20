from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.dependencies import get_db_session
from mutuo.auth.dependencies import user_is_owner

from mutuo.users.schemas import UserPublic

from .schemas import CreateListingRequest
from .usecases import create_listing

router = APIRouter(
    tags=["Listings"]
)

@router.post("", status_code=201)
async def listings_create(
    listing: CreateListingRequest,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(user_is_owner)
):
    return create_listing()

