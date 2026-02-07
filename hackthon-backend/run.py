"""Startet den Server so, dass er im ganzen WLAN erreichbar ist (--host 0.0.0.0)."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
