"""Safety classifier — 3 layer.

  Layer 1  hard_rule          — high-precision multi-word phrases (exact match)
  Layer 2  concept_rule       — feature-group combination rules (anatomy + symptom)
  Layer 3  embedding_fallback — semantic similarity vs concept anchor examples

Order: Layer 1 → Layer 2 → Layer 3. We collect all matches across layers
and combine them into a SafetyDecision.

This module reports `match_method` per match so eval_runner can split
recall by layer.

NOTE: For Layer 3 we use embedding_backend which auto-selects
sentence-transformers if installed, TF-IDF char-ngram otherwise.
Either way it stays fully local — no external API.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Optional, Tuple

from . import config
from . import safety_rules
from . import embedding_backend
from .types import SafetyMatch, SafetyDecision

# Tunable thresholds — per backend
# Cosine skalası TF-IDF ve sentence-transformers arasında ciddi farklı davranır.
# TF-IDF char-ngram tipik olarak 0.3-0.6 aralığında (yüksek benzerlik ~0.55+).
# Sentence-transformers multilingual MiniLM 0.2-0.9 arasında oynar; ilgisiz
# cümleler bile 0.4-0.5 verebilir, gerçek anlam yakınlığı 0.7+ gerekir.
# Bu yüzden threshold'u backend adına göre seçiyoruz.

LAYER3_THRESHOLDS = {
    "sentence-transformers": {"high": 0.72, "gray": 0.60},
    "tfidf-char-ngram":      {"high": 0.55, "gray": 0.42},
}
LAYER3_DEFAULT = {"high": 0.55, "gray": 0.42}


def _thresholds_for(backend_name: str) -> dict:
    return LAYER3_THRESHOLDS.get(backend_name, LAYER3_DEFAULT)


# Backwards-compat symbols (some tests / debug code may reference these)
LAYER3_HIGH_CONFIDENCE = LAYER3_DEFAULT["high"]
LAYER3_GRAY_BAND = LAYER3_DEFAULT["gray"]


# Concept anchor index for Layer 3
# belirli kavramları ("concept") temsil eden örnek metinleri ("anchors") almak, 
# bu metinleri matematiksel vektörlere dönüştürmek ve bu işlemin sonucunu bellekte tutarak (cache) uygulamanın hızını artırmaktır.
@lru_cache(maxsize=1)
def _build_anchor_index():
    """Build a fitted backend + matrix for concept anchor examples.

    Returns: (backend, matrix, concept_ids_per_row)
    """
    pairs = safety_rules.list_concept_anchors()
    rows: List[str] = []
    concept_for_row: List[str] = []
    for cid, anchors in pairs:
        for a in anchors:
            rows.append(a)
            concept_for_row.append(cid)
    backend = embedding_backend.get_backend(prefer_st=True)
    backend.fit(rows)  # for TF-IDF; no-op for ST
    matrix = backend.encode(rows)
    return backend, matrix, concept_for_row



# Public API

def classify(user_message: str, enable_layer3: bool = True) -> SafetyDecision:
    """Run the 3-layer classifier and return an aggregated SafetyDecision.

    Each SafetyMatch carries:
      - card_id, risk_level, route, allow_cbt, blocks_exercise
      - matched_signals          (group names / rule ids / anchor concept ids)
      - match_strength           (0..1)

    We also stash debugging info: matched_concepts, matched_rules, match_method.
    """
    matches: List[SafetyMatch] = []
    concept_decisions = {}     # concept_id -> (risk_level, target_card_ids, method, confidence)

    # ---------- Layer 1: hard rules ----------
    hard_hits = safety_rules.match_hard_rules(user_message)
    for h in hard_hits:
        cards = safety_rules.concept_to_target_cards(h.concept)
        risk = safety_rules.concept_to_risk_level(h.concept)
        if h.concept not in concept_decisions:
            concept_decisions[h.concept] = (risk, cards, "hard_rule", 1.0)

    # ---------- Layer 2: concept rules ----------
    concept_hits, group_hits = safety_rules.match_concept_rules(user_message)
    for c in concept_hits:
        if c.concept_id not in concept_decisions:
            concept_decisions[c.concept_id] = (c.risk_level, c.target_card_ids, "concept_rule", c.confidence)

    # ---------- Layer 3: embedding fallback ----------
    layer3_hits = []
    if enable_layer3 and len(concept_decisions) == 0:
        layer3_hits = _layer3_match(user_message)
        for cid, score in layer3_hits:
            if cid not in concept_decisions:
                cards = safety_rules.concept_to_target_cards(cid)
                risk = safety_rules.concept_to_risk_level(cid)
                concept_decisions[cid] = (risk, cards, "embedding_fallback", round(score, 3))

    # ---------- Aggregate into SafetyMatch list ----------
    safety_cards = _load_safety_cards_indexed()
    seen_cards = {}  # card_id -> SafetyMatch
    for cid, (risk, cards, method, conf) in concept_decisions.items():
        for card_id in cards:
            card_def = safety_cards.get(card_id)
            if not card_def:
                continue
            if card_id not in seen_cards:
                seen_cards[card_id] = SafetyMatch(
                    card_id=card_id,
                    risk_level=card_def["risk_level"],
                    route=card_def["route"],
                    allow_cbt=card_def["allow_cbt"],
                    blocks_exercise=card_def["blocks_exercise"],
                    matched_signals=[],
                    match_strength=0.0,
                )
            m = seen_cards[card_id]
            m.matched_signals.append(f"{method}:{cid}@{conf:.2f}")
            m.match_strength = max(m.match_strength, float(conf))
    matches = list(seen_cards.values())

    if not matches:
        return SafetyDecision(
            matches=[],
            final_route="cbt_support",
            allow_cbt=True,
            blocks_exercise=False,
            highest_risk="low",
            safety_card_ids=[],
        )

    dominant = _dominant_route_match(matches)
    allow_cbt = all(m.allow_cbt for m in matches)
    blocks_exercise = any(m.blocks_exercise for m in matches)
    highest_risk = _highest_risk(matches)
    return SafetyDecision(
        matches=matches,
        final_route=dominant.route,
        allow_cbt=allow_cbt,
        blocks_exercise=blocks_exercise,
        highest_risk=highest_risk,
        safety_card_ids=[m.card_id for m in matches],
    )


def classify_verbose(user_message: str, enable_layer3: bool = True) -> dict:
    """Same as classify(), but returns a dict with match_method, matched_rules,
    matched_concepts, and confidence per concept.
    """
    out = {
        "matched_rules": [],
        "matched_concepts": [],
        "matched_concepts_method": {},
        "matched_concepts_confidence": {},
        "matched_groups": {},
        "layer3_top": [],
    }
    hard_hits = safety_rules.match_hard_rules(user_message)
    out["matched_rules"] = [h.rule_id for h in hard_hits]
    for h in hard_hits:
        out["matched_concepts"].append(h.concept)
        out["matched_concepts_method"][h.concept] = "hard_rule"
        out["matched_concepts_confidence"][h.concept] = 1.0

    concept_hits, group_hits = safety_rules.match_concept_rules(user_message)
    for c in concept_hits:
        if c.concept_id not in out["matched_concepts"]:
            out["matched_concepts"].append(c.concept_id)
        out["matched_concepts_method"].setdefault(c.concept_id, "concept_rule")
        out["matched_concepts_confidence"].setdefault(c.concept_id, c.confidence)
    out["matched_groups"] = {g.group_id: g.matched_terms for g in group_hits.values()}

    if enable_layer3 and not out["matched_concepts"]:
        layer3 = _layer3_match(user_message, top_k=3, include_gray=True)
        out["layer3_top"] = [(cid, round(s, 3)) for cid, s in layer3]
        for cid, score in layer3:
            if score >= LAYER3_HIGH_CONFIDENCE:
                if cid not in out["matched_concepts"]:
                    out["matched_concepts"].append(cid)
                out["matched_concepts_method"].setdefault(cid, "embedding_fallback")
                out["matched_concepts_confidence"].setdefault(cid, round(score, 3))

    decision = classify(user_message, enable_layer3=enable_layer3)
    out["final_route"] = decision.final_route
    out["allow_cbt"] = decision.allow_cbt
    out["highest_risk"] = decision.highest_risk
    out["safety_card_ids"] = decision.safety_card_ids
    return out



# Helpers
def _load_safety_cards_indexed():
    """Compat shim — delegates to pipeline.cards. Kept as a thin wrapper
    so no other file needs to change its call sites."""
    from . import cards as _cards
    return _cards.safety_cards_by_id()


_RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
_ROUTE_PRIORITY = [
    "crisis_referral",
    "medical_emergency_referral",
    "professional_or_emergency_referral",
    "medical_professional_referral",
    "abuse_safety_referral",
    "minor_referral",
    "scope_boundary",
    "conditional_cbt_after_safety_check",
]


def _route_priority(route: str) -> int:
    try:
        return _ROUTE_PRIORITY.index(route)
    except ValueError:
        return len(_ROUTE_PRIORITY)


def _dominant_route_match(matches: List[SafetyMatch]) -> SafetyMatch:
    return sorted(matches, key=lambda m: _route_priority(m.route))[0]


def _highest_risk(matches: List[SafetyMatch]) -> str:
    return max(matches, key=lambda m: _RISK_ORDER.get(m.risk_level, 0)).risk_level


# Layer 3: embedding semantic match

def _layer3_match(user_text: str, top_k: int = 5, include_gray: bool = False) -> List[Tuple[str, float]]:
    """Compare user text against concept anchor examples; return concept_id
    rankings above the backend-appropriate threshold.

    Multiple anchor rows per concept; we keep the max similarity per concept.
    Threshold is chosen per backend name because TF-IDF and sentence-
    transformers cosine distributions live in different ranges.

    HEURISTIC (Layer 3 filter):
    Only allow high/critical risk concepts to fire via embedding fallback.
    Medium-risk concepts (diagnosis_boundary, ocd_signs, eating, prompt_injection,
    role_substitution, crisis_helpline_inquiry) require an exact hard/concept
    rule match — Layer 3 over-triggers on topical similarity for these, which
    disrupts CBT flow without a safety benefit. Missing a MEDIUM-risk concept
    via Layer 3 is fine because it can still be caught by the LLM composer.

    MINIMUM LENGTH GUARD:
    Very short user messages ("evet", "ikisi de", "olmadı") are
    conversational fillers whose semantic embedding is dominated by noise.
    Layer 3 similarity for them is effectively random. We skip embedding
    fallback if the message is fewer than 15 characters OR fewer than 3
    tokens — Layer 1/2 exact matches still run, and the composer still gets
    the message. Only the noisy embedding step is bypassed.
    """
    stripped = user_text.strip()
    if len(stripped) < 15 or len(stripped.split()) < 3:
        return []
    backend, matrix, concept_for_row = _build_anchor_index()
    q = backend.encode([user_text])
    sims = embedding_backend.cosine_similarity(q, matrix)
    sims = sims[0]
    # max sim per concept
    best = {}
    for i, cid in enumerate(concept_for_row):
        s = float(sims[i])
        if cid not in best or s > best[cid]:
            best[cid] = s
    th = _thresholds_for(backend.name)
    threshold = th["gray"] if include_gray else th["high"]
    ranked = []
    for cid, s in best.items():
        if s < threshold:
            continue
        # Filter: Layer 3 only for high/critical risk concepts
        risk = safety_rules.concept_to_risk_level(cid)
        if risk not in ("high", "critical"):
            continue
        ranked.append((cid, s))
    ranked.sort(key=lambda x: -x[1])
    return ranked[:top_k]


if __name__ == "__main__":
    import sys
    examples = [
        "Yaşamak istemiyorum, kendime zarar vermeyi düşünüyorum.",
        "Göğsüm sıkışıyor, nefes alamıyorum.",
        "Sürekli nabzımı kontrol ediyorum, kalbim hızlı atıyor.",
        "Ben 14 yaşındayım, annem babam haberi olmadan yardım eder misin?",
        "Bende panik bozukluk mu var, tanı koyar mısın?",
        "Antidepresan dozumu artırayım mı?",
        # Layer 3 candidates — should match by anchor similarity (no exact rules)
        "Hayatın artık bir anlamı yok gibi geliyor",
        "Soluk alamıyorum çok kötü",
        "Hava yetmiyor sanki nefesim yok",
    ]
    for ex in examples:
        d = classify(ex)
        v = classify_verbose(ex)
        print(f"\n>>> {ex}")
        print(f"   route={d.final_route} allow_cbt={d.allow_cbt} risk={d.highest_risk}")
        print(f"   rules={v['matched_rules']}")
        print(f"   concepts={v['matched_concepts']}")
        print(f"   methods={v['matched_concepts_method']}")
        if v.get("layer3_top"):
            print(f"   layer3_top={v['layer3_top']}")
