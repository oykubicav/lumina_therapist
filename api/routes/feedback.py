"""POST /feedback — persist to DB.

thumbs_down + comment → future response_test_set regression case.
flag → clinician review workflow (dashboard TBD).
"""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import FeedbackRequest, FeedbackResponse
from api.db import get_db
from api.db.models import Feedback, Turn


router = APIRouter(prefix="/feedback", tags=["feedback"])
log = logging.getLogger(__name__)


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    # Validate turn_id exists (loose — non-UUID gets 400)
    try:
        turn_uuid = uuid.UUID(req.turn_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="turn_id must be a UUID")

    turn = db.get(Turn, turn_uuid)
    if turn is None:
        # We accept feedback for unknown turns too — silently — for the case
        # where the user submits feedback after the turn expired. Optionally
        # return 404, but that leaks retention policy.
        pass

    session_uuid = None
    if req.session_id:
        try:
            session_uuid = uuid.UUID(req.session_id)
        except (ValueError, TypeError):
            session_uuid = None

    row = Feedback(
        turn_id=turn_uuid,
        session_id=session_uuid,
        verdict=req.verdict,
        comment=req.comment,
    )
    db.add(row)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        log.exception("failed to persist feedback")
        raise HTTPException(status_code=500, detail=f"persist error: {type(e).__name__}")

    log.info(
        "feedback_received",
        extra={
            "turn_id": req.turn_id,
            "session_id": req.session_id,
            "route": "/feedback",
        },
    )
    return FeedbackResponse(received=True, feedback_id=str(row.id))
