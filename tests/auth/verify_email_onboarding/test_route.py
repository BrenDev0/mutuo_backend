import pytest
from unittest.mock import patch
from mutuo.auth.routes import auth_request_onboarding_email_verification
from mutuo.auth.schemas import VerifyEmailRequest


@pytest.fixture
def mock_verify_email_request():
    return VerifyEmailRequest(
        email="email"
    )

@pytest.mark.asyncio
@patch("mutuo.auth.routes.request_onboarding_email_verification")
async def test_success(
    mock_verify_email,
    mock_request,
    mock_verify_email_request,
    mock_cache_store,
    db
):
    mock_verify_email.return_value = None

    result = await auth_request_onboarding_email_verification(
        db=db,
        data=mock_verify_email_request,
        cache_store=mock_cache_store
    )

    assert isinstance(result, dict)

    assert "verification email sent" in result["detail"][0]["msg"]