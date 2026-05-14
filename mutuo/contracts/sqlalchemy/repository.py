from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.listings.sqlalchemy.models import ListingRow

from ..models import Contract, ContractPartial
from .mappers import domain_partial_to_row, row_to_domain
from .models import ContractRow
from ..types import SelectContractByIdQuery

async def create(
    db: AsyncSession,
    contract_in: ContractPartial
)-> Contract:
    row = domain_partial_to_row(contract_in)
    db.add(row)
    await db.flush()
    await db.refresh(row)

    return row_to_domain(row)


async def get_by_id(
    db: AsyncSession,
    query: SelectContractByIdQuery
    
) -> Contract | None:
    stmt = select(ContractRow).join(
        ListingRow, 
        ContractRow.listing_id == ListingRow.listing_id
    ).where(
        ContractRow.contract_id == query.contract_id,
        ListingRow.user_id == query.user_id
    )

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None


async def delete_by_id(
    db: AsyncSession,
    contact_id: UUID
) -> Contract | None:
    stmt = delete(ContractRow).where(ContractRow.contract_id == contact_id).returning(ContractRow)

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None

    