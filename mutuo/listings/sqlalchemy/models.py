import uuid
from sqlalchemy import String, ForeignKey, Integer, Float
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID

from mutuo.database.sqlalchemy.models import Base, TimeStampMixin

class ListingRow(Base, TimeStampMixin):
    __tablename__ = "listings"

    listing_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String, nullable=False)
    beds: Mapped[int] = mapped_column(Integer, default=0)
    baths: Mapped[float] = mapped_column(Float(1), default=0.0)
    price: Mapped[float] = mapped_column(Float(2), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)


