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
    items: list[ListingPublic]


class ListingFilters(MutuoSchemaBase):
    name: str | None = None
    beds: str | None = None
    baths: str | None = None
    price: str | None = None
    status: str | None = None