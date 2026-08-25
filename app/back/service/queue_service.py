"""인박스(queue) — 2층. 캡처 → queue 행 생성 + 목록 + 재시도 (inbox.md Step 1·2).

v1 은 여기까지다 — 비동기 처리(Step 3)·게이트(gate 행)는 아직 없다.
그래서 retry 는 상태 전이만 한다: failed → queued, error 비움.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError, ValidationError
from dto.queue import QueueDTO, QueueList
from repository.queue_repo import QueueRepository

# 모달이 보내는 종류 — book·session 은 버튼만이라 안 온다(케이스 1 v1 구멍).
_CAPTURE_KINDS = frozenset({"youtube", "docs", "article", "blog"})

# 목록 counts 의 키 순서 — 파이프라인 진행 순 + failed.
_STATUSES = ("queued", "processing", "review", "done", "failed")


class QueueService:
    def __init__(self, queue_repo: QueueRepository) -> None:
        self._queue_repo = queue_repo

    async def create(
        self, session: AsyncSession, kind: str, source_url: str | None, note: str | None
    ) -> QueueDTO:
        """행 생성(queued). 검증은 「비었나」 정도만 — fallback 안 쌓는다(inbox.md).

        중복 검사 없음 — 같은 링크를 또 넣으면 또 돈다(erd §미결 4 는 미결로 유지).
        """
        if kind not in _CAPTURE_KINDS:
            raise ValidationError(
                f"kind 는 {'/'.join(sorted(_CAPTURE_KINDS))} 중 하나여야 합니다: {kind}"
            )
        url = (source_url or "").strip()
        if not url:
            raise ValidationError("URL 이 비었습니다")
        return await self._queue_repo.create(
            session,
            {"kind": kind, "source_url": url, "note": (note or "").strip() or None},
        )

    async def list_queue(self, session: AsyncSession) -> QueueList:
        """최신순 목록 + 상태별 counts. counts 는 목록과 같은 스냅샷에서 센다."""
        items = await self._queue_repo.list_all(session)
        counts = {status: 0 for status in _STATUSES}
        for item in items:
            counts[item.status] = counts.get(item.status, 0) + 1
        return QueueList(items=items, counts=counts)

    async def retry(self, session: AsyncSession, queue_id: int) -> QueueDTO:
        """failed → queued 로 되돌리고 error 를 비운다.

        처리 자체는 라우터가 백그라운드로 다시 건다(inbox_pipeline.process) —
        부분 재개 없이 그 단계 파이프라인의 처음부터 돈다(inbox.md Step 3).
        """
        existing = await self._queue_repo.get(session, queue_id)
        if existing is None:
            raise NotFoundError(f"queue item not found: {queue_id}")
        if existing.status != "failed":
            raise ValidationError(
                f"failed 상태만 재시도할 수 있습니다: {existing.status}"
            )
        dto = await self._queue_repo.update(
            session, queue_id, {"status": "queued", "error": None}
        )
        assert dto is not None  # 방금 존재를 확인했다
        return dto


queue_service = QueueService(QueueRepository())
