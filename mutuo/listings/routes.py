from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.dependencies import get_db_session
from mutuo.auth.dependencies import user_is_owner
from mutuo.schemas import Pagination
from mutuo.users.schemas import UserPublic

from .schemas import CreateListingRequest, ListingPublic, ListingPage, ListingFilters
from .usecases import handle_create_listing
from .repository import create, get_by_user_id

router = APIRouter(
    tags=["Listings"]
)

@router.post("", status_code=201, response_model=ListingPublic)
async def listings_create(
    data: CreateListingRequest,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(user_is_owner)
):
    """
    Create new listing

    ### Args:
    - **propertyType**: (CASA, LOCAL, TERRENO, ...ect)
    - **name**: name of listing
    - **description**: short description of listing
    - **address**: listing address
    - **beds**: (int) number of bedrooms in listing
    - **baths**: (float 0.0) number of baths in listing
    - **price**: (int) rent or price
    - **status**: (DISPONIBLE, OCCUPADO, ...ect)

    ### Returns:
    - **201**: public schema 
    """
    return await handle_create_listing(
        db=db,
        user_id=user.user_id,
        listing_in=data,
        create_listing=create
    )


# @router.get("", status_code=200, response_model=ListingPage)
# async def Listings_collection(
#     pagination: Pagination,
#     filters: ListingFilters | None = None,
#     db: AsyncSession = Depends(get_db_session),
#     user: UserPublic = Depends(user_is_owner)
# ):
#     pass

