"""조사 스테이지 — 레포별 fan-out (KDEV-WORK-017 P2 / KDEV-SPEC-011·013).

여기서 고정하는 것은 셋이다.

    1. 레포 수만큼 제출한다 — 한 프롬프트에 몰아넣지 않는다
    2. **부분 실패 때 결과가 엉뚱한 레포에 붙지 않는다** — `task_ref` 로 맞춘다
    3. 빠진 레포를 지어내지 않고 `missing` 으로 들고 간다
"""

from __future__ import annotations

from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import QueueItem
from service.pipeline.collect_dummy import investigate_payload
from service.pipeline.stages.investigate import (
    AgentInvestigate,
    group_by_repo,
    repo_prompt,
)
from tests.conftest import isolate_tables
from tests.fakes import FakeSummarizer

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
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
    await isolate_tables(conn, "queue_items")
    session = AsyncSession(
        bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
    )
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


class FakeClient:
    """open-kknaks 클라이언트를 흉내 낸다 — 제출만 받고 ref 를 돌려준다."""

    def __init__(self) -> None:
        self.prompts: list[str] = []
        self.metadata: list[dict[str, Any]] = []

    async def submit(self, prompt, *, provider, model, options, max_retries, metadata):
        self.prompts.append(prompt)
        self.metadata.append(metadata)
        return f"okk-{len(self.prompts)}"


def _item(note: str = "scenario:normal") -> QueueItem:
    return QueueItem(
        source_kind="daily_commit",
        source_url=None,
        normalized_url=None,
        note=note,
        channel="manual",
        status="preparing",
    )


def _stage(client) -> AgentInvestigate:
    return AgentInvestigate(client, provider="claude", model=None, work_dir=None)


def _prior(note: str = "scenario:normal") -> dict[str, Any]:
    return {"collect": investigate_payload(_item(note))}


class TestGrouping:
    def test_commits_group_by_repo(self):
        grouped = group_by_repo(
            [{"repo": "a", "sha": "1"}, {"repo": "b", "sha": "2"}, {"repo": "a", "sha": "3"}]
        )
        assert list(grouped) == ["a", "b"]
        assert len(grouped["a"]) == 2

    def test_blank_repo_is_dropped(self):
        assert group_by_repo([{"sha": "1"}]) == {}


class TestPrompt:
    def test_prompt_carries_the_repo_and_its_commits(self):
        prompt = repo_prompt("owner/x", [{"sha": "1"}], meta={"date": "2026-08-01"})
        assert "owner/x" in prompt and "2026-08-01" in prompt

    def test_truncation_notice_travels_with_the_repo(self):
        """상한에 걸린 사실이 프롬프트에 있어야 서술이 얕은 이유를 안다 (SPEC-011 S-3)."""
        meta = {"date": "d", "truncated": {"owner/x": {"diff_bytes": 32768, "commits": 30}}}
        assert "32768" in repo_prompt("owner/x", [], meta=meta)
        assert "32768" not in repo_prompt("owner/y", [], meta=meta)

    def test_prompt_does_not_carry_daily_format_rules(self):
        """형식은 `compose` 의 몫이다 — 조사는 재료만 만든다."""
        prompt = repo_prompt("owner/x", [], meta={})
        assert "frontmatter" not in prompt and "counts" not in prompt


class TestSubmit:
    async def test_one_submission_per_repo(self):
        client = FakeClient()
        submission = await _stage(client).submit(item=_item(), prior=_prior())
        # normal 시나리오는 레포 셋이다.
        assert len(submission.task_refs) == 3
        assert len(client.prompts) == 3
        assert {m["repo"] for m in client.metadata} == {
            "MediSolveAIDev/mediness",
            "MediSolveAIDev/Linky",
            "kknaks/kknaks_profile",
        }

    async def test_ref_to_repo_map_is_recorded(self):
        """대응표가 없으면 수확이 어느 레포가 빠졌는지 알 수 없다."""
        client = FakeClient()
        submission = await _stage(client).submit(item=_item(), prior=_prior())
        mapping = submission.payload["investigate_refs"]
        assert set(mapping) == set(submission.task_refs)

    async def test_no_commits_skips_without_failing(self):
        """커밋이 없어도 노트만으로 여기까지 온다 — 부를 것이 없을 뿐이다."""
        client = FakeClient()
        submission = await _stage(client).submit(
            item=_item("scenario:all_failed"), prior=_prior("scenario:all_failed")
        )
        assert submission.task_refs == []
        assert submission.error_code is None
        assert submission.payload["investigate"]["skipped"] is True
        assert client.prompts == []

    async def test_company_and_studio_are_investigated_alike(self):
        """조사 깊이는 균일하다 — 공개 통제는 게이트가 한다 (SPEC-011)."""
        client = FakeClient()
        await _stage(client).submit(item=_item(), prior=_prior())
        company = next(p for p in client.prompts if "mediness" in p)
        studio = next(p for p in client.prompts if "kknaks_profile" in p)
        assert company.split("\n\n")[0] == studio.split("\n\n")[0]


