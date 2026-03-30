import pytest 
from unittest.mock import patch, call
from mutuo.auth.usecases import update_credentials_with_verification
from mutuo.auth.schemas import UpdateCredentials
from mutuo.users.schemas import UserPublic
from mutuo.exceptions import UnprocessableException, NotfoundException

@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_update_password_success(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
    mock_user
):
    mock_cryptography.compare_hash.return_value = False
    mock_cryptography.deterministic_hash.retrurn_value = "hashed_email"
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_update_user_fn.return_value = mock_user

    mock_changes = UpdateCredentials(
        password="new"
    )

    result = await update_credentials_with_verification(
        db=db,
        cache_store=mock_cache_store,
        changes=mock_changes,
        cryptography=mock_cryptography,
        current_email="email",
        code=123,
        get_user_by_email_hash=mock_get_user_by_email_hash_fn,
        update_user=mock_update_user_fn
    )

    assert isinstance(result, UserPublic)
    mock_cryptography.compare_hash.assert_called_once_with("new", "hashed")
    mock_cryptography.hash.assert_called_once_with("new")
    mock_cryptography.encrypt.assert_not_called()
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_get_user_by_email_hash_fn.assert_called_once_with(db, "hashed_email")
    mock_update_user_fn.assert_called_once()


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_update_email_success(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
    mock_user
):
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_update_user_fn.return_value = mock_user

    mock_changes = UpdateCredentials(
        email="new"
    )

    result = await update_credentials_with_verification(
        db=db,
        cache_store=mock_cache_store,
        changes=mock_changes,
        cryptography=mock_cryptography,
        current_email="email",
        code=123,
        get_user_by_email_hash=mock_get_user_by_email_hash_fn,
        update_user=mock_update_user_fn
    )

    assert isinstance(result, UserPublic)
    mock_cryptography.hash.assert_not_called()
    mock_cryptography.compare_hash.assert_not_called()
    mock_cryptography.encrypt.assert_called_once_with("new")
    mock_cryptography.deterministic_hash.assert_has_calls([call("email"), call("new")])
    mock_get_user_by_email_hash_fn.assert_called_once_with(db, "hashed_email")
    mock_update_user_fn.assert_called_once()




@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_empty_request(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
):
    mock_verify_code_or_raise.return_value = None

    mock_changes = UpdateCredentials()

    with pytest.raises(UnprocessableException) as exc_info:
        await update_credentials_with_verification(
            db=db,
            cache_store=mock_cache_store,
            changes=mock_changes,
            cryptography=mock_cryptography,
            current_email="email",
            code=123,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    mock_cryptography.hash.assert_not_called()
    mock_cryptography.compare_hash.assert_not_called()
    mock_cryptography.encrypt.assert_not_called()
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_get_user_by_email_hash_fn.assert_not_called()
    mock_update_user_fn.assert_not_called()
    assert "At least one field required for update" in str(exc_info)



@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_email_and_password_in_request(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
):
    mock_verify_code_or_raise.return_value = None

    mock_changes = UpdateCredentials(
        email="new",
        password="new"
    )

    with pytest.raises(UnprocessableException) as exc_info:
        await update_credentials_with_verification(
            db=db,
            cache_store=mock_cache_store,
            changes=mock_changes,
            cryptography=mock_cryptography,
            current_email="email",
            code=123,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    mock_cryptography.hash.assert_not_called()
    mock_cryptography.compare_hash.assert_not_called()
    mock_cryptography.encrypt.assert_not_called()
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_get_user_by_email_hash_fn.assert_not_called()
    mock_update_user_fn.assert_not_called()
    assert "Cannot update both email and password" in str(exc_info)


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_user_not_found(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
):
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_email_hash_fn.return_value = None

    mock_changes = UpdateCredentials(
        email="new"
    )

    with pytest.raises(NotfoundException) as exc_info:
        await update_credentials_with_verification(
            db=db,
            cache_store=mock_cache_store,
            changes=mock_changes,
            cryptography=mock_cryptography,
            current_email="email",
            code=123,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    mock_cryptography.hash.assert_not_called()
    mock_cryptography.compare_hash.assert_not_called()
    mock_cryptography.encrypt.assert_not_called()
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_get_user_by_email_hash_fn.assert_called_once_with(db,"hashed_email")
    mock_update_user_fn.assert_not_called()
    assert "User not found" in str(exc_info)


@pytest.mark.asyncio
@patch("mutuo.auth.usecases.verify_code_or_raise")
async def test_current_password_match_new_password(
    mock_verify_code_or_raise,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_update_user_fn,
    db,
    mock_cache_store,
    mock_user
):
    mock_cryptography.compare_hash.return_value = True
    mock_verify_code_or_raise.return_value = None
    mock_get_user_by_email_hash_fn.return_value = mock_user

    mock_changes = UpdateCredentials(
        password="current"
    )

    with pytest.raises(UnprocessableException) as exc_info:
        await update_credentials_with_verification(
            db=db,
            cache_store=mock_cache_store,
            changes=mock_changes,
            cryptography=mock_cryptography,
            current_email="email",
            code=123,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            update_user=mock_update_user_fn
        )

    mock_cryptography.hash.assert_not_called()
    mock_cryptography.compare_hash.assert_called_once_with("current", "hashed")
    mock_cryptography.encrypt.assert_not_called()
    mock_cryptography.deterministic_hash.assert_called_once_with("email")
    mock_get_user_by_email_hash_fn.assert_called_once_with(db,"hashed_email")
    mock_update_user_fn.assert_not_called()
    assert "New password cannot be same as current password" in str(exc_info)