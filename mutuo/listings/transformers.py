from uuid import UUID

from .models import Listing
from .schemas import ListingPublic, CreateListingRequest

def to_listing_public(model: Listing) -> ListingPublic:
    return ListingPublic.model_validate(model)


def lising_in_to_model(schema: CreateListingRequest, user_id: UUID) -> Listing:
    return Listing(
        user_id=user_id,
        **schema.model_dump()
    )

