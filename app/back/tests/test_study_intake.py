"""공부 노트 접수 — `inbox/` 를 비우는 일 (KDEV-DEC-021 / KDEV-BL-007 케이스 5).

여기서 고정하는 것은 넷이다.

    1. **파일명이 멱등키다** — 같은 이름을 다시 넣어도 항목은 하나다
    2. **파일을 지우는가**가 상태를 말한다 — 남아 있으면 곧 미처리다
    3. 본문이 `note` 로 들어간다 — 수집이 없는 파이프라인이라 이것이 원문이다
    4. 발행이 입구 원본을 **같은 커밋으로** 회수한다
"""

from __future__ import annotations

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
