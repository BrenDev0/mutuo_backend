import asyncio
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.utils import utc_now
from mutuo.settings import settings
from mutuo.exceptions import UnauthorizedException, ConflictException, NotfoundException, UnprocessableException
from mutuo.security.types import DeterministicHashFn, CompareHashFn,  DecryptFn, HashFn, EncryptFn
from mutuo.cache.protocols import CacheStore

from mutuo.users.schemas import UserPublic
from mutuo.users.models import User
from mutuo.users.types import GetByEmailHashFn, UpdateUserFn, CreateUserFn
from mutuo.users.transformers import to_user_public
from mutuo.communications.types import SendEmailFn, CreateVerificationEmailFn

from .schemas import LoginCredentials, SessionContext, SessionSchema, UpdateCredentials, RegisterUserRequest
from .service import create_and_cache_verification_code, verify_code_or_raise, ensure_not_blocked_from_verification


async def register_user_with_verification(
    db: AsyncSession,
    user_in: RegisterUserRequest,
    encryption: EncryptFn,
    decryption: DecryptFn,
    hash: HashFn,
    deterministic_hash: DeterministicHashFn,
    cache_store: CacheStore,
    create_user: CreateUserFn
) -> UserPublic:
    
    await verify_code_or_raise(
        cache_store=cache_store,
        hashed_email=deterministic_hash(user_in.email),
        code_from_user=int(user_in.verification_code)
    )

    prepared_data = User(
        name=encryption(user_in.name),
        email= encryption(user_in.email),
        email_hash=deterministic_hash(user_in.email),
        password=hash(user_in.password),
        profile_type=user_in.profile_type
    )

    new_user = await create_user(
        db,
        prepared_data
    )


    return to_user_public(
        user=new_user,
        decryption=decryption
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
    deterministic_hash: DeterministicHashFn,
    compare_hash: CompareHashFn,
    decryption: DecryptFn,
    credentials: LoginCredentials,
    get_by_email_hash_fn: GetByEmailHashFn
) -> UserPublic:
    hashed_email = deterministic_hash(credentials.email)

    user_exists = await get_by_email_hash_fn(
        db,
        hashed_email
    )

    if not user_exists:
        raise UnauthorizedException("Incorrect email or password")
    
    password_ok = compare_hash(
        credentials.password,
        user_exists.password
    )

    if not password_ok:
        raise UnauthorizedException("Incorrect email or password")
    
    return to_user_public(user=user_exists, decryption=decryption)


async def verify_email_onboarding(
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
    
    code = await create_and_cache_verification_code(cache_store=cache_store, hashed_email=hashed_email)
    email_message = create_verification_email(code, email)

    await asyncio.to_thread(send_email, email_message)
    

async def verify_email_update_credentials(
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
    
    code = await create_and_cache_verification_code(cache_store=cache_store, hashed_email=hashed_email)
    email_message = create_verification_email(code, email)
    await asyncio.to_thread(send_email, email_message)
    

async def update_credentials_with_verification(
    db: AsyncSession,
    cache_store: CacheStore,
    changes: UpdateCredentials,
    email: str,
    code: int,
    deterministic_hash: DeterministicHashFn,
    hash: HashFn,
    encrypt: EncryptFn,
    decrypt: DecryptFn,
    get_user_by_email_hash: GetByEmailHashFn,
    update_user: UpdateUserFn
):
    hashed_email = deterministic_hash(email)
    
    await verify_code_or_raise(
        cache_store=cache_store,
        hashed_email=hashed_email,
        code_from_user=code
    )

    if not changes.password and not changes.email:
        raise UnprocessableException("At least one field required for update")

    if changes.password and changes.email:
        raise UnprocessableException("Cannot update both email and password")

    user: User | None = await get_user_by_email_hash(db, hashed_email)

    if user is None:
        raise NotfoundException("User not found")
    
    update_data = {}

    if changes.password is not None:
        update_data["password"] = hash(changes.password)

    if changes.email is not None:
        update_data["email"] = encrypt(changes.email)
        update_data["email_hash"] = deterministic_hash(changes.email)
    
    updated_user = await update_user(db, user.user_id, update_data)

    return to_user_public(user=updated_user, decryption=decrypt)
    
    



    

    

    

    
    
    
