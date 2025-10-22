from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    stream: bool = True
    temperature: float = 0.7
    language: Optional[str] = None


class ChatResponse(BaseModel):
    message_id: str
    content: str
    created_at: datetime
    model: str


class PreferenceUpdate(BaseModel):
    theme: Optional[Literal["light", "dark", "system"]] = None
    tts_voice: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None


class MemoryItem(BaseModel):
    key: str = Field(min_length=1, max_length=64)
    value: str = Field(min_length=1, max_length=2048)


class MemoryQuery(BaseModel):
    key: str


class ApiError(BaseModel):
    detail: str
