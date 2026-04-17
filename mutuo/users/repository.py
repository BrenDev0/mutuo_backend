from uuid import UUID
from typing import Dict, Any
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


async def create(
    db: AsyncSession,
    user_in: User
) -> User:
    db.add(user_in)
    await db.refresh(user_in)

    return user_in


async def get_by_id(
    db: AsyncSession,
    user_id: UUID
) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def get_by_email_hash(
    db: AsyncSession,
    email_hash: str
) -> User | None: 
    stmt = select(User).where(User.email_hash == email_hash)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def update_by_id(
    db: AsyncSession,
    user_id: UUID,
    changes: Dict[str, Any]
):
    stmt = update(User).where(User.user_id == user_id).values(**changes).returning(User)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def delete_by_id(
    db: AsyncSession,
    user_id: UUID
) -> User | None:
    stmt = delete(User).where(User.user_id == user_id).returning(User)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()



    