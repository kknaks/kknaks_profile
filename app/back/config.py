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
