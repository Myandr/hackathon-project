"""Einheitliche Request/Response-Schemas für alle AI-Provider."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Eine Nachricht im Chat (einheitlich für alle Modelle)."""
    role: str = Field(..., description="user | assistant | system")
    content: str = Field(..., description="Text der Nachricht")


class ChatRequest(BaseModel):
    """Anfrage an den Chat-Endpoint."""
    messages: list[ChatMessage] = Field(..., description="Konversationsverlauf")
    model: str | None = Field(
        default=None,
        description="Optional: Modell-Override (z.B. gpt-4o, claude-3-5-sonnet, gemini-2.0-flash). Lässt man weg, wird das konfigurierte Default genutzt."
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, description="Max. Tokens in der Antwort")


class ChatResponse(BaseModel):
    """Antwort des gewählten Modells."""
    content: str = Field(..., description="Antworttext")
    model_used: str = Field(..., description="Tatsächlich genutztes Modell")
    provider: str = Field(..., description="openai | anthropic | gemini")
