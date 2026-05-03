"""TDD — 페르소나 로더 + 검증."""

from pathlib import Path

import pytest

from service.persona_loader import PersonaError, load_persona

REPO = Path(__file__).resolve().parent.parent.parent
PERSONA = REPO / "persona"


class TestLoadRealPersona:
    """실제 persona/ (M1 시드) 로드 — fail-fast 검증 포함."""

    def test_loads_all_categories(self):
        data = load_persona(PERSONA)
        assert data["profile"] is not None
        assert data["profile"]["handle"] == "kknaks"
        assert len(data["career"]) >= 1
        assert len(data["projects"]) >= 1
        assert len(data["notes"]) >= 1
        assert len(data["contents"]) >= 1
        assert len(data["daily"]) >= 1

    def test_career_sorted_by_display_order(self):
        data = load_persona(PERSONA)
        orders = [c["display_order"] for c in data["career"]]
        assert orders == sorted(orders)

    def test_notes_indexed_by_id(self):
        # 구조 검증 — dict 키 = note id, 값에 group 필드 박혀있음
        data = load_persona(PERSONA)
        assert isinstance(data["notes"], dict)
        assert len(data["notes"]) >= 1
        first_id = next(iter(data["notes"]))
        assert "group" in data["notes"][first_id]

    def test_meta_loaded(self):
        # _meta.yaml 의 notes.clusters 가 list 로 박혀있음
        data = load_persona(PERSONA)
        clusters = data["_meta"]["notes"]["clusters"]
        assert isinstance(clusters, list)
        assert len(clusters) >= 1
        assert all("id" in c and "label" in c for c in clusters)

    def test_wikilinks_graph_built(self):
        # _edges 가 list. 실제 위키링크 존재 여부는 데이터 의존이라 강제 X.
        data = load_persona(PERSONA)
        assert isinstance(data["_edges"], list)
        assert isinstance(data["_backlinks"], dict)


class TestValidationFailures:
    """위반 케이스 — temp 디렉토리에 박은 mini persona."""

    def test_missing_required_field_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        # profile.md에서 email 빼기
        bad = (
            "---\n"
            "type: profile\n"
            "handle: x\n"
            "name: x\n"
            "role: x\n"
            "tagline: { ko: a, en: a }\n"
            "intro: { ko: a, en: a }\n"
            "stack: [a]\n"
            "---\n# body\n"
        )
        (tmp_path / "profile.md").write_text(bad, encoding="utf-8")
        with pytest.raises(PersonaError, match="missing required"):
            load_persona(tmp_path)

    def test_notes_id_filename_mismatch_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir(exist_ok=True)
        # 파일명은 foo.md 인데 frontmatter id는 bar
        (notes_dir / "foo.md").write_text(
            "---\n"
            "type: note\n"
            "id: bar\n"
            "title: { ko: t, en: t }\n"
            "date: '2026.05.01'\n"
            "group: py\n"
            "---\n# body\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="filename slug"):
            load_persona(tmp_path)

    def test_notes_group_not_in_meta_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir(exist_ok=True)
        (notes_dir / "x.md").write_text(
            "---\n"
            "type: note\n"
            "id: x\n"
            "title: { ko: t, en: t }\n"
            "date: '2026.05.01'\n"
            "group: nosuchgroup\n"
            "---\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="not in _meta"):
            load_persona(tmp_path)

    def test_contents_id_filename_mismatch_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        contents_dir = tmp_path / "contents"
        contents_dir.mkdir(exist_ok=True)
        (contents_dir / "wrongprefix-foo.md").write_text(
            "---\n"
            "type: content\n"
            "id: C-001\n"
            "date: '2026.05.01'\n"
            "day: Day 01\n"
            "title: { ko: t, en: t }\n"
            "summary: { ko: s, en: s }\n"
            "youtubeId: abc\n"
            "---\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="must be prefix"):
            load_persona(tmp_path)


def _scaffold_min_persona(root: Path) -> None:
    """검증 가능한 최소 persona — _meta + profile."""
    (root / "_meta.yaml").write_text(
        "projects:\n  categories:\n    - id: web\n      label: { ko: W, en: W }\n      order: 1\n"
        "notes:\n  clusters:\n    - id: py\n      label: { ko: P, en: P }\n      color: '#000'\n      order: 1\n",
        encoding="utf-8",
    )
    (root / "profile.md").write_text(
        "---\n"
        "type: profile\n"
        "handle: x\n"
        "name: x\n"
        "role: x\n"
        "email: a@b\n"
        "tagline: { ko: a, en: a }\n"
        "intro: { ko: a, en: a }\n"
        "stack: [a]\n"
        "---\n# body\n",
        encoding="utf-8",
    )
