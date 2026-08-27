"""daily 표 접근 — 3층. 하루 요약의 upsert(날짜당 1행) + 범위 조회."""

from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from dto.daily import DailyDTO
from models import Daily


class DailyRepository:
    async def upsert_summary(
        self, session: AsyncSession, day: date, summary: str
    ) -> None:
        """성공 착지 — summary 를 채우고 error 를 비운다(repo.last_error 규약)."""
        stmt = pg_insert(Daily).values(date=day, summary=summary, error=None)
        stmt = stmt.on_conflict_do_update(
            index_elements=["date"],
            set_={"summary": summary, "error": None, "updated_at": func.now()},
        )
        await session.execute(stmt)

    async def upsert_error(
        self, session: AsyncSession, day: date, error: str
    ) -> None:
        """실패 착지 — error 만 채운다. 기존 summary 는 건드리지 않는다."""
        stmt = pg_insert(Daily).values(date=day, error=error)
        stmt = stmt.on_conflict_do_update(
            index_elements=["date"],
            set_={"error": error, "updated_at": func.now()},
        )
        await session.execute(stmt)

    async def map_range(
        self, session: AsyncSession, since: date, until: date | None = None
    ) -> dict[date, DailyDTO]:
        """[since, until) 의 daily 행 — 날짜 키 dict. until=None 이면 상한 없음."""
        stmt = select(
            Daily.date, Daily.summary, Daily.error, Daily.updated_at
        ).where(Daily.date >= since)
        if until is not None:
            stmt = stmt.where(Daily.date < until)
        rows = (await session.execute(stmt)).all()
        return {
            r[0]: DailyDTO(date=r[0], summary=r[1], error=r[2], updated_at=r[3])
            for r in rows
        }


daily_repo = DailyRepository()
