import asyncio
from email.message import EmailMessage
from pathlib import Path
from typing import Callable, Awaitable
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.utils import utc_now
from mutuo.settings import settings
from mutuo.exceptions import UnauthorizedException, ConflictException
from mutuo.security.types import DeterministicHashFn, CompareHashFn,  DecryptFn
from mutuo.cache.protocols import CacheStore

from mutuo.users.models import User
from mutuo.users.schemas import UserPublic
from mutuo.users.transformers import to_user_public
from mutuo.communications.types import SendEmailFn

from .schemas import LoginCredentials, SessionContext, SessionSchema
from .utils import generate_random_code


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
) -> UUID:
    await asyncio.gather(
        cache_store.delete(str(session_id)),
        cache_store.delete(f"cache:user{user_id}")
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
        raise UnauthorizedException(detail="Incorrect email or password")
    
    return to_user_public(user=user_exists, decryption=decryption)


async def verify_email(
    db: AsyncSession,
    cache_store: CacheStore,
    email: str,
    deterministic_hash: DeterministicHashFn,
    get_user_by_email_hash: GetByEmailHashFn,
    send_email: SendEmailFn
):
    
    hashed_email = deterministic_hash(email)
    
    blocked_key = f"verification:blocked:{hashed_email}"
    user_is_blocked = await cache_store.get(blocked_key)
    if user_is_blocked:
        raise UnauthorizedException("Max verification attempts reached")


    email_in_use = await get_user_by_email_hash(db, hashed_email)

    if email_in_use:
        raise ConflictException("Email in use")
    
    code = generate_random_code()

    template_path = Path(__file__).parent.parent/"communications"/"templates"/"verify_email.html"

    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()

    email_body = template.replace('{{verification_code}}', str(code))
    
    email_message = EmailMessage()
    email_message["From"] = settings.MAILER_USER
    email_message["To"] = email
    email_message["Subject"] = "Verificar Correo Electrónico"
    email_message.set_content(email_body, subtype="html")

    verification_key = f"verification:code:{hashed_email}"
    await cache_store.set(
        key=verification_key,
        value=code,
        expire_seconds=60*15
    )

    send_email(
        email_message=email_message
    )



    

    

    

    
    
    
