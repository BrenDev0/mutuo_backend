from uuid import UUID
from fastapi import APIRouter, Request, Response, Depends

from mutuo.security.encryption import encrypt, decrypt
from mutuo.security.hashing import hash, deterministic_hash
from mutuo.settings import settings
from mutuo.auth.schemas import SessionContext
from mutuo.auth.usecases import create_session, delete_session
from mutuo.auth.dependencies import get_current_user

from .schemas import CreateUser,  UserPublic
from .usecases import (
    create_user
)
from .service import (
    create,
    delete_user
)


router = APIRouter(
    tags=["Users"]
)


@router.post("", status_code=201, response_model=UserPublic)
async def users_create(
    request: Request,
    response: Response,
    data: CreateUser
):
    cache_store = request.app.state.cache_store

    new_user = await create_user(
        db=request.state.db,
        user_in=data,
        encryption=encrypt,
        decryption=decrypt,
        hash=hash,
        deterministic_hash=deterministic_hash,
        create_fn=create,
        cache_store=cache_store
    )

   
    ip = getattr(request.state, "ip", None)
    client_agent=request.headers.get("user-agent")
    
    session_context = SessionContext(
        ip=ip,
        client_agent=client_agent
    )

    session_id = await create_session(
        session_context=session_context,
        cache_store=cache_store,
        user=new_user
    )

    
    response.set_cookie(
        key="session_id",
        value=str(session_id),
        max_age=settings.SESSION_MAX_AGE,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )

    return new_user


@router.delete("", status_code=200, response_model=UserPublic)
async def users_delete(
    request: Request,
    response: Response,
    user: UserPublic = Depends(get_current_user)
):
    deleted_user= await delete_user(
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







    