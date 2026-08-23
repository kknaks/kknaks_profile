"""지식 4층 모델 — layer 도출 · rank 방향 · 층별 orphan · type별 필수필드.

KDEV-DEC-010 / KDEV-SPEC-002 v0.0.3 / KDEV-SPEC-004 v0.0.5 / KDEV-WORK-013.

**핵심 함정**: rank 테이블만 갈아끼우고 비교 연산자를 그대로 두면 L4 가 조용히 반대로
동작한다. 종전은 `reference=4`(최상류) + `타겟 rank >= 자기 rank`, 신규는 `reference=1`
+ `<=` 다. 아래 `TestLayerDirection` 이 양방향을 모두 고정한다.
"""

from __future__ import annotations

from core.graph import (
    build_knowledge_graph,
    layer_of,
    unsourced_queue,
    validate_graph,
)


def _node(type_, *, body="", up=None, aliases=None, archived=False):
    return {
        "type": type_,
        "title": "t",
        "body": body,
        "up": up,
        "aliases": aliases,
        "archived": archived,
    }


def _graph(mapping):
    """stem→node 에 `id` 를 stem 으로 채워 넣는다.

    모든 노드에 같은 id 를 주면 alias 인덱스가 충돌해 L2 ERROR 가 섞인다 —
    층 규칙을 보려는 테스트에서 그 노이즈를 없앤다.
    """
    return {stem: {**node, "id": stem} for stem, node in mapping.items()}


def _check(mapping, rule=None):
    """신규 4층 규칙 산출만 골라낸다 (detail 이 `[layer]` 로 시작)."""
    violations = validate_graph(_graph(mapping))
    return [
        v for v in violations
        if v["detail"].startswith("[layer]") and (rule is None or v["rule"] == rule)
    ]


class TestLayerDerivation:
    def test_three_layers_map_from_type(self):
        assert layer_of("reference") == "source"
        assert layer_of("concept") == "concept"
        # KDEV-DEC-019 — 판단층 폐기. `permanent` 는 더 이상 층에 속하지 않는다.
        assert layer_of("permanent") is None
        for t in ("baseline", "decision", "spec", "work", "release", "runbook", "bugfix"):
            assert layer_of(t) == "execution", t

    def test_idea_is_node_without_layer(self):
        """idea 는 그래프 노드이지만 층에 속하지 않는다 (KDEV-DEC-010 D3)."""
        assert layer_of("idea") is None

    def test_graph_off_types_have_no_layer(self):
        for t in ("content", "algorithm", "daily", "career", "profile", None):
            assert layer_of(t) is None, t

    def test_graph_json_carries_layer(self):
        """frontmatter 에는 없고 빌더가 계산해 담는다 (KDEV-SPEC-002 v0.0.3)."""
        g = build_knowledge_graph(_graph({
            "stt": _node("concept"),
            "note-a": _node("reference"),
            "raw": _node("idea"),
        }))
        by_id = {n["id"]: n for n in g["nodes"]}
        assert by_id["stt"]["layer"] == "concept"
        assert by_id["note-a"]["layer"] == "source"
        assert by_id["raw"]["layer"] is None


class TestLayerDirection:
    """`up:` 은 상류(같거나 낮은 층)만 가리킨다."""

    def test_concept_may_reference_its_source(self):
        assert _check({
            "whisper": _node("reference"),
            "stt": _node("concept", body="[[whisper]]", up=["whisper"], aliases=["ASR"]),
        }, "L4") == []

    def test_synthesis_may_reference_concept(self):
        assert _check({
            "whisper": _node("reference"),
            "stt": _node("concept", aliases=["ASR"], up=["whisper"], body="[[whisper]]"),
            "strategy": _node("permanent", body="[[stt]]", up=["stt"]),
        }, "L4") == []

    def test_execution_may_reference_concept(self):
        assert _check({
            "whisper": _node("reference"),
            "stt": _node("concept", aliases=["ASR"], up=["whisper"], body="[[whisper]]"),
            "baseline-001-x": _node("baseline", body="[[stt]]", up=["stt"]),
        }, "L4") == []

    def test_source_may_not_reference_concept(self):
        """자료가 개념을 기반으로 할 수는 없다 — 방향이 거꾸로다."""
        found = _check({
            "stt": _node("concept", aliases=["ASR"]),
            "whisper": _node("reference", body="[[stt]]", up=["stt"]),
        }, "L4")
        assert len(found) == 1
        assert found[0]["node"] == "whisper"

    def test_concept_may_not_reference_execution(self):
        """개념이 제품 문서를 기반으로 삼을 수는 없다 — 방향이 거꾸로다."""
        found = _check({
            "baseline-001-x": _node("baseline"),
            "stt": _node("concept", body="[[baseline-001-x]]", up=["baseline-001-x"]),
        }, "L4")
        assert len(found) == 1
        assert found[0]["node"] == "stt"

    def test_same_layer_is_allowed(self):
        assert _check({
            "spec-001-a": _node("spec"),
            "work-001-b": _node("work", body="[[spec-001-a]]", up=["spec-001-a"]),
        }, "L4") == []

    def test_layerless_node_cannot_be_upstream(self):
        """층이 없는 노드는 상류가 될 수 없다 — `idea`(휘발)가 대표 사례.

        이 검사가 없으면 층 기반 비교가 `None` 타겟을 그냥 건너뛰어,
        "idea 는 상류가 될 수 없다"(KDEV-DEC-010 D3)가 아무도 안 지키게 된다.
        """
        found = _check({
            "raw": _node("idea"),
            "stt": _node("concept", aliases=["ASR"], body="[[raw]]", up=["raw"]),
        }, "L4")
        assert len(found) == 1
        assert found[0]["node"] == "stt"

    def test_idea_may_not_up_anything(self):
        """반대 방향 — idea 자신도 up 을 가질 수 없다 (기존 ERROR 가드 유지)."""
        v = validate_graph(_graph({
            "whisper": _node("reference"),
            "raw": _node("idea", body="[[whisper]]", up=["whisper"]),
        }))
        found = [x for x in v if x["rule"] == "L4" and x["node"] == "raw"]
        assert found and found[0]["level"] == "ERROR"


