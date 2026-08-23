"""PDF 생성 잡 — planning-02.

playwright (chromium headless) 로 front `/print/*` 라우트 hit → PDF 떨굼.
출력은 `app/front/public/{name}.pdf` + git commit/push (spec-06 §5 공유 함수).

생성 PDF: resume.pdf (A4 portrait), portfolio.pdf (A4 landscape).
"""

from __future__ import annotations

import logging
from pathlib import Path

import config
from service.jobs.git_push import commit_and_push_with_retry

logger = logging.getLogger("kknaks-back.pdf-generate")

# 출력 위치 — repo 의 app/front/public/ 고정 (planning-02 §2.2)
_REPO_ROOT = Path(__file__).resolve().parents[4]
PUBLIC_DIR = _REPO_ROOT / "app" / "front" / "public"

# A4 portrait — 핸드오프 §8 의 sheet 크기와 일치 (CSS 픽셀 794×1123 ≈ 210×297mm @ 96dpi)
_PDF_BASE_OPTS = {
    "format": "A4",
    "print_background": True,
    "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
}
PDF_OPTS_PORTRAIT = dict(_PDF_BASE_OPTS)
PDF_OPTS_LANDSCAPE = {**_PDF_BASE_OPTS, "landscape": True}


async def render_pdf(route: str, output_name: str, *, landscape: bool = False) -> Path:
    """front `route` 를 hit 해서 `app/front/public/{output_name}` 으로 PDF 저장.

    Returns 출력 파일 경로.
    """
    from playwright.async_api import async_playwright

    url = f"{config.frontend_url()}{route}"
    output_path = PUBLIC_DIR / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_opts = PDF_OPTS_LANDSCAPE if landscape else PDF_OPTS_PORTRAIT

    logger.info("rendering PDF: url=%s landscape=%s → %s", url, landscape, output_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            # @media print 활성 — desk padding/gap 0 + box-shadow 제거 (print.css).
            # 미적용 시 desk 패딩이 시트 사이에 누적되어 빈 PDF 페이지 발생.
            await page.emulate_media(media="print")
            # Next.js dev 첫 컴파일 + HMR ws → networkidle/load 모두 안 떨어짐.
            # domcontentloaded + Pager 측정 완료 sentinel 대기.
            await page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            # 모든 Pager 측정 + 분할 끝나면 PrintResume/Portfolio 가 [data-print-ready] sentinel 박음.
            # state="attached" — sentinel 은 display:none 이라 visible 대기 X.
            await page.wait_for_selector("[data-print-ready]", state="attached", timeout=30_000)
            await page.pdf(path=str(output_path), **pdf_opts)
        finally:
            await browser.close()

    logger.info("PDF saved: %s (%d bytes)", output_path, output_path.stat().st_size)
    return output_path


async def run_pdf_generate_job(*, dry_run_push: bool | None = None) -> int:
    """resume.pdf + portfolio.pdf 생성 → git commit/push (idempotent — diff 없으면 skip).

    Returns 생성 시도한 PDF 개수 (push 여부와 무관).
    """
    resume_path = await render_pdf("/print/resume", "resume.pdf", landscape=False)
    portfolio_path = await render_pdf("/print/portfolio", "portfolio.pdf", landscape=True)

    dry_run = config.job_git_push_dry_run() if dry_run_push is None else dry_run_push
    commit_and_push_with_retry(
        paths=[resume_path, portfolio_path],
        message="chore: regen resume.pdf + portfolio.pdf",
        dry_run=dry_run,
    )
    return 2
