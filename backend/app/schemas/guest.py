import uuid
from datetime import datetime

from pydantic import BaseModel


class GuestCreate(BaseModel):
    name: str | None = None
    room_number: str | None = None


class GuestRead(BaseModel):
    id: uuid.UUID
    name: str | None
    room_number: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
