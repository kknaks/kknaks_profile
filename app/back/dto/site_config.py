"""site_config DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SiteConfigDTO:
    key: str            # home.hero_headline
    value: Any          # 문자열이든 구조든 jsonb 그대로
    note: str | None
