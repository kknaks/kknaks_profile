"""진짜 `collect` 스테이지 (KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1).

**여기서 확인하는 것은 계약 동일성이다.** 더미가 내던 키를 진짜도 그대로 내야
하류(`investigate`·`daily` 게이트·발행부)가 한 줄도 안 바뀐다 — P2 가 더미 경계를
그렇게 그어 둔 값을 여기서 받는다.

네트워크를 쓰지 않는다. `GITHUB_CLONE_BASE` 를 `file://` 로 돌려 로컬 레포를
원격처럼 쓴다(`test_repo_sync.py` 와 같은 이음매).
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import QueueItem, TrackedRepo
from service.pipeline import collect_git
from service.pipeline.collect_dummy import investigate_payload
from service.pipeline.collect_git import GitCollect
from tests.conftest import isolate_tables

TARGET = date(2026, 7, 29)
WHEN = "2026-07-29T09:00:00+09:00"

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


def _git(*args: str, cwd: Path, env: dict | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True, env=env
    ).stdout.strip()


def _commit(repo: Path, name: str, body: str) -> None:
    target = repo / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    _git("add", "-A", cwd=repo)
    _git(
        "-c", "user.name=kknaks", "-c", "user.email=kknaks@example.com",
        "commit", "--date", WHEN, "-m", f"{name} 작업",
        cwd=repo,
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_COMMITTER_DATE": WHEN,
            "GIT_COMMITTER_NAME": "kknaks",
            "GIT_COMMITTER_EMAIL": "kknaks@example.com",
            "HOME": str(repo.parent),
        },
    )


def _item() -> QueueItem:
    return QueueItem(
        source_kind="daily_commit",
        source_url=None,
        normalized_url=f"daily:{TARGET.isoformat()}",
        note=None,
        channel="scheduler",
        status="in_review",
    )


@pytest.fixture(autouse=True)
def env(monkeypatch, tmp_path):
    monkeypatch.setenv("COMMIT_IDENTITY_PATTERNS", "kknaks")
    monkeypatch.setenv("GH_TOKEN_PERSONAL", "tok")
    monkeypatch.setenv("GH_TOKEN_COMPANY", "tok")
    monkeypatch.setenv("REPO_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("REPO_ROOT", str(tmp_path / "profile"))
    monkeypatch.setenv("GITHUB_CLONE_BASE", f"file://{tmp_path / 'origin'}/")


@pytest.fixture
def origins(tmp_path: Path) -> Path:
    """`MediSolveAIDev/mediness`(company) · `kknaks/wine_log`(studio)."""
    for slug, file in (
        ("MediSolveAIDev/mediness", "app/back/api.py"),
        ("kknaks/wine_log", "app/front/page.tsx"),
    ):
        path = tmp_path / "origin" / f"{slug}.git"
        path.mkdir(parents=True)
        _git("init", "-q", "-b", "main", ".", cwd=path)
        _commit(path, file, "x = 1\n")
    # 프로필 레포 — `counts.note`/`study` 를 읽는 작업트리다. 비어 있어도 된다.
    (tmp_path / "profile").mkdir()
    return tmp_path


@pytest.fixture
async def session_factory():
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
    await isolate_tables(conn, "tracked_repos")

    def factory():
        return AsyncSession(
            bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )

    try:
        yield factory
    finally:
        await trans.rollback()
        await conn.close()
        await engine.dispose()


async def _register(factory, rows: list[TrackedRepo]) -> None:
    async with factory() as db:
        for row in rows:
            db.add(row)
        await db.commit()


@needs_db
class TestContract:
    async def test_the_payload_keys_match_the_dummy(self, session_factory, origins, tmp_path):
        """**하류가 진짜인지 가짜인지 구분하지 못해야 한다.**"""
        await _register(
            session_factory,
            [
                TrackedRepo(
                    slug="MediSolveAIDev/mediness",
                    type="company",
                    detail="medisolve-ai",
                    account="company",
                ),
                TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal"),
            ],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        submission = await stage.submit(item=_item(), prior={})

        assert submission.task_refs == []  # LLM 을 부르지 않는다
        assert submission.error_code is None
        assert set(submission.payload["collect"]) == set(investigate_payload(_item()))

    async def test_commits_carry_repo_and_career_attribution(
        self, session_factory, origins, tmp_path
    ):
        await _register(
            session_factory,
            [
                TrackedRepo(
                    slug="MediSolveAIDev/mediness",
                    type="company",
                    detail="medisolve-ai",
                    account="company",
                ),
                TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal"),
            ],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        collect = (await stage.submit(item=_item(), prior={})).payload["collect"]

        assert {c["repo"] for c in collect["commits"]} == {
            "MediSolveAIDev/mediness",
            "kknaks/wine_log",
        }
        # studio 는 career 를 만들지 않는다 — 다닌 적 없는 조직을 이력에 넣지 않는다.
        assert collect["career_map"] == {"medisolve-ai": ["MediSolveAIDev/mediness"]}
        assert collect["counts"]["commit"] == 2
        assert set(collect["areas"]) == {"backend", "frontend"}

    async def test_a_disabled_repo_is_skipped(self, session_factory, origins, tmp_path):
        """SPEC-011 S-4 3항 — 지우지 않고 끈다. 클론은 남고 조사만 멈춘다."""
        await _register(
            session_factory,
            [
                TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal"),
                TrackedRepo(
                    slug="MediSolveAIDev/mediness",
                    type="company",
                    detail="medisolve-ai",
                    account="company",
                    enabled=False,
                ),
            ],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        collect = (await stage.submit(item=_item(), prior={})).payload["collect"]
        assert {c["repo"] for c in collect["commits"]} == {"kknaks/wine_log"}

    async def test_one_bad_repo_does_not_stop_the_rest(
        self, session_factory, origins, tmp_path, monkeypatch
    ):
        """SPEC-011 §5 「부분 실패」 — 실패는 `failures[]` 로 결과에 동반된다."""
        monkeypatch.setattr(collect_git, "notify_slack", _swallow)
        await _register(
            session_factory,
            [
                TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal"),
                TrackedRepo(slug="kknaks/gone", type="studio", account="personal"),
            ],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        collect = (await stage.submit(item=_item(), prior={})).payload["collect"]

        assert {c["repo"] for c in collect["commits"]} == {"kknaks/wine_log"}
        assert [f["repo"] for f in collect["failures"]] == ["kknaks/gone"]

    async def test_no_repos_means_no_activity(self, session_factory, origins, tmp_path):
        """활동 0은 실패가 아니다 — 항목이 `no_activity` 로 종결된다."""
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        submission = await stage.submit(item=_item(), prior={})
        assert submission.error_code == "NO_ACTIVITY"


@needs_db
class TestDrift:
    async def test_an_unregistered_identity_is_reported(
        self, session_factory, origins, tmp_path, monkeypatch
    ):
        """SPEC-011 S-2 — 알리되 **조사는 멈추지 않는다.**"""
        sent: list[str] = []

        async def capture(text: str) -> None:
            sent.append(text)

        monkeypatch.setattr(collect_git, "notify_slack", capture)
        monkeypatch.setenv("KNOWN_COMMIT_IDENTITIES", "kknaks <someone-else@x.com>")
        await _register(
            session_factory,
            [TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal")],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        collect = (await stage.submit(item=_item(), prior={})).payload["collect"]

        assert len(sent) == 1
        assert "kknaks@example.com" in sent[0]
        assert collect["commits"]  # 조사는 그대로 진행됐다

    async def test_a_registered_identity_is_quiet(
        self, session_factory, origins, tmp_path, monkeypatch
    ):
        sent: list[str] = []

        async def capture(text: str) -> None:
            sent.append(text)

        monkeypatch.setattr(collect_git, "notify_slack", capture)
        monkeypatch.setenv("KNOWN_COMMIT_IDENTITIES", "kknaks <kknaks@example.com>")
        await _register(
            session_factory,
            [TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal")],
        )
        stage = GitCollect(
            session_factory=session_factory, repo_root=tmp_path / "profile"
        )
        await stage.submit(item=_item(), prior={})
        assert sent == []


async def _swallow(text: str) -> None:
    return None
