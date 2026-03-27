import asyncio
import secrets
from mutuo.cache.protocols import CacheStore
from mutuo.exceptions import UnauthorizedException
from mutuo.settings import settings

def generate_random_code(
    len: int = 6
) -> int:
    min_value = 10 ** (len - 1)
    max_value = (10 ** len) -1

    return secrets.randbelow(max_value - min_value) + min_value


async def create_and_cache_verification_code(
    cache_store: CacheStore,
    hashed_email: str
) -> int:
    code = generate_random_code()

    verification_key = f"verification:code:{hashed_email}"
    await cache_store.set(
        key=verification_key,
        value=code,
        expire_seconds=60*15
    )

    return code

async def verify_code_or_raise(
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
    
    if code_from_user == int(verification_code):
        await asyncio.gather(
            cache_store.delete(verification_key),
            cache_store.delete(attempts_key),
            cache_store.delete(blocked_key)
        )
        return 
    
    attempts = await cache_store.increment(attempts_key)

    if attempts >= settings.MAX_VERIFICATION_ATTEMPTS:
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
