"""환경 변수 기반 설정 — docker-compose / 로컬 dev / CI 모두 통일.

원칙: 코드 안에 hard-coded path 박지 않음. 모든 외부 의존(persona 위치, redis url 등)은 env로.

함수형 — 매 호출마다 env 평가 (monkeypatch.setenv 호환).
"""

from __future__ import annotations

import os
from pathlib import Path

_BACK_DIR = Path(__file__).resolve().parent
_APP_DIR = _BACK_DIR.parent
_REPO_ROOT = _APP_DIR.parent


def _env_path(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    return Path(raw).expanduser().resolve() if raw else default


# 페르소나 콘텐츠 위치 (docker는 /repo/persona, 로컬은 repo/persona)
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
def frontend_url() -> str:
    """PDF 생성 잡 (planning-02) 이 hit 할 frontend base URL.

    로컬 dev: http://localhost:3000 (next dev)
    프로덕션: https://kknaks.dev (Vercel)
    docker (back container) Mac: host.docker.internal:3000.
    """
    return os.environ.get("FRONTEND_URL", "http://localhost:3000").rstrip("/")


def github_webhook_secret() -> str | None:
    return os.environ.get("GITHUB_WEBHOOK_SECRET")


def gh_accounts() -> list[dict]:
    """잔디 잡용 계정 list — 빈 user/token 은 skip.

    각 entry: {"user", "token", "email"}.
    email 은 commit author 필터 — 본인 commit 만 발라냄 (PR merge 시 다른 사람 commit 제외).
    """
    accounts: list[dict] = []
    personal_user = os.environ.get("GH_USER_PERSONAL", "kknaks")
    personal_token = os.environ.get("GH_TOKEN_PERSONAL", "")
    personal_email = os.environ.get("GH_EMAIL_PERSONAL", "")
    if personal_user and personal_token:
        accounts.append({"user": personal_user, "token": personal_token, "email": personal_email})

    company_user = os.environ.get("GH_USER_COMPANY", "")
    company_token = os.environ.get("GH_TOKEN_COMPANY", "")
    company_email = os.environ.get("GH_EMAIL_COMPANY", "")
    if company_user and company_token:
        accounts.append({"user": company_user, "token": company_token, "email": company_email})

    return accounts


def gh_token(account: str) -> str | None:
    """`tracked_repos.account` → 클론·fetch 토큰 (KDEV-SPEC-011 §5 「토큰」).

    `gh_accounts()` 와 달리 **user/email 이 없어도 토큰만 있으면 준다.** 클론에 필요한
    것은 토큰뿐이고, user/email 은 커밋 author 를 정할 때 쓰는 값이라 조사는 쓰지 않는다.
    """
    key = "GH_TOKEN_COMPANY" if account == "company" else "GH_TOKEN_PERSONAL"
    return os.environ.get(key, "").strip() or None


def bot_identity() -> dict | None:
    """서버가 git pull/commit/push 시 사용할 identity (planning-01 §3.6 ③/④ 채널).

    `gh_accounts()[0]` (= personal, default `kknaks`) 을 사용. user/token/email 모두 박혀야 valid.
    None 반환 시 호출자는 push/pull 자체를 skip 또는 dry_run 으로 fallback.
    """
    accounts = gh_accounts()
    if not accounts:
        return None
    primary = accounts[0]
    if not (primary.get("user") and primary.get("token") and primary.get("email")):
        return None
    return primary


def bot_emails() -> set[str]:
    """self-push webhook 필터용 — 서버가 commit 한 push 는 webhook 처리 skip.

    모든 account 의 email 을 한 set 으로. email 빈 account 는 자동 제외.
    """
    return {a["email"] for a in gh_accounts() if a.get("email")}


def database_url() -> str:
    """SQLAlchemy 2.0 동기 엔진용 DSN (auth-01 — DB화 토대).

    docker-compose 안: postgresql+psycopg://kknaks:kknaks@postgres:5432/kknaks
    호스트(로컬 dev): localhost:45433 로 노출.
    """
    return os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://kknaks:kknaks@localhost:45433/kknaks",
    )


def admin_username() -> str:
    """.env 로 시드하는 관리자 계정 아이디 (auth-01 §유저 시드)."""
    return os.environ.get("ADMIN_USERNAME", "admin")


def admin_password() -> str:
    """.env 로 시드하는 관리자 평문 비밀번호 — 시드 시 bcrypt 해시로 저장."""
    return os.environ.get("ADMIN_PASSWORD", "changeme")


def jwt_secret() -> str:
    """쿠키 JWT(HS256) 서명 시크릿. 운영은 반드시 .env 로 강한 값 주입."""
    return os.environ.get("JWT_SECRET", "dev-insecure-jwt-secret-change-me")


def jwt_expire_minutes() -> int:
    """로그인 세션(JWT exp) 유효 분. 기본 12시간."""
    return int(os.environ.get("JWT_EXPIRE_MINUTES", 720))


def auth_cookie_name() -> str:
    return os.environ.get("AUTH_COOKIE_NAME", "kknaks_session")


def auth_cookie_domain() -> str | None:
    """쿠키 domain. 로컬은 비움(host-only), 운영은 `.kknaks.cloud` 로 서브도메인 공유."""
    raw = os.environ.get("AUTH_COOKIE_DOMAIN", "").strip()
    return raw or None


def auth_cookie_secure() -> bool:
    """HTTPS 전용 여부. 로컬 http dev 는 0, 운영은 1."""
    return os.environ.get("AUTH_COOKIE_SECURE", "0") == "1"


