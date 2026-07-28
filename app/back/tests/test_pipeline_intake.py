"""접수 + 자동 준비 (KDEV-WORK-014 Phase 2 / KDEV-SPEC-007).

URL 정규화는 DB 없이 돌지만, 접수·준비는 제약과 함께 검증해야 의미가 있어
실 Postgres 를 쓴다(미가용이면 해당 클래스만 skip).
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import AITask, ItemPreparation, QueueItem
from service.pipeline import (
    SummaryResult,
    detect_source_kind,
    intake,
    normalize_url,
    prepare_item,
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


@pytest.fixture
async def db():
    """트랜잭션에 묶고 끝나면 롤백 — 실 DB 에 흔적을 남기지 않는다."""
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


# --- URL 정규화 -------------------------------------------------------------


class TestNormalizeUrl:
    def test_youtube_forms_collapse_to_one_key(self):
        """같은 영상이 어떤 모양으로 들어와도 한 항목이어야 한다."""
        keys = {
            normalize_url(u)
            for u in [
                "https://youtu.be/dQw4w9WgXcQ",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=120s",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL123&index=4",
                "https://youtu.be/dQw4w9WgXcQ?si=AbCdEf",
                "https://www.youtube.com/shorts/dQw4w9WgXcQ",
                "https://www.youtube.com/embed/dQw4w9WgXcQ",
            ]
        }
        assert keys == {"youtube:dQw4w9WgXcQ"}

    def test_different_videos_stay_separate(self):
        assert normalize_url("https://youtu.be/aaaaaaaaaaa") != normalize_url(
            "https://youtu.be/bbbbbbbbbbb"
        )

    def test_tracking_params_dropped_but_real_query_kept(self):
        """추적 파라미터만 뗀다 — 쿼리를 통째로 지우면 다른 글이 합쳐진다."""
        a = normalize_url("https://blog.example.com/post?p=1&utm_source=x&fbclid=y")
        b = normalize_url("https://blog.example.com/post?p=1")
        c = normalize_url("https://blog.example.com/post?p=2")
        assert a == b
        assert a != c

    def test_query_order_does_not_matter(self):
        assert normalize_url("https://e.com/a?x=1&y=2") == normalize_url("https://e.com/a?y=2&x=1")

    def test_host_case_www_slash_and_fragment_normalized(self):
        assert normalize_url("https://WWW.Example.com/post/#section") == normalize_url(
            "https://example.com/post"
        )

    @pytest.mark.parametrize("value", [None, "", "   ", "ftp://x/y", "그냥 텍스트", "javascript:alert(1)"])
    def test_unnormalizable_returns_none(self, value):
        """정규화할 수 없으면 `None` — 틀린 키로 서로 다른 자료를 묶는 것보다 낫다."""
        assert normalize_url(value) is None


class TestDetectSourceKind:
    @pytest.mark.parametrize(
        "url, expected",
        [
            ("https://youtu.be/dQw4w9WgXcQ", "youtube"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
            ("https://blog.example.com/post", "blog"),
            ("https://arxiv.org/abs/1234.5678", "blog"),
            (None, "manual"),
            ("메모만 남긴 항목", "manual"),
        ],
    )
    def test_kind(self, url, expected):
        assert detect_source_kind(url) == expected


# --- 접수 -------------------------------------------------------------------


@needs_db
class TestIntake:
    async def test_creates_item(self, db):
        result = await intake(
            db, source_url="https://youtu.be/newvideo01", note="메모", channel="slack",
            submitted_by="U123",
        )
        assert result.outcome == "created"
        item = await db.get(QueueItem, result.item_id)
        assert (item.status, item.source_kind, item.channel) == ("received", "youtube", "slack")
        assert item.normalized_url == "youtube:newvideo01"

    async def test_same_url_joins_pending_item(self, db):
        """발행 전 재투입은 새 항목이 아니라 합류다(S-4)."""
        first = await intake(db, source_url="https://youtu.be/joinvideo1", note="첫 메모")
        second = await intake(
            db, source_url="https://www.youtube.com/watch?v=joinvideo1&t=30s", note="둘째 메모"
        )
        assert second.outcome == "joined"
        assert second.item_id == first.item_id
        item = await db.get(QueueItem, first.item_id)
        assert "첫 메모" in item.note and "둘째 메모" in item.note

    async def test_joining_does_not_overwrite_note(self, db):
        """메모를 덮으면 첫 투입의 맥락이 사라진다."""
        first = await intake(db, source_url="https://youtu.be/keepnote001", note="원래 맥락")
        await intake(db, source_url="https://youtu.be/keepnote001", note=None)
        item = await db.get(QueueItem, first.item_id)
        assert item.note == "원래 맥락"

    async def test_published_url_is_flagged_not_auto_joined(self, db):
        """이미 발행된 자료의 재정리는 정당할 수 있어 사람이 정한다."""
        done = await intake(db, source_url="https://youtu.be/published01")
        item = await db.get(QueueItem, done.item_id)
        item.status = "published"
        await db.flush()

        again = await intake(db, source_url="https://youtu.be/published01")
        assert again.outcome == "duplicate_published"
        assert again.item_id is None
        assert again.existing_item_id == done.item_id

    async def test_republish_when_owner_decides(self, db):
        done = await intake(db, source_url="https://youtu.be/republish01")
        item = await db.get(QueueItem, done.item_id)
        item.status = "published"
        await db.flush()

        again = await intake(db, source_url="https://youtu.be/republish01", allow_republish=True)
        assert again.outcome == "created"
        assert again.item_id != done.item_id

    async def test_deleted_item_does_not_block_new_intake(self, db):
        first = await intake(db, source_url="https://youtu.be/deleted001")
        item = await db.get(QueueItem, first.item_id)
        item.status, item.deleted_at = "deleted", __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        )
        await db.flush()

        again = await intake(db, source_url="https://youtu.be/deleted001")
        assert again.outcome == "created"

    async def test_note_only_items_never_collide(self, db):
        """URL 없는 항목끼리는 중복 판정 대상이 아니다."""
        a = await intake(db, note="생각 1")
        b = await intake(db, note="생각 2")
        assert a.outcome == b.outcome == "created"
        assert a.item_id != b.item_id


# --- 자동 준비 ---------------------------------------------------------------


async def _fetch_ok(url):
    return {"url": url, "content": "원문 본문", "title": "제목"}


async def _fetch_fail(url):
    raise RuntimeError("transcript unavailable")


async def _summarize_ok(*, material, note):
    return SummaryResult(summary="요약본", session_ref="sess-1")


async def _summarize_fail(*, material, note):
    raise RuntimeError("provider timeout")


@needs_db
class TestPrepare:
    async def test_success_moves_to_in_review(self, db):
        created = await intake(db, source_url="https://youtu.be/prepok00001")
        result = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok)

        assert result.ok and result.version == 1
        item = await db.get(QueueItem, created.item_id)
        assert item.status == "in_review"
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.payload["summary"] == "요약본"
        assert prep.payload["material_source"] == "fetched"

    async def test_note_substitutes_for_unreachable_source(self, db):
        """수집이 막혀도 메모가 있으면 준비가 성립한다 — 수집 실패가 항목을 죽이지 않는다."""
        created = await intake(
            db, source_url="https://youtu.be/nocaption01", note="자막이 없어 직접 요약: 핵심은 X"
        )
        result = await prepare_item(db, created.item_id, fetch=_fetch_fail, summarize=_summarize_ok)

        assert result.ok
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.payload["material_source"] == "note"
        # 무엇이 막혔는지는 남는다 — 근거가 원문인지 기억인지 구분되어야 한다.
        assert "transcript unavailable" in prep.payload["collect_error"]

    async def test_no_source_and_no_note_fails_without_calling_ai(self, db):
        """요약할 것이 없으면 AI 를 부르지 않는다 — 부르면 환각을 근거로 route 를 판단한다."""
        created = await intake(db, source_url="https://youtu.be/nothing0001")

        async def _must_not_run(**kwargs):
            raise AssertionError("요약할 재료가 없는데 AI 를 호출했다")

        result = await prepare_item(db, created.item_id, fetch=_fetch_fail, summarize=_must_not_run)

        assert result.status == "prepare_failed"
        assert result.error_code == "NO_SOURCE_MATERIAL"
        item = await db.get(QueueItem, created.item_id)
        assert item.status == "prepare_failed"
        tasks = (await db.scalars(select(AITask).where(AITask.item_id == created.item_id))).all()
        assert tasks == []

    async def test_summarize_failure_keeps_task_row(self, db):
        created = await intake(db, source_url="https://youtu.be/aifail0001")
        result = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_fail)

        assert result.status == "prepare_failed"
        assert result.error_code == "SUMMARIZE_FAILED"
        task = await db.scalar(select(AITask).where(AITask.item_id == created.item_id))
        assert task.status == "failed"
        assert "provider timeout" in task.error_message

    async def test_retry_adds_version_and_preserves_failure(self, db):
        """재시도는 기존 실행 기록을 덮어쓰지 않는다 (SPEC-007 AC)."""
        created = await intake(db, source_url="https://youtu.be/retry000001")
        first = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_fail)
        assert first.status == "prepare_failed"

        # 사람이 메모를 보태고 재시도한다.
        item = await db.get(QueueItem, created.item_id)
        item.note = "메모 보완"
        await db.flush()
        second = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok)

        assert second.ok and second.version == 2
        preps = (
            await db.scalars(
                select(ItemPreparation)
                .where(ItemPreparation.item_id == created.item_id)
                .order_by(ItemPreparation.version)
            )
        ).all()
        assert [(p.version, p.status) for p in preps] == [(1, "failed"), (2, "succeeded")]

        tasks = (
            await db.scalars(
                select(AITask).where(AITask.item_id == created.item_id).order_by(AITask.id)
            )
        ).all()
        assert [t.status for t in tasks] == ["failed", "succeeded"]
        # 재시도 행이 원 실패를 가리켜 감사 이력이 이어진다.
        assert tasks[1].retry_of_task_id == tasks[0].id

    async def test_cannot_prepare_item_already_in_review(self, db):
        """검토 중인 항목을 다시 준비하면 사람이 보던 근거가 발밑에서 바뀐다."""
        created = await intake(db, source_url="https://youtu.be/inreview001")
        await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok)

        again = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok)
        assert again.status == "not_allowed"
        assert again.error_code == "PREPARE_RETRY_NOT_ALLOWED"

    async def test_deleted_item_is_not_prepared(self, db):
        created = await intake(db, source_url="https://youtu.be/deleted002")
        item = await db.get(QueueItem, created.item_id)
        item.deleted_at = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        )
        await db.flush()

        result = await prepare_item(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok)
        assert result.status == "not_allowed"
