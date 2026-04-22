from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .types import CreateListingFn
from .schemas import CreateListingRequest, ListingPublic
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
