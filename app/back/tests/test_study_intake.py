"""공부 노트 접수 — `inbox/` 를 비우는 일 (KDEV-DEC-021 / KDEV-BL-007 케이스 5).

여기서 고정하는 것은 넷이다.

    1. **파일명이 멱등키다** — 같은 이름을 다시 넣어도 항목은 하나다
    2. **파일을 지우는가**가 상태를 말한다 — 남아 있으면 곧 미처리다
    3. 본문이 `note` 로 들어간다 — 수집이 없는 파이프라인이라 이것이 원문이다
    4. 발행이 입구 원본을 **같은 커밋으로** 회수한다
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import QueueItem
from service.apply.plan import build_actions
from service.pipeline.study_intake import (
    inbox_files,
    intake_inbox,
    read_note,
    synthetic_key,
)
from tests.conftest import isolate_tables

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
def repo(tmp_path: Path) -> Path:
    (tmp_path / "inbox").mkdir()
    return tmp_path


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


def _write(repo: Path, name: str, body: str = "본문이다.", *, title: str | None = None) -> Path:
    head = "---\ntype: idea\n"
    if title:
        head += f"title: {title}\n"
    head += "---\n\n"
    path = repo / "inbox" / name
    path.write_text(head + body, encoding="utf-8")
    return path


class TestScanScope:
    """입구에 놓인 것과 입구에 사는 것은 다르다."""

    def test_readme_is_not_a_note(self, repo: Path):
        (repo / "inbox" / "README.md").write_text("# inbox\n", encoding="utf-8")
        _write(repo, "http-cache.md")
        assert [p.name for p in inbox_files(repo)] == ["http-cache.md"]

    def test_subdirectories_are_not_swept(self, repo: Path):
        """폴더를 통째로 던지는 것은 「입구에 넣는다」가 아니다."""
        nested = repo / "inbox" / "_restored"
        nested.mkdir()
        (nested / "old.md").write_text("옛 필기\n", encoding="utf-8")
        assert inbox_files(repo) == []

    def test_missing_inbox_is_not_an_error(self, tmp_path: Path):
        """입구가 없는 환경(테스트·신규 클론)에서 부팅이 막히면 안 된다."""
        assert inbox_files(tmp_path) == []


class TestReadNote:
    def test_frontmatter_is_stripped_and_title_kept(self, repo: Path):
        """`type: idea` 는 그래프용 값이라 요약 입력에 넣지 않는다."""
        path = _write(repo, "http-cache.md", "캐시 이야기", title="HTTP 캐시")
        body, title = read_note(path)
        assert title == "HTTP 캐시"
        assert body.startswith("# HTTP 캐시")
        assert "type: idea" not in body

    def test_existing_heading_is_not_doubled(self, repo: Path):
        path = _write(repo, "http-cache.md", "# 이미 제목이 있다\n\n본문", title="HTTP 캐시")
        body, _ = read_note(path)
        assert body.count("#") == 1


@needs_db
class TestIntakeInbox:
    async def test_note_becomes_an_item_and_the_file_goes(self, db, repo: Path):
        _write(repo, "http-cache.md", "캐시는 이렇게 동작한다")

        result = await intake_inbox(db, repo_root=repo)

        assert result.summary() == {"created": 1}
        item = await db.get(QueueItem, result.items[0].item_id)
        assert item.source_kind == "study_note"
        assert item.source_url is None  # 수집할 URL 이 없다 — 본문이 이미 있다
        assert item.normalized_url == synthetic_key("http-cache")
        # 본문이 곧 원문이다. `submit_preparation` 이 URL 없는 항목에서 메모를 원문
        # 대신 쓰는 분기를 그대로 탄다.
        assert "캐시는 이렇게 동작한다" in item.note
        assert not (repo / "inbox" / "http-cache.md").exists()

    async def test_same_filename_joins_instead_of_duplicating(self, db, repo: Path):
        """멱등키는 파일명이다 — 오탈자를 고쳐 다시 넣어도 같은 항목이다."""
        _write(repo, "http-cache.md", "첫 판")
        first = await intake_inbox(db, repo_root=repo)

        _write(repo, "http-cache.md", "오탈자를 고친 둘째 판")
        second = await intake_inbox(db, repo_root=repo)

        assert second.summary() == {"already_queued": 1}
        assert second.items[0].item_id == first.items[0].item_id
        rows = (await db.scalars(select(QueueItem))).all()
        assert len(rows) == 1
        # 본문을 **덧붙이지 않는다.** 노트 통째가 메모라 합류시키면 같은 글이 두 번
        # 들어간 입력이 요약으로 간다.
        assert rows[0].note.count("첫 판") == 1
        assert "둘째 판" not in rows[0].note
        # 큐가 이미 갖고 있으므로 파일은 지운다 — 입구에 남으면 미처리로 읽힌다.
        assert not (repo / "inbox" / "http-cache.md").exists()

    async def test_empty_note_stays_in_the_inbox(self, db, repo: Path):
        """항목을 만들어 실패시키느니 입구에 둔다 — 실패 항목은 사람이 지워야 한다."""
        _write(repo, "http-cache.md", "")

        result = await intake_inbox(db, repo_root=repo)

        assert result.items[0].outcome == "skipped"
        assert (await db.scalars(select(QueueItem))).all() == []
        assert (repo / "inbox" / "http-cache.md").exists()

    async def test_published_slug_stays_in_the_inbox(self, db, repo: Path):
        """이미 발행된 slug 는 사람이 정할 일이다(SPEC-007 S-4). 조용히 지우지 않는다."""
        _write(repo, "http-cache.md", "다시 정리하고 싶다")
        first = await intake_inbox(db, repo_root=repo)
        item = await db.get(QueueItem, first.items[0].item_id)
        item.status = "published"
        await db.flush()

        _write(repo, "http-cache.md", "다시 정리하고 싶다")
        again = await intake_inbox(db, repo_root=repo)

        assert again.items[0].outcome == "duplicate_published"
        assert (repo / "inbox" / "http-cache.md").exists()

    async def test_created_ids_are_what_the_driver_follows(self, db, repo: Path):
        _write(repo, "a.md", "가")
        _write(repo, "b.md", "나")

        result = await intake_inbox(db, repo_root=repo)

        assert len(result.created_ids) == 2


class TestInboxReclaim:
    """발행이 입구 원본을 회수한다 (KDEV-DEC-021 D1)."""

    APPROVED = {
        "source_note": {
            "target_path": "resources/source/2026-08-11-http-cache.md",
            "content": "---\ntype: reference\n---\n\n본문",
            "filename_stem": "2026-08-11-http-cache",
        }
    }

    def test_study_note_publish_removes_the_inbox_file(self):
        actions = build_actions(self.APPROVED, source_key=synthetic_key("http-cache"))

        removes = [a for a in actions if a.action == "remove"]
        assert [a.path for a in removes] == ["inbox/http-cache.md"]

    def test_other_sources_reclaim_nothing(self):
        """유튜브 항목의 `normalized_url` 은 URL 이다 — 입구와 무관하다."""
        actions = build_actions(
            self.APPROVED, source_key="https://www.youtube.com/watch?v=abc"
        )
        assert [a.action for a in actions] == ["create"]

    def test_nothing_published_reclaims_nothing(self):
        """지우기만 하는 커밋은 발행이 아니다."""
        assert build_actions({}, source_key=synthetic_key("http-cache")) == []


class TestPostIsPublished:
    """`post` 게이트 산출이 계획에 들어간다 — 없으면 승인해도 파일이 안 나간다."""

    def test_post_becomes_a_file_action(self):
        actions = build_actions(
            {
                "post": {
                    "target_path": "persona/posts/http-cache.md",
                    "content": "---\ntype: post_note\n---\n\n## 주제",
                    "filename_stem": "http-cache",
                }
            }
        )
        assert [(a.action, a.path, a.note_type) for a in actions] == [
            ("create", "persona/posts/http-cache.md", "post_note")
        ]


class TestReclaimOnTermination:
    """회수는 **종결 시점의 일**이다 (KDEV-DEC-021 D1).

    발행은 산출물과 같은 커밋으로 지우고(`TestInboxReclaim`), 갈 곳이 없는 종결
    (폐기·삭제)은 회수 커밋 하나를 낸다. 그러지 않으면 접수가 지운 파일의 삭제가
    커밋될 자리가 없어 `reset --hard` 한 번에 되살아난다.

    **진짜 git 을 쓴다.** 원격까지 둔 이유는 `publish_atomic` 이 커밋 뒤 fetch·rebase·
    push 를 하기 때문이다 — 원격이 없으면 fetch 가 실패해 롤백으로 끝나고, 그러면
    「회수가 커밋에 실렸는가」를 못 본다.
    """

    @pytest.fixture
    def repo(self, tmp_path: Path, monkeypatch) -> Path:
        from service.apply import git as apply_git

        monkeypatch.setattr(
            apply_git.config,
            "bot_identity",
            lambda: {"user": "t", "email": "t@example.com", "token": "x"},
        )

        origin = tmp_path / "origin.git"
        subprocess.run(
            ["git", "init", "-q", "--bare", "-b", "main", str(origin)],
            check=True,
            capture_output=True,
        )

        work = tmp_path / "work"
        (work / "inbox").mkdir(parents=True)
        (work / "inbox" / "http-cache.md").write_text("본문\n", encoding="utf-8")
        for args in (
            ["git", "init", "-q", "-b", "main"],
            ["git", "config", "user.email", "t@example.com"],
            ["git", "config", "user.name", "t"],
            ["git", "remote", "add", "origin", str(origin)],
            ["git", "add", "-A"],
            ["git", "commit", "-qm", "init"],
            ["git", "push", "-q", "origin", "main"],
        ):
            subprocess.run(args, cwd=work, check=True, capture_output=True)
        return work

    def _item(self, key: str | None, status: str = "discarded") -> QueueItem:
        item = QueueItem(
            source_kind="study_note",
            source_url=None,
            normalized_url=key,
            note="본문",
            channel="inbox",
            status=status,
        )
        item.id = 7
        return item

    def _tracked(self, repo: Path) -> str:
        return subprocess.run(
            ["git", "ls-files", "inbox/"], cwd=repo, capture_output=True, text=True
        ).stdout

    def test_the_deletion_reaches_git(self, repo: Path):
        from service.apply.reclaim import reclaim_inbox

        (repo / "inbox" / "http-cache.md").unlink()  # 접수가 지운 상태
        assert "http-cache.md" in self._tracked(repo)  # 아직 커밋에는 살아 있다

        outcome = reclaim_inbox(
            self._item(synthetic_key("http-cache")), repo_root=repo, dry_run=False
        )

        assert outcome is not None and outcome.ok, outcome
        assert "http-cache.md" not in self._tracked(repo)

    def test_a_leftover_file_is_removed_too(self, repo: Path):
        """접수가 `delete=False` 였어도 종결이면 입구는 비어야 한다."""
        from service.apply.reclaim import reclaim_inbox

        reclaim_inbox(
            self._item(synthetic_key("http-cache")), repo_root=repo, dry_run=False
        )
        assert not (repo / "inbox" / "http-cache.md").exists()
        assert "http-cache.md" not in self._tracked(repo)

    def test_other_sources_reclaim_nothing(self, repo: Path):
        """유튜브 항목의 `normalized_url` 은 URL 이다 — 입구와 무관하다."""
        from service.apply.reclaim import reclaim_inbox

        assert (
            reclaim_inbox(
                self._item("https://youtu.be/abc"), repo_root=repo, dry_run=False
            )
            is None
        )
        assert (repo / "inbox" / "http-cache.md").exists()

    def test_git_failure_does_not_undo_the_termination(self, repo: Path, monkeypatch):
        """폐기는 이미 확정된 사람의 결정이다 — git 이 죽었다고 되돌리지 않는다."""
        from service.apply import reclaim as reclaim_mod

        def boom(*a, **kw):
            raise RuntimeError("git 이 죽었다")

        monkeypatch.setattr(reclaim_mod, "publish_atomic", boom)
        assert (
            reclaim_mod.reclaim_inbox(
                self._item(synthetic_key("http-cache")), repo_root=repo, dry_run=False
            )
            is None
        )

    def test_untracked_path_never_reaches_git(self, repo: Path):
        """지울 커밋 이력이 없으면 **git 을 부르지 않는다.**

        그냥 넘기면 `git add` 가 `did not match any files` 로 죽고, `publish_atomic`
        이 그것을 발행 실패로 보아 레포 전체에 `reset --hard` + `clean -fd` 를 건다 —
        남의 미커밋 작업까지 날아간다.
        """
        from service.apply.reclaim import reclaim_inbox

        (repo / "미커밋.txt").write_text("남의 작업", encoding="utf-8")

        assert (
            reclaim_inbox(
                self._item(synthetic_key("없던-노트")), repo_root=repo, dry_run=False
            )
            is None
        )
        assert (repo / "미커밋.txt").exists()  # clean -fd 가 안 돌았다

    def test_dry_run_touches_no_commit(self, repo: Path):
        """운영 기본값이 dry_run 이다 — 그때는 작업트리만 정리되고 커밋은 없다."""
        from service.apply.reclaim import reclaim_inbox

        outcome = reclaim_inbox(
            self._item(synthetic_key("http-cache")), repo_root=repo, dry_run=True
        )
        assert outcome is not None and outcome.dry_run
        assert "http-cache.md" in self._tracked(repo)
