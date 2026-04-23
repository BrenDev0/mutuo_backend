import pytest
from unittest.mock import AsyncMock, Mock
from mutuo.auth.usecases import request_onboarding_email_verification
from mutuo.exceptions import ConflictException, UnauthorizedException

@pytest.fixture
def mock_create_verify_email_message():
    return Mock()

@pytest.fixture
def mock_get_by_email_fn():
    return AsyncMock()

@pytest.fixture
def mock_send_email():
    return Mock()

@pytest.mark.asyncio
async def test_success(
    mock_cryptography,
    mock_get_by_email_fn,
    mock_send_email,
    mock_cache_store,
    mock_create_verify_email_message
):
    mock_get_by_email_fn.return_value = None
    mock_cache_store.get.return_value = None

    await request_onboarding_email_verification(
        cache_store=mock_cache_store,
        email="email",
        deterministic_hash=mock_cryptography.deterministic_hash,
        get_user_by_email_hash=mock_get_by_email_fn,
        create_verification_email=mock_create_verify_email_message,
        send_email=mock_send_email
    )

    mock_send_email.assert_called_once()
    mock_get_by_email_fn.assert_called_once()


@pytest.mark.asyncio
async def test_email_in_use(
    mock_user,
    mock_cryptography,
    mock_send_email,
    mock_get_by_email_fn,
    mock_cache_store,
    mock_create_verify_email_message
):
    mock_get_by_email_fn.return_value = mock_user
    mock_cache_store.get.return_value = None

    with pytest.raises(ConflictException) as exc_info:
        await request_onboarding_email_verification(
            cache_store=mock_cache_store,
            email="email",
            deterministic_hash=mock_cryptography.deterministic_hash,
            get_user_by_email_hash=mock_get_by_email_fn,
            create_verification_email=mock_create_verify_email_message,
            send_email=mock_send_email
        )
    
    assert "Email in use" in str(exc_info)

    mock_send_email.assert_not_called()


@pytest.mark.asyncio
async def test_max_attemts(
    mock_user,
    mock_cryptography,
    mock_send_email,
    mock_get_by_email_fn,
    mock_cache_store,
    mock_create_verify_email_message
):
    mock_get_by_email_fn.return_value = mock_user
    mock_cache_store.get.return_value = 1

    with pytest.raises(UnauthorizedException) as exc_info:
        await request_onboarding_email_verification(
            cache_store=mock_cache_store,
            email="email",
            deterministic_hash=mock_cryptography.deterministic_hash,
            get_user_by_email_hash=mock_get_by_email_fn,
            create_verification_email=mock_create_verify_email_message,
            send_email=mock_send_email
        )
    
    assert "Max verification attempts reached" in str(exc_info)

    mock_send_email.assert_not_called()
