from uuid import UUID
from datetime import datetime

from dataclasses import dataclass

@dataclass(frozen=True)
class Listing:
    listing_id: UUID
    user_id: UUID
    property_type: str
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: str
    created_at: datetime



@dataclass(frozen=True)
class ListingPartial:
    user_id: UUID
    property_type: str
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: str

