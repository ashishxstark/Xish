from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..auth import get_current_user, AuthenticatedUser
from ..db import get_db_session
from ..schemas import PreferenceUpdate

router = APIRouter()


@router.get("/preferences")
async def get_preferences(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    sql = text("SELECT preferences FROM preferences WHERE user_id = :uid LIMIT 1")
    row = (await db.execute(sql, {"uid": user.user_id})).first()
    return row[0] if row else {}


@router.post("/preferences")
async def set_preferences(
    payload: PreferenceUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    sql = text(
        """
        INSERT INTO preferences (user_id, preferences)
        VALUES (:uid, :prefs)
        ON CONFLICT (user_id) DO UPDATE SET preferences = EXCLUDED.preferences
        """
    )
    await db.execute(sql, {"uid": user.user_id, "prefs": payload.model_dump(exclude_none=True)})
    await db.commit()
    return {"ok": True}


@router.delete("/account")
async def delete_account(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    await db.execute(text("DELETE FROM memory WHERE user_id = :uid"), {"uid": user.user_id})
    await db.execute(text("DELETE FROM chat_history WHERE user_id = :uid"), {"uid": user.user_id})
    await db.execute(text("DELETE FROM preferences WHERE user_id = :uid"), {"uid": user.user_id})
    await db.commit()
    return {"ok": True}
