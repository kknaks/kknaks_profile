"""site_config 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.site_config import SiteConfigDTO
from models import SiteConfig


class SiteConfigRepository:
    async def get_all(self, session: AsyncSession) -> list[SiteConfigDTO]:
        rows = (
            (await session.execute(select(SiteConfig).order_by(SiteConfig.key)))
            .scalars()
            .all()
        )
        return [SiteConfigDTO(key=r.key, value=r.value, note=r.note) for r in rows]

    async def update(
        self, session: AsyncSession, key: str, fields: dict[str, Any]
    ) -> SiteConfigDTO | None:
        """key 행에 `fields`(value·note) 만 얹는다. 없는 key 면 None — 판단은 service."""
        row = (
            await session.execute(select(SiteConfig).where(SiteConfig.key == key))
        ).scalar_one_or_none()
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        return SiteConfigDTO(key=row.key, value=row.value, note=row.note)
