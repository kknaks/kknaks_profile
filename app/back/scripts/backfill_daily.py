"""daily 백필 — 과거 날짜의 커밋 AI 요약을 사람이 하나씩 소급한다.

자동 판(summarize_recent)은 최근 7일 창만 돌므로, 그보다 오래된 날짜는
이 스크립트로 하나씩 요약한다.

사용법:
    호스트:   cd app/back && uv run python -m scripts.backfill_daily [YYYY-MM-DD]
    컨테이너: docker exec kknaks-back uv run python -m scripts.backfill_daily [YYYY-MM-DD]

- 인자 있으면 그 날짜(KST)를 요약한다
- 인자 없으면 **가장 오래된 미요약 날짜 하나**를 골라 요약한다

전제: open-kknaks 워커가 호스트에 떠 있어야 한다 — `bash app/back/scripts/run-worker.sh`.
실패하면 daily.error 에 남는다 — 같은 날짜를 다시 돌리면 재시도다.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date

from core.db import SessionLocal, engine
from repository.commit_repo import CommitRepository
from service.summarize_service import summarize_service


async def _main() -> int:
    if len(sys.argv) > 2:
        print(__doc__)
        return 2
    if len(sys.argv) == 2:
        try:
            day = date.fromisoformat(sys.argv[1])
        except ValueError:
            print(f"날짜 형식이 아님: {sys.argv[1]} — YYYY-MM-DD")
            return 2
    else:
        async with SessionLocal() as session:
            day = await CommitRepository().oldest_unsummarized_day(session)
        if day is None:
            print("미요약 날짜 없음 — 전부 요약돼 있다")
            return 0
        print(f"가장 오래된 미요약 날짜: {day}")

    print(f"{day} 요약 시작 — codex 한 호출(수십 초 걸릴 수 있다)…")
    try:
        n = await summarize_service.summarize_date(day)
    except Exception as exc:
        print(f"실패 — daily.error 에 남음: {exc}")
        return 1
    if n == 0:
        print(f"{day} — 커밋 0건, 스킵")
    else:
        print(f"{day} — 커밋 {n}건 요약 완료 (daily.summary 갱신)")
    return 0


def main() -> None:
    async def run() -> int:
        try:
            return await _main()
        finally:
            await engine.dispose()

    raise SystemExit(asyncio.run(run()))


if __name__ == "__main__":
    main()
