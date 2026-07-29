"""Slack 스레드 → 승인 큐 (KDEV-WORK-014 P2 / KDEV-SPEC-007 S-1).

`KnowledgeCaptureRunner` 를 대체한다. 둘의 차이는 **어디서 멈추는가**다.

    종전:  Slack → 수집 → AI 가 노트 전문 작성 → 렌더 → 파일 쓰기 → origin/main 커밋
    현행:  Slack → 큐 적재 → 수집 + 요약 제출 → **접수 회신** → (수확) → 검토 대기

노트 전문은 route 승인 **뒤에** 쓴다(WORK-015). 목적지를 정하기 전에 본문을 만들면
폐기될 자료의 노트까지 쓰게 되고, 무엇보다 **사람이 보기 전에 결과가 확정된다.**

이 클래스는 파일시스템도 git 도 건드리지 않는다. 그것이 이 work 의 요점이다.

**회신은 요약을 기다리지 않는다** (KDEV-WORK-016 P2). 접수 시점에 확실한 것은
"큐에 들어갔고 준비가 시작됐다"까지다. 검토 카드가 열렸다고 미리 말하면, 요약이
실패했을 때 Slack 에는 성공이 남고 화면에는 실패가 남는다.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any, Callable

from service.knowledge_capture.session import CaptureSession, CaptureSessionStore
from service.knowledge_capture.source import find_urls

from .flow import start_preparation
from .intake import intake
from .prepare import PREPARABLE_STATUSES, Fetcher, Summarizer

logger = logging.getLogger("kknaks-back.pipeline.slack")


#: Slack 은 링크를 `<url|표시텍스트>` 또는 `<url>` 로 감싸 보낸다.
_SLACK_LINK_RE = re.compile(r"<(https?://[^|>]+)(?:\|[^>]*)?>")


def unwrap_slack_links(text: str) -> str:
    """Slack 링크 표기를 순수 URL 로 되돌린다.

    벗기지 않으면 두 곳이 망가진다.
    - URL 에 `|표시텍스트` 가 붙어 영상 ID 파싱이 실패한다 → 유튜브가 `blog` 로
      판정돼 파이프라인 정의를 못 찾고 **게이트가 안 열린다.**
    - 메모에서 URL 만 걷어내면 `< >`, `|텍스트>` 같은 찌꺼기가 남는다.
    """
    return _SLACK_LINK_RE.sub(r"\1", text or "")


def _strip_urls(text: str, urls: list[str]) -> str:
    """메모에서 URL 을 걷어낸다 — 링크는 `source_url` 이 이미 들고 있다."""
    for url in urls:
        text = text.replace(url, " ")
    return " ".join(text.split()).strip()


class QueueIntakeRunner:
    """Slack 이벤트 하나를 큐 항목 하나로 만든다.

    `CaptureRunner` Protocol(`handle(request, slack_client)`)을 그대로 만족하므로
    Bolt 핸들러 조립부(`create_capture_app`)는 손대지 않는다.
    """

    def __init__(
        self,
        *,
        session_factory: Callable[[], Any],
        sessions: CaptureSessionStore,
        fetch: Fetcher,
        summarize: Summarizer,
        now: Callable[[], datetime],
    ) -> None:
        self.session_factory = session_factory
        self.sessions = sessions
        self.fetch = fetch
        self.summarize = summarize
        self.now = now

    async def handle(self, request, slack_client) -> None:
        placeholder = await slack_client.chat_postMessage(
            channel=request.channel_id,
            thread_ts=request.root_thread_ts,
            text="⏳ 큐에 넣는 중입니다.",
        )
        message_ts = placeholder["ts"]
        try:
            existing = await self.sessions.get(request.channel_id, request.root_thread_ts)
            if existing is not None and existing.item_id is not None:
                text = await self._append_note(existing.item_id, request.text)
            else:
                text, item_id = await self._create(request)
                await self._remember(request, existing, item_id)
            await slack_client.chat_update(
                channel=request.channel_id, ts=message_ts, text=text
            )
        except Exception as exc:
            logger.exception("큐 적재 실패 request=%s", request.request_id)
            await slack_client.chat_update(
                channel=request.channel_id,
                ts=message_ts,
                text=f"❌ 큐 적재 실패: {type(exc).__name__}",
            )
            raise

    async def _create(self, request) -> tuple[str, int | None]:
        text = unwrap_slack_links(request.text)
        urls = find_urls(text)
        source_url = urls[0] if urls else None
        note = _strip_urls(text, urls) or None

        async with self.session_factory() as db:
            result = await intake(
                db,
                source_url=source_url,
                note=note,
                channel="slack",
                submitted_by=request.user_id,
            )
            await db.commit()

            if result.outcome == "duplicate_published":
                # 자동으로 막지 않는다 — 같은 자료의 재정리가 정당한 경우가 있다(S-4).
                return (
                    f"↩︎ 이미 발행된 자료입니다 (항목 #{result.existing_item_id}).\n"
                    "새로 정리하려면 관리자 큐 화면에서 진행해 주세요.",
                    None,
                )
            if result.outcome == "joined":
                return (
                    f"↩︎ 이미 큐에 있는 자료라 항목 #{result.item_id} 에 메모를 붙였습니다.",
                    result.item_id,
                )

            prepared = await start_preparation(
                db,
                result.item_id,
                fetch=self.fetch,
                summarize=self.summarize,
            )
            await db.commit()

        if prepared.running:
            return (
                f"✅ 접수됨 — 준비 중 (항목 #{result.item_id})\n"
                "요약이 끝나면 관리자 큐 화면에 검토 카드가 열립니다. "
                "**아직 레포에는 아무것도 쓰이지 않았습니다.**",
                result.item_id,
            )
        return (
            f"⚠️ 접수는 됐지만 준비에 실패했습니다 (항목 #{result.item_id}).\n"
            f"사유: `{prepared.error_code}`\n"
            "이 스레드에 내용을 요약해 남겨 주시면 그걸로 다시 시도합니다.",
            result.item_id,
        )

    async def _append_note(self, item_id: int, text: str) -> str:
        """스레드 후속 발언을 항목 메모로 흘려보낸다.

        준비가 실패한 항목이면 그대로 재시도까지 간다 — 메모가 원문을 대체할 수 있어서,
        사람이 한 줄 남기는 것만으로 막힌 항목이 풀린다(SPEC-007 S-3).
        """
        from core.models import QueueItem

        from .intake import _merge_note

        text = unwrap_slack_links(text)
        addition = _strip_urls(text, find_urls(text))
        async with self.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            if item is None or item.deleted_at is not None:
                return "이 스레드의 항목을 찾을 수 없습니다 (삭제되었을 수 있습니다)."
            item.note = _merge_note(item.note, addition)
            retryable = item.status == "prepare_failed"
            await db.commit()

            if not retryable:
                return f"📝 항목 #{item_id} 메모에 반영했습니다 (상태: {item.status})."

            prepared = await start_preparation(
                db,
                item_id,
                fetch=self.fetch,
                summarize=self.summarize,
            )
            await db.commit()

        if prepared.running:
            return f"✅ 메모로 준비를 다시 시작했습니다 — 준비 중 (항목 #{item_id})."
        return (
            f"⚠️ 메모를 반영했지만 준비가 다시 실패했습니다 (항목 #{item_id}).\n"
            f"사유: `{prepared.error_code}`"
        )

    async def _remember(self, request, existing, item_id: int | None) -> None:
        stamp = self.now().isoformat(timespec="seconds")
        await self.sessions.set(
            CaptureSession(
                channel_id=request.channel_id,
                root_thread_ts=request.root_thread_ts,
                session_id=existing.session_id if existing else None,
                kind=None,
                output_path=None,
                first_prompt=(existing.first_prompt if existing else request.text[:200]),
                created_at=(existing.created_at if existing else stamp),
                last_seen_at=stamp,
                item_id=item_id,
            )
        )


__all__ = ["QueueIntakeRunner", "PREPARABLE_STATUSES"]
