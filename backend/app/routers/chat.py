import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.chat import ChatService
from app.services.knowledge import KnowledgeService

router = APIRouter()
knowledge = KnowledgeService()
chat_service = ChatService(knowledge)


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    history: list[dict] = []

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            user_text = message.get("content", "")

            history.append({"role": "user", "content": user_text})

            reply = await chat_service.get_response(history)
            history.append({"role": "assistant", "content": reply})

            await websocket.send_text(json.dumps({"role": "assistant", "content": reply}))
    except WebSocketDisconnect:
        pass
