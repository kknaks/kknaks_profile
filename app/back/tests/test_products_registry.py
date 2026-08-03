"""제품 등록 오케스트레이션 (KDEV-WORK-018 P3 / KDEV-SPEC-014 §4 Case Matrix).

여기서 지키는 계약 셋.

- **검증 실패면 아무것도 만들어지지 않는다** — 파일도 행도 없다
- **`company` 는 파일을 만들지 않는다**(D9)
- **커밋 실패면 파일이 남지 않는다** — `publish_atomic` 이 되돌린다
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import frontmatter
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import config
from core.models import TrackedRepo
from service.products import registry, scaffold
from service.products.errors import ProductError, ProductNotFound, ScaffoldError
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

CARD = {
    "title": {"ko": "제품", "en": "Product"},
    "summary": {"ko": "한 줄", "en": "One line"},
    "category": "backend",
    "status": "wip",
    "stack": ["FastAPI"],
}


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
    """**진짜 git 레포다.** 롤백을 검증하려면 커밋 이력이 있어야 한다."""
    templates = tmp_path / "templates" / "product"
    for rel in scaffold.SCAFFOLD_FILES:
        target = templates / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# {rel}\n", encoding="utf-8")

    (tmp_path / "products").mkdir()
    (tmp_path / "products" / "README.md").write_text(
        "# Products\n\n| Product | Context |\n|---|---|\n", encoding="utf-8"
    )
    meta = tmp_path / "persona" / "_meta.yaml"
    meta.parent.mkdir(parents=True, exist_ok=True)
    meta.write_text("projects:\n  categories:\n    - id: backend\n", encoding="utf-8")
    career = tmp_path / "persona" / "career"
    career.mkdir(parents=True, exist_ok=True)
    (career / "medisolve-ai.md").write_text("---\ntype: career\n---\n", encoding="utf-8")

    for args in (
        ["git", "init", "-q", "-b", "main"],
        ["git", "config", "user.email", "t@example.com"],
        ["git", "config", "user.name", "t"],
        ["git", "add", "-A"],
        ["git", "commit", "-qm", "init"],
    ):
        subprocess.run(args, cwd=tmp_path, check=True, capture_output=True)
    return tmp_path


@needs_db
class TestRegisterStudio:
    async def test_files_and_row_land_together(self, db, repo: Path) -> None:
        row = await registry.register(
            db,
            repo="github.com/kknaks/ax-graph",
            kind="studio",
            product_slug="ax-knowledge-graph",
            card=CARD,
            repo_root=repo,
            dry_run=True,
        )
        assert row.slug == "kknaks/ax-graph"
        assert row.product_slug == "ax-knowledge-graph"
        assert row.detail is None  # studio 는 career 귀속이 없다

        base = repo / "products" / "ax-knowledge-graph"
        assert {p.name for p in base.rglob("*.md")} >= {"README.md", "showcase.md"}
        card = frontmatter.load(base / "showcase.md").metadata
        assert card["type"] == "project" and card["visible"] is False

    async def test_index_row_is_added(self, db, repo: Path) -> None:
        await registry.register(
            db,
            repo="kknaks/ax-graph",
            kind="studio",
            product_slug="ax-knowledge-graph",
            card=CARD,
            repo_root=repo,
            dry_run=True,
        )
        text_ = (repo / "products" / "README.md").read_text(encoding="utf-8")
        assert "| ax-knowledge-graph | `products/ax-knowledge-graph/` |" in text_


@needs_db
class TestRegisterCompany:
    async def test_company_makes_no_files(self, db, repo: Path) -> None:
        """회사 레포는 문서 트리도 카드도 없이 레지스트리에만 산다 (D9)."""
        before = {p for p in (repo / "products").rglob("*")}
        row = await registry.register(
            db,
            repo="MediSolveAIDev/mediness",
            kind="company",
            detail="medisolve-ai",
            repo_root=repo,
            dry_run=True,
        )
        assert row.type == "company" and row.detail == "medisolve-ai"
        assert row.product_slug is None
        assert {p for p in (repo / "products").rglob("*")} == before

    async def test_company_without_career_is_refused(self, db, repo: Path) -> None:
        with pytest.raises(ProductError) as exc:
            await registry.register(
                db, repo="org/x", kind="company", repo_root=repo, dry_run=True
            )
        assert exc.value.code == "CAREER_REQUIRED"


@needs_db
class TestNothingIsCreatedOnRejection:
    @pytest.mark.parametrize(
        "kwargs,code",
        [
            ({"repo": "not a repo", "product_slug": "alpha"}, "INVALID_SLUG"),
            ({"repo": "a/b", "product_slug": "Alpha"}, "INVALID_PRODUCT_SLUG"),
            ({"repo": "a/b", "product_slug": None}, "INVALID_PRODUCT_SLUG"),
        ],
    )
    async def test_no_files_no_row(self, db, repo: Path, kwargs, code) -> None:
        with pytest.raises(ProductError) as exc:
            await registry.register(
                db, kind="studio", card=CARD, repo_root=repo, dry_run=True, **kwargs
            )
        assert exc.value.code == code
        assert (await db.scalars(select(TrackedRepo))).all() == []
        assert [p.name for p in (repo / "products").iterdir()] == ["README.md"]

    async def test_bad_category_creates_nothing(self, db, repo: Path) -> None:
        """**통과했다면 persona 로드 전체가 죽는다.**"""
        with pytest.raises(ProductError) as exc:
            await registry.register(
                db,
                repo="a/b",
                kind="studio",
                product_slug="alpha",
                card={**CARD, "category": "mobile"},
                repo_root=repo,
                dry_run=True,
            )
        assert exc.value.code == "CATEGORY_INVALID"
        assert not (repo / "products" / "alpha").exists()


@needs_db
class TestCommitFailureLeavesNothing:
    async def test_push_failure_rolls_back_files(self, db, repo: Path, monkeypatch) -> None:
        """`commit_and_push_with_retry` 를 안 쓰는 이유가 이것이다 — 롤백이 없다.

        여기서는 커밋까지 갔다가 push 에서 죽는 상황을 만든다. 파일이 남으면 다음
        `reset --hard origin/main` 이 조용히 지우고, 그 사이 `product_doc_pipeline` 은
        미완성 트리를 본다.
        """
        real = subprocess.run

        def fake(args, *a, **kw):
            if isinstance(args, list) and "push" in args:
                raise subprocess.CalledProcessError(1, args, b"", b"push rejected")
            return real(args, *a, **kw)

        monkeypatch.setattr(subprocess, "run", fake)

        with pytest.raises(ScaffoldError):
            await registry.register(
                db,
                repo="kknaks/ax-graph",
                kind="studio",
                product_slug="alpha",
                card=CARD,
                repo_root=repo,
                dry_run=False,
            )

        assert not (repo / "products" / "alpha").exists()
        assert (await db.scalars(select(TrackedRepo))).all() == []


@needs_db
class TestUpdate:
    async def test_unsent_field_is_not_cleared(self, db, repo: Path) -> None:
        """**`detail` 을 안 보낸 것과 `null` 을 보낸 것은 다르다.**

        구분하지 않으면 `enabled` 만 토글하는 요청이 company 행의 career 귀속을
        조용히 지운다.
        """
        row = await registry.register(
            db,
            repo="MediSolveAIDev/mediness",
            kind="company",
            detail="medisolve-ai",
            repo_root=repo,
            dry_run=True,
        )
        updated = await registry.update(
            db, row.id, enabled=False, fields_set={"enabled"}, repo_root=repo
        )
        assert updated.enabled is False
        assert updated.detail == "medisolve-ai"

    async def test_product_link_changes_without_moving_files(self, db, repo: Path) -> None:
        row = await registry.register(
            db,
            repo="kknaks/ax-graph",
            kind="studio",
            product_slug="alpha",
            card=CARD,
            repo_root=repo,
            dry_run=True,
        )
        updated = await registry.update(
            db,
            row.id,
            product_slug="beta",
            fields_set={"product_slug"},
            repo_root=repo,
        )
        assert updated.product_slug == "beta"
        # 파일은 그대로다 — 연결만 바뀐다.
        assert (repo / "products" / "alpha" / "showcase.md").exists()

    async def test_missing_row_is_reported(self, db, repo: Path) -> None:
        with pytest.raises(ProductNotFound):
            await registry.update(db, 999_999, fields_set=set(), repo_root=repo)


@needs_db
class TestDerivedFields:
    async def test_product_exists_is_computed_not_stored(self, db, repo: Path) -> None:
        """저장하면 디렉토리를 지운 순간부터 값이 거짓말을 한다 (D7)."""
        row = await registry.register(
            db,
            repo="kknaks/ax-graph",
            kind="studio",
            product_slug="alpha",
            card=CARD,
            repo_root=repo,
            dry_run=True,
        )
        assert registry.product_exists(row.product_slug, repo) is True

        for path in sorted(
            (repo / "products" / "alpha").rglob("*"), reverse=True
        ):
            path.unlink() if path.is_file() else path.rmdir()
        (repo / "products" / "alpha").rmdir()
        assert registry.product_exists(row.product_slug, repo) is False

    async def test_card_visible_distinguishes_hidden_from_absent(
        self, db, repo: Path
    ) -> None:
        """`False`(숨김)와 `None`(카드 없음)은 화면에서 다르게 보여야 한다."""
        await registry.register(
            db,
            repo="kknaks/ax-graph",
            kind="studio",
            product_slug="alpha",
            card=CARD,
            repo_root=repo,
            dry_run=True,
        )
        assert registry.card_visible("alpha", repo) is False
        assert registry.card_visible("no-such-product", repo) is None
