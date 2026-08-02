"""레포 레지스트리 (KDEV-WORK-017 P5 / KDEV-SPEC-011).

여기서 고정하는 것은 셋이다.

    1. `github.com/` 접두를 떼야 클론 URL 이 깨지지 않는다
    2. 개인 계정이 **둘**이다 — 소유자만 보고 토큰을 고르면 하나가 샌다
    3. `company` 는 `detail` 없이 못 들어간다. 시드가 지어내지 않는다
"""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import TrackedRepo
from service.jobs.repo_registry import (
    UnknownCareerError,
    account_for,
    enabled_repos,
    parse_slug,
    scan_showcase,
    seed_company_from_showcase,
    seed_from_showcase,
)
from tests.conftest import isolate_tables

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

needs_db = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


@pytest.fixture
async def db():
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
    await isolate_tables(conn, "tracked_repos")
    session = AsyncSession(
        bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint"
    )
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    def showcase(name: str, org: str, url: str, visible: str = "true") -> None:
        d = tmp_path / "products" / name
        d.mkdir(parents=True)
        (d / "showcase.md").write_text(
            f"---\ntype: project\norg: {org}\nvisible: {visible}\n"
            f"links:\n  repo: \"{url}\"\n---\n\n# {name}\n",
            encoding="utf-8",
        )

    showcase("mediness", "company", "github.com/MediSolveAIDev/mediness", "false")
    showcase("profile", "studio", "github.com/kknaks/kknaks_profile")
    showcase("mykakao", "studio", "github.com/kknaksss/mykakao", "false")

    # company 시드가 `detail` 이 실재하는 career stem 인지 확인한다.
    career = tmp_path / "persona" / "career"
    career.mkdir(parents=True)
    (career / "medisolve-ai.md").write_text(
        "---\ntype: career\nis_current: true\n---\n\n## 무슨 일 하는지\n", encoding="utf-8"
    )
    return tmp_path


class TestParseSlug:
    def test_strips_the_host(self):
        """안 떼면 클론 URL 이 github.com/github.com/... 이 된다."""
        assert parse_slug("github.com/kknaks/wine_log") == "kknaks/wine_log"
        assert parse_slug("https://github.com/kknaks/wine_log") == "kknaks/wine_log"
        assert parse_slug("https://www.github.com/kknaks/wine_log.git") == "kknaks/wine_log"

    def test_bare_slug_passes_through(self):
        assert parse_slug("kknaks/wine_log") == "kknaks/wine_log"

    def test_garbage_is_none(self):
        assert parse_slug("") is None
        assert parse_slug("not a repo") is None


class TestAccount:
    def test_both_personal_accounts_use_the_personal_token(self):
        """개인 계정이 둘이다 — 하나만 알면 나머지가 조용히 빠진다."""
        assert account_for("kknaks/wine_log") == "personal"
        assert account_for("kknaksss/mykakao") == "personal"

    def test_org_uses_the_company_token(self):
        assert account_for("MediSolveAIDev/mediness") == "company"


class TestScan:
    def test_visible_false_is_still_tracked(self, repo):
        """사이트 표시와 추적은 다른 축이다 — 그 둘을 가르려고 레지스트리를 만들었다."""
        slugs = {e.slug for e in scan_showcase(repo)}
        assert "MediSolveAIDev/mediness" in slugs
        assert "kknaksss/mykakao" in slugs

    def test_org_decides_the_type(self, repo):
        by_slug = {e.slug: e for e in scan_showcase(repo)}
        assert by_slug["MediSolveAIDev/mediness"].type == "company"
        assert by_slug["kknaks/kknaks_profile"].type == "studio"


