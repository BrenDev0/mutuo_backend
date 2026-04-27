import pytest
from datetime import datetime
from uuid import uuid4
from mutuo.listings.usecases import get_user_owned_listings
from mutuo.listings.models import Listing
from mutuo.listings.schemas import ListingPage
from mutuo.schemas import Pagination
from mutuo.listings.types import UserListingQuery


mock_collection = [
        Listing(
            listing_id=uuid4(),
            user_id=uuid4(),
            property_type="CASA",
            name="name",
            description="description",
            address="address",
            beds=3,
            baths=2.5,
            price=9999,
            status="DIPSONIBLE",
            created_at=datetime.now()
        ),
        Listing(
            listing_id=uuid4(),
            user_id=uuid4(),
            name="name",
            property_type="CASA",
            description="description",
            address="address",
            beds=3,
            baths=2.5,
            price=9999,
            status="DIPSONIBLE",
            created_at=datetime.now()
        ),
        Listing(
            listing_id=uuid4(),
            user_id=uuid4(),
            name="name",
            property_type="CASA",
            description="description",
            address="address",
            beds=3,
            baths=2.5,
            price=9999,
            status="DIPSONIBLE",
            created_at=datetime.now()
        )
    ]

@pytest.mark.asyncio
async def test_success(
    mock_get_listings_by_user_id

):
    mock_page = Pagination(
        items_per_page=10,
        page_number=1
    )

    user_id = uuid4()
    mock_get_listings_by_user_id.return_value = mock_collection
    result = await get_user_owned_listings(
        user_id=user_id,
        pagination=mock_page,
        get_by_user_id=mock_get_listings_by_user_id
    )

    assert isinstance(result, ListingPage)
    assert hasattr(result, "items")
    assert len(result.items) == 3

    called_query = mock_get_listings_by_user_id.await_args.args[0]

    assert isinstance(called_query, UserListingQuery)
    assert hasattr(called_query, "user_id")
    assert hasattr(called_query, "offset")
    assert hasattr(called_query, "limit")
    assert hasattr(called_query, "filters")
    assert getattr(called_query, "filters") is None
    assert getattr(called_query, "user_id") == user_id



@pytest.mark.asyncio
async def test_no_results(
    mock_get_listings_by_user_id

):
    mock_page = Pagination(
        items_per_page=10,
        page_number=1
    )

    user_id = uuid4()
    mock_get_listings_by_user_id.return_value = list()
    result = await get_user_owned_listings(
        user_id=user_id,
        pagination=mock_page,
        get_by_user_id=mock_get_listings_by_user_id
    )

    assert isinstance(result, ListingPage)
    assert hasattr(result, "items")
    assert len(result.items) == 0

    called_query = mock_get_listings_by_user_id.await_args.args[0]

    assert isinstance(called_query, UserListingQuery)
    assert hasattr(called_query, "user_id")
    assert hasattr(called_query, "offset")
    assert hasattr(called_query, "limit")
    assert hasattr(called_query, "filters")
    assert getattr(called_query, "filters") is None
    assert getattr(called_query, "user_id") == user_id