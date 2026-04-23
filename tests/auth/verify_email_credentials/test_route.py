import pytest
from unittest.mock import patch
from mutuo.auth.routes import auth_request_update_credentials_email_verification
from mutuo.auth.schemas import VerifyEmailRequest

@pytest.mark.asyncio
@patch("mutuo.auth.routes.request_update_credentials_email_verification")
async def test_success(
    mock_usecase,
    mock_get_user_by_email_hash_fn,
    mock_cache_store,
):
    mock_usecase.return_value = None
    mock_verify_email_request = VerifyEmailRequest(
        email="email"
    )

    result = await auth_request_update_credentials_email_verification(
        get_by_email_hash=mock_get_user_by_email_hash_fn,
        data=mock_verify_email_request,
        cache_store=mock_cache_store
    )

    assert "verification email sent" in result["detail"][0]["msg"]
    mock_usecase.assert_called_once()