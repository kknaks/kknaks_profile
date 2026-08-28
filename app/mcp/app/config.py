"""mcp 설정 — 전부 env.

back 주소만 필수다. 이 서버는 **상태를 갖지 않는다** — 토큰 검증도 노출 판정도 back 이
하고, 여기는 tool 스키마를 정의해 중계할 뿐이다(DEC-027 D5).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # 컨테이너 기준 주소. compose 가 덮는다.
    chat_back_url: str = "http://back:8000"
    chat_back_timeout_sec: float = 10.0

    log_level: str = "INFO"

    # Streamable HTTP transport 의 DNS rebinding 보호. 컨테이너 이름·포트로 들어오므로
    # 기본값(localhost 한정)으로는 거부된다 — 실제 Host 를 명시한다.
    mcp_allowed_hosts: str = "mcp,mcp:28081,localhost,localhost:28081,127.0.0.1:28081"
    mcp_allowed_origins: str = ""

    @property
    def allowed_hosts(self) -> list[str]:
        return [h.strip() for h in self.mcp_allowed_hosts.split(",") if h.strip()]

    @property
    def allowed_origins(self) -> list[str]:
        return [o.strip() for o in self.mcp_allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
