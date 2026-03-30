import pytest
from unittest.mock import patch, call
from mutuo.auth.service import verify_code_or_raise
from mutuo.exceptions import UnauthorizedException


@pytest.mark.asyncio
@patch("mutuo.auth.service.ensure_not_blocked_from_verification")
async def test_success(
    mock_ensure_not_blocked,
    mock_cache_store
):
    mock_ensure_not_blocked.return_value = None
    mock_cache_store.get.return_value = 123456

    result = await verify_code_or_raise(
        cache_store=mock_cache_store,
        hashed_email="hashed_email",
        code_from_user=123456
    )

    assert result == None
    mock_cache_store.get.assert_called_once_with(
        key="verification:code:hashed_email"
    )

    mock_cache_store.delete.assert_has_calls([
        call("verification:code:hashed_email"),
        call("verification:attempts:hashed_email"),
        call("verification:blocked:hashed_email")
    ])

    mock_cache_store.increment.assert_not_called()


@pytest.mark.asyncio
@patch("mutuo.auth.service.ensure_not_blocked_from_verification")
async def test_expired_or_no_verification_code(
    mock_ensure_not_blocked,
    mock_cache_store
):
    mock_cache_store.get.return_value = None
    mock_ensure_not_blocked.return_value = None

    with pytest.raises(UnauthorizedException) as exc_info:
        await verify_code_or_raise(
            cache_store=mock_cache_store,
            hashed_email="hashed_email",
            code_from_user=123456
        )

    assert "Invalid or expired verification code" in str(exc_info)

    mock_cache_store.get.assert_called_once_with(
        key="verification:code:hashed_email"
    )

    mock_cache_store.delete.assert_not_called()

    mock_cache_store.increment.assert_not_called()


@pytest.mark.asyncio
@patch("mutuo.auth.service.ensure_not_blocked_from_verification")
async def test_incorrect_code(
    mock_ensure_not_blocked,
    mock_cache_store
):
    mock_cache_store.get.return_value = 123456
    mock_ensure_not_blocked.return_value = None
    mock_cache_store.increment.return_value = 1

    with pytest.raises(UnauthorizedException) as exc_info:
        await verify_code_or_raise(
            cache_store=mock_cache_store,
            hashed_email="hashed_email",
            code_from_user=123457
        )

    assert "Unauthorized" in str(exc_info)

    mock_cache_store.get.assert_called_once_with(
        key="verification:code:hashed_email"
    )

    mock_cache_store.delete.assert_not_called()

    mock_cache_store.increment.assert_called_once_with("verification:attempts:hashed_email")


@pytest.mark.asyncio
@patch("mutuo.auth.service.ensure_not_blocked_from_verification")
async def test_incorrect_code_max_attempts_reached(
    mock_ensure_not_blocked,
    mock_cache_store
):
    mock_cache_store.get.return_value = 123456
    mock_ensure_not_blocked.return_value = None
    mock_cache_store.increment.return_value = 3

    with pytest.raises(UnauthorizedException) as exc_info:
        await verify_code_or_raise(
            cache_store=mock_cache_store,
            hashed_email="hashed_email",
            code_from_user=123457
        )

    assert "Unauthorized" in str(exc_info)

    mock_cache_store.get.assert_called_once_with(
        key="verification:code:hashed_email"
    )

    mock_cache_store.delete.assert_has_calls([
        call("verification:code:hashed_email"),
        call("verification:attempts:hashed_email")
    ])

    mock_cache_store.set.assert_called_once_with(
        key="verification:blocked:hashed_email",
        value=1,
        expire_seconds=60*10
    )

    mock_cache_store.increment.assert_called_once_with("verification:attempts:hashed_email")