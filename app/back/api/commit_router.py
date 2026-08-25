"""커밋 히스토리 — 1층. 어드민 조회 전용(/admin/commits 화면).

- GET /api/admin/commits/calendar — 월 달력: 총 건수 · KST 날짜별 건수 · 레포 칩
- GET /api/admin/commits          — 목록: authored_at DESC 50행 페이지네이션

수정·삭제 엔드포인트 없음 — 커밋은 수집기(케이스 6·7) 소유다.
message 원문은 여기서만 내린다 — 공개 표면(/api/activity) 금지.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.commit import AdminCommitCalendarResponse, AdminCommitsResponse
from service.commit_service import commit_service

admin_router = APIRouter(
    prefix="/api/admin/commits",
    tags=["commit"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get(
    "/calendar",
    response_model=AdminCommitCalendarResponse,
    response_model_by_alias=True,
)
async def get_calendar(
    year: int = Query(ge=2000, le=2100),
    month: int = Query(ge=1, le=12),
    repo_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> AdminCommitCalendarResponse:
    """total·repos 는 그 달 전체(필터 무관), days 만 repo_id 필터를 탄다."""
    dto = await commit_service.get_calendar(db, year, month, repo_id)
    return AdminCommitCalendarResponse.from_dto(dto)


@admin_router.get("", response_model=AdminCommitsResponse, response_model_by_alias=True)
async def list_commits(
    year: int = Query(ge=2000, le=2100),
    month: int = Query(ge=1, le=12),
    repo_id: int | None = Query(default=None),
    day: int | None = Query(default=None, ge=1, le=31),  # KST 날짜 필터
    page: int = Query(default=1, ge=1),
    db: AsyncSession = Depends(get_db),
) -> AdminCommitsResponse:
    dto = await commit_service.list_commits(db, year, month, repo_id, day, page)
    return AdminCommitsResponse.from_dto(dto)
