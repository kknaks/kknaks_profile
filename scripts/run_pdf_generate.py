"""수동 호출용 dev 스크립트 — PDF 생성 잡 1회 실행 (planning-02 P1.0).

전제:
- frontend dev server 떠있음 (cd frontend && npm run dev → :3000)
- back/.venv 셋업 완료 (uv sync) + playwright chromium 설치
    cd back && uv add playwright && uv run playwright install chromium

실행:
    cd back && uv run python ../scripts/run_pdf_generate.py

출력: frontend/public/resume.pdf
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

BACK_DIR = Path(__file__).resolve().parent.parent / "back"
sys.path.insert(0, str(BACK_DIR))

from service.jobs.pdf_generate import run_pdf_generate_job  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


async def main() -> int:
    n = await run_pdf_generate_job()
    print(f"\n=== pdf_generate done: rendered={n} ===")
    print("frontend/public/resume.pdf 확인 — 브라우저로 열어서 PDF 정상인지 검증.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
