import pytest
from mutuo.users.routes import users_create
from unittest.mock import patch
from uuid import uuid4
from mutuo.users.schemas import UserPublic, CreateUser
from mutuo.settings import settings
from mutuo.auth.schemas import SessionContext


@pytest.mark.asyncio
@patch("mutuo.users.routes.create_session")
@patch("mutuo.users.routes.create_user")
async def test_success(
    mock_create_user,
    mock_create_session,
    mock_request,
    mock_response,
    mock_create_user_schema,
    mock_cache_store,
    mock_user_public
):
    session_id = uuid4()
    mock_create_user.return_value = mock_user_public
    mock_request.state.ip = "0.0.0.0"
    mock_request.headers = {"user-agent": "mock_agent"}
    mock_create_session.return_value = session_id
    mock_context = SessionContext(
        ip="0.0.0.0",
        client_agent="mock_agent"
    )
    mock_request.app.state.cache_store = mock_cache_store

    result = await users_create(
        request=mock_request,
        response=mock_response,
        data=mock_create_user_schema
    )

    assert isinstance(result, UserPublic)

    mock_create_session.assert_called_once_with(
        session_context=mock_context,
        cache_store=mock_cache_store,
        user=mock_user_public
    )

    mock_response.set_cookie.assert_called_once_with(
        key="session_id",
        value=str(session_id),
        max_age=settings.SESSION_MAX_AGE,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )



    