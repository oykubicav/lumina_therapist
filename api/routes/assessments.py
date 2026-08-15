"""Assessments endpoints — PHQ-9 / GAD-7 submission + history.

Routes:
  POST   /assessments              — submit new assessment
  GET    /assessments/latest       — most recent score (frontend "you were 12, now 8")
  GET    /assessments              — full history (trend chart)

KVKK: session cascade delete — session silindiğinde assessments da gider.
Suicide flag: PHQ-9 item 9 > 0 ise submit response'unda crisis_alert=True döner,
frontend crisis UI'ını gösterir.
"""
from __future__ import annotations

import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.db.models import Assessment
from api.deps import session_store_dep
from api.session import InMemorySessionStore
from pipeline.assessments import score

router = APIRouter(prefix="/assessments", tags=["assessments"])
log = logging.getLogger(__name__)

_CRISIS_MESSAGE_TR = (
    "PHQ-9'da kendine zarar verme düşüncesi bildirdin. "
    "Acil durumdaysan 112'yi ara veya en yakın acil servise git. "
    "Aile hekimin, psikiyatri veya klinik psikolog desteği alabilirsin."
)

# Schemas
class AssessmentSubmitRequest(BaseModel):
    session_id: str
    kind: str = Field(..., pattern="^(phq9|gad7)$")
    answers: List[int]
    notes: Optional[str] = None


class AssessmentResponse(BaseModel):
    id: str
    kind: str
    total_score: int
    severity: str
    suicide_flag: bool
    taken_at: str


class AssessmentSubmitResponse(BaseModel):
    assessment: AssessmentResponse
    crisis_alert: bool = False
    crisis_message: Optional[str] = None


def _row_to_response(row: Assessment) -> AssessmentResponse:
    return AssessmentResponse(
        id=str(row.id),
        kind=row.kind,
        total_score=row.total_score,
        severity=row.severity,
        suicide_flag=row.suicide_flag,
        taken_at=row.taken_at.isoformat(),
    )


@router.post("", response_model=AssessmentSubmitResponse)
async def submit_assessment(
    req: AssessmentSubmitRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    try:
        session_uuid = uuid.UUID(req.session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid session_id")
    try:
        scored = score(req.kind, req.answers)  # type: ignore[arg-type]
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    store.ensure(req.session_id)

    session_local = store._SessionLocal()
    with session_local() as db, db.begin():
        row = Assessment(
            session_id=session_uuid,
            kind=req.kind,
            answers=req.answers,
            total_score=scored.total_score,
            severity=scored.severity,
            suicide_flag=scored.suicide_flag,
            notes=req.notes,
        )
        db.add(row)
        db.flush()
        db.refresh(row)

    crisis_alert = scored.suicide_flag
    return AssessmentSubmitResponse(
        assessment=AssessmentResponse(
            id=str(row.id),
            kind=row.kind,
            total_score=row.total_score,
            severity=row.severity,
            suicide_flag=row.suicide_flag,
            taken_at=row.taken_at.isoformat(),
        ),
        crisis_alert=crisis_alert,
        crisis_message=_CRISIS_MESSAGE_TR if crisis_alert else None,
    )


@router.get("/latest", response_model=Optional[AssessmentResponse])
async def latest_assessment(
    session_id: str = Query(...),
    kind: Optional[str] = Query(None, pattern="^(phq9|gad7)$"),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid session_id")

    session_local = store._SessionLocal()
    with session_local() as db:
        q = db.query(Assessment).filter_by(session_id=session_uuid)
        if kind is not None:
            q = q.filter_by(kind=kind)
        row = q.order_by(Assessment.taken_at.desc()).first()

    if row is None:
        return None
    return _row_to_response(row)


@router.get("", response_model=List[AssessmentResponse])
async def list_assessments(
    session_id: str,
    kind: Optional[str] = Query(None, pattern="^(phq9|gad7)$"),
    limit: int = Query(20, ge=1, le=100),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid session_id")
        
    session_local = store._SessionLocal()
    with session_local() as db:
        q = db.query(Assessment).filter_by(session_id=session_uuid)
        
        if kind is not None:
            q = q.filter_by(kind=kind)
            
        rows = q.order_by(Assessment.taken_at.asc()).limit(limit).all()
        
        results = [_row_to_response(x) for x in rows]

    return results



