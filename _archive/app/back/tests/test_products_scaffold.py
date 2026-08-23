"""제품 스캐폴딩과 검증 (KDEV-WORK-018 P3 / KDEV-SPEC-014).

가장 중요한 것은 **`test_two_products_keep_the_graph_valid`** 다. 템플릿을 통째로
복사하면 예시 문서 8개가 그래프 노드가 되고, 제품을 둘 만드는 순간 stem 이 중복돼
백엔드가 부팅되지 않는다. 그 회귀를 여기서 잡는다.
"""

from __future__ import annotations

from pathlib import Path

import frontmatter
import pytest

from service.products import scaffold, validate
from service.products.errors import ProductError
from utils.slug import next_card_id, parse_repo_slug, product_dir


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """템플릿·메타·career 를 갖춘 최소 레포."""
    templates = tmp_path / "templates" / "product"
    for rel in scaffold.SCAFFOLD_FILES:
        target = templates / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# {rel}\n", encoding="utf-8")

    # 복사되면 안 되는 예시 문서 — frontmatter `type` 을 갖는다.
    for rel in ("00-baseline/baseline.md", "10-decision/decision.md", "20-spec/spec.md"):
        target = templates / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "---\ntype: baseline\nid: BASE-001\ntitle: \"\"\n---\n\n# Title\n",
            encoding="utf-8",
        )

    (tmp_path / "products").mkdir()
    (tmp_path / "products" / "README.md").write_text(
        "# Products\n\n| Product | Context |\n|---|---|\n| existing | `products/existing/` |\n",
        encoding="utf-8",
    )
    meta = tmp_path / "persona" / "_meta.yaml"
    meta.parent.mkdir(parents=True, exist_ok=True)
    meta.write_text(
        "projects:\n  categories:\n    - id: web\n    - id: backend\n", encoding="utf-8"
    )
    career = tmp_path / "persona" / "career"
    career.mkdir(parents=True, exist_ok=True)
    (career / "medisolve-ai.md").write_text("---\ntype: career\n---\n", encoding="utf-8")
    return tmp_path


CARD = {
    "title": {"ko": "제품", "en": "Product"},
    "summary": {"ko": "한 줄", "en": "One line"},
    "category": "backend",
    "status": "wip",
    "stack": ["FastAPI"],
}


class TestWhitelist:
    def test_never_copy_and_scaffold_do_not_overlap(self) -> None:
        """목록 둘이 겹치면 하나가 거짓말을 하고 있는 것이다."""
        assert not set(scaffold.SCAFFOLD_FILES) & set(scaffold.NEVER_COPY)

    def test_scaffold_covers_required_stage_readmes(self) -> None:
        """`product_doc_pipeline` 필수 4종 + 제품 README + log 를 덮는다."""
        required = {
            "00-baseline/README.md",
            "10-decision/README.md",
            "20-spec/README.md",
            "30-work/README.md",
            "README.md",
            "log.md",
        }
        assert required == set(scaffold.SCAFFOLD_FILES)

    def test_sample_docs_are_not_copied(self, repo: Path) -> None:
        """**예시 문서가 복사되면 그래프 노드가 된다.**"""
        scaffold.write_scaffold("alpha", repo)
        created = {
            str(p.relative_to(repo / product_dir("alpha")))
            for p in (repo / product_dir("alpha")).rglob("*.md")
        }
        assert created == set(scaffold.SCAFFOLD_FILES)
        assert not any(p.name == "baseline.md" for p in (repo / "products").rglob("*"))

    def test_two_products_keep_the_graph_valid(self, repo: Path) -> None:
        """제품을 둘 만들어도 **같은 stem 을 가진 노드가 생기지 않는다.**

        통째 복사였다면 `baseline`·`decision`·`spec` stem 이 각각 둘이 되어 L2 중복
        ERROR → enforce raise → 백엔드 미부팅이다.
        """
        scaffold.write_scaffold("alpha", repo)
        scaffold.write_scaffold("beta", repo)

        stems: list[str] = []
        for path in (repo / "products").rglob("*.md"):
            meta = frontmatter.load(path).metadata
            if meta.get("type"):
                stems.append(path.stem)
        assert len(stems) == len(set(stems)), f"중복 stem — {stems}"


