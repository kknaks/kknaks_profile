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
from core.models import AITask, Gate, ItemPreparation, QueueItem
from service.pipeline import (
    detect_source_kind,
    harvest_preparation,
    intake,
    normalize_url,
    start_preparation,
)
from tests.fakes import FakeRunner, FakeSummarizer, prepare

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
    """**실물 타입**(`SourceMaterial` dataclass)을 돌려준다.

    dict 를 돌려주는 가짜를 쓰면 "객체를 그대로 JSON 직렬화해서 터지는" 버그를
    못 잡는다 — 운영 첫 시도에서 실제로 그렇게 터졌다.
    """
    from service.knowledge_capture.source import SourceMaterial

    return SourceMaterial(
        url=url, source_type="youtube", title="제목", content="원문 본문",
        accessed_at="2026-07-28T00:00:00+00:00",
    )


async def _fetch_fail(url):
    raise RuntimeError("transcript unavailable")


def _summarize_ok():
    return FakeSummarizer(summary="요약본", session_ref="sess-1")


def _summarize_fail():
    return FakeSummarizer(fail_times=1)


@needs_db
class TestPrepare:
    async def test_success_moves_to_in_review(self, db):
        created = await intake(db, source_url="https://youtu.be/prepok00001")
        result = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok())

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
        result = await prepare(db, created.item_id, fetch=_fetch_fail, summarize=_summarize_ok())

        assert result.ok
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.payload["material_source"] == "note"
        # 무엇이 막혔는지는 남는다 — 근거가 원문인지 기억인지 구분되어야 한다.
        assert "transcript unavailable" in prep.payload["collect_error"]

    async def test_no_source_and_no_note_fails_without_calling_ai(self, db):
        """요약할 것이 없으면 AI 를 부르지 않는다 — 부르면 환각을 근거로 route 를 판단한다."""
        created = await intake(db, source_url="https://youtu.be/nothing0001")

        def _explode(**kwargs):
            raise AssertionError("요약할 재료가 없는데 AI 를 호출했다")

        result = await prepare(
            db,
            created.item_id,
            fetch=_fetch_fail,
            summarize=FakeSummarizer(on_submit=_explode),
        )

        assert result.status == "prepare_failed"
        assert result.error_code == "NO_SOURCE_MATERIAL"
        item = await db.get(QueueItem, created.item_id)
        assert item.status == "prepare_failed"
        tasks = (await db.scalars(select(AITask).where(AITask.item_id == created.item_id))).all()
        assert tasks == []

    async def test_summarize_failure_keeps_task_row(self, db):
        """실패 사유는 **실행기가 준 코드 그대로** 올라온다.

        `TASK_NOT_FOUND` 와 `EXECUTION_TIMEOUT` 은 사람이 할 일이 다르다 —
        하나로 뭉뚱그리면 화면이 그 차이를 말하지 못한다.
        """
        created = await intake(db, source_url="https://youtu.be/aifail0001")
        result = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_fail())

        assert result.status == "prepare_failed"
        assert result.error_code == "RuntimeError"
        assert "provider timeout" in result.error_message
        task = await db.scalar(select(AITask).where(AITask.item_id == created.item_id))
        assert task.status == "failed"
        assert "provider timeout" in task.error_message
        # 실패도 준비 버전으로 남는다 — 상세 화면이 무엇이 막혔는지 보여줘야 한다.
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.status == "failed"
        assert prep.payload["error_code"] == "RuntimeError"

    async def test_retry_adds_version_and_preserves_failure(self, db):
        """재시도는 기존 실행 기록을 덮어쓰지 않는다 (SPEC-007 AC)."""
        created = await intake(db, source_url="https://youtu.be/retry000001")
        first = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_fail())
        assert first.status == "prepare_failed"

        # 사람이 메모를 보태고 재시도한다.
        item = await db.get(QueueItem, created.item_id)
        item.note = "메모 보완"
        await db.flush()
        second = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok())

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
        await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok())

        again = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok())
        assert again.status == "not_allowed"
        assert again.error_code == "PREPARE_RETRY_NOT_ALLOWED"

    async def test_deleted_item_is_not_prepared(self, db):
        created = await intake(db, source_url="https://youtu.be/deleted002")
        item = await db.get(QueueItem, created.item_id)
        item.deleted_at = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        )
        await db.flush()

        result = await prepare(db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok())
        assert result.status == "not_allowed"


@needs_db
class TestMaterialSerialization:
    """수집기는 dataclass 를 돌려준다 — 그걸 그대로 흘리면 요약 프롬프트에서 터진다.

    운영 첫 시도가 `Object of type SourceMaterial is not JSON serializable` 로 실패했다.
    테스트 가짜가 dict 를 돌려주고 있어 못 잡았다.
    """

    async def test_summarizer_receives_json_serializable_material(self, db):
        import json

        seen = {}

        def strict(*, material, note):
            # 실제 요약기가 제출 시점에 하는 일 — 여기서 터지면 운영에서도 터진다.
            json.dumps({"source_material": material, "note": note}, ensure_ascii=False)
            seen["material"] = material

        created = await intake(db, source_url="https://youtu.be/serialize01")
        result = await prepare(
            db,
            created.item_id,
            fetch=_fetch_ok,
            summarize=FakeSummarizer(on_submit=strict),
        )

        assert result.ok
        assert isinstance(seen["material"], dict)
        assert seen["material"]["content"] == "원문 본문"


