import uuid
from datetime import datetime

from pydantic import BaseModel


class VoiceNoteCreate(BaseModel):
    guest_name: str
    message: str


class VoiceNoteRead(BaseModel):
    id: uuid.UUID
    guest_name: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}
