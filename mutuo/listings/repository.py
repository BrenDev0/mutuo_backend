from uuid import UUID
from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.models import Pagation

from .models import Listing

async def create(db: AsyncSession, listing_in: Listing) -> Listing:
    db.add(listing_in)
    await db.refresh(listing_in)

    return listing_in


async def get_listings_by_user_id(db: AsyncSession, user_id: UUID, pageation: Pagation, filters: dict = None) -> List[Listing]:
    stmt = select(Listing).where(Listing.user_id == user_id)

    result = await db.execute(stmt)

    return result.scalars().all()