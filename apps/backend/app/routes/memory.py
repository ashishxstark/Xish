from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..auth import get_current_user, AuthenticatedUser
from ..db import get_db_session
from ..schemas import MemoryItem, MemoryQuery

router = APIRouter()

MEMORY_LIMIT = 100


@router.get("/")
async def list_memory(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    rows = (await db.execute(text("SELECT key, value FROM memory WHERE user_id = :uid ORDER BY created_at DESC"), {"uid": user.user_id})).all()
    return [{"key": r.key, "value": r.value} for r in rows]


@router.post("/")
async def upsert_memory(
    item: MemoryItem,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    await db.execute(
        text(
            """
            INSERT INTO memory (user_id, key, value)
            VALUES (:uid, :key, :value)
            ON CONFLICT (user_id, key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
            """
        ),
        {"uid": user.user_id, "key": item.key, "value": item.value},
    )
    # Enforce limit by deleting oldest
    await db.execute(
        text(
            """
            DELETE FROM memory WHERE user_id = :uid AND key NOT IN (
                SELECT key FROM memory WHERE user_id = :uid ORDER BY updated_at DESC, created_at DESC LIMIT :limit
            )
            """
        ),
        {"uid": user.user_id, "limit": MEMORY_LIMIT},
    )
    await db.commit()
    return {"ok": True}


@router.delete("/")
async def delete_memory(
    item: MemoryQuery,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    await db.execute(text("DELETE FROM memory WHERE user_id = :uid AND key = :key"), {"uid": user.user_id, "key": item.key})
    await db.commit()
    return {"ok": True}


@router.delete("/all")
async def clear_memory(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    await db.execute(text("DELETE FROM memory WHERE user_id = :uid"), {"uid": user.user_id})
    await db.commit()
    return {"ok": True}
