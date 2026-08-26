"""역할별 persona md 렌더 — DB 파생물. SoT 는 DB(career·product·problem).

erd 의 personal/company 규약: 표면에 보이는 것은 DB, md 는 파생. 이 서비스는
career 한 행을 읽어 그 역할의 persona md 를 **통째로 덮어쓴다**(append 아님) —
md 는 순수 DB 파생이라 손으로 안 고치고, 매일 다시 렌더해도 같은 결과가 나온다.

경로는 career.persona_path 가 있으면 그 경로, 없으면
`para/areas/personal/company/<회사 slug>/<역할 title kebab>.md` 로 파생한다.
쓰기 기준은 LEDGER_PATH(승인 착지와 같은 원장 루트).

요청 밖(스케줄·수동 트리거)에서 돌아 get_db 를 못 쓴다 — 세션을 직접 연다.
문제(problem)는 0건이면 견본과 같은 「아직 없음」 문구로 채운다.
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from config import get_settings
from core.db import SessionLocal
from dto.career import CareerDTO
from dto.problem import ProblemDTO
from dto.product import ProductDTO
from repository.career_repo import CareerRepository
from repository.company_repo import CompanyRepository
from repository.problem_repo import ProblemRepository
from repository.product_repo import ProductRepository

logger = logging.getLogger(__name__)

_KST = ZoneInfo("Asia/Seoul")
_SCHEDULE_HOUR = 8        # 매일 KST 08:10 — 잔디(08:00) 뒤에 돈다
_SCHEDULE_MINUTE = 10

# 견본 두 장(ax-lead·backend-dev)의 머리 주석 그대로.
_HEADER = (
    "<!-- DB 파생 · 자동 생성 — 손으로 고치지 않는다. "
    "SoT 는 DB(career·product·problem·commit).\n"
    "     스케줄이 career.persona_path 를 따라 이 파일을 매일 덮어쓴다. -->"
)
_NO_PROBLEM = "_(아직 없음 — 이력서 알맹이. 회고에서 올라온다)_"


def _kebab(text: str) -> str:
    """역할 title 을 파일명 slug 로 — 소문자·공백은 하이픈."""
    return re.sub(r"\s+", "-", text.strip().lower())


def _period(career: CareerDTO) -> str:
    """`YYYY.MM — YYYY.MM` (진행 중이면 오른쪽이 「현재」)."""
    start = f"{career.started_on:%Y.%m}"
    end = "현재" if career.ended_on is None else f"{career.ended_on:%Y.%m}"
    return f"{start} — {end}"


class PersonaService:
    def __init__(
        self,
        career_repo: CareerRepository,
        product_repo: ProductRepository,
        problem_repo: ProblemRepository,
        company_repo: CompanyRepository,
    ) -> None:
        self._career_repo = career_repo
        self._product_repo = product_repo
        self._problem_repo = problem_repo
        self._company_repo = company_repo
        self._running = False

    # ── 트리거 ──────────────────────────────────────────────────────────
    def start(self) -> bool:
        """백그라운드로 전체 재렌더를 건다. 이미 돌고 있으면 안 겹치고 False."""
        if self._running:
            return False
        asyncio.get_running_loop().create_task(self.render_all())
        return True

    async def render_all(self) -> list[str]:
        """모든 career 의 persona md 를 다시 렌더한다 — 반환은 쓴 상대경로 목록."""
        if self._running:
            logger.info("persona: already running — skip")
            return []
        self._running = True
        try:
            async with SessionLocal() as session:
                careers = await self._career_repo.list_public(session)
                products = await self._product_repo.list_with_career(session)
                problems = await self._problem_repo.list_with_names(session)
                companies = await self._company_repo.list_with_stats(session)

            slug_by_company = {c.company.id: c.company.slug for c in companies}

            # visible 제품만, 역할별로 묶고 id ASC(만든 순서) 정렬.
            products_by_career: dict[int, list[ProductDTO]] = {}
            for p in products:
                if p.visible:
                    products_by_career.setdefault(p.career_id, []).append(p)
            for items in products_by_career.values():
                items.sort(key=lambda p: p.id)

            problems_by_career: dict[int, list[ProblemDTO]] = {}
            for pr in problems:
                problems_by_career.setdefault(pr.career_id, []).append(pr)

            ledger = Path(get_settings().ledger_path)
            written: list[str] = []
            for career in careers:
                rel = self._resolve_path(career, slug_by_company)
                text = self._render(
                    career,
                    products_by_career.get(career.id, []),
                    problems_by_career.get(career.id, []),
                )
                target = ledger / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
                written.append(rel)
            logger.info("persona: rendered %d files — %s", len(written), written)
            return written
        finally:
            self._running = False

    # ── 경로·렌더 ───────────────────────────────────────────────────────
    def _resolve_path(
        self, career: CareerDTO, slug_by_company: dict[int, str]
    ) -> str:
        if career.persona_path:
            return career.persona_path
        slug = slug_by_company.get(career.company_id) or f"company-{career.company_id}"
        return f"para/areas/personal/company/{slug}/{_kebab(career.title)}.md"

    def _render(
        self,
        career: CareerDTO,
        products: list[ProductDTO],
        problems: list[ProblemDTO],
    ) -> str:
        lines: list[str] = [_HEADER, "", f"# {career.title} · {career.company_name}", ""]

        status = "재직 중" if career.ended_on is None else "퇴임"
        meta = f"`{_period(career)}` · {status}"
        if career.company_location:
            meta += f" · {career.company_location}"
        lines.append(meta)
        if career.stack:
            lines.append("스택 — " + " · ".join(career.stack))

        lines += ["", "## 역할", ""]
        lines.append((career.description or "").strip() or "_(아직 없음)_")

        lines += ["", "## 만든 것", ""]
        if products:
            for p in products:
                head = f"- **{p.title}**"
                if p.status:
                    head += f" `{p.status}`"
                if p.summary:
                    head += f" — {p.summary}"
                lines.append(head)
                if p.detail_path:
                    lines.append(f"  → `{p.detail_path}`")
        else:
            lines.append("_(아직 없음)_")

        lines += ["", "## 해결한 문제", ""]
        if problems:
            for pr in problems:
                lines.append(f"- **{pr.title}**")
                if pr.body:
                    lines += ["", pr.body.strip(), ""]
        else:
            lines.append(_NO_PROBLEM)

        return "\n".join(lines).rstrip() + "\n"

    # ── 스케줄 — 매일 KST 08:10 ─────────────────────────────────────────
    async def run_scheduler(self) -> None:
        """가벼운 asyncio 루프 — 다음 08:10 까지 자고 전체를 재렌더한다."""
        while True:
            now = datetime.now(_KST)
            next_run = now.replace(
                hour=_SCHEDULE_HOUR,
                minute=_SCHEDULE_MINUTE,
                second=0,
                microsecond=0,
            )
            if next_run <= now:
                next_run += timedelta(days=1)
            wait = (next_run - now).total_seconds()
            logger.info("persona scheduler: next run %s (in %.0fs)", next_run, wait)
            await asyncio.sleep(wait)
            try:
                await self.render_all()
            except Exception:  # 스케줄 루프는 죽지 않는다
                logger.exception("persona scheduler: run failed")


persona_service = PersonaService(
    CareerRepository(),
    ProductRepository(),
    ProblemRepository(),
    CompanyRepository(),
)
