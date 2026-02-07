"""FastAPI-App: Ein Endpoint, alle Modelle – Modell nur in Config/Request wechseln!"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse
from app.ai.factory import get_ai_provider

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
        "usage": "POST /chat mit messages + optional model/temperature/max_tokens",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


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
