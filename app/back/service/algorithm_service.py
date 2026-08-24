"""알고리즘(algorithm) — 2층.

원장은 para/resources/algorithms/ 의 md 파일이다 — detail_path 가 실존
파일을 가리키지 않으면 등록·수정이 422 로 막힌다(md 가 먼저, DB 가 나중).

「오늘의 문제」는 하나뿐이다. today=true 로 올리는 요청은 **한 트랜잭션에서**
기존 today 행을 먼저 내리고 이 행을 올린다 — DB 의 partial unique index
(uq_algorithm_today) 가 최종 방어다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.exceptions import ConflictError, NotFoundError, ValidationError
from dto.algorithm import AlgorithmDTO
from repository.algorithm_repo import AlgorithmRepository
from repository.profile_repo import ProfileRepository

# DB 에서 NOT NULL — null 로 지우려는 요청은 여기서 막는다.
# profile_id 는 입력받지 않는다 — 서버가 첫 profile 로 채운다.
_NOT_NULLABLE = frozenset(
    {"slug", "title", "difficulty", "source_platform", "today", "detail_path", "visible"}
)

_DIFFICULTIES = frozenset({"easy", "medium", "hard"})

# 리포 루트 기준 — 알고리즘 md 원장이 사는 곳.
_ALGORITHMS_DIR = ("para", "resources", "algorithms")


def _require_difficulty(value: str) -> None:
    if value not in _DIFFICULTIES:
        raise ValidationError(
            f"difficulty 는 easy·medium·hard 중 하나여야 합니다: {value}"
        )


def _require_detail_file(detail_path: str) -> None:
    """detail_path 검사 — para/resources/algorithms/ 하위 실존 파일이어야 한다.

    경로 조립이라 탈출을 먼저 막는다 — `..`·역슬래시·절대경로는 422.
    """
    prefix = "/".join(_ALGORITHMS_DIR) + "/"
    if "\\" in detail_path or ".." in detail_path or detail_path.startswith("/"):
        raise ValidationError(f"detail_path 에 경로 탈출 문자를 쓸 수 없습니다: {detail_path}")
    if not detail_path.startswith(prefix):
        raise ValidationError(
            f"detail_path 는 {prefix} 하위여야 합니다: {detail_path}"
        )
    full = Path(get_settings().repo_root) / detail_path
    if not full.is_file():
        raise ValidationError(
            f"detail_path 가 가리키는 md 가 없습니다 — 원장이 먼저입니다: {detail_path}"
        )


class AlgorithmService:
    def __init__(
        self, algorithm_repo: AlgorithmRepository, profile_repo: ProfileRepository
    ) -> None:
        self._algorithm_repo = algorithm_repo
        self._profile_repo = profile_repo

    async def _require_free_slug(
        self, session: AsyncSession, slug: str, exclude_id: int | None = None
    ) -> None:
        existing = await self._algorithm_repo.get_by_slug(session, slug)
        if existing and existing.id != exclude_id:
            raise ConflictError(f"slug already exists: {slug}")

    async def list_algorithms(self, session: AsyncSession) -> list[AlgorithmDTO]:
        return await self._algorithm_repo.list_all(session)

    async def create(
        self, session: AsyncSession, fields: dict[str, Any]
    ) -> AlgorithmDTO:
        _require_difficulty(fields["difficulty"])
        _require_detail_file(fields["detail_path"])
        await self._require_free_slug(session, fields["slug"])

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise NotFoundError("profile not found — seed_profile 을 먼저 돌린다")
        fields["profile_id"] = profile.id

        if fields.get("today"):
            # 새 행을 today 로 올리려면 기존 today 를 같은 트랜잭션에서 먼저 내린다.
            await self._algorithm_repo.clear_today(session)
        return await self._algorithm_repo.create(session, fields)

    async def update(
        self, session: AsyncSession, algorithm_id: int, fields: dict[str, Any]
    ) -> AlgorithmDTO:
        for name in _NOT_NULLABLE & fields.keys():
            if fields[name] is None:
                raise ValidationError(f"{name} cannot be null")
        if "difficulty" in fields:
            _require_difficulty(fields["difficulty"])
        if "detail_path" in fields:
            _require_detail_file(fields["detail_path"])
        if "slug" in fields:
            await self._require_free_slug(
                session, fields["slug"], exclude_id=algorithm_id
            )
        if fields.get("today"):
            current = await self._algorithm_repo.get_today(session)
            if current is not None and current.id != algorithm_id:
                # 이전 「오늘의 문제」를 먼저 내린다 — 같은 트랜잭션이라 중간
                # 실패면 통째로 롤백. DB partial unique 가 최종 방어다.
                await self._algorithm_repo.clear_today(session)
        dto = await self._algorithm_repo.update(session, algorithm_id, fields)
        if dto is None:
            raise NotFoundError(f"algorithm not found: {algorithm_id}")
        return dto

    async def delete(self, session: AsyncSession, algorithm_id: int) -> None:
        if not await self._algorithm_repo.delete(session, algorithm_id):
            raise NotFoundError(f"algorithm not found: {algorithm_id}")


algorithm_service = AlgorithmService(AlgorithmRepository(), ProfileRepository())
