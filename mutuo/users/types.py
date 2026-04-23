from typing import Callable, Awaitable, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

GetByEmailHashFn = Callable[[AsyncSession, str], Awaitable[User | None]]
CreateUserFn = Callable[[User], Awaitable[User]]
UpdateUserFn = Callable[[AsyncSession, UUID, dict[str, Any]], Awaitable[User]]
GetByIdFn = Callable[[AsyncSession, UUID], Awaitable[User | None]]