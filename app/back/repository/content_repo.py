"""content 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.content import ContentDTO
from models import Content


def _to_dto(row: Content) -> ContentDTO:
    return ContentDTO(
        id=row.id,
        profile_id=row.profile_id,
        slug=row.slug,
        title=row.title,
        summary=row.summary,
        detail_path=row.detail_path,
        youtube_id=row.youtube_id,
        duration=row.duration,
        speaker=row.speaker,
        tags=row.tags,
        published_on=row.published_on,
        visible=row.visible,
    )


class ContentRepository:
    async def list_all(self, session: AsyncSession) -> list[ContentDTO]:
        """전체 목록. published_on DESC NULLS LAST — 어드민이라 visible 로 거르지 않는다."""
        stmt = select(Content).order_by(
            Content.published_on.desc().nulls_last(), Content.id.desc()
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def list_visible(self, session: AsyncSession) -> list[ContentDTO]:
        """공개 목록. visible=true 만, published_on DESC NULLS LAST.

        이 정렬이 곧 이웃(newer/older)의 기준이다 — 정렬을 바꾸면 이웃도 바뀐다.
        """
        stmt = (
            select(Content)
            .where(Content.visible.is_(True))
            .order_by(Content.published_on.desc().nulls_last(), Content.id.desc())
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def list_slugs(self, session: AsyncSession) -> list[str]:
        """slug 만 전부 — 인박스 채번(C-NNN 최대값)이 쓴다. visible 무관."""
        return list((await session.execute(select(Content.slug))).scalars().all())

    async def get(self, session: AsyncSession, content_id: int) -> ContentDTO | None:
        row = await session.get(Content, content_id)
        return _to_dto(row) if row else None

    async def get_by_ids(
        self, session: AsyncSession, content_ids: list[int]
    ) -> dict[int, ContentDTO]:
        """id 묶음 조회 — 게이트 이력이 result.contentId 로 콘텐츠를 붙일 때 쓴다."""
        if not content_ids:
            return {}
        stmt = select(Content).where(Content.id.in_(content_ids))
        rows = (await session.execute(stmt)).scalars().all()
        return {row.id: _to_dto(row) for row in rows}

    async def get_by_slug(self, session: AsyncSession, slug: str) -> ContentDTO | None:
        row = (
            await session.execute(select(Content).where(Content.slug == slug))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ContentDTO:
        row = Content(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, content_id: int, fields: dict[str, Any]
    ) -> ContentDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Content, content_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, content_id: int) -> bool:
        row = await session.get(Content, content_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
