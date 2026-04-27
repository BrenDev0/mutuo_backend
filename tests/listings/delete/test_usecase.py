import pytest
from uuid import uuid4
from mutuo.listings.usecases import handle_delete_listing
from mutuo.listings.schemas import ListingPublic
from mutuo.listings.types import DeleteListingCommand
from mutuo.exceptions import NotfoundException


@pytest.mark.asyncio
async def test_success(
    mock_delete_listing_by_id,
    mock_listing
):
    mock_delete_listing_by_id.return_value = mock_listing
    mock_user_id = uuid4()
    mock_listing_id = uuid4()
    result = await handle_delete_listing(
        user_id=mock_user_id,
        listing_id=mock_listing_id,
        delete_listing_by_id=mock_delete_listing_by_id
    )

    assert isinstance(result, ListingPublic)

    repo_call_args = mock_delete_listing_by_id.await_args.args[0]

    assert isinstance(repo_call_args, DeleteListingCommand)
    assert repo_call_args.user_id == mock_user_id
    assert repo_call_args.listing_id == mock_listing_id


@pytest.mark.asyncio
async def test_not_found(
    mock_delete_listing_by_id
):
    mock_delete_listing_by_id.return_value = None
    mock_user_id = uuid4()
    mock_listing_id = uuid4()

    with pytest.raises(NotfoundException) as exc_info:
        await handle_delete_listing(
            user_id=mock_user_id,
            listing_id=mock_listing_id,
            delete_listing_by_id=mock_delete_listing_by_id
        )

    repo_call_args = mock_delete_listing_by_id.await_args.args[0]

    assert isinstance(repo_call_args, DeleteListingCommand)
    assert repo_call_args.user_id == mock_user_id
    assert repo_call_args.listing_id == mock_listing_id

    assert "Listing not found" in str(exc_info)
