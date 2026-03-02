import uuid
from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: uuid.UUID
    role: str
    content: str


class MessageRead(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
