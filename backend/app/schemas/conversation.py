import uuid
from datetime import datetime

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    guest_id: uuid.UUID


class ConversationRead(BaseModel):
    id: uuid.UUID
    guest_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
