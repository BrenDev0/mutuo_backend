from dataclasses import asdict
from .models import UserRow
from ..models import User, UserPartial

def row_to_domain(row: UserRow) -> User:
    return User(
        user_id=row.user_id,
        name=row.name,
        email=row.email,
        email_hash=row.email_hash,
        password=row.password,
        profile_type=row.profile_type,
        created_at=row.created_at
    )


def domain_partial_to_row(partial: UserPartial) -> UserRow:
    return UserRow(
        **asdict(partial)
    )


