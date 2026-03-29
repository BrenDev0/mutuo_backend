import pytest
from unittest.mock import patch
from mutuo.auth.routes import auth_verify_email
from mutuo.auth.schemas import VerifyEmailRequest


@pytest.fixture
def mock_verify_email_request():
    return VerifyEmailRequest(
        email="email"
    )

@pytest.mark.asyncio
@patch("mutuo.auth.routes.verify_email_onboarding")
async def test_success(
    mock_verify_email,
    mock_cryptography,
    mock_request,
    mock_verify_email_request,
    mock_cache_store,
    db
):
    mock_verify_email.return_value = None
    mock_request.db = db

    result = await auth_verify_email(
        request=mock_request,
        data=mock_verify_email_request,
        cache_store=mock_cache_store,
        cryptography=mock_cryptography
    )

    assert isinstance(result, dict)

    assert "verification email sent" in result["detail"][0]["msg"]