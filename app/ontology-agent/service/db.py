"""서빙용 DB 접속 — 도구와 API 가 **같은 읽기 전용 커넥션 헬퍼**를 쓴다(WORK-002 계약).

`connect_ro` 가 빌드 표식까지 확인하므로, 게이트를 통과하지 못한 DB 는 여기서 열리지
않는다 — 실패한 빌드가 정상처럼 서빙되는 경로를 남기지 않는다.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from db.connection import BuildIncomplete, connect_ro

from .errors import SourceUnavailable


@contextmanager
def open_serving_db(db_path: Path | str | None = None):
    """읽기 전용 커넥션 하나. 접근 실패는 전부 `SOURCE_UNAVAILABLE` 로 모은다."""
    try:
        conn = connect_ro(db_path, require_build=True)
    except FileNotFoundError as exc:
        raise SourceUnavailable(str(exc)) from exc
    except BuildIncomplete as exc:
        raise SourceUnavailable(str(exc)) from exc
    except sqlite3.Error as exc:
        raise SourceUnavailable(f"DB 접근 실패: {exc}") from exc
    try:
        yield conn
    except sqlite3.Error as exc:
        raise SourceUnavailable(f"조회 실패: {exc}") from exc
    finally:
        conn.close()
