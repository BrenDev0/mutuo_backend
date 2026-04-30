import pytest 
from unittest.mock import patch
from mutuo.contracts.routes import contracts_create
from mutuo.contracts.schemas import ContractPublic

@pytest.mark.asyncio
@patch('mutuo.contracts.routes.handle_create_contract')
async def test_success(
    mock_usecase,
    mock_create_request,
    mock_user_public,
    mock_create_contract,
    mock_get_users_listings,
    mock_contract_public
):
    
    mock_usecase.return_value = mock_contract_public
    
    result = await contracts_create(
        data=mock_create_request,
        user=mock_user_public,
        create_contract=mock_create_contract,
        get_users_listings=mock_get_users_listings
    )

    assert isinstance(result, ContractPublic)