import anthropic

from app.config import settings
from app.services.knowledge import KnowledgeService


class ChatService:
    def __init__(self, knowledge: KnowledgeService):
        self.knowledge = knowledge
        self._client: anthropic.AsyncAnthropic | None = None

    @property
    def client(self) -> anthropic.AsyncAnthropic:
        if self._client is None:
            self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        return self._client

    async def get_response(self, history: list[dict]) -> str:
        if not settings.anthropic_api_key:
            # Echo mode when no API key configured
            last = history[-1]["content"] if history else ""
            return f"[Echo] {last} (set ANTHROPIC_API_KEY for Claude responses)"

        system = self.knowledge.get_system_context()

        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system,
            messages=history,
        )

        return response.content[0].text
