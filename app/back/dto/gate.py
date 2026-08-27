"""게이트(gate) DTO — 내부 계층 이동용."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from dto.queue import QueueDTO


@dataclass(frozen=True)
class GateDTO:
    """gate 행 그대로. 표현은 schemas 가 한다."""

    id: int
    queue_id: int
    stage: str                  # document / concept
    payload: dict
    status: str                 # open / approved / rejected
    commit_ref: str | None
    result: dict | None
    decided_at: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class GateWithQueue:
    """승인 화면 한 건 — 게이트 + 그 queue 행(종류·URL·메모 표시용).

    content_* 는 확정 게이트(result.contentId)의 콘텐츠 표시값 — 이력 펼침이
    「어떤 콘텐츠가 생겼는지」를 보여준다(2026-08-25). 없으면 None.
    """

    gate: GateDTO
    queue: QueueDTO
    content_title: str | None = None
    content_slug: str | None = None


@dataclass(frozen=True)
class ConceptSeed:
    """게이트 1 승인 직후 개념 생성에 필요한 것 전부 — 라우터가 백그라운드로 넘긴다.

    백그라운드 태스크는 요청 트랜잭션이 닫히기 전에 gate 행을 다시 읽지 않는다 —
    필요한 값을 여기 담아 그대로 가져간다.
    """

    queue_id: int
    kind: str
    stem: str
    body: str
    session_id: str | None
