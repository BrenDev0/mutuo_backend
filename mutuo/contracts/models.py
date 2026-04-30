from uuid import UUID
from datetime import datetime

from dataclasses import dataclass

@dataclass(frozen=True)
class Contract:
    contract_id: UUID
    status: str
    listing_id: UUID
    created_at: datetime
    expiration: datetime


@dataclass(frozen=True)
class ContractPartial:
    status: str
    listing_id: UUID
    expiration: datetime