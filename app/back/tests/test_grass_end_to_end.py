"""잔디 한 바퀴 — 접수부터 발행까지 (KDEV-WORK-017 P4 완주 조건).

**조사만 더미이고 그 하류는 전부 진짜다.** `DummyCollect`·`AgentInvestigate`·
`DailyStage`·게이트·발행부가 실제 코드로 돌고, AI 호출만 가짜 클라이언트가 답한다.
DB 도 실물이고 파일도 실제로 써진다.

이 파일이 P2·P3 를 잇는 유일한 검증이다. 각 조각의 단위 테스트는 자기 계약만 보므로,
`collect` 산출물이 `investigate` 를 지나 게이트 payload 가 되고 그것이 발행 계획으로
조립되는 **연결부**는 여기서만 깨진다.

`dry_run` 이라 커밋과 push 는 생략되지만 **파일은 실제로 써진다**(`_write_all` 이
`publish_atomic` 앞에서 돈다). 그래서 완주의 관측 결과는 "파일이 생겼고 커밋은 없다" 다.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import Gate, GateRevision, ItemPreparation, QueueItem
from service import content_format
from service.apply.executor import apply_item
from service.pipeline import gates as gates_service
from service.pipeline import runtime
from service.pipeline.collect_dummy import DummyCollect
from service.pipeline.daily_intake import intake_daily
from service.pipeline.stages.daily import DailyStage
from service.pipeline.stages.investigate import AgentInvestigate
from tests.fakes import InlineDriver

#: 레포에 이미 있는 개념 — 잔디 concept 가 `up:` 으로 거는 상류다.
#: 운영에서는 로더가 만든 노드 맵이 오지만, 테스트는 필요한 것만 세운다.
CURRENT_NODES = {
    # reference → concept → concept. 실제 그래프의 계보를 그대로 세운다.
    "2026-07-01-api-design": {
        "type": "reference",
        "id": "2026-07-01-api-design",
        "title": "API 설계 자료",
        "up": None,
        "aliases": [],
        "body": "- [[api-contract]] — 개념",
        "archived": False,
    },
    "api-contract": {
        "type": "concept",
        "id": "api-contract",
        "title": "API 계약",
        "up": ["2026-07-01-api-design"],
        "aliases": ["api contract"],
        "body": "## 출처\n\n- [[2026-07-01-api-design]] — 출처",
        "archived": False,
    },
}

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")

CAREER_MD = """---
type: career
period: "2026.02 — present"
display_order: 1
is_current: true
title:
  ko: "백엔드 개발자"
org:
  ko: "메디솔브 AI"
summary:
  ko: "요약"
stack:
  - Python
bullets:
  ko:
    - "이력서 문장 1"
---

## 무슨 일 하는지

(TBD — 사용자 채움)

## 챌린지

