"""게이트 공통 계약 + route (KDEV-WORK-014 P3 / KDEV-SPEC-008·009).

여기서 지키는 것은 **세 상태를 섞지 않는 것**이다. 게이트가 `review_pending` 인데
실행은 `succeeded` 이고 버전은 `reviewable` 인 것이 정상이다 — 합치면 "AI 가 실패한 것"과
"사람이 아직 안 본 것"이 구분되지 않는다.

실행이 비동기가 된 뒤(KDEV-WORK-016)로 게이트를 여는 것은 **제출까지**다. 내용은
`harvest()` 가 채운다 — 테스트도 그 두 단계를 그대로 밟는다.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import AITask, Gate, GateRevision, QueueItem
from service.pipeline import gates as gates_service
from service.pipeline import intake
from service.pipeline.gates import GateError, harvest, open_first_gate
from service.pipeline.route import route_outcome, validate_route_result
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

def _route_payload(*, reference=True, concept=True, derived=False, exclusive=None):
    destinations = {
        "reference": {"enabled": reference},
        "concept": {"enabled": concept},
        "derived": {"enabled": derived},
    }
    return {"destinations": destinations, "exclusive": exclusive, "rationale": "근거"}


# --- route 결과 검증 (DB 불필요) ---------------------------------------------


class TestValidateRouteResult:
    def test_normalizes_valid_payload(self):
        result = validate_route_result(_route_payload())
        assert result["destinations"]["reference"] == {"enabled": True}
        assert result["destinations"]["derived"] == {"enabled": False}
        assert result["exclusive"] is None

    def test_exclusive_with_destination_rejected(self):
        """둘 다면 무엇이 우선인지 알 수 없다 — 조용히 한쪽을 고르지 않는다."""
        with pytest.raises(GateError):
            validate_route_result(_route_payload(exclusive="discard"))

    def test_nothing_selected_requires_exclusive(self):
        with pytest.raises(GateError):
            validate_route_result(
                _route_payload(reference=False, concept=False, derived=False)
            )

    def test_discard_is_the_only_exclusive(self):
        """`inbox_hold` 는 KDEV-DEC-021 로 폐기됐다 — `inbox/` 는 입구다."""
        payload = _route_payload(
            reference=False, concept=False, derived=False, exclusive="discard"
        )
        assert validate_route_result(payload)["exclusive"] == "discard"

        with pytest.raises(GateError):
            validate_route_result(
                _route_payload(
                    reference=False, concept=False, derived=False, exclusive="inbox_hold"
                )
            )

    @pytest.mark.parametrize("bad", [None, [], "문자열", {}, {"destinations": "x"}])
    def test_malformed_rejected(self, bad):
        with pytest.raises(GateError):
            validate_route_result(bad)

    def test_outcome_only_discard_ends_item(self):
        assert route_outcome({"exclusive": "discard"}) == "discarded"
        assert route_outcome({"exclusive": None}) == "publishable"


# --- 게이트 절차 -------------------------------------------------------------


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


def Recorder(*, payload=None, session_ref="sess-1", fail_times=0, pending=False):
    """route 결과를 내는 가짜 실행기."""
    return FakeRunner(
        payload=payload or _route_payload(),
        session_ref=session_ref,
        fail_times=fail_times,
        pending=pending,
    )


async def _open(db, item, *, runner, harvested: bool = True) -> Gate:
    """게이트를 열고(제출) 바로 한 번 수확한다 — 화면 폴링 한 번에 해당한다."""
    gate = await open_first_gate(db, item, runner=runner)
    if harvested and gate is not None:
        await harvest(db, gate, item=item, runner=runner)
    return gate


async def _ready_item(db, *, url: str, kind: str = "youtube") -> QueueItem:
    created = await intake(db, source_url=url, source_kind=kind)
    item = await db.get(QueueItem, created.item_id)
    item.status = "in_review"
    await db.flush()
    return item


async def _reviewable_gate(db, stage_name: str, payload: dict):
    """`reviewable` 리비전 하나를 가진 게이트를 직접 만든다.

    실행기를 태우지 않는다 — 여기서 보는 것은 **승인이 payload 를 어떻게 다루는가**
    한 가지라, 생성 경로를 끼우면 검증 대상이 흐려진다.
    """
    item = await _ready_item(db, url=f"https://x.test/{stage_name}-{len(payload)}")
    gate = Gate(item_id=item.id, stage_name=stage_name, stage_no=1, status="review_pending")
    db.add(gate)
    await db.flush()
    revision = GateRevision(
        gate_id=gate.id, version=1, status="reviewable", payload=payload
    )
    db.add(revision)
    await db.flush()
    gate.active_revision_id = revision.id
    await db.flush()
    return gate, revision


async def _fetch_ok(url):
    return {"url": url, "content": "본문"}


def _summarize_ok():
    return FakeSummarizer(summary="요약본", session_ref="prep-sess")


@needs_db
class TestOpenGate:
    async def test_prepare_success_opens_route_gate(self, db):
        """준비가 끝나면 첫 게이트가 자동으로 열린다 (SPEC-007 S-1 4항).

        열리는 시점에는 **제출만** 돼 있다 — 내용은 수확이 채운다 (SPEC-009).
        """
        created = await intake(db, source_url="https://youtu.be/gateopen001")
        runner = Recorder()
        result = await prepare(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok(), runner=runner
        )
        assert result.ok

        gate = await db.scalar(select(Gate).where(Gate.item_id == created.item_id))
        assert gate.stage_name == "route" and gate.stage_no == 3
        assert gate.status == "generating"
        assert gate.active_revision_id is None  # 아직 검토 대상이 아니다

        revision = await db.scalar(select(GateRevision).where(GateRevision.gate_id == gate.id))
        assert revision.version == 1 and revision.status == "drafting"
        assert revision.payload is None

        task = await db.get(AITask, revision.ai_task_id)
        assert task.status == "running"
        # 이 참조가 있어야 back 이 재시작해도 실행기 큐에서 다시 찾는다.
        assert task.external_task_ref == "task-1"

    async def test_harvest_fills_the_proposal(self, db):
        """폴링이 완료를 감지하면 그때 검토 대기가 된다."""
        created = await intake(db, source_url="https://youtu.be/gateharv001")
        runner = Recorder()
        await prepare(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok(), runner=runner
        )
        gate = await db.scalar(select(Gate).where(Gate.item_id == created.item_id))
        item = await db.get(QueueItem, created.item_id)

        assert await harvest(db, gate, item=item, runner=runner) is True
        assert gate.status == "review_pending"
        revision = await db.get(GateRevision, gate.active_revision_id)
        assert revision.version == 1 and revision.status == "reviewable"
        assert revision.payload is not None
        task = await db.get(AITask, revision.ai_task_id)
        assert task.status == "succeeded" and task.finished_at is not None

    async def test_harvest_is_idempotent(self, db):
        """조회를 두 번 해도 revision 이 하나만 생긴다 (WORK-016 P1 검증)."""
        item = await _ready_item(db, url="https://youtu.be/gateidem001")
        runner = Recorder()
        gate = await open_first_gate(db, item, runner=runner)

        assert await harvest(db, gate, item=item, runner=runner) is True
        assert await harvest(db, gate, item=item, runner=runner) is False

        revisions = (
            await db.scalars(select(GateRevision).where(GateRevision.gate_id == gate.id))
        ).all()
        assert len(revisions) == 1
        assert len(runner.calls) == 1  # 재제출도 없다

    async def test_running_execution_changes_nothing(self, db):
        """아직 안 끝났으면 게이트는 그대로 `generating` 이다."""
        item = await _ready_item(db, url="https://youtu.be/gatehold001")
        runner = Recorder(pending=True)
        gate = await open_first_gate(db, item, runner=runner)

        assert await harvest(db, gate, item=item, runner=runner) is False
        assert gate.status == "generating"
        revision = await db.scalar(select(GateRevision).where(GateRevision.gate_id == gate.id))
        assert revision.status == "drafting" and revision.payload is None

    async def test_harvest_resumes_after_restart(self, db):
        """back 이 재시작해도 이어 수확한다 — 재료를 DB 에서 다시 조립하기 때문이다."""
        item = await _ready_item(db, url="https://youtu.be/gaterest001")
        submitter = Recorder(pending=True)
        gate = await open_first_gate(db, item, runner=submitter)
        await harvest(db, gate, item=item, runner=submitter)

        # 제출한 객체를 잃어버린 상태 — 새 런타임이 같은 task_id 를 수확한다.
        reborn = Recorder()
        assert await harvest(db, gate, item=item, runner=reborn) is True
        assert reborn.polled == ["task-1"]
        assert gate.status == "review_pending"
        assert reborn.parsed[0].item.id == item.id

    async def test_generator_receives_summary_not_raw_only(self, db):
        """route 판단의 근거는 요약이다 — 자막 원문을 그대로 읽히지 않는다."""
        created = await intake(db, source_url="https://youtu.be/gatesumm001")
        runner = Recorder()
        await prepare(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok(), runner=runner
        )
        request = runner.calls[0]
        assert request.preparation is not None
        assert request.preparation.payload["summary"] == "요약본"

    async def test_unknown_pipeline_leaves_item_without_gate(self, db):
        """정의 없는 종류에 유튜브 체인을 갖다 붙이지 않는다."""
        item = await _ready_item(db, url="https://blog.example.com/x", kind="blog")
        gate = await open_first_gate(db, item, runner=Recorder())
        assert gate is None

    async def test_no_generator_keeps_prepare_result(self, db):
        """AI 경로가 없어도 준비 결과를 버리지 않는다 — 게이트는 나중에 열 수 있다."""
        created = await intake(db, source_url="https://youtu.be/nogen000001")
        result = await prepare(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok(), runner=None
        )
        assert result.ok
        assert await db.scalar(select(Gate).where(Gate.item_id == created.item_id)) is None


async def _regenerate(db, gate, *, item, runner):
    """피드백 반영본을 제출하고 수확한다."""
    revision = await gates_service.regenerate(db, gate, item=item, runner=runner)
    await harvest(db, gate, item=item, runner=runner)
    return revision


@needs_db
class TestFeedbackAndRegenerate:
    async def test_v1_survives_as_read_only(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback001")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)
        v1_id = gate.active_revision_id

        await gates_service.submit_feedback(db, gate, "concept 를 하나로 합쳐 달라")
        assert gate.status == "feedback_pending"
        v2 = await _regenerate(db, gate, item=item, runner=runner)

        v1 = await db.get(GateRevision, v1_id)
        assert v1.status == "superseded"      # 밀려났지만
        assert v1.payload is not None          # 내용은 그대로 남는다
        assert v2.version == 2 and v2.status == "reviewable"
        assert v2.parent_revision_id == v1_id
        assert gate.active_revision_id == v2.id

    async def test_regeneration_responds_before_the_new_version_exists(self, db):
        """재생성 요청은 즉시 끝난다 — v1 은 그때까지 화면에 그대로 있다."""
        item = await _ready_item(db, url="https://youtu.be/feedback004")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)
        v1_id = gate.active_revision_id

        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        runner.pending = True  # 재생성은 아직 실행기 큐에 있다
        v2 = await gates_service.regenerate(db, gate, item=item, runner=runner)

        assert gate.status == "regenerating"
        assert v2.status == "drafting" and v2.payload is None
        # 아직 v1 이 검토 대상이다 — 빈 카드를 보여주지 않는다.
        assert gate.active_revision_id == v1_id

    async def test_feedback_reaches_generator(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback002")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)
        await gates_service.submit_feedback(db, gate, "derived 도 켜 달라")
        await _regenerate(db, gate, item=item, runner=runner)

        assert runner.calls[-1].feedback == "derived 도 켜 달라"
        assert runner.calls[-1].previous_payload is not None

    async def test_feedback_is_consumed_once(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback003")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)
        feedback = await gates_service.submit_feedback(db, gate, "합쳐 달라")
        await _regenerate(db, gate, item=item, runner=runner)
        assert feedback.status == "consumed"

    async def test_two_regenerations_leave_one_reviewable(self, db):
        """게이트당 검토 대상은 항상 하나 (SPEC-009 S-3)."""
        item = await _ready_item(db, url="https://youtu.be/sweep000001")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)

        for _ in range(2):
            await gates_service.submit_feedback(db, gate, "다시 해 달라")
            await _regenerate(db, gate, item=item, runner=runner)

        revisions = (
            await db.scalars(select(GateRevision).where(GateRevision.gate_id == gate.id))
        ).all()
        assert len(revisions) == 3
        assert [r.status for r in revisions if r.status == "reviewable"] == ["reviewable"]

    async def test_short_feedback_rejected(self, db):
        item = await _ready_item(db, url="https://youtu.be/short00001")
        gate = await _open(db, item, runner=Recorder())
        with pytest.raises(GateError) as exc:
            await gates_service.submit_feedback(db, gate, "응")
        assert exc.value.code == "FEEDBACK_TOO_SHORT"

    async def test_session_is_resumed(self, db):
        """원문·지침 재전송 없이 피드백만 반영하려면 세션이 이어져야 한다."""
        item = await _ready_item(db, url="https://youtu.be/session0001")
        runner = Recorder(session_ref="sess-abc")
        gate = await _open(db, item, runner=runner)
        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        await _regenerate(db, gate, item=item, runner=runner)

        assert runner.calls[-1].session_ref == "sess-abc"

    async def test_missing_session_does_not_fail(self, db):
        """세션이 없으면 stateless 로 만든다 — 실패시키지 않는다 (SPEC-009 S-5)."""
        item = await _ready_item(db, url="https://youtu.be/nosession01")
        runner = Recorder(session_ref=None)
        gate = await _open(db, item, runner=runner)
        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        revision = await _regenerate(db, gate, item=item, runner=runner)

        assert runner.calls[-1].session_ref is None
        assert revision.status == "reviewable"


@needs_db
class TestFailureAndRetry:
    async def test_failure_marks_gate_and_keeps_rows(self, db):
        item = await _ready_item(db, url="https://youtu.be/genfail0001")
        runner = Recorder(fail_times=1)
        gate = await _open(db, item, runner=runner)

        assert gate.status == "failed"
        revision = await db.scalar(select(GateRevision).where(GateRevision.gate_id == gate.id))
        assert revision.status == "failed" and revision.payload is None
        task = await db.scalar(select(AITask).where(AITask.item_id == item.id))
        assert task.status == "failed" and "provider timeout" in task.error_message

    async def test_submit_failure_is_a_state_not_an_exception(self, db):
        """제출 자체가 막혀도(브로커 다운) 예외를 올리지 않고 실패로 남긴다."""

        class Broken(FakeRunner):
            async def submit(self, request):
                raise RuntimeError("broker down")

        item = await _ready_item(db, url="https://youtu.be/submitfail1")
        gate = await open_first_gate(db, item, runner=Broken())

        assert gate.status == "failed"
        task = await db.scalar(select(AITask).where(AITask.item_id == item.id))
        assert task.status == "failed" and task.external_task_ref is None

    async def test_retry_creates_new_run_linked_to_failure(self, db):
        item = await _ready_item(db, url="https://youtu.be/genretry001")
        runner = Recorder(fail_times=1)
        gate = await _open(db, item, runner=runner)

        revision = await gates_service.retry(db, gate, item=item, runner=runner)
        await harvest(db, gate, item=item, runner=runner)
        assert gate.status == "review_pending"
        assert revision.version == 2 and revision.status == "reviewable"

        tasks = (
            await db.scalars(
                select(AITask).where(AITask.item_id == item.id).order_by(AITask.id)
            )
        ).all()
        assert [t.status for t in tasks] == ["failed", "succeeded"]
        assert tasks[1].retry_of_task_id == tasks[0].id

    async def test_retry_rejected_when_not_failed(self, db):
        item = await _ready_item(db, url="https://youtu.be/noretry0001")
        gate = await _open(db, item, runner=Recorder())
        with pytest.raises(GateError) as exc:
            await gates_service.retry(db, gate, item=item, runner=Recorder())
        assert exc.value.code == "RETRY_NOT_ALLOWED"


@needs_db
class TestApprove:
    async def test_approve_locks_revision(self, db):
        item = await _ready_item(db, url="https://youtu.be/approve0001")
        gate = await _open(db, item, runner=Recorder())
        revision = await gates_service.approve(db, gate)

        assert gate.status == "approved"
        assert gate.approved_revision_id == revision.id
        assert revision.status == "approved"

    async def test_generating_gate_cannot_be_approved(self, db):
        """수확 전에는 승인할 것이 없다 — 내용 없는 버전이 확정되면 안 된다."""
        item = await _ready_item(db, url="https://youtu.be/approve0006")
        gate = await open_first_gate(db, item, runner=Recorder(pending=True))
        with pytest.raises(GateError) as exc:
            await gates_service.approve(db, gate)
        assert exc.value.code == "RETRY_NOT_ALLOWED"

    async def test_approved_gate_rejects_feedback(self, db):
        """승인된 단계는 변경할 수 없다 — 되돌리려면 route 재오픈뿐이다(D5)."""
        item = await _ready_item(db, url="https://youtu.be/approve0002")
        gate = await _open(db, item, runner=Recorder())
        await gates_service.approve(db, gate)

        with pytest.raises(GateError) as exc:
            await gates_service.submit_feedback(db, gate, "역시 아닌 것 같다")
        assert exc.value.code == "GATE_ALREADY_APPROVED"

    async def test_human_edit_becomes_the_approved_content(self, db):
        """AI 제안 그대로가 아니라 **사람이 고친 결과**가 승인 대상이다."""
        item = await _ready_item(db, url="https://youtu.be/approve0003")
        gate = await _open(db, item, runner=Recorder())
        edited = _route_payload(concept=False, derived=True)

        revision = await gates_service.approve(db, gate, payload_override=edited)
        assert revision.payload["destinations"]["concept"] == {"enabled": False}
        assert revision.payload["destinations"]["derived"] == {"enabled": True}

    async def test_stale_revision_id_is_rejected(self, db):
        """다른 탭에서 재생성이 돌았는데 옛 화면의 승인이 먹으면 안 본 내용을 승인하게 된다."""
        item = await _ready_item(db, url="https://youtu.be/approve0004")
        runner = Recorder()
        gate = await _open(db, item, runner=runner)
        stale_id = gate.active_revision_id

        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        await _regenerate(db, gate, item=item, runner=runner)

        with pytest.raises(GateError) as exc:
            await gates_service.approve(db, gate, expected_revision_id=stale_id)
        assert exc.value.code == "STALE_REVISION"

    async def test_failed_gate_cannot_be_approved(self, db):
        item = await _ready_item(db, url="https://youtu.be/approve0005")
        gate = await _open(db, item, runner=Recorder(fail_times=1))
        with pytest.raises(GateError):
            await gates_service.approve(db, gate)


class TestApproveKeepsOutputs:
    """승인이 산출물을 통째로 지우지 못하게 (KDEV-WORK-017 결함 ⑧).

    실제로 잔디 게이트가 이렇게 당했다. 화면의 concept 판정이 `"concepts" in payload`
    였는데 **잔디 payload 도 `concepts` 를 가진다** — `{daily, career, concepts,
    collection}`. 그래서 승인이 `{concepts}` 만 보냈고 `daily`·`career` 가 버려졌다.

    화면에는 「승인됨」이 떴고, 사람은 **발행에서 `EMPTY_PLAN` 을 만나서야** 알았다.
    사람이 고친 것이 조용히 사라지는 경로라 화면만 고치고 넘어가지 않는다.
    """

    async def test_dropping_the_daily_output_is_refused(self, db):
        gate, revision = await _reviewable_gate(
            db, "daily", {"daily": {"summary": {"ko": ["줄"]}}, "career": {}, "concepts": []}
        )
        with pytest.raises(GateError) as exc:
            await gates_service.approve(db, gate, payload_override={"concepts": []})
        assert exc.value.code == "PAYLOAD_KEYS_DROPPED"
        assert gate.status != "approved"

    async def test_editing_values_is_still_allowed(self, db):
        """값을 바꾸는 것은 편집이다 — 막으면 승인 화면이 무의미해진다."""
        gate, revision = await _reviewable_gate(
            db, "daily", {"daily": {"summary": {"ko": ["원본"]}}, "concepts": []}
        )
        edited = {"daily": {"summary": {"ko": ["사람이 고친 줄"]}}, "concepts": []}
        approved = await gates_service.approve(db, gate, payload_override=edited)
        assert approved.payload["daily"]["summary"]["ko"] == ["사람이 고친 줄"]

    async def test_other_stages_are_untouched(self, db):
        """route 는 `rationale` 이 정당하게 빠질 수 있어 이 가드 대상이 아니다."""
        gate, revision = await _reviewable_gate(
            db, "route", {"destinations": ["a"], "exclusive": None, "rationale": "근거"}
        )
        approved = await gates_service.approve(
            db, gate, payload_override={"destinations": ["a"], "exclusive": None}
        )
        assert "rationale" not in approved.payload


class TestPostStage:
    """공개 글은 `resources/source/` 와 **1:1** 이다 (KDEV-DEC-020 D3)."""

    POST = (
        "---\n"
        "type: post_note\n"
        "id: idempotency-basics\n"
        "title: 멱등성\n"
        "date: 2026.08.11\n"
        "up:\n"
        "  - 2026-08-10-idempotency-in-our-decisions\n"
        "---\n\n## 주제\n\n본문\n"
    )

    def test_single_up_passes(self):
        from service.pipeline.stages.post import check_post

        assert check_post("idempotency-basics", self.POST)["type"] == "post_note"

    def test_multiple_up_is_rejected(self):
        """여러 자료를 묶는 글은 이 계열이 아니다 — `up:` 하나가 그 제약이다."""
        from service.pipeline.stages.post import check_post

        two = self.POST.replace(
            "  - 2026-08-10-idempotency-in-our-decisions\n",
            "  - a\n  - b\n",
        )
        with pytest.raises(GateError):
            check_post("idempotency-basics", two)

    def test_missing_up_is_rejected(self):
        from service.pipeline.stages.post import check_post

        none = self.POST.replace(
            "up:\n  - 2026-08-10-idempotency-in-our-decisions\n", ""
        )
        with pytest.raises(GateError):
            check_post("idempotency-basics", none)

    def test_wrong_type_is_rejected(self):
        from service.pipeline.stages.post import check_post

        with pytest.raises(GateError):
            check_post("idempotency-basics", self.POST.replace("post_note", "concept"))

    def test_dated_stem_is_rejected(self):
        """자료의 날짜는 `up:` 이 가리키는 source 가 갖는다."""
        from service.pipeline.stages.post import check_post

        with pytest.raises(GateError):
            check_post("2026-08-11-idempotency", self.POST)
