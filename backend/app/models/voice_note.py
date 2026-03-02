from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class VoiceNote(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "voice_notes"

    guest_name: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
