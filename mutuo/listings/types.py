from typing import Callable, Awaitable, Any
from uuid import UUID
from dataclasses import dataclass

from .models import Listing, ListingPartial

CreateListingFn = Callable[[ListingPartial], Awaitable[Listing]]

@dataclass(frozen=True)
class UserListingQuery:
    user_id: UUID
    offset: int
    limit: int
    filters: dict[str, Any] | None = None


GetListingsByUserIdFn = Callable[[UserListingQuery], Awaitable[list[Listing]]]