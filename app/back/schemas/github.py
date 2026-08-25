"""GitHub 조회 — front ↔ back 계약. 레포 연결 모달이 읽는다.

DB 행이 아니라 조회 시점의 GitHub 스냅샷 — 저장 계약은 여전히 repo(RepoCreate)다.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from dto.github import GithubOwnerDTO, GithubRepoDTO


class GithubOwnerItem(BaseModel):
    owner: str                                                   # medisolve-ai / kknaks
    label: str                                                   # 「… — 회사 조직」 표시문
    source: str                                                  # org / account
    token_id: int | None = Field(
        default=None, serialization_alias="tokenId"              # 조회·저장에 딸려 가는 토큰
    )

    @classmethod
    def from_dto(cls, dto: GithubOwnerDTO) -> GithubOwnerItem:
        return cls(
            owner=dto.owner, label=dto.label, source=dto.source, token_id=dto.token_id
        )


class GithubOwnersResponse(BaseModel):
    """빈 items — 그 스코프에 쓸 토큰이 없다. 안내는 프론트 문구가 맡는다."""

    items: list[GithubOwnerItem]


class GithubRepoItem(BaseModel):
    slug: str                                                    # owner/name — repo.slug 로 저장
    name: str
    private: bool
    updated_at: str | None = Field(
        default=None, serialization_alias="updatedAt"            # GitHub ISO 그대로 — 표시용
    )

    @classmethod
    def from_dto(cls, dto: GithubRepoDTO) -> GithubRepoItem:
        return cls(
            slug=dto.slug,
            name=dto.name,
            private=dto.private,
            updated_at=dto.updated_at,
        )


class GithubReposResponse(BaseModel):
    items: list[GithubRepoItem]
