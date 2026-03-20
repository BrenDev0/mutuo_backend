from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Awaitable

from mutuo.security.hashing import DeterministicHashFn, HashFn, CompareHashFn
from mutuo.security.encryption import EncryptFn, DecryptFn
from mutuo.exceptions import UnauthorizedException

from .models import User
from .schemas import CreateUser, UserPublic, UserLogin

def _get_public_schema(
    user: User,
    decryption: DecryptFn
) -> UserPublic:
    return UserPublic(
        user_id=user.user_id,
        name=decryption(user.name),
        email=decryption(user.email),
        profile_type=user.profile_type,
        created_at=user.created_at
    )


CreateUserFn = Callable[[AsyncSession, User], Awaitable[User]]
GetByEmailHashFn = Callable[[AsyncSession, str], Awaitable[User | None]]

async def create_user(
    db: AsyncSession,
    user_in: CreateUser,
    encryption: EncryptFn,
    decryption: DecryptFn,
    hash: HashFn,
    deterministic_hash: DeterministicHashFn,
    create_fn: CreateUserFn
) -> UserPublic:
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


    return _get_public_schema(
        user=new_user,
        decryption=decryption
    )


async def login(
    db: AsyncSession,
    deterministic_hash: DeterministicHashFn,
    compare_hash: CompareHashFn,
    decrryption: DecryptFn,
    credencials: UserLogin,
    get_by_email_hash_fn: GetByEmailHashFn
):
    hashed_email = deterministic_hash(credencials.email)

    user_exists = await get_by_email_hash_fn(
        db,
        hashed_email
    )

    if not user_exists:
        raise UnauthorizedException("Incorrect email or password")
    
    password_ok = compare_hash(
        credencials.password,
        user_exists.password
    )

    if not password_ok:
        raise UnauthorizedException(detail="Incorrect email or password")
    
    return _get_public_schema(user=user_exists, decryption=decrryption)




    