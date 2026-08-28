"""테스트 토대 — 일회용 postgres + alembic upgrade + 앱 클라이언트.

## sqlite 로 안 되는 이유

이 스키마는 postgres 기능에 기대 있다 — `JSONB` · `ARRAY(Text)` · **부분 유니크
인덱스**(`uq_chat_message_pending` · `uq_algorithm_today`). 직렬화 invariant 를 DB 가
강제한다는 것이 계약의 일부인데(SPEC-017 §5), sqlite 로 돌리면 그 부분이 통째로
검증에서 빠진다.

## create_all 이 아니라 alembic 인 이유

migration 이 스키마의 정본이다. `Base.metadata.create_all` 로 세우면 모델과 migration 이
갈려도 테스트가 초록으로 남는다 — 배포에서만 터진다. 그래서 실제 배포와 같은 경로로
세운다.

컨테이너는 `TEST_DATABASE_URL` 이 있으면 띄우지 않는다 — CI 나 이미 띄워 둔 DB 를 쓸 때.
"""

from __future__ import annotations

import os
import socket
import subprocess
import time
import uuid
from pathlib import Path

import pytest

_BACK_DIR = Path(__file__).resolve().parent.parent
_IMAGE = "postgres:16-alpine"
_PG_USER = "kknaks"
_PG_PASSWORD = "kknaks"
_PG_DB = "kknaks_test"
_container: str | None = None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _wait_ready(container: str, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        probe = subprocess.run(
            ["docker", "exec", container, "pg_isready", "-U", _PG_USER, "-d", _PG_DB],
            capture_output=True,
        )
        if probe.returncode == 0:
            return
        time.sleep(0.4)
    raise RuntimeError(f"테스트 postgres 가 {timeout}초 안에 뜨지 않았다: {container}")


def _start_postgres() -> str:
    """일회용 postgres 하나. 반환 = DATABASE_URL."""
    global _container
    port = _free_port()
    name = f"kknaks-test-pg-{uuid.uuid4().hex[:12]}"
    result = subprocess.run(
        [
            "docker", "run", "-d", "--rm", "--name", name,
            "-e", f"POSTGRES_USER={_PG_USER}",
            "-e", f"POSTGRES_PASSWORD={_PG_PASSWORD}",
            "-e", f"POSTGRES_DB={_PG_DB}",
            "-p", f"127.0.0.1:{port}:5432",
            _IMAGE,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"docker 로 테스트 postgres 를 띄우지 못했다: {result.stderr.strip()}")
    _container = name
    _wait_ready(name)
    return (
        f"postgresql+psycopg://{_PG_USER}:{_PG_PASSWORD}@127.0.0.1:{port}/{_PG_DB}"
    )


# ── 앱 import **전에** env 를 세운다 ─────────────────────
# `core/db.py` 가 import 시점에 엔진을 만든다 — 그 전에 URL 이 정해져 있어야 한다.
DATABASE_URL = os.environ.get("TEST_DATABASE_URL") or _start_postgres()
os.environ["DATABASE_URL"] = DATABASE_URL
# 리포 루트 — `detail_path` 해석의 기준. 테스트는 실제 원장을 읽지 않지만 공개 루트
# 판정(`core/chat_detail.py`)이 이 값을 쓴다.
os.environ.setdefault("REPO_ROOT", str(_BACK_DIR.parent.parent))

subprocess.run(
    ["uv", "run", "alembic", "upgrade", "head"],
    cwd=_BACK_DIR,
    env={**os.environ, "DATABASE_URL": DATABASE_URL},
    check=True,
    capture_output=True,
)


def pytest_sessionfinish(session, exitstatus) -> None:  # noqa: ARG001
    if _container:
        subprocess.run(["docker", "rm", "-f", _container], capture_output=True)


# ── fixtures ────────────────────────────────────────────
@pytest.fixture
async def db():
    """요청 밖에서 DB 를 만질 때 쓰는 세션(시드·검증)."""
    from core.db import SessionLocal

    async with SessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def _clean_tables():
    """테스트마다 빈 DB — 표를 지우지 않고 비운다(스키마는 한 번만 세운다)."""
    from sqlalchemy import text

    from core.db import SessionLocal
    from models import Base

    names = ", ".join(f'"{t}"' for t in Base.metadata.tables)
    async with SessionLocal() as session:
        await session.execute(text(f"TRUNCATE {names} RESTART IDENTITY CASCADE"))
        await session.commit()
    yield


@pytest.fixture
async def client(monkeypatch):
    """앱 클라이언트. **AI 제출은 막는다** — 큐도 워커도 없는 곳에서 도는 테스트다.

    `start_turn` 을 갈아 끼우는 이유: 라우터가 `BackgroundTasks` 로 부르므로 의존성
    override 로는 못 잡는다. 제출 배선 자체는 `test_chat_submission.py` 가 따로 본다.
    """
    import httpx

    import api.chat_router as chat_router
    from main import create_app

    submitted: list[int] = []

    async def _fake_start_turn(message_id: int) -> None:
        submitted.append(message_id)

    monkeypatch.setattr(chat_router, "start_turn", _fake_start_turn)

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as http_client:
        http_client.submitted = submitted  # type: ignore[attr-defined]
        yield http_client
