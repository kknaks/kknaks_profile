"""체인 진행 + source_note 초안 (KDEV-WORK-015 P1 / SPEC-008).

**체인 길이는 route 승인이 확정한다.** 정의만으로는 다음 스테이지를 알 수 없고
route 결과를 함께 봐야 한다 — 이 파일이 그 결합을 고정한다.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import AITask, Gate, QueueItem
from service.pipeline import gates as gates_service
from service.pipeline import intake
from service.pipeline.chain import advance, enabled_stages, next_stage
from service.pipeline.gates import GateError, harvest, open_first_gate
from tests.fakes import FakeRunner
from service.pipeline.stages.common import (
    CONCEPT_STEM_RE,
    REFERENCE_STEM_RE,
    body_links,
    check_note,
    parse_note_output,
    require_up_in_body,
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


def route(*, reference=True, concept=True, derived=False, exclusive=None, group="study"):
    return {
        "destinations": {
            "reference": {"enabled": reference, "group": group},
            "concept": {"enabled": concept},
            "derived": {"enabled": derived},
        },
        "exclusive": exclusive,
    }


# --- 체인 계산 (DB 불필요) ---------------------------------------------------


class TestChainShape:
    def test_enabled_stages_follow_definition_order(self):
        assert enabled_stages(route(derived=True)) == ("source_note", "concept", "derived")

    def test_disabled_destination_is_skipped(self):
        assert enabled_stages(route(concept=False)) == ("source_note",)

    def test_exclusive_opens_no_gate(self):
        """폐기는 만들 것이 없으니 검토할 것도 없다."""
        payload = route(reference=False, concept=False, exclusive="discard")
        assert enabled_stages(payload) == ()

    def test_next_stage_skips_disabled(self):
        """개념을 끄면 source_note 다음은 derived 다 — 중간이 비어도 건너뛴다."""
        payload = route(concept=False, derived=True)
        assert next_stage("youtube", payload, after="route") == "source_note"
        assert next_stage("youtube", payload, after="source_note") == "derived"
        assert next_stage("youtube", payload, after="derived") is None

    def test_last_stage_returns_none(self):
        """`None` 은 '발행 차례'라는 뜻이다."""
        assert next_stage("youtube", route(), after="concept") is None

    def test_unknown_pipeline_has_no_next(self):
        assert next_stage("없는_소스", route(), after="route") is None


# --- 초안 검사 (DB 불필요) ---------------------------------------------------


REFERENCE_MD = """---
type: reference
title: 샘플 자료
date: 2026-07-28
---

# 샘플 자료

## 개요

