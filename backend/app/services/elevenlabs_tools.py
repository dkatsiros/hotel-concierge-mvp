"""Sync custom tools to ElevenLabs Conversational AI agent."""

import logging

import httpx

from app.config import settings
from app.tools import TOOL_PREFIX, discover_tools

logger = logging.getLogger(__name__)

BASE_URL = "https://api.elevenlabs.io"


class ElevenLabsToolSync:
    def __init__(self):
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers={"xi-api-key": settings.elevenlabs_api_key},
            timeout=30,
        )

    def list_existing_tools(self) -> list[dict]:
        """List tools with our prefix."""
        resp = self._client.get("/v1/convai/agents/tools")
        resp.raise_for_status()
        tools = resp.json().get("tools", [])
        return [t for t in tools if t.get("name", "").startswith(TOOL_PREFIX)]

    def delete_tool(self, tool_id: str) -> None:
        resp = self._client.delete(f"/v1/convai/agents/tools/{tool_id}")
        resp.raise_for_status()

    def create_tool(self, config: dict) -> dict:
        """Create a webhook tool. Returns created tool metadata."""
        tool_name = config["name"]
        webhook_url = f"{settings.webhook_base_url}/api/tools/{tool_name}"
        payload = {
            "name": config["name"],
            "description": config["description"],
            "type": "webhook",
            "webhook": {
                "url": webhook_url,
                "method": "POST",
            },
            "parameters": config["parameters"],
        }
        resp = self._client.post("/v1/convai/agents/tools", json=payload)
        resp.raise_for_status()
        return resp.json()

    def patch_agent_tools(self, tool_ids: list[str]) -> None:
        """Update agent with tool IDs."""
        agent_id = settings.elevenlabs_agent_id
        tools = [{"type": "webhook", "id": tid} for tid in tool_ids]
        resp = self._client.patch(
            f"/v1/convai/agents/{agent_id}",
            json={
                "conversation_config": {
                    "agent": {
                        "prompt": {
                            "tools": tools,
                        }
                    }
                }
            },
        )
        resp.raise_for_status()

    def sync(self) -> list[dict]:
        """Full sync: delete old tools, create from registry, patch agent."""
        # 1. Delete existing prefixed tools
        existing = self.list_existing_tools()
        for tool in existing:
            logger.info("Deleting tool: %s", tool["name"])
            self.delete_tool(tool["id"])

        # 2. Create tools from registry
        registry = discover_tools()
        created: list[dict] = []
        for name, entry in registry.items():
            logger.info("Creating tool: %s", name)
            tool = self.create_tool(entry["config"])
            created.append(tool)

        # 3. Patch agent with tool IDs
        if created:
            tool_ids = [t["id"] for t in created]
            self.patch_agent_tools(tool_ids)
            logger.info("Patched agent with %d tools", len(created))

        return created
