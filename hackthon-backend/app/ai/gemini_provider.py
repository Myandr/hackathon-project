"""Google (Gemini) Provider – einheitliche Schnittstelle."""

import asyncio
from google import genai
from google.genai import types

from app.schemas import ChatMessage, ChatResponse
from app.ai.base import BaseAIProvider
from app.config import settings


class GeminiProvider(BaseAIProvider):
    provider_name = "gemini"

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._default_model = settings.gemini_model

    def _to_gemini_contents(self, messages: list[ChatMessage]) -> list[types.Content]:
        """Konvertiert einheitliche Messages in Gemini-Format (roles + parts)."""
        contents = []
        for m in messages:
            role = "user" if m.role == "user" else "model" if m.role == "assistant" else "user"
            if m.role == "system":
                role = "user"
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=m.content)])
            )
        return contents

    def _chat_sync(
        self,
        model_id: str,
        contents: list,
        temperature: float,
        max_tokens: int | None,
    ) -> str:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        resp = self._client.models.generate_content(
            model=model_id,
            contents=contents,
            config=config,
        )
        return resp.text if resp.text else ""

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        model_id = model or self._default_model
        contents = self._to_gemini_contents(messages)
        text = await asyncio.to_thread(
            self._chat_sync, model_id, contents, temperature, max_tokens
        )
        return ChatResponse(
            content=text,
            model_used=model_id,
            provider=self.provider_name,
        )
