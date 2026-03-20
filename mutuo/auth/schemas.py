from dataclasses import dataclass
from typing import Optional

from mutuo.schemas import MutuoSchemaBase


class LoginCredentials(MutuoSchemaBase):
    email: str
    password: str


@dataclass(frozen=True)
class SessionContext:
    ip: Optional[str] = None
    client_agent: Optional[str] = None