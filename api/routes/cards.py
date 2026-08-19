"""Cards endpoints — content library exposure.

  GET /cards                    → filtered CBT card list (summary)
  GET /cards/topics             → topic dropdown + counts
  GET /cards/safety             → all safety cards (admin gated)
  GET /cards/safety/{card_id}   → single safety card
  GET /cards/{card_id}          → single CBT card (full content)

Route order matters: /cards/{card_id} MUST be last so specific routes
(/topics, /safety) aren't shadowed.
"""

from __future__ import annotations

from typing import Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, Query

from api.schemas import (
    CBTCardOut, CBTCardSummary, CBTCardListResponse,
    SafetyCardOut, SafetyCardListResponse,
    TopicInfo, TopicsResponse,
)
from api.deps import require_admin
from api import card_store
from api.card_store import TOPIC_DISPLAY_TR, TOPICS_ORDER
from pipeline import cards as _cards


router = APIRouter(prefix="/cards", tags=["cards"])


# ------------------------------------------------------------
# /cards — CBT list
# ------------------------------------------------------------

@router.get("", response_model=CBTCardListResponse)
async def list_cards(
    topic: Optional[Literal[
        "health_anxiety", "panic", "gad", "depression", "low_self_esteem", "insomnia", "work_stress", "relationship_stress", "grief_loss", "life_transitions", "trauma_awareness", "social_anxiety"
    ]] = Query(None),
    type: Optional[Literal[
        "psychoeducation", "self_assessment", "exercise", "technique", "safety"
    ]] = Query(None),
    q: Optional[str] = Query(None, description="Substring search on title_tr"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    filtered = card_store.filter_cbt_cards(topic=topic, type_=type, q=q)
    total = len(filtered)
    page = filtered[offset: offset + limit]
    return CBTCardListResponse(
        cards=[
            CBTCardSummary(
                id=c["id"],
                topic=c["topic"],
                type=c["type"],
                title_tr=c["title_tr"],
                review_status=c.get("review_status", "needs_review"),
            )
            for c in page
        ],
        total=total, limit=limit, offset=offset,
    )


# ------------------------------------------------------------
# /cards/topics
# ------------------------------------------------------------

@router.get("/topics", response_model=TopicsResponse)
async def list_topics():
    counts = card_store.topic_counts()
    return TopicsResponse(
        topics=[
            TopicInfo(
                topic=t,
                count=counts.get(t, 0),
                display_name_tr=TOPIC_DISPLAY_TR.get(t, t),
            )
            for t in TOPICS_ORDER
        ]
    )


# ------------------------------------------------------------
# /cards/safety — admin gated
# ------------------------------------------------------------

@router.get(
    "/safety",
    response_model=SafetyCardListResponse,
    dependencies=[Depends(require_admin)],
)
async def list_safety_cards():
    """Safety kartları — klinisyen/admin dashboard için. Frontend'e default
    gösterme (route/policy alanı kullanıcıyı yanıltabilir)."""
    all_sf = _cards.all_safety_cards()
    return SafetyCardListResponse(
        cards=[_to_safety_out(c) for c in all_sf],
        total=len(all_sf),
    )


@router.get(
    "/safety/{card_id}",
    response_model=SafetyCardOut,
    dependencies=[Depends(require_admin)],
)
async def get_safety_card(card_id: str):
    c = _cards.safety_cards_by_id().get(card_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"safety card not found: {card_id}")
    return _to_safety_out(c)


# ------------------------------------------------------------
# /cards/{card_id} — MUST be last
# ------------------------------------------------------------

@router.get("/{card_id}", response_model=CBTCardOut)
async def get_card(card_id: str):
    c = _cards.cbt_cards_by_id().get(card_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"card not found: {card_id}")
    return CBTCardOut(
        id=c["id"],
        topic=c["topic"],
        type=c["type"],
        title_tr=c["title_tr"],
        content_tr=c["content_tr"],
        safety_notes=c.get("safety_notes"),
        source_refs=c.get("source_refs", []),
        review_status=c.get("review_status", "needs_review"),
    )


# ------------------------------------------------------------
# helpers
# ------------------------------------------------------------

def _to_safety_out(c: dict) -> SafetyCardOut:
    return SafetyCardOut(
        card_id=c["card_id"],
        module=c["module"],
        card_type=c["card_type"],
        title=c["title"],
        risk_level=c["risk_level"],
        route=c["route"],
        allow_cbt=c["allow_cbt"],
        blocks_exercise=c["blocks_exercise"],
        must_do_tr=c.get("must_do_tr", ""),
        must_not_do_tr=c.get("must_not_do_tr", []),
        safe_response_template_tr=c.get("safe_response_template_tr", ""),
        concept_ids=c.get("concept_ids", []),
        review_status=c.get("review_status", "needs_clinician_review"),
    )
