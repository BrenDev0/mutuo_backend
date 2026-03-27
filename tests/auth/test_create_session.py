import pytest
from uuid import UUID
from unittest.mock import call
from mutuo.auth.usecases import create_session



@pytest.mark.asyncio
async def test_success(
    mock_user_public,
    mock_cache_store,
    mock_context
):
    result = await create_session(
        session_context=mock_context,
        cache_store=mock_cache_store,
        user=mock_user_public
    )

    assert mock_cache_store.set.call_count == 2
    assert isinstance(result, UUID)



