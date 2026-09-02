"""project 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.project import ProjectDTO
from models import Project


def _to_dto(row: Project) -> ProjectDTO:
    return ProjectDTO(
        id=row.id,
        profile_id=row.profile_id,
        slug=row.slug,
        title=row.title,
        summary=row.summary,
        detail_path=row.detail_path,
        category=row.category,
        status=row.status,
        started_on=row.started_on,
        stack=row.stack,
        thumbnail=row.thumbnail,
        links=row.links,
        visible=row.visible,
        chat_exposed=row.chat_exposed,
    )


class ProjectRepository:
    async def list_all(self, session: AsyncSession) -> list[ProjectDTO]:
        """전체 목록. started_on DESC NULLS LAST — 어드민이라 visible 로 거르지 않는다."""
        stmt = select(Project).order_by(
            Project.started_on.desc().nulls_last(), Project.id.desc()
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def get(self, session: AsyncSession, project_id: int) -> ProjectDTO | None:
        row = await session.get(Project, project_id)
        return _to_dto(row) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> ProjectDTO | None:
        row = (
            await session.execute(select(Project).where(Project.slug == slug))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProjectDTO:
        row = Project(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, project_id: int, fields: dict[str, Any]
    ) -> ProjectDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Project, project_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, project_id: int) -> bool:
        row = await session.get(Project, project_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
