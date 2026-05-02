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


def github_webhook_secret() -> str | None:
    return os.environ.get("GITHUB_WEBHOOK_SECRET")


def gh_accounts() -> list[dict]:
    """잔디 잡용 계정 list — 빈 user/token 은 skip.

    각 entry: {"user", "token", "email"}.
    email 은 commit author 필터 — 본인 commit 만 발라냄 (PR merge 시 다른 사람 commit 제외).
    `GH_TOKEN` (legacy) 는 GH_TOKEN_PERSONAL fallback.
    """
    accounts: list[dict] = []
    personal_user = os.environ.get("GH_USER_PERSONAL", "kknaks")
    personal_token = os.environ.get("GH_TOKEN_PERSONAL") or os.environ.get("GH_TOKEN", "")
    personal_email = os.environ.get("GH_EMAIL_PERSONAL", "")
    if personal_user and personal_token:
        accounts.append({"user": personal_user, "token": personal_token, "email": personal_email})

    company_user = os.environ.get("GH_USER_COMPANY", "")
    company_token = os.environ.get("GH_TOKEN_COMPANY", "")
    company_email = os.environ.get("GH_EMAIL_COMPANY", "")
    if company_user and company_token:
        accounts.append({"user": company_user, "token": company_token, "email": company_email})

    return accounts
