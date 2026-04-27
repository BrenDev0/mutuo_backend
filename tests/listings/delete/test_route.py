import pytest 
from unittest.mock import patch
from uuid import uuid4
from mutuo.listings.routes import listings_delete_by_id
from mutuo.listings.schemas import ListingPublic


@pytest.mark.asyncio
@patch("mutuo.listings.routes.handle_delete_listing")
async def test_success(
    mock_usecase,
    mock_user_public,
    mock_delete_listing_by_id,
    mock_listing_public
):
    mock_usecase.return_value = mock_listing_public 
    result = await listings_delete_by_id(
        listing_id=uuid4(),
        user=mock_listing_public,
        delete_listing_by_id=mock_delete_listing_by_id
    )

    assert isinstance(result, ListingPublic)
