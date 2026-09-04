"""Auth endpoints — email + password, magic verification, JWT tokens.

Endpoints:
  POST   /auth/register        — email + password, verify email yollar
  POST   /auth/verify          — verify token → email_verified=True
  POST   /auth/login           — email + password → JWT
  POST   /auth/forgot-password — email → reset link
  POST   /auth/reset-password  — token + new_password → success
  GET    /auth/me              — current user (auth required)
  DELETE /auth/me              — hesap + cascade delete (auth required)

KVKK: DELETE /me tüm user data'yı cascade siler (sessions, turns, profiles, assessments).
"""
from __future__ import annotations

import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy import select, func as sqlfunc
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from api.auth.dependencies import get_current_user
from api.auth.email import send_verification_email, send_password_reset_email
from api.auth.jwt_utils import encode_token
from api.auth.passwords import hash_password, verify_password
from api.db.models import User,ChatSession, Turn
from api.deps import session_store_dep
from api.session import InMemorySessionStore

router = APIRouter(prefix="/auth", tags=["auth"])
log = logging.getLogger(__name__)

class RegisterRequest(BaseModel):
    email:EmailStr
    password: str = Field(..., min_length=8, max_length=128)
class LoginRequest(BaseModel):
    email:EmailStr
    password: str
class VerifyRequest(BaseModel):
    token:str
class ForgotRequest(BaseModel):
    email:EmailStr
class ResetRequest(BaseModel):
    token:str
    new_password: str = Field(..., min_length=8, max_length=128)
class UserView(BaseModel):
    id:str
    email:str
    email_verified:bool
    created_at: str
    display_name: Optional[str] = None
    focus_topics: list[str] = []
    onboarded_at: Optional[str] = None
    focus_greeted_at: Optional[str] = None


class ProfileUpdate(BaseModel):
    """Onboarding ekranından gelen tercihler. Hepsi isteğe bağlı —
    kullanıcı adı boş bırakıp yalnızca konu seçebilir ya da tümünü atlayabilir.

    focus_greeted: karşılamada konular anıldığında bir kez True gönderilir,
    sonraki sohbetlerde aynı cümle kurulmasın diye.
    """
    display_name: Optional[str] = Field(None, max_length=60)
    focus_topics: Optional[list[str]] = Field(None, max_length=10)
    focus_greeted: Optional[bool] = None
class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"
    user: UserView
class RegisterResponse(BaseModel):
    user: UserView
    email_sent: bool
class ResendVerifyRequest(BaseModel):
    email: EmailStr
class SessionSummary(BaseModel):
    session_id: str
    title: str
    created_at: str
    last_active: str
    turn_count: int

class SessionListResponse(BaseModel):
    sessions: list[SessionSummary]
    total: int
class SessionTurnView(BaseModel):
    turn_id: str
    ts: str
    user_message: Optional[str]
    response: str
class SessionDetail(BaseModel):
    session_id: str
    title: str
    created_at: str
    last_active: str
    turns: list[SessionTurnView]
def _session_title(first_message: Optional[str], created_at: datetime) -> str:
    """Başlık ilk kullanıcı mesajından türetiliyor — ayrı bir kolon yok.
    Mesaj silinmişse tarihe düşüyor."""
    if first_message:
        t = " ".join(first_message.split())
        return t[:57] + "…" if len(t) > 60 else t
    return created_at.strftime("%d.%m.%Y") + " sohbeti"
