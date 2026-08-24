"""개인 프로젝트(project) — 2층.

케이스 2 (case_flow.md): **md 가 먼저, DB 가 나중.**
`para/projects/summer-star/<slug>/` 디렉토리가 없으면 등록이 막힌다 —
스캐폴딩이 원천이고 DB 행은 그 뒤에 선다. showcase.md 내용까지는 검사하지
않는다(미결 — 디렉토리 존재까지만).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.project import ProjectDTO
from repository.profile_repo import ProfileRepository
from repository.project_repo import ProjectRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
# profile_id 는 입력받지 않는다 — 서버가 첫 profile 로 채운다.
_NOT_NULLABLE = frozenset({"slug", "title", "visible"})

# 리포 루트 기준 — 프로젝트 md 원장이 사는 곳.
_PROJECTS_DIR = ("para", "projects", "summer-star")


def _require_project_dir(slug: str) -> None:
    """slug 디렉토리 검사 — 없으면 422. 경로 조립이라 탈출 문자를 먼저 막는다."""
    if "/" in slug or "\\" in slug or ".." in slug:
        raise ValidationError(f"slug 에 경로 문자를 쓸 수 없습니다: {slug}")
    root = Path(get_settings().repo_root).joinpath(*_PROJECTS_DIR)
    if not (root / slug).is_dir():
        raise ValidationError(
            "프로젝트 디렉토리가 없습니다 — 스캐폴딩이 먼저입니다 (케이스 2)"
        )


def _default_detail_path(slug: str) -> str:
    """detail_path 를 안 보내면 showcase.md 를 가리킨다 (케이스 2)."""
    return "/".join((*_PROJECTS_DIR, slug, "showcase.md"))


class ProjectService:
    def __init__(
        self, project_repo: ProjectRepository, profile_repo: ProfileRepository
    ) -> None:
        self._project_repo = project_repo
        self._profile_repo = profile_repo

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._project_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_projects(self, session: AsyncSession) -> list[ProjectDTO]:
        return await self._project_repo.list_all(session)

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> ProjectDTO:
        slug = fields["slug"]
        _require_project_dir(slug)
        await self._require_free_slug(session, slug)

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found — seed_profile 을 먼저 돌린다")
        fields["profile_id"] = profile.id

        if fields.get("detail_path") is None:
            fields["detail_path"] = _default_detail_path(slug)
        return await self._project_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, project_id: int, fields: dict[str, Any]
    ) -> ProjectDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "slug" in fields:
            # slug 를 바꾸는 것도 새 디렉토리를 가리키는 일 — 같은 검사를 거친다.
            _require_project_dir(fields["slug"])
            await self._require_free_slug(session, fields["slug"], exclude_id=project_id)
        dto = await self._project_repo.update(session, project_id, fields)
        if dto is None:
            raise NotFoundError(f"project not found: {project_id}")
        return dto

    async def delete(self, session: AsyncSession, project_id: int) -> None:
        if not await self._project_repo.delete(session, project_id):
            raise NotFoundError(f"project not found: {project_id}")


project_service = ProjectService(ProjectRepository(), ProfileRepository())
