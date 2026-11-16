"""P1 — DB 부트스트랩과 브론즈 스키마."""

from __future__ import annotations

import sqlite3

import pytest

from build.__main__ import STAGES, main
from db.connection import connect_ro
from db.schema import BRONZE_TABLES, table_names


def test_부트스트랩이_브론즈_16테이블을_만든다(empty_db):
    tables = table_names(empty_db, "bronze_")
    assert len(tables) == 16
    assert sorted(tables) == sorted(BRONZE_TABLES)


def test_읽기전용_커넥션은_쓰기를_거부한다(tmp_path):
    path = tmp_path / "ro.db"
    write = sqlite3.connect(path)
    write.execute("CREATE TABLE t (a)")
    write.commit()
    write.close()

    # 빌드 표식이 없는 생 DB 라 `require_build=False` — 여기서 보는 것은 쓰기 거부다
    ro = connect_ro(path, require_build=False)
    assert ro.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 0
    with pytest.raises(sqlite3.OperationalError):
        ro.execute("INSERT INTO t VALUES (1)")
    with pytest.raises(sqlite3.OperationalError):
        ro.execute("CREATE TABLE t2 (a)")
    ro.close()


def test_읽기전용_커넥션은_없는_DB_를_열지_않는다(tmp_path):
    with pytest.raises(FileNotFoundError):
        connect_ro(tmp_path / "없다.db")


def test_빌드_표식이_없으면_기본적으로_열리지_않는다(tmp_path):
    """「한 번도 안 만든 DB」와 「빌드가 실패한 DB」를 파일 존재만으로는 구분할 수 없다 —
    표식이 그 구분을 만든다(WORK-001 재검수 관찰 · WORK-002 도입)."""
    from db.connection import BuildIncomplete
    from db.schema import bootstrap

    path = tmp_path / "unbuilt.db"
    conn = sqlite3.connect(path)
    bootstrap(conn)
    conn.commit()
    conn.close()

    with pytest.raises(BuildIncomplete):
        connect_ro(path)
    connect_ro(path, require_build=False).close()   # 명시하면 열린다


def test_CLI_가_단계별_실행과_게이트_단독_재실행을_노출한다(capsys):
    """WORK-005 전건 재실행이 이 인터페이스를 쓴다."""
    for stage in ("bronze", "silver", "gold", "ontology", "all", "gate1", "gate2", "gate3"):
        assert stage in STAGES

    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "python -m build" in out
    assert "--db" in out
