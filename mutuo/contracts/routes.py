from  uuid import UUID

from fastapi import Depends, APIRouter

from mutuo.users.schemas import UserPublic
from mutuo.auth.dependencies import user_is_owner
from mutuo.listings.sqlalchemy.dependencies import provide_get_listings_by_user_id
from mutuo.listings.types import GetListingsByUserIdFn

from .sqlalchemy.dependencies import provide_create_contract, provide_delete_contract_by_id, provide_get_contract_by_id
from .schemas import ContractPublic, CreateContractRequest
from .types import CreateContractFn, GetContractByIdFn, DeleteContractByIdFn
from .usecases import handle_create_contract, handle_delete_contract

router = APIRouter(
    tags=['Contracts']
)


@router.post("", status_code=201, response_model=ContractPublic)
async def contracts_create(
    data: CreateContractRequest,
    user: UserPublic = Depends(user_is_owner),
    create_contract: CreateContractFn = Depends(provide_create_contract),
    get_users_listings: GetListingsByUserIdFn = Depends(provide_get_listings_by_user_id)
):
    return await handle_create_contract(
        contract_data=data,
        user_id=user.user_id,
        get_users_listings=get_users_listings,
        create_contract=create_contract
    )


@router.delete("/{contract_id}", status_code=200, response_model=ContractPublic)
async def contracts_delete(
    contract_id: UUID,
    user: UserPublic = Depends(user_is_owner),
    get_contract_by_id: GetContractByIdFn = Depends(provide_get_contract_by_id),
    delete_contract: DeleteContractByIdFn = Depends(provide_delete_contract_by_id)
):
    return await handle_delete_contract(
        contract_id=contract_id,
        user_id=user.user_id,
        get_contract_by_id=get_contract_by_id,
        delete_contract=delete_contract
    )