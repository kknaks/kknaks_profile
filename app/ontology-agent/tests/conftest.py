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


@pytest.fixture
def empty_db(tmp_path) -> sqlite3.Connection:
    conn = sqlite3.connect(tmp_path / "empty.db")
    conn.row_factory = sqlite3.Row
    bootstrap(conn)
    yield conn
    conn.close()
