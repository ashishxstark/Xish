from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
import httpx

from .config import settings


bearer_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser:
    def __init__(self, user_id: str, email: Optional[str] = None):
        self.user_id = user_id
        self.email = email


async def fetch_jwks() -> dict:  # cache could be added if needed
    if not settings.supabase_jwks_url:
        raise RuntimeError("SUPABASE_JWKS_URL is not configured")
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(settings.supabase_jwks_url)
        resp.raise_for_status()
        return resp.json()


async def verify_token(token: str) -> dict:
    jwks = await fetch_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        keys = jwks.get("keys", [])
        key = next((k for k in keys if k.get("kid") == kid), None)
        if not key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token key")
        payload = jwt.decode(
            token,
            key,
            algorithms=[key.get("alg", "RS256")],
            audience=settings.jwt_aud,
            issuer=settings.jwt_iss,
            options={"verify_aud": bool(settings.jwt_aud), "verify_iss": bool(settings.jwt_iss)},
        )
        return payload
    except JWTError as exc:  # pragma: no cover - safety net
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> AuthenticatedUser:
    if credentials is None:
        # Allow guest usage; downstream can enforce if needed
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = await verify_token(credentials.credentials)
    user_id = str(payload.get("sub") or payload.get("user_id"))
    email = payload.get("email")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return AuthenticatedUser(user_id=user_id, email=email)


async def get_optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> AuthenticatedUser | None:
    if credentials is None:
        return None
    payload = await verify_token(credentials.credentials)
    user_id = str(payload.get("sub") or payload.get("user_id"))
    email = payload.get("email")
    if not user_id:
        return None
    return AuthenticatedUser(user_id=user_id, email=email)
