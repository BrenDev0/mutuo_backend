from uuid import UUID

from .models import Listing
from .schemas import ListingPublic, CreateListingRequest

def model_to_listing_public(model: Listing) -> ListingPublic:
    return ListingPublic.model_validate(model, from_attributes=True)


def listing_in_to_model(schema: CreateListingRequest, user_id: UUID) -> Listing:
    return Listing(
        user_id=user_id,
        **schema.model_dump(by_alias=False)
    )

