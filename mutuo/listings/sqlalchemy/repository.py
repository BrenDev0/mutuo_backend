from uuid import UUID
from typing import Any

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Listing


async def create(db: AsyncSession, listing_in: Listing) -> Listing:
    db.add(listing_in)
    await db.refresh(listing_in)

    return listing_in


async def get_by_id(
    db: AsyncSession,
    lisitng_id: UUID,
    user_id: UUID
) -> Listing | None:
    stmt = select(Listing).where(Listing.user_id == user_id).where(Listing.listing_id == lisitng_id)

    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def get_by_user_id(
    db: AsyncSession, 
    user_id: UUID, 
    offset: int,
    limit: int,
    filters: dict[str, Any] | None = None
) -> list[Listing]:
    stmt = select(Listing).where(Listing.user_id == user_id)

    if filters:
        for k, v in filters.items():
            stmt = stmt.where(getattr(Listing, k) == v)

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)

    return list(result.scalars().all())


async def update_by_id(
    db: AsyncSession,
    listing_id: UUID,
    user_id: UUID,
    changes: dict[str, Any]
) -> Listing | None:
    stmt = update(Listing).where(Listing.user_id == user_id).where(Listing.listing_id == listing_id).values(**changes).returning(Listing)

    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def delete_by_id(
    db: AsyncSession,
    listing_id: UUID,
    user_id: UUID
)-> Listing | None:
    stmt = delete(Listing).where(Listing.listing_id == listing_id).where(Listing.user_id == user_id).returning(Listing)

    result = await db.execute(stmt)

    return result.scalar_one_or_none()