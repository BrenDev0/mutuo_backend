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

from .schemas import  UserPublic, UpdateUserRequest
from .usecases import update_user

from .service import (
    delete_by_id,
    update_by_id,
    get_by_id
)


router = APIRouter(
    tags=["Users"]
)


@router.patch("", status_code=200, response_model=UserPublic)
async def users_update(
    data: UpdateUserRequest,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(get_current_user),
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    return await update_user(
        db=db,
        user_id=user.user_id,
        changes=data,
        cryptography=cryptography,
        get_user_by_id=get_by_id,
        update_user_by_id=update_by_id
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







    