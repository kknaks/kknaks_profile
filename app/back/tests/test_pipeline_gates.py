"""게이트 공통 계약 + route (KDEV-WORK-014 P3 / KDEV-SPEC-008·009).

여기서 지키는 것은 **세 상태를 섞지 않는 것**이다. 게이트가 `review_pending` 인데
실행은 `succeeded` 이고 버전은 `reviewable` 인 것이 정상이다 — 합치면 "AI 가 실패한 것"과
"사람이 아직 안 본 것"이 구분되지 않는다.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import AITask, Gate, GateRevision, QueueItem
from service.pipeline import gates as gates_service
from service.pipeline import intake, prepare_and_open_gate
from service.pipeline.gates import GateError, GenerationResult, open_first_gate
from service.pipeline.route import route_outcome, validate_route_result

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")

GROUPS = frozenset({"study", "ai_skills"})


def _route_payload(*, reference=True, concept=True, derived=False, exclusive=None, group="study"):
    destinations = {
        "reference": {"enabled": reference, "group": group},
        "concept": {"enabled": concept},
        "derived": {"enabled": derived},
    }
    return {"destinations": destinations, "exclusive": exclusive, "rationale": "근거"}


# --- route 결과 검증 (DB 불필요) ---------------------------------------------


class TestValidateRouteResult:
    def test_normalizes_valid_payload(self):
        result = validate_route_result(_route_payload(), groups=GROUPS)
        assert result["destinations"]["reference"] == {"enabled": True, "group": "study"}
        assert result["destinations"]["derived"] == {"enabled": False}
        assert result["exclusive"] is None

    def test_unknown_group_rejected(self):
        """group 은 `persona/_meta.yaml` 의 clusters 값이어야 한다 — 아니면 로더가 터진다."""
        with pytest.raises(GateError) as exc:
            validate_route_result(_route_payload(group="없는그룹"), groups=GROUPS)
        assert exc.value.code == "INVALID_REFERENCE_GROUP"

    def test_group_not_required_when_reference_off(self):
        payload = _route_payload(reference=False, group="")
        assert validate_route_result(payload, groups=GROUPS)["destinations"]["reference"] == {
            "enabled": False
        }

    def test_exclusive_with_destination_rejected(self):
        """둘 다면 무엇이 우선인지 알 수 없다 — 조용히 한쪽을 고르지 않는다."""
        with pytest.raises(GateError):
            validate_route_result(_route_payload(exclusive="discard"), groups=GROUPS)

    def test_nothing_selected_requires_exclusive(self):
        with pytest.raises(GateError):
            validate_route_result(
                _route_payload(reference=False, concept=False, derived=False), groups=GROUPS
            )

    def test_hold_and_discard_are_both_valid(self):
        for value in ("inbox_hold", "discard"):
            payload = _route_payload(
                reference=False, concept=False, derived=False, exclusive=value
            )
            assert validate_route_result(payload, groups=GROUPS)["exclusive"] == value

    @pytest.mark.parametrize("bad", [None, [], "문자열", {}, {"destinations": "x"}])
    def test_malformed_rejected(self, bad):
        with pytest.raises(GateError):
            validate_route_result(bad, groups=GROUPS)

    def test_outcome_only_discard_ends_item(self):
        """`inbox_hold` 는 끝이 아니다 — inbox 노트를 남기는 발행이 남아 있다."""
        assert route_outcome({"exclusive": "discard"}) == "discarded"
        assert route_outcome({"exclusive": "inbox_hold"}) == "publishable"
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


class Recorder:
    """호출 이력을 남기는 generator. 실패·세션을 흉내 낸다."""

    def __init__(self, *, payload=None, session_ref="sess-1", fail_times=0) -> None:
        self.payload = payload or _route_payload()
        self.session_ref = session_ref
        self.fail_times = fail_times
        self.calls: list = []

    async def __call__(self, request):
        self.calls.append(request)
        if self.fail_times > 0:
            self.fail_times -= 1
            raise RuntimeError("provider timeout")
        return GenerationResult(payload=self.payload, session_ref=self.session_ref)


async def _ready_item(db, *, url: str, kind: str = "youtube") -> QueueItem:
    created = await intake(db, source_url=url, source_kind=kind)
    item = await db.get(QueueItem, created.item_id)
    item.status = "in_review"
    await db.flush()
    return item


async def _fetch_ok(url):
    return {"url": url, "content": "본문"}


async def _summarize_ok(*, material, note):
    from service.pipeline import SummaryResult

    return SummaryResult(summary="요약본", session_ref="prep-sess")


@needs_db
class TestOpenGate:
    async def test_prepare_success_opens_route_gate(self, db):
        """준비가 끝나면 첫 게이트가 자동으로 열린다 (SPEC-007 S-1 4항)."""
        created = await intake(db, source_url="https://youtu.be/gateopen001")
        generator = Recorder()
        result = await prepare_and_open_gate(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok, generator=generator
        )
        assert result.ok

        gate = await db.scalar(select(Gate).where(Gate.item_id == created.item_id))
        assert gate.stage_name == "route" and gate.stage_no == 3
        assert gate.status == "review_pending"
        revision = await db.get(GateRevision, gate.active_revision_id)
        assert revision.version == 1 and revision.status == "reviewable"

    async def test_generator_receives_summary_not_raw_only(self, db):
        """route 판단의 근거는 요약이다 — 자막 원문을 그대로 읽히지 않는다."""
        created = await intake(db, source_url="https://youtu.be/gatesumm001")
        generator = Recorder()
        await prepare_and_open_gate(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok, generator=generator
        )
        request = generator.calls[0]
        assert request.preparation is not None
        assert request.preparation.payload["summary"] == "요약본"

    async def test_unknown_pipeline_leaves_item_without_gate(self, db):
        """정의 없는 종류에 유튜브 체인을 갖다 붙이지 않는다."""
        item = await _ready_item(db, url="https://blog.example.com/x", kind="blog")
        gate = await open_first_gate(db, item, generator=Recorder())
        assert gate is None

    async def test_no_generator_keeps_prepare_result(self, db):
        """AI 경로가 없어도 준비 결과를 버리지 않는다 — 게이트는 나중에 열 수 있다."""
        created = await intake(db, source_url="https://youtu.be/nogen000001")
        result = await prepare_and_open_gate(
            db, created.item_id, fetch=_fetch_ok, summarize=_summarize_ok, generator=None
        )
        assert result.ok
        assert await db.scalar(select(Gate).where(Gate.item_id == created.item_id)) is None


@needs_db
class TestFeedbackAndRegenerate:
    async def test_v1_survives_as_read_only(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback001")
        generator = Recorder()
        gate = await open_first_gate(db, item, generator=generator)
        v1_id = gate.active_revision_id

        await gates_service.submit_feedback(db, gate, "concept 를 하나로 합쳐 달라")
        assert gate.status == "feedback_pending"
        v2 = await gates_service.regenerate(db, gate, item=item, generator=generator)

        v1 = await db.get(GateRevision, v1_id)
        assert v1.status == "superseded"      # 밀려났지만
        assert v1.payload is not None          # 내용은 그대로 남는다
        assert v2.version == 2 and v2.status == "reviewable"
        assert v2.parent_revision_id == v1_id
        assert gate.active_revision_id == v2.id

    async def test_feedback_reaches_generator(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback002")
        generator = Recorder()
        gate = await open_first_gate(db, item, generator=generator)
        await gates_service.submit_feedback(db, gate, "derived 도 켜 달라")
        await gates_service.regenerate(db, gate, item=item, generator=generator)

        assert generator.calls[-1].feedback == "derived 도 켜 달라"
        assert generator.calls[-1].previous_payload is not None

    async def test_feedback_is_consumed_once(self, db):
        item = await _ready_item(db, url="https://youtu.be/feedback003")
        generator = Recorder()
        gate = await open_first_gate(db, item, generator=generator)
        feedback = await gates_service.submit_feedback(db, gate, "합쳐 달라")
        await gates_service.regenerate(db, gate, item=item, generator=generator)
        assert feedback.status == "consumed"

    async def test_two_regenerations_leave_one_reviewable(self, db):
        """게이트당 검토 대상은 항상 하나 (SPEC-009 S-3)."""
        item = await _ready_item(db, url="https://youtu.be/sweep000001")
        generator = Recorder()
        gate = await open_first_gate(db, item, generator=generator)

        for _ in range(2):
            await gates_service.submit_feedback(db, gate, "다시 해 달라")
            await gates_service.regenerate(db, gate, item=item, generator=generator)

        revisions = (
            await db.scalars(select(GateRevision).where(GateRevision.gate_id == gate.id))
        ).all()
        assert len(revisions) == 3
        assert [r.status for r in revisions if r.status == "reviewable"] == ["reviewable"]

    async def test_short_feedback_rejected(self, db):
        item = await _ready_item(db, url="https://youtu.be/short00001")
        gate = await open_first_gate(db, item, generator=Recorder())
        with pytest.raises(GateError) as exc:
            await gates_service.submit_feedback(db, gate, "응")
        assert exc.value.code == "FEEDBACK_TOO_SHORT"

    async def test_session_is_resumed(self, db):
        """원문·지침 재전송 없이 피드백만 반영하려면 세션이 이어져야 한다."""
        item = await _ready_item(db, url="https://youtu.be/session0001")
        generator = Recorder(session_ref="sess-abc")
        gate = await open_first_gate(db, item, generator=generator)
        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        await gates_service.regenerate(db, gate, item=item, generator=generator)

        assert generator.calls[-1].session_ref == "sess-abc"

    async def test_missing_session_does_not_fail(self, db):
        """세션이 없으면 stateless 로 만든다 — 실패시키지 않는다 (SPEC-009 S-5)."""
        item = await _ready_item(db, url="https://youtu.be/nosession01")
        generator = Recorder(session_ref=None)
        gate = await open_first_gate(db, item, generator=generator)
        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        revision = await gates_service.regenerate(db, gate, item=item, generator=generator)

        assert generator.calls[-1].session_ref is None
        assert revision.status == "reviewable"


@needs_db
class TestFailureAndRetry:
    async def test_failure_marks_gate_and_keeps_rows(self, db):
        item = await _ready_item(db, url="https://youtu.be/genfail0001")
        generator = Recorder(fail_times=1)
        gate = await open_first_gate(db, item, generator=generator)

        assert gate.status == "failed"
        revision = await db.scalar(select(GateRevision).where(GateRevision.gate_id == gate.id))
        assert revision.status == "failed" and revision.payload is None
        task = await db.scalar(select(AITask).where(AITask.item_id == item.id))
        assert task.status == "failed" and "provider timeout" in task.error_message

    async def test_retry_creates_new_run_linked_to_failure(self, db):
        item = await _ready_item(db, url="https://youtu.be/genretry001")
        generator = Recorder(fail_times=1)
        gate = await open_first_gate(db, item, generator=generator)

        revision = await gates_service.retry(db, gate, item=item, generator=generator)
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
        gate = await open_first_gate(db, item, generator=Recorder())
        with pytest.raises(GateError) as exc:
            await gates_service.retry(db, gate, item=item, generator=Recorder())
        assert exc.value.code == "RETRY_NOT_ALLOWED"


@needs_db
class TestApprove:
    async def test_approve_locks_revision(self, db):
        item = await _ready_item(db, url="https://youtu.be/approve0001")
        gate = await open_first_gate(db, item, generator=Recorder())
        revision = await gates_service.approve(db, gate)

        assert gate.status == "approved"
        assert gate.approved_revision_id == revision.id
        assert revision.status == "approved"

    async def test_approved_gate_rejects_feedback(self, db):
        """승인된 단계는 변경할 수 없다 — 되돌리려면 route 재오픈뿐이다(D5)."""
        item = await _ready_item(db, url="https://youtu.be/approve0002")
        gate = await open_first_gate(db, item, generator=Recorder())
        await gates_service.approve(db, gate)

        with pytest.raises(GateError) as exc:
            await gates_service.submit_feedback(db, gate, "역시 아닌 것 같다")
        assert exc.value.code == "GATE_ALREADY_APPROVED"

    async def test_human_edit_becomes_the_approved_content(self, db):
        """AI 제안 그대로가 아니라 **사람이 고친 결과**가 승인 대상이다."""
        item = await _ready_item(db, url="https://youtu.be/approve0003")
        gate = await open_first_gate(db, item, generator=Recorder())
        edited = _route_payload(concept=False, derived=True)

        revision = await gates_service.approve(db, gate, payload_override=edited)
        assert revision.payload["destinations"]["concept"] == {"enabled": False}
        assert revision.payload["destinations"]["derived"] == {"enabled": True}

    async def test_stale_revision_id_is_rejected(self, db):
        """다른 탭에서 재생성이 돌았는데 옛 화면의 승인이 먹으면 안 본 내용을 승인하게 된다."""
        item = await _ready_item(db, url="https://youtu.be/approve0004")
        generator = Recorder()
        gate = await open_first_gate(db, item, generator=generator)
        stale_id = gate.active_revision_id

        await gates_service.submit_feedback(db, gate, "다시 판단해 달라")
        await gates_service.regenerate(db, gate, item=item, generator=generator)

        with pytest.raises(GateError) as exc:
            await gates_service.approve(db, gate, expected_revision_id=stale_id)
        assert exc.value.code == "STALE_REVISION"

    async def test_failed_gate_cannot_be_approved(self, db):
        item = await _ready_item(db, url="https://youtu.be/approve0005")
        gate = await open_first_gate(db, item, generator=Recorder(fail_times=1))
        with pytest.raises(GateError):
            await gates_service.approve(db, gate)
