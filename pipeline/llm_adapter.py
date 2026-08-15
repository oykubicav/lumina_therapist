"""LLM adapter — switchable provider behind a uniform interface.

The point: components (intent classifier, composer, critic) never import
anthropic or openai directly. They call `llm_complete(...)`. That gives us
a single chokepoint for:
  - provider switching (KVKK migration to local)
  - PII redaction
  - logging policy
  - rate-limit / retry

For Stage 2 we ship anthropic + a "mock" provider that returns canned
responses for offline tests.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable

from . import config



# PII redaction (KVKK)
# Patterns kept conservative — we'd rather over-redact than leak.
# This is a minimum, not a final list. A clinical product needs
# a proper PII engine; this is the MVP stub.
_PII_PATTERNS = [
    # Turkish T.C. ID — 11 digits, sometimes spaced
    (re.compile(r"\b\d{11}\b"), "[REDACTED_TCKN]"),
    # Phone numbers (Turkey common formats)
    (re.compile(r"\b(?:\+?90|0)?\s?\(?5\d{2}\)?\s?\d{3}\s?\d{2}\s?\d{2}\b"), "[REDACTED_PHONE]"),
    # Generic 10-15 digit numbers (potential ID/account)
    (re.compile(r"\b\d{10,15}\b"), "[REDACTED_NUM]"),
    # Email
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "[REDACTED_EMAIL]"),
    # IBAN-ish
    (re.compile(r"\bTR\d{2}\s?(?:\d{4}\s?){5}\d{2}\b", re.IGNORECASE), "[REDACTED_IBAN]"),
]


def redact_pii(text: str) -> str:
    """Run PII redaction over text. Conservative, regex-based.

    NOTE: This is a STARTING POINT. A real product needs:
      - named-entity recognition for Turkish
      - address detection
      - rare-name detection
      - context-aware health record matching
    """
    if not config.ENABLE_PII_REDACTION:
        return text
    out = text
    for pat, repl in _PII_PATTERNS:
        out = pat.sub(repl, out)
    return out



# Adapter interface
@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    latency_ms: float
    raw: Optional[Dict[str, Any]] = None


def llm_complete(
    system: str,
    user: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.2,
    redact: bool = True,
) -> LLMResponse:
    """Single-turn LLM completion.

    All component code in this pipeline calls THIS function and ONLY this
    function for LLM access. Provider can be swapped via env var
    CBT_LLM_PROVIDER without touching component code.
    """
    provider = provider or config.LLM_PROVIDER
    if redact:
        user = redact_pii(user)

    start = time.time()
    if provider == "anthropic":
        resp = _call_anthropic(system, user, model=model, max_tokens=max_tokens, temperature=temperature)
    elif provider == "openai":
        resp = _call_openai(system, user, model=model, max_tokens=max_tokens, temperature=temperature)
    elif provider == "local":
        resp = _call_local(system, user, model=model, max_tokens=max_tokens, temperature=temperature)
    elif provider == "mock":
        resp = _call_mock(system, user, model=model)
    else:
        raise ValueError(f"Unknown LLM provider: {provider!r}")
    latency = (time.time() - start) * 1000

    return LLMResponse(
        text=resp["text"],
        provider=provider,
        model=resp.get("model", model or "?"),
        latency_ms=latency,
        raw=resp.get("raw"),
    )



# Provider implementations
def _call_anthropic(system, user, *, model, max_tokens, temperature):
    """Calls Anthropic Claude. Requires ANTHROPIC_API_KEY env var.

    Lazy-imported so the pipeline can be used in mock mode without
    the anthropic package installed.
    """
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "anthropic package not installed. Run: pip install anthropic"
        ) from e

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY env var not set. Set it or switch CBT_LLM_PROVIDER=mock."
        )

    client = anthropic.Anthropic(api_key=api_key)
    model = model or config.LLM_MODEL_COMPOSER
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    return {"text": text, "model": model, "raw": resp.model_dump() if hasattr(resp, "model_dump") else None}


def _call_openai(system, user, *, model, max_tokens, temperature):
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("openai package not installed.") from e
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY env var not set.")
    client = OpenAI(api_key=api_key)
    model = model or "gpt-4o-mini"
    resp = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return {"text": resp.choices[0].message.content, "model": model}


def _call_local(system, user, *, model, max_tokens, temperature):
    """Local model via OpenAI-compatible endpoint (Ollama, vLLM, llama.cpp).

    Reads CBT_LOCAL_BASE_URL env var (default http://localhost:11434/v1).
    """
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("openai package required for local OpenAI-compatible endpoint.") from e
    base_url = os.environ.get("CBT_LOCAL_BASE_URL", "http://localhost:11434/v1")
    client = OpenAI(api_key="local", base_url=base_url)
    model = model or os.environ.get("CBT_LOCAL_MODEL", "llama3.1:8b")
    resp = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return {"text": resp.choices[0].message.content, "model": model}



# Mock provider — for offline test runs

_MOCK_HANDLERS: list[tuple[Callable[[str, str], bool], Callable[[str, str], str]]] = []


def register_mock_handler(matcher, responder):
    """Register a (matcher, responder) pair used by the mock provider.

    matcher(system, user) -> bool
    responder(system, user) -> str
    """
    _MOCK_HANDLERS.append((matcher, responder))


def _call_mock(system, user, *, model):
    for matcher, responder in _MOCK_HANDLERS:
        if matcher(system, user):
            return {"text": responder(system, user), "model": model or "mock"}
    # default mock — return a generic CBT-safe placeholder
    return {"text": "[MOCK_RESPONSE]", "model": model or "mock"}
