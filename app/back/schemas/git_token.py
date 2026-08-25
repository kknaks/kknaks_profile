"""git_token — front ↔ back 계약. 어드민 설정 화면이 읽고 쓴다.

토큰 원문은 **등록·교체 요청에만** 있다 — 응답에는 절대 싣지 않는다.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from dto.git_token import GitTokenDTO


class GitTokenItem(BaseModel):
    id: int
    kind: str                                                    # personal / company
    account: str                                                 # 깃 계정 id
    email: str                                                   # 착지 커밋 신원(user.email)
    company_id: int | None = Field(
        default=None, serialization_alias="companyId"            # kind=company 토큰의 소속
    )
    company_name: str | None = Field(
        default=None, serialization_alias="companyName"          # company.name 조인 — 표시용
    )
    enabled: bool                                                # 끄면 수집에서 무토큰 취급
    created_at: datetime | None = Field(
        default=None, serialization_alias="createdAt"
    )

    @classmethod
    def from_dto(cls, dto: GitTokenDTO) -> GitTokenItem:
        return cls(
            id=dto.id,
            kind=dto.kind,
            account=dto.account,
            email=dto.email,
            company_id=dto.company_id,
            company_name=dto.company_name,
            enabled=dto.enabled,
            created_at=dto.created_at,
        )


class GitTokensResponse(BaseModel):
    items: list[GitTokenItem]


class GitTokenCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    kind: str = Field(max_length=16)                             # personal / company
    account: str = Field(min_length=1, max_length=64)            # 깃 계정 id
    email: str = Field(min_length=1, max_length=255)             # 착지 커밋 신원(user.email)
    token: str = Field(min_length=1)                             # 원문 — 서버가 즉시 암호화
    company_id: int | None = Field(
        default=None, validation_alias="companyId"               # company 필수 · personal 무시
    )


class GitTokenReplace(BaseModel):
    token: str = Field(min_length=1)                             # 새 원문


class GitTokenPatch(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). 규칙 검증은 service 가."""

    model_config = ConfigDict(populate_by_name=True)

    enabled: bool | None = None
    company_id: int | None = Field(
        default=None, validation_alias="companyId"               # null = 해제. personal 은 무시
    )
