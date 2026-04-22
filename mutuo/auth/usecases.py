import asyncio
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.utils import utc_now
from mutuo.settings import settings
from mutuo.exceptions import UnauthorizedException, ConflictException, NotfoundException, UnprocessableException
from mutuo.security.protocols import CryptographyService
from mutuo.security.types import DeterministicHashFn
from mutuo.cache.protocols import CacheStore

from mutuo.users.schemas import UserPublic
from mutuo.users.models import User
from mutuo.users.types import GetByEmailHashFn, UpdateUserFn, CreateUserFn, GetByIdFn
from mutuo.users.mappers import to_user_public
from mutuo.communications.types import SendEmailFn, CreateVerificationEmailFn

from .schemas import (
    LoginCredentials, 
    SessionContext, 
    SessionSchema, 
    UpdateEmailRequest, 
    UpdatePasswordRequest, 
    UpdatePasswordWithVerificationCodeRequest, 
    RegisterUserRequest
)
from .service import create_and_cache_verification_code, verify_code_or_raise, ensure_not_blocked_from_verification


async def _create_and_send_verification_email(
    cache_store: CacheStore,
    create_verification_email: CreateVerificationEmailFn, 
    send_email: SendEmailFn,
    hashed_email: str, 
    unhashed_email: str
):
    code = await create_and_cache_verification_code(cache_store=cache_store, hashed_email=hashed_email)
    email_message = create_verification_email(code, unhashed_email)

    await asyncio.to_thread(send_email, email_message)


async def register_user_with_verification(
    db: AsyncSession,
    user_in: RegisterUserRequest,
    cryptography: CryptographyService,
    cache_store: CacheStore,
    create_user: CreateUserFn
) -> UserPublic:
    
    await verify_code_or_raise(
        cache_store=cache_store,
        hashed_email=cryptography.deterministic_hash(user_in.email),
        code_from_user=int(user_in.verification_code)
    )

    prepared_data = User(
        name=cryptography.encrypt(user_in.name),
        email=cryptography.encrypt(user_in.email),
        email_hash=cryptography.deterministic_hash(user_in.email),
        password=cryptography.hash(user_in.password),
        profile_type=user_in.profile_type
    )

    new_user = await create_user(
        db,
        prepared_data
    )


    return to_user_public(
        user=new_user,
        decryption=cryptography.decrypt
    )


async def create_session(
    session_context: SessionContext,
    cache_store: CacheStore,
    user: UserPublic
) -> UUID:
    session_id = uuid4()

    session_cache = SessionSchema(
        user_id=user.user_id,
        ip=session_context.ip,
        client_agent=session_context.client_agent,
        created_at=utc_now()
    )

    user_cache = user.model_dump(mode="json")

    await asyncio.gather(
        cache_store.set(
            key=f"session:{session_id}",
            value=session_cache.model_dump(mode="json"),
            expire_seconds=settings.SESSION_MAX_AGE
        ),
        cache_store.set(
            key=f"user:cache:{user.user_id}",
            value=user_cache,
            expire_seconds=settings.USER_CACHE_MAX_AGE
        )
    )

    return session_id


async def delete_session(
    cache_store: CacheStore,
    session_id: UUID,
    user_id: UUID
) -> UUID:
    await asyncio.gather(
        cache_store.delete(f"session:{session_id}"),
        cache_store.delete(f"user:cache:{user_id}")
    )

    return session_id


async def login(
    db: AsyncSession,
    cryptography: CryptographyService,
    credentials: LoginCredentials,
    get_user_by_email_hash: GetByEmailHashFn
) -> UserPublic:
    hashed_email = cryptography.deterministic_hash(credentials.email)

    user_exists = await get_user_by_email_hash(
        db,
        hashed_email
    )

    if not user_exists:
        raise UnauthorizedException("Incorrect email or password")
    
    password_ok = cryptography.compare_hash(
        credentials.password,
        user_exists.password
    )

    if not password_ok:
        raise UnauthorizedException("Incorrect email or password")
    
    return to_user_public(user=user_exists, decryption=cryptography.decrypt)


