import pytest 
from uuid import uuid4
from mutuo.contracts.usecases import handle_delete_contract
from mutuo.exceptions import NotfoundException
from mutuo.contracts.schemas import ContractPublic
from mutuo.contracts.types import SelectContractByIdQuery

@pytest.mark.asyncio
async def test_success(
    mock_delete_contract_by_id,
    mock_get_contract_by_id,
    mock_contract
):
    mock_get_contract_by_id.return_value = mock_contract
    user_id = uuid4()
    mock_delete_contract_by_id.return_value = mock_contract


    result = await handle_delete_contract(
        contract_id=mock_contract.contract_id,
        user_id=user_id,
        get_contract_by_id=mock_get_contract_by_id,
        delete_contract=mock_delete_contract_by_id
    )

    assert isinstance(result, ContractPublic)

    mock_get_contract_by_id.assert_called_once()
    query = mock_get_contract_by_id.await_args.args[0]
    assert isinstance(query, SelectContractByIdQuery)
    assert hasattr(query, "user_id")
    assert query.user_id == user_id
    assert hasattr(query, "contract_id")
    assert query.contract_id == mock_contract.contract_id
    mock_delete_contract_by_id.assert_called_once_with(mock_contract.contract_id)


@pytest.mark.asyncio
async def test_not_found(
    mock_delete_contract_by_id,
    mock_get_contract_by_id
):
    mock_get_contract_by_id.return_value = None
    user_id = uuid4()
    contract_id = uuid4()
 
    with pytest.raises(NotfoundException) as exc_info:
        await handle_delete_contract(
            contract_id=contract_id,
            user_id=user_id,
            get_contract_by_id=mock_get_contract_by_id,
            delete_contract=mock_delete_contract_by_id
        )

    assert "Contract not found" in str(exc_info)

    mock_get_contract_by_id.assert_called_once()
    query = mock_get_contract_by_id.await_args.args[0]
    assert isinstance(query, SelectContractByIdQuery)
    assert hasattr(query, "user_id")
    assert query.user_id == user_id
    assert hasattr(query, "contract_id")
    assert query.contract_id == contract_id
    mock_delete_contract_by_id.assert_not_called()

