"""FastAPI-App: Ein Endpoint, alle Modelle – Modell nur in Config/Request wechseln!"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse, WordRequest, WordResponse
from app.ai.factory import get_ai_provider
from app.schemas import ChatMessage

# Temporäre Speicherung des zuletzt empfangenen Worts (vom Frontend per POST)
_stored_word: str | None = None

app = FastAPI(
    title="AI Backend",
    description="Einheitliche KI-API für OpenAI, Claude, Gemini – Modell per Config/Request wählbar.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "AI Backend",
        "docs": "/docs",
        "usage": "POST /chat mit messages + optional model/temperature/max_tokens; POST /word mit word → speichern + Satz erzeugen",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/word", response_model=WordResponse)
async def receive_word(req: WordRequest) -> WordResponse:
    """Wort vom Frontend entgegennehmen, temporär speichern und per KI einen Satz mit diesem Wort erzeugen."""
    global _stored_word
    word = req.word.strip()
    if not word:
        raise HTTPException(status_code=400, detail="word darf nicht leer sein")
    _stored_word = word

    prompt = (
        f'Erzeuge genau einen kurzen, natürlichen deutschen Satz, der das Wort "{word}" enthält. '
        "Antworte nur mit diesem einen Satz, ohne Anführungszeichen, ohne Erklärungen, ohne Punkt am Ende zu vergessen."
    )
    messages = [ChatMessage(role="user", content=prompt)]
    try:
        provider = get_ai_provider()
        response = await provider.chat(messages, temperature=0.7, max_tokens=150)
        sentence = (response.content or "").strip().strip('"')
        return WordResponse(word=word, sentence=sentence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"KI-Fehler beim Satz erzeugen: {e!s}")


@app.get("/word")
async def get_stored_word():
    """Liefert das zuletzt per POST /word gespeicherte Wort (temporär)."""
    if _stored_word is None:
        raise HTTPException(status_code=404, detail="Noch kein Wort gespeichert")
    return {"word": _stored_word}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Chat-Completion mit dem konfigurierten Provider. Optional anderes Modell in req.model."""
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages darf nicht leer sein")
    try:
        provider = get_ai_provider()
        return await provider.chat(
            req.messages,
            model=req.model,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI-Provider Fehler: {e!s}")
