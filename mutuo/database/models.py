from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped

from pydantic import BaseModel

from mutuo.utils import utc_now

class Base(DeclarativeBase):
    pass

class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class Pagation(BaseModel):
    items_per_page: int
    page_number: int