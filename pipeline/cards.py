"""Centralized card loaders — SINGLE SOURCE OF TRUTH.

Every pipeline module and the API layer reads cbt_cards.jsonl and
safety_cards.jsonl through THIS module. Do not open those files directly
from anywhere else.

Design:
- Each loader is @lru_cache(maxsize=1). First call reads from disk;
  subsequent calls return the cached list/dict.
- all_cbt_cards() precomputes a `_text` field per card (title + content)
  so the retriever can use it directly without duplicating the concat.
- reset_cache() is exposed for tests that want to reload after modifying
  the underlying JSONL files.

KVKK: This module never sends anything to the network. It is a plain
disk read + in-memory cache.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Dict, List

from . import config



# CBT cards
@lru_cache(maxsize=1)
def all_cbt_cards() -> List[dict]:
    """Return the full list of CBT cards, in file order.

    Each card gets a precomputed `_text` field: title + content joined.
    Downstream consumers (retriever) rely on this field.
    """
    cards: List[dict] = []
    with open(config.CARDS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line)
            c["_text"] = f"{c['title_tr']}\n\n{c['content_tr']}"
            cards.append(c)
    return cards


@lru_cache(maxsize=1)
def cbt_cards_by_id() -> Dict[str, dict]:
    """id -> card dict."""
    return {c["id"]: c for c in all_cbt_cards()}



# Safety cards
@lru_cache(maxsize=1)
def all_safety_cards() -> List[dict]:
    cards: List[dict] = []
    with open(config.SAFETY_CARDS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cards.append(json.loads(line))
    return cards


@lru_cache(maxsize=1)
def safety_cards_by_id() -> Dict[str, dict]:
    """card_id -> safety card dict."""
    return {c["card_id"]: c for c in all_safety_cards()}


# Test helper
def reset_cache() -> None:
    """Clear all card-loader caches. Use in tests when the underlying
    JSONL is monkey-patched between runs.
    """
    all_cbt_cards.cache_clear()
    cbt_cards_by_id.cache_clear()
    all_safety_cards.cache_clear()
    safety_cards_by_id.cache_clear()
