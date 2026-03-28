from uuid import UUID
from fastapi import APIRouter, Request, Response, Depends

from mutuo.auth.usecases import  delete_session
from mutuo.auth.dependencies import get_current_user
from mutuo.security.hashing import hash, compare_hash
from mutuo.security.encryption import encrypt, decrypt

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
    request: Request,
    data: UpdateUserRequest,
    user: UserPublic = Depends(get_current_user)
):
    return await update_user(
        db=request.state.db,
        user_id=user.user_id,
        changes=data,
        hash=hash,
        compare_hash=compare_hash,
        encrypt=encrypt,
        decrypt=decrypt,
        get_by_id=get_by_id,
        update_user_by_id=update_by_id
    )


@router.delete("", status_code=200, response_model=UserPublic)
async def users_delete(
    request: Request,
    response: Response,
    user: UserPublic = Depends(get_current_user)
):
    await delete_by_id(
        db=request.state.db,
        user_id=user.user_id
    )

    cache_store = request.app.state.cache_store
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







    