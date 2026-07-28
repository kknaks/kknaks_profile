"""Slack → 승인 큐 (KDEV-WORK-014 P2 / KDEV-SPEC-007 S-1).

이 파일의 핵심 검증은 하나다 — **Slack 입력이 레포에 파일을 만들지 않는다.**
그게 이 프로젝트가 고치려던 문제(AI 결과물이 사람 검토 없이 origin/main 에 커밋)의
차단 지점이다. 그래서 "파일이 안 생겼다"를 사후 확인하지 않고, 아예 파일 쓰기와
git push 를 **폭발하게 만들어 놓고** 흐름을 돌린다.
"""

from __future__ import annotations

import pathlib

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import QueueItem
from service.pipeline import SummaryResult
from service.pipeline.slack_intake import QueueIntakeRunner

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

pytestmark = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


class FakeSlackClient:
    def __init__(self) -> None:
        self.messages: list[str] = []

    async def chat_postMessage(self, **kwargs):
        self.messages.append(kwargs["text"])
        return {"ts": "1700000000.000100"}

    async def chat_update(self, **kwargs):
        self.messages.append(kwargs["text"])
        return {"ok": True}

    @property
    def last(self) -> str:
        return self.messages[-1]


class FakeSessionStore:
    """Redis 대신 dict — 스레드↔항목 연결만 보면 된다."""

    def __init__(self) -> None:
        self.data: dict[tuple[str, str], object] = {}

    async def get(self, channel_id, root_thread_ts):
        return self.data.get((channel_id, root_thread_ts))

    async def set(self, session):
        self.data[(session.channel_id, session.root_thread_ts)] = session


class Request:
    def __init__(self, text: str, *, thread: str = "t1") -> None:
        self.request_id = f"evt-{thread}"
        self.entrypoint = "app_mention"
        self.team_id = "T1"
        self.channel_id = "C1"
        self.user_id = "U1"
        self.root_thread_ts = thread
        self.text = text


@pytest.fixture
def no_filesystem_writes(monkeypatch):
    """파일 쓰기와 git push 를 지뢰로 만든다 — 밟으면 테스트가 터진다."""

    def explode(*args, **kwargs):
        raise AssertionError("승인 전에 레포에 쓰려고 했다")

    monkeypatch.setattr(pathlib.Path, "write_text", explode)
    monkeypatch.setattr(pathlib.Path, "write_bytes", explode)
    monkeypatch.setattr("service.jobs.git_push.commit_and_push_with_retry", explode)
    return True


@pytest.fixture
async def make_runner():
    """실 DB 트랜잭션에 묶인 runner 를 만든다. 끝나면 전부 롤백."""
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()

    def session_factory():
        # `create_savepoint` 라야 runner 의 commit() 이 바깥 트랜잭션을 확정하지 않는다.
        return AsyncSession(
            bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )

    state: dict = {}

    def build(*, fetch, summarize):
        sessions = FakeSessionStore()
        state["sessions"] = sessions
        state["factory"] = session_factory
        return QueueIntakeRunner(
            session_factory=session_factory,
            sessions=sessions,
            fetch=fetch,
            summarize=summarize,
            now=lambda: __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ),
        )

    build.state = state  # type: ignore[attr-defined]
    build.session_factory = session_factory  # type: ignore[attr-defined]
    try:
        yield build
    finally:
        await trans.rollback()
        await conn.close()
        await engine.dispose()


async def _fetch_ok(url):
    return {"url": url, "content": "본문", "title": "제목"}


async def _fetch_fail(url):
    raise RuntimeError("transcript unavailable")


async def _summarize_ok(*, material, note):
    return SummaryResult(summary="요약본", session_ref="s1")


async def test_link_lands_in_queue_and_writes_no_file(make_runner, no_filesystem_writes):
    runner = make_runner(fetch=_fetch_ok, summarize=_summarize_ok)
    slack = FakeSlackClient()

    await runner.handle(Request("<@BOT> https://youtu.be/slacktest01 이거 정리해줘"), slack)

    async with make_runner.session_factory() as db:
        item = await db.scalar(
            select(QueueItem).where(QueueItem.normalized_url == "youtube:slacktest01")
        )
    assert item is not None
    assert (item.status, item.channel, item.source_kind) == ("in_review", "slack", "youtube")
    assert item.submitted_by == "U1"
    # 메모에는 링크가 아니라 사람의 말이 남는다.
    assert "이거 정리해줘" in item.note and "youtu.be" not in item.note
    assert "검토 대기" in slack.last


async def test_reply_says_nothing_was_written(make_runner, no_filesystem_writes):
    """회신 문구가 사실과 달라지면 안 된다 — 사람이 그 문구를 믿고 행동한다."""
    runner = make_runner(fetch=_fetch_ok, summarize=_summarize_ok)
    slack = FakeSlackClient()

    await runner.handle(Request("https://youtu.be/slacktest02", thread="t2"), slack)

    assert "레포에는 아무것도 쓰이지 않았습니다" in slack.last
    assert "저장 완료" not in slack.last  # 흡수 전 문구가 남아 있으면 오해를 준다


