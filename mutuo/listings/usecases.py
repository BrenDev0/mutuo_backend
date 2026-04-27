from uuid import UUID

from mutuo.schemas import Pagination
from mutuo.exceptions import NotfoundException

from .types import CreateListingFn, GetListingsByUserIdFn, UserListingQuery, DeleteListingById, DeleteListingCommand
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
    get_by_user_id: GetListingsByUserIdFn,
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


async def handle_delete_listing(
    user_id: UUID,
    listing_id: UUID,
    delete_listing_by_id: DeleteListingById
) -> ListingPublic:
    command = DeleteListingCommand(
        user_id=user_id,
        listing_id=listing_id
    )

    deleted_listing = await delete_listing_by_id(command)

    if not deleted_listing:
        raise NotfoundException("Listing not found")
    
    return listing_to_public(deleted_listing)




