import pytest
from mutuo.auth.schemas import LoginCredentials, SessionContext


@pytest.fixture
def mock_credentials():
    return LoginCredentials(
        email="email",
        password="password"
    )

@pytest.fixture
def mock_context():
    return SessionContext(
        ip="1.1.1.1",
        client_agent="client-agent"
    )
