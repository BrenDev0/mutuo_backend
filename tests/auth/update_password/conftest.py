import pytest
from mutuo.auth.schemas import UpdatePasswordRequest

@pytest.fixture
def mock_update_password_request():
    return UpdatePasswordRequest(
        new_password="new",
        current_password="current"
    )
