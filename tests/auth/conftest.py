import pytest
from mutuo.auth.schemas import LoginCredentials, SessionContext
import pytest
from mutuo.auth.schemas import RegisterUserRequest

@pytest.fixture
def mock_create_user_schema():
    return RegisterUserRequest(
        name="Carpincha Lucia",
        email="carpincha@carpinchaCo.com",
        password="chonchdeagua",
        profile_type="PROPIETARIO",
        verification_code=123
    )



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
