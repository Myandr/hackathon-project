"""Abstrakte Basis für alle AI-Provider – einheitliche Schnittstelle."""

from abc import ABC, abstractmethod

from app.schemas import ChatMessage, ChatResponse


class BaseAIProvider(ABC):
    """Gemeinsames Interface: Modell wechseln = nur Config/Parameter ändern."""

    provider_name: str

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        """Chat-Completion ausführen. Gibt einheitliche ChatResponse zurück."""
        ...
