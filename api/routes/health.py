# api/routes/health.py
"""Health + readiness endpoints.

  GET /health   → liveness (always fast, no work)
  GET /readyz   → readiness (validates card/rule loading + API key presence)
"""

import os
import logging
from fastapi import APIRouter

from api.schemas import HealthResponse, ReadyzResponse
from api import __version__

router = APIRouter(tags=["health"])
log = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(ok=True, version=__version__)


@router.get("/readyz", response_model=ReadyzResponse)
async def readyz():
    checks = {}
    details = {}

    # Cards & rules
    try:
        from pipeline import cards
        cbt_n = len(cards.all_cbt_cards())
        sf_n = len(cards.all_safety_cards())
        checks["cbt_cards"] = cbt_n > 0
        checks["safety_cards"] = sf_n > 0
        details["cbt_cards"] = f"{cbt_n} loaded"
        details["safety_cards"] = f"{sf_n} loaded"
    except Exception as e:
        checks["cbt_cards"] = False
        checks["safety_cards"] = False
        details["cbt_cards"] = f"error: {type(e).__name__}: {e}"

    try:
        from pipeline import safety_rules
        _ = safety_rules._load_rules()
        checks["safety_rules"] = True
    except Exception as e:
        checks["safety_rules"] = False
        details["safety_rules"] = f"error: {e}"

    # LLM provider
    from pipeline import config as pcfg
    provider = pcfg.LLM_PROVIDER
    if provider == "anthropic":
        checks["llm_api_key"] = bool(os.environ.get("ANTHROPIC_API_KEY"))
        details["llm_provider"] = "anthropic"
        if not checks["llm_api_key"]:
            details["llm_api_key"] = "ANTHROPIC_API_KEY missing"
    elif provider == "mock":
        checks["llm_api_key"] = True
        details["llm_provider"] = "mock"
    else:
        checks["llm_api_key"] = True  # unknown provider — trust config
        details["llm_provider"] = provider

    # Embedding backend
    try:
        from pipeline import embedding_backend
        backend = embedding_backend.get_backend()
        checks["embedding_backend"] = True
        details["embedding_backend"] = backend.name
    except Exception as e:
        checks["embedding_backend"] = False
        details["embedding_backend"] = f"error: {e}"

    ok = all(checks.values())
    return ReadyzResponse(ok=ok, checks=checks, details=details)