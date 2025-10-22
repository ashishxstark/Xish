from __future__ import annotations

from datetime import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..auth import get_current_user, get_optional_user, AuthenticatedUser
from ..db import get_db_session
from ..schemas import ChatRequest, ChatResponse
from ..services.ai import stream_ai_response, complete_ai_response
from ..services.ratelimit import rate_limit_allow

router = APIRouter()


@router.post("/")
async def chat(
    payload: ChatRequest,
    user: AuthenticatedUser | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db_session),
):
    model = payload.model or "gpt-4o-mini"

    # Best-effort rate limiting per user
    allowed, retry_after = rate_limit_allow(user.user_id if user else "guest")
    if not allowed:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Retry after {retry_after} seconds")

    if payload.stream:
        async def event_stream():  # type: ignore[no-untyped-def]
            async for chunk in stream_ai_response(payload.message, model=model, temperature=payload.temperature):
                yield f"data: {chunk}\n\n"
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        content = await complete_ai_response(payload.message, model=model, temperature=payload.temperature)
        message_id = str(uuid.uuid4())
        await db.execute(
            text(
                """
                INSERT INTO chat_history (id, user_id, role, content, model)
                VALUES (:id, :uid, 'assistant', :content, :model)
                """
            ),
            {"id": message_id, "uid": (user.user_id if user else None), "content": content, "model": model},
        )
        await db.commit()
        return JSONResponse(
            ChatResponse(
                message_id=message_id, content=content, created_at=datetime.utcnow(), model=model
            ).model_dump()
        )