class TestRequiredFields:
    def test_concept_requires_aliases_and_up(self):
        found = _check({"stt": _node("concept")}, "L2")
        missing = {f for f in ("aliases", "up") if any(f"'{f}' 필수" in v["detail"] for v in found)}
        assert missing == {"aliases", "up"}

    def test_concept_with_both_passes(self):
        assert _check({
            "whisper": _node("reference"),
            "stt": _node("concept", aliases=["ASR"], up=["whisper"], body="[[whisper]]"),
        }, "L2") == []

    def test_concept_requires_up(self):
        found = _check({"stt": _node("concept", aliases=["STT"])}, "L2")
        assert any("'up' 필수" in v["detail"] for v in found)

    def test_reference_needs_neither(self):
        assert _check({"whisper": _node("reference")}, "L2") == []

    def test_deprecated_type_is_reported(self):
        found = _check({"n": _node("note")}, "L2")
        assert any("폐기 예정 type" in v["detail"] for v in found)


class TestLayeredOrphan:
    def test_source_orphan_is_queue_not_violation(self):
        """157건이 상시 WARN 이던 것을 '정제 작업 큐' 지표로 뒤집는다 (KDEV-DEC-010 D5)."""
        v = validate_graph(_graph({"whisper": _node("reference")}))
        orphans = [x for x in v if x["rule"] == "L5"]
        assert len(orphans) == 1
        assert orphans[0]["level"] == "INFO"
        assert unsourced_queue(v) == ["whisper"]

    def test_layerless_type_orphan_is_not_checked(self):
        """KDEV-DEC-019 — `permanent` 는 층이 없어져 orphan 판정 대상이 아니다."""
        v = validate_graph(_graph({"strategy": _node("permanent", up=["x"])}))
        assert [x for x in v if x["rule"] == "L5"] == []

    def test_execution_orphan_is_not_checked(self):
        """제품 문서는 제품 파이프라인이 관리한다."""
        v = validate_graph(_graph({"spec-001-a": _node("spec")}))
        assert [x for x in v if x["rule"] == "L5"] == []

    def test_idea_orphan_is_not_checked(self):
        v = validate_graph(_graph({"raw": _node("idea")}))
        assert [x for x in v if x["rule"] == "L5"] == []

    def test_connected_source_leaves_queue(self):
        v = validate_graph(_graph({
            "whisper": _node("reference"),
            "stt": _node("concept", aliases=["ASR"], up=["whisper"], body="[[whisper]]"),
        }))
        assert unsourced_queue(v) == []


class TestEnforcement:
    """Phase 5 — 실데이터 위반 0 을 확인한 뒤 기본 enforce 로 전환했다."""

    def _broken(self):
        return _graph({
            "stt": _node("concept"),                                    # aliases·up 누락
            "whisper": _node("reference", body="[[stt]]", up=["stt"]),  # 방향 위반
            "n": _node("note"),                                         # 폐기 type
        })

    def test_layer_rules_block_by_default(self):
        v = validate_graph(self._broken())
        assert [x for x in v if x["level"] == "ERROR"]

    def test_kill_switch_downgrades_to_warn(self, monkeypatch):
        """부팅이 막히면 `GRAPH_LAYER_ENFORCE=0` 으로 즉시 풀 수 있어야 한다."""
        monkeypatch.setenv("GRAPH_LAYER_ENFORCE", "0")
        v = validate_graph(self._broken())
        assert [x for x in v if x["level"] == "ERROR"] == []
        assert [x for x in v if x["detail"].startswith("[layer]")]  # 보고는 계속 된다

    def test_source_orphan_never_blocks(self):
        """미소화 큐는 enforce 여부와 무관하게 차단 대상이 아니다."""
        v = validate_graph(_graph({"whisper": _node("reference")}))
        assert [x for x in v if x["level"] == "ERROR"] == []
