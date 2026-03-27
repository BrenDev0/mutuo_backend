from typing import Callable, Awaitable, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

GetByEmailHashFn = Callable[[AsyncSession, str], Awaitable[User | None]]
CreateUserFn = Callable[[AsyncSession, User], Awaitable[User]]
UpdateUserFn = Callable[[AsyncSession, UUID, Dict[str, Any]], Awaitable[User]]
GetByIdFn = Callable[[AsyncSession, UUID], Awaitable[User]]