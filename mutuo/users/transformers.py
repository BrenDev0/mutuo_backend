from mutuo.security.encryption import DecryptFn

from .schemas import UserPublic
from .models import User


def to_user_public(
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
