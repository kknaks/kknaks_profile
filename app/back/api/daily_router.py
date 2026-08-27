"""daily(하루 요약) — 1층. 어드민 재요약 트리거.

- POST /api/admin/daily/{date}/summarize — 그 날짜만 백그라운드 재요약, 즉시 202

창 제한 없음 — 과거 날짜도 허용한다(자동 판은 최근 7일 창만, 소급은 여기와
백필 스크립트 몫). 결과는 달력 재조회(dailyStatus·dailySummary)로 본다.
daily 조회 전용 GET 이 없다 — 달력 응답이 daily 를 함께 나른다.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends

from api.deps import require_admin
from service.summarize_service import summarize_service

admin_router = APIRouter(
    prefix="/api/admin/daily",
    tags=["daily"],
    dependencies=[Depends(require_admin)],
)


@admin_router.post("/{day}/summarize", status_code=202)
async def summarize_day(day: date) -> dict:
    """재요약을 백그라운드로 걸고 바로 돌아온다 — 몇 초 뒤 달력 재조회로 확인."""
    summarize_service.start_date(day)
    return {"ok": True, "started": True}
