"""site — front ↔ back 계약.

DB key `<그룹>.<필드>` (snake) 를 `site.<그룹>.<camelField>` 로 접어 내려준다 —
`home.hero_headline` → `site.home.heroHeadline`. 키가 늘어도 스키마를 안 고치게
동적 dict 로 두고, 프론트 타입이 알려진 키를 optional 로 서술한다.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from dto.site_config import SiteConfigDTO


def _camel(snake: str) -> str:
    head, *rest = snake.split("_")
    return head + "".join(part.title() for part in rest)


class SiteConfigItem(BaseModel):
    """어드민 목록의 행 — DB 행 그대로."""

    key: str
    value: Any
    note: str | None = None


class SiteConfigUpdate(BaseModel):
    """PATCH body — value·note 만, **보낸 필드만 반영**한다 (exclude_unset).

    key 는 경로로만 받고 변경할 수 없다. value 는 jsonb 그대로라 어떤 형이든 된다.
    """

    value: Any = None
    note: str | None = None


class AdminSiteConfigResponse(BaseModel):
    items: list[SiteConfigItem]

    @classmethod
    def from_dtos(cls, dtos: list[SiteConfigDTO]) -> AdminSiteConfigResponse:
        return cls(
            items=[SiteConfigItem(key=d.key, value=d.value, note=d.note) for d in dtos]
        )


class SiteResponse(BaseModel):
    site: dict[str, dict[str, Any]]

    @classmethod
    def from_dtos(cls, dtos: list[SiteConfigDTO]) -> SiteResponse:
        site: dict[str, dict[str, Any]] = {}
        for dto in dtos:
            group, _, field = dto.key.partition(".")
            if not field:  # 점 없는 키는 그대로 최상위 그룹 "site" 로
                group, field = "site", dto.key
            site.setdefault(group, {})[_camel(field)] = dto.value
        return cls(site=site)
