import pytest
from unittest.mock import patch
from mutuo.auth.usecases import update_email
from mutuo.users.schemas import UserPublic
from mutuo.exceptions import NotfoundException


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_success(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_cache_store,
    mock_update_user_fn,
    mock_get_user_by_id_fn,
    mock_user,
    mock_update_email_req
):
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_id_fn.return_value = mock_user
    mock_update_user_fn.return_value = mock_user
    mock_cryptography.deterministic_hash.return_value = "hashed_email"
    mock_cryptography.encrypt.return_value = "encrypted"
    
    result = await update_email(
        user_id=mock_user.user_id,
        cryptography=mock_cryptography,
        cache_store=mock_cache_store,
        get_user_by_id=mock_get_user_by_id_fn,
        update_user=mock_update_user_fn,
        data_in=mock_update_email_req
    )

    assert isinstance(result, UserPublic)
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_verify_code_or_raise.assert_called_once_with(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=123456
    )
    mock_get_user_by_id_fn.assert_called_once_with(mock_user.user_id)
    mock_cryptography.encrypt.assert_called_once_with("email")  
    mock_update_user_fn.assert_awaited_once_with(
        mock_user.user_id,
        {
            "email": "encrypted",
            "email_hash": "hashed_email"  
        }
    )


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_user_not_found(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_cache_store,
    mock_update_user_fn,
    mock_get_user_by_id_fn,
    mock_user,
    mock_update_email_req
):
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_id_fn.return_value = None
    mock_cryptography.deterministic_hash.return_value = "hashed_email"


    with pytest.raises(NotfoundException) as exc_info:

        await update_email(
            user_id=mock_user.user_id,
            cryptography=mock_cryptography,
            cache_store=mock_cache_store,
            get_user_by_id=mock_get_user_by_id_fn,
            update_user=mock_update_user_fn,
            data_in=mock_update_email_req
        )


    assert "User not found" in str(exc_info)
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_verify_code_or_raise.assert_called_once_with(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=123456
    )
    mock_get_user_by_id_fn.assert_called_once_with(mock_user.user_id)
    mock_cryptography.encrypt.assert_not_called() 
    mock_update_user_fn.assert_not_called()