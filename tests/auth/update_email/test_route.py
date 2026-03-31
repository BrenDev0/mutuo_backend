import pytest
from unittest.mock import patch
from mutuo.auth.routes import auth_update_email
from mutuo.users.schemas import UserPublic


@pytest.mark.asyncio
@patch("mutuo.auth.routes.update_email")
async def test_success(
    mock_usecase,
    db,
    mock_user_public,
    mock_cryptography,
    mock_cache_store,
    mock_update_email_req
):
    
    mock_usecase.return_value = mock_user_public
 
    result = await auth_update_email(
        data=mock_update_email_req,
        current_user=mock_user_public,
        db=db,
        cryptography=mock_cryptography,
        cache_store=mock_cache_store
    )

    assert isinstance(result, UserPublic)