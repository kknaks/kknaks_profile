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

    # 채팅 AI 노출(DEC-027 D4) — `visible` 과 다른 축이다. 어드민 목록이 토글 현재값을
    # 그리는 데 쓴다.
    chat_exposed: bool = False


@dataclass(frozen=True)
class PublicProject:
    """공개 /projects 한 건 — 행 + detail_path md 전문.

    상세 페이지가 별도 API 없이 목록 응답의 body 를 쓴다 — 항목이 적어
    전문을 목록에 실어도 된다(정보는 DB, 상세는 md).
    """

    dto: ProjectDTO
    body: str | None
