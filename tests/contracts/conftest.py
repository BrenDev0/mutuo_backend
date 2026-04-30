import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from datetime import datetime

from mutuo.contracts.models import Contract
from mutuo.listings.models import Listing
from mutuo.contracts.schemas import CreateContractRequest, ContractPublic


@pytest.fixture
def mock_create_request():
    return CreateContractRequest(
        listing_id=uuid4(),
        expiration=datetime.now()
    )


@pytest.fixture
def mock_create_contract():
    return AsyncMock()


@pytest.fixture
def mock_get_users_listings():
    return AsyncMock()


@pytest.fixture
def mock_contract():
    return Contract(
        contract_id=uuid4(),
        status="ACTIVO",
        listing_id=uuid4(),
        expiration=datetime.now(),
        created_at=datetime.now()
    )


@pytest.fixture
def mock_listing():
    return Listing(
        listing_id=uuid4(),
        user_id=uuid4(),
        property_type="CASA",
        name="mock",
        description="mock description",
        address="1234 mock st",
        beds=3,
        baths=2.5,
        price=15000,
        status="DISPONIBLE",
        created_at=datetime.now()
    )


@pytest.fixture
def mock_contract_public():
    return ContractPublic(
        contract_id=uuid4(),
        listing_id=uuid4(),
        status="ACTIVO",
        expiration=datetime.now()
    )
