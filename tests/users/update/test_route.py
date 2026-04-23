import pytest 
from unittest.mock import patch, AsyncMock
from mutuo.users.routes import users_update_profile
from mutuo.users.schemas import UpdateUserRequest, UserPublic

@pytest.fixture
def mock_update_request():
    return UpdateUserRequest(
        name="name"
    )





@pytest.mark.asyncio
@patch("mutuo.users.routes.handle_update_user")
async def test_success(
    mock_update_user,
    mock_user_public,
    mock_update_request,

):
    mock_update_user.return_value = mock_user_public
    mock_update_user_repo = AsyncMock()
    mock_get_by_id_repo = AsyncMock()
    result = await users_update_profile(
        get_by_id=mock_get_by_id_repo,
        update_user=mock_update_user_repo,
        data=mock_update_request,
        user=mock_user_public
    )

    assert isinstance(result, UserPublic)
    