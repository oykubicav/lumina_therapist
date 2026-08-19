"""Pipeline data structures (no business logic)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class SafetyMatch:
    """One matched safety card."""
    card_id: str
    risk_level: str           # critical | high | medium | low
    route: str
    allow_cbt: bool
    blocks_exercise: bool
    matched_signals: List[str]   # which trigger phrases matched
    match_strength: float        # 0..1, simple normalised score


@dataclass
class SafetyDecision:
    """Aggregated decision over all matched safety cards."""
    matches: List[SafetyMatch]
    final_route: str             # one of the allowed routes, or "cbt_support"
    allow_cbt: bool              # final gate
    blocks_exercise: bool
    highest_risk: str            # max risk level among matches
    safety_card_ids: List[str]   # for retrieval inclusion (e.g. do_not_delay_care)

    # Sinyal kesin bir ifade eşleşmesinden değil, çıkarımdan geldiyse True.
    # Bu durumda kriz metni doğrudan basılmaz; önce kullanıcıya doğru anlaşılıp
    # anlaşılmadığı sorulur.
    needs_confirmation: bool = False


@dataclass
class IntentDecision:
    """Module routing from intent classifier."""
    primary_module: str          # health_anxiety | panic | gad | depression | low_self_esteem | safety | unknown
    secondary_modules: List[str] # for cross-module cases
    confidence: float            # 0..1
    rationale: str               # short LLM rationale (for debugging only)



@dataclass
class RetrievedCard:
    """One card returned by the retriever."""
    card_id: str
    topic: str
    type: str
    title_tr: str
    score: float
    snippet: str                 # first ~200 chars for debug

    # --- Graph enrichment (opsiyonel — vektör kartlarında None) ---
    source: str = "vector"                       # "vector" | "graph_technique" | "graph_neighbor" | "safety"
    via_technique: Optional[str] = None          # graf: aynı tekniği paylaştığı kart üzerinden geldiyse
    via_neighbor_of: Optional[str] = None        # graf: komşu modülden bir kart üzerinden geldiyse


@dataclass
class PipelineResponse:
    """End-to-end response."""
    user_message: str
    safety: SafetyDecision
    intent: Optional[IntentDecision]
    retrieved: List[RetrievedCard]
    composed_text: Optional[str]
    critic_passed: Optional[bool]
    critic_findings: List[str]
    # tracing
    timing_ms: Dict[str, float] = field(default_factory=dict)
    debug: Dict[str, Any] = field(default_factory=dict)
