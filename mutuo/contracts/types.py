from typing import Callable, Awaitable
from uuid import UUID
from dataclasses import dataclass

from .models import ContractPartial, Contract

CreateContractFn = Callable[[ContractPartial], Awaitable[Contract]]
DeleteContractByIdFn = Callable[[UUID], Awaitable[Contract | None]]

@dataclass(frozen=True)
class SelectContractByIdQuery:
    user_id: UUID
    contract_id: UUID

GetContractByIdFn = Callable[[SelectContractByIdQuery], Awaitable[Contract | None]]


