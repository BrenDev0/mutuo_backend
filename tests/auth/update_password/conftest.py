import pytest
from mutuo.auth.schemas import UpdatePasswordRequest, UpdatePasswordWithVerificationCodeRequest

@pytest.fixture
def mock_update_password_request():
    return UpdatePasswordRequest(
        new_password="new",
        current_password="current"
    )

@pytest.fixture
def mock_update_password_with_verification_code_request():
    return UpdatePasswordWithVerificationCodeRequest(
        current_email="current_email",
        new_password="new_password",
        verification_code=123456
    )
