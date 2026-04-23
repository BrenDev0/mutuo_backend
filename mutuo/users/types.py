from typing import Callable, Awaitable, Any
from uuid import UUID

from .models import User, UserPartial

GetByEmailHashFn = Callable[[str], Awaitable[User | None]]
CreateUserFn = Callable[[UserPartial], Awaitable[User]]
UpdateUserFn = Callable[[UUID, dict[str, Any]], Awaitable[User]]
GetByIdFn = Callable[[UUID], Awaitable[User | None]]
DeleteByIdFn = Callable[[UUID], Awaitable[User | None]]