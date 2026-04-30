import pytest 
from uuid import uuid4
from datetime import datetime
from mutuo.contracts.usecases import handle_create_contract
from mutuo.contracts.schemas import CreateContractRequest, ContractPublic
from mutuo.contracts.models import ContractPartial
from mutuo.exceptions import NotfoundException
from mutuo.listings.types import UserListingQuery


@pytest.mark.asyncio
async def test_success(
    mock_create_contract,
    mock_get_users_listings,
    mock_listing,
    mock_contract,
    mock_create_request
):
    mock_get_users_listings.return_value = mock_listing
    mock_create_contract.return_value = mock_contract

    user_id = uuid4()

    result = await handle_create_contract(
        contract_data=mock_create_request,
        user_id=user_id,
        get_users_listings=mock_get_users_listings,
        create_contract=mock_create_contract
    )


    
    assert isinstance(result, ContractPublic)
    mock_get_users_listings.assert_awaited_once()
    listings_query = mock_get_users_listings.await_args.args[0]
    assert isinstance(listings_query,UserListingQuery)
    mock_create_contract.assert_called_once()
    create_call = mock_create_contract.await_args.args[0]
    assert isinstance(create_call, ContractPartial)


@pytest.mark.asyncio
async def test_listing_not_found(
    mock_create_contract,
    mock_get_users_listings,
    mock_contract,
    mock_create_request
):
    mock_get_users_listings.return_value = []
    mock_create_contract.return_value = mock_contract

    user_id = uuid4()

    with pytest.raises(NotfoundException) as exc_info:
        await handle_create_contract(
            contract_data=mock_create_request,
            user_id=user_id,
            get_users_listings=mock_get_users_listings,
            create_contract=mock_create_contract
        )

    assert "Listing not found" in str(exc_info)
    mock_get_users_listings.assert_awaited_once()
    listings_query = mock_get_users_listings.await_args.args[0]
    assert isinstance(listings_query,UserListingQuery)
    mock_create_contract.assert_not_called()
