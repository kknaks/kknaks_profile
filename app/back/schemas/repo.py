"""repo — front ↔ back 계약. 어드민 레포 화면(/admin/repos)이 읽고 쓴다.

productTitle · projectTitle 은 컬럼이 아니라 선택 조인의 읽기 전용 표시값 —
수정은 productId / projectId 로 한다(둘 중 정확히 하나, DB CHECK).
lastFetchedAt · lastError 는 수집기의 상태 — 화면은 읽기만 한다.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from dto.repo import RepoDTO


class AdminRepoItem(BaseModel):
    id: int
    product_id: int | None = Field(default=None, serialization_alias="productId")
    project_id: int | None = Field(default=None, serialization_alias="projectId")
    product_title: str | None = Field(default=None, serialization_alias="productTitle")
    project_title: str | None = Field(default=None, serialization_alias="projectTitle")
    slug: str                                                    # owner/name
    role: str | None = None                                      # spec / app / infra
    git_token_id: int | None = Field(default=None, serialization_alias="gitTokenId")
    enabled: bool
    last_fetched_at: datetime | None = Field(
        default=None, serialization_alias="lastFetchedAt"
    )
    last_error: str | None = Field(default=None, serialization_alias="lastError")

    @classmethod
    def from_dto(cls, dto: RepoDTO) -> AdminRepoItem:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            project_id=dto.project_id,
            product_title=dto.product_title,
            project_title=dto.project_title,
            slug=dto.slug,
            role=dto.role,
            git_token_id=dto.git_token_id,
            enabled=dto.enabled,
            last_fetched_at=dto.last_fetched_at,
            last_error=dto.last_error,
        )


class AdminReposResponse(BaseModel):
    items: list[AdminRepoItem]


class RepoCreate(BaseModel):
    """등록 — slug 형식(owner/name)·부모 「정확히 하나」 검증은 service 가 한다."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=3, max_length=160)
    role: str | None = Field(default=None, max_length=32)
    git_token_id: int | None = Field(default=None, validation_alias="gitTokenId")
    product_id: int | None = Field(default=None, validation_alias="productId")
    project_id: int | None = Field(default=None, validation_alias="projectId")
    enabled: bool = True


class RepoUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=3, max_length=160)
    role: str | None = Field(default=None, max_length=32)
    git_token_id: int | None = Field(default=None, validation_alias="gitTokenId")  # null = 무토큰
    product_id: int | None = Field(default=None, validation_alias="productId")
    project_id: int | None = Field(default=None, validation_alias="projectId")
    enabled: bool | None = None