async def request_onboarding_email_verification(
    db: AsyncSession,
    cache_store: CacheStore,
    email: str,
    deterministic_hash: DeterministicHashFn,
    get_user_by_email_hash: GetByEmailHashFn,
    create_verification_email: CreateVerificationEmailFn, 
    send_email: SendEmailFn,
):
    
    hashed_email = deterministic_hash(email)
    
    await ensure_not_blocked_from_verification(hashed_email=hashed_email, cache_store=cache_store)

    email_in_use = await get_user_by_email_hash(db, hashed_email)

    if email_in_use:
        raise ConflictException("Email in use")
    
    await _create_and_send_verification_email(
        cache_store=cache_store,
        create_verification_email=create_verification_email,
        send_email=send_email,
        hashed_email=hashed_email,
        unhashed_email=email
    )
    

async def request_update_credentials_email_verification(
    db: AsyncSession,
    cache_store: CacheStore,
    email: str,
    deterministic_hash: DeterministicHashFn,
    get_user_by_email_hash: GetByEmailHashFn,
    create_verification_email: CreateVerificationEmailFn,
    send_email: SendEmailFn,
):
    
    hashed_email = deterministic_hash(email)

    await ensure_not_blocked_from_verification(hashed_email=hashed_email, cache_store=cache_store)

    user = await get_user_by_email_hash(db, hashed_email)
    if user is None:
        raise NotfoundException(detail="User not found")
    
    await _create_and_send_verification_email(
        cache_store=cache_store,
        create_verification_email=create_verification_email,
        send_email=send_email,
        hashed_email=hashed_email,
        unhashed_email=email
    )
    

async def update_email(
    db: AsyncSession,
    user_id: UUID,
    cryptography: CryptographyService,
    cache_store: CacheStore,
    get_user_by_id: GetByIdFn,
    update_user: UpdateUserFn,
    data_in: UpdateEmailRequest
):
    new_email_hash = cryptography.deterministic_hash(data_in.new_email)

    await verify_code_or_raise(
        cache_store=cache_store,
        hashed_email=new_email_hash,
        code_from_user=data_in.verification_code
    )

    user: User | None = await get_user_by_id(db, user_id)
    if user is None:
        raise NotfoundException("User not found")
    
    
    new_email_encrypted = cryptography.encrypt(data_in.new_email)
    
    update_data = {
        "email": new_email_encrypted,
        "email_hash": new_email_hash 
    }

    updated_user = await update_user(db, user.user_id, update_data)

    return to_user_public(updated_user, cryptography.decrypt)


async def update_password_with_verification_code(
    db: AsyncSession,
    cache_store: CacheStore,
    cryptography: CryptographyService,
    data_in: UpdatePasswordWithVerificationCodeRequest,
    get_user_by_email_hash: GetByEmailHashFn,
    update_user: UpdateUserFn
):
    email_hash = cryptography.deterministic_hash(data_in.current_email)

    await verify_code_or_raise(
        cache_store=cache_store,
        hashed_email=email_hash,
        code_from_user=data_in.verification_code
    )

    user: User | None = await get_user_by_email_hash(db, email_hash)

    if not user:
        raise NotfoundException("User not found")
    
    if cryptography.compare_hash(data_in.new_password, user.password):
        raise UnprocessableException("New password cannot be same as old password")
    
    new_password_hash = cryptography.hash(data_in.new_password)
    update_data = {
        "password": new_password_hash
    }

    await update_user(db, user.user_id, update_data)


async def update_password_with_current_password(
    db: AsyncSession,
    user_id: UUID,
    cryptography: CryptographyService,
    get_user_by_id: GetByIdFn,
    update_user: UpdateUserFn,
    data_in: UpdatePasswordRequest
    
):
    user: User | None = await get_user_by_id(db, user_id)

    if user is None:
        raise NotfoundException("User not found")
    
    if not cryptography.compare_hash(data_in.current_password, user.password):
        raise UnauthorizedException("Incorrect password")
    
    if cryptography.compare_hash(data_in.new_password, user.password):
        raise UnprocessableException("New password cannot be same as current password")
    
    new_password_hash = cryptography.hash(data_in.new_password)

    update_data = {
        "password": new_password_hash
    }

    updated_user = await update_user(db, user.user_id, update_data)

    return to_user_public(updated_user, cryptography.decrypt)


    

    

    

    
    
    