async def test_prepare_failure_is_reported_with_retry_path(make_runner, no_filesystem_writes):
    runner = make_runner(fetch=_fetch_fail, summarize=_summarize_ok)
    slack = FakeSlackClient()

    await runner.handle(Request("https://youtu.be/slacktest03", thread="t3"), slack)

    async with make_runner.session_factory() as db:
        item = await db.scalar(
            select(QueueItem).where(QueueItem.normalized_url == "youtube:slacktest03")
        )
    assert item.status == "prepare_failed"
    assert "준비에 실패" in slack.last
    # 막다른 길로 두지 않는다 — 사람이 뭘 하면 되는지 알려준다.
    assert "스레드에" in slack.last


async def test_thread_followup_supplies_note_and_unblocks(make_runner, no_filesystem_writes):
    """수집이 막힌 항목을 사람이 한 줄 남겨 푸는 경로 (SPEC-007 S-3)."""
    fetch_calls = {"n": 0}

    async def flaky_fetch(url):
        fetch_calls["n"] += 1
        raise RuntimeError("no transcript")

    runner = make_runner(fetch=flaky_fetch, summarize=_summarize_ok)
    slack = FakeSlackClient()

    await runner.handle(Request("https://youtu.be/slacktest04", thread="t4"), slack)
    await runner.handle(Request("자막이 없어서 요약하면: 핵심은 X 다", thread="t4"), slack)

    async with make_runner.session_factory() as db:
        item = await db.scalar(
            select(QueueItem).where(QueueItem.normalized_url == "youtube:slacktest04")
        )
    assert item.status == "in_review"
    assert "핵심은 X" in item.note
    assert "검토 대기" in slack.last


async def test_duplicate_link_joins_instead_of_creating(make_runner, no_filesystem_writes):
    runner = make_runner(fetch=_fetch_ok, summarize=_summarize_ok)
    slack = FakeSlackClient()

    await runner.handle(Request("https://youtu.be/slacktest05 첫 번째", thread="t5"), slack)
    await runner.handle(
        Request("https://www.youtube.com/watch?v=slacktest05&t=99s 두 번째", thread="t6"), slack
    )

    async with make_runner.session_factory() as db:
        items = (
            await db.scalars(
                select(QueueItem).where(QueueItem.normalized_url == "youtube:slacktest05")
            )
        ).all()
    assert len(items) == 1
    assert "첫 번째" in items[0].note and "두 번째" in items[0].note
    assert "합류" in slack.last or "메모를 붙였" in slack.last


async def test_failure_is_reported_not_swallowed(make_runner, no_filesystem_writes):
    """조용히 실패하면 던진 사람은 접수된 줄 안다."""

    async def boom(url):
        raise RuntimeError("x")

    async def summarize_boom(*, material, note):
        raise RuntimeError("x")

    runner = make_runner(fetch=boom, summarize=summarize_boom)
    slack = FakeSlackClient()

    # 수집·요약이 모두 실패해도 항목은 남고 사람에게 알려진다.
    await runner.handle(Request("https://youtu.be/slacktest07 메모", thread="t7"), slack)
    assert "실패" in slack.last


class TestSlackLinkMarkup:
    """Slack 은 링크를 `<url|표시텍스트>` 로 감싼다 — 운영 첫 시도에서 이걸로 막혔다.

    벗기지 않으면 URL 에 `|텍스트` 가 붙어 **유튜브가 `blog` 로 판정**되고,
    파이프라인 정의를 못 찾아 게이트가 아예 안 열린다.
    """

    def test_unwrap(self):
        from service.pipeline.slack_intake import unwrap_slack_links

        assert (
            unwrap_slack_links("<https://www.youtube.com/watch?v=ZVuHZ2Fjkl4|youtube.com/watch>")
            == "https://www.youtube.com/watch?v=ZVuHZ2Fjkl4"
        )
        assert unwrap_slack_links("<https://youtu.be/abc12345678>") == "https://youtu.be/abc12345678"
        assert unwrap_slack_links("링크 없음") == "링크 없음"

    async def test_wrapped_link_still_becomes_youtube_item(
        self, make_runner, no_filesystem_writes
    ):
        runner = make_runner(fetch=_fetch_ok, summarize=_summarize_ok)
        slack = FakeSlackClient()
        raw = "<https://www.youtube.com/watch?v=slackwrap1|youtube.com/watch?v=slackwrap1> 정리해줘"

        await runner.handle(Request(raw, thread="tw1"), slack)

        async with make_runner.session_factory() as db:
            item = await db.scalar(
                select(QueueItem).where(QueueItem.normalized_url == "youtube:slackwrap1")
            )
        assert item is not None
        assert item.source_kind == "youtube"          # blog 로 떨어지면 게이트가 안 열린다
        assert item.source_url == "https://www.youtube.com/watch?v=slackwrap1"
        # 메모에 `< >`·`|텍스트>` 찌꺼기가 남지 않아야 한다.
        assert item.note == "정리해줘"
