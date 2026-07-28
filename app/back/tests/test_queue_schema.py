"""승인 큐·게이트 스키마 제약 검증 (KDEV-WORK-014 Phase 1).

여기서 검사하는 것은 **DB가 강제하는 불변식**이다. 앱 코드가 실수해도 깨지면 안 되는
것만 제약으로 걸었고, 그 제약이 실제로 발동하는지 확인한다. 걸어만 두고 발동을
확인하지 않으면 "제약이 있으니 안전하다"는 잘못된 믿음이 남는다.

라이브 Postgres 가 필요하다 — 미가용이면 모듈 전체 skip (test_auth 와 같은 패턴).
partial unique 는 Postgres 기능이라 SQLite 로 대체할 수 없다.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

import config

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

pytestmark = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용 — 스키마 테스트 skip")


@pytest.fixture
def conn():
    """트랜잭션 안에서 돌리고 끝나면 롤백 — 실 DB에 흔적을 남기지 않는다."""
    engine = create_engine(config.database_url())
    with engine.connect() as c:
        trans = c.begin()
        try:
            yield c
        finally:
            trans.rollback()
            engine.dispose()


@contextmanager
def rejected(conn):
    """제약 위반을 기대한다.

    savepoint 를 `pytest.raises` **안쪽**에 둬야 한다 — 예외가 `begin_nested` 의
    `__exit__` 을 통과하며 savepoint 를 롤백하고, 그래야 바깥 트랜잭션이 살아남아
    다음 문장을 실행할 수 있다. 순서를 뒤집으면 aborted 트랜잭션에 RELEASE 를 걸어
    제약 위반이 아니라 엉뚱한 InFailedSqlTransaction 이 잡힌다.
    """
    with pytest.raises(DBAPIError):
        with conn.begin_nested():
            yield


def _item(conn, *, url: str | None = None, status: str = "received") -> int:
    return conn.execute(
        text(
            "INSERT INTO queue_items (source_kind, source_url, normalized_url, status) "
            "VALUES ('youtube', :u, :u, :s) RETURNING id"
        ),
        {"u": url, "s": status},
    ).scalar_one()


def _gate(conn, item_id: int, *, stage: str = "route", status: str = "review_pending") -> int:
    return conn.execute(
        text(
            "INSERT INTO gates (item_id, stage_name, stage_no, status) "
            "VALUES (:i, :n, 1, :s) RETURNING id"
        ),
        {"i": item_id, "n": stage, "s": status},
    ).scalar_one()


def _revision(conn, gate_id: int, version: int, status: str) -> int:
    return conn.execute(
        text(
            "INSERT INTO gate_revisions (gate_id, version, status) "
            "VALUES (:g, :v, :s) RETURNING id"
        ),
        {"g": gate_id, "v": version, "s": status},
    ).scalar_one()


class TestApprovedRevisionUniqueness:
    """게이트당 승인 버전은 하나 — 둘이면 무엇을 발행할지 알 수 없다."""

    def test_two_approved_revisions_rejected(self, conn):
        gate = _gate(conn, _item(conn))
        _revision(conn, gate, 1, "approved")
        with rejected(conn):
            _revision(conn, gate, 2, "approved")

    def test_many_superseded_allowed(self, conn):
        """승인은 하나뿐이어야 하지만 폐기된 이력은 얼마든지 쌓인다."""
        gate = _gate(conn, _item(conn))
        _revision(conn, gate, 1, "superseded")
        _revision(conn, gate, 2, "superseded")
        _revision(conn, gate, 3, "approved")

    def test_same_version_twice_rejected(self, conn):
        gate = _gate(conn, _item(conn))
        _revision(conn, gate, 1, "reviewable")
        with rejected(conn):
            _revision(conn, gate, 1, "drafting")


class TestLiveGateUniqueness:
    """항목·스테이지당 살아 있는 게이트는 하나. cancelled 는 이력이라 예외."""

    def test_duplicate_live_stage_rejected(self, conn):
        item = _item(conn)
        _gate(conn, item, stage="route")
        with rejected(conn):
            _gate(conn, item, stage="route")

    def test_reopened_stage_allowed_after_cancel(self, conn):
        """route 재오픈으로 무효화한 뒤 같은 스테이지를 다시 여는 경로."""
        item = _item(conn)
        _gate(conn, item, stage="concept", status="cancelled")
        _gate(conn, item, stage="concept", status="generating")  # 통과해야 한다


class TestPendingUrlUniqueness:
    """발행 전 같은 URL 은 기존 항목에 합류한다(SPEC-007 S-4)."""

    def test_duplicate_pending_url_rejected(self, conn):
        _item(conn, url="https://youtu.be/abc")
        with rejected(conn):
            _item(conn, url="https://youtu.be/abc")

    def test_same_url_allowed_after_publish(self, conn):
        """이미 발행된 자료의 재정리는 정당하다 — 제약이 막으면 안 된다."""
        _item(conn, url="https://youtu.be/dup", status="published")
        _item(conn, url="https://youtu.be/dup", status="received")

    def test_null_url_items_do_not_collide(self, conn):
        """텍스트 입력 항목은 URL 이 없다 — 여러 건이 공존해야 한다."""
        _item(conn, url=None)
        _item(conn, url=None)


class TestStatusChecks:
    """상태는 텍스트 + CHECK. 오타가 조용히 저장되면 상태기계가 무의미해진다."""

    @pytest.mark.parametrize(
        "sql, params",
        [
            (
                "INSERT INTO queue_items (source_kind, status) VALUES ('youtube', :s)",
                {"s": "bogus"},
            ),
            (
                "INSERT INTO ai_tasks (item_id, kind, status) VALUES (:i, 'route', :s)",
                {"s": "bogus"},
            ),
        ],
    )
    def test_unknown_status_rejected(self, conn, sql, params):
        if ":i" in sql:
            params["i"] = _item(conn)
        with rejected(conn):
            conn.execute(text(sql), params)

    def test_stage_name_is_not_constrained(self, conn):
        """파이프라인 정의가 데이터다(DEC-011 D2) — 새 스테이지에 마이그레이션이 필요하면 안 된다."""
        _gate(conn, _item(conn), stage="some_future_stage")


def test_models_and_migrations_agree():
    """ORM 모델과 마이그레이션이 어긋나지 않는지 — `alembic check` 를 상시 검증으로 건다.

    둘은 손으로 각각 쓴 두 벌의 진실이라 언제든 갈라질 수 있다. 모델에 컬럼을 더하고
    리비전을 빼먹으면 로컬은 멀쩡한데 배포에서만 깨진다 — 그때는 이미 늦다.
    """
    from alembic import command
    from alembic.config import Config
    from alembic.util.exc import AutogenerateDiffsDetected

    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    try:
        command.check(cfg)
    except AutogenerateDiffsDetected as exc:
        pytest.fail(f"모델과 마이그레이션 불일치 — 리비전이 필요하다:\n{exc}")


def test_item_delete_cascades_to_children(conn):
    """hard delete 는 운영 경로가 아니지만(soft delete), 고아 행이 남는 구조는 두지 않는다."""
    item = _item(conn)
    gate = _gate(conn, item)
    _revision(conn, gate, 1, "reviewable")
    conn.execute(text("DELETE FROM queue_items WHERE id = :i"), {"i": item})
    left = conn.execute(
        text("SELECT count(*) FROM gate_revisions WHERE gate_id = :g"), {"g": gate}
    ).scalar_one()
    assert left == 0
