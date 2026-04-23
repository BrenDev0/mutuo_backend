from dataclasses import asdict
from .models import ListingRow
from ..models import Listing, ListingPartial

def row_to_domain(row: ListingRow) -> Listing:
    return Listing(
        listing_id=row.listing_id,
        user_id=row.user_id,
        property_type=row.property_type,
        name=row.name,
        description=row.description,
        address=row.address,
        beds=row.beds,
        baths=row.baths,
        price=row.price,
        status=row.status,
        created_at=row.created_at
    )

def domain_partial_to_row(partial: ListingPartial) -> ListingRow:
    return ListingRow(**asdict(partial))