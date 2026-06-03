"""neetcode-canonical 잡 1회 수동 실행 (cron 23:00 UTC 안 기다리고 즉시 검증).

push 정책: env `JOB_GIT_PUSH_DRY_RUN` 따름 (1=dry-run / 0=실 push).

전제:
- redis + worker 컨테이너 떠있음 (잔디 잡과 동일 인프라 — spec-03 §11.8)
- app/back deps 설치됨
- repo root 의 `.env` 박혀있음 (CLAUDE_CODE_OAUTH_TOKEN, GH_TOKEN_PERSONAL ...)

사용법:
    docker exec -w /repo/app/back kknaks-back uv run python ../scripts/run_neetcode_canonical.py

또는 로컬 (app/back/.env 박혀있고 redis worker 띄운 상태):
    cd app/back && uv run python ../scripts/run_neetcode_canonical.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "app" / "back"))

# load .env
ENV_PATH = REPO / ".env"
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


async def main() -> None:
    # 백엔드 부팅 안 한 환경에서 호출 가능하도록 — load_all() 셀프 호출 시 PERSONA_DIR 가야 함
    from service.jobs.algorithms.main import run_neetcode_canonical_job

    result = await run_neetcode_canonical_job()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
