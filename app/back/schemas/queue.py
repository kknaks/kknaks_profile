"""queue — front ↔ back 계약. 어드민 인박스(/admin/capture) 화면이 읽고 쓴다.

행이 갖는 건 넣은 것 그대로 — 종류·URL·메모·상태·error(inbox.md Step 2 정책).
ai_session_id 는 파이프라인 내부 사정이라 계약에 없다.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from dto.queue import QueueDTO, QueueList


class AdminQueueItem(BaseModel):
    id: int
    kind: str                                                    # youtube / docs / article / blog
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")
    note: str | None = None
    status: str                                                  # queued / processing / review / done / failed
    error: str | None = None
    created_at: datetime = Field(serialization_alias="createdAt")

    @classmethod
    def from_dto(cls, dto: QueueDTO) -> AdminQueueItem:
        return cls(
            id=dto.id,
            kind=dto.kind,
            source_url=dto.source_url,
            note=dto.note,
            status=dto.status,
            error=dto.error,
            created_at=dto.created_at,
        )


class AdminQueueResponse(BaseModel):
    items: list[AdminQueueItem]
    counts: dict[str, int]

    @classmethod
    def from_list(cls, result: QueueList) -> AdminQueueResponse:
        return cls(
            items=[AdminQueueItem.from_dto(d) for d in result.items],
            counts=result.counts,
        )


class QueueCreate(BaseModel):
    """모달의 넣기 — kind 는 사람이 고른 것(분류를 AI 에 안 맡긴다, 케이스 1).

    kind 검증(youtube/docs/article/blog)과 URL 비었나 검사는 service 가 한다 —
    여기는 모양만 받는다.
    """

    model_config = ConfigDict(populate_by_name=True)

    kind: str = Field(min_length=1, max_length=16)
    source_url: str | None = Field(
        default=None, max_length=512, validation_alias="sourceUrl"
    )
    note: str | None = None
