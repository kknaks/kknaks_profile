"""AgentClient orchestration from a Slack thread to one Markdown note."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Callable

from service.knowledge_capture import (
    EMPTY_PREVIOUS,
    CaptureArtifact,
    CaptureSession,
    CaptureSessionStore,
    CaptureStore,
    RenderContext,
    output_path,
    parse_document,
    render_document,
)
from service.knowledge_capture.source import fetch_source, find_urls

from .app import CaptureRequest


class KnowledgeCaptureRunner:
    """Slack 스레드 → 지식 노트 한 건.

    이 runner 는 **무엇을 만들지**(원문 수집·AI 호출·파싱·경로 결정·렌더)까지만 책임진다.
    **어디에 남기고 어디서 다시 읽을지**는 주입된 `store` 가 정한다 — 파일로 쓸지,
    승인 큐에 적재할지 (KDEV-WORK-012 / KDEV-DEC-013 D2).

    runner 안에 파일시스템 접근이 없어야 store 교체가 성립한다.
    """

    def __init__(
        self,
        client,
        sessions: CaptureSessionStore,
        *,
        repo_root: Path,
        provider: str,
        model: str | None,
        work_dir: str | None,
        known_stems: Callable[[], set[str]],
        allowed_groups: Callable[[], set[str]],
        store: CaptureStore,
        now: Callable[[], datetime],
        timeout_seconds: float = 600,
    ) -> None:
        self.client = client
        self.sessions = sessions
        self.repo_root = repo_root
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.known_stems = known_stems
        self.allowed_groups = allowed_groups
        self.store = store
        self.now = now
        self.timeout_seconds = timeout_seconds

    async def handle(self, request: CaptureRequest, slack_client) -> None:
        existing = await self.sessions.get(request.channel_id, request.root_thread_ts)
        placeholder = await slack_client.chat_postMessage(
            channel=request.channel_id,
            thread_ts=request.root_thread_ts,
            text="⏳ 지식 노트를 정리하고 있습니다.",
        )
        message_ts = placeholder["ts"]
        try:
            source_material = None
            urls = find_urls(request.text)
            if urls:
                source_material = (await fetch_source(urls[0])).to_dict()
            previous = await self.store.load_previous(existing) if existing else EMPTY_PREVIOUS
            prompt = self._prompt(request, source_material, previous.markdown, existing)
            options = {"cwd": self.work_dir} if self.work_dir else {}
            if existing and existing.session_id:
                options["resume"] = {"mode": "session", "session_id": existing.session_id}
            task_id = await self.client.submit(
                prompt,
                provider=self.provider,
                model=self.model,
                options=options or None,
                max_retries=2,
                metadata={
                    "source": "slack-capture",
                    "channel_id": request.channel_id,
                    "root_thread_ts": request.root_thread_ts,
                },
            )
            task = await self.client.result(task_id, timeout=self.timeout_seconds)
            if task is None or not task.result:
                raise RuntimeError(getattr(task, "error", None) or "open_kknaks returned no result")
            session_id = task.result_session_id or (existing.session_id if existing else None)
            if not session_id:
                raise RuntimeError("provider did not return a resumable session id")
            document = parse_document(task.result, known_stems=self.known_stems())
            if existing and existing.kind and document.kind != existing.kind:
                raise ValueError("follow-up cannot change capture kind")
            timestamp = self.now()
            context = RenderContext(
                repo_root=self.repo_root,
                request_id=request.request_id,
                root_thread_ts=request.root_thread_ts,
                captured_at=timestamp,
                group="study",
                allowed_groups=frozenset(self.allowed_groups()),
                output_override=previous.output_override,
            )
            path = output_path(document, context)
            rendered = render_document(document, context)
            result = await self.store.store(CaptureArtifact(
                path=path,
                rendered=rendered,
                document=document,
                replace=previous.output_override is not None,
                request=request,
            ))

            created_at = existing.created_at if existing else timestamp.isoformat(timespec="seconds")
            await self.sessions.set(CaptureSession(
                channel_id=request.channel_id,
                root_thread_ts=request.root_thread_ts,
                session_id=session_id,
                kind=document.kind,
                output_path=result.stored_ref,
                first_prompt=existing.first_prompt if existing else request.text[:200],
                created_at=created_at,
                last_seen_at=timestamp.isoformat(timespec="seconds"),
            ))
            warning = "".join(f"\n{item}" for item in result.warnings)
            await slack_client.chat_update(
                channel=request.channel_id,
                ts=message_ts,
                text=(
                    f"✅ 저장 완료: {document.title}\n"
                    f"종류: {document.kind}\n경로: `{result.location}`\n"
                    f"연결 후보: {len(document.connection_candidates)}{warning}"
                ),
            )
        except Exception as exc:
            await slack_client.chat_update(
                channel=request.channel_id,
                ts=message_ts,
                text=f"❌ 지식 수집 실패: {type(exc).__name__}",
            )
            raise

    @staticmethod
    def _prompt(request, source_material, existing_markdown, existing) -> str:
        payload = {
            "request": {
                "entrypoint": request.entrypoint,
                "text": request.text,
                "requested_kind": existing.kind if existing and existing.kind else "auto",
                "root_thread_ts": request.root_thread_ts,
            },
            "source_material": source_material,
            "existing_markdown": existing_markdown,
        }
        return (
            "Use the capture-knowledge skill. Return exactly one complete JSON object matching "
            "schema_version 1.0; no code fence or prose.\n\n"
            + json.dumps(payload, ensure_ascii=False)
        )
