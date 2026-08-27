"""profile — front ↔ back 계약. 프론트 lib/types.ts 의 Profile 과 1:1 이다.

신원·연락·스택만 — 표면 문구는 site_config(/api/site)가 내려준다.
프론트가 camelCase 라 serialization alias 로 맞춘다.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dto.profile import ProfileDTO


class ProfileOut(BaseModel):
    id: int

    handle: str
    name: str
    role: str
    years: str | None = None
    location: str | None = None
    focus: str | None = None
    avatar_url: str | None = Field(default=None, serialization_alias="avatarUrl")

    email: str
    github: str | None = None
    linkedin: str | None = None

    stack: list[str] = []

    @classmethod
    def from_dto(cls, dto: ProfileDTO) -> ProfileOut:
        return cls(
            id=dto.id,
            handle=dto.handle,
            name=dto.name,
            role=dto.role,
            years=dto.years,
            location=dto.location,
            focus=dto.focus,
            avatar_url=dto.avatar_url,
            email=dto.email,
            github=dto.github,
            linkedin=dto.linkedin,
            stack=dto.stack or [],
        )


class ProfileUpdate(BaseModel):
    """PATCH body — 모든 필드 optional. **보낸 필드만 반영**한다 (exclude_unset).

    안 보낸 것과 null 을 보낸 것은 다르다. id·created_at·updated_at 은 받지
    않는다(필드가 없으므로 무시된다). 프론트가 camelCase(avatarUrl)로 보내므로
    validation alias + populate_by_name 으로 양쪽 다 받는다.
    """

    model_config = ConfigDict(populate_by_name=True)

    handle: str | None = None
    name: str | None = None
    role: str | None = None
    years: str | None = None
    location: str | None = None
    focus: str | None = None
    avatar_url: str | None = Field(default=None, validation_alias="avatarUrl")

    email: str | None = None
    github: str | None = None
    linkedin: str | None = None

    stack: list[str] | None = None


class ProfileResponse(BaseModel):
    profile: ProfileOut
