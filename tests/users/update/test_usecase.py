import pytest
from unittest.mock import AsyncMock
from mutuo.exceptions import UnauthorizedException, NotfoundException, UnprocessableException
from mutuo.users.usecases import update_user
from mutuo.users.schemas import UpdateUserRequest, UserPublic

@pytest.fixture
def mock_update_user_by_id():
    return AsyncMock()


@pytest.fixture
def mock_get_by_id():
    return AsyncMock()


@pytest.mark.asyncio
async def test_success(
    security_mocks,
    mock_user,
    db,
    mock_update_user_by_id,
    mock_get_by_id
):
    
    hash = security_mocks.hash_fn
    comapre_hash = security_mocks.compare_hash
    encrypt = security_mocks.encryption
    decrypt = security_mocks.decryption
    mock_get_by_id.return_value = mock_user
    mock_update_user_by_id.return_value = mock_user
    mock_update_request = UpdateUserRequest(
        name="name"
    )

    result = await update_user(
        db=db,
        user_id=mock_user.user_id,
        changes=mock_update_request,
        hash=hash,
        compare_hash=comapre_hash,
        encrypt=encrypt,
        decrypt=decrypt,
        get_by_id=mock_get_by_id,
        update_user_by_id=mock_update_user_by_id
    )

    assert isinstance(result, UserPublic)
    mock_get_by_id.assert_called_once_with(
        db,
        mock_user.user_id
    )

    update_data = {
        "name": "enc(name)"
    }

    mock_update_user_by_id.assert_called_once_with(db, mock_user.user_id, update_data)

    

@pytest.mark.asyncio
async def test_user_not_found(
    security_mocks,
    mock_user,
    db,
    mock_update_user_by_id,
    mock_get_by_id
):
    
    hash = security_mocks.hash_fn
    comapre_hash = security_mocks.compare_hash
    encrypt = security_mocks.encryption
    decrypt = security_mocks.decryption
    mock_get_by_id.return_value = None
    mock_update_request = UpdateUserRequest(
        name="name"
    )

    with pytest.raises(NotfoundException) as exc_info:
        await update_user(
            db=db,
            user_id=mock_user.user_id,
            changes=mock_update_request,
            hash=hash,
            compare_hash=comapre_hash,
            encrypt=encrypt,
            decrypt=decrypt,
            get_by_id=mock_get_by_id,
            update_user_by_id=mock_update_user_by_id
        )

    assert "User not found" in str(exc_info)
    mock_update_user_by_id.assert_not_called()




@pytest.mark.asyncio
async def test_no_current_password(
    security_mocks,
    mock_user,
    db,
    mock_update_user_by_id,
    mock_get_by_id
):
    
    hash = security_mocks.hash_fn
    comapre_hash = security_mocks.compare_hash
    encrypt = security_mocks.encryption
    decrypt = security_mocks.decryption
    mock_get_by_id.return_value = mock_user
    mock_update_request = UpdateUserRequest(
        name="name",
        password="new"
    )

    with pytest.raises(UnprocessableException) as exc_info:
        await update_user(
            db=db,
            user_id=mock_user.user_id,
            changes=mock_update_request,
            hash=hash,
            compare_hash=comapre_hash,
            encrypt=encrypt,
            decrypt=decrypt,
            get_by_id=mock_get_by_id,
            update_user_by_id=mock_update_user_by_id
        )

    assert "Cannot update password without current password" in str(exc_info)
    mock_update_user_by_id.assert_not_called()


@pytest.mark.asyncio
async def test_incorrect_password(
    security_mocks,
    mock_user,
    db,
    mock_update_user_by_id,
    mock_get_by_id
):
    
    hash = security_mocks.hash_fn
    comapre_hash = security_mocks.compare_hash
    comapre_hash.return_value = False
    encrypt = security_mocks.encryption
    decrypt = security_mocks.decryption
    mock_get_by_id.return_value = mock_user
    mock_update_request = UpdateUserRequest(
        name="name",
        password="new",
        current_password="current"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        await update_user(
            db=db,
            user_id=mock_user.user_id,
            changes=mock_update_request,
            hash=hash,
            compare_hash=comapre_hash,
            encrypt=encrypt,
            decrypt=decrypt,
            get_by_id=mock_get_by_id,
            update_user_by_id=mock_update_user_by_id
        )

    assert "Incorrect password" in str(exc_info)
    mock_update_user_by_id.assert_not_called()


@pytest.mark.asyncio
async def test_empty_request(
    security_mocks,
    mock_user,
    db,
    mock_update_user_by_id,
    mock_get_by_id
):
    
    hash = security_mocks.hash_fn
    comapre_hash = security_mocks.compare_hash
    encrypt = security_mocks.encryption
    decrypt = security_mocks.decryption
    mock_get_by_id.return_value = mock_user
    mock_update_request = UpdateUserRequest()

    with pytest.raises(UnprocessableException) as exc_info:
        await update_user(
            db=db,
            user_id=mock_user.user_id,
            changes=mock_update_request,
            hash=hash,
            compare_hash=comapre_hash,
            encrypt=encrypt,
            decrypt=decrypt,
            get_by_id=mock_get_by_id,
            update_user_by_id=mock_update_user_by_id
        )

    assert "At least one field required" in str(exc_info)
    mock_update_user_by_id.assert_not_called()