내용.
"""


class TestNoteOutput:
    def test_parses_record_and_code_fence(self):
        raw = "```text\nfilename_stem: 2026-07-28-a-b\n---8<---\nx\n---8<--- end\n```"
        assert parse_note_output(raw) == ("2026-07-28-a-b", "x")

    @pytest.mark.parametrize(
        "raw",
        [
            "not a record",
            # 옛 JSON 계약. 조용히 받아 주지 않는다 — 두 형식을 다 받으면 SoT 가 둘이 된다.
            '{"filename_stem": "a", "content": "x"}',
            "---8<---\nx",  # stem 없음
            "filename_stem: a\n---8<---\n   ",  # 본문 빔
            "filename_stem: a",  # 구분자 없음
        ],
    )
    def test_malformed_rejected(self, raw):
        with pytest.raises(GateError):
            parse_note_output(raw)

    @pytest.mark.parametrize("stem", ["resources/source/x", "x.md", "a/b/c"])
    def test_path_in_stem_rejected(self, stem):
        """경로를 지어내면 allowlist 밖으로 쓰는 계획이 만들어진다."""
        with pytest.raises(GateError):
            parse_note_output(f"filename_stem: {stem}\n---8<---\nx")

    def test_valid_reference_passes(self):
        meta = check_note(
            "2026-07-28-sample-source",
            REFERENCE_MD,
            expected_type="reference",
            stem_pattern=REFERENCE_STEM_RE,
            required=("title", "date"),
        )
        assert meta["title"] == "샘플 자료"

    @pytest.mark.parametrize(
        "stem", ["sample", "2026-7-28-x", "2026-07-28-Sample", "2026-07-28"]
    )
    def test_bad_reference_stem_rejected(self, stem):
        with pytest.raises(GateError):
            check_note(
                stem,
                REFERENCE_MD,
                expected_type="reference",
                stem_pattern=REFERENCE_STEM_RE,
                required=("title",),
            )

    def test_missing_type_rejected(self):
        """**없는 type 도 막는다** — 종전에는 *틀린* type 만 막았다.

        그래프 빌더가 노드 종류를 이 필드에서 읽으므로 없으면 발행 직전에
        `UNKNOWN_TYPE` 으로 거부된다. 즉 게이트를 넷 다 승인한 **뒤에** 막힌다 —
        item #3881 이 실제로 그랬다. 여기서 막으면 그 게이트 하나가 실패하고
        재시도가 그 자리에서 고친다.
        """
        with pytest.raises(GateError) as exc:
            check_note(
                "2026-07-28-x-y",
                "---\ntitle: 제목\ndate: 2026.07.28\n---\n본문",
                expected_type="reference",
                stem_pattern=REFERENCE_STEM_RE,
                required=("title", "date"),
            )
        assert exc.value.code == "MISSING_NOTE_FIELD"
        assert "type" in exc.value.message

    def test_missing_required_field_rejected(self):
        with pytest.raises(GateError) as exc:
            check_note(
                "2026-07-28-x-y",
                "---\ntype: reference\ntitle: 제목\n---\n본문",
                expected_type="reference",
                stem_pattern=REFERENCE_STEM_RE,
                required=("title", "date"),
            )
        assert exc.value.code == "MISSING_NOTE_FIELD"

    def test_wrong_type_rejected(self):
        with pytest.raises(GateError):
            check_note(
                "2026-07-28-x-y",
                "---\ntype: concept\ntitle: 제목\ndate: 2026-07-28\n---\n본문",
                expected_type="reference",
                stem_pattern=REFERENCE_STEM_RE,
                required=("title",),
            )

    def test_id_must_match_stem(self):
        """지식 노트는 `id` = 파일명 stem — 다르면 로더가 실패한다."""
        with pytest.raises(GateError):
            check_note(
                "2026-07-28-x-y",
                "---\ntype: reference\nid: 다른아이디\ntitle: 제목\ndate: 2026-07-28\n---\n본문",
                expected_type="reference",
                stem_pattern=REFERENCE_STEM_RE,
                required=("title",),
            )

    def test_body_links_strip_alias(self):
        assert body_links("보라 [[a-b|별칭]] 그리고 [[c-d]]") == {"a-b", "c-d"}

    def test_up_must_appear_in_body(self):
        """`up:` 은 본문 링크의 부분집합이어야 한다 (L3)."""
        meta = {"up": ["2026-07-28-src"]}
        require_up_in_body(meta, "본문에 [[2026-07-28-src]] 가 있다")
        with pytest.raises(GateError) as exc:
            require_up_in_body(meta, "본문에 링크가 없다")
        assert exc.value.code == "UP_NOT_IN_BODY"

    @pytest.mark.parametrize("stem", ["structure-content-separation", "gpt-4", "http2", "stt"])
    def test_concept_stem_accepts_plain_slug(self, stem):
        assert CONCEPT_STEM_RE.fullmatch(stem)

    @pytest.mark.parametrize("stem", ["2026-07-28-concept", "2026-07-28"])
    def test_concept_stem_rejects_leading_date(self, stem):
        """개념은 특정 시점에 묶이지 않는다 — 날짜를 붙이면 자료 단위로 갈라진다."""
        assert not CONCEPT_STEM_RE.fullmatch(stem)


# --- 승인 → 다음 게이트 -------------------------------------------------------


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


def maker(payload):
    """스테이지 실행기 하나 — 제출하면 곧바로 수확 가능한 상태가 된다."""
    return FakeRunner(payload=payload, session_ref="s")


async def _advance(db, item, gate, *, runners):
    """승인 뒤 다음 게이트를 열고, 그 게이트를 한 번 수확한다.

    실제로는 화면 폴링이 하는 일이다 — 여기서는 그 한 번을 대신 돌린다.
    """
    result = await advance(db, item, gate, runners=runners)
    if result.gate is not None:
        await harvest(db, result.gate, item=item, runner=runners[result.gate.stage_name])
    return result


async def _routed(db, url: str, payload: dict) -> tuple[QueueItem, Gate]:
    """route 게이트를 승인한 상태의 항목을 만든다."""
    created = await intake(db, source_url=url, source_kind="youtube")
    item = await db.get(QueueItem, created.item_id)
    item.status = "in_review"
    await db.flush()
    runner = maker(payload)
    gate = await open_first_gate(db, item, runner=runner)
    await harvest(db, gate, item=item, runner=runner)
    await gates_service.approve(db, gate)
    return item, gate


NOTE_PAYLOAD = {
    "filename_stem": "2026-07-28-sample-source",
    "content": REFERENCE_MD,
    "group": "study",
    "target_path": "resources/source/2026-07-28-sample-source.md",
}


@needs_db
class TestAdvance:
    async def test_route_approval_opens_source_note(self, db):
        item, gate = await _routed(db, "https://youtu.be/chain000001", route())
        nxt = (await _advance(
            db, item, gate, runners={"source_note": maker(NOTE_PAYLOAD)}
        )).gate
        assert nxt is not None and nxt.stage_name == "source_note"
        assert nxt.status == "review_pending"
        assert nxt.stage_no == 4

    async def test_disabled_destination_is_not_opened(self, db):
        """reference 를 끄면 source_note 게이트가 아예 생기지 않는다."""
        item, gate = await _routed(
            db, "https://youtu.be/chain000002", route(reference=False)
        )
        nxt = (await _advance(
            db,
            item,
            gate,
            runners={"source_note": maker(NOTE_PAYLOAD), "concept": maker({"x": 1})},
        )).gate
        assert nxt is not None and nxt.stage_name == "concept"

    async def test_exclusive_opens_nothing(self, db):
        item, gate = await _routed(
            db,
            "https://youtu.be/chain000003",
            route(reference=False, concept=False, exclusive="discard"),
        )
        result = await _advance(db, item, gate, runners={"source_note": maker(NOTE_PAYLOAD)})
        assert result.gate is None and result.chain_complete
        gates = (await db.scalars(select(Gate).where(Gate.item_id == item.id))).all()
        assert [g.stage_name for g in gates] == ["route"]

    async def test_missing_runner_does_not_open_dead_card(self, db):
        """승인할 수 없는 카드를 화면에 남기지 않는다.

        그리고 **체인 끝과 구분돼야 한다** — 섞으면 미완성 체인이 발행된다.
        """
        item, gate = await _routed(db, "https://youtu.be/chain000004", route())
        result = await _advance(db, item, gate, runners={})
        assert result.gate is None
        assert result.blocked and not result.chain_complete
        assert result.pending_stage == "source_note"
        gates = (await db.scalars(select(Gate).where(Gate.item_id == item.id))).all()
        assert [g.stage_name for g in gates] == ["route"]

    async def test_full_chain_walks_to_the_end(self, db):
        """route → source_note → concept → (발행 차례)."""
        item, gate = await _routed(db, "https://youtu.be/chain000005", route())
        runners = {"source_note": maker(NOTE_PAYLOAD), "concept": maker({"concepts": []})}

        second = (await _advance(db, item, gate, runners=runners)).gate
        await gates_service.approve(db, second)
        third = (await _advance(db, item, second, runners=runners)).gate
        await gates_service.approve(db, third)
        end = await _advance(db, item, third, runners=runners)

        assert [second.stage_name, third.stage_name] == ["source_note", "concept"]
        assert end.chain_complete  # 발행 차례

    async def test_approval_does_not_create_files(self, db, monkeypatch):
        """중간 승인은 다음 스테이지를 열 뿐 파일을 만들지 않는다 (DEC-011 D6)."""
        import pathlib

        def explode(*a, **k):
            raise AssertionError("게이트 승인이 레포에 썼다")

        monkeypatch.setattr(pathlib.Path, "write_text", explode)
        item, gate = await _routed(db, "https://youtu.be/chain000006", route())
        await _advance(db, item, gate, runners={"source_note": maker(NOTE_PAYLOAD)})


@needs_db
class TestSessionInheritance:
    """스테이지 사이 세션 승계 (KDEV-DEC-024 / SPEC-009 S-6·S-7).

    **체인 하나가 한 대화다.** 그전까지는 스테이지가 넘어가면 무조건 새 세션이라
    매 스테이지가 규칙·양식을 다시 읽고 원문을 다시 받았다.
    """

    async def test_next_gate_resumes_previous_stage_session(self, db):
        item, gate = await _routed(db, "https://youtu.be/sess000001", route())
        note_runner = FakeRunner(payload=NOTE_PAYLOAD, session_ref="note-sess")
        concept_runner = FakeRunner(payload={"concepts": []}, session_ref="con-sess")
        runners = {"source_note": note_runner, "concept": concept_runner}

        second = (await _advance(db, item, gate, runners=runners)).gate
        await gates_service.approve(db, second)
        third = (await _advance(db, item, second, runners=runners)).gate

        # route 가 남긴 세션을 자료 노트가, 자료 노트의 세션을 개념이 문다.
        assert note_runner.calls[-1].session_ref == "s"
        assert concept_runner.calls[-1].session_ref == "note-sess"
        assert third.stage_name == "concept"

    async def test_first_gate_has_nothing_to_resume(self, db):
        """앞이 없으면 `None` — stateless 다. 실패시키지 않는다 (D4)."""
        created = await intake(db, source_url="https://youtu.be/sess000002")
        item = await db.get(QueueItem, created.item_id)
        item.status = "in_review"
        await db.flush()
        runner = maker(route())
        await open_first_gate(db, item, runner=runner)
        assert runner.calls[-1].session_ref is None

    async def test_cancelled_gate_session_is_not_resumed(self, db):
        """재오픈은 「앞의 판단이 틀렸다」는 선언이다 (D2).

        그 선언 뒤에 틀린 판단의 세션이 조용히 살아 있으면, 사람은 되돌렸다고 믿는데
        시스템은 안 되돌린 상태가 된다.
        """
        from service.pipeline.chain import reopen_route

        item, gate = await _routed(db, "https://youtu.be/sess000003", route())
        stale = FakeRunner(payload=NOTE_PAYLOAD, session_ref="stale-note-sess")
        await _advance(db, item, gate, runners={"source_note": stale})

        # 목적지가 틀렸다 — route 를 다시 연다. 뒤 게이트는 cancelled.
        reopened = FakeRunner(payload=route(), session_ref="route-2-sess")
        await reopen_route(db, item, runner=reopened)
        await harvest(db, gate, item=item, runner=reopened)
        await gates_service.approve(db, gate)

        fresh = FakeRunner(payload=NOTE_PAYLOAD, session_ref="note-2-sess")
        again = (await _advance(db, item, gate, runners={"source_note": fresh})).gate

        assert again.id != stale.parsed[0].gate.id  # 새 게이트다
        # 취소된 자료 노트가 아니라 **다시 승인된 route** 를 문다.
        assert fresh.calls[-1].session_ref == "route-2-sess"

        # 한 칸 더 간다 — 앞 스테이지를 훑을 때도 취소된 쪽이 아니라 산 쪽을 봐야 한다.
        await gates_service.approve(db, again)
        concept = FakeRunner(payload={"concepts": []}, session_ref="con-2-sess")
        await _advance(db, item, again, runners={"concept": concept})
        assert concept.calls[-1].session_ref == "note-2-sess"


@needs_db
class TestDeadSession:
    """이어받을 세션이 실행기에서 사라졌을 때 (KDEV-DEC-024 D4 / OQ-4).

    **세션은 실행기 컨테이너의 파일시스템에 산다 — 배포 한 번이면 전부 사라진다.**
    승계가 들어온 뒤로는 그것이 진행 중 항목 **전부**를 막았다. 실제로 item #3881 이
    재배포 뒤 `No conversation found with session ID: …` 로 멎었다.
    """

    DEAD = "Error: No conversation found with session ID: 506af245-d111-4f33-9d67-89126fef8015"

    async def test_dead_session_is_forgotten_and_resubmitted_stateless(self, db):
        item, gate = await _routed(db, "https://youtu.be/dead00001", route())
        # 첫 실행은 죽은 세션으로 실패하고, 다음 제출은 성공한다.
        runner = FakeRunner(
            payload=NOTE_PAYLOAD, session_ref="note-sess", fail_times=1, fail_message=self.DEAD
        )
        opened = (await advance(db, item, gate, runners={"source_note": runner})).gate
        assert runner.calls[0].session_ref == "s"  # route 세션을 물고 나갔다

        # 수확이 죽은 세션을 알아채고 **지운 뒤 다시 제출**한다 — 실패로 닫지 않는다.
        assert await harvest(db, opened, item=item, runner=runner) is True
        assert opened.status == "generating"
        assert len(runner.calls) == 2
        assert runner.calls[1].session_ref is None  # 이번엔 stateless

        # 실패 기록은 남는다 (SPEC-009 S-4).
        failed = (
            await db.scalars(
                select(AITask).where(AITask.item_id == item.id, AITask.status == "failed")
            )
        ).all()
        assert [t.error_code for t in failed] == ["SESSION_LOST"]

        # 두 번째 수확에서 정상적으로 검토 대기가 된다.
        assert await harvest(db, opened, item=item, runner=runner) is True
        assert opened.status == "review_pending"

    async def test_forgetting_does_not_rely_on_parsing_the_id(self, db):
        """**메시지에서 뽑은 id 에만 기대지 않는다.**

        이 픽스처의 실제 세션은 `s` 인데 실패 메시지에는 다른 uuid 가 들어 있다 —
        실행기가 다른 표기를 쓰거나 세션이 내부적으로 갈린 경우를 흉내 낸 것이다.
        파싱한 id 만 지우면 재제출이 **같은 세션을 또 물어** 되돌이표가 된다.
        """
        item, gate = await _routed(db, "https://youtu.be/dead00002", route())
        runner = FakeRunner(
            payload=NOTE_PAYLOAD, session_ref="note-sess", fail_times=1, fail_message=self.DEAD
        )
        opened = (await advance(db, item, gate, runners={"source_note": runner})).gate
        await harvest(db, opened, item=item, runner=runner)

        # 이 항목에는 물릴 세션이 남아 있지 않다 — 다음 스테이지도 stateless 로 간다.
        left = (
            await db.scalars(
                select(AITask.session_ref).where(
                    AITask.item_id == item.id, AITask.session_ref.is_not(None)
                )
            )
        ).all()
        assert left == []

    async def test_unrelated_failure_keeps_the_session(self, db):
        """문구가 다르면 건드리지 않는다 — 무관한 실패에서 세션을 버리면 안 된다."""
        item, gate = await _routed(db, "https://youtu.be/dead00003", route())
        runner = FakeRunner(
            payload=NOTE_PAYLOAD, session_ref="note-sess", fail_times=1,
            fail_message="provider timeout",
        )
        opened = (await advance(db, item, gate, runners={"source_note": runner})).gate
        await harvest(db, opened, item=item, runner=runner)

        assert opened.status == "failed"  # 평소대로 실패로 닫힌다
        assert len(runner.calls) == 1  # 자동 재제출 없음


class TestBlogAndStudyNotePipelines:
    """KDEV-BL-007 케이스 3·5 — 유튜브와 같은 모양, `collect` 와 산출만 다르다."""

    def test_blog_mirrors_youtube_but_makes_posts(self):
        from service.pipeline.definitions import pipeline_for

        blog = [s.name for s in pipeline_for("blog").stages]
        youtube = [s.name for s in pipeline_for("youtube").stages]
        # 앞의 셋(수집·요약·라우팅)은 같다.
        assert blog[:3] == youtube[:3] == ["collect", "summarize", "route"]
        # 갈리는 것은 산출이다 — 유튜브는 교안, 블로그는 공개 글.
        assert "derived" in youtube and "derived" not in blog
        assert "post" in blog and "post" not in youtube

    def test_study_note_has_no_collect(self):
        """본문이 이미 있어 수집할 것이 없다 (KDEV-DEC-021)."""
        from service.pipeline.definitions import pipeline_for

        stages = [s.name for s in pipeline_for("study_note").stages]
        assert "collect" not in stages
        assert stages[0] == "summarize"

    def test_post_destination_opens_the_post_gate(self):
        assert enabled_stages(
            {"destinations": {"post": {"enabled": True}}, "exclusive": None}
        ) == ("post",)
