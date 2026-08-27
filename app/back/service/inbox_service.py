"""인박스 비동기 처리기 — 케이스 1 의 사람 눈에 안 보이는 구간.

라우터가 FastAPI 백그라운드 태스크로 `process(queue_id)` 를 건다(생성 직후·재시도).
요청 트랜잭션과 분리된 자기 세션(SessionLocal)으로 돈다 — 상태 전이마다 짧게 열고
닫아서, 수십 초짜리 AI 대기가 커넥션을 물고 있지 않게 한다.

흐름(케이스 1, 2026-08-25 개정 — 문서 게이트 없음, 자동 착지):
processing → 가져오기 → AI 초안 → **서버 검증**(양식 절 · 실행 실패 흔적)
→ 자동 착지(md → commit·push → content 행, gate(document) 는 auto-approved 기록)
→ 곧바로 개념 생성(resume) → gate(concept) open → review.
개념 게이트 승인/거절은 사람 몫(gate_service) → done.

실패는 어느 단계든 `failed` + error 한 줄 — 검증 탈락도 착지하지 않고 여기로
빠진다. 재시도는 그 단계 파이프라인의 처음부터 다시 돈다. 문서가 이미 착지 확정
(approved + commit_ref)이면 재시도는 개념 단계로 간다 — 착지·커밋된 문서를 다시
만들 수는 없다(UNIQUE(queue_id, stage)). 문서 푸시 실패(비 dry-run)는 failed 가
아니라 approved + commit_ref NULL — 화면의 [재시도](gate retry-push)가 집는다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from config import get_settings
from core.db import SessionLocal
from dto.gate import ConceptSeed, GateDTO
from dto.queue import QueueDTO
from repository.content_repo import ContentRepository
from repository.gate_repo import GateRepository
from repository.queue_repo import QueueRepository
from service import ai_service
from service.fetch_service import fetch_source

logger = logging.getLogger(__name__)

# youtube 채번 — 파일명 stem(`C-026-…`)과 content.slug(`C-026`) 양쪽에서 번호를 뽑는다.
_C_NUMBER = re.compile(r"^C-(\d+)")


def normalize_stem(stem: str) -> str:
    """codex 가 stem 에 `.md` 접미를 붙여 내면 착지 파일이 `….md.md` 가 된다
    (실측: C-031). 확장자는 착지가 붙인다 — stem 에서는 뗀다."""
    stem = (stem or "").strip()
    while stem.lower().endswith(".md"):
        stem = stem[: -len(".md")].rstrip()
    return stem


class DocumentInvalid(Exception):
    """서버 검증 탈락 — 착지하지 않고 queue failed + error 로 빠진다."""


# codex 실행 실패 흔적 — output 스키마만 맞춘 「작업 중단 사유문」이 초안으로 통과된
# 실사고(2026-08-25, queue 6·7) 이후 본문에서 걸러낸다. 일반 기술 본문에 나올 법한
# 낱말(sandbox 등)은 안 넣는다 — 오탐으로 정상 초안을 떨구지 않기 위해서다.
_FAILURE_TRACES = (
    "작업 중단",
    "작업을 중단",
    "읽을 수 없었",
    "bwrap:",
    "No permissions to create a new namespace",
)


def validate_document_body(body: str) -> None:
    """문서 초안 서버 검증(케이스 1 개정) — 실패는 DocumentInvalid(사유 명시).

    - 실행 실패 흔적이 본문에 보이면 실패 — 스키마만 맞은 사유문 차단
    - H1 이 없으면 실패 — 템플릿 머리(제목) 위반
    - `## 요지` 를 포함해 `## ` 절이 3개 미만이면 실패 — 템플릿 핵심 절 위반
      (네 종류 템플릿 전부 `## 요지` + 본문 절 3개 이상이다 — templates/resources/)
    """
    text = body or ""
    for trace in _FAILURE_TRACES:
        if trace in text:
            raise DocumentInvalid(f"본문에 실행 실패 흔적: {trace!r} — 재시도 필요")
    lines = text.splitlines()
    if not any(line.startswith("# ") for line in lines):
        raise DocumentInvalid("본문에 H1(`# 제목`) 이 없음 — 템플릿 양식 위반")
    h2 = [line.strip() for line in lines if line.startswith("## ")]
    if not any(h.startswith("## 요지") for h in h2):
        raise DocumentInvalid("본문에 `## 요지` 절이 없음 — 템플릿 양식 위반")
    if len(h2) < 3:
        raise DocumentInvalid(
            f"본문 `## ` 절이 {len(h2)}개 — 템플릿 핵심 절(3개 이상) 미달"
        )


class InboxPipeline:
    def __init__(
        self,
        queue_repo: QueueRepository,
        gate_repo: GateRepository,
        content_repo: ContentRepository,
    ) -> None:
        self._queue_repo = queue_repo
        self._gate_repo = gate_repo
        self._content_repo = content_repo

    async def _set_status(self, queue_id: int, fields: dict) -> None:
        async with SessionLocal() as session:
            await self._queue_repo.update(session, queue_id, fields)
            await session.commit()

    async def _fail(self, queue_id: int, error: str) -> None:
        one_line = " ".join(error.split()) or "알 수 없는 실패"
        await self._set_status(queue_id, {"status": "failed", "error": one_line[:500]})

    async def process(self, queue_id: int) -> None:
        """생성·재시도의 진입점 — 어느 단계를 돌지 gate 상태로 정한다."""
        async with SessionLocal() as session:
            queue = await self._queue_repo.get(session, queue_id)
            doc_gate = await self._gate_repo.get_by_queue_stage(
                session, queue_id, "document"
            )
        if queue is None:
            logger.warning("inbox process: queue %s 없음", queue_id)
            return

        try:
            if doc_gate and doc_gate.status == "approved" and doc_gate.commit_ref:
                # 문서는 착지 확정됐다 — 개념 단계 실패의 재시도다
                payload = doc_gate.payload
                seed = ConceptSeed(
                    queue_id=queue_id,
                    kind=queue.kind,
                    stem=str(payload.get("stem", "")),
                    body=str(payload.get("body", "")),
                    session_id=queue.ai_session_id,
                )
                await self.run_concept(seed)
            elif doc_gate and doc_gate.status == "approved":
                # auto-approved 인데 확정(commit_ref)이 안 끝났다 — 착지·확정 중
                # 실패한 경우다. 초안은 저장돼 있으니 재생성 없이 착지부터 다시 돈다
                # (착지는 멱등 — 같은 내용이면 커밋 없이 HEAD 재사용, content 도 멱등).
                await self._set_status(
                    queue_id, {"status": "processing", "error": None}
                )
                await self._land_document(queue, doc_gate)
            else:
                await self._run_document(queue)
        except Exception as exc:  # 실패는 failed + error 한 줄이 전부
            logger.exception("inbox process 실패: queue %s", queue_id)
            await self._fail(queue_id, f"{type(exc).__name__}: {exc}")

    async def _force_youtube_number(self, payload: dict) -> None:
        """youtube 채번은 서버가 강제한다 — codex 가 낸 번호를 **신뢰하지 않는다**.

        codex 가 원장을 못 읽은 상태로 C-000·C-001 을 낸 실사고(2026-08-25) 이후,
        게이트 payload 를 저장하기 전에 여기서 번호를 덮는다:
        - 다음 번호 = max(para/resources/youtube/ 파일명 stem 의 C-NNN 최대,
          content.slug 의 C-NNN 최대) + 1 — 결번 재사용 금지 규약이라 둘 중 큰 쪽 기준
        - codex stem 에서는 slug 부분만 취한다(`C-NNN-<slug>` 의 `<slug>`)
        - youtube 만 C-NNN 채번이다 — docs/article/blog 는 stem 에 번호가 없다
        """
        settings = get_settings()
        max_n = 0
        ydir = Path(settings.repo_root) / "para" / "resources" / "youtube"
        if ydir.is_dir():
            for p in ydir.glob("*.md"):
                m = _C_NUMBER.match(p.stem)
                if m:
                    max_n = max(max_n, int(m.group(1)))
        async with SessionLocal() as session:
            for slug in await self._content_repo.list_slugs(session):
                m = _C_NUMBER.match(slug)
                if m:
                    max_n = max(max_n, int(m.group(1)))
        number = f"C-{max_n + 1:03d}"

        raw_stem = str(payload.get("stem", ""))
        slug_part = _C_NUMBER.sub("", raw_stem).strip("-") or "untitled"
        payload["stem"] = f"{number}-{slug_part}"
        # meta 에 slug 류가 실려 오면(스키마엔 없지만 방어) 서버 번호로 맞춘다
        meta = payload.get("meta")
        if isinstance(meta, dict) and "slug" in meta:
            meta["slug"] = number

    async def _run_document(self, queue: QueueDTO) -> None:
        """문서 단계(2026-08-25 개정) — 가져오기 + AI 초안 → 서버 검증 → 자동 착지.

        검증 통과 시 gate(document) 를 **auto-approved 로 기록**(payload ·
        decided_at — 이력용)하고 곧바로 착지 → 개념 생성으로 잇는다.
        검증 탈락은 DocumentInvalid — 호출자(process)가 failed 로 남긴다.
        """
        await self._set_status(queue.id, {"status": "processing", "error": None})

        source = await fetch_source(queue.kind, queue.source_url or "")
        document = await ai_service.generate_document(
            queue.kind, queue.source_url or "", queue.note, source
        )
        document.payload["stem"] = normalize_stem(str(document.payload.get("stem", "")))
        if queue.kind == "youtube":
            await self._force_youtube_number(document.payload)

        # 정형(stem 경로 안전 · meta) 검증은 승인 경로와 같은 것을 쓰고(gate_service),
        # 그 위에 본문 양식·실행 실패 흔적 검증(케이스 1 개정)을 얹는다.
        from service.gate_service import validate_document_payload

        payload = validate_document_payload(document.payload, queue.kind)
        validate_document_body(payload["body"])

        # 검증 통과 — 착지 전에 auto-approved 기록부터 확정한다. 착지·확정이 도중에
        # 죽어도 초안이 남아, 재시도가 재생성 없이 착지부터 다시 돈다(process 분기).
        async with SessionLocal() as session:
            fields = {
                "payload": payload,
                "status": "approved",
                "decided_at": datetime.now(timezone.utc),
                "commit_ref": None,
                "result": None,
            }
            existing = await self._gate_repo.get_by_queue_stage(
                session, queue.id, "document"
            )
            if existing:  # 재시도로 다시 온 경우 — 초안을 덮는다
                gate = await self._gate_repo.update(session, existing.id, fields)
                assert gate is not None
            else:
                gate = await self._gate_repo.create(
                    session, {"queue_id": queue.id, "stage": "document", **fields}
                )
            await self._queue_repo.update(
                session,
                queue.id,
                {"error": None, "ai_session_id": document.session_id},
            )
            await session.commit()

        # ConceptSeed.session_id 는 방금 저장한 세션이다 — 손의 queue DTO 는 낡았다.
        await self._land_document(
            replace(queue, ai_session_id=document.session_id), gate
        )

    async def _land_document(self, queue: QueueDTO, gate: GateDTO) -> None:
        """자동 착지 — gate_service 의 착지 로직 재사용 후 곧바로 개념 생성으로.

        푸시 실패(비 dry-run)면 approved + commit_ref NULL 그대로 두고 review 로
        올린다 — 화면의 [재시도](gate retry-push)가 착지부터 다시 돈다(경로 유지).
        """
        from service.gate_service import gate_service  # 순환 없음 — gate_service 는 inbox 를 모른다

        async with SessionLocal() as session:
            gate_final, seed, push_error = await gate_service.auto_land_document(
                session, gate, queue
            )
            await session.commit()

        if push_error:
            logger.warning(
                "문서 자동 착지 push 실패: queue %s — %s", queue.id, push_error
            )
            await self._set_status(queue.id, {"status": "review", "error": None})
            return

        logger.info(
            "문서 자동 착지 확정: queue %s → %s (%s)",
            queue.id,
            (gate_final.result or {}).get("paths"),
            gate_final.commit_ref,
        )
        assert seed is not None  # document 확정은 항상 개념 seed 를 낸다
        await self.run_concept(seed)

    async def run_concept(self, seed: ConceptSeed) -> None:
        """개념 단계 — 문서 자동 착지 직후, 또는 그 실패의 재시도.

        문서 생성 세션을 resume 하고 착지 확정본을 동봉한다(ai_service).
        """
        try:
            await self._set_status(seed.queue_id, {"status": "processing", "error": None})
            payload = await ai_service.generate_concepts(
                seed.kind, seed.stem, seed.body, seed.session_id
            )
            async with SessionLocal() as session:
                existing = await self._gate_repo.get_by_queue_stage(
                    session, seed.queue_id, "concept"
                )
                if existing:
                    await self._gate_repo.update(
                        session, existing.id, {"payload": payload, "status": "open"}
                    )
                else:
                    await self._gate_repo.create(
                        session,
                        {"queue_id": seed.queue_id, "stage": "concept", "payload": payload},
                    )
                await self._queue_repo.update(
                    session, seed.queue_id, {"status": "review", "error": None}
                )
                await session.commit()
        except Exception as exc:
            logger.exception("concept 생성 실패: queue %s", seed.queue_id)
            await self._fail(seed.queue_id, f"{type(exc).__name__}: {exc}")


inbox_pipeline = InboxPipeline(QueueRepository(), GateRepository(), ContentRepository())
