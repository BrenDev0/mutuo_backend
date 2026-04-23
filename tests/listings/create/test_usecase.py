import pytest 

from mutuo.listings.usecases import handle_create_listing
from mutuo.listings.schemas import ListingPublic
from mutuo.listings.models import ListingPartial

@pytest.mark.asyncio
async def test_success(
    mock_listing,
    mock_create,
    mock_listing_in
):
    
    mock_create.return_value = mock_listing


    result = await handle_create_listing(
        user_id=mock_listing.user_id,
        listing_in=mock_listing_in,
        create_listing=mock_create
    )


    assert isinstance(result, ListingPublic)
    mock_create.assert_called_once()

    called_listing = mock_create.await_args.args[0]


    assert isinstance(called_listing, ListingPartial)
    assert called_listing.name == "mock"
    assert called_listing.description == "mock description"
    assert called_listing.address == "1234 mock"
    assert called_listing.beds == 3
    assert called_listing.baths == 2.5
    assert called_listing.price == 8000
    assert called_listing.status == "DISPONIBLE"



