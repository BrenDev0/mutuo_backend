from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum

from mutuo.schemas import MutuoSchemaBase


class ProfileType(StrEnum):
    OWNER = "PROPIETARIO"
    RENTER = "INQUILINO"


@dataclass(frozen=True)
class SessionContext:
    ip: Optional[str] = None
    client_agent: Optional[str] = None


class VerificationCodeMixin(BaseModel):
    verification_code: int


class LoginCredentials(MutuoSchemaBase):
    email: str
    password: str


class SessionSchema(BaseModel):
    user_id: UUID
    ip: Optional[str] = None
    client_agent: Optional[str] = None
    created_at: datetime


class RegisterUserRequest(MutuoSchemaBase, VerificationCodeMixin):
    name: str
    email: str
    profile_type: ProfileType
    password: str


class VerifyEmailRequest(MutuoSchemaBase):
    email: str


class UpdateEmailRequest(MutuoSchemaBase, VerificationCodeMixin):
    new_email: str


class UpdatePasswordRequest(MutuoSchemaBase):
    new_password: str
    current_password: str


class UpdatePasswordWithVerificationCodeRequest(MutuoSchemaBase, VerificationCodeMixin):
    current_email: str
    new_password: str




