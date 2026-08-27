"""gate 표 접근 — 3층."""

from __future__ import annotations

from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.gate import GateDTO, GateWithQueue
from models import Gate, Queue
from repository.queue_repo import _to_dto as _queue_to_dto


def _to_dto(row: Gate) -> GateDTO:
    return GateDTO(
        id=row.id,
        queue_id=row.queue_id,
        stage=row.stage,
        payload=row.payload,
        status=row.status,
        commit_ref=row.commit_ref,
        result=row.result,
        decided_at=row.decided_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class GateRepository:
    async def list_pending(self, session: AsyncSession) -> list[GateWithQueue]:
        """승인 화면 목록 — open + 「approved 인데 commit_ref 없음」(푸시 실패분).

        result 까지 NULL 이어야 푸시 실패분이다 — 착지할 것이 없어(개념 0건 승인)
        커밋 없이 종결된 게이트는 result 만 있고 commit_ref 가 없다.
        오래 기다린 것이 위 — created_at ASC.
        """
        stmt = (
            select(Gate, Queue)
            .join(Queue, Gate.queue_id == Queue.id)
            .where(
                or_(
                    Gate.status == "open",
                    (Gate.status == "approved")
                    & Gate.commit_ref.is_(None)
                    & Gate.result.is_(None),
                )
            )
            .order_by(Gate.created_at.asc(), Gate.id.asc())
        )
        rows = (await session.execute(stmt)).all()
        return [
            GateWithQueue(gate=_to_dto(gate), queue=_queue_to_dto(queue))
            for gate, queue in rows
        ]

    async def list_all(self, session: AsyncSession) -> list[GateWithQueue]:
        """전체 목록 — 닫힌 게이트(approved·rejected)도 포함한다.

        done 행 펼침 이력(2026-08-25 개정)용. 프론트가 queue 별로 묶으므로
        정렬은 list_pending 과 같은 created_at ASC 하나면 된다.
        """
        stmt = (
            select(Gate, Queue)
            .join(Queue, Gate.queue_id == Queue.id)
            .order_by(Gate.created_at.asc(), Gate.id.asc())
        )
        rows = (await session.execute(stmt)).all()
        return [
            GateWithQueue(gate=_to_dto(gate), queue=_queue_to_dto(queue))
            for gate, queue in rows
        ]

    async def get(self, session: AsyncSession, gate_id: int) -> GateDTO | None:
        row = await session.get(Gate, gate_id)
        return _to_dto(row) if row else None

    async def get_with_queue(
        self, session: AsyncSession, gate_id: int
    ) -> GateWithQueue | None:
        stmt = (
            select(Gate, Queue)
            .join(Queue, Gate.queue_id == Queue.id)
            .where(Gate.id == gate_id)
        )
        row = (await session.execute(stmt)).first()
        if row is None:
            return None
        gate, queue = row
        return GateWithQueue(gate=_to_dto(gate), queue=_queue_to_dto(queue))

    async def get_by_queue_stage(
        self, session: AsyncSession, queue_id: int, stage: str
    ) -> GateDTO | None:
        stmt = select(Gate).where(Gate.queue_id == queue_id, Gate.stage == stage)
        row = (await session.execute(stmt)).scalar_one_or_none()
        return _to_dto(row) if row else None

    async def create(self, session: AsyncSession, fields: dict[str, Any]) -> GateDTO:
        row = Gate(**fields)
        session.add(row)
        await session.flush()
        return _to_dto(row)

    async def update(
        self, session: AsyncSession, gate_id: int, fields: dict[str, Any]
    ) -> GateDTO | None:
        """보낸 필드만 얹는다. 없는 id 면 None, 판단은 service."""
        row = await session.get(Gate, gate_id)
        if row is None:
            return None
        for name, value in fields.items():
            setattr(row, name, value)
        await session.flush()
        await session.refresh(row)  # updated_at 은 서버가 채운다 — queue_repo 와 같은 이유
        return _to_dto(row)
