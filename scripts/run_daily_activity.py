"""수동 호출용 dev 스크립트 — 잔디 잡 1회 실행 (cron 00:05 KST 안 기다리고 즉시 검증).

target_date 미지정 → 어제 entry 박음 (spec-03 §1.1).

전제:
- redis + worker 컨테이너 떠있음 (`docker compose up -d redis worker`)
- back deps 설치됨 (`cd back && uv sync`)
- repo root 의 `.env` 박혀있음 (CLAUDE_CODE_OAUTH_TOKEN, GH_TOKEN_PERSONAL, GH_EMAIL_PERSONAL ...)

사용법:
    cd back && uv run python ../scripts/run_daily_activity.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACK_DIR = REPO_ROOT / "back"
sys.path.insert(0, str(BACK_DIR))


def _load_dotenv(path: Path) -> None:
    """수동 .env 로더 — python-dotenv 의존 회피. setdefault 라 기존 env 가 우선."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv(REPO_ROOT / ".env")

from main import load_all  # noqa: E402
from service.jobs.main_job import run_daily_activity_job  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


async def main() -> int:
    """잡 1회 실행. dry_run_push=True 로 실 push 안 함 (daily/{date}.md 만 갱신, working tree 에 남음)."""
    # 호스트 스크립트는 lifespan 안 발동 → 메모리 dict 빈 상태. 잡 시작 전 explicit load.
    load_all()
    entry = await run_daily_activity_job(dry_run_push=True)

    print("\n=== daily_activity_job done ===")
    print(f"date:    {entry['date']}")
    if entry.get("skipped"):
        print(f"skipped: {entry.get('reason')}")
        return 0
    counts = entry.get("counts", {})
    print(f"counts:  commit={counts.get('commit', 0)} note={counts.get('note', 0)} study={counts.get('study', 0)}")
    summary = entry.get("summary")
    if summary:
        print(f"summary ko: {summary.get('ko')}")
        print(f"summary en: {summary.get('en')}")
    else:
        print("summary: (활동 없음 — LLM 호출 skip)")
    print()
    print(f"daily/{entry['date'].replace('.', '-')}.md 변경분: git diff persona/daily/")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
