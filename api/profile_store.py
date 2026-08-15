"""UserProfile store — CRUD + ProfilePatch apply.

- get_or_create(session_id) → UserProfile row (yeni ise boş bir tane döner)
- apply_patch(session_id, patch) → mevcut değerlere merge, kaydet
- get_summary(session_id) → composer için string özet
- delete(session_id) → KVKK unutulma hakkı için (session cascade zaten
  yapıyor ama explicit endpoint için burada da)

Design: idempotent, sessiz-fail. Herhangi bir hata olursa exception yerine
log at ve None dön. Profile arka planda çalışıyor — cevap akışını asla
bloklamamalı.
"""

from __future__ import annotations

import logging
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from api.db.models import UserProfile
from api.db.models import ChatSession
from pipeline.profile_extractor import ProfilePatch, format_profile_for_composer

logger = logging.getLogger(__name__)


# ============================================================
# CRUD
# ============================================================

def get_or_create(db: Session, session_id: uuid.UUID) -> Optional[UserProfile]:
    """Session için profil bul; yoksa boş bir tane yarat."""
    try:
        row = db.query(UserProfile).filter_by(session_id=session_id).one_or_none()
        if row is not None:
            return row
        session_row = db.get(ChatSession, session_id)
        user_id = session_row.user_id if session_row else None

        row = UserProfile(
            session_id=session_id,
            user_id=user_id,  
            triggers=[],
            themes=[],
            coping_tried={},
            modules_engaged=[],
            progress_notes=[],
            turn_count=0,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row
    except Exception as e:
        logger.warning(f"profile_store.get_or_create failed: {e}")
        db.rollback()
        return None


def get_summary_for_composer(db: Session, session_id: uuid.UUID) -> str:
    """Composer'ın system prompt'una girecek Türkçe özet. Yoksa boş string."""
    try:
        row = db.query(UserProfile).filter_by(session_id=session_id).one_or_none()
        if row is None:
            return ""
        profile_dict = {
            "triggers": row.triggers,
            "themes": row.themes,
            "coping_tried": row.coping_tried,
            "modules_engaged": row.modules_engaged,
            "progress_notes": row.progress_notes,
        }
        return format_profile_for_composer(profile_dict)
    except Exception as e:
        logger.warning(f"profile_store.get_summary failed: {e}")
        return ""


# ============================================================
# Apply patch
# ============================================================

def _merge_list(existing: list | None, new: list, max_len: int = 20) -> list:
    """Duplicate'siz union, en fazla max_len."""
    existing = existing or []
    seen = set(x.lower() for x in existing if isinstance(x, str))
    for item in new:
        if isinstance(item, str) and item.lower() not in seen:
            existing.append(item)
            seen.add(item.lower())
    return existing[-max_len:]   # yeni maddeler önde kalsın


def apply_patch(db: Session, session_id: uuid.UUID, patch: ProfilePatch) -> bool:
    """ProfilePatch'i mevcut profile'a merge et. Sessiz-fail."""
    if patch.is_empty():
        # Sadece turn_count artır
        return _bump_turn_count(db, session_id)

    try:
        row = get_or_create(db, session_id)
        if row is None:
            return False

        # Merge — mevcut liste + yeni items (dedupe)
        row.triggers = _merge_list(row.triggers, patch.add_triggers, max_len=15)
        row.themes = _merge_list(row.themes, patch.add_themes, max_len=10)
        row.modules_engaged = _merge_list(row.modules_engaged, patch.add_modules, max_len=11)

        # coping_updates: dict merge, yeni değer eski değeri override eder
        current_coping = dict(row.coping_tried or {})
        current_coping.update(patch.coping_updates)
        # Max 20 technique tut
        if len(current_coping) > 20:
            current_coping = dict(list(current_coping.items())[-20:])
        row.coping_tried = current_coping

        # progress_notes: append, en son 10 tut
        if patch.progress_note:
            notes = list(row.progress_notes or [])
            notes.append(patch.progress_note)
            row.progress_notes = notes[-10:]

        row.turn_count = (row.turn_count or 0) + 1

        # last_summary — bir sonraki turn'de composer bu string'i alacak
        profile_dict = {
            "triggers": row.triggers,
            "themes": row.themes,
            "coping_tried": row.coping_tried,
            "modules_engaged": row.modules_engaged,
            "progress_notes": row.progress_notes,
        }
        row.last_summary = format_profile_for_composer(profile_dict)

        db.commit()
        return True

    except Exception as e:
        logger.warning(f"profile_store.apply_patch failed: {e}")
        db.rollback()
        return False


def _bump_turn_count(db: Session, session_id: uuid.UUID) -> bool:
    """Patch boş ise sadece turn sayacı artır."""
    try:
        row = db.query(UserProfile).filter_by(session_id=session_id).one_or_none()
        if row is None:
            return False
        row.turn_count = (row.turn_count or 0) + 1
        db.commit()
        return True
    except Exception as e:
        logger.warning(f"profile_store._bump_turn_count failed: {e}")
        db.rollback()
        return False


# ============================================================
# KVKK — delete
# ============================================================

def delete(db: Session, session_id: uuid.UUID) -> bool:
    """Explicit unutulma hakkı endpoint'i için. Session cascade zaten
    profili siler ama kullanıcı 'sadece profili unut, sohbeti tut' isterse
    bu endpoint çağrılır."""
    try:
        db.query(UserProfile).filter_by(session_id=session_id).delete()
        db.commit()
        return True
    except Exception as e:
        logger.warning(f"profile_store.delete failed: {e}")
        db.rollback()
        return False
