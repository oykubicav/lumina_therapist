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
import uuid

from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from api.auth.jwt_utils import decode_token
from api.db.models import User
from api.deps import session_store_dep
from api.session import InMemorySessionStore

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
    store: InMemorySessionStore = Depends(session_store_dep),
) -> Optional[User]:
token = _extract_token(authorization)
if not token:
    return None
user_id = decode_token(token)
if not user_id:
    return None
factory = store._SessionLocal()
with factory as db:
    user = db.get(User, user_id)
    if user and user.deleted_at is None:
        return user
    return None

async def get_current_user(
    authorization: Optional[str]= header(None),
    store: InMemorySessionStore = Depends(session_store_dep),
) -> User:
    user = await get_current_user_optional(authorization, store)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


