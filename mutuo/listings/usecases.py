from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.schemas import Pagination

from .types import CreateListingFn, GetByUserIdFn
from .schemas import CreateListingRequest, ListingPublic, ListingFilters, ListingPage
from .mappers import listing_in_to_model, model_to_listing_public
from .models import Listing

async def handle_create_listing(
    db: AsyncSession,
    user_id: UUID,
    listing_in: CreateListingRequest, 
    create_listing: CreateListingFn
) -> ListingPublic:
    listing_data: Listing = listing_in_to_model(schema=listing_in, user_id=user_id)

    new_listing = await create_listing(db, listing_data)

    return model_to_listing_public(model=new_listing)


async def get_page_of_user_owned_listings(
    db: AsyncSession,
    user_id: UUID,
    pagination: Pagination,
    get_by_user_id: GetByUserIdFn,
    filters: ListingFilters | None = None,
    
) -> ListingPage:
    offset = (pagination.page_number - 1) * pagination.items_per_page
    limit = pagination.items_per_page

    cleaned_filters = filters.model_dump(exclude_none=True) if filters else None

    listings = await get_by_user_id(
        db,
        user_id,
        offset,
        limit,
        cleaned_filters
    )


    return ListingPage(
        **pagination.model_dump(),
        items=[
            model_to_listing_public(listing)
            for listing in listings
        ]
    )


