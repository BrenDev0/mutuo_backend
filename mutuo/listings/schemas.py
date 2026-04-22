from uuid import UUID
from datetime import datetime
from mutuo.schemas import MutuoSchemaBase, Pagination
from enum import StrEnum

class ListingStatus(StrEnum):
    AVAILABLE = "DISPONIBLE"
    OCCUPIED = "OCUPADO"
    UNAVAILABLE = "NO DISPONIBLE"



class CreateListingRequest(MutuoSchemaBase):
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: ListingStatus


class ListingPublic(MutuoSchemaBase):
    listing_id: UUID
    user_id: UUID
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: str
    created_at: datetime


class ListingPage(Pagination):
    items: list[ListingPublic]


class ListingFilters(MutuoSchemaBase):
    name: str | None = None
    beds: str | None = None
    baths: str | None = None
    price: str | None = None
    status: str | None = None