"""TDD — 지식그래프 빌더 + L1~L6 검증 (KDEV-SPEC-002/004, KDEV-WORK-001)."""

from core.graph import (
    build_alias_index,
    build_knowledge_graph,
    summarize,
    validate_graph,
)


def _node(type_="note", title="t", body="", up=None, aliases=None, id_=None,
          archived=False):
    return {
        "id": id_ if id_ is not None else "ID",
        "type": type_,
        "title": title,
        "body": body,
        "up": up,
        "aliases": aliases,
        "archived": archived,
    }


class TestAliasIndex:
    def test_resolves_id_to_stem(self):
        nodes = {
            "spec-001-foo": _node("spec", id_="KDEV-SPEC-001"),
            "work-001-bar": _node("work", id_="KDEV-WORK-001",
                                   body="see [[KDEV-SPEC-001]]"),
        }
        index, collisions = build_alias_index(nodes)
        assert index["KDEV-SPEC-001"] == "spec-001-foo"
        assert index["spec-001-foo"] == "spec-001-foo"  # stem 자기참조
        assert collisions == []

    def test_explicit_aliases(self):
        nodes = {"a": _node(aliases=["A-1", "alpha"])}
        index, _ = build_alias_index(nodes)
        assert index["A-1"] == "a"
        assert index["alpha"] == "a"

    def test_alias_collision_reported(self):
        nodes = {
            "a": _node(aliases=["dup"]),
            "b": _node(aliases=["dup"]),
        }
        _, collisions = build_alias_index(nodes)
        assert any(c["rule"] == "L2" for c in collisions)


class TestKnowledgeGraph:
    def test_edge_assoc_default(self):
        nodes = {"a": _node(body="[[b]]"), "b": _node()}
        g = build_knowledge_graph(nodes)
        edge = next(e for e in g["edges"] if e["source"] == "a")
        assert edge["target"] == "b"
        assert edge["type"] == "assoc"
        assert edge["dir"] is None

    def test_up_marks_lineage(self):
        # up 타겟은 lineage + dir up (KDEV-SPEC-002 §4)
        nodes = {
            "post-1": _node("post", body="based on [[spec-1]]", up=["spec-1"]),
            "spec-1": _node("spec"),
        }
        g = build_knowledge_graph(nodes)
        edge = next(e for e in g["edges"] if e["source"] == "post-1")
        assert edge["type"] == "lineage"
        assert edge["dir"] == "up"

    def test_id_link_resolves_to_stem(self):
        nodes = {
            "spec-1": _node("spec", id_="KDEV-SPEC-001"),
            "w": _node("work", body="[[KDEV-SPEC-001]]"),
        }
        g = build_knowledge_graph(nodes)
        assert any(e["target"] == "spec-1" for e in g["edges"])

    def test_folder_and_alias_forms_resolve(self):
        nodes = {
            "spec-2": _node("spec"),
            "w": _node("work", body="[[20-spec/spec-2]] and [[spec-2|SPEC]]"),
        }
        g = build_knowledge_graph(nodes)
        targets = {e["target"] for e in g["edges"] if e["source"] == "w"}
        assert targets == {"spec-2"}

    def test_backlinks(self):
        nodes = {"a": _node(body="[[c]]"), "b": _node(body="[[c]]"), "c": _node()}
        g = build_knowledge_graph(nodes)
        assert g["backlinks"]["c"] == ["a", "b"]

    def test_dead_target_not_in_edges(self):
        nodes = {"a": _node(body="[[ghost]]")}
        g = build_knowledge_graph(nodes)
        assert g["edges"] == []


class TestValidateL1toL6:
    def test_l1_dead_link(self):
        nodes = {"a": _node(body="[[ghost]]")}
        v = validate_graph(nodes)
        assert any(x["rule"] == "L1" and "ghost" in x["detail"] for x in v)

    def test_l2_missing_type(self):
        nodes = {"a": {"id": "X", "type": None, "body": "[[a]]"}}
        v = validate_graph(nodes)
        assert any(x["rule"] == "L2" and "type" in x["detail"] for x in v)

    def test_l2_duplicate_stem_from_loader(self):
        nodes = {"a": _node(body="[[a]]")}
        dups = [{"rule": "L2", "level": "ERROR", "node": "a", "detail": "중복"}]
        v = validate_graph(nodes, duplicate_stems=dups)
        assert any(x["rule"] == "L2" and "중복" in x["detail"] for x in v)

    def test_l3_overlay_up_not_in_body(self):
        # up 에 있지만 본문 [[]] 에 없음 → L3
        nodes = {
            "p": _node("post", body="no links", up=["spec-1"]),
            "spec-1": _node("spec", body="[[p]]"),
        }
        v = validate_graph(nodes)
        assert any(x["rule"] == "L3" and x["node"] == "p" for x in v)

    def test_l4_idea_up_forbidden(self):
        nodes = {
            "i": _node("idea", body="[[spec-1]]", up=["spec-1"]),
            "spec-1": _node("spec", body="[[i]]"),
        }
        v = validate_graph(nodes)
        assert any(x["rule"] == "L4" for x in v)

    def test_l4_downstream_up_forbidden(self):
        # spec(상류)이 note(하류)를 up → 방향 위반
        nodes = {
            "spec-1": _node("spec", body="[[note-1]]", up=["note-1"]),
            "note-1": _node("note", body="[[spec-1]]"),
        }
        v = validate_graph(nodes)
        assert any(x["rule"] == "L4" for x in v)

    def test_l5_orphan(self):
        # KDEV-WORK-002 Phase 3 — orphan 검사는 지식 노드(reference 등)만 대상
        nodes = {
            "lonely": _node("reference", body="no links"),
            "a": _node("reference", body="[[a]]"),
        }
        v = validate_graph(nodes)
        assert any(x["rule"] == "L5" and x["node"] == "lonely" for x in v)

    def test_l5_skips_non_knowledge_node(self):
        # daily/note 등 비지식 노드는 엣지 0이어도 orphan 아님
        nodes = {"daily-1": _node("daily", body="no links")}
        v = validate_graph(nodes)
        assert not any(x["rule"] == "L5" for x in v)

    def test_l6_archive_reference(self):
        nodes = {
            "live": _node("post", body="[[old]]", up=["old"]),
            "old": _node("spec", archived=True),
        }
        v = validate_graph(nodes)
        assert any(x["rule"] == "L6" and x["node"] == "live" for x in v)

    def test_report_only_never_raises(self):
        # 깨진 입력에도 raise 안 함 (report-only 계약)
        nodes = {"x": {"body": None, "type": "??", "id": None}}
        v = validate_graph(nodes)
        assert isinstance(v, list)

    def test_summarize_counts(self):
        v = [
            {"rule": "L1", "level": "ERROR", "node": "a", "detail": ""},
            {"rule": "L5", "level": "WARN", "node": "b", "detail": ""},
        ]
        s = summarize(v)
        assert s["L1"] == 1 and s["ERROR"] == 1 and s["WARN"] == 1
