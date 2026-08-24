"""DB 엔진 · 세션 — SQLAlchemy 2.0 async.

트랜잭션 경계는 요청 하나다. `get_db` 가 요청 끝에서 commit 하고 예외면
rollback 한다 — service · repository 는 flush 까지만 하고 commit 을 모른다.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import get_settings

_settings = get_settings()

engine: AsyncEngine = create_async_engine(
    _settings.database_url,
    echo=_settings.db_echo,
    pool_pre_ping=True,  # 홈서버 재부팅 등으로 끊긴 커넥션을 재사용하지 않게
)

# expire_on_commit=False — commit 뒤에도 객체 속성을 재조회 없이 읽는다.
# async 에서는 lazy-load 재조회가 MissingGreenlet 으로 터지므로 사실상 필수.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI 의존성 — 요청당 세션 하나, 성공하면 commit · 예외면 rollback."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
