from uuid import UUID
from datetime import datetime
from mutuo.schemas import MutuoSchemaBase, Pagination
from enum import StrEnum

class ListingStatus(StrEnum):
    AVAILABLE = "DISPONIBLE"
    OCCUPIED = "OCUPADO"
    UNAVAILABLE = "NO DISPONIBLE"


class PropertyType(StrEnum):
    HOUSE = "CASA"
    APARTMENT = "DEPARTAMENTO"
    LAND = "TERRENO"
    COMMERCIAL = "LOCAL"
    BUILDING = "EDIFICIO"
    CONDO = "CONDOMINIO"


class CreateListingRequest(MutuoSchemaBase):
    property_type: PropertyType
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
    property_type: str
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
    property_type: str | None
    name: str | None = None
    beds: str | None = None
    baths: str | None = None
    price: str | None = None
    status: str | None = None