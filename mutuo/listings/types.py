from typing import Callable, Awaitable
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Listing

CreateListingFn = Callable[[AsyncSession, Listing], Awaitable[Listing]]
GetByUserIdFn = Callable[[AsyncSession, UUID, int, int, dict], Awaitable[list[Listing]]]