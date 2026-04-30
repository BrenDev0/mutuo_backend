import uuid
from sqlalchemy import String, UUID
from sqlalchemy.orm import mapped_column, Mapped

from mutuo.database.sqlalchemy.models import Base, TimeStampMixin


class UserRow(Base, TimeStampMixin):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    email_hash: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_type: Mapped[str] = mapped_column(String, nullable=False)

