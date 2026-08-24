"""algorithm 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.algorithm import AlgorithmDTO
from models import Algorithm


def _to_dto(row: Algorithm) -> AlgorithmDTO:
    return AlgorithmDTO(
        id=row.id,
        profile_id=row.profile_id,
        slug=row.slug,
        title=row.title,
        difficulty=row.difficulty,
        summary=row.summary,
        source_platform=row.source_platform,
        source_number=row.source_number,
        source_url=row.source_url,
        curated_in=row.curated_in,
        tags=row.tags,
        today=row.today,
        detail_path=row.detail_path,
        published_on=row.published_on,
        visible=row.visible,
    )


class AlgorithmRepository:
    async def list_all(self, session: AsyncSession) -> list[AlgorithmDTO]:
        """전체 목록. **today 행이 맨 앞**, 그 뒤 published_on DESC NULLS LAST.

        어드민이라 visible 로 거르지 않는다.
        """
        stmt = select(Algorithm).order_by(
            Algorithm.today.desc(),
            Algorithm.published_on.desc().nulls_last(),
            Algorithm.id.desc(),
        )
        rows = (await session.execute(stmt)).scalars().all()
        return [_to_dto(row) for row in rows]

    async def get(self, session: AsyncSession, algorithm_id: int) -> AlgorithmDTO | None:
        row = await session.get(Algorithm, algorithm_id)
        return _to_dto(row) if row else None

    async def get_by_slug(self, session: AsyncSession, slug: str) -> AlgorithmDTO | None:
        row = (
            await session.execute(select(Algorithm).where(Algorithm.slug == slug))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def get_today(self, session: AsyncSession) -> AlgorithmDTO | None:
        """현재 「오늘의 문제」. partial unique index 가 최대 한 행을 보장한다."""
        row = (
            await session.execute(select(Algorithm).where(Algorithm.today))
        ).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def clear_today(self, session: AsyncSession) -> None:
        """기존 today 행을 내리고 flush — 새 행을 올리기 **전에** 불러야 한다.

        같은 트랜잭션 안이라 중간 실패면 통째로 롤백된다. DB 의
        uq_algorithm_today 가 최종 방어다.
        """
        row = (
            await session.execute(select(Algorithm).where(Algorithm.today))
        ).scalar_one_or_none()
        if row is not None:
            row.today = False
            await session.flush()

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> AlgorithmDTO:
        row = Algorithm(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, algorithm_id: int, fields: dict[str, Any]
    ) -> AlgorithmDTO | None:
        """보낸 필드만 얹는다 — PATCH 시맨틱. 없는 id 면 None, 판단은 service."""
        row = await session.get(Algorithm, algorithm_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return _to_dto(row)

    async def delete(self, session: AsyncSession, algorithm_id: int) -> bool:
        row = await session.get(Algorithm, algorithm_id)
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        return True
