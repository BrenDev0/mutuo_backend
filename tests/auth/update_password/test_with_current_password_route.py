import pytest
from unittest.mock import patch
from mutuo.auth.routes import auth_update_password
from mutuo.users.schemas import UserPublic

@pytest.mark.asyncio
@patch("mutuo.auth.routes.update_password_with_current_password")
async def test_success(
    mock_usecase,
    mock_update_password_request,
    mock_user_public,
    mock_cryptography,
    mock_get_user_by_id_fn,
    mock_update_user_fn
):
    mock_usecase.return_value = mock_user_public
    result = await auth_update_password(
        mock_update_password_request,
        update_by_id=mock_update_user_fn,
        get_by_id=mock_get_user_by_id_fn,
        user=mock_user_public,
        cryptography=mock_cryptography
    )


    assert isinstance(result, UserPublic)
