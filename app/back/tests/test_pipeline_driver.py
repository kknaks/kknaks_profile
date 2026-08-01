"""백그라운드 드라이버 (KDEV-WORK-016 / KDEV-SPEC-009 「실행은 비동기다」).

요청은 제출까지만 하고, 그 뒤를 드라이버가 이어받는다. 여기서 고정하는 것은 셋이다.

    1. 접수 하나로 수집 → 요약 → 첫 게이트 제안까지 간다
    2. **게이트가 열리면 멈춘다** — 승인은 사람의 몫이다
    3. 재시작해도 이어붙는다 (`recover`)
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import AITask, Gate, GateRevision, ItemPreparation, QueueItem
from service.pipeline import intake, runtime
from tests.fakes import FakeAutoStage, FakeRunner, FakeSummarizer, InlineDriver

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")

ROUTE_PAYLOAD = {
    "destinations": {
        "reference": {"enabled": True},
        "concept": {"enabled": False},
        "derived": {"enabled": False},
    },
    "exclusive": None,
}


async def _fetch_ok(url):
    return {"url": url, "content": "원문 본문"}


async def _fetch_fail(url):
    raise RuntimeError("no transcript")


@pytest.fixture
async def world():
    """실 DB 트랜잭션에 묶인 드라이버 한 벌. 끝나면 전부 롤백."""
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()

    def session_factory():
        return AsyncSession(
            bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )

    def build(*, fetch=_fetch_ok, summarizer=None, runner=None, auto_stages=None, stages=None):
        summarizer = summarizer or FakeSummarizer(summary="요약본")
        runner = runner or FakeRunner(payload=ROUTE_PAYLOAD)
        runtime._registry.clear()
        driver = InlineDriver(session_factory=session_factory, fetch=fetch)
        runtime.register(
            summarizer=summarizer,
            stages=stages or {"route": runner, "source_note": runner},
            auto_stages=auto_stages,
            driver=driver,
        )
        return driver, summarizer, runner

    build.session_factory = session_factory  # type: ignore[attr-defined]
    try:
        yield build
    finally:
        runtime._registry.clear()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


async def _new_item(session_factory, url: str) -> int:
    async with session_factory() as db:
        created = await intake(db, source_url=url, source_kind="youtube")
        await db.commit()
    return created.item_id


@needs_db
class TestDrive:
    async def test_one_follow_walks_to_the_first_gate(self, world):
        """접수 하나로 수집·요약·route 제안까지 간다 — 요청은 아무것도 기다리지 않았다."""
        driver, summarizer, runner = world()
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00001")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            gate = await db.scalar(select(Gate).where(Gate.item_id == item_id))
            revision = await db.get(GateRevision, gate.active_revision_id)
            prep = await db.scalar(
                select(ItemPreparation).where(ItemPreparation.item_id == item_id)
            )

        assert item.status == "in_review"
        assert prep.status == "succeeded" and prep.payload["summary"] == "요약본"
        assert gate.stage_name == "route" and gate.status == "review_pending"
        assert revision.status == "reviewable" and revision.payload == ROUTE_PAYLOAD
        # 수집도 드라이버가 했다 — 접수 요청 안에서 돌지 않는다.
        assert summarizer.calls[0][0]["content"] == "원문 본문"

    async def test_driver_stops_at_the_human(self, world):
        """게이트가 열리면 멈춘다. 승인 없이 다음 스테이지로 넘어가면 안 된다."""
        driver, _, runner = world()
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00002")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            gates = (
                await db.scalars(select(Gate).where(Gate.item_id == item_id))
            ).all()
        assert [g.stage_name for g in gates] == ["route"]
        # route 제안 한 번 — 뒤 스테이지를 미리 만들지 않았다.
        assert len(runner.calls) == 1

    async def test_pending_execution_leaves_it_in_flight(self, world):
        """아직 안 끝난 실행을 억지로 닫지 않는다."""
        driver, _, _ = world(summarizer=FakeSummarizer(pending=True))
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00003")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            prep = await db.scalar(
                select(ItemPreparation).where(ItemPreparation.item_id == item_id)
            )
        assert item.status == "preparing" and prep.status == "running"

    async def test_collect_failure_ends_as_state_not_exception(self, world):
        """수집이 막히고 메모도 없으면 AI 를 부르지 않고 실패로 남긴다."""
        driver, summarizer, _ = world(fetch=_fetch_fail)
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00004")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
        assert item.status == "prepare_failed"
        assert summarizer.calls == []

    async def test_driver_failure_does_not_escape(self, world):
        """제출이 터져도 예외가 새어 나오지 않고 상태로 남는다."""
        driver, _, _ = world()
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00005")

        class Exploding(FakeSummarizer):
            async def submit(self, **kwargs):
                raise RuntimeError("broker down")

        runtime.register(summarizer=Exploding())
        await driver.follow(item_id)  # 예외가 새어 나오면 여기서 터진다

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
        assert item.status == "prepare_failed"


@needs_db
class TestRecover:
    async def test_recover_picks_up_in_flight_items(self, world):
        """재시작 뒤에도 진행 중이던 것을 다시 따라붙는다."""
        driver, _, _ = world(summarizer=FakeSummarizer(pending=True))
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00006")
        await driver.follow(item_id)  # preparing 에서 멈춘다

        # 새 프로세스가 뜬 셈 — 드라이버를 새로 만들고 복구시킨다.
        reborn, _, _ = world(summarizer=FakeSummarizer(summary="이어받은 요약"))
        count = await reborn.recover()

        assert count >= 1
        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            prep = await db.scalar(
                select(ItemPreparation).where(ItemPreparation.item_id == item_id)
            )
        assert item.status == "in_review"
        assert prep.payload["summary"] == "이어받은 요약"

    async def test_recover_leaves_the_human_turn_alone(self, world):
        """검토 대기 중인 항목은 복구가 건드리지 않는다 — 밀 것이 없다."""
        driver, _, runner = world()
        item_id = await _new_item(world.session_factory, "https://youtu.be/drive00007")
        await driver.follow(item_id)  # review_pending 까지 간다
        submitted = len(runner.calls)

        await driver.recover()

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            gates = (await db.scalars(select(Gate).where(Gate.item_id == item_id))).all()
        assert item.status == "in_review"
        assert [g.status for g in gates] == ["review_pending"]
        assert len(runner.calls) == submitted  # 재제출 없음


async def _new_daily_item(session_factory, note: str) -> int:
    async with session_factory() as db:
        created = await intake(db, note=note, source_kind="daily_commit")
        await db.commit()
    return created.item_id


def _daily_stages(**overrides):
    """잔디의 auto 스테이지 셋. `investigate` 만 fan-out 이다."""
    stages = {
        "collect": FakeAutoStage(stages=("collect",), submits=0, piece={"collect": "조사"}),
        "investigate": FakeAutoStage(
            stages=("investigate",), submits=3, piece={"investigate": "레포별"}
        ),
        "compose": FakeAutoStage(stages=("compose",), submits=1, piece={"compose": "초안"}),
    }
    stages.update(overrides)
    return stages


@needs_db
class TestDailyCommitRail:
    """auto 스테이지 셋을 정의 순서로 지나 `daily` 게이트까지 (KDEV-WORK-017 P2).

    유튜브는 준비가 한 번이라 이 경로를 밟지 않는다 — 여기서만 검증된다.
    """

    async def test_three_auto_stages_then_daily_gate(self, world):
        auto = _daily_stages()
        gate_runner = FakeRunner(payload={"daily": {"summary": []}})
        driver, _, _ = world(auto_stages=auto, stages={"daily": gate_runner})
        item_id = await _new_daily_item(world.session_factory, "2026-08-01 잔디")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            preps = (
                await db.scalars(
                    select(ItemPreparation)
                    .where(ItemPreparation.item_id == item_id)
                    .order_by(ItemPreparation.version)
                )
            ).all()
            gates = (await db.scalars(select(Gate).where(Gate.item_id == item_id))).all()

        # 스테이지마다 준비 버전 하나씩, 정의 순서대로.
        assert [p.payload.get("stage") for p in preps] == ["collect", "investigate", "compose"]
        assert all(p.status == "succeeded" for p in preps)
        # 게이트는 정의에서 골라야 한다 — route 가 아니라 daily 다.
        assert [g.stage_name for g in gates] == ["daily"]
        assert item.status == "in_review"

    async def test_payload_accumulates_across_stages(self, world):
        """앞 스테이지 산출물이 뒤로 흘러야 한다 — `latest_preparation` 이 하나만 집는다."""
        auto = _daily_stages()
        driver, _, _ = world(
            auto_stages=auto, stages={"daily": FakeRunner(payload={})}
        )
        item_id = await _new_daily_item(world.session_factory, "누적 확인")

        await driver.follow(item_id)

        # compose 가 받은 prior 에 앞 둘의 산출물이 다 들어 있다.
        assert auto["compose"].submitted[-1]["collect"] == "조사"
        assert auto["compose"].submitted[-1]["investigate"] == "레포별"

        async with world.session_factory() as db:
            last = await db.scalar(
                select(ItemPreparation)
                .where(ItemPreparation.item_id == item_id)
                .order_by(ItemPreparation.version.desc())
                .limit(1)
            )
        assert last.payload["collect"] == "조사"
        assert last.payload["compose"] == "초안"

    async def test_fan_out_submits_one_execution_per_repo(self, world):
        """`investigate` 는 N 건을 낸다 — 단일 `ai_task_id` 로는 못 가리킨다."""
        auto = _daily_stages()
        driver, _, _ = world(auto_stages=auto, stages={"daily": FakeRunner(payload={})})
        item_id = await _new_daily_item(world.session_factory, "fan-out")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            tasks = (
                await db.scalars(
                    select(AITask).where(
                        AITask.item_id == item_id, AITask.kind == "investigate"
                    )
                )
            ).all()
            prep = await db.scalar(
                select(ItemPreparation).where(
                    ItemPreparation.item_id == item_id,
                    ItemPreparation.payload["stage"].astext == "investigate",
                )
            )
        assert len(tasks) == 3
        assert all(t.status == "succeeded" for t in tasks)
        assert prep.ai_task_id is None  # N 건이라 비운다
        assert auto["investigate"].parsed[-1] == [f"result:investigate-{i}" for i in (1, 2, 3)]

    async def test_partial_failure_still_advances(self, world):
        """레포 하나가 막혀도 나머지로 간다 (SPEC-011 §5)."""
        auto = _daily_stages(
            investigate=FakeAutoStage(
                stages=("investigate",), submits=3, fail_times=1, piece={"investigate": "일부"}
            )
        )
        driver, _, _ = world(auto_stages=auto, stages={"daily": FakeRunner(payload={})})
        item_id = await _new_daily_item(world.session_factory, "부분 실패")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            gates = (await db.scalars(select(Gate).where(Gate.item_id == item_id))).all()
        assert [g.stage_name for g in gates] == ["daily"]  # 게이트는 열린다
        assert item.status == "in_review"
        assert len(auto["investigate"].parsed[-1]) == 2  # 성공분 둘만 넘어갔다

    async def test_all_failed_closes_the_stage(self, world):
        """전 레포 실패는 스테이지 실패다 — 재시도를 열어 둔다."""
        auto = _daily_stages(
            investigate=FakeAutoStage(stages=("investigate",), submits=2, fail_times=2)
        )
        driver, _, _ = world(auto_stages=auto, stages={"daily": FakeRunner(payload={})})
        item_id = await _new_daily_item(world.session_factory, "전부 실패")

        await driver.follow(item_id)

        async with world.session_factory() as db:
            item = await db.get(QueueItem, item_id)
            gates = (await db.scalars(select(Gate).where(Gate.item_id == item_id))).all()
        assert item.status == "prepare_failed"
        assert gates == []  # 게이트를 열지 않는다
