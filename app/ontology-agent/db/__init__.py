"""DB 계층 — 커넥션 규약과 스키마 부트스트랩.

메달리온 전 계층(bronze/silver/gold/ontology)이 SQLite 한 파일에 들어간다.
소비자(도구·API·에이전트)는 `connect_ro()` + 마스킹 뷰로만 닿는다 — DEC-002.
"""

from .connection import (
    BuildIncomplete,
    assert_build_complete,
    atomic,
    build_stamp,
    connect,
    connect_ro,
    resolved_db_path,
)
from .schema import BRONZE_TABLES, bootstrap

__all__ = [
    "connect", "connect_ro", "atomic", "resolved_db_path", "bootstrap", "BRONZE_TABLES",
    "BuildIncomplete", "assert_build_complete", "build_stamp",
]
