from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mutuo.database.dependencies import get_db_session

from .repository import create, get_by_id, delete_by_id
from ..types import CreateContractFn, GetContractByIdFn, DeleteContractByIdFn, SelectContractByIdQuery
from ..models import Contract, ContractPartial

def provide_create_contract(db: AsyncSession = Depends(get_db_session)) -> CreateContractFn:
    async def create_contract(contract_in: ContractPartial) -> Contract:
        return await create(db=db, contract_in=contract_in)
    
    return create_contract


def provide_get_contract_by_id(db: AsyncSession = Depends(get_db_session)) -> GetContractByIdFn:
    async def get_contract_by_id(query: SelectContractByIdQuery) -> Contract | None:
        return await get_by_id(db=db, query=query)
    
    return get_contract_by_id


def provide_delete_contract_by_id(db: AsyncSession = Depends(get_db_session)) -> DeleteContractByIdFn:
    async def delete_contract_by_id(contract_id: UUID) -> Contract | None:
        return await delete_by_id(db=db, contact_id=contract_id)
    
    return delete_contract_by_id