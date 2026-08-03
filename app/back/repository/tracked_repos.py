"""`tracked_repos` DB 접근 (KDEV-WORK-018 P2 / KDEV-DEC-017).

**이 파일 밖에서 `TrackedRepo` 를 `select()` 하지 않는다.** ORM 객체도 나가지 않는다 —
전부 `TrackedRepoDTO` 로 바꿔 돌려준다.

종전에는 `service/jobs/repo_registry.enabled_repos()` 가 ORM 리스트를 돌려주고
`service/jobs/repos.sync_all()` 이 그 객체의 `last_fetched_at`·`last_error` 를 직접
대입했다. ORM 이 도메인 코드로 새면 lazy load·세션 수명·`expire_on_commit` 이 같이
새고, service 가 DB 세션의 사정을 알아야 하는 상태로 되돌아간다. 그래서 상태 기록도
`mark_synced`/`mark_failed` 로 여기 들어와 있다.

도메인 규칙은 두지 않는다 — 무엇이 유효한 `product_slug` 인지, 어느 career 로 보낼지는
`service/products/` 가 정한다.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import TrackedRepo
from service.products.dto import RepoCreate, RepoPatch, TrackedRepoDTO


def _to_dto(row: TrackedRepo) -> TrackedRepoDTO:
    """ORM → DTO. **경계가 여기 하나뿐이라 변환도 하나뿐이다.**"""
    return TrackedRepoDTO(
        id=row.id,
        slug=row.slug,
        type=row.type,
        detail=row.detail,
        product_slug=row.product_slug,
        account=row.account,
        enabled=row.enabled,
        path_rules=row.path_rules,
        last_fetched_at=row.last_fetched_at,
        last_error=row.last_error,
    )


async def list_all(db: AsyncSession) -> list[TrackedRepoDTO]:
    """전체. 관리 화면이 쓴다 — 꺼진 것도 보여야 다시 켤 수 있다."""
    rows = (await db.scalars(select(TrackedRepo).order_by(TrackedRepo.slug))).all()
    return [_to_dto(r) for r in rows]


async def list_enabled(db: AsyncSession) -> list[TrackedRepoDTO]:
    """조사 대상. `enabled` 가 꺼진 것은 클론을 남긴 채 fetch 만 멈춘다.

    잔디 조사의 유일한 입구다(`service/pipeline/collect_git.py`). 여기서 걸러지므로
    화면에서 토글을 끄면 다음 조사부터 빠진다 — 별도 필터가 필요 없다.
    """
    rows = (
        await db.scalars(
            select(TrackedRepo)
            .where(TrackedRepo.enabled.is_(True))
            .order_by(TrackedRepo.slug)
        )
    ).all()
    return [_to_dto(r) for r in rows]


async def get_by_id(db: AsyncSession, repo_id: int) -> TrackedRepoDTO | None:
    row = await db.get(TrackedRepo, repo_id)
    return _to_dto(row) if row else None


async def get_by_slug(db: AsyncSession, slug: str) -> TrackedRepoDTO | None:
    row = (
        await db.scalars(select(TrackedRepo).where(TrackedRepo.slug == slug))
    ).first()
    return _to_dto(row) if row else None


async def existing_slugs(db: AsyncSession) -> set[str]:
    """중복 판정용. 행 전체를 만들지 않는다 — 시드가 매번 부른다."""
    return set((await db.scalars(select(TrackedRepo.slug))).all())


async def create(db: AsyncSession, payload: RepoCreate) -> TrackedRepoDTO:
    row = TrackedRepo(
        slug=payload.slug,
        type=payload.type,
        detail=payload.detail,
        product_slug=payload.product_slug,
        account=payload.account,
        enabled=payload.enabled,
    )
    db.add(row)
    await db.flush()
    return _to_dto(row)


async def patch(
    db: AsyncSession, repo_id: int, payload: RepoPatch
) -> TrackedRepoDTO | None:
    """부분 수정. **전달된 필드만 반영한다.**

    `exclude_unset=True` 가 핵심이다 — 그것이 없으면 `detail` 을 안 보낸 요청이
    `detail=None` 으로 해석돼 company 행의 career 귀속이 조용히 지워진다.
    """
    row = await db.get(TrackedRepo, repo_id)
    if row is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    return _to_dto(row)


async def mark_synced(db: AsyncSession, repo_id: int, at: datetime) -> None:
    """클론·fetch 성공. **`last_error` 를 비운다** — 남아 있으면 지금 막혀 있다는 뜻이라,
    지우지 않으면 고쳐진 뒤에도 화면이 계속 빨갛다."""
    row = await db.get(TrackedRepo, repo_id)
    if row is None:
        return
    row.last_fetched_at = at
    row.last_error = None
    await db.flush()


async def mark_failed(db: AsyncSession, repo_id: int, code: str, message: str) -> None:
    """클론·fetch 실패. `last_fetched_at` 은 **건드리지 않는다** — 마지막으로 성공한
    시점이 언제인지가 실패 사유만큼 중요하다."""
    row = await db.get(TrackedRepo, repo_id)
    if row is None:
        return
    row.last_error = f"{code}: {message}"
    await db.flush()
