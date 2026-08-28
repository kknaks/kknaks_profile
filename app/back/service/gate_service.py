"""게이트(gate) — 2층. 게이트 목록 + 착지·승인·거절·푸시 재시도 (케이스 1).

케이스 1 정본(2026-08-25 개정): **문서는 서버 검증 통과 시 자동 착지한다** —
사람 승인은 concept 게이트 하나다. gate(document) 행은 auto-approved 기록으로
남는다(이력용). 착지 자체는 양쪽이 같다: **파일이 원장이므로 파일이 먼저 착지한다.**
순서는 payload 저장 → approved → md 착지 → commit·push → commit_ref →
(youtube) content 행. 푸시가 실패하면 DB 는 아무것도 확정하지 않는다 —
approved + commit_ref NULL 로 남고, 화면의 [재시도] 가 착지부터 다시 돈다.
별도 재시도 잡은 없다.

게이트마다 커밋 하나 — 메시지는 게이트 1 `<종류> {stem}`, 게이트 2
`fix/concept - {stem}` (케이스 1 정본).
"""

from __future__ import annotations

import logging
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.crypto import decrypt_token
from core.exceptions import ConflictError, NotFoundError, ValidationError
from core.git import (
    GitIdentity,
    GitPushCredentials,
    GitPushError,
    commit_and_push,
    pull_ledger,
)
from dto.gate import ConceptSeed, GateDTO, GateWithQueue
from dto.queue import QueueDTO
from repository.content_repo import ContentRepository
from repository.gate_repo import GateRepository
from repository.git_token_repo import GitTokenRepository
from repository.profile_repo import ProfileRepository
from repository.queue_repo import QueueRepository

logger = logging.getLogger(__name__)

# dry-run(JOB_GIT_PUSH_DRY_RUN=1, dev) 확정 마커 — 커밋·푸시 없이 md 만 착지한
# 게이트의 commit_ref (사용자 결정 2026-08-25). NULL 이면 「푸시 실패·재시도 대기」와
# 겹치므로 반드시 문자열로 구분한다(varchar(40) 안).
DRY_RUN_REF = "dry-run"

# 착지일(published_on) 기준 시간대 — 서버가 KST 오늘로 강제한다(케이스 1).
_KST = ZoneInfo("Asia/Seoul")

# stem·area 는 파일 경로가 된다 — 탈출 문자를 여기서 막는다.
_SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$", re.IGNORECASE)

_CONCEPT_AREAS = frozenset(
    {"ai", "back", "cs", "db", "design", "front", "infra", "pm", "qa"}
)


def _require_safe_name(value: str, what: str) -> str:
    value = (value or "").strip()
    if not value or ".." in value or not _SAFE_NAME.match(value):
        raise ValidationError(f"{what} 이 파일명으로 쓸 수 없는 값입니다: {value!r}")
    return value


def validate_document_payload(payload: dict, kind: str) -> dict:
    """문서 payload 정형 검증 — stem 은 파일 경로가 되므로 탈출 문자를 여기서 막는다.

    승인 경로(approve)와 자동 착지 경로(inbox 파이프라인) **양쪽이 같은 검증**을
    쓴다 — 자동 착지가 생기면서(2026-08-25 개정) 공개로 올렸다.
    """
    stem = _require_safe_name(str(payload.get("stem", "")), "stem")
    body = str(payload.get("body", ""))
    if not body.strip():
        raise ValidationError("본문(body)이 비었습니다")
    clean: dict = {"stem": stem, "body": body}
    if kind == "youtube":
        meta = payload.get("meta")
        if not isinstance(meta, dict) or not str(meta.get("title", "")).strip():
            raise ValidationError("youtube 는 카드 메타(meta.title)가 필요합니다")
        clean["meta"] = meta
    return clean


def _validate_concept_payload(payload: dict) -> dict:
    items = payload.get("concepts")
    if not isinstance(items, list):
        raise ValidationError("concepts 배열이 없습니다")
    clean = []
    for item in items:
        if not isinstance(item, dict):
            raise ValidationError("concepts 항목이 객체가 아닙니다")
        mode = item.get("mode")
        if mode not in ("create", "supplement"):
            raise ValidationError(f"mode 는 create/supplement 만 됩니다: {mode}")
        area = str(item.get("area", "")).strip()
        if area not in _CONCEPT_AREAS:
            raise ValidationError(f"area 가 아홉 영역이 아닙니다: {area}")
        stem = _require_safe_name(str(item.get("stem", "")), "concept stem")
        body = str(item.get("body", ""))
        if not body.strip():
            raise ValidationError(f"개념 {stem} 의 본문(body)이 비었습니다")
        clean.append(
            {"mode": mode, "area": area, "stem": stem, "body": body,
             "diff": str(item.get("diff", ""))}
        )
    return {"concepts": clean}


