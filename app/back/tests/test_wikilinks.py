"""TDD — 위키링크 파싱 + 그래프/백링크 빌더 검증."""

from core.wikilinks import build_graph, dead_links, extract_wikilinks


class TestExtractWikilinks:
    def test_finds_single_link(self):
        assert extract_wikilinks("see [[python-asyncio]] for context") == ["python-asyncio"]

    def test_finds_multiple_links(self):
        body = "[[a]] and [[b]] and [[c]]"
        assert extract_wikilinks(body) == ["a", "b", "c"]

    def test_preserves_duplicates(self):
        # 같은 id 두 번 등장 시 두 번 반환 (등장 순서 의미 있음)
        assert extract_wikilinks("[[x]] [[y]] [[x]]") == ["x", "y", "x"]

    def test_allows_uppercase_id_form(self):
        # KDEV-SPEC-002 §4 — 대문자 id-style stem 허용 ([[KDEV-SPEC-001]])
        assert extract_wikilinks("see [[KDEV-SPEC-001]] and [[ok-id]]") == [
            "KDEV-SPEC-001",
            "ok-id",
        ]

    def test_ignores_prose_with_space(self):
        # 공백 포함은 stem 규약 위반 → 산문 오탐 방지로 무시
        assert extract_wikilinks("[[Foo Bar]] and [[ok-id]]") == ["ok-id"]

    def test_parses_alias_form(self):
        # [[stem|alias]] — alias 표시는 버리고 stem
        assert extract_wikilinks("[[decision-001-foo|KDEV-DEC-001]]") == [
            "decision-001-foo"
        ]

    def test_parses_folder_form(self):
        # [[folder/stem]] — 마지막 경로 세그먼트가 stem
        assert extract_wikilinks("[[20-spec/spec-002-graph-schema]]") == [
            "spec-002-graph-schema"
        ]

    def test_parses_underscore_stem(self):
        # 아카이브 버전 prefix stem (v1_0_1-work-005) 허용
        assert extract_wikilinks("[[v1_0_1-work-005-websocket-server]]") == [
            "v1_0_1-work-005-websocket-server"
        ]

    def test_empty_body(self):
        assert extract_wikilinks("") == []
        assert extract_wikilinks(None) == []

    def test_skips_inline_code(self):
        # KDEV-WORK-002 Phase 1 — 인라인 코드 안의 [[]] 는 문법 설명, 엣지 아님
        body = "문법은 `[[stem]]` 처럼 쓰고 실제로는 [[real-note]] 를 건다"
        assert extract_wikilinks(body) == ["real-note"]

    def test_skips_fenced_code(self):
        # KDEV-WORK-002 Phase 1 — fenced 코드블록 안의 [[]] 제외
        body = "예시:\n```md\n[[example-stem]] 이렇게\n```\n본문 [[real-note]]"
        assert extract_wikilinks(body) == ["real-note"]

    def test_keeps_links_outside_code(self):
        # 코드 밖 링크는 stripping 후에도 그대로 (회귀 방지)
        body = "[[a]] 그리고 `code` 그리고 [[b]]"
        assert extract_wikilinks(body) == ["a", "b"]


class TestBuildGraph:
    def test_extracts_edges(self):
        notes = {
            "a": {"body": "see [[b]] and [[c]]"},
            "b": {"body": "back to [[a]]"},
            "c": {"body": "no links here"},
        }
        edges, _ = build_graph(notes)
        assert {"source": "a", "target": "b"} in edges
        assert {"source": "a", "target": "c"} in edges
        assert {"source": "b", "target": "a"} in edges
        assert len(edges) == 3

    def test_dedupes_edges(self):
        notes = {"a": {"body": "[[b]] and [[b]] again"}}
        edges, _ = build_graph(notes)
        assert edges == [{"source": "a", "target": "b"}]

    def test_builds_backlinks(self):
        notes = {
            "a": {"body": "[[target]]"},
            "b": {"body": "[[target]] also"},
            "target": {"body": "no out-links"},
        }
        _, backlinks = build_graph(notes)
        assert backlinks == {"target": ["a", "b"]}

    def test_sorted_outputs(self):
        # 결정성 — 같은 입력이면 같은 순서
        notes = {
            "z": {"body": "[[a]]"},
            "y": {"body": "[[a]]"},
            "x": {"body": "[[a]]"},
        }
        _, backlinks = build_graph(notes)
        assert backlinks["a"] == ["x", "y", "z"]


class TestDeadLinks:
    def test_finds_targets_not_in_notes(self):
        notes = {
            "a": {"body": "valid [[b]] and dead [[ghost]]"},
            "b": {"body": ""},
        }
        assert dead_links(notes) == [("a", "ghost")]

    def test_no_dead_links(self):
        notes = {
            "a": {"body": "[[b]]"},
            "b": {"body": "[[a]]"},
        }
        assert dead_links(notes) == []
