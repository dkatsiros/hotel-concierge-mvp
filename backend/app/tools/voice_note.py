"""Tool: save a voice note from a guest for the front desk."""

from app.database import async_session
from app.models.voice_note import VoiceNote

TOOL_CONFIG = {
    "name": "hotel-concierge:voice_note",
    "description": "Save a voice note from a guest for the front desk",
    "parameters": {
        "type": "object",
        "properties": {
            "guest_name": {
                "type": "string",
                "description": "Name of the guest leaving the note",
            },
            "message": {
                "type": "string",
                "description": "The message content for the front desk",
            },
        },
        "required": ["guest_name", "message"],
    },
}


async def handler(params: dict) -> dict:
    """Save voice note to DB."""
    async with async_session() as session:
        note = VoiceNote(
            guest_name=params["guest_name"],
            message=params["message"],
        )
        session.add(note)
        await session.commit()
    return {"status": "ok", "message": "Voice note saved for the front desk"}
