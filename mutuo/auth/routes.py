from fastapi import APIRouter, Request, Response, Depends

from mutuo.settings import settings
from mutuo.users.schemas import UserPublic
from mutuo.users.service import get_by_email_hash, create
from mutuo.security.dependencies import get_cryptography_service
from mutuo.security.protocols import CryptographyService
from mutuo.security.hashing import deterministic_hash
from mutuo.cache.protocols import CacheStore
from mutuo.cache.dependencies import get_cache_store
from mutuo.communications.service import send_email, create_verification_email

from .schemas import LoginCredentials, SessionContext, VerifyEmailRequest, RegisterUserRequest
from .usecases import login, create_session, verify_email_onboarding, register_user_with_verification

router = APIRouter(
    tags=["Auth"]
)

async def _create_session_and_set_cookie(
    request: Request,
    response: Response,
    user: UserPublic
):
    ip = getattr(request.state, "ip", None)
    client_agent=request.headers.get("user-agent")
    
    session_context = SessionContext(
        ip=ip,
        client_agent=client_agent
    )

    session_id = await create_session(
        session_context=session_context,
        cache_store=request.app.state.cache_store,
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
    

@router.post("/onboarding/verify-email", status_code=200)
async def auth_verify_email(
    request: Request,
    data: VerifyEmailRequest,
    cache_store: CacheStore = Depends(get_cache_store)
):
    await verify_email_onboarding(
        db=request.state.db,
        cache_store=cache_store,
        email=data.email,
        deterministic_hash=deterministic_hash,
        get_user_by_email_hash=get_by_email_hash,
        create_verification_email=create_verification_email,
        send_email=send_email
    )

    return {"detail": [{"msg": "verification email sent"}]}


@router.post("/register", status_code=201, response_model=UserPublic)
async def auth_register(
    request: Request,
    response: Response,
    data: RegisterUserRequest,
    cryptography: CryptographyService = Depends(get_cryptography_service),
    cache_store: CacheStore = Depends(get_cache_store)
):
    new_user = await register_user_with_verification(
        db=request.state.db,
        user_in=data,
        create_user=create,
        cryptography=cryptography, 
        cache_store=cache_store
    )

   
    await _create_session_and_set_cookie(
        request=request,
        response=response,
        user=new_user
    )

    return new_user


@router.post("/login", status_code=200, response_model=UserPublic)
async def auth_login(
    request: Request,
    response: Response,
    data: LoginCredentials,
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    user = await login(
        db=request.state.db,
        cryptography=cryptography,
        credentials=data,
        get_user_by_email_hash=get_by_email_hash
    )

    await _create_session_and_set_cookie(
        request=request,
        response=response,
        user=user
    )
    
    return user


@router.post("/logout", status_code=200)
async def auth_logout(
    request: Request,
    response: Response,
    cache_store: CacheStore = Depends(get_cache_store)
):
    session_id = request.cookies.get("session_id")

    if session_id:
        await cache_store.delete(f"session:{session_id}")

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return {"detail": [{"msg": "Logout successful"}]}


