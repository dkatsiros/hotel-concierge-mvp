import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Message(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id")
    )
    role: Mapped[str] = mapped_column(String(20))  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text)

    conversation = relationship("Conversation", back_populates="messages")
