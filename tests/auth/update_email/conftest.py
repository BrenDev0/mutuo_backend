import pytest 
from mutuo.auth.schemas import UpdateEmailRequest


@pytest.fixture
def mock_update_email_req():
    return UpdateEmailRequest(
        verification_code=123456,
        new_email="email"
    )