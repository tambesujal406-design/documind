"""DocuMind backend entry point.

Run it from the backend folder with:
    python -m uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="DocuMind API",
    description="Backend for DocuMind: understand documents, discover intelligence.",
    version="0.1.0",
)

# A browser lets a web page read this API's responses only if the API names the
# page's origin as allowed (CORS). The list comes from configuration, so
# production can use the real frontend address without a code change (TD-014).
# Cookies are not enabled; Phase 9 decides how login works across domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Report that the API is running."""
    return {"status": "ok", "service": "documind-api"}