class GateService:
    def __init__(
        self,
        gate_repo: GateRepository,
        queue_repo: QueueRepository,
        content_repo: ContentRepository,
        profile_repo: ProfileRepository,
        git_token_repo: GitTokenRepository,
    ) -> None:
        self._gate_repo = gate_repo
        self._queue_repo = queue_repo
        self._content_repo = content_repo
        self._profile_repo = profile_repo
        self._git_token_repo = git_token_repo

    # ── 조회 ──────────────────────────────────────────────

    async def list_pending(self, session: AsyncSession) -> list[GateWithQueue]:
        """열린 게이트 + 「승인됨·푸시 실패」(approved & commit_ref NULL)."""
        return await self._gate_repo.list_pending(session)

    async def list_all(self, session: AsyncSession) -> list[GateWithQueue]:
        """닫힌 것 포함 전체 — done 행 펼침 이력용(2026-08-25 개정).

        확정 게이트(result.contentId)에는 콘텐츠 제목·slug 를 붙인다 — 이력이
        「어떤 콘텐츠가 생겼는지」를 보여준다.
        """
        return await self._attach_content(
            session, await self._gate_repo.list_all(session)
        )

    async def _attach_content(
        self, session: AsyncSession, items: list[GateWithQueue]
    ) -> list[GateWithQueue]:
        """result.contentId → content 조인해 content_title·content_slug 를 얹는다."""
        ids = [
            cid
            for item in items
            if isinstance(cid := (item.gate.result or {}).get("contentId"), int)
        ]
        if not ids:
            return items
        contents = await self._content_repo.get_by_ids(session, ids)
        out: list[GateWithQueue] = []
        for item in items:
            cid = (item.gate.result or {}).get("contentId")
            content = contents.get(cid) if isinstance(cid, int) else None
            out.append(
                replace(item, content_title=content.title, content_slug=content.slug)
                if content
                else item
            )
        return out

    async def get(self, session: AsyncSession, gate_id: int) -> GateWithQueue:
        item = await self._gate_repo.get_with_queue(session, gate_id)
        if item is None:
            raise NotFoundError(f"gate not found: {gate_id}")
        return item

    # ── 착지 (md → commit·push) ───────────────────────────

    async def _land_and_push(
        self, session: AsyncSession, gate: GateDTO, queue: QueueDTO, payload: dict
    ) -> tuple[str, list[str]]:
        """착지 직전 pull → md 착지 → commit·push. (sha, 상대경로들) 반환.

        **pull 이 md 쓰기보다 먼저다** — 순서를 뒤집으면 착지가 자기가 쓴 파일 때문에
        pull 에서 죽고, 그 파일이 워킹트리에 남아 다음 착지까지 막는다(core.git
        `pull_ledger` 주석 — 2026-08-28 실사고).

        커밋 신원은 git_token personal 행(account·email) — 없으면 422 (사용자 결정).
        JOB_GIT_PUSH_DRY_RUN=1(dev)이면 **커밋·푸시 둘 다 안 한다**(사용자 결정
        2026-08-25) — md 파일만 워킹트리에 쓰고 DRY_RUN_REF 로 확정한다.
        실패는 GitPushError 그대로 위로 — 호출자가 「approved + commit_ref NULL」로
        남긴다.
        """
        settings = get_settings()
        ledger = Path(settings.ledger_path)
        dry_run = settings.job_git_push_dry_run

        identity: GitIdentity | None = None
        credentials: GitPushCredentials | None = None
        if not dry_run:
            # dry-run 은 git 을 아예 안 만지므로 신원·자격이 필요 없다.
            personal = await self._git_token_repo.get_personal_with_cipher(session)
            if personal is None:
                raise ValidationError(
                    "personal 토큰을 등록하세요 — 착지 커밋 신원(git_token personal)이 필요합니다"
                )
            token_dto, cipher = personal
            identity = GitIdentity(name=token_dto.account, email=token_dto.email)
            credentials = GitPushCredentials(
                account=token_dto.account, token=decrypt_token(cipher)
            )
        if gate.stage == "document":
            stem = payload["stem"]
            rel_paths = [f"para/resources/{queue.kind}/{stem}.md"]
            bodies = [payload["body"]]
            message = f"{queue.kind} {stem}"
        else:
            doc_gate = await self._gate_repo.get_by_queue_stage(
                session, queue.id, "document"
            )
            doc_stem = (doc_gate.payload.get("stem") if doc_gate else None) or queue.kind
            rel_paths = [
                f"para/areas/concept/{item['area']}/{item['stem']}.md"
                for item in payload["concepts"]
            ]
            bodies = [item["body"] for item in payload["concepts"]]
            message = f"fix/concept - {doc_stem}"

        if not dry_run:
            # 반드시 write 앞 — 여기서 실패하면 워킹트리를 건드리지 않은 채로 끝난다.
            assert identity is not None
            await pull_ledger(str(ledger), identity, credentials=credentials)

        for rel, body in zip(rel_paths, bodies):
            target = ledger / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            content = body if body.endswith("\n") else body + "\n"
            target.write_text(content, encoding="utf-8")

        if dry_run:
            # 커밋·푸시 전부 스킵 — 파일 착지만. 확정 마커는 DRY_RUN_REF(문자열).
            logger.info(
                "착지 dry-run(JOB_GIT_PUSH_DRY_RUN=1) — git add/commit/push 스킵: %s",
                ", ".join(rel_paths),
            )
            return DRY_RUN_REF, rel_paths

        assert identity is not None
        result = await commit_and_push(
            str(ledger), rel_paths, message, identity, credentials=credentials,
        )
        return result.sha, rel_paths

    async def _finalize(
        self,
        session: AsyncSession,
        gate: GateDTO,
        queue: QueueDTO,
        payload: dict,
        sha: str,
        rel_paths: list[str],
    ) -> tuple[GateDTO, ConceptSeed | None]:
        """푸시 성공 후 DB 확정 — commit_ref · (게이트 1 youtube) content 행 · queue 전이."""
        result: dict = {"paths": rel_paths}
        seed: ConceptSeed | None = None

        if gate.stage == "document":
            if queue.kind == "youtube":
                content_id = await self._insert_content(session, payload, rel_paths[0])
                result["contentId"] = content_id
            # 개념 보강안 생성으로 이어진다 — 라우터가 백그라운드로 건다(Step 5·6)
            seed = ConceptSeed(
                queue_id=queue.id,
                kind=queue.kind,
                stem=payload["stem"],
                body=payload["body"],
                session_id=queue.ai_session_id,
            )
        else:
            await self._queue_repo.update(session, queue.id, {"status": "done"})

        updated = await self._gate_repo.update(
            session, gate.id, {"commit_ref": sha, "result": result}
        )
        assert updated is not None
        return updated, seed

    async def _insert_content(
        self, session: AsyncSession, payload: dict, rel_path: str
    ) -> int:
        """게이트 1 · youtube 확정 — content 행 INSERT (승인 확정 메타 그대로).

        detail_path 실존 검사는 안 한다 — 방금 이 요청이 착지한 파일이고, 착지
        원장(ledger_path)은 md 서빙 루트(repo_root)와 다를 수 있다.
        """
        meta = payload.get("meta") or {}
        stem = payload["stem"]
        m = re.match(r"^(C-\d+)", stem)
        slug = m.group(1) if m else stem[:64]

        existing = await self._content_repo.get_by_slug(session, slug)
        if existing:
            if existing.detail_path == rel_path:
                return existing.id  # 푸시 재시도의 멱등 — 이미 확정됐다
            raise ConflictError(f"content slug 가 이미 있습니다: {slug}")

        profile = await self._profile_repo.get_first(session)
        if profile is None:
            raise ValidationError("profile 이 없습니다 — 시드를 먼저 넣어야 합니다")

        tags = meta.get("tags")
        content = await self._content_repo.create(
            session,
            {
                "profile_id": profile.id,
                "slug": slug,
                "title": str(meta.get("title", "")).strip() or stem,
                "summary": str(meta.get("summary", "")).strip() or None,
                "detail_path": rel_path,
                "youtube_id": str(meta.get("youtubeId", "")).strip(),
                "duration": str(meta.get("duration", "")).strip() or None,
                "speaker": str(meta.get("speaker", "")).strip() or None,
                "tags": [str(t) for t in tags] if isinstance(tags, list) and tags else None,
                # published_on 은 **착지일**(KST 오늘)이다 — 기존 규약(C-0NN frontmatter)의
                # published_on 이 「내가 정리한 날」이기 때문. codex meta 의 publishedOn
                # (영상 게시일)을 쓰면 공개 목록(published_on DESC)에서 옛날 위치에
                # 처박힌다(2026-08-25 실측). 영상 게시일은 md 출처 줄에 이미 있다.
                "published_on": datetime.now(_KST).date(),
            },
        )
        return content.id

    # ── 승인 · 거절 · 푸시 재시도 ─────────────────────────

    async def approve(
        self, session: AsyncSession, gate_id: int, payload: dict
    ) -> tuple[GateDTO, QueueDTO, ConceptSeed | None, str | None]:
        """승인 — 다듬은 payload 가 저장되고 그대로 착지한다(inbox.md Step 4).

        반환: (gate, queue, 개념 생성 seed, push_error). push_error 가 있으면
        approved + commit_ref NULL 로 남은 것 — 화면의 [재시도] 대기다.
        """
        item = await self.get(session, gate_id)
        gate, queue = item.gate, item.queue
        if gate.status != "open":
            raise ValidationError(f"open 게이트만 승인할 수 있습니다: {gate.status}")

        clean = (
            validate_document_payload(payload, queue.kind)
            if gate.stage == "document"
            else _validate_concept_payload(payload)
        )

        updated = await self._gate_repo.update(
            session,
            gate_id,
            {
                "payload": clean,
                "status": "approved",
                "decided_at": datetime.now(timezone.utc),
            },
        )
        assert updated is not None

        # 게이트 2 인데 올릴 항목이 하나도 없다 — 착지·커밋 없이 종결한다.
        # (체크를 전부 해제하고 승인한 경우. 거절은 전체를 버릴 때만이므로 유효한 길이다)
        if gate.stage == "concept" and not clean["concepts"]:
            updated = await self._gate_repo.update(
                session, gate_id, {"result": {"paths": []}}
            )
            assert updated is not None
            await self._queue_repo.update(session, queue.id, {"status": "done"})
            return updated, queue, None, None

        try:
            sha, rel_paths = await self._land_and_push(session, updated, queue, clean)
        except GitPushError as exc:
            # 파일이 먼저, DB 가 나중 — 푸시 실패면 approved 만 남기고 확정하지 않는다
            return updated, queue, None, str(exc)

        gate_final, seed = await self._finalize(
            session, updated, queue, clean, sha, rel_paths
        )
        return gate_final, queue, seed, None

    async def reject(
        self, session: AsyncSession, gate_id: int
    ) -> tuple[GateDTO, QueueDTO]:
        """거절 — rejected 기록, queue 는 done. 이유는 안 적는다(inbox.md Step 4)."""
        item = await self.get(session, gate_id)
        gate, queue = item.gate, item.queue
        if gate.status != "open":
            raise ValidationError(f"open 게이트만 거절할 수 있습니다: {gate.status}")
        updated = await self._gate_repo.update(
            session,
            gate_id,
            {"status": "rejected", "decided_at": datetime.now(timezone.utc)},
        )
        assert updated is not None
        await self._queue_repo.update(session, queue.id, {"status": "done"})
        return updated, queue

    async def retry_push(
        self, session: AsyncSession, gate_id: int
    ) -> tuple[GateDTO, QueueDTO, ConceptSeed | None, str | None]:
        """푸시 실패분 재시도 — 저장된 payload 로 착지부터 다시(3번부터, Step 5)."""
        item = await self.get(session, gate_id)
        gate, queue = item.gate, item.queue
        if gate.status != "approved" or gate.commit_ref is not None or gate.result is not None:
            raise ValidationError("승인됨 + 푸시 실패 상태만 재시도할 수 있습니다")

        try:
            sha, rel_paths = await self._land_and_push(session, gate, queue, gate.payload)
        except GitPushError as exc:
            return gate, queue, None, str(exc)

        gate_final, seed = await self._finalize(
            session, gate, queue, gate.payload, sha, rel_paths
        )
        return gate_final, queue, seed, None

    # ── 문서 자동 착지 — 케이스 1, 2026-08-25 개정 ─────────

    async def auto_land_document(
        self, session: AsyncSession, gate: GateDTO, queue: QueueDTO
    ) -> tuple[GateDTO, ConceptSeed | None, str | None]:
        """검증 통과한 문서 초안을 **사람 승인 없이** 착지한다 — inbox 파이프라인이 부른다.

        gate(document) 행은 파이프라인이 approved(auto) 로 미리 기록해 뒀다(이력용).
        착지·확정 로직은 승인 경로와 같다(_land_and_push → _finalize 재사용).
        푸시 실패면 (gate, None, error) — approved + commit_ref NULL 로 남고
        화면의 [재시도](retry_push)가 착지부터 다시 돈다(기존 경로 유지).
        """
        try:
            sha, rel_paths = await self._land_and_push(session, gate, queue, gate.payload)
        except GitPushError as exc:
            return gate, None, str(exc)
        gate_final, seed = await self._finalize(
            session, gate, queue, gate.payload, sha, rel_paths
        )
        return gate_final, seed, None


gate_service = GateService(
    GateRepository(),
    QueueRepository(),
    ContentRepository(),
    ProfileRepository(),
    GitTokenRepository(),
)
