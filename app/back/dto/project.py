"""개인 프로젝트(project) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ProjectDTO:
    """project 행 그대로. 표현은 schemas 가 한다."""

    id: int
    profile_id: int
    slug: str
    title: str
    summary: str | None
    detail_path: str | None
    category: str | None
    status: str | None
    started_on: date | None
    stack: list[str] | None
    thumbnail: str | None
    links: dict[str, Any] | None
    visible: bool
