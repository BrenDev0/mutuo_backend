import asyncio
from typing import Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.settings import settings
from mutuo.security.types import EncryptFn, DecryptFn, DeterministicHashFn, HashFn
from mutuo.exceptions import UnauthorizedException
from mutuo.cache.protocols import CacheStore

from .models import User
from .schemas import CreateUser, UserPublic
from .transformers import to_user_public


CreateUserFn = Callable[[AsyncSession, User], Awaitable[User]]


async def _handle_verification(
    cache_store: CacheStore,
    hashed_email: str,
    code_from_user: int
):
    verification_key = f"verification:code:{hashed_email}"
    attempts_key = f"verification:attempts:{hashed_email}"
    blocked_key = f"verification:blocked:{hashed_email}"

    user_is_blocked = await cache_store.get(blocked_key)
    if user_is_blocked:
        raise UnauthorizedException("Max verification attempts reached")

    verification_code = await cache_store.get(
        key=verification_key
    )
    if verification_code is None:
        raise UnauthorizedException("Invalid or expired verification code")
    
    if int(code_from_user) == int(verification_code):
        await asyncio.gather(
            cache_store.delete(verification_key),
            cache_store.delete(attempts_key),
            cache_store.delete(blocked_key)
        )
        return 
    
    attemps = await cache_store.increment(attempts_key)

    if attemps >= settings.MAX_VERIFICATION_ATTEMPTS:
        await asyncio.gather(
            cache_store.delete(verification_key),
            cache_store.delete(attempts_key),
            cache_store.set(
                key=blocked_key,
                value=1,
                expire_seconds=60 * 10 #10 mins
            )
        )

    raise UnauthorizedException()


async def create_user(
    db: AsyncSession,
    user_in: CreateUser,
    encryption: EncryptFn,
    decryption: DecryptFn,
    hash: HashFn,
    deterministic_hash: DeterministicHashFn,
    cache_store: CacheStore,
    create_fn: CreateUserFn
) -> UserPublic:
    
    await _handle_verification(
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

    new_user = await create_fn(
        db,
        prepared_data
    )


    return to_user_public(
        user=new_user,
        decryption=decryption
    )





    