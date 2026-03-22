import asyncio
from typing import Callable, Awaitable
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.utils import utc_now
from mutuo.settings import settings
from mutuo.exceptions import UnauthorizedException
from mutuo.security.hashing import DeterministicHashFn, CompareHashFn
from mutuo.security.encryption import DecryptFn
from mutuo.cache.protocols import CacheStore

from mutuo.users.models import User
from mutuo.users.schemas import UserPublic
from mutuo.users.transformers import to_user_public

from .schemas import LoginCredentials, SessionContext, SessionSchema


GetByEmailHashFn = Callable[[AsyncSession, str], Awaitable[User | None]]

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

    user_cahe = user.model_dump(mode="json")

    await asyncio.gather(
        cache_store.set(
            key=f"{str(session_id)}",
            value=session_cache.model_dump(mode="json"),
            expire_seconds=settings.SESSION_MAX_AGE
        ),
        cache_store.set(
            key=f"user:cache:{user.user_id}",
            value=user_cahe,
            expire_seconds=settings.USER_CACHE_MAX_AGE
        )
    )

    return session_id

async def delete_session(
    cache_store: CacheStore,
    session_id: UUID,
    user_id: UUID
):
    await asyncio.gather(
        cache_store.delete(str(session_id)),
        cache_store.delete(f"cache:user{user_id}")
    )



async def login(
    db: AsyncSession,
    deterministic_hash: DeterministicHashFn,
    compare_hash: CompareHashFn,
    decryption: DecryptFn,
    credentials: LoginCredentials,
    get_by_email_hash_fn: GetByEmailHashFn
):
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
        raise UnauthorizedException(detail="Incorrect email or password")
    
    return to_user_public(user=user_exists, decryption=decryption)