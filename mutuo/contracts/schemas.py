from enum import StrEnum
from uuid import UUID
from datetime import datetime

from mutuo.schemas import MutuoSchemaBase

class ContractStatus(StrEnum):
    ACTIVE = "ACTIVO"
    EXPIRED = "EXPIRADO"
    PENDING = "EN POROCESO"


class CreateContractRequest(MutuoSchemaBase):
    listing_id: UUID
    expiration: datetime


class ContractPublic(MutuoSchemaBase):
    contract_id: UUID
    listing_id: UUID
    status: str
    expiration: datetime
