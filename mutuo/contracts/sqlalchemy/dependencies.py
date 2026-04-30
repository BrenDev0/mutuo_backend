from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mutuo.database.dependencies import get_db_session

from .repository import create
from ..types import CreateContractFn
from ..models import Contract, ContractPartial

def provide_create_contract(db: AsyncSession = Depends(get_db_session)) -> CreateContractFn:
    async def create_contract(contract_in: ContractPartial) -> Contract:
        return await create(db=db, contract_in=contract_in)
    
    return create_contract