import pytest 
from unittest.mock import patch
from uuid import uuid4

from mutuo.contracts.routes import contracts_delete
from mutuo.contracts.schemas import ContractPublic


@pytest.mark.asyncio
@patch("mutuo.contracts.routes.handle_delete_contract")
async def test_success(
    mock_usecase,
    mock_contract_public,
    mock_get_contract_by_id,
    mock_delete_contract_by_id,
    mock_user_public
):
    mock_usecase.return_value = mock_contract_public
    contract_id = uuid4()
    result = await contracts_delete(
        contract_id=contract_id,
        user=mock_user_public,
        get_contract_by_id=mock_get_contract_by_id,
        delete_contract=mock_delete_contract_by_id
    )

    assert isinstance(result, ContractPublic)
    