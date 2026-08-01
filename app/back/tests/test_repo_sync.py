"""bare 클론 관리 (KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1 2~4항).

**네트워크를 쓰지 않는다.** `GITHUB_CLONE_BASE` 를 `file://` 로 돌려 로컬 레포를
원격처럼 쓴다 — 그 이음매가 없으면 아래 첫 번째 테스트를 재현할 방법이 없다.

여기서 고정하는 것은 넷이다.

    1. **`clone --bare` 는 fetch refspec 을 남기지 않는다.** 그대로 두면 이후 fetch 가
       새 브랜치를 못 가져오고, 전 브랜치를 보려고 API 를 버린 의미가 사라진다
    2. 클론 루트가 작업트리 안이면 **돌기 전에** 멈춘다
    3. 토큰이 없으면 시도조차 하지 않는다
    4. 하나가 실패해도 나머지가 진행되고, 실패는 `last_error` 와 Slack 한 통으로 남는다
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import TrackedRepo
from service.jobs import repos as repo_sync

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


def _git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _commit(repo: Path, name: str) -> None:
    (repo / name).write_text(name, encoding="utf-8")
    _git("add", "-A", cwd=repo)
    _git(
        "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", name, cwd=repo
    )


@pytest.fixture
def origin(tmp_path: Path, monkeypatch) -> Path:
    """`owner/name` 레이아웃의 로컬 원격. `main` 과 `feature/x` 둘을 갖는다."""
    src = tmp_path / "origin" / "kknaks" / "wine_log.git"
    src.parent.mkdir(parents=True)
    src.mkdir()
    _git("init", "-q", "-b", "main", ".", cwd=src)
    _commit(src, "first")
    _git("checkout", "-q", "-b", "feature/x", cwd=src)
    _commit(src, "on-feature")
    _git("checkout", "-q", "main", cwd=src)

    monkeypatch.setenv("GITHUB_CLONE_BASE", f"file://{tmp_path / 'origin'}/")
    monkeypatch.setenv("GH_TOKEN_PERSONAL", "tok-personal")
    return src


@pytest.fixture
def cache(tmp_path: Path) -> Path:
    return tmp_path / "cache"


class TestCloneLayout:
    def test_clone_dir_is_flat(self, tmp_path):
        """`owner/name.git` 으로 중첩시키면 빈 owner 디렉터리가 남는다."""
        assert repo_sync.clone_dir("kknaks/wine_log", tmp_path).name == "kknaks__wine_log.git"

    def test_token_is_not_in_the_url(self, monkeypatch):
        monkeypatch.setenv("GITHUB_CLONE_BASE", "https://github.com/")
        assert repo_sync.clone_url("a/b") == "https://github.com/a/b.git"


class TestWorktreeGuard:
    def test_inside_the_worktree_is_refused(self, monkeypatch, tmp_path):
        """발행 경로의 작업트리 초기화가 클론을 지운다 — 돌기 전에 멈춘다."""
        monkeypatch.setenv("REPO_ROOT", str(tmp_path))
        with pytest.raises(RuntimeError, match="작업트리 안"):
            repo_sync.assert_outside_worktree(tmp_path / "app" / "cache")

    def test_the_worktree_root_itself_is_refused(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REPO_ROOT", str(tmp_path))
        with pytest.raises(RuntimeError):
            repo_sync.assert_outside_worktree(tmp_path)

    def test_a_sibling_is_fine(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REPO_ROOT", str(tmp_path / "repo"))
        repo_sync.assert_outside_worktree(tmp_path / "cache")  # 예외 없음


class TestToken:
    def test_missing_token_does_not_touch_disk(self, monkeypatch, cache):
        """SPEC-011 §5 「토큰」 — 없으면 클론을 시도하지 않는다."""
        monkeypatch.setenv("GH_TOKEN_COMPANY", "")
        result = repo_sync.sync_repo("org/x", "company", root=cache)
        assert result.ok is False
        assert result.code == repo_sync.CODE_TOKEN_MISSING
        assert not cache.exists()

    def test_the_account_picks_the_token(self, monkeypatch):
        monkeypatch.setenv("GH_TOKEN_PERSONAL", "p")
        monkeypatch.setenv("GH_TOKEN_COMPANY", "c")
        assert config.gh_token("personal") == "p"
        assert config.gh_token("company") == "c"


class TestSync:
    def test_all_branches_are_cloned(self, origin, cache):
        result = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert result.ok, result.message
        heads = _git("for-each-ref", "--format=%(refname)", "refs/heads", cwd=result.path)
        assert "refs/heads/feature/x" in heads

    def test_a_branch_born_after_the_clone_is_fetched(self, origin, cache):
        """**이 발주에서 가장 조용한 결함이다.**

        `git clone --bare` 는 `remote.origin.fetch` 를 남기지 않는다. 그 상태에서
        `fetch` 는 `FETCH_HEAD` 만 갱신하고 `refs/heads/*` 는 클론 시점에 멈추는데,
        **에러가 나지 않아 겉으로는 정상이다.** 둘째 날부터 새 브랜치의 커밋이 통째로
        빠지고, 그것은 전 브랜치를 보려고 GitHub API 를 버린 이유 그 자체다.
        """
        first = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert first.ok

        _git("checkout", "-q", "-b", "feature/born-later", cwd=origin)
        _commit(origin, "later")
        _git("checkout", "-q", "main", cwd=origin)

        second = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert second.ok, second.message

        heads = _git("for-each-ref", "--format=%(refname)", "refs/heads", cwd=second.path)
        assert "refs/heads/feature/born-later" in heads
        assert "later" in _git("log", "--all", "--pretty=%s", cwd=second.path)

    def test_a_deleted_branch_is_pruned(self, origin, cache):
        repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        _git("branch", "-D", "feature/x", cwd=origin)
        result = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        heads = _git("for-each-ref", "--format=%(refname)", "refs/heads", cwd=result.path)
        assert "refs/heads/feature/x" not in heads

    def test_syncing_twice_is_idempotent(self, origin, cache):
        """SPEC-011 §5 「멱등성」 — 두 번 돌려도 같다."""
        first = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        head = _git("rev-parse", "main", cwd=first.path)
        second = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert second.ok
        assert _git("rev-parse", "main", cwd=second.path) == head

    def test_a_missing_remote_fails_without_raising(self, origin, cache):
        result = repo_sync.sync_repo("kknaks/does_not_exist", "personal", root=cache)
        assert result.ok is False
        assert result.code == repo_sync.CODE_CLONE_FAILED

    def test_a_broken_directory_is_reported_not_deleted(self, origin, cache):
        """수백 MB 를 일시적 이상으로 날리지 않는다 — 사람이 본다."""
        path = repo_sync.clone_dir("kknaks/wine_log", cache)
        path.mkdir(parents=True)
        (path / "junk").write_text("x", encoding="utf-8")

        result = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert result.ok is False
        assert result.code == repo_sync.CODE_CLONE_FAILED
        assert (path / "junk").exists()

    def test_a_refspec_less_clone_is_repaired(self, origin, cache):
        """앞선 버전이 refspec 없이 만들어 둔 클론도 다음 실행에서 고쳐진다."""
        path = repo_sync.clone_dir("kknaks/wine_log", cache)
        path.parent.mkdir(parents=True, exist_ok=True)
        _git("clone", "--bare", "-q", str(origin), str(path), cwd=cache.parent)
        subprocess.run(
            ["git", "-C", str(path), "config", "--unset", "remote.origin.fetch"],
            capture_output=True,
            check=False,
        )

        result = repo_sync.sync_repo("kknaks/wine_log", "personal", root=cache)
        assert result.ok, result.message
        assert (
            _git("config", "remote.origin.fetch", cwd=path) == "+refs/heads/*:refs/heads/*"
        )


class TestScrub:
    def test_the_token_never_reaches_last_error(self):
        """`last_error` 는 DB 에 남고 Slack 으로도 나간다."""
        scrubbed = repo_sync._scrub("fatal: auth failed for ghp_secret", "ghp_secret")
        assert "ghp_secret" not in scrubbed
        assert "<redacted>" in scrubbed


@pytest.fixture
async def db():
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
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


@needs_db
class TestSyncAll:
    async def test_one_failure_does_not_stop_the_rest(
        self, db, origin, cache, monkeypatch
    ):
        """SPEC-011 §5 「부분 실패」 — 하나의 실패가 조사 전체를 실패시키지 않는다."""
        sent: list[str] = []
        monkeypatch.setattr(
            repo_sync, "notify_slack", lambda text: _record(sent, text)
        )

        rows = [
            TrackedRepo(slug="kknaks/does_not_exist", type="studio", account="personal"),
            TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal"),
        ]
        for row in rows:
            db.add(row)
        await db.flush()

        results = await repo_sync.sync_all(db, rows, root=cache)

        assert [r.ok for r in results] == [False, True]
        assert rows[0].last_error and rows[0].last_error.startswith("CLONE_FAILED")
        assert rows[0].last_fetched_at is None
        assert rows[1].last_error is None
        assert rows[1].last_fetched_at is not None

    async def test_success_clears_a_stale_error(self, db, origin, cache, monkeypatch):
        """`last_error` 가 남아 있으면 **지금 막혀 있다**는 뜻이어야 한다."""
        monkeypatch.setattr(repo_sync, "notify_slack", lambda text: _record([], text))
        row = TrackedRepo(
            slug="kknaks/wine_log",
            type="studio",
            account="personal",
            last_error="FETCH_FAILED: 어제의 실패",
        )
        db.add(row)
        await db.flush()

        await repo_sync.sync_all(db, [row], root=cache)
        assert row.last_error is None

    async def test_failures_are_one_slack_message(self, db, cache, monkeypatch):
        """13개가 한꺼번에 죽으면 13통이 온다 — 묶어서 한 통으로."""
        sent: list[str] = []
        monkeypatch.setattr(
            repo_sync, "notify_slack", lambda text: _record(sent, text)
        )
        monkeypatch.setenv("GH_TOKEN_PERSONAL", "")

        rows = [
            TrackedRepo(slug="a/one", type="studio", account="personal"),
            TrackedRepo(slug="b/two", type="studio", account="personal"),
        ]
        for row in rows:
            db.add(row)
        await db.flush()

        await repo_sync.sync_all(db, rows, root=cache)

        assert len(sent) == 1
        assert "a/one" in sent[0] and "b/two" in sent[0]

    async def test_no_failure_means_no_notification(self, db, origin, cache, monkeypatch):
        sent: list[str] = []
        monkeypatch.setattr(
            repo_sync, "notify_slack", lambda text: _record(sent, text)
        )
        row = TrackedRepo(slug="kknaks/wine_log", type="studio", account="personal")
        db.add(row)
        await db.flush()

        await repo_sync.sync_all(db, [row], root=cache)
        assert sent == []


async def _record(bucket: list[str], text: str) -> None:
    bucket.append(text)