class TestParse:
    async def test_results_map_to_the_right_repo(self):
        client = FakeClient()
        stage = _stage(client)
        submission = await stage.submit(item=_item(), prior=_prior())
        mapping = submission.payload["investigate_refs"]
        results = {ref: f"{repo} 조사문" for ref, repo in mapping.items()}

        piece = stage.parse(results, item=_item(), prior=submission.payload)

        for repo in mapping.values():
            assert piece["investigate"]["repos"][repo] == f"{repo} 조사문"
        assert piece["investigate"]["missing"] == []

    async def test_partial_failure_does_not_shift_results(self):
        """**색인이 밀리면 A 레포 결과가 B 것으로 읽힌다.** 그래서 ref 로 맞춘다."""
        client = FakeClient()
        stage = _stage(client)
        submission = await stage.submit(item=_item(), prior=_prior())
        mapping = submission.payload["investigate_refs"]
        first_ref = submission.task_refs[0]
        # 첫 건이 실패해 수확에서 빠진 상태를 만든다.
        survived = {ref: f"{mapping[ref]} 조사문" for ref in submission.task_refs[1:]}

        piece = stage.parse(survived, item=_item(), prior=submission.payload)

        assert piece["investigate"]["missing"] == [mapping[first_ref]]
        for ref in submission.task_refs[1:]:
            assert piece["investigate"]["repos"][mapping[ref]] == f"{mapping[ref]} 조사문"

    async def test_empty_body_counts_as_missing(self):
        """빈 조사문을 성공으로 넘기면 `compose` 가 근거 없이 서술한다."""
        client = FakeClient()
        stage = _stage(client)
        submission = await stage.submit(item=_item(), prior=_prior())
        results = {ref: "   " for ref in submission.task_refs}

        piece = stage.parse(results, item=_item(), prior=submission.payload)

        assert piece["investigate"]["repos"] == {}
        assert len(piece["investigate"]["missing"]) == 3


@needs_db
class TestLegacyHarvesterKeepsOff:
    """레거시 수확기가 fan-out 준비를 건드리지 않는다 (KDEV-WORK-017 결함 ⑨).

    `harvest_preparation` 은 "수집+요약 한 덩어리, 실행 1건" 을 전제한다. fan-out
    준비는 `ai_task_id` 가 비어 있어서 그 함수에 닿는 순간 `TASK_REF_MISSING` 으로
    닫힌다.

    **실제로 승인 큐 화면이 그것을 했다.** 목록 조회(`_harvest_item`)가 `preparing`
    항목마다 이 함수를 불렀고, 드라이버가 investigate 2건을 정상적으로 기다리는
    동안 조사 중인 항목을 죽였다 — 화면을 열어 둔 것이 파이프라인을 멈췄다.
    로컬 e2e 를 브라우저로 돌리기 전까지는 안 나왔다(어제는 curl 로만 봤다).
    """

    async def _preparing_item(self, db):
        from core.models import ItemPreparation, QueueItem

        item = QueueItem(
            source_kind="daily_commit",
            source_url=None,
            normalized_url="daily:2026-08-01",
            note=None,
            channel="scheduler",
            status="preparing",
        )
        db.add(item)
        await db.flush()
        prep = ItemPreparation(
            item_id=item.id,
            version=1,
            status="running",
            ai_task_id=None,  # fan-out 은 비운다 — N 건을 `AITask.item_id` 로 찾는다
            payload={"stage": "investigate", "task_refs": ["ref-1", "ref-2"]},
        )
        db.add(prep)
        await db.flush()
        return item, prep

    async def test_auto_stage_preparation_is_left_alone(self, db):
        from service.pipeline.prepare import harvest_preparation

        item, prep = await self._preparing_item(db)

        result = await harvest_preparation(db, item, summarize=FakeSummarizer())

        assert result.status == "preparing", "조사 중인 준비를 닫으면 안 된다"
        await db.refresh(prep)
        await db.refresh(item)
        assert prep.status == "running"
        assert item.status == "preparing"

    async def test_legacy_preparation_is_still_harvested(self, db):
        """레거시 경로는 그대로여야 한다 — 유튜브가 아직 그쪽이다."""
        from core.models import ItemPreparation, QueueItem
        from service.pipeline.prepare import harvest_preparation

        item = QueueItem(
            source_kind="youtube",
            source_url="https://youtu.be/x",
            normalized_url="https://youtu.be/x",
            note=None,
            channel="manual",
            status="preparing",
        )
        db.add(item)
        await db.flush()
        # `stage` 키가 없다 — 레거시의 표식이다.
        db.add(
            ItemPreparation(
                item_id=item.id, version=1, status="running", ai_task_id=None, payload={}
            )
        )
        await db.flush()

        result = await harvest_preparation(db, item, summarize=FakeSummarizer())

        assert result.status == "prepare_failed"
        assert result.error_code == "TASK_REF_MISSING"
