import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Conversation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    guest_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("guests.id")
    )

    guest = relationship("Guest", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