@needs_db
class TestSeed:
    async def test_company_is_skipped_and_counted(self, db, repo):
        """`detail` 을 지어내지 않는다 — 어느 career 로 갈지는 사람이 정한다."""
        result = await seed_from_showcase(db, repo)
        assert result["added"] == 2  # studio 둘
        assert result["needs_detail"] == 1  # company 하나

        rows = (await db.scalars(select(TrackedRepo))).all()
        assert {r.slug for r in rows} == {"kknaks/kknaks_profile", "kknaksss/mykakao"}
        assert all(r.type == "studio" and r.detail is None for r in rows)

    async def test_seeding_twice_adds_nothing(self, db, repo):
        """사람이 손본 detail·enabled 를 덮지 않는다."""
        await seed_from_showcase(db, repo)
        second = await seed_from_showcase(db, repo)
        assert second["added"] == 0

    async def test_company_needs_detail_at_the_db_level(self, db):
        """앱이 아니라 DB 가 막는다 — 깨지면 career 귀속이 조용히 틀린다."""
        db.add(TrackedRepo(slug="org/x", type="company", account="company"))
        with pytest.raises(IntegrityError):
            await db.flush()

    async def test_studio_must_not_carry_detail(self, db):
        db.add(
            TrackedRepo(
                slug="kknaks/y", type="studio", account="personal", detail="medisolve-ai"
            )
        )
        with pytest.raises(IntegrityError):
            await db.flush()

    async def test_disabled_repo_drops_out_of_the_scan(self, db, repo):
        await seed_from_showcase(db, repo)
        rows = (await db.scalars(select(TrackedRepo))).all()
        rows[0].enabled = False
        await db.flush()

        active = await enabled_repos(db)
        assert rows[0].slug not in {r.slug for r in active}
        # 지우지 않는다 — 과거 조사 이력의 참조가 끊긴다.
        assert (await db.scalars(select(TrackedRepo))).all()


@needs_db
class TestCompanySeed:
    """`company` 를 넣는 경로 (KDEV-WORK-017 결함 ④).

    `seed_from_showcase()` 가 company 를 건너뛰는 것은 옳지만, 그러면 **넣을 방법이
    아무데도 없었다.** 프로덕션 호출부가 0이라 배포하면 레지스트리가 빈 채로 뜨고
    잔디가 매일 `NO_ACTIVITY` 로 끝난다 — 실패로 보이지 않아서 한참 모른다.
    """

    async def test_company_lands_with_the_given_detail(self, db, repo):
        await seed_from_showcase(db, repo)
        result = await seed_company_from_showcase(db, repo, detail="medisolve-ai")

        assert result["added"] == 1
        row = (
            await db.scalars(
                select(TrackedRepo).where(TrackedRepo.type == "company")
            )
        ).one()
        assert row.slug == "MediSolveAIDev/mediness"
        assert row.detail == "medisolve-ai"
        # 회사 레포는 회사 토큰으로 클론한다 — 개인 토큰이면 권한이 없다.
        assert row.account == "company"

    async def test_unknown_career_stem_is_refused(self, db, repo):
        """오타는 DB CHECK 를 통과한다 — `detail IS NOT NULL` 만 보기 때문이다.

        막지 않으면 조사까지 정상으로 돌다가 **발행 단계에서** 없는 문서에 쓰려다
        그날 career 가 사라진다. 승인 화면까지 가서야 보이는 실패다.
        """
        with pytest.raises(UnknownCareerError):
            await seed_company_from_showcase(db, repo, detail="medisolve-ia")

        assert (await db.scalars(select(TrackedRepo))).all() == []

    async def test_running_twice_adds_nothing(self, db, repo):
        """배포 스크립트는 다시 돌려도 안전해야 한다 — 사람이 손본 값을 안 덮는다."""
        await seed_company_from_showcase(db, repo, detail="medisolve-ai")
        second = await seed_company_from_showcase(db, repo, detail="medisolve-ai")
        assert second["added"] == 0

    async def test_existing_detail_is_not_overwritten(self, db, repo):
        """사람이 다른 career 로 옮겨 놨으면 그대로 둔다."""
        await seed_company_from_showcase(db, repo, detail="medisolve-ai")
        row = (
            await db.scalars(select(TrackedRepo).where(TrackedRepo.type == "company"))
        ).one()
        row.detail = "bitcamp"
        await db.flush()

        await seed_company_from_showcase(db, repo, detail="medisolve-ai")

        refreshed = (
            await db.scalars(select(TrackedRepo).where(TrackedRepo.type == "company"))
        ).one()
        assert refreshed.detail == "bitcamp"
