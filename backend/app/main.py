"""DocuMind backend entry point.

Run it from the backend folder with:
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(
    title="DocuMind API",
    description="Backend for DocuMind: understand documents, discover intelligence.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Report that the API is running."""
    return {"status": "ok", "service": "documind-api"}