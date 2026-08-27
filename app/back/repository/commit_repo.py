"""commit 표 접근 — 3층. 잔디 집계 + 수집기의 upsert + 어드민 히스토리 조회."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, cast, func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from dto.commit import CommitDayCountDTO, CommitItemDTO, CommitRepoCountDTO
from dto.daily import DailyCommitDTO
from models import Commit, GitToken, Repo

# 어드민 히스토리의 날짜 기준 — authored_at(timestamptz)의 KST 날짜.
# DB 세션 TZ 에 기대지 않고 식에 못박는다: timezone('Asia/Seoul', ts)::date
_KST = "Asia/Seoul"


def _kst_day():
    return cast(func.timezone(_KST, Commit.authored_at), Date)

# 전체 소급이면 수천 행이 온다 — 한 문장에 다 싣지 않고 자른다.
_INSERT_CHUNK = 500


class CommitRepository:
    async def insert_ignore(
        self, session: AsyncSession, rows: list[dict[str, Any]]
    ) -> int:
        """수집기의 upsert — (repo_id, tree) 충돌은 skip (erd uq_commit_repo_tree).

        리베이스가 같은 작업을 새 sha 로 되풀이하므로 충돌 키가 sha 가 아니라
        tree 다(models/commit.py). 넣은 행 수를 돌려준다.
        """
        inserted = 0
        for start in range(0, len(rows), _INSERT_CHUNK):
            chunk = rows[start : start + _INSERT_CHUNK]
            stmt = (
                pg_insert(Commit)
                .values(chunk)
                .on_conflict_do_nothing(index_elements=["repo_id", "tree"])
                .returning(Commit.id)
            )
            inserted += len((await session.execute(stmt)).scalars().all())
        return inserted

    async def list_daily(
        self, session: AsyncSession, since: date
    ) -> list[tuple[date, int]]:
        """날짜별 커밋 수 — 날짜는 KST(_kst_day), 어드민 달력과 같은 기준.

        summary 는 여기서 안 나른다 — 공개 잔디의 문장은 daily.summary 가
        정본이다(activity_service 가 합친다).
        """
        day = _kst_day()
        rows = (
            await session.execute(
                select(day.label("day"), func.count().label("count"))
                .where(day >= since)
                .group_by(day)
                .order_by(day)
            )
        ).all()
        return [(r[0], r[1]) for r in rows]

    # ── AI 하루 요약 파이프라인 ─────────────────────────────────────────

    async def list_for_kst_day(
        self, session: AsyncSession, day_on: date
    ) -> list[DailyCommitDTO]:
        """그날(KST) 커밋 전부 — 요약 프롬프트 입력용. message 원문 포함.

        회사 레포 여부는 레포에 연결된 git_token.kind == 'company' 로 판정한다
        — 프롬프트가 사내 정보를 추상화하는 근거.
        """
        day = _kst_day()
        rows = (
            await session.execute(
                select(Commit.id, Repo.slug, GitToken.kind, Commit.message)
                .join(Repo, Repo.id == Commit.repo_id)
                .outerjoin(GitToken, GitToken.id == Repo.git_token_id)
                .where(day == day_on)
                .order_by(Commit.authored_at, Commit.id)
            )
        ).all()
        return [
            DailyCommitDTO(
                id=r[0], repo_slug=r[1], is_company=(r[2] == "company"), message=r[3]
            )
            for r in rows
        ]

    async def update_summaries(
        self,
        session: AsyncSession,
        summaries: dict[int, str],
        summarized_at: datetime,
    ) -> None:
        """AI 한 줄로 summary 를 덮고 summarized_at 을 찍는다 — PK 벌크 UPDATE."""
        if not summaries:
            return
        await session.execute(
            update(Commit),
            [
                {"id": cid, "summary": s, "summarized_at": summarized_at}
                for cid, s in summaries.items()
            ],
        )

    async def unsummarized_days(
        self, session: AsyncSession, since: date, until: date
    ) -> list[date]:
        """[since, until] 안에서 미요약(summarized_at IS NULL) 커밋이 있는 KST 날짜들 — 오래된 순."""
        day = _kst_day()
        rows = (
            await session.execute(
                select(day.label("day"))
                .where(day >= since, day <= until, Commit.summarized_at.is_(None))
                .group_by(day)
                .order_by(day)
            )
        ).all()
        return [r[0] for r in rows]

    async def oldest_unsummarized_day(
        self, session: AsyncSession
    ) -> date | None:
        """가장 오래된 미요약 KST 날짜 — 백필 스크립트가 하나씩 소급할 때 쓴다."""
        day = _kst_day()
        row = (
            await session.execute(
                select(day.label("day"))
                .where(Commit.summarized_at.is_(None))
                .group_by(day)
                .order_by(day)
                .limit(1)
            )
        ).first()
        return row[0] if row else None

    # ── 어드민 커밋 히스토리 — 조회 전용 ────────────────────────────────

    async def count_days(
        self,
        session: AsyncSession,
        since: date,
        until: date,
        repo_id: int | None = None,
    ) -> list[CommitDayCountDTO]:
        """[since, until) 안의 KST 날짜별 커밋 수 — 한 달 스트립용."""
        day = _kst_day()
        stmt = (
            select(day.label("day"), func.count().label("count"))
            .where(day >= since, day < until)
            .group_by(day)
            .order_by(day)
        )
        if repo_id is not None:
            stmt = stmt.where(Commit.repo_id == repo_id)
        rows = (await session.execute(stmt)).all()
        return [CommitDayCountDTO(day=r[0].day, count=r[1]) for r in rows]

    async def count_repos(
        self, session: AsyncSession, since: date, until: date
    ) -> list[CommitRepoCountDTO]:
        """[since, until) 안에 커밋이 있는 레포만 — 칩 목록용. 건수 내림차순."""
        day = _kst_day()
        rows = (
            await session.execute(
                select(Repo.id, Repo.slug, func.count().label("count"))
                .select_from(Commit)
                .join(Repo, Repo.id == Commit.repo_id)
                .where(day >= since, day < until)
                .group_by(Repo.id, Repo.slug)
                .order_by(func.count().desc(), Repo.slug)
            )
        ).all()
        return [CommitRepoCountDTO(id=r[0], slug=r[1], count=r[2]) for r in rows]

    async def list_page(
        self,
        session: AsyncSession,
        since: date,
        until: date,
        repo_id: int | None,
        on_day: date | None,
        limit: int,
        offset: int,
    ) -> tuple[list[CommitItemDTO], int]:
        """필터(달 · 레포 · KST 날짜) 안의 한 페이지 + 전체 건수.

        message 원문을 함께 나른다 — 어드민 전용 펼침용. 공개 표면 금지.
        """
        day = _kst_day()
        conds = [day >= since, day < until]
        if repo_id is not None:
            conds.append(Commit.repo_id == repo_id)
        if on_day is not None:
            conds.append(day == on_day)

        total = (
            await session.execute(
                select(func.count()).select_from(Commit).where(*conds)
            )
        ).scalar_one()
        rows = (
            await session.execute(
                select(
                    Commit.id,
                    Repo.slug,
                    Commit.author,
                    Commit.authored_at,
                    Commit.summary,
                    Commit.message,
                    Commit.sha,
                )
                .join(Repo, Repo.id == Commit.repo_id)
                .where(*conds)
                .order_by(Commit.authored_at.desc(), Commit.id.desc())
                .limit(limit)
                .offset(offset)
            )
        ).all()
        items = [
            CommitItemDTO(
                id=r[0],
                repo_slug=r[1],
                author=r[2],
                authored_at=r[3],
                summary=r[4],
                message=r[5],
                sha=r[6],
            )
            for r in rows
        ]
        return items, total
