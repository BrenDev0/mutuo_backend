from uuid import UUID
from mutuo.exceptions import UnprocessableException, NotfoundException
from mutuo.security.protocols import CryptographyService

from .models import User
from .schemas import UpdateUserRequest
from .mappers import to_user_public
from .types import  UpdateUserFn, GetByIdFn


async def handle_update_user(
    user_id: UUID,
    changes: UpdateUserRequest,
    cryptography: CryptographyService,
    get_user_by_id: GetByIdFn,
    update_user_by_id: UpdateUserFn
):
    user: User | None = await get_user_by_id(user_id)
    if user is None:
        raise NotfoundException("User not found")
    
    update_data = {}
    
    if changes.name is not None:
        update_data["name"] = cryptography.encrypt(changes.name)

    if not update_data:
        raise UnprocessableException("At least one field required for update")
    
    updated_user = await update_user_by_id(user.user_id, update_data)

    return to_user_public(updated_user, cryptography.decrypt)

    
        

    

