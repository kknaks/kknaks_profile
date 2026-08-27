"""GitHub 조회 DTO — 내부 계층 이동용. DB 행이 아니라 조회 시점의 스냅샷이다.

레포 연결 모달(어드민)이 쓰는 owner 후보와 GitHub 레포 목록.
저장은 여전히 repo 표(slug 텍스트)로만 간다 — 여기 값은 DB 에 앉지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GithubOwnerDTO:
    """owner 라디오 한 항목. token_id 는 조회·저장에 딸려 가는 토큰(git_token 행)."""

    owner: str                      # medisolve-ai / kknaks
    label: str                      # 「medisolve-ai — 회사 조직」 표시문
    source: str                     # org / account
    token_id: int | None            # None — 그 회사에 연결된 토큰이 없다(무토큰 조회)


@dataclass(frozen=True)
class GithubRepoDTO:
    """GitHub 레포 한 줄 — 모달의 체크박스 목록용."""

    slug: str                       # owner/name — repo.slug 로 저장될 값
    name: str
    private: bool
    updated_at: str | None          # GitHub ISO 문자열 그대로 — 표시용
