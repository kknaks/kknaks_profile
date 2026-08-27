"""게이트(gate) — 1층. 게이트 목록 + 승인·거절·푸시 재시도 (케이스 1).

- GET  /api/admin/gates                 — open + 승인됨·푸시 실패분 (기존 계약)
- GET  /api/admin/gates?scope=all       — 닫힌 게이트 포함 전체 (done 행 펼침 이력,
                                          2026-08-25 개정 — 파라미터 추가로 확장)
- GET  /api/admin/gates/{id}            — 상세(payload 포함)
- POST /api/admin/gates/{id}/approve    — 다듬은 payload 동봉 → 착지·commit·push
                                          (문서는 자동 착지라 실질 concept 전용)
- POST /api/admin/gates/{id}/reject     — rejected 기록, queue 는 done
- POST /api/admin/gates/{id}/retry-push — approved + commit_ref NULL 만

문서(게이트 1)의 착지 확정이 개념 보강안 생성으로 이어진다 — 자동 착지는
inbox 파이프라인이 곧바로 잇고, 여기서는 푸시 실패분 retry-push 성공이 잇는다.
요청 트랜잭션이 닫힌 뒤에 돌도록 FastAPI BackgroundTasks 를 쓴다.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.gate import AdminGateItem, AdminGateResponse, GateApproveRequest
from service.gate_service import gate_service
from service.inbox_service import inbox_pipeline

admin_router = APIRouter(
    prefix="/api/admin/gates",
    tags=["gate"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminGateResponse, response_model_by_alias=True)
async def list_gates(
    scope: Literal["pending", "all"] = "pending",
    db: AsyncSession = Depends(get_db),
) -> AdminGateResponse:
    """기본(scope=pending)은 기존 계약 그대로 — open + 푸시 실패분.
    scope=all 은 닫힌 게이트까지 전부(프론트가 queue 별 이력을 그린다)."""
    items = (
        await gate_service.list_all(db)
        if scope == "all"
        else await gate_service.list_pending(db)
    )
    return AdminGateResponse(items=[AdminGateItem.from_pair(p) for p in items])


@admin_router.get(
    "/{gate_id}", response_model=AdminGateItem, response_model_by_alias=True
)
async def get_gate(gate_id: int, db: AsyncSession = Depends(get_db)) -> AdminGateItem:
    pair = await gate_service.get(db, gate_id)
    return AdminGateItem.from_pair(pair)


@admin_router.post(
    "/{gate_id}/approve", response_model=AdminGateItem, response_model_by_alias=True
)
async def approve_gate(
    gate_id: int,
    body: GateApproveRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AdminGateItem:
    gate, queue, seed, push_error = await gate_service.approve(
        db, gate_id, body.payload
    )
    if seed is not None:
        # 백그라운드 태스크가 teardown commit 보다 먼저 돌 수 있다(queue_router 와 동일)
        # — 확정 상태를 커밋한 뒤에 개념 생성을 건다.
        await db.commit()
        background.add_task(inbox_pipeline.run_concept, seed)
    return AdminGateItem.from_dto(gate, queue, push_error)


@admin_router.post(
    "/{gate_id}/reject", response_model=AdminGateItem, response_model_by_alias=True
)
async def reject_gate(
    gate_id: int, db: AsyncSession = Depends(get_db)
) -> AdminGateItem:
    gate, queue = await gate_service.reject(db, gate_id)
    return AdminGateItem.from_dto(gate, queue)


@admin_router.post(
    "/{gate_id}/retry-push", response_model=AdminGateItem, response_model_by_alias=True
)
async def retry_gate_push(
    gate_id: int,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AdminGateItem:
    gate, queue, seed, push_error = await gate_service.retry_push(db, gate_id)
    if seed is not None:
        await db.commit()  # approve 와 같은 이유
        background.add_task(inbox_pipeline.run_concept, seed)
    return AdminGateItem.from_dto(gate, queue, push_error)
