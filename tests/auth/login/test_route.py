import pytest
from mutuo.auth.routes import auth_login
from unittest.mock import patch
from uuid import uuid4
from mutuo.users.schemas import UserPublic
from mutuo.settings import settings
from mutuo.auth.schemas import SessionContext


@pytest.mark.asyncio
@patch("mutuo.auth.routes.create_session")
@patch("mutuo.auth.routes.login")
async def test_success(
    mock_login,
    mock_create_session,
    mock_user_public,
    mock_cache_store,
    mock_request,
    mock_response,
    mock_credentials,
    db
):
    mock_session_id = uuid4()
    mock_login.return_value = mock_user_public
    mock_request.app.state.cache_store = mock_cache_store
    mock_request.state.db = db
    mock_request.state.ip = "1.1.1.1"
    mock_request.headers = {"user-agent": "mock_agent"}
    mock_create_session.return_value = mock_session_id

   
    result = await auth_login(
        request=mock_request,
        response=mock_response,
        data=mock_credentials
    )



    assert isinstance(result, UserPublic)
    mock_context = SessionContext(
        ip="1.1.1.1",
        client_agent="mock_agent"
    )

    mock_create_session.assert_called_once_with(
        cache_store=mock_cache_store,
        session_context=mock_context,
        user=mock_user_public
    )

    
    mock_response.set_cookie.assert_called_once_with(
        key="session_id",
        value=str(mock_session_id),
        max_age=settings.SESSION_MAX_AGE,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )
    