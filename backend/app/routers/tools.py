import logging

from fastapi import APIRouter, HTTPException, Request

from app.tools import get_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tools"])


@router.post("/tools/{tool_name}")
async def handle_tool(tool_name: str, request: Request):
    handler = get_handler(tool_name)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_name}")

    body = await request.json()
    logger.info("Tool call: %s params=%s", tool_name, body)
    result = await handler(body)
    return result
