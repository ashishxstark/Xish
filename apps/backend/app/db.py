from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

from .config import settings


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata


_engine: AsyncEngine | None = None
_Session: async_sessionmaker[AsyncSession] | None = None


def get_database_url() -> str:
    if settings.database_url:
        return settings.database_url.get_secret_value()
    # Fallback to a local Postgres URL placeholder
    return "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(get_database_url(), pool_pre_ping=True)
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _Session
    if _Session is None:
        _Session = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _Session


@asynccontextmanager
async def lifespan(app):  # type: ignore[no-untyped-def]
    # Placeholder for running migrations or ensuring schema
    yield
    engine = get_engine()
    await engine.dispose()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session
