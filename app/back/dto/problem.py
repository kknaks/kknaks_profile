"""해결한 문제(problem) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProblemDTO:
    """problem 행 + 역할 제목·회사 이름(2단 조인) + 제품 제목(선택 조인).

    표현은 schemas 가 한다. product_title 은 product_id 가 NULL 이면 None.
    """

    id: int
    career_id: int
    career_title: str
    company_name: str
    product_id: int | None
    product_title: str | None
    title: str
    body: str | None
    display_order: int
