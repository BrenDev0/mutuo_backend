from sqlalchemy.ext.asyncio import AsyncSession

from mutuo.security.hashing import DeterministicHashFn, HashFn, CompareHashFn
from mutuo.security.encryption import EncryptFn, DecryptFn

from .models import User
from .service import create, get_by_email_hash
from .schemas import CreateUser, UserPublic, UserLogin

def get_public_schema(
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

async def create_user(
    db: AsyncSession,
    user_in: CreateUser,
    encryption: EncryptFn,
    decryption: DecryptFn,
    hash: HashFn,
    deterministic_hash: DeterministicHashFn
) -> UserPublic:
    prepared_data = User(
        name=encryption(user_in.name),
        email= encryption(user_in.email),
        email_hash=deterministic_hash(user_in.email),
        password=hash(user_in.password),
        profile_type=user_in.profile_type
    )

    new_user = await create(
        db=db,
        user_in=prepared_data
    )


    return get_public_schema(
        user=new_user,
        decryption=decryption
    )

async def login(
    db: AsyncSession,
    deterministic_hash: DeterministicHashFn,
    compare_hash: CompareHashFn,
    credencials: UserLogin
):
    hashed_email = deterministic_hash(credencials.email)

    user_exists = await get_by_email_hash(
        db=db,
        email_hash=hashed_email
    )

    if not user_exists:
        raise FileNotFoundError("User not found")
    