class TestCardRendering:
    def test_card_id_is_max_plus_one(self) -> None:
        assert next_card_id(["P-02", "P-14", "P-03"]) == "P-15"

    def test_gaps_are_not_reused(self) -> None:
        """지워진 번호를 재사용하면 자산 경로가 과거 이미지를 가리킨다(D6)."""
        assert next_card_id(["P-02", "P-03"]) == "P-04"

    def test_system_owns_type_id_org(self, repo: Path) -> None:
        path, content = scaffold.render_card(slug="alpha", card=CARD, repo_root=repo)
        meta = frontmatter.loads(content).metadata
        assert path == "products/alpha/showcase.md"
        assert meta["type"] == "project" and meta["org"] == "studio"
        assert meta["id"] == "P-01"

    def test_new_cards_are_hidden(self, repo: Path) -> None:
        """본문이 빈 채로 사이트에 올라가지 않게 한다."""
        _, content = scaffold.render_card(slug="alpha", card=CARD, repo_root=repo)
        assert frontmatter.loads(content).metadata["visible"] is False

    def test_pdf_block_is_not_seeded(self, repo: Path) -> None:
        """빈 케이스 스터디를 미리 깔면 "채워야 할 것" 과 구분되지 않는다."""
        _, content = scaffold.render_card(slug="alpha", card=CARD, repo_root=repo)
        meta = frontmatter.loads(content).metadata
        assert not {"problem", "approach", "impact", "learnings", "troubles"} & set(meta)

    def test_body_has_the_three_required_sections(self, repo: Path) -> None:
        _, content = scaffold.render_card(slug="alpha", card=CARD, repo_root=repo)
        body = frontmatter.loads(content).content
        assert "# 개요" in body and "# 기술스택" in body and "# 주요기능" in body


class TestValidation:
    def test_repo_slug_forms(self) -> None:
        assert parse_repo_slug("https://github.com/kknaks/ax-graph.git") == "kknaks/ax-graph"
        assert parse_repo_slug("github.com/kknaks/ax-graph") == "kknaks/ax-graph"
        assert parse_repo_slug("kknaks/ax-graph") == "kknaks/ax-graph"
        assert parse_repo_slug("ax-graph") is None

    def test_invalid_slug_is_refused(self) -> None:
        with pytest.raises(ProductError) as exc:
            validate.normalize_repo_slug("not a repo")
        assert exc.value.code == "INVALID_SLUG"

    def test_duplicate_slug_is_refused(self) -> None:
        with pytest.raises(ProductError) as exc:
            validate.check_slug_available("a/b", {"a/b"})
        assert exc.value.code == "SLUG_TAKEN"

    @pytest.mark.parametrize("bad", ["Mac-Remote", "mac_remote", "-mac", "mac--remote", ""])
    def test_product_slug_shape(self, bad: str) -> None:
        with pytest.raises(ProductError) as exc:
            validate.check_product_slug_shape(bad)
        assert exc.value.code == "INVALID_PRODUCT_SLUG"

    def test_existing_product_dir_is_refused(self, repo: Path) -> None:
        (repo / "products" / "taken").mkdir()
        with pytest.raises(ProductError) as exc:
            validate.check_product_dir_free("taken", repo)
        assert exc.value.code == "PRODUCT_EXISTS"

    def test_company_needs_a_real_career(self, repo: Path) -> None:
        with pytest.raises(ProductError) as missing:
            validate.check_career(None, repo)
        assert missing.value.code == "CAREER_REQUIRED"

        with pytest.raises(ProductError) as typo:
            validate.check_career("medisolve-ia", repo)
        assert typo.value.code == "CAREER_NOT_FOUND"

    def test_category_must_come_from_meta(self, repo: Path) -> None:
        """**허용 목록 밖 값 하나가 persona 로드 전체를 실패시킨다.**"""
        with pytest.raises(ProductError) as exc:
            validate.check_card({**CARD, "category": "mobile"}, repo)
        assert exc.value.code == "CATEGORY_INVALID"

    def test_categories_come_from_the_repo_not_code(self, repo: Path) -> None:
        assert validate.load_categories(repo) == ["web", "backend"]

    @pytest.mark.parametrize("field", ["title", "summary", "category", "stack"])
    def test_missing_card_field_is_refused(self, repo: Path, field: str) -> None:
        card = {k: v for k, v in CARD.items() if k != field}
        with pytest.raises(ProductError) as exc:
            validate.check_card(card, repo)
        assert exc.value.code in ("CARD_FIELD_MISSING", "CATEGORY_INVALID")

    def test_half_translated_title_is_refused(self, repo: Path) -> None:
        with pytest.raises(ProductError) as exc:
            validate.check_card({**CARD, "title": {"ko": "제품", "en": ""}}, repo)
        assert exc.value.field == "title"
