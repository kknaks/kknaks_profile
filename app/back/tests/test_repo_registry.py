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
    account_for,
    enabled_repos,
    parse_slug,
    scan_showcase,
    seed_from_showcase,
)

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
