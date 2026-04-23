from uuid import UUID
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.dependencies import get_db_session
from mutuo.auth.usecases import  delete_session
from mutuo.auth.dependencies import get_current_user
from mutuo.security.protocols import CryptographyService
from mutuo.security.dependencies import get_cryptography_service
from mutuo.cache.protocols import CacheStore
from mutuo.cache.dependencies import get_cache_store

from .sqlalchemy.dependencies import provide_update_user, provide_get_by_id
from .schemas import  UserPublic, UpdateUserRequest
from .usecases import handle_update_user
from .types import UpdateUserFn, GetByIdFn

from .repository import (
    delete_by_id
)


router = APIRouter(
    tags=["Users"]
)


@router.patch("", status_code=200, response_model=UserPublic)
async def users_update_profile(
    data: UpdateUserRequest,
    update_user: UpdateUserFn = Depends(provide_update_user),
    get_by_id: GetByIdFn = Depends(provide_get_by_id),
    user: UserPublic = Depends(get_current_user),
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    """
    Update user profile info

    ### Args: 
    - **name**: New name(optional)
    
    ### Returns:
    - **200**: user public schema

    ### Raises
    - **422 UNPROCESSABLE**: If empty request
    - **404 NOT FOUND**: If user not found
    """
    return await handle_update_user(
        user_id=user.user_id,
        changes=data,
        cryptography=cryptography,
        get_user_by_id=get_by_id,
        update_user_by_id=update_user
    )


@router.delete("", status_code=200, response_model=UserPublic)
async def users_delete(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(get_current_user),
    cache_store: CacheStore = Depends(get_cache_store)
):
    await delete_by_id(
        db=db,
        user_id=user.user_id
    )

    session_id = UUID(request.cookies.get("session_id"))

    await delete_session(
        cache_store=cache_store,
        session_id=session_id,
        user_id=user.user_id
    )

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return user







    