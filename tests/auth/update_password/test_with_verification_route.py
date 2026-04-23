import pytest 
from unittest.mock import patch
from mutuo.auth.routes import auth_update_password_with_verification_code


@pytest.mark.asyncio
@patch("mutuo.auth.routes.update_password_with_verification_code")
async def test_success(
    mock_usecase,
    mock_update_password_with_verification_code_request,
    mock_get_user_by_email_hash_fn,
    mock_cache_store,
    mock_cryptography
):
    mock_usecase.return_value = None
    result = await auth_update_password_with_verification_code(
        data=mock_update_password_with_verification_code_request,
        get_by_email_hash=mock_get_user_by_email_hash_fn,
        cache_store=mock_cache_store,
        cryptography=mock_cryptography
    )

    assert "Password reset" in result["detail"][0]["msg"]