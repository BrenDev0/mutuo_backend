import pytest
from mutuo.users.schemas import CreateUser

@pytest.fixture
def mock_create_user_schema():
    return CreateUser(
        name="Carpincha Lucia",
        email="carpincha@carpinchaCo.com",
        password="chonchdeagua",
        profile_type="PROPIETARIO",
        verification_code=123
    )
