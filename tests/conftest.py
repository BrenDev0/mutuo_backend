import pytest
from uuid import uuid4
from dataclasses import dataclass
from unittest.mock import AsyncMock, Mock
from datetime import datetime
from mutuo.users.schemas import UserPublic
from mutuo.users.models import User

@pytest.fixture
def db():
    return AsyncMock()

@pytest.fixture
def mock_cache_store():
    return AsyncMock()

@dataclass
class Cryptography:
    encrypt = Mock(side_effect=lambda x: f"enc({x})")
    decrypt = Mock(side_effect=lambda x: x.replace("enc(", "").replace(")", ""))
    hash = Mock(return_value="hashed")
    compare_hash = Mock(return_value=True)
    deterministic_hash = Mock(return_value="hashed_email")

@pytest.fixture
def mock_cryptography():
    return  Cryptography()


@pytest.fixture
def mock_request():
    return Mock()

@pytest.fixture
def mock_response():
    return Mock()

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

@pytest.fixture
def mock_update_user_fn():
    return AsyncMock()


@pytest.fixture
def mock_get_user_by_email_hash_fn():
    return AsyncMock()
