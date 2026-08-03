"""잔디 접수 진입점 (KDEV-WORK-017 P2 / KDEV-SPEC-013).

여기서 고정하는 것은 셋이다.

    1. 날짜가 중복 축이다 — 같은 날짜로 두 번 접수하면 항목이 하나다
    2. 본인이 쓴 날은 **만들지 않는다** — 만들고 실패시키는 것이 아니다
    3. 백필은 날짜 지정으로 되고, 미래 날짜는 막힌다
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import QueueItem
from service.pipeline.daily_intake import (
    KST,
    DailyIntakeResult,
    default_target,
    intake_daily,
    synthetic_key,
    user_authored,
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
    (tmp_path / "persona" / "daily").mkdir(parents=True)
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


def _write_daily(repo: Path, target: date, *, auto) -> None:
    body = "---\ntype: daily\n"
    if auto is not None:
        body += f"auto: {'true' if auto else 'false'}\n"
    body += f"date: {target.isoformat().replace('-', '.')}\n---\n\n# 한 일\n"
    (repo / "persona" / "daily" / f"{target.isoformat()}.md").write_text(
        body, encoding="utf-8"
    )


class TestTargetDate:
    def test_default_is_yesterday_kst(self):
        """09:05 KST 에 도는 잡의 '어제' 가 방금 끝난 하루다."""
        now = datetime(2026, 8, 1, 9, 5, tzinfo=KST)
        assert default_target(now) == date(2026, 7, 31)

    def test_key_is_the_date(self):
        assert synthetic_key(date(2026, 7, 29)) == "daily:2026-07-29"


class TestUserAuthored:
    def test_missing_file_is_not_user_authored(self, repo):
        assert user_authored(repo, date(2026, 7, 31)) is False

    def test_auto_true_is_ours(self, repo):
        _write_daily(repo, date(2026, 7, 31), auto=True)
        assert user_authored(repo, date(2026, 7, 31)) is False

    def test_auto_false_is_the_users(self, repo):
        _write_daily(repo, date(2026, 7, 31), auto=False)
        assert user_authored(repo, date(2026, 7, 31)) is True

    def test_missing_auto_key_is_the_users(self, repo):
        """자동 생성분만 명시적으로 표시된다 — 키가 없으면 사람 것으로 본다."""
        _write_daily(repo, date(2026, 7, 31), auto=None)
        assert user_authored(repo, date(2026, 7, 31)) is True


@needs_db
class TestIntake:
    async def test_creates_an_item_with_the_date_as_key(self, db, repo):
        result = await intake_daily(db, repo_root=repo, target=date(2026, 7, 20))
        assert result.created and result.date == "2026-07-20"

        item = await db.get(QueueItem, result.item_id)
        assert item.source_kind == "daily_commit"
        assert item.normalized_url == "daily:2026-07-20"
        assert item.status == "received"
        # 접수는 행 하나를 만들고 끝난다 — 조사도 AI 도 여기서 돌지 않는다.
        assert item.source_url is None

    async def test_same_date_twice_joins_instead_of_duplicating(self, db, repo):
        """날짜가 중복 축이다 (SPEC-013 「날짜 축 중복」)."""
        first = await intake_daily(db, repo_root=repo, target=date(2026, 7, 21))
        second = await intake_daily(db, repo_root=repo, target=date(2026, 7, 21))

        assert first.created
        assert second.outcome == "joined"
        assert second.item_id == first.item_id

        rows = (
            await db.scalars(
                select(QueueItem).where(QueueItem.normalized_url == "daily:2026-07-21")
            )
        ).all()
        assert len(rows) == 1

    async def test_different_dates_are_separate_items(self, db, repo):
        a = await intake_daily(db, repo_root=repo, target=date(2026, 7, 22))
        b = await intake_daily(db, repo_root=repo, target=date(2026, 7, 23))
        assert a.item_id != b.item_id

    async def test_backfill_takes_an_explicit_date(self, db, repo):
        """놓친 날을 되살리는 경로다 — 2026-07-29 가 실제로 비어 있었다."""
        result = await intake_daily(db, repo_root=repo, target=date(2026, 7, 29))
        assert result.created and result.date == "2026-07-29"

    async def test_future_date_is_blocked(self, db, repo):
        now = datetime(2026, 8, 1, 9, 5, tzinfo=KST)
        result = await intake_daily(
            db, repo_root=repo, target=date(2026, 8, 2), now=now
        )
        assert result.outcome == "blocked" and result.reason == "FUTURE_DATE"
        assert result.item_id is None

    async def test_today_is_allowed(self, db, repo):
        """어제가 기본이지만 오늘 지정은 막지 않는다 — 아직 안 끝났을 뿐 조사는 된다."""
        now = datetime(2026, 8, 1, 23, 0, tzinfo=KST)
        result = await intake_daily(
            db, repo_root=repo, target=date(2026, 8, 1), now=now
        )
        assert result.created

    async def test_user_authored_day_is_not_received_at_all(self, db, repo):
        """**만들고 실패시키지 않는다.** 그날 산출물 전체가 사람 소유다 (SPEC-012 S-5)."""
        target = date(2026, 7, 24)
        _write_daily(repo, target, auto=False)

        result = await intake_daily(db, repo_root=repo, target=target)

        assert result.outcome == "blocked" and result.reason == "USER_AUTHORED_DAILY"
        rows = (
            await db.scalars(
                select(QueueItem).where(QueueItem.normalized_url == synthetic_key(target))
            )
        ).all()
        assert rows == []

    async def test_our_own_previous_daily_does_not_block(self, db, repo):
        """auto:true 는 우리가 쓴 것이라 다시 만들어도 된다 — upsert 가 받는다."""
        target = date(2026, 7, 25)
        _write_daily(repo, target, auto=True)
        assert (await intake_daily(db, repo_root=repo, target=target)).created

    async def test_default_target_is_used_when_omitted(self, db, repo):
        now = datetime(2026, 8, 1, 9, 5, tzinfo=KST)
        result = await intake_daily(db, repo_root=repo, now=now)
        assert result.date == "2026-07-31"


class TestJobWakesTheDriver:
    """스케줄러 잡이 접수 뒤 드라이버를 깨우는지 (KDEV-WORK-017 결함 ②).

    수동 접수(`api/routers/queue.py`)는 커밋 뒤 `_follow()` 를 부른다. 그 대칭이
    빠져서 매일 09:05 에 항목이 `received` 로 멎었다 — 실증에서 120초간 정지해
    있다가 목록 API 를 한 번 치니 그제서야 진행했다(조회 시 수확 안전망).

    **DB 없이 돈다.** 잡의 배선만 보는 것이라 실 세션이 필요 없고, 그래야 이 검증이
    Postgres 유무에 걸리지 않는다.
    """

    @pytest.fixture
    def job(self, monkeypatch):
        """`run_daily_intake_job` 을 세션·접수·드라이버를 다 가짜로 두고 부른다."""
        import contextlib

        import core.db

        from service.pipeline import daily_intake as mod

        followed: list[int] = []

        class _StubSession:
            async def commit(self) -> None:
                return None

        @contextlib.asynccontextmanager
        async def _fake_session():
            yield _StubSession()

        monkeypatch.setattr(core.db, "new_session", _fake_session)
        monkeypatch.setattr(config, "repo_root", lambda: Path("/nonexistent"))

        def _install(result, *, follow_error: Exception | None = None):
            async def _fake_intake(db, **kwargs):
                return result

            async def _fake_follow(item_id: int) -> None:
                if follow_error is not None:
                    raise follow_error
                followed.append(item_id)

            monkeypatch.setattr(mod, "intake_daily", _fake_intake)
            monkeypatch.setattr(mod, "follow", _fake_follow)
            return mod.run_daily_intake_job

        return _install, followed

    async def test_accepted_item_is_handed_to_the_driver(self, job):
        install, followed = job
        run = install(DailyIntakeResult(outcome="created", date="2026-08-01", item_id=4852))

        result = await run()

        assert result["item_id"] == 4852
        assert followed == [4852], "접수만 하고 끝나면 항목이 received 로 멎는다"

    async def test_blocked_intake_has_nothing_to_follow(self, job):
        """본인 작성·미래 날짜는 항목을 만들지 않는다 — 밀 것이 없다."""
        install, followed = job
        run = install(
            DailyIntakeResult(
                outcome="blocked", date="2026-08-01", reason="USER_AUTHORED_DAILY"
            )
        )

        assert (await run())["outcome"] == "blocked"
        assert followed == []

    async def test_driver_failure_does_not_fail_the_accepted_intake(self, job):
        """접수는 이미 커밋됐다. 미는 데 실패했다고 잡 실패로 보고하면 안 된다.

        조회 시 수확이 남아 있어 화면을 열면 따라잡는다 — 되돌릴 이유가 없다.
        """
        install, _ = job
        run = install(
            DailyIntakeResult(outcome="created", date="2026-08-01", item_id=1),
            follow_error=RuntimeError("드라이버 없음"),
        )

        assert (await run())["item_id"] == 1
