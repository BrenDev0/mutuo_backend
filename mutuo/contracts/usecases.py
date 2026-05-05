from uuid import UUID

from mutuo.listings.types import GetListingsByUserIdFn, UserListingQuery
from mutuo.exceptions import NotfoundException

from .schemas import CreateContractRequest, ContractStatus, ContractPublic
from .types import CreateContractFn, DeleteContractByIdFn, GetContractByIdFn, SelectContractByIdQuery
from .models import ContractPartial
from .mappers import contract_to_public



async def handle_create_contract(
    contract_data: CreateContractRequest,
    user_id: UUID,
    get_users_listings: GetListingsByUserIdFn,
    create_contract: CreateContractFn,
) -> ContractPublic:
    listing_query = UserListingQuery(
        user_id=user_id,
        offset=0,
        limit=1,
        filters={"listing_id": contract_data.listing_id}
    )

    listings = await get_users_listings(listing_query)

    if not listings:
        raise NotfoundException("Listing not found")
    

    contract_in = ContractPartial(
        status=ContractStatus.PENDING,
        **contract_data.model_dump(by_alias=False)
    )

    new_contract = await create_contract(contract_in)

    return contract_to_public(new_contract)
    


async def handle_delete_contract(
    contract_id: UUID,
    user_id: UUID,
    get_contract_by_id: GetContractByIdFn,
    delete_contract: DeleteContractByIdFn
) -> ContractPublic:
    query = SelectContractByIdQuery(
        user_id=user_id,
        contract_id=contract_id
    )

    contract = await get_contract_by_id(query)

    if not contract:
        raise NotfoundException("Contract not found")
    
    deleted_contract = await delete_contract(contract_id)

    return contract_to_public(deleted_contract)
    
