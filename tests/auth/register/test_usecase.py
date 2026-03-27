import pytest
from unittest.mock import AsyncMock, call

from mutuo.users.schemas import UserPublic
from mutuo.auth.usecases import register_user_with_verification
from mutuo.exceptions import UnauthorizedException

@pytest.fixture
def mock_create_fn():
    return AsyncMock()


@pytest.mark.asyncio
async def test_success(
    db,
    security_mocks,
    mock_create_user_schema,
    mock_create_fn,
    mock_user,
    mock_cache_store
):
    
    encryption = security_mocks.encryption
    decryption = security_mocks.decryption
    hash = security_mocks.hash_fn
    deterministic_hash = security_mocks.deterministic_hash
    mock_cache_store.get.side_effect = [None, 123]

    mock_create_fn.return_value = mock_user

    result = await register_user_with_verification(
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


@pytest.mark.asyncio
async def test_incorrect_verification_code(
    mock_cache_store,
    security_mocks,
    mock_create_user_schema,
    mock_create_fn,
    db
):
    encryption = security_mocks.encryption
    decryption = security_mocks.decryption
    hash = security_mocks.hash_fn
    deterministic_hash = security_mocks.deterministic_hash
    mock_cache_store.get.side_effect = [None, 1333]
    mock_cache_store.increment.return_value = 1


    with pytest.raises(UnauthorizedException) as exc: 
        await register_user_with_verification(
            db=db,
            user_in=mock_create_user_schema,
            encryption=encryption,
            decryption=decryption,
            hash=hash,
            deterministic_hash=deterministic_hash,
            create_fn=mock_create_fn,
            cache_store=mock_cache_store
        )
    
    assert "Unauthorized" in str(exc)

@pytest.mark.asyncio
async def test_max_attemps_blocked(
    mock_cache_store,
    security_mocks,
    mock_create_user_schema,
    mock_create_fn,
    db
):
    encryption = security_mocks.encryption
    decryption = security_mocks.decryption
    hash = security_mocks.hash_fn
    deterministic_hash = security_mocks.deterministic_hash
    mock_cache_store.get.return_value = 1


    with pytest.raises(UnauthorizedException) as exc: 
        await register_user_with_verification(
            db=db,
            user_in=mock_create_user_schema,
            encryption=encryption,
            decryption=decryption,
            hash=hash,
            deterministic_hash=deterministic_hash,
            create_fn=mock_create_fn,
            cache_store=mock_cache_store
        )
    
    assert "Max verification" in str(exc)



@pytest.mark.asyncio
async def test_expired_code(
    mock_cache_store,
    security_mocks,
    mock_create_user_schema,
    mock_create_fn,
    db
):
    encryption = security_mocks.encryption
    decryption = security_mocks.decryption
    hash = security_mocks.hash_fn
    deterministic_hash = security_mocks.deterministic_hash
    mock_cache_store.get.side_effect = [None, None]


    with pytest.raises(UnauthorizedException) as exc: 
        await register_user_with_verification(
            db=db,
            user_in=mock_create_user_schema,
            encryption=encryption,
            decryption=decryption,
            hash=hash,
            deterministic_hash=deterministic_hash,
            create_fn=mock_create_fn,
            cache_store=mock_cache_store
        )
    
    assert "Invalid or expired" in str(exc)


    



    