from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Guest(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "guests"

    name: Mapped[str | None] = mapped_column(String(255))
    room_number: Mapped[str | None] = mapped_column(String(20))

    conversations = relationship("Conversation", back_populates="guest")
