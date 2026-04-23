import pytest 
from unittest.mock import patch
from mutuo.auth.usecases import update_password_with_verification_code
from mutuo.exceptions import NotfoundException, UnprocessableException

@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_success(
    mock_verify_code_or_raise,
    mock_cache_store,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    mock_user,
    mock_update_password_with_verification_code_request
):
    mock_verify_code_or_raise.return_value = None
    mock_cryptography.deterministic_hash.return_value = "hashed_email"
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_cryptography.compare_hash.return_value = False
    mock_cryptography.hash.return_value = "hashed"

    await update_password_with_verification_code(
        cache_store=mock_cache_store,
        cryptography=mock_cryptography,
        data_in=mock_update_password_with_verification_code_request,
        get_user_by_email_hash=mock_get_user_by_email_hash_fn,
        update_user=mock_update_user_fn
    )

    mock_cryptography.deterministic_hash.assert_called_once_with(
        mock_update_password_with_verification_code_request.current_email
    )

    mock_verify_code_or_raise.assert_called_once_with(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=mock_update_password_with_verification_code_request.verification_code
    )

    mock_get_user_by_email_hash_fn.assert_called_once_with("hashed_email")
    mock_cryptography.compare_hash.assert_called_once_with(
        mock_update_password_with_verification_code_request.new_password,
        "hashed"
    )
    mock_update_user_fn.assert_called_once_with(
        mock_user.user_id,
        {
            "password": "hashed"
        }
    )


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_user_not_found(
    mock_verify_code_or_raise,
    mock_cache_store,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    mock_update_password_with_verification_code_request
):
    mock_verify_code_or_raise.return_value = None
    mock_cryptography.deterministic_hash.return_value = "hashed_email"
    mock_get_user_by_email_hash_fn.return_value = None

    with pytest.raises(NotfoundException) as exc_info:
        await update_password_with_verification_code(
            cache_store=mock_cache_store,
            cryptography=mock_cryptography,
            data_in=mock_update_password_with_verification_code_request,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    assert "User not found" in str(exc_info)
    mock_cryptography.deterministic_hash.assert_called_once_with(
        mock_update_password_with_verification_code_request.current_email
    )

    mock_verify_code_or_raise.assert_called_once_with(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=mock_update_password_with_verification_code_request.verification_code
    )

    mock_get_user_by_email_hash_fn.assert_called_once_with("hashed_email")
    mock_cryptography.compare_hash.assert_not_called()
    mock_update_user_fn.assert_not_called()


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_same_as_current_password(
    mock_verify_code_or_raise,
    mock_cache_store,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    mock_user,
    mock_update_password_with_verification_code_request
):
    mock_verify_code_or_raise.return_value = None
    mock_cryptography.deterministic_hash.return_value = "hashed_email"
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_cryptography.compare_hash.return_value = True

    with pytest.raises(UnprocessableException) as exc_info:
        await update_password_with_verification_code(
            cache_store=mock_cache_store,
            cryptography=mock_cryptography,
            data_in=mock_update_password_with_verification_code_request,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    assert "New password cannot be same as old password" in str(exc_info)

    mock_cryptography.deterministic_hash.assert_called_once_with(
        mock_update_password_with_verification_code_request.current_email
    )

    mock_verify_code_or_raise.assert_called_once_with(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=mock_update_password_with_verification_code_request.verification_code
    )

    mock_get_user_by_email_hash_fn.assert_called_once_with("hashed_email")
    mock_cryptography.compare_hash.assert_called_once_with(
        mock_update_password_with_verification_code_request.new_password,
        "hashed"
    )
    mock_update_user_fn.assert_not_called()