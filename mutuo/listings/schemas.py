from typing import List, Optional
from uuid import UUID

from mutuo.schemas import MutuoSchemaBase, Pagination


class CreateListingRequest(MutuoSchemaBase):
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: str


class ListingPublic(MutuoSchemaBase):
    listing_id: UUID
    user_id: UUID


class ListingPage(Pagination):
    items: List[ListingPublic]


class ListingFilters(MutuoSchemaBase):
    name: Optional[str] = None
    beds: Optional[str] = None
    baths: Optional[str] = None
    price: Optional[str] = None
    status: Optional[str] = None