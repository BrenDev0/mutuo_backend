from typing import Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Listing

CreateListingFn = Callable[[AsyncSession, Listing], Awaitable[Listing]]