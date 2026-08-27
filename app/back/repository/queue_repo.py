"""queue 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.queue import QueueDTO
from models import Queue


def _to_dto(row: Queue) -> QueueDTO:
    return QueueDTO(
        id=row.id,
        kind=row.kind,
        source_url=row.source_url,
        note=row.note,
        status=row.status,
        error=row.error,
        ai_session_id=row.ai_session_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class QueueRepository:
    async def list_all(self, session: AsyncSession) -> list[QueueDTO]:
        """전체 목록. 최신이 위 — created_at DESC, 동시각이면 id DESC."""
        stmt = select(Queue).order_by(Queue.created_at.desc(), Queue.id.desc())
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def get(self, session: AsyncSession, queue_id: int) -> QueueDTO | None:
        row = await session.get(Queue, queue_id)
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> QueueDTO:
        row = Queue(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, queue_id: int, fields: dict[str, Any]
    ) -> QueueDTO | None:
        """보낸 필드만 얹는다. 없는 id 면 None, 판단은 service."""
        row = await session.get(Queue, queue_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        # updated_at 은 서버(onupdate=now())가 채운다 — flush 뒤 만료된 값을
        # 동기 lazy-load 로 읽으면 MissingGreenlet 이라 명시적으로 다시 읽는다.
        await session.refresh(row)
        return _to_dto(row)
