from fastapi import APIRouter, Request, Response

from mutuo.settings import settings
from mutuo.users.schemas import UserPublic
from mutuo.users.service import get_by_email_hash
from mutuo.security.hashing import deterministic_hash, compare_hash
from mutuo.security.encryption import decrypt
from mutuo.cache.protocols import CacheStore
from mutuo.communications.service import send_email

from .schemas import LoginCredentials, SessionContext, VerifyEmailRequest
from .usecases import login, create_session, verify_email

router = APIRouter(
    tags=["Auth"]
)

@router.post("/login", status_code=200, response_model=UserPublic)
async def auth_login(
    request: Request,
    response: Response,
    data: LoginCredentials
):
    user = await login(
        db=request.state.db,
        deterministic_hash=deterministic_hash,
        compare_hash=compare_hash,
        decryption=decrypt,
        credentials=data,
        get_by_email_hash_fn=get_by_email_hash
    )

    cache_store = request.app.state.cache_store
    ip = getattr(request.state, "ip", None)
    client_agent=request.headers.get("user-agent")
    
    session_context = SessionContext(
        ip=ip,
        client_agent=client_agent
    )

    session_id = await create_session(
        session_context=session_context,
        cache_store=cache_store,
        user=user
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
    
    return user


@router.post("/logout", status_code=200)
async def auth_logout(
    request: Request,
    response: Response
):
    session_id = request.cookies.get("session_id")

    cache_store: CacheStore = request.app.state.cache_store
    await cache_store.delete(str(session_id))

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return {"detail": [{"msg": "Logout successfull"}]}


@router.post("/verify-email", status_code=200)
async def auth_verify_email(
    request: Request,
    data: VerifyEmailRequest
):
    await verify_email(
        db=request.state.db,
        cache_store=request.app.state.cache_store,
        email=data.email,
        deterministic_hash=deterministic_hash,
        get_user_by_email_hash=get_by_email_hash,
        send_email=send_email
    )

    return {"detail": [{"msg": "verification email sent"}]}