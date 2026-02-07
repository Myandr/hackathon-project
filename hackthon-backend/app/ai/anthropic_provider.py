"""Anthropic (Claude) Provider – einheitliche Schnittstelle."""

import anthropic

from app.schemas import ChatMessage, ChatResponse
from app.ai.base import BaseAIProvider
from app.config import settings


class AnthropicProvider(BaseAIProvider):
    provider_name = "anthropic"

    def __init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._default_model = settings.anthropic_model

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        model_id = model or self._default_model
        system_parts = [m.content for m in messages if m.role == "system"]
        system = "\n".join(system_parts) if system_parts else ""
        chat_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role in ("user", "assistant")
        ]
        kwargs = {
            "model": model_id,
            "messages": chat_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 1024,
        }
        if system:
            kwargs["system"] = system

        resp = await self._client.messages.create(**kwargs)
        content = resp.content[0].text if resp.content else ""
        return ChatResponse(
            content=content,
            model_used=model_id,
            provider=self.provider_name,
        )
