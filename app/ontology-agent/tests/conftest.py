"""테스트 픽스처.

원천은 레포 밖(PII 포함)이라 `ONTOLOGY_DATA_DIR` 이 가리키는 경로가 있어야 돈다.
없으면 전 테스트를 skip 한다 — 원천 없는 환경에서 빨간 줄을 만들지 않기 위함.

**픽스처에 PII 원값을 쓰지 않는다.** 위조 표본은 전부 합성값이다.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build import gates, gold, load_bronze, masking, ontology, silver  # noqa: E402
from config import settings  # noqa: E402
from db.schema import bootstrap  # noqa: E402


def _source_available() -> bool:
    return (settings.data_dir / "bronze" / "vegas").is_dir()


requires_source = pytest.mark.skipif(
    not _source_available(),
    reason=f"원천 데이터 없음 — ONTOLOGY_DATA_DIR 를 지정하라 (현재: {settings.data_dir})",
)


@pytest.fixture(scope="session")
def built_db(tmp_path_factory) -> sqlite3.Connection:
    """전 계층을 한 번 빌드해 세션 내내 공유한다 — 78,216행 적재를 매번 돌리지 않는다."""
    if not _source_available():
        pytest.skip("원천 데이터 없음")
    path = tmp_path_factory.mktemp("db") / "ontology_demo.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    load_bronze.load(conn)
    silver.build(conn)
    masking.build(conn)
    gold.build(conn)
    try:
        ontology.load(conn)
    except Exception:
        # 1:1 대조는 전용 테스트가 판정한다 — 다른 테스트를 여기서 막지 않는다
        pass
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def built_db_path(tmp_path_factory):
    """전 게이트를 통과한 DB 파일 하나 — **빌드 표식까지 찍힌** 서빙 가능 상태.

    `built_db`(커넥션)와 달리 API 테스트는 앱이 자기 커넥션을 열어야 해서 경로가 필요하다.
    CLI `all` 을 그대로 태우므로 표식도 실제 경로로 찍힌다.
    """
    if not _source_available():
        pytest.skip("원천 데이터 없음")
    from build.__main__ import main as build_main

    path = tmp_path_factory.mktemp("serving") / "ontology_demo.db"
    assert build_main(["all", "--db", str(path)]) == 0
    return path


#: 로컬 검증용 임시값 — 배포 값과 무관하고 레포의 어느 기본값도 아니다.
TEST_PASSWORD = "test-only-not-a-real-secret"


@pytest.fixture
def client(monkeypatch, built_db_path):
    """게이트를 통과하지 않은 API 클라이언트. 401 경로를 보는 데 쓴다."""
    from fastapi.testclient import TestClient

    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "session_cookie_secure", False)  # TestClient 는 http 다
    import main

    with TestClient(main.app) as c:
        yield c


@pytest.fixture
def auth_client(client):
    r = client.post("/api/auth/session", json={"password": TEST_PASSWORD})
    assert r.status_code == 200
    return client


@pytest.fixture
def empty_db(tmp_path) -> sqlite3.Connection:
    conn = sqlite3.connect(tmp_path / "empty.db")
    conn.row_factory = sqlite3.Row
    bootstrap(conn)
    yield conn
    conn.close()
