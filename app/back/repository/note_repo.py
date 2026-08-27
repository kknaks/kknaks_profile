"""note 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.note import NoteDTO
from models import Note


def _to_dto(row: Note) -> NoteDTO:
    return NoteDTO(
        id=row.id,
        profile_id=row.profile_id,
        slug=row.slug,
        title=row.title,
        summary=row.summary,
        detail_path=row.detail_path,
        tags=row.tags,
        published_on=row.published_on,
        visible=row.visible,
    )


class NoteRepository:
    async def list_all(self, session: AsyncSession) -> list[NoteDTO]:
        """전체 목록. published_on DESC NULLS LAST — 어드민이라 visible 로 거르지 않는다."""
        stmt = select(Note).order_by(
            Note.published_on.desc().nulls_last(), Note.id.desc()
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def list_detail_paths(self, session: AsyncSession) -> set[str]:
        """등록된 detail_path 전부 — 파일 후보 목록에서 이미 등록된 것을 빼는 데 쓴다."""
        rows = (await session.execute(select(Note.detail_path))).scalars().all()
        return set(rows)

    async def get(self, session: AsyncSession, note_id: int) -> NoteDTO | None:
        row = await session.get(Note, note_id)
        return _to_dto(row) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> NoteDTO | None:
        row = (
            await session.execute(select(Note).where(Note.slug == slug))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> NoteDTO:
        row = Note(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, note_id: int, fields: dict[str, Any]
    ) -> NoteDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Note, note_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, note_id: int) -> bool:
        row = await session.get(Note, note_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
