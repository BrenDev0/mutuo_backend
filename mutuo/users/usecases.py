from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.exceptions import UnprocessableException, NotfoundException, UnauthorizedException
from mutuo.security.types import EncryptFn, HashFn, CompareHashFn, DecryptFn

from .models import User
from .schemas import UpdateUserRequest
from .transformers import to_user_public
from .types import  UpdateUserFn, GetByIdFn


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    changes: UpdateUserRequest,
    hash: HashFn,
    compare_hash: CompareHashFn,
    encrypt: EncryptFn,
    decrypt: DecryptFn,
    get_by_id: GetByIdFn,
    update_user: UpdateUserFn
):
    user: User | None = await get_by_id(db, user_id)
    if user is None:
        raise NotfoundException("User not found")
    
    update_data = {}
    
    if changes.password != None:
        if not changes.current_password:
            raise UnprocessableException("Cannot update password without current password")
        
        if not compare_hash(changes.current_password, user.password):
            raise UnauthorizedException("Incorrect password")
        
        update_data["password"] = hash(changes.password)

    
    if changes.name != None:
        changes["name"] = encrypt(changes.name)

    if not update_data:
        raise UnprocessableException("At least one field required for update")
    
    updated_user = await update_user(db, user.user_id, changes)

    return to_user_public(updated_user, decrypt)

    
        

    

