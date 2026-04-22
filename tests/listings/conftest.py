import pytest
from uuid import uuid4
from datetime import datetime

from mutuo.listings.schemas import ListingPublic, CreateListingRequest
from mutuo.listings.models import Listing


@pytest.fixture
def mock_listing_in():
    return CreateListingRequest(
        name="mock",
        description="mock description",
        address="1234 mock",
        beds=3,
        baths=2.5,
        price=8000,
        status="DISPONIBLE"
    )


@pytest.fixture
def mock_listing():
    return Listing(
        listing_id=uuid4(),
        user_id=uuid4(),
        name="mock",
        description="mock description",
        address="1234 mock st",
        beds=3,
        baths=2.5,
        price=15000,
        status="DISPONIBLE",
        created_at=datetime.now()
    )


@pytest.fixture
def mock_listing_public(mock_listing):
    return ListingPublic.model_validate(mock_listing, from_attributes=True)