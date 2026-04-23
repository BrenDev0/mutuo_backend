from uuid import UUID

from .models import Listing, ListingPartial
from .schemas import ListingPublic, CreateListingRequest

def listing_to_public(model: Listing) -> ListingPublic:
    return ListingPublic.model_validate(model, from_attributes=True)


def create_request_to_partial(schema: CreateListingRequest, user_id: UUID) -> ListingPartial:
    return ListingPartial(
        user_id=user_id,
        **schema.model_dump(by_alias=False)
    )

