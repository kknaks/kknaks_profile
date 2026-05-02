"""환경 변수 기반 설정 — docker-compose / 로컬 dev / CI 모두 통일.

원칙: 코드 안에 hard-coded path 박지 않음. 모든 외부 의존(persona 위치, redis url 등)은 env로.

함수형 — 매 호출마다 env 평가 (monkeypatch.setenv 호환).
"""

from __future__ import annotations

import os
from pathlib import Path

_BACK_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _BACK_DIR.parent


def _env_path(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    return Path(raw).expanduser().resolve() if raw else default


# 페르소나 콘텐츠 위치 (docker는 /persona, 로컬은 ../persona)
# 모듈 import 시점에 한 번 평가 — 부팅 후 변경 X
PERSONA_DIR: Path = _env_path("PERSONA_DIR", _REPO_ROOT / "persona")


# 함수형 — 매 호출마다 env 평가 (테스트의 monkeypatch.setenv 호환)
def redis_url() -> str:
    return os.environ.get("REDIS_URL", "redis://localhost:46379")


def reload_token() -> str | None:
    return os.environ.get("RELOAD_TOKEN")


def run_scheduler() -> bool:
    return os.environ.get("RUN_SCHEDULER", "1") == "1"


def web_concurrency() -> int:
    return int(os.environ.get("WEB_CONCURRENCY", 1))


def job_git_push_dry_run() -> bool:
    return os.environ.get("JOB_GIT_PUSH_DRY_RUN", "1") == "1"
