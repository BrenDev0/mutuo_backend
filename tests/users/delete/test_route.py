import pytest
from unittest.mock import patch
from uuid import uuid4
from mutuo.users.routes import users_delete
from mutuo.users.schemas import UserPublic


@pytest.mark.asyncio
@patch("mutuo.users.routes.delete_session")
@patch("mutuo.users.routes.delete_by_id")
async def test_success(
    mock_delete_by_id,
    mock_delete_session,
    mock_request,
    mock_response,
    mock_user_public,
    mock_cache_store,
    db
):
    session_id = uuid4()
    cookies = {"session_id": str(session_id)}
    mock_request.cookies = cookies
    mock_delete_by_id.return_value = mock_user_public
    mock_delete_session.return_value = session_id

    result = await users_delete(
        request=mock_request,
        response=mock_response,
        user=mock_user_public,
        db=db,
        cache_store=mock_cache_store
    )

    assert isinstance(result, UserPublic)
    mock_response.delete_cookie.assert_called_once_with(
        key="session_id",
        path="/"
    )
    mock_delete_session.assert_called_once_with(
        cache_store=mock_cache_store,
        session_id=session_id,
        user_id=mock_user_public.user_id
    )