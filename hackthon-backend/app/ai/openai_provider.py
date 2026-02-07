"""OpenAI (GPT) Provider – einheitliche Schnittstelle."""

from openai import AsyncOpenAI

from app.schemas import ChatMessage, ChatResponse
from app.ai.base import BaseAIProvider
from app.config import settings


class OpenAIProvider(BaseAIProvider):
    provider_name = "openai"

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._default_model = settings.openai_model

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        model_id = model or self._default_model
        openai_messages = [{"role": m.role, "content": m.content} for m in messages]
        kwargs = {
            "model": model_id,
            "messages": openai_messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        resp = await self._client.chat.completions.create(**kwargs)
        content = resp.choices[0].message.content or ""
        return ChatResponse(
            content=content,
            model_used=model_id,
            provider=self.provider_name,
        )
