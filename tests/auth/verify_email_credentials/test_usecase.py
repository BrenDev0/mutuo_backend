import pytest
from unittest.mock import Mock, patch
from mutuo.exceptions import NotfoundException
from mutuo.auth.usecases import request_update_credentials_email_verification

@pytest.fixture
def mock_send_email():
    return Mock()


@pytest.fixture
def mock_create_verification_email():
    return Mock()


@pytest.mark.asyncio
@patch("mutuo.auth.usecases._create_and_send_verification_email")
@patch("mutuo.auth.usecases.ensure_not_blocked_from_verification")
async def test_success(
    mock_ensure_not_blocked,
    mock_create_and_send_verification_email,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_send_email,
    mock_user,
    db,
    mock_cache_store,
    mock_create_verification_email
):
    mock_ensure_not_blocked.return_value = None
    d_hash = mock_cryptography.deterministic_hash
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_create_and_send_verification_email.return_value = None

    await request_update_credentials_email_verification(
        db=db,
        cache_store=mock_cache_store,
        email="email",
        deterministic_hash=d_hash,
        get_user_by_email_hash=mock_get_user_by_email_hash_fn,
        create_verification_email=mock_create_verification_email,
        send_email=mock_send_email
    )

    d_hash.assert_called_once_with("email")
    mock_ensure_not_blocked.assert_called_once_with(
        hashed_email="hashed_email",
        cache_store=mock_cache_store
    )

    mock_get_user_by_email_hash_fn.assert_called_once_with(
        db,
        "hashed_email"
    )

    mock_create_and_send_verification_email.assert_called_once_with(
        cache_store=mock_cache_store,
        create_verification_email=mock_create_verification_email,
        send_email=mock_send_email,
        hashed_email="hashed_email",
        unhashed_email="email"
    )


    


@pytest.mark.asyncio
@patch("mutuo.auth.usecases._create_and_send_verification_email")
@patch("mutuo.auth.usecases.ensure_not_blocked_from_verification")
async def test_user_not_found(
    mock_ensure_not_blocked,
    mock_create_and_send_verification_email,
    mock_cryptography,
    mock_get_user_by_email_hash_fn,
    mock_send_email,
    db,
    mock_cache_store,
    mock_create_verification_email
):
    mock_ensure_not_blocked.return_value = None
    d_hash = mock_cryptography.deterministic_hash
    mock_get_user_by_email_hash_fn.return_value = None

    with pytest.raises(NotfoundException) as exc_info:
        await request_update_credentials_email_verification(
            db=db,
            cache_store=mock_cache_store,
            email="email",
            deterministic_hash=d_hash,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn,
            create_verification_email=mock_create_verification_email,
            send_email=mock_send_email
        )

    assert "User not found" in str(exc_info)

    d_hash.assert_called_once_with("email")
    mock_ensure_not_blocked.assert_called_once_with(
        hashed_email="hashed_email",
        cache_store=mock_cache_store
    )

    mock_get_user_by_email_hash_fn.assert_called_once_with(
        db,
        "hashed_email"
    )

    mock_create_and_send_verification_email.assert_not_called()
