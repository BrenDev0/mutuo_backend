import pytest 
from mutuo.auth.service import ensure_not_blocked_from_verification
from mutuo.exceptions import UnauthorizedException

@pytest.mark.asyncio
async def test_not_blocked(
    mock_cache_store
):
    
    mock_cache_store.get.return_value = None

    result = await ensure_not_blocked_from_verification(
        hashed_email="hashed_email",
        cache_store=mock_cache_store
    )

    mock_cache_store.get.assert_called_once_with(
        "verification:blocked:hashed_email"
    )

    assert result is None


@pytest.mark.asyncio
async def test_user_blocked(
    mock_cache_store
):
    mock_cache_store.return_value = 1

    with pytest.raises(UnauthorizedException) as exc_info:
        await ensure_not_blocked_from_verification(
            hashed_email="hashed_email",
            cache_store=mock_cache_store
        )

    assert "Max verification attempts reached" in str(exc_info)
    mock_cache_store.get.assert_called_once_with(
        "verification:blocked:hashed_email"
    )


