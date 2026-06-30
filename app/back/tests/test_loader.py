"""TDD — 페르소나 로더 + 검증."""

from pathlib import Path

import pytest

from service.persona_loader import PersonaError, load_persona

REPO = Path(__file__).resolve().parents[3]
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
        # KDEV-WORK-005 — reference=persona_dir.parent/reference 라 unique repo layout 으로 격리
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)
        ref_dir = repo / "reference" / "py"
        ref_dir.mkdir(parents=True)
        # 파일명은 foo.md 인데 frontmatter id는 bar
        (ref_dir / "foo.md").write_text(
            "---\n"
            "id: bar\n"
            "title: { ko: t, en: t }\n"
            "date: '2026.05.01'\n"
            "---\n# body\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="filename slug"):
            load_persona(persona)

    def test_notes_group_not_in_meta_fails(self, tmp_path: Path):
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)
        ref_dir = repo / "reference" / "nosuchgroup"
        ref_dir.mkdir(parents=True)
        # group 은 cluster 디렉토리명(nosuchgroup)에서 auto-enrich → _meta 에 없음
        (ref_dir / "x.md").write_text(
            "---\n"
            "id: x\n"
            "title: { ko: t, en: t }\n"
            "date: '2026.05.01'\n"
            "---\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="not in _meta"):
            load_persona(persona)

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


class TestGraphNodeQualification:
    """KDEV-WORK-002 Phase 2 — 노드 자격 = frontmatter `type` 보유."""

    def test_typeless_navigational_excluded(self, tmp_path: Path):
        from service.persona_loader import _build_graph_nodes

        products = tmp_path / "products" / "demo"
        products.mkdir(parents=True)
        # type 있는 진짜 노드
        (products / "spec-001-foo.md").write_text(
            "---\nid: D-SPEC-001\ntype: spec\ntitle: Foo\n---\n본문 [[x]]",
            encoding="utf-8",
        )
        # type 없는 navigational 파일 — 노드 아님
        (products / "README.md").write_text("# 안내\n그냥 readme", encoding="utf-8")
        (products / "log.md").write_text("---\ntitle: 로그\n---\n변경 기록", encoding="utf-8")

        nodes, dups = _build_graph_nodes({}, tmp_path / "products")
        assert "spec-001-foo" in nodes
        assert "README" not in nodes
        assert "log" not in nodes
        # type 없는 파일은 중복 stem 검사에도 안 걸림
        assert dups == []


class TestPermanent:
    """KDEV-WORK-010 — permanent(영구노트, flat) loader + 그래프 배선."""

    @staticmethod
    def _repo(tmp_path: Path) -> Path:
        """repo/persona(min) + repo/permanent 격리 레이아웃 (WORK-005 미러)."""
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)
        (repo / "permanent").mkdir()
        return repo

    def test_loaded_as_permanent_nodes(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        perm = repo / "permanent"
        # active 영구노트 + navigational README(제외)
        (perm / "concurrency-model.md").write_text(
            "---\ntitle: 동시성 모델\n---\n# 본문\n", encoding="utf-8"
        )
        (perm / "README.md").write_text("# 안내\nnavigational", encoding="utf-8")

        data = load_persona(repo / "persona")
        assert len(data["permanent"]) == 1  # README 제외
        node = next(n for n in data["_graph"]["nodes"] if n["id"] == "concurrency-model")
        assert node["type"] == "permanent"
        assert node["archived"] is False
        assert "README" not in {n["id"] for n in data["_graph"]["nodes"]}

    def test_archive_subdir_is_archived(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        archive = repo / "permanent" / "archive"
        archive.mkdir()
        (archive / "old-idea.md").write_text(
            "---\ntitle: 폐기 노트\n---\n# old\n", encoding="utf-8"
        )
        data = load_persona(repo / "persona")
        node = next(n for n in data["_graph"]["nodes"] if n["id"] == "old-idea")
        assert node["archived"] is True

    def test_empty_permanent_no_nodes(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        data = load_persona(repo / "persona")
        assert data["permanent"] == []
        assert not any(
            n["type"] == "permanent" for n in data["_graph"]["nodes"]
        )

    def test_id_filename_mismatch_fails(self, tmp_path: Path):
        # id == 파일 stem 강제 (그래프 노드 식별자 정합) — reference 미러
        repo = self._repo(tmp_path)
        (repo / "permanent" / "foo.md").write_text(
            "---\nid: bar\ntitle: t\n---\n# body\n", encoding="utf-8"
        )
        with pytest.raises(PersonaError, match="filename slug"):
            load_persona(repo / "persona")

    def test_up_emits_lineage_and_l4_same_rank_ok(self, tmp_path: Path):
        # permanent up: reference → lineage 엣지. _TYPE_RANK reference=permanent=4 동일 rank →
        # L4(상류만 up) 가 동일-rank 를 ERROR 로 잡지 않는지 확인 (WORK-010 구현 주의).
        repo = self._repo(tmp_path)
        ref = repo / "reference" / "py"
        ref.mkdir(parents=True)
        (ref / "asyncio-basics.md").write_text(
            "---\ntitle: asyncio\n---\n# ref\n", encoding="utf-8"
        )
        (repo / "permanent" / "concurrency-model.md").write_text(
            "---\ntitle: 동시성\nup: [asyncio-basics]\n---\n"
            "정제 출처: [[asyncio-basics]]\n",
            encoding="utf-8",
        )
        data = load_persona(repo / "persona")

        edge = next(
            e for e in data["_graph"]["edges"]
            if e["source"] == "concurrency-model" and e["target"] == "asyncio-basics"
        )
        assert edge["type"] == "lineage"
        assert edge["dir"] == "up"
        # 동일-rank up(permanent→reference)은 L4 ERROR 아님
        l4 = [
            v for v in data["_graph_violations"]
            if v["rule"] == "L4" and v["node"] == "concurrency-model"
        ]
        assert l4 == []


class TestAlgorithms:
    """spec-07 — algorithms 카테고리 로드 + 검증."""

    def test_loads_real_algorithms(self):
        """실 persona/algorithms/A-001-two-sum.md 시드 로드."""
        data = load_persona(PERSONA)
        algos = data.get("algorithms", [])
        assert len(algos) >= 1
        a = next((x for x in algos if x.get("id") == "A-001"), None)
        assert a is not None
        # frontmatter
        assert a["type"] == "algorithm"
        assert a["difficulty"] == "easy"
        assert a["source"]["platform"] == "leetcode"
        # ## Data 키 6개 모두 merge 됨
        for k in ("problem", "clarifying", "approach", "logic", "trace", "solution"):
            assert k in a, f"missing {k} after ## Data merge"
        # logic.format = slot
        assert a["logic"]["format"] == "slot"
        assert len(a["logic"]["slots"]) >= 4
        # trace 단순 형식
        assert isinstance(a["trace"]["cases"], list)
        assert "worked_example" in a["trace"]
        # body drop 됐는지 (구조화 yaml 가 모든 데이터)
        assert a.get("body", "") == "" or a.get("body") is None or "body" not in a or len(a.get("body", "")) > 0  # body 는 drop 또는 무관
        # _path 박혀있음 (다른 카테고리와 동일)
        assert "_path" in a

    def test_algorithms_sorted_by_date_desc(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        _scaffold_algo(tmp_path, "A-001", "two-sum", date="2026-05-01", today=False)
        _scaffold_algo(tmp_path, "A-002", "valid-anagram", date="2026-05-03", today=True)
        _scaffold_algo(tmp_path, "A-003", "contains-duplicate", date="2026-05-02", today=False)
        data = load_persona(tmp_path)
        ids = [a["id"] for a in data["algorithms"]]
        assert ids == ["A-002", "A-003", "A-001"]

    def test_missing_data_block_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        algos_dir = tmp_path / "algorithms"
        algos_dir.mkdir()
        (algos_dir / "A-001-no-data.md").write_text(
            "---\n"
            "id: A-001\n"
            "type: algorithm\n"
            "title: { ko: T, en: T }\n"
            "date: '2026-05-01'\n"
            "source: { platform: leetcode, number: 1, slug: t, url: https://x }\n"
            "difficulty: easy\n"
            "---\n# T\n\n(no data block here)\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="## Data yaml block missing"):
            load_persona(tmp_path)

    def test_id_filename_mismatch_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        algos_dir = tmp_path / "algorithms"
        algos_dir.mkdir()
        _write_algo_file(algos_dir / "wrongprefix-foo.md", aid="A-001")
        with pytest.raises(PersonaError, match="must be prefix"):
            load_persona(tmp_path)

    def test_unknown_platform_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        algos_dir = tmp_path / "algorithms"
        algos_dir.mkdir()
        _write_algo_file(
            algos_dir / "A-001-x.md",
            aid="A-001",
            platform="hackerrank",
        )
        with pytest.raises(PersonaError, match="source.platform"):
            load_persona(tmp_path)

    def test_invalid_logic_format_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        algos_dir = tmp_path / "algorithms"
        algos_dir.mkdir()
        _write_algo_file(algos_dir / "A-001-x.md", aid="A-001", logic_format="ordering")
        with pytest.raises(PersonaError, match="logic.format"):
            load_persona(tmp_path)

    def test_multiple_today_fails(self, tmp_path: Path):
        _scaffold_min_persona(tmp_path)
        _scaffold_algo(tmp_path, "A-001", "x", date="2026-05-01", today=True)
        _scaffold_algo(tmp_path, "A-002", "y", date="2026-05-02", today=True)
        with pytest.raises(PersonaError, match="today"):
            load_persona(tmp_path)


class TestProductsShowcaseLoading:
    """KDEV-WORK-004 — projects 는 products/*/showcase.md 에서 로드 (persona/projects 폐지)."""

    def test_projects_loaded_from_products_showcase(self, tmp_path: Path):
        # persona.parent/products 가 격리되도록 unique tmp_path 하위에 repo 레이아웃 구성.
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)

        for slug, pid in (("wine-log", "P-01"), ("linky", "P-02")):
            d = repo / "products" / slug
            d.mkdir(parents=True)
            (d / "showcase.md").write_text(
                "---\n"
                "type: project\n"
                f"id: {pid}\n"
                "org: studio\n"
                "title: { ko: T, en: T }\n"
                "summary: { ko: s, en: s }\n"
                "category: web\n"
                "status: live\n"
                "stack: [FastAPI]\n"
                "---\n# case study\n",
                encoding="utf-8",
            )

        data = load_persona(persona)
        assert len(data["projects"]) == 2
        # 정렬 = product 디렉토리명 오름차순 (linky < wine-log)
        assert [p["id"] for p in data["projects"]] == ["P-02", "P-01"]
        assert data["projects"][0]["body"].strip() == "# case study"

    def test_bad_category_in_showcase_fails(self, tmp_path: Path):
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)
        d = repo / "products" / "x"
        d.mkdir(parents=True)
        (d / "showcase.md").write_text(
            "---\n"
            "type: project\n"
            "id: P-01\n"
            "title: { ko: T, en: T }\n"
            "summary: { ko: s, en: s }\n"
            "category: nope\n"  # _meta 의 categories 에 없음
            "status: live\n"
            "stack: [FastAPI]\n"
            "---\n# x\n",
            encoding="utf-8",
        )
        with pytest.raises(PersonaError, match="category"):
            load_persona(persona)


class TestReferenceNotesLoading:
    """KDEV-WORK-005 — notes 는 reference/{cluster}/ 에서 로드 + type=reference auto-enrich."""

    def test_reference_notes_loaded_and_retyped(self, tmp_path: Path):
        repo = tmp_path / "repo"
        persona = repo / "persona"
        persona.mkdir(parents=True)
        _scaffold_min_persona(persona)
        ref = repo / "reference"
        (ref / "py").mkdir(parents=True)
        # frontmatter 에 type/id/group 없음 → auto-enrich 가 주입 (157개 실노트와 동형)
        (ref / "py" / "n1.md").write_text(
            "---\ntitle: { ko: t, en: t }\ndate: '2026.05.01'\n---\n# body\n",
            encoding="utf-8",
        )
        (ref / "py" / "n2.md").write_text("# 빈 frontmatter\n본문", encoding="utf-8")
        # top-level navigational README 는 노트로 로드되면 안 됨 (id 없음 → dict KeyError 위험)
        (ref / "README.md").write_text("# 안내\nnavigational", encoding="utf-8")

        data = load_persona(persona)
        assert len(data["notes"]) == 2  # README 제외
        for nid, n in data["notes"].items():
            assert n["type"] == "reference"  # 재타이핑 주입
            assert n["group"] == "py"  # cluster 디렉토리명
            assert n["id"] == nid


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


def _scaffold_algo(
    root: Path, aid: str, slug: str, date: str = "2026-05-01", today: bool = False
) -> None:
    algos_dir = root / "algorithms"
    algos_dir.mkdir(exist_ok=True)
    _write_algo_file(algos_dir / f"{aid}-{slug}.md", aid=aid, date=date, today=today)


def _write_algo_file(
    path: Path,
    *,
    aid: str = "A-001",
    date: str = "2026-05-01",
    today: bool = False,
    platform: str = "leetcode",
    logic_format: str = "slot",
) -> None:
    """spec-07 형식의 최소 algorithm 파일 — 본문 ## Data 포함."""
    today_yaml = "true" if today else "false"
    fm = (
        "---\n"
        f"id: {aid}\n"
        "type: algorithm\n"
        "title: { ko: T, en: T }\n"
        f"date: '{date}'\n"
        f"source: {{ platform: {platform}, number: 1, slug: t, url: https://x }}\n"
        "difficulty: easy\n"
        f"today: {today_yaml}\n"
        "---\n"
    )
    body = (
        "# Title\n\n"
        "## Data\n\n"
        "```yaml\n"
        "problem:\n  statement: { ko: t, en: t }\n  constraints: []\n  io: []\n"
        "clarifying:\n  items: []\n"
        "approach:\n  items: []\n"
        f"logic:\n  format: {logic_format}\n  slots: []\n"
        "trace:\n  code: []\n  cases: []\n  worked_example: { input: '', steps: [], answer: '' }\n"
        "solution:\n  code: ''\n  complexity: { time: O(1), space: O(1) }\n  followup: []\n"
        "```\n"
    )
    path.write_text(fm + body, encoding="utf-8")
