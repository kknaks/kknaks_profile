"""수동 호출용 dev 스크립트 — content enrich 잡 1회 실행.

trigger (webhook/scheduler) 박기 전 검증용 — 사용자가 pending MD 박은 후 직접 호출:

    cd back && uv run python ../scripts/run_content_enrich.py

전제:
- redis 컨테이너 떠있음 (docker compose up redis)
- ClaudeWorker 컨테이너 떠있음 (docker compose up worker)
- back/ 의 deps install 완료 (uv sync)
- persona/contents/ 에 status: pending 인 MD 존재
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# back/ 을 sys.path 에 추가 (스크립트가 repo root 의 scripts/ 에서 실행되므로)
BACK_DIR = Path(__file__).resolve().parent.parent / "back"
sys.path.insert(0, str(BACK_DIR))

from service.jobs.content_enrich import run_content_enrich_job  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


async def main() -> int:
    """잡 1회 실행. dry_run_push=True 로 실 push 안 함 (수정된 MD 는 working tree 에 남음)."""
    n = await run_content_enrich_job(dry_run_push=True)
    print(f"\n=== content_enrich done: processed={n} ===")
    if n > 0:
        print("수정된 MD 는 git working tree 에 있음 — git diff 로 확인 후 직접 commit.")
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
