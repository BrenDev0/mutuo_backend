from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.exceptions import UnprocessableException, NotfoundException, UnauthorizedException
from mutuo.security.protocols import CryptographyService

from .models import User
from .schemas import UpdateUserRequest
from .transformers import to_user_public
from .types import  UpdateUserFn, GetByIdFn


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    changes: UpdateUserRequest,
    cryptography: CryptographyService,
    get_user_by_id: GetByIdFn,
    update_user_by_id: UpdateUserFn
):
    user: User | None = await get_user_by_id(db, user_id)
    if user is None:
        raise NotfoundException("User not found")
    
    update_data = {}
    
    if changes.password is not None:
        if not changes.current_password:
            raise UnprocessableException("Cannot update password without current password")
        
        if not cryptography.compare_hash(changes.current_password, user.password):
            raise UnauthorizedException("Incorrect password")
        
        update_data["password"] = cryptography.hash(changes.password)

    
    if changes.name is not None:
        update_data["name"] = cryptography.encrypt(changes.name)

    if not update_data:
        raise UnprocessableException("At least one field required for update")
    
    updated_user = await update_user_by_id(db, user.user_id, update_data)

    return to_user_public(updated_user, cryptography.decrypt)

    
        

    

