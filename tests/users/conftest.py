import pytest 
from uuid import uuid4
from mutuo.users.schemas import UserPublic
from mutuo.users.models import User
from datetime import datetime

user_id = uuid4()

@pytest.fixture
def mock_user_public():
    return UserPublic(
        user_id=user_id,
        name="Carpincha Lucia",
        email="carpincha@carpinchaCo.com",
        profile_type="PROPIETARIO",
        created_at=datetime.now()
    )

@pytest.fixture
def mock_user():
    return User(
        user_id=user_id,
        name="Carpincha Lucia",
        email="carpincha@carpinchaCo.com",
        email_hash="hash",
        password="hashed",
        profile_type="PROPIETARIO",
        created_at=datetime.now()
    )