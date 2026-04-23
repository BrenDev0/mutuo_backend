from uuid import UUID
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    user_id: UUID
    name: str
    email: str
    email_hash: str
    password: str
    profile_type: str
    created_at: datetime


@dataclass(frozen=True)
class UserPartial:
    name: str
    email: str
    email_hash: str
    password: str
    profile_type: str


