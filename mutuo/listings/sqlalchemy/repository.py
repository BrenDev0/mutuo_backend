from uuid import UUID
from typing import Any

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from.mappers import row_to_domain, domain_partial_to_row
from .models import ListingRow
from ..models import Listing, ListingPartial


async def create(db: AsyncSession, listing_in: ListingPartial) -> Listing:
    row = domain_partial_to_row(listing_in)
    db.add(row)
    await db.flush()
    await db.refresh(row)

    return row_to_domain(row)


async def get_by_id(
    db: AsyncSession,
    lisitng_id: UUID,
    user_id: UUID
) -> Listing | None:
    stmt = select(ListingRow).where(ListingRow.user_id == user_id).where(ListingRow.listing_id == lisitng_id)

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None


async def get_by_user_id(
    db: AsyncSession, 
    user_id: UUID, 
    offset: int,
    limit: int,
    filters: dict[str, Any] | None = None
) -> list[Listing]:
    stmt = select(ListingRow).where(ListingRow.user_id == user_id)

    if filters:
        for k, v in filters.items():
            stmt = stmt.where(getattr(Listing, k) == v)

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    return list(row_to_domain(row) for row in rows)


async def update_by_id(
    db: AsyncSession,
    listing_id: UUID,
    user_id: UUID,
    changes: dict[str, Any]
) -> Listing | None:
    stmt = update(ListingRow).where(ListingRow.user_id == user_id).where(ListingRow.listing_id == listing_id).values(**changes).returning(ListingRow)

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None


async def delete_by_id(
    db: AsyncSession,
    listing_id: UUID,
    user_id: UUID
)-> Listing | None:
    stmt = delete(ListingRow).where(ListingRow.listing_id == listing_id).where(ListingRow.user_id == user_id).returning(ListingRow)

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None