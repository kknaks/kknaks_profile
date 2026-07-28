"""derived 게이트 + route 재오픈 (KDEV-WORK-015 P3).

교안 경로는 **게이트와 손 경로가 공존**한다(owner 결정). 그래서 게이트 산출물이
`content_enrich` 의 스캔 조건(`status: pending`)에 걸리지 않는 것이 이 Phase 의
전제다 — 걸리면 그 잡이 한 번 더 덮어쓴다.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import frontmatter
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import Gate, GateRevision, ItemPreparation, QueueItem
from service.pipeline import gates as gates_service
from service.pipeline import intake
from service.pipeline.chain import advance, reopen_route
from service.pipeline.gates import GateError, GenerationResult, open_first_gate
from service.pipeline.stages.derived import (
    build_content_note,
    format_duration,
    next_content_id,
    video_header,
)

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")

PREPARATION = {
    "material_source": "fetched",
    "source": {
        "content": '{"video_id": "abc12345678", "channel": "Decoded AI", "duration_s": 382}\n\n자막...',
    },
}

GOOD = {
    "title": {"ko": "제목", "en": "Title"},
    "summary": {"ko": "요약", "en": "Summary"},
    "tags": ["#fastapi"],
    "concept": ["문장1", "문장2"],
    "kind": "study",
    "body": "## 개요\n\n내용\n",
}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "persona/contents").mkdir(parents=True)
    return tmp_path


def _build(repo: Path, data=None, **kw):
    return build_content_note(
        {**GOOD, **(data or {})},
        repo_root=repo,
        preparation_payload=PREPARATION,
        source_url="https://youtu.be/abc12345678",
        today=date(2026, 7, 28),
        **kw,
    )


class TestSystemAssignedFields:
    """식별자와 순번은 AI 가 정하지 않는다 — 맡기면 중복 번호가 나온다."""

    def test_first_content_id(self, repo):
        assert next_content_id(repo) == ("C-001", 1)

    def test_id_continues_from_existing(self, repo):
        for name in ("C-001.md", "C-007.md", "C-003-pending.md"):
            (repo / "persona/contents" / name).write_text("---\nid: x\n---\n", encoding="utf-8")
        assert next_content_id(repo) == ("C-008", 4)

    def test_ai_cannot_override_id(self, repo):
        note = _build(repo, {"id": "C-999", "day": "Day 99"})
        meta = frontmatter.loads(note["content"]).metadata
        assert meta["id"] == "C-001" and meta["day"] == "Day 01"

    def test_target_path_is_assembled(self, repo):
        assert _build(repo)["target_path"] == "persona/contents/C-001.md"


class TestNoPendingStatus:
    def test_status_is_published_not_pending(self, repo):
        """`pending` 이면 content_enrich 가 게이트 산출물을 한 번 더 덮어쓴다."""
        meta = frontmatter.loads(_build(repo)["content"]).metadata
        assert meta["status"] == "published"

    def test_enrich_job_would_skip_it(self, repo):
        """실제 스캔 함수로 확인한다 — 조건을 짐작하지 않는다."""
        from service.jobs.content_enrich import scan_pending_contents

        note = _build(repo)
        (repo / note["target_path"]).write_text(note["content"], encoding="utf-8")
        assert scan_pending_contents(repo / "persona/contents") == []


class TestVideoMetadata:
    def test_header_is_parsed(self):
        assert video_header(PREPARATION)["channel"] == "Decoded AI"

    def test_missing_header_is_tolerated(self):
        assert video_header({"source": {"content": "자막만 있음"}}) == {}

    def test_duration_formatted(self):
        assert format_duration(382) == "6:22"
        assert format_duration(None) == ""

    def test_speaker_and_duration_come_from_metadata(self, repo):
        meta = frontmatter.loads(_build(repo)["content"]).metadata
        assert meta["speaker"] == "Decoded AI" and meta["duration"] == "6:22"

    def test_transcript_flag_reflects_material_source(self, repo):
        note = build_content_note(
            GOOD,
            repo_root=repo,
            preparation_payload={"material_source": "note", "source": {}},
            source_url=None,
            today=date(2026, 7, 28),
        )
        assert frontmatter.loads(note["content"]).metadata["transcript"] is False


class TestValidation:
    @pytest.mark.parametrize(
        "bad",
        [
            {"kind": "bogus"},
            {"title": {"ko": "제목"}},
            {"summary": {"en": "only"}},
            {"tags": []},
            {"body": "섹션 없는 본문"},
            {"body": ""},
        ],
    )
    def test_malformed_rejected(self, repo, bad):
        with pytest.raises(GateError):
            _build(repo, bad)


# --- route 재오픈 -------------------------------------------------------------


@pytest.fixture
async def db():
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


def route(*, reference=True, concept=True, derived=False, exclusive=None):
    return {
        "destinations": {
            "reference": {"enabled": reference, "group": "study"},
            "concept": {"enabled": concept},
            "derived": {"enabled": derived},
        },
        "exclusive": exclusive,
    }


def maker(payload):
    async def _gen(request):
        return GenerationResult(payload=payload, session_ref="s")

    return _gen


NOTE = {"filename_stem": "2026-07-28-a-b", "content": "---\ntype: reference\n---\n"}


@needs_db
class TestReopen:
    async def _prepared(self, db, url: str, payload: dict):
        created = await intake(db, source_url=url, source_kind="youtube")
        item = await db.get(QueueItem, created.item_id)
        item.status = "in_review"
        db.add(
            ItemPreparation(
                item_id=item.id, version=1, status="succeeded", payload={"summary": "요약"}
            )
        )
        await db.flush()
        gate = await open_first_gate(db, item, generator=maker(payload))
        await gates_service.approve(db, gate)
        return item, gate

    async def test_reopen_cancels_later_gates_but_keeps_records(self, db):
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00001", route())
        second = await advance(db, item, route_gate, generators={"source_note": maker(NOTE)})
        assert second is not None
        second_revision_id = second.active_revision_id

        await reopen_route(db, item, generator=maker(route(derived=True)))

        assert second.status == "cancelled"
        # 기록은 남는다 — 무엇을 만들려 했는지 조회 가능해야 한다.
        kept = await db.get(GateRevision, second_revision_id)
        assert kept is not None and kept.payload is not None

    async def test_previous_approval_is_superseded_not_deleted(self, db):
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00002", route())
        old_revision_id = route_gate.approved_revision_id

        await reopen_route(db, item, generator=maker(route(concept=False)))

        old = await db.get(GateRevision, old_revision_id)
        assert old.status == "superseded" and old.payload is not None
        assert route_gate.approved_revision_id is None
        assert route_gate.status == "review_pending"

    async def test_reopen_does_not_rerun_preparation(self, db):
        """목적지 판단이 틀린 것이지 원문이 바뀐 게 아니다."""
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00003", route())
        await reopen_route(db, item, generator=maker(route()))

        preparations = (
            await db.scalars(
                select(ItemPreparation).where(ItemPreparation.item_id == item.id)
            )
        ).all()
        assert len(preparations) == 1

    async def test_chain_length_changes_after_reopen(self, db):
        """파생을 켜면 체인이 길어진다."""
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00004", route())
        await advance(db, item, route_gate, generators={"source_note": maker(NOTE)})

        await reopen_route(db, item, generator=maker(route(reference=False, concept=False, derived=True)))
        new_route = await db.scalar(
            select(Gate).where(Gate.item_id == item.id, Gate.stage_name == "route")
        )
        await gates_service.approve(db, new_route)
        nxt = await advance(
            db, item, new_route, generators={"source_note": maker(NOTE), "derived": maker(NOTE)}
        )
        assert nxt is not None and nxt.stage_name == "derived"

    async def test_reopen_revives_discarded_item(self, db):
        item, route_gate = await self._prepared(
            db,
            "https://youtu.be/reopen00005",
            route(reference=False, concept=False, exclusive="discard"),
        )
        item.status = "discarded"
        await db.flush()

        await reopen_route(db, item, generator=maker(route()))
        assert item.status == "in_review"

    async def test_published_item_cannot_be_reopened(self, db):
        """이미 나간 것을 되돌리는 것은 제품 기능이 아니다(DEC-012 D7)."""
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00006", route())
        item.status = "published"
        await db.flush()

        with pytest.raises(GateError) as exc:
            await reopen_route(db, item, generator=maker(route()))
        assert exc.value.code == "REOPEN_NOT_ALLOWED"

    async def test_cancelled_stage_can_be_reopened_later(self, db):
        """무효화한 스테이지를 다시 여는 경로 — partial unique 제약이 막지 않아야 한다."""
        item, route_gate = await self._prepared(db, "https://youtu.be/reopen00007", route())
        await advance(db, item, route_gate, generators={"source_note": maker(NOTE)})
        await reopen_route(db, item, generator=maker(route()))

        new_route = await db.scalar(
            select(Gate).where(Gate.item_id == item.id, Gate.stage_name == "route")
        )
        await gates_service.approve(db, new_route)
        again = await advance(db, item, new_route, generators={"source_note": maker(NOTE)})
        assert again is not None and again.stage_name == "source_note"
        assert again.status == "review_pending"
