from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from ..auth import get_current_user, AuthenticatedUser

router = APIRouter()


@router.post("/stt")
async def speech_to_text(
    audio: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_current_user),
):
    # Stub: Echo back a fake transcription
    # In production, integrate with native speech services or cloud APIs
    return {"text": "[transcribed] Hello from Xish AI"}


@router.post("/tts")
async def text_to_speech(
    payload: dict,
    user: AuthenticatedUser = Depends(get_current_user),
):
    text = str(payload.get("text") or "")
    if not text:
        return JSONResponse({"detail": "text required"}, status_code=400)

    async def audio_stream():  # type: ignore[no-untyped-def]
        # Stub: yield silent audio bytes placeholder
        yield b""  # Replace with actual encoded audio chunks

    return StreamingResponse(audio_stream(), media_type="audio/mpeg")
