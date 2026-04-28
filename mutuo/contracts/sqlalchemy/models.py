import uuid
from datetime import datetime

from sqlalchemy import UUID, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from mutuo.database.sqlalchemy.models import Base, TimeStampMixin


class ContractRow(Base, TimeStampMixin):
    __tablename__ = "contracts"

    contract_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Mapped[str] = mapped_column(String, nullable=False)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("listings.listing_id", ondelete="CASCADE"), nullable=False)
    expiration: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)