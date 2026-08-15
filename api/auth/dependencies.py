"""FastAPI dependencies for auth.

Usage in an endpoint:
    from api.auth.dependencies import get_current_user

    @router.get("/me")
    async def me(user: User = Depends(get_current_user)):
        return {"email": user.email}

    # optional-auth pattern:
    @router.post("/chat")
    async def chat(user: Optional[User] = Depends(get_current_user_optional)):
        # user None ise anonim
        ...
"""
from typing import Optional

from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from api.auth.jwt_utils import decode_token
from api.db import get_db
from api.db.models import User


def _extract_token(authorization: Optional[str]) -> Optional[str]:
    """Authorization header'dan 'Bearer XXX' pattern'inden token çek."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Return the authenticated user, or None if no/invalid token.

    Never raises — anonymous requests just get None. Use this on endpoints
    that support both anon and authed users (e.g. /chat).
    """
    token = _extract_token(authorization)
    if not token:
        return None
    user_id = decode_token(token)
    if not user_id:
        return None
    user = db.get(User, user_id)
    if user is None or user.deleted_at is not None:
        return None
    return user


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Return the authenticated user or raise 401.

    Use on endpoints that require auth (e.g. /me, /progress).
    """
    user = await get_current_user_optional(authorization, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
