from mutuo.schemas import MutuoSchemaBase


class CreateListingRequest(MutuoSchemaBase):
    name: str
    description: str
    address: str
    beds: int
    baths: float
    price: float
    status: str