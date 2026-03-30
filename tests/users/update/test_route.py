import pytest 
from unittest.mock import patch
from mutuo.users.routes import users_update
from mutuo.users.schemas import UpdateUserRequest, UserPublic

@pytest.fixture
def mock_update_request():
    return UpdateUserRequest(
        name="name"
    )



@pytest.mark.asyncio
@patch("mutuo.users.routes.update_user")
async def test_success(
    mock_update_user,
    mock_user_public,
    mock_update_request,
    db
):
    mock_update_user.return_value = mock_user_public

    result = await users_update(
        db=db,
        data=mock_update_request,
        user=mock_user_public
    )

    assert isinstance(result, UserPublic)
    