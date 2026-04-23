from uuid import UUID

from mutuo.schemas import Pagination

from .types import CreateListingFn, GetByUserIdFn, UserListingQuery
from .schemas import CreateListingRequest, ListingPublic, ListingFilters, ListingPage
from .mappers import listing_to_public, create_request_to_partial


async def handle_create_listing(
    user_id: UUID,
    listing_in: CreateListingRequest, 
    create_listing: CreateListingFn
) -> ListingPublic:
    listing_data = create_request_to_partial(schema=listing_in, user_id=user_id)
   
    new_listing = await create_listing(listing_data)

    return listing_to_public(model=new_listing)


async def get_user_owned_listings(
    user_id: UUID,
    pagination: Pagination,
    get_by_user_id: GetByUserIdFn,
    filters: ListingFilters | None = None,
    
) -> ListingPage:
    offset = (pagination.page_number - 1) * pagination.items_per_page
    limit = pagination.items_per_page

    cleaned_filters = filters.model_dump(exclude_none=True) if filters else None

    query = UserListingQuery(
        user_id=user_id,
        offset=offset,
        limit=limit,
        filters=cleaned_filters
    )
    
    listings = await get_by_user_id(query)


    return ListingPage(
        **pagination.model_dump(),
        items=[
            listing_to_public(listing)
            for listing in listings
        ]
    )


