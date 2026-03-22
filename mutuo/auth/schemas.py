from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from mutuo.schemas import MutuoSchemaBase


class LoginCredentials(MutuoSchemaBase):
    email: str
    password: str


class SessionSchema(BaseModel):
    user_id: UUID
    ip: Optional[str] = None
    client_agent: Optional[str] = None
    created_at: datetime


@dataclass(frozen=True)
class SessionContext:
    ip: Optional[str] = None
    client_agent: Optional[str] = None


