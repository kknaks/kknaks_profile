"""사이트 문구 — 2층."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from dto.site_config import SiteConfigDTO
from repository.site_config_repo import SiteConfigRepository


class SiteService:
    def __init__(self, site_repo: SiteConfigRepository) -> None:
        self._site_repo = site_repo

    async def get_all(self, session: AsyncSession) -> list[SiteConfigDTO]:
        return await self._site_repo.get_all(session)

    async def update(
        self, session: AsyncSession, key: str, fields: dict[str, Any]
    ) -> SiteConfigDTO:
        """key 행의 value·note 를 보낸 필드만 갱신한다. 없는 key 는 404."""
        dto = await self._site_repo.update(session, key, fields)
        if dto is None:
            raise NotFoundError(f"site_config key not found: {key}")
        return dto


site_service = SiteService(SiteConfigRepository())
