"""콘텐츠(content) — 2층. 영상 + 교안. 원장은 para/resources/youtube/.

md 가 먼저, DB 가 나중(케이스 2 와 같은 방향) — detail_path 가 가리키는 md 가
리포에 실존해야 등록이 선다. DB 는 본문을 복사하지 않고 경로로 가리키기만 한다
(정보는 DB, 상세는 md).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.content import ContentDTO
from repository.content_repo import ContentRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
# profile_id 는 입력받지 않는다 — 서버가 첫 profile 로 채운다.
_NOT_NULLABLE = frozenset({"slug", "title", "youtube_id", "detail_path", "visible"})

# 리포 루트 기준 — 콘텐츠 md 원장이 사는 곳.
_CONTENTS_DIR = ("para", "resources", "youtube")


def _require_detail_path(detail_path: str) -> None:
    """detail_path 검사 — para/resources/youtube/ 하위 실존 파일이 아니면 422.

    경로 조립이라 탈출을 먼저 막는다 — `..`·역슬래시·절대경로는 접두 검사를
    통과해도 원장 밖을 가리킬 수 있다.
    """
    if ".." in detail_path or "\\" in detail_path or detail_path.startswith("/"):
        raise ValidationError(f"detail_path 에 경로 탈출 문자를 쓸 수 없습니다: {detail_path}")
    prefix = "/".join(_CONTENTS_DIR) + "/"
    if not detail_path.startswith(prefix):
        raise ValidationError(f"detail_path 는 {prefix} 하위여야 합니다: {detail_path}")
    target = Path(get_settings().repo_root) / detail_path
    if not target.is_file():
        raise ValidationError(
            "detail_path 가 가리키는 md 가 없습니다 — 원장이 먼저입니다"
        )


class ContentService:
    def __init__(
        self, content_repo: ContentRepository, profile_repo: ProfileRepository
    ) -> None:
        self._content_repo = content_repo
        self._profile_repo = profile_repo

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._content_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_contents(self, session: AsyncSession) -> list[ContentDTO]:
        return await self._content_repo.list_all(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ContentDTO:
        _require_detail_path(fields["detail_path"])
        await self._require_free_slug(session, fields["slug"])

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found — seed_profile 을 먼저 돌린다")
        fields["profile_id"] = profile.id
        return await self._content_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, content_id: int, fields: dict[str, Any]
    ) -> ContentDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "detail_path" in fields:
            # 경로를 바꾸는 것도 새 md 를 가리키는 일 — 같은 검사를 거친다.
            _require_detail_path(fields["detail_path"])
        if "slug" in fields:
            await self._require_free_slug(session, fields["slug"], exclude_id=content_id)
        dto = await self._content_repo.update(session, content_id, fields)
        if dto is None:
            raise NotFoundError(f"content not found: {content_id}")
        return dto

    async def delete(self, session: AsyncSession, content_id: int) -> None:
        if not await self._content_repo.delete(session, content_id):
            raise NotFoundError(f"content not found: {content_id}")


content_service = ContentService(ContentRepository(), ProfileRepository())
