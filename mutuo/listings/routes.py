from uuid import UUID

from fastapi import APIRouter, Depends
from mutuo.auth.dependencies import user_is_owner
from mutuo.users.schemas import UserPublic
from mutuo.schemas import Pagination

from .schemas import CreateListingRequest, ListingPublic, ListingPage, ListingFilters
from .usecases import handle_create_listing, get_user_owned_listings, handle_delete_listing
from .sqlalchemy.dependencies import provide_create_listing, provide_get_listings_by_user_id, provide_delete_listing_by_id
from .types import CreateListingFn, GetListingsByUserIdFn, DeleteListingById

router = APIRouter(
    tags=["Listings"]
)

@router.post("", status_code=201, response_model=ListingPublic)
async def listings_create(
    data: CreateListingRequest,
    create_listing: CreateListingFn = Depends(provide_create_listing),
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
        user_id=user.user_id,
        listing_in=data,
        create_listing=create_listing
    )


@router.get("", status_code=200, response_model=ListingPage)
async def listings_owners_collection(
    pagination: Pagination,
    filters: ListingFilters | None = None,
    user: UserPublic = Depends(user_is_owner),
    get_by_user_id: GetListingsByUserIdFn = Depends(provide_get_listings_by_user_id)
):
    """
    Get Listings uploaded by user

    ### Args: 
    - **pagination**: dictionary representing a page of listings
    - **filters**: Optional filter values(can include more than one)
    
    ### Returns:
    - **200**: Listings pagination schema ('items' in pagination schema)
    """
    return await get_user_owned_listings(
        user_id=user.user_id,
        pagination=pagination,
        get_by_user_id=get_by_user_id,
        filters=filters
    )


@router.delete("/{listing_id}", status_code=200, response_model=ListingPublic)
async def listings_delete_by_id(
    listing_id: UUID,
    user: UserPublic = Depends(user_is_owner),
    delete_listing_by_id: DeleteListingById = Depends(provide_delete_listing_by_id)
):
    """
    Delete litsing by id

    ### Params:
    - **listingId**: id of listing to be deleted

    ### Returns:
    - **200"": public schema of deleted listing

    ### Raises: 
    -**404 NOT FOUND**: if listing matching id is not found in database
    """
    return await handle_delete_listing(
        user_id=user.user_id,
        listing_id=listing_id,
        delete_listing_by_id=delete_listing_by_id
    )

