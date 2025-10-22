from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

from .config import settings
from .db import lifespan
from .routes import chat, memory, user, health, voice


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/health", tags=["health"]) 
    app.include_router(user.router, prefix="/user", tags=["user"]) 
    app.include_router(memory.router, prefix="/memory", tags=["memory"]) 
    app.include_router(chat.router, prefix="/chat", tags=["chat"]) 
    app.include_router(voice.router, prefix="/voice", tags=["voice"]) 

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):  # type: ignore[no-untyped-def]
        if settings.debug:
            raise exc
        return JSONResponse({"detail": "Internal server error"}, status_code=500)

    return app


app = create_app()
