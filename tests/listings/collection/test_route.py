import pytest 
from uuid import uuid4
from datetime import datetime
from unittest.mock import patch
from mutuo.listings.routes import listings_owners_collection
from mutuo.listings.schemas import ListingPage, ListingPublic
from mutuo.schemas import Pagination


@pytest.mark.asyncio
@patch("mutuo.listings.routes.get_user_owned_listings")
async def test_success(
    mock_usecase,
    mock_user_public,
    mock_get_listings_by_user_id
):
    mock_page = ListingPage(
        items_per_page=10,
        page_number=2,
        items=[
        ListingPublic(
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
        ListingPublic(
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
    ]
    )


    mock_usecase.return_value = mock_page

    result = await listings_owners_collection(
        pagination=Pagination(items_per_page=10, page_number=2),
        user=mock_user_public,
        get_by_user_id=mock_get_listings_by_user_id,
    )

    assert isinstance(result, ListingPage)
