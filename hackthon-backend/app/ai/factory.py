"""Factory: Liefert den konfigurierten AI-Provider – Modellwechsel nur über Config/Request."""

from app.config import settings
from app.ai.base import BaseAIProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.anthropic_provider import AnthropicProvider
from app.ai.gemini_provider import GeminiProvider

_PROVIDERS: dict[str, type[BaseAIProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
}

_instance: BaseAIProvider | None = None


def get_ai_provider() -> BaseAIProvider:
    """Singleton-Provider gemäß AI_PROVIDER (openai | anthropic | gemini)."""
    global _instance
    if _instance is None:
        name = settings.ai_provider.strip().lower()
        if name not in _PROVIDERS:
            raise ValueError(
                f"Unbekannter AI_PROVIDER: {name}. Erlaubt: {list(_PROVIDERS.keys())}"
            )
        _instance = _PROVIDERS[name]()
    return _instance
