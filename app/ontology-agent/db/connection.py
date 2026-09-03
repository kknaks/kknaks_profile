"""SQLite 커넥션 — 쓰기용과 읽기 전용 두 갈래.

읽기 전용은 `mode=ro` URI 다. 소비자 표면(WORK-002 도구·API)은 이 헬퍼만 쓴다 —
쓰기 시도가 코드 리뷰가 아니라 드라이버에서 막히게 하기 위함(S-002).

**주의(WORK-002 착수 조건)** — `connect_ro()` 는 **쓰기만** 막는다. 같은 커넥션으로
`SELECT * FROM bronze_vegas_reservations` 가 그대로 되므로 AC-8(뷰 경유 강제)을 이것만으로
강제할 수 없다. 도구 계층이 허용 테이블 화이트리스트(`v_*`·`gold_*`·`ontology_*`)를
따로 세워야 한다 — DEC-002 의 「새 경로가 곧 구멍」.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import settings

_SAVEPOINT_SEQ = "ontology_build"


def resolved_db_path(db_path: Path | str | None = None) -> Path:
    return Path(db_path) if db_path is not None else settings.resolved_db_path


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """쓰기 가능 커넥션 — 빌드 전용. 디렉토리가 없으면 만든다.

    `isolation_level=None` 으로 파이썬의 암묵 트랜잭션을 끄고 `atomic()` 이 전부 쥔다 —
    게이트 실패 시 「이전 DB 유지」(SPEC-001 §5)를 코드가 확실히 보장하기 위함이다.
    """
    path = resolved_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def atomic(conn: sqlite3.Connection, name: str = "step"):
    """전부 반영되거나 전부 없던 일이 되는 구간. **중첩 가능**하다.

    SAVEPOINT 라 단독 실행(`build silver`)과 전체 실행(`build all`)이 같은 코드를 쓴다 —
    가장 바깥 savepoint 의 RELEASE 가 곧 커밋이고, 안쪽이 터지면 그 지점까지만 되감긴다.
    SQLite 는 DDL 도 트랜잭션 안이라 `write_table` 의 DROP/CREATE 까지 함께 되감긴다.
    """
    sp = f"{_SAVEPOINT_SEQ}_{name}"
    conn.execute(f'SAVEPOINT "{sp}"')
    try:
        yield conn
    except BaseException:
        conn.execute(f'ROLLBACK TO "{sp}"')
        conn.execute(f'RELEASE "{sp}"')
        raise
    conn.execute(f'RELEASE "{sp}"')


class BuildIncomplete(RuntimeError):
    """빌드가 전 게이트를 통과하지 않은 DB — 서빙하면 안 된다."""


def connect_ro(
    db_path: Path | str | None = None, *, require_build: bool = True
) -> sqlite3.Connection:
    """읽기 전용 커넥션 — 소비자용. INSERT/UPDATE/DDL 이 전부 실패한다.

    기본으로 **빌드 표식(`build_meta`)을 확인**한다. 파일 존재만 보면 「한 번도 안 만든 DB」와
    「빌드가 실패해 빈 스키마만 남은 DB」가 같아 보이고, 소비자가 빈 골드를 「데이터 없음」으로
    오독한다(WORK-001 재검수 관찰). 표식은 전 게이트 통과 시에만 찍힌다.

    `require_build=False` 는 빌드 도중·테스트처럼 아직 표식이 없는 DB 를 열 때만 쓴다.
    """
    path = resolved_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"DB 가 없다: {path} — 먼저 빌드해야 한다")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    if require_build:
        try:
            assert_build_complete(conn)
        except BuildIncomplete:
            conn.close()
            raise
    return conn


def build_stamp(conn: sqlite3.Connection) -> sqlite3.Row | None:
    """빌드 표식 1행. 없으면 None(미빌드 또는 실패 빌드)."""
    has_table = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='build_meta'"
    ).fetchone()[0]
    if not has_table:
        return None
    return conn.execute("SELECT * FROM build_meta WHERE id = 1").fetchone()


def assert_build_complete(conn: sqlite3.Connection) -> sqlite3.Row:
    stamp = build_stamp(conn)
    if stamp is None:
        raise BuildIncomplete(
            "빌드 표식(build_meta)이 없다 — 미빌드이거나 게이트를 통과하지 못한 DB 다. "
            "`uv run python -m build all` 로 전 게이트를 통과시켜야 서빙할 수 있다"
        )
    return stamp
