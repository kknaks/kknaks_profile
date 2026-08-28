"""환경 설정 — 전부 env 에서 읽는다.

env 변수 이름은 레거시(compose · .env.prod)와 동일하게 유지한다 —
배포 환경의 .env 를 그대로 쓰기 위해서다.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# app/back/config.py → 리뉴얼 레포 루트. 컨테이너는 env REPO_ROOT 로 덮는다.
_DEFAULT_REPO_ROOT = str(Path(__file__).resolve().parent.parent.parent)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── 리포 루트 — para/ 의 md 원장을 검사할 때 기준 경로 ─
    # env 이름 REPO_ROOT 는 레거시 compose 와 동일하게 유지한다.
    repo_root: str = _DEFAULT_REPO_ROOT

    # ── DB ──────────────────────────────────────────────
    # 호스트에서 돌릴 때 기본값. 컨테이너는 compose 가 postgres:5432 로 덮는다.
    database_url: str = "postgresql+psycopg://kknaks:kknaks@localhost:45433/kknaks"
    db_echo: bool = False

    # ── redis — AI 실행 제출 큐(inbox.md Step 6·7) ────────
    # 컨테이너는 compose 가 redis:6379 로 덮는다. 워커(호스트)는 노출 포트로 붙는다.
    redis_url: str = "redis://localhost:46379/0"

    # ── 원장 — 승인 착지·commit·push 가 쓰는 레포 경로 ────
    # 읽기(md 서빙·codex cwd)는 repo_root/ai_cwd, 쓰기(착지)는 ledger_path 로
    # 분리 가능하다(inbox.md Step 7). 기본은 셋 다 이 레포 루트.
    ledger_path: str = _DEFAULT_REPO_ROOT

    # 착지 push 토글 — env 이름은 레거시(JOB_GIT_PUSH_DRY_RUN)와 동일하게 유지한다.
    # 1(dev): md 착지 + 그 파일만 로컬 commit, pull·push 는 스킵 — 커밋 sha 로
    #         commit_ref 를 확정하고 이후 단계는 정상 진행한다.
    # 0(운영): pull → push, push 성공이 확정 조건(케이스 1 정본 그대로).
    job_git_push_dry_run: bool = False

    # ── AI 실행 — open-kknaks 경유 codex (inbox.md Step 6) ─
    # ai_cwd·ai_schema_dir 는 **워커(호스트) 기준 경로**다 — codex 가 읽는다.
    # back 이 컨테이너면 컨테이너 내부 경로가 아니라 호스트 경로를 넣어야 한다.
    ai_cwd: str = _DEFAULT_REPO_ROOT                    # codex 읽기 전용 cwd (원장 레포)
    ai_schema_dir: str = str(Path(__file__).resolve().parent / "ai_schemas")
    ai_namespace: str = "kknaks_profile"                # redis 네임스페이스 — 워커와 일치
    ai_queue: str = "default"                           # 큐 이름 — 워커 --queues 와 일치
    ai_model: str | None = None                         # None 이면 codex 기본 모델
    ai_timeout_sec: int = 1200                          # 문서 생성 한 건의 상한

    # ── GitHub — 잔디(commit 수집) 케이스 6·7 ─────────────
    # 토큰 원문은 DB `git_token` 표에 Fernet 암호문으로 있고(어드민 설정에서 입력),
    # 여기는 복호 키 하나만 갖는다. 키 생성은 core/crypto.py 머리 주석.
    git_token_key: str | None = None

    # ── 인증 — httpOnly 쿠키 JWT ─────────────────────────
    jwt_secret: str = "dev-insecure-jwt-secret-change-me"
    jwt_expire_minutes: int = 720
    auth_cookie_name: str = "kknaks_session"
    auth_cookie_domain: str | None = None  # 운영은 .kknaks.cloud
    auth_cookie_secure: bool = False       # 운영은 1 — HTTPS 전용

    @field_validator("auth_cookie_domain", mode="before")
    @classmethod
    def _empty_domain_is_none(cls, v: str | None) -> str | None:
        """AUTH_COOKIE_DOMAIN= (빈 값) → None — 빈 Domain 속성을 쿠키에 싣지 않는다."""
        return v or None

    # ── 채용담당자 채팅 (SPEC-017 · DEC-026 · DEC-027) ────
    # 익명 세션 쿠키. **secure · domain 은 admin 쿠키(auth_cookie_*)를 그대로 쓴다** —
    # 같은 사이트·같은 배포라 두 벌로 두면 한쪽만 갱신되고 조용히 갈린다.
    chat_cookie_name: str = "chat_sid"
    chat_cookie_max_age_sec: int = 30 * 24 * 3600      # 30일 sliding (DEC-026 D1)

    # 제출 계약 — DEC-027 OQ-5 에서 닫힌 값들이다.
    # ⚠ 모델은 **정식 표기만** 유효하다. 축약형(`terra`)은 metadata 조회 실패로 400 이
    #   되고 에러 문구가 인증 문제처럼 읽힌다(레퍼런스 실측 — mediness submission.py).
    # ⚠ 모델과 reasoning effort 는 짝이다 — 모델을 바꾸면 허용 effort 를 다시 잰다.
    chat_model: str = "gpt-5.6-terra"
    chat_queue: str = "chat"                            # 전용 큐 — default 와 줄을 안 세운다
    chat_timeout_sec: int = 180
    chat_reasoning_effort: str = "low"

    # MCP — 별도 HTTP 서버(DEC-027 D5). 컨테이너 기준 주소를 compose 가 덮는다.
    chat_mcp_url: str = "http://mcp:28081/mcp"
    chat_mcp_server_key: str = "kknaks"                  # `-c mcp_servers.<key>.…` 의 key
    # turn 전용 Bearer 토큰의 수명. turn 상한(180초)보다 넉넉히 길게 둔다 —
    # 마감 때 해시를 지우는 것이 실제 폐기이고, 이 값은 그마저 실패했을 때의 자연 만료다.
    chat_turn_token_ttl_sec: int = 900

    # ── 시드 — admin 계정 (seed/seed_users.py 만 읽는다) ──
    admin_username: str = "admin"
    admin_password: str = "changeme"

    # ── CORS — 쿠키 인증이라 origin 을 * 로 열 수 없다 ────
    cors_origins: list[str] = [
        "http://localhost:3000",           # front dev (npm run dev)
        "https://profile.kknaks.cloud",    # front 운영 (Vercel)
    ]


@lru_cache
def get_settings() -> Settings:
    """싱글턴 — import 시점이 아니라 첫 호출 시점에 env 를 읽는다 (테스트에서 덮기 쉽게)."""
    return Settings()
