"""제품(product) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ProductDTO:
    """product 행 + 역할 제목·회사 이름(2단 조인). 표현은 schemas 가 한다."""

    id: int
    career_id: int
    career_title: str
    company_name: str
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

    # 채팅 AI 노출(DEC-027 D4 · spec v0.0.8). 어드민 목록이 토글 현재값을 그리는 데 쓴다.
    chat_exposed: bool = False
