# AI Backend (FastAPI)

Schnelles Setup für ein KI-Backend mit **einheitlicher API** für mehrere Modelle. Du wechselst nur das Modell (per Env oder Request), der Rest bleibt gleich.

## Unterstützte Provider

| Provider | Env-Wert   | Beispiele Modelle        |
|----------|------------|---------------------------|
| OpenAI   | `openai`   | gpt-4o, gpt-4o-mini       |
| Anthropic| `anthropic`| claude-3-5-sonnet, claude-3-haiku |
| Google   | `gemini`   | gemini-2.0-flash, gemini-1.5-pro |

## Setup

```bash
# Virtuelle Umgebung (empfohlen)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Abhängigkeiten
pip install -r requirements.txt

# Konfiguration
cp .env.example .env
# In .env: AI_PROVIDER setzen und den passenden API-Key eintragen
```

## Start

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000  
- Docs: http://127.0.0.1:8000/docs  

## Modell wechseln

**1. Global (für alle Requests):** In `.env` z.B. `AI_PROVIDER=gemini` und den zugehörigen API-Key setzen.

**2. Pro Request:** `POST /chat` mit Body z.B.:

```json
{
  "messages": [
    { "role": "user", "content": "Hallo, was ist 2+2?" }
  ],
  "model": "gpt-4o",
  "temperature": 0.7,
  "max_tokens": 500
}
```

`model` ist optional – wenn weggelassen, wird das Default-Modell des gewählten Providers genutzt (siehe `.env`).

## Beispiel-Curl

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Sag Hallo auf Deutsch."}]}'
```

Antwort (einheitlich für alle Provider):

```json
{
  "content": "Hallo! ...",
  "model_used": "gpt-4o-mini",
  "provider": "openai"
}
```

## Wort → Satz (Frontend-API)

Ein Wort per POST schicken → wird temporär gespeichert → die KI erzeugt einen Satz mit diesem Wort.

**Beispiel curl:**

```bash
curl -X POST http://127.0.0.1:8000/word \
  -H "Content-Type: application/json" \
  -d '{"word": "Haus"}'
```

Antwort:

```json
{
  "word": "Haus",
  "sentence": "Das Haus steht am Ende der Straße."
}
```

Das zuletzt gespeicherte Wort abrufen: `GET http://127.0.0.1:8000/word`

## Projektstruktur

```
app/
  main.py         # FastAPI-App, /chat + /word
  config.py       # Settings aus .env
  schemas.py      # ChatRequest, ChatResponse
  ai/
    base.py       # Abstraktes Provider-Interface
    openai_provider.py
    anthropic_provider.py
    gemini_provider.py
    factory.py    # Liefert Provider nach AI_PROVIDER
```

Neue Provider: Klasse von `BaseAIProvider` ableiten, in `factory.py` eintragen, fertig.




curl -X 'POST' \
  'http://127.0.0.1:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "assistant",
      "content": "test message for you to answer"
    }
  ],
  "model": "gemini-2.0-flash",
  "temperature": 0.7,
  "max_tokens": 100
}'





curl -X 'POST' \
  'http://127.0.0.1:8000/word' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "word": "string"
}'


172.22.13.251