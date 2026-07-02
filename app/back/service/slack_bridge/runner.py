"""AgentClient orchestration from a Slack thread to one Markdown note."""

from __future__ import annotations

import inspect
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Awaitable, Callable

from service.knowledge_capture import (
    CaptureSession,
    CaptureSessionStore,
    RenderContext,
    atomic_write,
    output_path,
    parse_document,
    render_document,
)
from service.knowledge_capture.source import fetch_source, find_urls

from .app import CaptureRequest


class KnowledgeCaptureRunner:
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
        reload_data: Callable[[], bool | Awaitable[bool]],
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
        self.reload_data = reload_data
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
            existing_markdown = None
            if existing and existing.output_path:
                path = (self.repo_root / existing.output_path).resolve()
                if path.is_relative_to(self.repo_root.resolve()) and path.is_file():
                    existing_markdown = path.read_text(encoding="utf-8")
            prompt = self._prompt(request, source_material, existing_markdown, existing)
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
            relative_override = Path(existing.output_path) if existing and existing.output_path else None
            context = RenderContext(
                repo_root=self.repo_root,
                request_id=request.request_id,
                root_thread_ts=request.root_thread_ts,
                captured_at=timestamp,
                group="study",
                allowed_groups=frozenset(self.allowed_groups()),
                output_override=relative_override,
            )
            path = output_path(document, context)
            rendered = render_document(document, context)
            atomic_write(path, rendered, replace=relative_override is not None)
            reload_result = self.reload_data()
            reload_ok = await reload_result if inspect.isawaitable(reload_result) else reload_result
            relative = path.relative_to(self.repo_root.resolve()).as_posix()
            created_at = existing.created_at if existing else timestamp.isoformat(timespec="seconds")
            await self.sessions.set(CaptureSession(
                channel_id=request.channel_id,
                root_thread_ts=request.root_thread_ts,
                session_id=session_id,
                kind=document.kind,
                output_path=relative,
                first_prompt=existing.first_prompt if existing else request.text[:200],
                created_at=created_at,
                last_seen_at=timestamp.isoformat(timespec="seconds"),
            ))
            warning = "" if reload_ok else "\n⚠ 파일은 저장됐지만 그래프 reload가 거부됐습니다."
            await slack_client.chat_update(
                channel=request.channel_id,
                ts=message_ts,
                text=(
                    f"✅ 저장 완료: {document.title}\n"
                    f"종류: {document.kind}\n경로: `{relative}`\n"
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
