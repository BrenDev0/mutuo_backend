from dataclasses import asdict

from .models import ContractRow
from ..models import ContractPartial, Contract


def row_to_domain(row: ContractRow) -> Contract:
    return Contract(
        contract_id=row.contract_id,
        status=row.status,
        listing_id=row.listing_id,
        created_at=row.created_at,
        expiration=row.expiration
    )


def domain_partial_to_row(partial: ContractPartial) -> ContractRow:
    return ContractRow(**asdict(partial))
