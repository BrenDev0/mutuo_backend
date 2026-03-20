from uuid import UUID
from datetime import datetime

from mutuo.schemas import MutuoSchemaBase
from enum import StrEnum

class ProfileType(StrEnum):
    OWNER = "PROPIETARIO"
    RENTER = "INQUILINO"

class UserPublic(MutuoSchemaBase):
    user_id: UUID
    name: str
    email: str
    profile_type: str
    created_at: datetime


class CreateUser(MutuoSchemaBase):
    name: str
    email: str
    profile_type: str
    password: str
    verification_code: int