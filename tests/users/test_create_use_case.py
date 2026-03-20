import pytest
from unittest.mock import AsyncMock, call

from mutuo.users.schemas import CreateUser, UserPublic
from mutuo.users.usecases import create_user

@pytest.fixture
def mock_create_fn():
    return AsyncMock()


@pytest.fixture
def mock_create_user_schema():
    return CreateUser(
        name="Carpincha Lucia",
        email="carpincha@carpinchaCo.com",
        password="chonchdeagua",
        profile_type="PROPIETARIO",
        verification_code=123
    )



@pytest.mark.asyncio
async def test_success(
    db,
    security_mocks,
    mock_create_user_schema,
    mock_create_fn,
    mock_user,
    mock_cache_store
):
    
    encryption = security_mocks["encryption"]
    decryption = security_mocks["decryption"]
    hash = security_mocks["hash"]
    deterministic_hash = security_mocks["deterministic_hash"]
    mock_cache_store.get.side_effect = [None, 123]

    mock_create_fn.return_value = mock_user

    result = await create_user(
        db=db,
        user_in=mock_create_user_schema,
        encryption=encryption,
        decryption=decryption,
        hash=hash,
        deterministic_hash=deterministic_hash,
        create_fn=mock_create_fn,
        cache_store=mock_cache_store
    )

    assert isinstance(result, UserPublic)
    encryption.assert_has_calls(calls=[call("Carpincha Lucia"), call("carpincha@carpinchaCo.com")])
    decryption.assert_has_calls(calls=[call("Carpincha Lucia"), call("carpincha@carpinchaCo.com")])
    hash.assert_called_once_with("chonchdeagua")
    assert mock_cache_store.get.call_count == 2
    deterministic_hash.assert_has_calls(calls=[call("carpincha@carpinchaCo.com"), call("carpincha@carpinchaCo.com")])

    