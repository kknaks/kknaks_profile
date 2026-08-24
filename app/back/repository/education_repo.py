"""education 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.education import EducationDTO
from models import Education


def _to_dto(row: Education) -> EducationDTO:
    return EducationDTO(
        id=row.id,
        profile_id=row.profile_id,
        org=row.org,
        title=row.title,
        location=row.location,
        started_on=row.started_on,
        ended_on=row.ended_on,
        summary=row.summary,
        detail_path=row.detail_path,
        stack=row.stack,
    )


class EducationRepository:
    async def list_all(self, session: AsyncSession) -> list[EducationDTO]:
        """started_on DESC — 파생 정렬(erd: display_order 는 컬럼이 아니다)."""
        stmt = select(Education).order_by(
            Education.started_on.desc(), Education.id.desc()
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def get(self, session: AsyncSession, education_id: int) -> EducationDTO | None:
        row = await session.get(Education, education_id)
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> EducationDTO:
        row = Education(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, education_id: int, fields: dict[str, Any]
    ) -> EducationDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Education, education_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, education_id: int) -> bool:
        row = await session.get(Education, education_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
