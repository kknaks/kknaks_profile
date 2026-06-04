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

    def test_ignores_non_kebab(self):
        # 위키링크는 영문 소문자 + 하이픈만 (spec-01 §2.4)
        assert extract_wikilinks("[[Foo Bar]] and [[ok-id]]") == ["ok-id"]

    def test_empty_body(self):
        assert extract_wikilinks("") == []
        assert extract_wikilinks(None) == []


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
