"""SQLAlchemy 2.0 async 엔진 · 세션 · Base (auth-01 — DB화 토대).

지금까지 persona 콘텐츠는 md 파일 in-memory 로딩이었고, 여기서부터 관계형 DB 를
도입한다. 첫 테이블은 users(관리자 인증). 드라이버는 psycopg3(async 네이티브 지원) —
URL `postgresql+psycopg://` 그대로 create_async_engine 에 넘긴다.

엔진은 lazy singleton — import 시점이 아니라 첫 사용 시 생성해 테스트/마이그레이션에서
DATABASE_URL monkeypatch 를 존중한다. (Alembic 은 마이그레이션 CLI 라 동기 엔진을
따로 쓴다 — alembic/env.py 참고.)
"""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """모든 ORM 모델의 공통 부모 — Alembic 이 metadata 로 스키마를 잡는다."""


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """async 엔진 singleton. pool_pre_ping 으로 홈서버 재기동 후 stale 커넥션 회피."""
    import config

    return create_async_engine(config.database_url(), pool_pre_ping=True)


@lru_cache(maxsize=1)
def _sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=get_engine(), autoflush=False, expire_on_commit=False
    )


async def get_db():
    """FastAPI 의존성 — 요청 스코프 async 세션. 커밋은 라우터가 명시적으로."""
    async with _sessionmaker()() as db:
        yield db
