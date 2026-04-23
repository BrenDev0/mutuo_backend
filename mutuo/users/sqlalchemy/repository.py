from uuid import UUID
from typing import Any
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .mappers import row_to_domain, domain_partial_to_row
from .models import UserRow
from ..models import User, UserPartial


async def create(
    db: AsyncSession,
    user_in: UserPartial
) -> User:
    row = domain_partial_to_row(user_in)
    db.add(row)
    await db.flush()
    await db.refresh(row)

    return row_to_domain(row)


async def get_by_id(
    db: AsyncSession,
    user_id: UUID
) -> User | None:
    stmt = select(UserRow).where(UserRow.user_id == user_id)
    result = await db.execute(stmt)

    row = result.scalar_one_or_none()
    return row_to_domain(row) if row else None


async def get_by_email_hash(
    db: AsyncSession,
    email_hash: str
) -> User | None: 
    stmt = select(UserRow).where(UserRow.email_hash == email_hash)
    result = await db.execute(stmt)

    row = result.scalar_one_or_none()
    return row_to_domain(row) if row else None


async def update_by_id(
    db: AsyncSession,
    user_id: UUID,
    changes: dict[str, Any]
) -> User:
    stmt = update(UserRow).where(UserRow.user_id == user_id).values(**changes).returning(UserRow)
    result = await db.execute(stmt)

    row = result.scalar_one()
    return row_to_domain(row)


async def delete_by_id(
    db: AsyncSession,
    user_id: UUID
) -> User | None:
    stmt = delete(UserRow).where(UserRow.user_id == user_id).returning(UserRow)
    result = await db.execute(stmt)

    row = result.scalar_one_or_none()
    return row_to_domain(row) if row else None



    