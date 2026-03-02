"""Sync local knowledge base files to ElevenLabs Conversational AI agent."""

import json
import logging
from pathlib import Path

import httpx

from app.config import settings
from app.services.knowledge import DATA_DIR

logger = logging.getLogger(__name__)

BASE_URL = "https://api.elevenlabs.io"
DOC_PREFIX = "hotel-concierge:"


class ElevenLabsKBSync:
    def __init__(self):
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers={"xi-api-key": settings.elevenlabs_api_key},
            timeout=30,
        )

    def _headers(self) -> dict:
        return {"xi-api-key": settings.elevenlabs_api_key}

    def list_existing_docs(self) -> list[dict]:
        """List KB docs with our prefix."""
        resp = self._client.get("/v1/convai/knowledge-base")
        resp.raise_for_status()
        docs = resp.json().get("documents", [])
        return [d for d in docs if d.get("name", "").startswith(DOC_PREFIX)]

    def delete_doc(self, doc_id: str) -> None:
        resp = self._client.delete(
            f"/v1/convai/knowledge-base/{doc_id}",
            params={"force": "true"},
        )
        resp.raise_for_status()

    def create_text_doc(self, name: str, text: str) -> dict:
        """Upload a text document to the KB. Returns created doc metadata."""
        resp = self._client.post(
            "/v1/convai/knowledge-base/text",
            json={"name": f"{DOC_PREFIX}{name}", "text": text},
        )
        resp.raise_for_status()
        return resp.json()

    def patch_agent_kb(self, docs: list[dict]) -> None:
        """Update agent's knowledge_base config with the given doc list."""
        agent_id = settings.elevenlabs_agent_id
        kb_entries = [
            {
                "type": "file",
                "id": d["id"],
                "name": d["name"],
                "usage_mode": settings.elevenlabs_kb_usage_mode,
            }
            for d in docs
        ]
        resp = self._client.patch(
            f"/v1/convai/agents/{agent_id}",
            json={
                "conversation_config": {
                    "agent": {
                        "prompt": {
                            "knowledge_base": kb_entries,
                        }
                    }
                }
            },
        )
        resp.raise_for_status()

    def _read_local_files(self) -> list[tuple[str, str]]:
        """Read all data files, return (filename, text_content) pairs."""
        files: list[tuple[str, str]] = []
        if not DATA_DIR.exists():
            return files
        for path in sorted(DATA_DIR.iterdir()):
            if path.suffix == ".json":
                data = json.loads(path.read_text())
                files.append((path.name, json.dumps(data, indent=2)))
            elif path.suffix == ".txt":
                files.append((path.name, path.read_text()))
        return files

    def sync(self) -> list[dict]:
        """Full sync: delete old docs, upload local files, patch agent.

        Returns list of created docs.
        """
        # 1. Delete existing prefixed docs
        existing = self.list_existing_docs()
        for doc in existing:
            logger.info("Deleting KB doc: %s", doc["name"])
            self.delete_doc(doc["id"])

        # 2. Upload local files
        local_files = self._read_local_files()
        created: list[dict] = []
        for name, text in local_files:
            logger.info("Uploading KB doc: %s%s", DOC_PREFIX, name)
            doc = self.create_text_doc(name, text)
            created.append(doc)

        # 3. Patch agent with new doc IDs
        if created:
            self.patch_agent_kb(created)
            logger.info("Patched agent with %d KB docs", len(created))

        return created
