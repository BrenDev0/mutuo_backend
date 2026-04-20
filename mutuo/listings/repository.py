from uuid import UUID
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.schemas import Pagination

from .schemas import ListingFilters
from .models import Listing

async def create(db: AsyncSession, listing_in: Listing) -> Listing:
    db.add(listing_in)
    await db.refresh(listing_in)

    return listing_in


async def filter_and_page_listings(
    db: AsyncSession, 
    user_id: UUID, 
    pagination: Pagination,
    filters: Optional[ListingFilters] = None
) -> list[Listing]:
    offset = (pagination.page_number - 1) * pagination.items_per_page
    stmt = select(Listing).where(Listing.user_id == user_id)

    if filters:
        for k, v in filters.model_dump(exclude_none=True).items():
            stmt = stmt.where(getattr(Listing, k) == v)

    stmt = stmt.limit(pagination.items_per_page).offset(offset)

    result = await db.execute(stmt)

    return list(result.scalars().all())