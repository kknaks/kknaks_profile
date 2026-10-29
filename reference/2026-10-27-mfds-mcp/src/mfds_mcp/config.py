"""설정 — 프로세스 env 가 먼저, 없으면 프로젝트 폴더의 `.env`."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# src/mfds_mcp/config.py → 프로젝트 폴더
PROJECT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_BASE_URL = "https://apis.data.go.kr/1471000"


def read_env_file(path: Path) -> dict[str, str]:
    """`KEY=VALUE` 줄만 읽는다. 주석 · 빈 줄 · 따옴표를 처리한다. 값은 어디에도 출력하지 않는다."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        name, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[name.strip()] = value
    return values


@dataclass(frozen=True)
class Config:
    api_key: str | None
    base_url: str = DEFAULT_BASE_URL
    cache_dir: Path = PROJECT_DIR / "cache"
    cache_ttl_days: int = 7
    daily_limit: int = 1000
    max_pages: int = 10
    timeout_seconds: float = 30.0

    def __repr__(self) -> str:  # 키 값이 repr · 로그로 새지 않게
        return (
            f"Config(api_key={'<set>' if self.api_key else None}, base_url={self.base_url!r}, "
            f"cache_dir={str(self.cache_dir)!r}, cache_ttl_days={self.cache_ttl_days}, "
            f"daily_limit={self.daily_limit}, max_pages={self.max_pages}, timeout_seconds={self.timeout_seconds})"
        )

    __str__ = __repr__

    @classmethod
    def load(cls, env: dict[str, str] | None = None, env_file: Path | None = None) -> Config:
        file_values = read_env_file(env_file or Path(os.environ.get("MFDS_ENV_FILE", PROJECT_DIR / ".env")))
        source = os.environ if env is None else env

        def get(name: str) -> str | None:
            value = source.get(name)
            if value is None or value.strip() == "":
                value = file_values.get(name)
            if value is None or value.strip() == "":
                return None
            return value.strip()

        def get_int(name: str, default: int) -> int:
            value = get(name)
            return int(value) if value is not None else default

        cache_dir = get("MFDS_CACHE_DIR")
        return cls(
            api_key=get("MFDS_API_KEY"),
            base_url=(get("MFDS_BASE_URL") or DEFAULT_BASE_URL).rstrip("/"),
            cache_dir=Path(cache_dir).expanduser() if cache_dir else PROJECT_DIR / "cache",
            cache_ttl_days=get_int("MFDS_CACHE_TTL_DAYS", 7),
            daily_limit=get_int("MFDS_DAILY_LIMIT", 1000),
            max_pages=get_int("MFDS_MAX_PAGES", 10),
            timeout_seconds=float(get("MFDS_TIMEOUT_SECONDS") or 30),
        )