def graph_json_path() -> Path:
    """KDEV-WORK-001 — 지식그래프 산출물 `_graph.json` 경로 (best-effort write).

    기본은 repo 루트(`persona` 와 sibling). 읽기전용 FS 등으로 실패해도 부팅 영향 없음.
    """
    raw = os.environ.get("GRAPH_JSON_PATH")
    return Path(raw).expanduser().resolve() if raw else PERSONA_DIR.parent / "_graph.json"


# ── 잔디 커밋 조사 (KDEV-WORK-017 P5 / KDEV-SPEC-011) ──


def repo_cache_dir() -> Path:
    """bare 클론을 두는 곳. **레포 작업트리 밖이어야 한다**(SPEC-011 §5 「클론 위치」).

    안에 두면 발행 경로의 작업트리 초기화가 클론을 통째로 지운다 — 321MB 를 매번
    다시 받는다는 뜻이다. 그 불변은 `service/jobs/repos.py` 가 실행 시점에 확인한다.

    컨테이너는 `/var/cache/repos`(compose 볼륨), 로컬은 `~/.cache/kknaks/repos`.
    """
    raw = os.environ.get("REPO_CACHE_DIR")
    if raw:
        return Path(raw).expanduser().resolve()
    return Path.home().joinpath(".cache", "kknaks", "repos").resolve()


def github_clone_base() -> str:
    """클론 URL 의 앞부분. `{base}{slug}.git` 로 조립한다.

    바꿀 일은 사실상 없고 **테스트가 로컬 레포를 원격처럼 쓰기 위한 이음매다.**
    이 seam 이 없으면 「`clone --bare` 는 refspec 을 남기지 않는다」 같은 결함을
    네트워크 없이 재현할 방법이 없다.
    """
    return os.environ.get("GITHUB_CLONE_BASE", "https://github.com/")


def commit_identity_patterns() -> list[str]:
    """author 매칭 패턴. **고정 email 목록을 쓰지 않는다**(SPEC-011 §4 수집 규칙).

    `git log --author` 는 부분매칭이라 `kknaks` 하나로 name·email 여러 형태를 잡는다.
    BL-004 이 실측한 identity 3종(`kknaks@medisolveai.com`·`benesia93@naver.com`·
    `*@*.local`)이 전부 이 한 패턴에 걸린다 — 목록으로 두면 새 identity 가 조용히 샌다.
    """
    raw = _csv_env("COMMIT_IDENTITY_PATTERNS")
    return sorted(raw) if raw else ["kknaks"]


def commit_max_per_repo() -> int:
    """레포당 커밋 상한. 넘으면 최신 순으로 자르고 `truncated` 에 남긴다."""
    return int(os.environ.get("COMMIT_MAX_PER_REPO", 30))


def commit_diff_bytes_per_repo() -> int:
    """레포당 diff 총량 상한(바이트)."""
    return int(os.environ.get("COMMIT_DIFF_BYTES_PER_REPO", 32 * 1024))


def commit_diff_bytes_per_commit() -> int:
    """커밋당 diff 상한(바이트)."""
    return int(os.environ.get("COMMIT_DIFF_BYTES_PER_COMMIT", 8 * 1024))


def git_timeout_seconds() -> float:
    """클론·fetch 한 번의 상한. 걸리면 그 레포만 실패로 남고 나머지는 계속한다."""
    return float(os.environ.get("GIT_TIMEOUT_SECONDS", 600))


# ── Slack 지식 캡처 (KDEV-WORK-012 — 별도 프로세스에서 back lifespan 으로 흡수) ──


def repo_root() -> Path:
    """레포 루트. 캡처 노트 경로 조립과 git 작업의 기준."""
    raw = os.environ.get("REPO_ROOT")
    return Path(raw).expanduser().resolve() if raw else PERSONA_DIR.parent


def slack_capture_enabled() -> bool:
    """Socket Mode 캡처 기동 여부. 기본 0 — 토큰이 없는 환경에서 부팅을 막지 않는다."""
    return os.environ.get("SLACK_CAPTURE_ENABLED", "0") == "1"


def slack_bot_token() -> str | None:
    return os.environ.get("SLACK_BOT_TOKEN") or None


def slack_app_token() -> str | None:
    return os.environ.get("SLACK_APP_TOKEN") or None


def _csv_env(key: str) -> set[str]:
    return {v.strip() for v in os.environ.get(key, "").split(",") if v.strip()}


def allowed_slack_users() -> set[str]:
    """허용 사용자. 비어 있으면 fail-closed — 모든 입력을 무시한다(OKK-SPEC-011 §4)."""
    return _csv_env("ALLOWED_SLACK_USERS")


def allowed_slack_channels() -> set[str]:
    """허용 채널. 비어 있으면 fail-closed."""
    return _csv_env("ALLOWED_SLACK_CHANNELS")


def capture_namespace() -> str:
    return os.environ.get("NAMESPACE", "kknaks-portfolio")


def capture_provider() -> str:
    return os.environ.get("CAPTURE_PROVIDER", "claude")


def capture_model() -> str | None:
    return os.environ.get("CAPTURE_MODEL") or None


def capture_work_dir() -> str:
    return os.environ.get("CAPTURE_WORK_DIR", str(repo_root()))


def capture_timeout_seconds() -> float:
    return float(os.environ.get("CAPTURE_TIMEOUT_SECONDS", 600))
