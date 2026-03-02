import anthropic
import openai

from app.config import settings
from app.services.knowledge import KnowledgeService

_ANTHROPIC_DEFAULT = "claude-sonnet-4-20250514"
_OPENAI_DEFAULT = "gpt-4o"


class ChatService:
    def __init__(self, knowledge: KnowledgeService):
        self.knowledge = knowledge
        self._anthropic: anthropic.AsyncAnthropic | None = None
        self._openai: openai.AsyncOpenAI | None = None

    def _get_anthropic(self) -> anthropic.AsyncAnthropic:
        if self._anthropic is None:
            self._anthropic = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        return self._anthropic

    def _get_openai(self) -> openai.AsyncOpenAI:
        if self._openai is None:
            self._openai = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        return self._openai

    def _echo(self, history: list[dict], key_name: str) -> str:
        last = history[-1]["content"] if history else ""
        return f"[Echo] {last} (set {key_name} for AI responses)"

    async def get_response(self, history: list[dict]) -> str:
        if settings.chat_provider == "openai":
            if not settings.openai_api_key:
                return self._echo(history, "OPENAI_API_KEY")
            return await self._call_openai(history)
        else:
            if not settings.anthropic_api_key:
                return self._echo(history, "ANTHROPIC_API_KEY")
            return await self._call_anthropic(history)

    async def _call_anthropic(self, history: list[dict]) -> str:
        model = settings.chat_model or _ANTHROPIC_DEFAULT
        system = self.knowledge.get_system_context()
        response = await self._get_anthropic().messages.create(
            model=model,
            max_tokens=1024,
            system=system,
            messages=history,
        )
        return response.content[0].text

    async def _call_openai(self, history: list[dict]) -> str:
        model = settings.chat_model or _OPENAI_DEFAULT
        system = self.knowledge.get_system_context()
        messages = [{"role": "system", "content": system}] + history
        response = await self._get_openai().chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=messages,
        )
        return response.choices[0].message.content
