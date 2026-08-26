"""persona — 1층. 역할별 persona md(DB 파생) 재렌더 트리거.

- POST /api/admin/persona/render — 전체 재렌더를 백그라운드로 걸고 즉시 202

스케줄(매일 KST 08:10)이 정상 경로이고, 이 엔드포인트는 나중 확인용 수동 트리거다.
공개 라우터 없음 — persona md 는 파일로 있고 사이트 표면은 없다.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import require_admin
from service.persona_service import persona_service

admin_router = APIRouter(
    prefix="/api/admin/persona",
    tags=["persona"],
    dependencies=[Depends(require_admin)],
)


@admin_router.post("/render", status_code=202)
async def render_now() -> dict:
    """전체 재렌더를 백그라운드로 걸고 바로 돌아온다."""
    started = persona_service.start()
    return {"ok": True, "started": started}  # started=false — 이미 돌고 있다
