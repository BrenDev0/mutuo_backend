from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from mutuo.schemas import MutuoSchemaBase


@dataclass(frozen=True)
class SessionContext:
    ip: Optional[str] = None
    client_agent: Optional[str] = None



class LoginCredentials(MutuoSchemaBase):
    email: str
    password: str


class SessionSchema(BaseModel):
    user_id: UUID
    ip: Optional[str] = None
    client_agent: Optional[str] = None
    created_at: datetime


class RegisterUserRequest(MutuoSchemaBase):
    name: str
    email: str
    profile_type: str
    password: str
    verification_code: int


class VerifyEmailRequest(MutuoSchemaBase):
    email: str


class UpdateCredentials(MutuoSchemaBase):
    email: Optional[str] = None
    password: Optional[str] = None


class UpdateCredentialsRequest(MutuoSchemaBase):
    email: str
    code: int
    changes: UpdateCredentials


