import pytest
from unittest.mock import patch 

from mutuo.listings.routes import listings_create
from mutuo.listings.schemas import ListingPublic


@pytest.mark.asyncio
@patch("mutuo.listings.routes.handle_create_listing")
async def test_success(
    mock_usecase,
    mock_listing_in,
    mock_user_public,
    mock_listing_public,
    mock_create
):
    mock_usecase.return_value = mock_listing_public
    result = await listings_create(
        data=mock_listing_in,
        create_listing=mock_create,
        user=mock_user_public
    )

    assert isinstance(result, ListingPublic)