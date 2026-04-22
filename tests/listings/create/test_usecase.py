import pytest 
from unittest.mock import AsyncMock

from mutuo.listings.usecases import handle_create_listing
from mutuo.listings.schemas import CreateListingRequest, ListingPublic
from mutuo.listings.models import Listing

@pytest.fixture
def mock_create():
    return AsyncMock()


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



@pytest.mark.asyncio
async def test_success(
    mock_listing,
    mock_create,
    mock_listing_in,
    db
):
    
    mock_create.return_value = mock_listing


    result = await handle_create_listing(
        db=db,
        user_id=mock_listing.user_id,
        listing_in=mock_listing_in,
        create_listing=mock_create
    )


    assert isinstance(result, ListingPublic)
    mock_create.assert_called_once()
    called_db, called_listing = mock_create.await_args.args

    assert called_db is db
    assert isinstance(called_listing, Listing)
    assert called_listing.name == "mock"
    assert called_listing.description == "mock description"
    assert called_listing.address == "1234 mock"
    assert called_listing.beds == 3
    assert called_listing.baths == 2.5
    assert called_listing.price == 8000
    assert called_listing.status == "DISPONIBLE"



