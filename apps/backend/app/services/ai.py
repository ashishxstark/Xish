from __future__ import annotations

import asyncio
import os
import random
import time
from typing import AsyncGenerator, Optional

import httpx

from ..config import settings


async def stream_ai_response(prompt: str, model: Optional[str] = None, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    # Placeholder streaming generator for development
    content = (
        "Thanks for trying Xish AI — I am a personal AI companion with memory,"
        " voice, and streaming responses."
    )
    # Simulate character-by-character streaming with variable delays
    for ch in content:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        yield ch


async def complete_ai_response(prompt: str, model: Optional[str] = None, temperature: float = 0.7) -> str:
    # Fallback to a complete response (no streaming)
    return (
        "Thanks for trying Xish AI — I am a personal AI companion with memory, voice, and streaming responses."
    )
