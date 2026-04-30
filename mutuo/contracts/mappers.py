from .models import Contract
from .schemas import ContractPublic

def contract_to_public(model: Contract) -> ContractPublic:
    return ContractPublic.model_validate(model, from_attributes=True)