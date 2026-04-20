from fastapi import Request, HTTPException, Depends
from uuid import UUID

from mutuo.cache.protocols import CacheStore
from mutuo.security.encryption import decrypt
from mutuo.users.repository import get_by_id
from mutuo.users.transformers import to_user_public
from mutuo.users.schemas import UserPublic

from .schemas import SessionSchema, ProfileType


def get_session_id(
    request: Request
):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=400, detail="Unauthorized")
    
    return UUID(session_id)


async def get_current_user(
    request: Request,
    session_id: UUID = Depends(get_session_id)
):
    cache_store: CacheStore = request.app.state.cache_store
    session = await cache_store.get(str(session_id))

    if session is None:
        raise HTTPException(status_code=400, detail="Unauthorized")
    
    session = SessionSchema(**session)
    
    user_cache_key = f"cache:user:{session.user_id}"
    user_cache = await cache_store.get(user_cache_key)

    if not user_cache:
        user = await get_by_id(
            db=request.state.db,
            user_id=session.user_id
        )

        if not user:
            raise HTTPException(status_code=400, detail="Unauthorized")
        
        user_public = to_user_public(
            user=user,
            decryption=decrypt
        )

        await cache_store.set(
            key=user_cache_key,
            value=user_public.model_dump(mode="json"),
            expire_seconds=60*5
        )

    return user_public


async def user_is_owner(
    user: UserPublic = Depends(get_current_user)
):
    if user.profile_type == ProfileType.OWNER:
        return user
    
    else:
        raise HTTPException(status_code=403, detail="Current profile type is not authorized to create listings")


        

