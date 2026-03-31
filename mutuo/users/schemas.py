from uuid import UUID
from datetime import datetime
from typing import Optional

from mutuo.schemas import MutuoSchemaBase


class UserPublic(MutuoSchemaBase):
    user_id: UUID
    name: str
    email: str
    profile_type: str
    created_at: datetime
    

class UpdateUserRequest(MutuoSchemaBase):
    name: Optional[str] = None



    

