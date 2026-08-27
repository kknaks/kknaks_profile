"""커밋 AI 요약 — 하루(KST 날짜) 단위. 잔디 수집(케이스 6·7) 뒤에 자동 연쇄.

게이트 없음(케이스 6 「잔디는 자동이어도 된다」). 호출은 **날짜당 1번** —
그날 커밋 메시지 전부를 open-kknaks·codex 한 호출에 넣고 output_schema
(ai_schemas/daily_summary.json)로 {commits, daily} 를 받는다. 입력은 메시지만
— diff 는 안 나른다.

착지는 두 곳이다:
- commit.summary  — 수집 때 넣은 「메시지 첫 줄」을 AI 한 줄로 덮고 summarized_at
- daily.summary   — 레포 단위 불릿(줄바꿈 구분). 공개 잔디 툴팁의 정본

자동 판(summarize_recent)은 **최근 7일 창만** 돈다 — 과거 소급은
scripts/backfill_daily.py 로 사람이 하나씩. 실패 격리는 날짜 단위 —
실패는 daily.error 에 남고(성공하면 비운다) 다음 판이 자동 재시도한다.

요청 밖(백그라운드·스케줄)에서 돌아 get_db 를 못 쓴다 — 세션을 직접 연다.
AI 제출은 ai_service 의 검증된 경로(_run_codex — redis 제출·output_schema
전달)를 그대로 탄다. 실행 주체는 호스트 워커(scripts/run-worker.sh)다.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from core.db import SessionLocal
from dto.daily import DailyCommitDTO
from repository.commit_repo import CommitRepository
from repository.daily_repo import DailyRepository
from service.ai_service import _run_codex

logger = logging.getLogger(__name__)

_KST = ZoneInfo("Asia/Seoul")
_WINDOW_DAYS = 7          # 자동 판의 창 — 오늘 포함 최근 7일
_MSG_CAP = 1500           # 커밋 메시지 하나의 상한 — codex 컨텍스트 보호
_SCHEMA = "daily_summary.json"


def _clip(text: str) -> str:
    return text if len(text) <= _MSG_CAP else text[:_MSG_CAP] + "\n…(잘림)"


def _prompt(day: date, commits: list[DailyCommitDTO]) -> str:
    """하루치 커밋 메시지 → 요약 지시. 회사 레포는 사내 정보 추상화를 명시한다."""
    by_repo: dict[str, list[DailyCommitDTO]] = {}
    for c in commits:
        by_repo.setdefault(c.repo_slug, []).append(c)

    lines = [
        f"하루치 커밋 메시지를 요약한다. 날짜: {day.isoformat()} (KST) · 총 {len(commits)}건.",
        "",
        "## 출력 (강제된 JSON schema)",
        "- commits: 아래 **모든** 커밋에 대해 하나씩 — id 는 입력 그대로, summary 는"
        " 한국어 한 줄 80자 이내. 무엇을 했는지가 남게 다듬는다(접두어·이슈번호 제거).",
        "- daily: 하루 요약 불릿 배열 — **레포(제품/프로젝트) 단위**로 묶는다."
        " 형식: `<레포 이름> — <핵심 작업 요지들> (<그 레포 커밋 수>)`."
        " 예: `mediness — 사용량 집계 버그 수정, 목록 페이지네이션 (5)`.",
        "- daily 는 한 줄 80자 이내, **최대 4줄**. 레포가 4개를 넘으면 작은 것끼리"
        " 한 줄에 묶는다(커밋 수는 합산). 레포 이름은 owner 없이 name 만 쓴다.",
        "",
        "## 보안 — [회사] 표시가 붙은 레포",
        "- 사내 정보는 추상화한다 — 제품명·기능 수준까지만 쓴다.",
        "- 고객명·내부 시스템명·URL·호스트명·티켓/이슈 번호를 출력에 넣지 않는다.",
        "",
        "## 커밋 메시지 (id · 원문)",
    ]
    for slug, items in by_repo.items():
        mark = " [회사]" if items[0].is_company else ""
        lines.append("")
        lines.append(f"### {slug}{mark} — {len(items)}건")
        for c in items:
            lines.append(f"- id={c.id}")
            body = _clip((c.message or "").strip()) or "(메시지 없음)"
            lines.extend("  " + ln for ln in body.splitlines())
    return "\n".join(lines)


class SummarizeService:
    def __init__(
        self, commit_repo: CommitRepository, daily_repo: DailyRepository
    ) -> None:
        self._commit_repo = commit_repo
        self._daily_repo = daily_repo

    # ── 트리거 ──────────────────────────────────────────────────────────
    def start_date(self, day: date) -> None:
        """한 날짜 재요약을 백그라운드로 건다 — 어드민 202 응답용."""
        asyncio.get_running_loop().create_task(self._run_date_logged(day))

    async def _run_date_logged(self, day: date) -> None:
        try:
            await self.summarize_date(day)
        except Exception:  # 실패는 summarize_date 가 daily.error 에 이미 남겼다
            logger.exception("summarize: %s failed", day)

    # ── 하루 요약 ───────────────────────────────────────────────────────
    async def summarize_date(self, day: date) -> int:
        """그날(KST) 커밋 전부를 1호출로 요약. 넣은 커밋 요약 수를 돌려준다.

        커밋 0건이면 아무것도 안 하고 0. 실패는 daily.error 에 남기고 다시 던진다.
        """
        async with SessionLocal() as session:
            commits = await self._commit_repo.list_for_kst_day(session, day)
        if not commits:
            logger.info("summarize: %s — 커밋 0건, 스킵", day)
            return 0

        try:
            payload, _ = await _run_codex(_prompt(day, commits), _SCHEMA)
            known = {c.id for c in commits}
            summaries = {
                int(e["id"]): str(e["summary"]).strip()
                for e in payload.get("commits", [])
                if int(e["id"]) in known and str(e["summary"]).strip()
            }
            bullets = [
                str(b).strip() for b in payload.get("daily", []) if str(b).strip()
            ]
            if not summaries or not bullets:
                raise ValueError("AI 응답에 commits/daily 가 비어 있음")
        except Exception as exc:
            # 실패 격리 — 날짜 단위. error 만 남기고(summary 는 유지) 다음 판이 재시도.
            async with SessionLocal() as session:
                await self._daily_repo.upsert_error(session, day, str(exc)[:1000])
                await session.commit()
            raise

        now = datetime.now(timezone.utc)
        async with SessionLocal() as session:
            await self._commit_repo.update_summaries(session, summaries, now)
            await self._daily_repo.upsert_summary(session, day, "\n".join(bullets))
            await session.commit()
        logger.info(
            "summarize: %s — %d/%d commits, %d bullets",
            day,
            len(summaries),
            len(commits),
            len(bullets),
        )
        return len(summaries)

    # ── 자동 판 — 최근 7일 창 ───────────────────────────────────────────
    async def summarize_recent(self) -> None:
        """오늘(KST)~7일 전 중 미요약 커밋이 있는 날짜만, 오래된 순으로.

        날짜별 try/except — 한 날짜가 실패해도 다른 날짜는 계속 간다.
        """
        today = datetime.now(_KST).date()
        since = today - timedelta(days=_WINDOW_DAYS - 1)
        async with SessionLocal() as session:
            days = await self._commit_repo.unsummarized_days(session, since, today)
        if not days:
            logger.info("summarize: 최근 %d일 창에 미요약 날짜 없음", _WINDOW_DAYS)
            return
        for day in days:
            try:
                await self.summarize_date(day)
            except Exception:
                logger.exception("summarize: %s failed — 다음 날짜 계속", day)


summarize_service = SummarizeService(CommitRepository(), DailyRepository())