def _iso_utc(dt: Optional[datetime]) -> Optional[str]:
    """Her zaman saat dilimi bilgisiyle döndür.

    SQLite tz bilgisini saklamıyor, Postgres saklıyor. Normalize etmezsek
    aynı alan ortama göre farklı biçimde çıkıyor ve istemci naive değeri
    yerel saat sanabiliyor.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _to_user_view(user: User) -> UserView:
    return UserView(
        id=str(user.id),
        email=user.email,
        email_verified=user.email_verified,
        created_at=_iso_utc(user.created_at),
        display_name=user.display_name,
        focus_topics=user.focus_topics or [],
        onboarded_at=_iso_utc(user.onboarded_at),
        focus_greeted_at=_iso_utc(user.focus_greeted_at),
    )


@router.post("/register", response_model=RegisterResponse)
async def register(
    req: RegisterRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    factory = store._SessionLocal()
    verify_token = secrets.token_urlsafe(32)

    try:
        with factory() as db:
            with db.begin():
                existing = db.query(User).filter_by(email=req.email).one_or_none()
                if existing:
                    raise HTTPException(status_code=409, detail="Bu e-posta zaten kayıtlı")

                user = User(
                    email=req.email,
                    password_hash=hash_password(req.password),
                    email_verified=False,
                    verification_token=verify_token,
                )
                db.add(user)

            db.refresh(user)
            view = _to_user_view(user)

        # DB kapandı — email
        sent = send_verification_email(req.email, verify_token)
        return RegisterResponse(user=view, email_sent=sent)

    except HTTPException:
        raise
    except Exception:
        log.exception("register failed")
        raise HTTPException(status_code=500, detail="Kayıt sırasında bir hata oluştu")
        
@router.post("/verify")
async def verify_email(
    req: VerifyRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """Verification token → email_verified=True. Idempotent."""
    factory = store._SessionLocal()
    
    with factory() as db:
        # TODO 1: Token ile user bul
        user = db.query(User).filter_by(verification_token=req.token).one_or_none()
        
        # TODO 2: Yoksa 404 "invalid token"
        if not user:
            raise HTTPException(status_code=404, detail="invalid token")
        
        # TODO 3: email_verified=True + verification_token=None (tek kullanımlık)
        try:
            user.email_verified = True
            user.verification_token = None
            db.commit()
        except Exception:
            db.rollback()
            log.exception("email verification failed")
            raise HTTPException(status_code=500, detail="Doğrulama işlemi sırasında bir hata oluştu")
            
        # TODO 4: {"status": "verified"} dön
        return {"status": "verified"}
@router.post("/resend-verify")
async def resend_verify(
    req: ResendVerifyRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """Verify email kaybolduysa tekrar yolla. Timing-attack koruması için
    var/yok her durumda 200 dön."""
    factory = store._SessionLocal()
    new_token = secrets.token_urlsafe(32)

    with factory() as db:
        with db.begin():
            user = db.query(User).filter_by(email=req.email).one_or_none()
            if user and not user.email_verified:
                user.verification_token = new_token

    # DB dışına çıktıktan sonra email atıyoruz
    if user and not user.email_verified:
        send_verification_email(req.email, new_token)

    return {"status": "ok"}
    




@router.post("/login", response_model=TokenResponse)
async def login(
    req: LoginRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    factory = store._SessionLocal()
    with factory() as db:
        user = db.query(User).filter_by(email=req.email).one_or_none()
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="E-posta ya da şifre hatalı")

        if user.deleted_at is not None:
            raise HTTPException(status_code=401, detail="E-posta ya da şifre hatalı")
        if not user.email_verified:
            raise HTTPException(
                status_code=403,
                detail="Önce e-posta adresini doğrula. Kayıt sırasında gönderilen linke tıkla."
            )
        token = encode_token(user.id)
        return TokenResponse(access_token=token,user=_to_user_view(user))


        
@router.get("/me", response_model=UserView)
async def get_me(
    user: User = Depends(get_current_user),
):
    """Current user info. Auth required (401 if no token)."""
    return _to_user_view(user)

_FOCUS_IDS = {
    "anxiety", "mood", "sleep", "self", "work",
    "relationships", "loss", "change", "panic", "unsure",
}


@router.patch("/me/profile", response_model=UserView)
async def update_my_profile(
    req: ProfileUpdate,
    user: User = Depends(get_current_user),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """Onboarding tercihlerini kaydeder ve onboarded_at'i damgalar.

    Boş gövdeyle çağrılması geçerli: kullanıcı adı da konu da vermeden
    "şimdilik geç" dediğinde tekrar sorulmaması için damga yine atılır.
    """
    factory = store._SessionLocal()
    with factory() as db, db.begin():
        row = db.get(User, user.id)
        if row is None:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        if req.display_name is not None:
            temiz = req.display_name.strip()
            row.display_name = temiz[:60] or None

        if req.focus_topics is not None:
            row.focus_topics = [t for t in req.focus_topics if t in _FOCUS_IDS]

        # Bir kez damgalanır; sonraki istekler tarihi ileri taşımaz.
        if req.focus_greeted and row.focus_greeted_at is None:
            row.focus_greeted_at = datetime.now(timezone.utc)

        if row.onboarded_at is None:
            row.onboarded_at = datetime.now(timezone.utc)

        db.flush()
        view = _to_user_view(row)

    return view


@router.delete("/me")
async def delete_me(
    user: User = Depends(get_current_user),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """KVKK: hesap + tüm ilgili data (sessions/turns/profiles/assessments) cascade siliniyor."""
    factory = store._SessionLocal()
    with factory() as db, db.begin():
        db.delete(db.get(User, user.id))
    return {"status": "deleted"}


@router.post("/forgot-password")
async def forgot_password(
    req: ForgotRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """Reset email yolla. Timing-attack koruması için var/yok her durumda 200 dön."""
    factory = store._SessionLocal()

    email_payload: tuple[str, str] | None = None

    with factory() as db:
        user = db.query(User).filter_by(email=req.email).one_or_none()
        if user and user.deleted_at is None:
            reset_token = secrets.token_urlsafe(32)
            reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            try:
                user.reset_token = reset_token
                user.reset_token_expires_at = reset_token_expires_at
                db.commit()
                email_payload = (req.email, reset_token)
            except Exception:
                db.rollback()
                log.exception("forgot-password db update failed")

    if email_payload:
        email, token = email_payload
        send_password_reset_email(email, token)

    return {"status": "ok", "message": "Eğer e-posta kayıtlı ise reset linki gönderildi"}

@router.post("/reset-password")
async def reset_password(
    req: ResetRequest,
    store: InMemorySessionStore = Depends(session_store_dep),
):
    """Token + new_password → success. Token tek kullanımlık, 1 saat geçerli."""
    factory = store._SessionLocal()

    with factory() as db:
        user = db.query(User).filter_by(reset_token=req.token).one_or_none()
        if not user or user.deleted_at is not None:
            raise HTTPException(status_code=404, detail="invalid token")
        # SQLite tz-naive datetime döner; Postgres tz-aware. Karşılaştırma için normalize.
        expires_at = user.reset_token_expires_at
        if not expires_at:
            raise HTTPException(status_code=400, detail="token expired")
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=400, detail="token expired")

        try:
            user.password_hash = hash_password(req.new_password)
            user.reset_token = None
            user.reset_token_expires_at = None
            db.commit()
        except Exception:
            db.rollback()
            log.exception("reset-password db update failed")
            raise HTTPException(status_code=500, detail="Şifre sıfırlama sırasında bir hata oluştu")

    return {"status": "ok", "message": "Şifre başarıyla sıfırlandı"}

@router.get("/sessions", response_model=SessionListResponse)
async def list_my_sessions(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    factory = store._SessionLocal()
    with factory() as db:
        total = db.execute(
            select(sqlfunc.count(ChatSession.id)).where(ChatSession.user_id == user.id)
        ).scalar_one()
        rows= db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user.id)
            .order_by(ChatSession.last_active.desc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()
        ids = [s.id for s in rows]
        counts,firsts = {},{}
        if ids:
            counts=dict(db.execute(
                select(Turn.session_id, sqlfunc.count(Turn.id))
                .where(Turn.session_id.in_(ids))
                .group_by(Turn.session_id)
            ).all())
            for sid,msg in db.execute(
                select(Turn.session_id, Turn.user_message)
                .where(Turn.session_id.in_(ids))
                .order_by(Turn.ts.asc())
            ).all():
                firsts.setdefault(sid,msg)
        out =[
            SessionSummary(
                session_id=str(s.id),
                title=_session_title(firsts.get(s.id), s.created_at),
                created_at=s.created_at.isoformat(),
                last_active=s.last_active.isoformat(),
                turn_count=counts.get(s.id, 0),
            )
            for s in rows
            if counts.get(s.id, 0) > 0  # only include sessions with at least one turn
        ]
        return SessionListResponse(sessions=out, total=total)

    



@router.get("/sessions/{session_id}", response_model=SessionDetail)
async def get_my_session(
    session_id:str,
    user: User = Depends(get_current_user),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    try:
        sid=uuid.UUID(session_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")
    factory = store._SessionLocal()
    with factory() as db:
        sess= db.get(ChatSession, sid)
        if sess is None or sess.user_id != user.id:
            raise HTTPException(status_code=404, detail="Sohbet bulunamadı")
        rows = db.execute(
            select(Turn).where(Turn.session_id == sid).order_by(Turn.ts.asc())
        ).scalars().all()
        return SessionDetail(
            session_id=str(sess.id),
            title=_session_title(rows[0].user_message if rows else None, sess.created_at),
            created_at=sess.created_at.isoformat(),
            last_active=sess.last_active.isoformat(),
            turns=[
                SessionTurnView(
                    turn_id=str(t.id),
                    ts=t.ts.isoformat(),
                    user_message=t.user_message,
                    response=t.response,
                )
                for t in rows
            ],
        )
@router.delete("/sessions/{session_id}")
async def delete_my_session(
    session_id: str,
    user: User = Depends(get_current_user),
    store: InMemorySessionStore = Depends(session_store_dep),
):
    try:
        sid = uuid.UUID(session_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    factory = store._SessionLocal()
    with factory() as db, db.begin():
        sess = db.get(ChatSession, sid)
        if sess is None or sess.user_id != user.id:
            raise HTTPException(status_code=404, detail="Sohbet bulunamadı")
        db.delete(sess)
    return {"status": "deleted"}
    
    






    