@needs_db
class TestAsyncPreparation:
    """준비도 제출/수확으로 갈린다 (KDEV-WORK-016 P2 / SPEC-009 「실행은 비동기다」).

    접수 응답이 요약을 기다리면 30~60초를 붙잡게 되고, 앞단 프록시가 끊으면
    트랜잭션이 롤백돼 **접수 자체가 사라진다.**
    """

    async def test_submit_does_not_wait_for_the_summary(self, db):
        created = await intake(db, source_url="https://youtu.be/async000001")
        summarize = FakeSummarizer(pending=True)
        result = await start_preparation(
            db, created.item_id, fetch=_fetch_ok, summarize=summarize
        )

        assert result.running and not result.ok
        item = await db.get(QueueItem, created.item_id)
        assert item.status == "preparing"

        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.status == "running"
        # 수집 결과는 **이미 저장돼 있다** — 그래야 재시작해도 수확할 재료가 남는다.
        assert prep.payload["source"]["content"] == "원문 본문"
        assert prep.payload["summary"] is None

        task = await db.get(AITask, prep.ai_task_id)
        assert task.status == "running" and task.external_task_ref == "sum-1"

    async def test_harvest_finishes_and_opens_the_first_gate(self, db):
        created = await intake(db, source_url="https://youtu.be/async000002")
        summarize = FakeSummarizer(summary="요약본")
        runner = FakeRunner(payload={"x": 1})
        await start_preparation(db, created.item_id, fetch=_fetch_ok, summarize=summarize)

        item = await db.get(QueueItem, created.item_id)
        result = await harvest_preparation(db, item, summarize=summarize, runner=runner)

        assert result.ok and item.status == "in_review"
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.status == "succeeded" and prep.payload["summary"] == "요약본"
        # 준비가 끝나면 첫 게이트가 열린다 — 열리는 시점에는 제출까지다.
        gate = await db.scalar(select(Gate).where(Gate.item_id == item.id))
        assert gate is not None and gate.stage_name == "route"
        assert gate.status == "generating"

    async def test_running_summary_changes_nothing(self, db):
        created = await intake(db, source_url="https://youtu.be/async000003")
        summarize = FakeSummarizer(pending=True)
        await start_preparation(db, created.item_id, fetch=_fetch_ok, summarize=summarize)

        item = await db.get(QueueItem, created.item_id)
        result = await harvest_preparation(db, item, summarize=summarize)

        assert result.status == "preparing" and item.status == "preparing"
        assert await db.scalar(select(Gate).where(Gate.item_id == item.id)) is None

    async def test_harvest_is_idempotent(self, db):
        """폴링이 겹쳐도 준비 버전도 게이트도 두 번 만들어지지 않는다."""
        created = await intake(db, source_url="https://youtu.be/async000004")
        summarize = FakeSummarizer()
        runner = FakeRunner(payload={"x": 1})
        await start_preparation(db, created.item_id, fetch=_fetch_ok, summarize=summarize)

        item = await db.get(QueueItem, created.item_id)
        first = await harvest_preparation(db, item, summarize=summarize, runner=runner)
        second = await harvest_preparation(db, item, summarize=summarize, runner=runner)

        assert first.ok and second.status == "in_review"
        preps = (
            await db.scalars(
                select(ItemPreparation).where(ItemPreparation.item_id == item.id)
            )
        ).all()
        gates = (await db.scalars(select(Gate).where(Gate.item_id == item.id))).all()
        assert len(preps) == 1 and len(gates) == 1
        assert len(runner.calls) == 1

    async def test_harvest_resumes_after_restart(self, db):
        """back 이 재시작해도 실행기 큐의 작업을 이어 수확한다."""
        created = await intake(db, source_url="https://youtu.be/async000005")
        await start_preparation(
            db, created.item_id, fetch=_fetch_ok, summarize=FakeSummarizer(pending=True)
        )

        item = await db.get(QueueItem, created.item_id)
        reborn = FakeSummarizer(summary="이어받은 요약")
        result = await harvest_preparation(db, item, summarize=reborn)

        assert reborn.polled == ["sum-1"]  # 제출 객체를 잃어도 참조로 찾는다
        assert result.ok
        prep = await db.get(ItemPreparation, result.preparation_id)
        assert prep.payload["summary"] == "이어받은 요약"

    async def test_failed_harvest_closes_the_same_version(self, db):
        """실패는 진행 중이던 버전을 닫는다 — 같은 시도가 두 줄이 되면 안 된다."""
        created = await intake(db, source_url="https://youtu.be/async000006")
        summarize = FakeSummarizer(fail_times=1)
        await start_preparation(db, created.item_id, fetch=_fetch_ok, summarize=summarize)

        item = await db.get(QueueItem, created.item_id)
        result = await harvest_preparation(db, item, summarize=summarize)

        assert result.status == "prepare_failed" and item.status == "prepare_failed"
        preps = (
            await db.scalars(
                select(ItemPreparation).where(ItemPreparation.item_id == item.id)
            )
        ).all()
        assert [(p.version, p.status) for p in preps] == [(1, "failed")]
        task = await db.get(AITask, preps[0].ai_task_id)
        assert task.status == "failed"
        # 수집 결과는 실패해도 남는다 — 재시도 판단의 근거다.
        assert preps[0].payload["source"]["content"] == "원문 본문"