- 기존 챌린지 한 줄
"""

DAILY_REPLY = {
    "daily": {
        "summary": {
            "ko": ["[MediSolveAIDev/mediness] 차트 요약 API 스키마를 정리했다"],
            "en": ["[MediSolveAIDev/mediness] Tidied the chart summary API schema"],
        },
        "body": "# 한 일\n\n차트 요약 API 응답 스키마를 정리했다.",
    },
    "career": {
        "changed": True,
        "stem": "medisolve-ai",
        "content": "## 무슨 일 하는지\n\n피부과 CRM 백엔드를 맡고 있다.\n\n## 챌린지\n\n- 기존 챌린지 한 줄\n- 응답 스키마가 커져 정리했다",
    },
    "concepts": [
        {
            "stem": "response-schema-trim",
            "title": "응답 스키마 정리",
            # **기존 개념**을 상류로 건다. daily·career 는 그래프 밖이라 걸 수 없다.
            "content": (
                "---\ntype: concept\ntitle: 응답 스키마 정리\n"
                "aliases:\n  - schema trim\nup:\n  - api-contract\n---\n\n"
                "# 응답 스키마 정리\n\n## 출처\n\n- [[api-contract]] — 상류 개념\n"
            ),
            "mode": "create",
        }
    ],
}

class ReplyingClient:
    """open-kknaks 를 흉내 낸다 — 프롬프트를 받아 미리 정한 답을 돌려준다."""

    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.prompts: list[str] = []

    async def submit(self, prompt, *, provider, model, options, max_retries, metadata):
        self.prompts.append(prompt)
        return f"task-{len(self.prompts)}"

    async def result(self, task_id):  # pragma: no cover - 폴링 경로에서 안 쓰인다
        return self.reply


def _execution(result: str):
    from service.pipeline.executor import Execution

    return Execution(status="succeeded", result=result, session_ref="sess-e2e")


class StubInvestigate(AgentInvestigate):
    """제출은 진짜 코드로, 폴링만 가짜 답으로."""

    async def wait(self, task_ref: str):
        return _execution("레포별 조사문")

    async def poll(self, task_ref: str):
        return _execution("레포별 조사문")


class StubDaily(DailyStage):
    async def wait(self, task_ref: str):
        return _execution(json.dumps(DAILY_REPLY, ensure_ascii=False))

    async def poll(self, task_ref: str):
        return _execution(json.dumps(DAILY_REPLY, ensure_ascii=False))


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """git 레포 하나 — 발행이 실제로 파일을 쓰는 곳."""
    root = tmp_path / "repo"
    (root / "templates" / "persona").mkdir(parents=True)
    for name in ("daily", "career"):
        (root / "templates" / "persona" / f"{name}.md").write_text(
            f"{name} 형식 명세", encoding="utf-8"
        )
    (root / "persona" / "career").mkdir(parents=True)
    (root / "persona" / "career" / "medisolve-ai.md").write_text(CAREER_MD, encoding="utf-8")
    (root / "persona" / "daily").mkdir(parents=True)
    (root / "permanent" / "concept").mkdir(parents=True)
    # 잔디 concept 가 `up:` 으로 걸 **실재하는 상류**. 개념이 개념에서 자란다.
    (root / "permanent" / "concept" / "api-contract.md").write_text(
        "---\ntype: concept\ntitle: API 계약\naliases:\n  - api contract\n---\n\n# API 계약\n\n본문\n",
        encoding="utf-8",
    )

    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"],
        cwd=root,
        check=True,
    )
    content_format.reset_cache()
    yield root
    content_format.reset_cache()


@pytest.fixture
async def world(repo: Path):
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()

    def session_factory():
        return AsyncSession(
            bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )

    runtime._registry.clear()
    daily_client = ReplyingClient(json.dumps(DAILY_REPLY, ensure_ascii=False))
    driver = InlineDriver(session_factory=session_factory, fetch=None)
    runtime.register(
        driver=driver,
        auto_stages={
            # 조사만 더미다 — 나머지는 진짜 코드다.
            "collect": DummyCollect(),
            "investigate": StubInvestigate(
                ReplyingClient("레포별 조사문"),
                provider="claude",
                model=None,
                work_dir=None,
            ),
        },
        stages={
            "daily": StubDaily(
                daily_client,
                repo_root=repo,
                provider="claude",
                model=None,
                work_dir=None,
            )
        },
    )
    try:
        yield driver, session_factory, daily_client
    finally:
        runtime._registry.clear()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


@needs_db
class TestFullLap:
    async def test_intake_to_publish(self, world, repo):
        """접수 → collect → investigate → 게이트 → 승인 → 발행. 한 바퀴."""
        driver, session_factory, daily_client = world

        # --- 접수 ---------------------------------------------------------
        async with session_factory() as db:
            received = await intake_daily(
                db, repo_root=repo, target=date(2026, 7, 29), note="scenario:normal"
            )
            await db.commit()
        assert received.created, received

        # --- 자동 스테이지 + 게이트 ----------------------------------------
        await driver.follow(received.item_id)

        async with session_factory() as db:
            item = await db.get(QueueItem, received.item_id)
            preps = (
                await db.scalars(
                    select(ItemPreparation)
                    .where(ItemPreparation.item_id == received.item_id)
                    .order_by(ItemPreparation.version)
                )
            ).all()
            gates = (
                await db.scalars(select(Gate).where(Gate.item_id == received.item_id))
            ).all()

        assert [p.payload.get("stage") for p in preps] == ["collect", "investigate"]
        assert item.status == "in_review"
        # 게이트는 **하나**다 — 승인이 곧 체인 종료이자 발행 트리거다.
        assert [g.stage_name for g in gates] == ["daily"]
        assert gates[0].status == "review_pending"
        # 형식은 템플릿에서 실려 왔다.
        assert "daily 형식 명세" in daily_client.prompts[0]

        # --- 승인 (사람이 요약 한 줄을 지운 채로) ---------------------------
        async with session_factory() as db:
            gate = await db.get(Gate, gates[0].id)
            revision = await db.get(GateRevision, gate.active_revision_id)
            edited = dict(revision.payload)
            edited["daily"] = {**edited["daily"], "summary": {"ko": ["[손으로 고친 줄]"], "en": []}}
            await gates_service.approve(db, gate, payload_override=edited)
            await db.commit()

        # --- 발행 (dry-run) ------------------------------------------------
        async with session_factory() as db:
            item = await db.get(QueueItem, received.item_id)
            outcome = await apply_item(
                db, item, repo_root=repo, current_nodes=CURRENT_NODES, dry_run=True
            )
            await db.commit()

        assert outcome.status == "succeeded", outcome

        # --- 관측: 파일은 생겼고 커밋은 없다 --------------------------------
        daily_path = repo / "persona" / "daily" / "2026-07-29.md"
        career_path = repo / "persona" / "career" / "medisolve-ai.md"
        concept_path = repo / "permanent" / "concept" / "response-schema-trim.md"

        assert daily_path.exists()
        assert concept_path.exists()

        written = daily_path.read_text(encoding="utf-8")
        # 사람이 고친 것이 발행됐다 — AI 제안 원본이 아니다.
        assert "[손으로 고친 줄]" in written
        # counts 는 코드가 센 값이다.
        assert "commit: 3" in written
        # 로더가 대조하는 점 표기.
        assert "date: 2026.07.29" in written

        career = career_path.read_text(encoding="utf-8")
        # 사람 전용 필드가 살아남았다 — 본문만 갈아 끼웠다.
        assert "이력서 문장 1" in career
        assert "응답 스키마가 커져 정리했다" in career

        # dry-run 이라 커밋은 없다.
        log = subprocess.run(
            ["git", "log", "--oneline"], cwd=repo, capture_output=True, text=True
        ).stdout
        assert log.count("\n") == 1  # init 하나뿐

    async def test_studio_only_day_publishes_without_career(self, world, repo):
        """`type=studio` 만 커밋한 날은 career 파일이 바뀌지 않는다."""
        driver, session_factory, _ = world
        before = (repo / "persona" / "career" / "medisolve-ai.md").read_text(encoding="utf-8")

        async with session_factory() as db:
            received = await intake_daily(
                db, repo_root=repo, target=date(2026, 7, 28), note="scenario:studio_only"
            )
            await db.commit()
        await driver.follow(received.item_id)

        async with session_factory() as db:
            gate = await db.scalar(
                select(Gate).where(Gate.item_id == received.item_id)
            )
            await gates_service.approve(db, gate)
            item = await db.get(QueueItem, received.item_id)
            await apply_item(db, item, repo_root=repo, current_nodes=CURRENT_NODES, dry_run=True)
            await db.commit()

        assert (repo / "persona" / "career" / "medisolve-ai.md").read_text(
            encoding="utf-8"
        ) == before

    async def test_user_authored_day_is_never_received(self, world, repo):
        """본인이 쓴 날은 항목 자체가 만들어지지 않는다."""
        _, session_factory, _ = world
        (repo / "persona" / "daily" / "2026-07-27.md").write_text(
            "---\ntype: daily\nauto: false\ndate: 2026.07.27\n---\n\n내가 씀",
            encoding="utf-8",
        )
        async with session_factory() as db:
            result = await intake_daily(db, repo_root=repo, target=date(2026, 7, 27))
            await db.commit()
        assert result.outcome == "blocked" and result.reason == "USER_AUTHORED_DAILY"

