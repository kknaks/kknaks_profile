"""git_token DTO — 내부 계층 이동용. 암호문·원문은 DTO 에 싣지 않는다."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GitTokenDTO:
    """토큰 행의 표시용 조각 — 원문·암호문 제외. 복호는 수집기만 한다."""

    id: int
    kind: str                       # personal / company
    account: str                    # 깃 계정 id
    email: str                      # 착지 커밋의 git 신원(user.email)에 쓴다
    company_id: int | None          # kind=company 토큰의 소속. personal 은 None
    company_name: str | None        # company.name 조인 — 읽기 전용 표시
    enabled: bool                   # 끄면 수집에서 무토큰 취급. 지우지 않는다
    created_at: datetime | None
