import pytest
from unittest.mock import patch
from mutuo.auth.service import create_and_cache_verification_code


@pytest.mark.asyncio
@patch("mutuo.auth.service.generate_random_code")
async def test_success(
    mock_generate_code,
    mock_cache_store
):
    code = 123456
    mock_generate_code.return_value = code
    
    result = await create_and_cache_verification_code(
        cache_store=mock_cache_store,
        hashed_email="hashed_email"
    )

    assert isinstance(result, int)

    mock_cache_store.set.assert_called_once_with(
        key="verification:code:hashed_email",
        value=code,
        expire_seconds=60*15
    )