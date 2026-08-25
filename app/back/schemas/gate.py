"""gate — front ↔ back 계약. 승인 대기(/admin/approvals) 화면이 읽고 쓴다.

payload 의 모양은 stage 가 정한다(erd §gate — DDL 이 아니라 코드가 정한다):
- document: {stem, body, meta?} — meta 는 youtube 만(카드 메타)
- concept:  {concepts: [{mode, area, stem, body, diff}]}

승인은 다듬은 payload 를 그대로 동봉한다 — 그게 저장되고 그대로 착지한다.
게이트 2 는 체크된 항목만 concepts 에 담아 보낸다(체크 해제 = 안 올림).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from dto.gate import GateDTO, GateWithQueue
from dto.queue import QueueDTO


class AdminGateItem(BaseModel):
    id: int
    queue_id: int = Field(serialization_alias="queueId")
    stage: str                                                   # document / concept
    status: str                                                  # open / approved / rejected
    # queue 행에서 온 표시값 — 종류·URL·메모
    kind: str
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")
    note: str | None = None
    # 목록 한 줄 제목 — payload 에서 파생(meta.title → stem → 종류)
    title: str
    payload: dict
    commit_ref: str | None = Field(default=None, serialization_alias="commitRef")
    result: dict | None = None
    # 확정 게이트의 생성 콘텐츠 표시값 — result.contentId 조인(scope=all 이력용).
    # 필드 추가라 기존 계약은 안 깨진다(없으면 null).
    content_title: str | None = Field(default=None, serialization_alias="contentTitle")
    content_slug: str | None = Field(default=None, serialization_alias="contentSlug")
    decided_at: datetime | None = Field(default=None, serialization_alias="decidedAt")
    created_at: datetime = Field(serialization_alias="createdAt")
    # 이번 요청의 푸시 실패 사유 — DB 에 없고 응답에만 실린다(재시도 안내용)
    push_error: str | None = Field(default=None, serialization_alias="pushError")

    @classmethod
    def from_dto(
        cls,
        gate: GateDTO,
        queue: QueueDTO,
        push_error: str | None = None,
        *,
        content_title: str | None = None,
        content_slug: str | None = None,
    ) -> AdminGateItem:
        return cls(
            id=gate.id,
            queue_id=gate.queue_id,
            stage=gate.stage,
            status=gate.status,
            kind=queue.kind,
            source_url=queue.source_url,
            note=queue.note,
            title=_title_of(gate),
            payload=gate.payload,
            commit_ref=gate.commit_ref,
            result=gate.result,
            content_title=content_title,
            content_slug=content_slug,
            decided_at=gate.decided_at,
            created_at=gate.created_at,
            push_error=push_error,
        )

    @classmethod
    def from_pair(cls, pair: GateWithQueue) -> AdminGateItem:
        return cls.from_dto(
            pair.gate,
            pair.queue,
            content_title=pair.content_title,
            content_slug=pair.content_slug,
        )


def _title_of(gate: GateDTO) -> str:
    payload = gate.payload or {}
    meta = payload.get("meta")
    if isinstance(meta, dict) and str(meta.get("title", "")).strip():
        return str(meta["title"]).strip()
    if str(payload.get("stem", "")).strip():
        return str(payload["stem"]).strip()
    return gate.stage


class AdminGateResponse(BaseModel):
    items: list[AdminGateItem]


class GateApproveRequest(BaseModel):
    """승인 — 화면에서 다듬은 payload 그대로. 모양 검증은 service 가 stage 로 한다."""

    model_config = ConfigDict(populate_by_name=True)

    payload: dict
