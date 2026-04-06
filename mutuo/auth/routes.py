from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.database.dependencies import get_db_session
from mutuo.settings import settings
from mutuo.users.schemas import UserPublic
from mutuo.users.service import get_by_email_hash, create, update_by_id, get_by_id
from mutuo.security.dependencies import get_cryptography_service
from mutuo.security.protocols import CryptographyService
from mutuo.security.hashing import deterministic_hash
from mutuo.cache.protocols import CacheStore
from mutuo.cache.dependencies import get_cache_store
from mutuo.communications.service import send_email, create_verification_email

from .schemas import (
    LoginCredentials, 
    SessionContext,
    VerifyEmailRequest, 
    RegisterUserRequest,
    UpdateEmailRequest,
    UpdatePasswordRequest,
    UpdatePasswordWithVerificationCodeRequest
)
from .usecases import (
    login, 
    create_session, 
    request_onboarding_email_verification, 
    request_update_credentials_email_verification, 
    register_user_with_verification,
    update_password_with_current_password,
    update_password_with_verification_code,
    update_email
)
from .dependencies import get_current_user

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
    

@router.post("/email-verification/onboarding", status_code=200)
async def auth_request_onboarding_email_verification(
    data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db_session),
    cache_store: CacheStore = Depends(get_cache_store)
):
    """
    Send verification code to users email. 

    **For user registration only**
    
    ### Args: 
    - **email**: email to send the verification link to

    ### Returns: 
    - success message
    
    ### Rasies: 
    - **409 CONFLICT**: if email is in use
    
    """
    await request_onboarding_email_verification(
        db=db,
        cache_store=cache_store,
        email=data.email,
        deterministic_hash=deterministic_hash,
        get_user_by_email_hash=get_by_email_hash,
        create_verification_email=create_verification_email,
        send_email=send_email
    )

    return {"detail": [{"msg": "verification email sent"}]}


@router.post("/email-verification/credentials", status_code=200)
async def auth_request_update_credentials_email_verification(
    data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db_session),
    cache_store: CacheStore = Depends(get_cache_store)
):
    """
    Send verification code to users email. 

    **For user updating credentials; email, or password(account recovery) only**
    
    ### Args: 
    - **email**: email to send the verification link to

    ### Returns: 
    - **200**: success message
    
    ### Rasies: 
    - **404 NOT FOUND**: if user with email provided is not found
    
    """
    await request_update_credentials_email_verification(
        db=db,
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
    db: AsyncSession = Depends(get_db_session),
    cryptography: CryptographyService = Depends(get_cryptography_service),
    cache_store: CacheStore = Depends(get_cache_store)
):
    """
    User registration
    
    **must call auth/email-verification/onboarding before calling this endpoint**

    ### Args: 
    - **name**: name of user
    - **email**: email of user
    - **profileType**: must be 'PROPIETARIO' or 'INQUILINO'
    - **password**: user password
    - **verificationCode**: code sent to users email
    
    ### Returns:
    - **201**: user public schema

    ### Raises
    - **401 UNAUTHORIZED**: if incorrect code givin, max attempst (3) reached, or if code has expired or not been sent.
    
    **If max attempts are reached user will be blocked for 10 mins**

    """
    new_user = await register_user_with_verification(
        db=db,
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
    db: AsyncSession = Depends(get_db_session),
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    """
    User login

    ### Args: 
    - **email**: email of user
    - **password**: user password
    
    ### Returns:
    - **200**: user public schema

    ### Raises
    - **401 UNAUTHORIZED**: if incorrect email or password provided
    """
    user = await login(
        db=db,
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
    """
    User logout

    ### Returns:
    - **200**: success message 
    """
    session_id = request.cookies.get("session_id")

    if session_id:
        await cache_store.delete(f"session:{session_id}")

    response.delete_cookie(
        key="session_id",
        path="/"
    )

    return {"detail": [{"msg": "Logout successful"}]}


@router.patch("/email", status_code=200, response_model=UserPublic)
async def auth_update_email(
    data: UpdateEmailRequest,
    current_user: UserPublic = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    cryptography: CryptographyService = Depends(get_cryptography_service),
    cache_store: CacheStore = Depends(get_cache_store),
):
    """
    Update users email

    **Must call auth/email-verification/credentials before calling this endpoint**

    ### Args: 
        - **newEmail**: the email that verification was sent to in verification request
        - **verificationCode**: Code from verification email
    ### Returns:
        - **200**: UserPublic schema

    ### Raises:
    - **401 UNAUTHORIZED**: if code exipred or invalid, or user has reached max attempts
    - **404 NOT FOUND**: user is not found in db
    """
    return await update_email(
        db=db,
        user_id=current_user.user_id,
        cryptography=cryptography,
        cache_store=cache_store,
        get_user_by_id=get_by_id,
        update_user=update_by_id,
        data_in=data
    )


@router.patch("/password", status_code=200, response_model=UserPublic)
async def auth_update_password(
    data: UpdatePasswordRequest,
    db: AsyncSession = Depends(get_db_session),
    user: UserPublic = Depends(get_current_user),
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    return await update_password_with_current_password(
        db=db,
        user_id=user.user_id,
        cryptography=cryptography,
        get_user_by_id=get_by_id,
        update_user=update_by_id,
        data_in=data
    )


@router.patch("/recovery/password", status_code=200)
async def auth_update_password_with_verification_code(
    data: UpdatePasswordWithVerificationCodeRequest,
    db: AsyncSession = Depends(get_db_session),
    cache_store: CacheStore = Depends(get_cache_store),
    cryptography: CryptographyService = Depends(get_cryptography_service)
):
    await update_password_with_verification_code(
        db=db,
        cache_store=cache_store,
        cryptography=cryptography,
        data_in=data,
        get_user_by_email_hash=get_by_email_hash,
        update_user=update_by_id
    )

    return {"detail": [{"msg": "Password reset"}]}