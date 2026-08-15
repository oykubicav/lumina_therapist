"""POST /consent — KVKK açık rıza kayıt endpoint'i.

Kullanıcı chat başlamadan önce onay veriyor. Backend:
  - consent_records tablosuna insert
  - session yoksa yaratır, consent_id'yi bağlar
  - ip + user-agent hash'i tutar (adli audit için, PII değil)
"""

from __future__ import annotations

import hashlib
import logging
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from api.db import get_db
from api.db.models import ConsentRecord, ChatSession
from api.schemas import ConsentRequest, ConsentResponse


router = APIRouter(prefix="/consent", tags=["consent"])
log = logging.getLogger(__name__)

CURRENT_POLICY_VERSION = os.environ.get("CBT_POLICY_VERSION", "0.2")
_HASH_SALT = os.environ.get("CBT_HASH_SALT", "cbt-mvp-salt-change-me")


def _hash(s: str) -> str:
    return hashlib.sha256((s + _HASH_SALT).encode("utf-8")).hexdigest()[:24]


@router.post("", response_model=ConsentResponse)
async def submit_consent(
    req: ConsentRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    if req.policy_version != CURRENT_POLICY_VERSION:
        raise HTTPException(
            status_code=400,
            detail=f"policy_version mismatch (server: {CURRENT_POLICY_VERSION})",
        )

    # Session upsert
    if req.session_id:
        try:
            sid_uuid = uuid.UUID(req.session_id)
        except (ValueError, TypeError):
            sid_uuid = uuid.uuid4()
            req.session_id = str(sid_uuid)
        sess = db.get(ChatSession, sid_uuid)
        if sess is None:
            sess = ChatSession(id=sid_uuid)
            db.add(sess)
    else:
        sess = ChatSession()
        db.add(sess)
        db.flush()

    # Extract client identifiers (hashed for audit)
    fwd = request.headers.get("x-forwarded-for") or ""
    ip = fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "")
    ua = request.headers.get("user-agent") or ""

    consent = ConsentRecord(
        session_id=sess.id,
        policy_version=req.policy_version,
        ip_hash=_hash(ip) if ip else None,
        user_agent_hash=_hash(ua) if ua else None,
    )
    db.add(consent)
    db.flush()
    sess.consent_id = consent.id

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        log.exception("failed to persist consent")
        raise HTTPException(500, detail=f"persist error: {type(e).__name__}")

    log.info(
        "consent_recorded",
        extra={
            "session_id": str(sess.id),
            "route": "/consent",
        },
    )
    return ConsentResponse(
        session_id=str(sess.id),
        consent_id=str(consent.id),
        policy_version=req.policy_version,
    )
