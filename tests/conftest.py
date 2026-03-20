import pytest
from unittest.mock import AsyncMock, Mock


@pytest.fixture
def db():
    return AsyncMock()

@pytest.fixture
def mock_cache_store():
    return AsyncMock()


@pytest.fixture
def security_mocks():
    encryption = Mock(side_effect=lambda x: f"enc({x})")
    decryption = Mock(side_effect=lambda x: x.replace("enc(", "").replace(")", ""))
    hash_fn = Mock(return_value="hashed_password")
    deterministic_hash = Mock(return_value="hashed_email")

    return {
    "encryption": encryption,
    "decryption": decryption,
    "hash": hash_fn,
    "deterministic_hash": deterministic_hash,
}