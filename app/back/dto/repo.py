"""레포(repo) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RepoDTO:
    """repo 행 + 부모 이름(선택 조인). 표현은 schemas 가 한다.

    부모는 product / project 둘 중 정확히 하나다(DB CHECK ck_repo_one_parent) —
    product_title · project_title 중 하나만 채워진다.
    """

    id: int
    product_id: int | None
    project_id: int | None
    product_title: str | None
    project_title: str | None
    slug: str                       # owner/name
    role: str | None                # spec / app / infra
    git_token_id: int | None        # 수집 토큰(git_token 행). None 무토큰
    enabled: bool
    last_fetched_at: datetime | None
    last_error: str | None
