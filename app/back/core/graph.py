"""지식그래프 — 노드/층/엣지(type,dir)/백링크 + L1~L6 검증.

KDEV-SPEC-002 §4 (그래프 스키마) · KDEV-SPEC-004 (검증 게이트 L1~L6) 구현.
검증은 위반 리스트를 반환만 하고 **절대 raise 하지 않는다** — 차단 판정은
`persona_loader._enforce_graph` 가 ERROR-level 만 보고 수행한다(KDEV-WORK-007).

KDEV-WORK-013 — 지식을 4층으로 재편했고, KDEV-DEC-019 가 판단층(synthesis)을 걷어내
3층(source → concept → execution)으로 줄였다.
`layer` 는 frontmatter 가 아니라 `type` 에서 도출한다(KDEV-DEC-010 D3).

노드 식별자 = 파일명 stem (spec-002 §4). 노드 dict 기대 키:
    type, title, body, up(list[str]), aliases(list[str]), id, archived(bool).
"""

from __future__ import annotations

import os
from collections import defaultdict
from typing import Any

from core.wikilinks import extract_wikilinks

# spec-002 §4 + spec-001/007 (persona) + products frontmatter type 합집합.
ALLOWED_NODE_TYPES: set[str] = {
    # 지식 4층 (KDEV-DEC-010 D3)
    "reference", "concept",
    "baseline", "decision", "spec", "work", "release", "runbook", "bugfix",
    # 노드이되 층 없음
    "idea",
    # persona (그래프 밖이지만 type 자체는 유효)
    "profile", "career", "content", "daily", "algorithm",
    # 공개 글 (KDEV-DEC-020 D3 — A 의 귀결). 층은 없다 — persona 계열은 그래프 밖이다.
    # `post` 하나였던 것을 둘로 가른다: 자료가 말한 요지(article) / 내가 이해한 것(note).
    "post_article", "post_note",
}

# KDEV-DEC-010 D3 로 폐기 예정인 type. Phase 5 에서 ALLOWED 에서 완전히 뺀다.
# `note` 는 WORK-005 에서 reference 로 전량 재타이핑돼 실사용 0건(2026-07-28 실측),
# `product`/`project` 는 showcase 라 빌더가 이미 그래프에서 제외한다(WORK-004).
DEPRECATED_NODE_TYPES: set[str] = {"note", "product", "project"}

# ── 지식 4층 (KDEV-DEC-010 D1/D3) ──────────────────────────────────────────
# `layer` 는 frontmatter 에 적지 않고 `type` 에서 도출한다 — 같은 사실을 두 곳에 두면
# 언젠가 어긋난다. 빌더가 계산해 `_graph.json` nodes[].layer 에 담는다.
_TYPE_LAYER: dict[str, str] = {
    "reference": "source",
    "concept": "concept",
    "baseline": "execution",
    "decision": "execution",
    "spec": "execution",
    "work": "execution",
    "release": "execution",
    "runbook": "execution",
    "bugfix": "execution",
}

# 층 rank = 지식의 성장 방향(출처 → 개념 → 판단 → 실행).
# `up:` 타겟의 rank 는 자기 rank **이하**여야 한다 — 상류(출처 방향)만 가리킨다.
#
# ⚠ 종전 `_TYPE_RANK`(WORK-013 에서 제거) 와 비교 방향이 반대였다. 그쪽은 "높을수록 상류,
# 타겟 rank >= 자기 rank" 였고 `reference=4`(최상류)였다. 새 모델은 rank 를 파이프라인
# 진행 순서로 쓰므로 `reference=1` 이고 비교가 `<=` 다. 되돌리거나 이식할 일이 있으면
# **테이블과 비교 연산자를 반드시 함께** 본다 (KDEV-SPEC-002 §4).
_LAYER_RANK: dict[str, int] = {
    "source": 1,
    "concept": 2,
    "execution": 4,
}

# L2 type 별 추가 필수 필드 (KDEV-SPEC-004 §4).
# `idea` 의 `up` 금지는 L4 가 담당한다(기존 가드) — 여기서 중복 보고하지 않는다.
_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "concept": ("aliases", "up"),   # aliases=개념 중복 생성 방지 / up=출처 없는 개념은 성립 안 함
}


def layer_of(node_type: str | None) -> str | None:
    """`type` → `layer`. 층에 속하지 않으면 None (idea·persona 계열)."""
    return _TYPE_LAYER.get(node_type) if node_type else None


def layer_rules_enforced() -> bool:
    """4층 규칙(L2 필수필드·L4 방향·L5 concept·폐기 type)을 ERROR 로 차단할지.

    KDEV-WORK-013 Phase 1~4 를 report-only 로 돌려 실데이터 위반이 0 임을 확인한 뒤
    Phase 5 에서 **기본 enforce** 로 전환했다(WORK-001~007 에서 검증된 순서).
    `GRAPH_LAYER_ENFORCE=0` 이 kill-switch — `GRAPH_ENFORCE` 와 같은 패턴이다.
    """
    return os.environ.get("GRAPH_LAYER_ENFORCE", "1") == "1"


def _new_level(target: str) -> str:
    """신규 규칙의 보고 레벨. enforce 전에는 차단하지 않는다."""
    return target if layer_rules_enforced() else "WARN"


def build_alias_index(nodes: dict[str, dict]) -> tuple[dict[str, str], list[dict]]:
    """alias/id → canonical stem 인덱스.

    각 노드 stem 자체 + frontmatter `id` + `aliases` 항목을 stem 으로 매핑.
    같은 키가 서로 다른 stem 두 곳을 가리키면 alias 충돌(L2) 로 보고.
    Returns (index, collisions) — collisions: [{rule, level, node, detail}].
    """
    index: dict[str, str] = {}
    collisions: list[dict] = []

    def _register(key: str, stem: str) -> None:
        if not key:
            return
        prev = index.get(key)
        if prev is not None and prev != stem:
            collisions.append({
                "rule": "L2",
                "level": "ERROR",
                "node": stem,
                "detail": f"alias/id '{key}' 가 '{prev}' 와 '{stem}' 양쪽을 가리킴 (전역 유일 위반)",
            })
            return
        index[key] = stem

    for stem, node in nodes.items():
        _register(stem, stem)  # stem 자체로도 resolve (archived 도 stem 으로는 reachable)
        if node.get("archived"):
            # 동결 스냅샷 — canonical id/alias 는 live 가 소유 (KDEV-SPEC-004 §7 Option 2).
            # archived 사본은 자기 stem(v1_0_1-X)으로만 resolve, MRT-* 를 claim 하지 않음 → live 와 L2 충돌 0.
            continue
        fid = node.get("id")
        if isinstance(fid, str):
            _register(fid, stem)
        for a in _as_list(node.get("aliases")):
            if isinstance(a, str):
                _register(a, stem)
    return index, collisions


def _as_list(v: Any) -> list:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def _resolve(target: str, nodes: dict[str, dict], alias_index: dict[str, str]) -> str | None:
    """링크 stem → 실존 노드 stem (직접 또는 alias). 없으면 None."""
    if target in nodes:
        return target
    return alias_index.get(target)


def build_knowledge_graph(nodes: dict[str, dict]) -> dict[str, Any]:
    """products 포함 노드 dict(stem→node) → _graph.json 형태.

    {
      "nodes":     [{"id": stem, "type", "layer", "title", "archived"}],
      "edges":     [{"source", "target", "type": assoc|lineage, "dir": up|null}],
      "backlinks": {stem: [source_stem, ...]},
    }
    엣지 target 은 실존 노드로 resolve 된 것만 (dead link 는 검증 L1 으로 별도 보고).
    """
    alias_index, _ = build_alias_index(nodes)

    edges_map: dict[tuple[str, str], dict] = {}
    backlinks: dict[str, set[str]] = defaultdict(set)

    for stem, node in sorted(nodes.items()):
        up_targets = {
            r for t in _as_list(node.get("up"))
            if isinstance(t, str) and (r := _resolve(t, nodes, alias_index))
        }
        for raw in extract_wikilinks(node.get("body", "")):
            target = _resolve(raw, nodes, alias_index)
            if target is None or target == stem:
                continue
            is_lineage = target in up_targets
            key = (stem, target)
            # lineage 가 assoc 보다 우선 (같은 엣지면 승격)
            if key not in edges_map or is_lineage:
                edges_map[key] = {
                    "source": stem,
                    "target": target,
                    "type": "lineage" if is_lineage else "assoc",
                    "dir": "up" if is_lineage else None,
                }
            backlinks[target].add(stem)

    node_list = [
        {
            "id": stem,
            "type": node.get("type"),
            # KDEV-SPEC-002 v0.0.3 — frontmatter 에는 없고 빌더가 type 에서 계산해 담는다.
            # 소비자(열람 표면의 층 필터, 검증기)가 매번 매핑을 다시 구현하지 않게 하기 위함.
            "layer": layer_of(node.get("type")),
            "title": _title(node),
            "archived": bool(node.get("archived", False)),
        }
        for stem, node in sorted(nodes.items())
    ]
    edges = [edges_map[k] for k in sorted(edges_map)]
    backlinks_sorted = {k: sorted(v) for k, v in sorted(backlinks.items())}
    return {"nodes": node_list, "edges": edges, "backlinks": backlinks_sorted}


def _title(node: dict) -> str:
    t = node.get("title")
    if isinstance(t, dict):  # i18n {ko,en}
        return t.get("ko") or t.get("en") or ""
    return str(t) if t else ""


def validate_graph(
    nodes: dict[str, dict],
    duplicate_stems: list[dict] | None = None,
) -> list[dict]:
    """L1~L6 검증 → 위반 리스트 [{rule, level, node, detail}]. **절대 raise 안 함.**

    L1 dead link        ERROR  본문 `[[]]`·`up:` 타겟 미실존
    L2 노드 스키마/유일  ERROR  id/type 필수, type 허용값, stem/alias 전역 유일
    L3 오버레이 정합     ERROR  `up:` stem 이 본문 `[[]]` 에도 존재
    L4 방향 정합         ERROR  up 타겟이 상류(같거나 낮은 층), idea up 금지
    L5 orphan            층별   source=INFO(미소화 큐) / concept=ERROR
    L6 archive 참조      WARN   활성 노트가 archived 를 up 의존

    **신규 4층 규칙(L2 필수필드·L4 방향·L5 concept·폐기 type)은 `GRAPH_LAYER_ENFORCE=1`
    이전까지 WARN 으로만 보고한다** — 데이터가 green 이 된 뒤 켠다(KDEV-WORK-013).
    detail 이 `[layer]` 로 시작하는 항목이 신규 규칙 산출이다.
    """
    violations: list[dict] = []
    alias_index, alias_collisions = build_alias_index(nodes)

    # L2 — 중복 stem (로더가 수집) + alias/id 충돌
    if duplicate_stems:
        violations.extend(duplicate_stems)
    violations.extend(alias_collisions)

    # 연결 차수 (L5 orphan 판정) — resolve 된 엣지만 카운트
    degree: dict[str, int] = defaultdict(int)

    for stem, node in sorted(nodes.items()):
        node_type = node.get("type")
        body_targets = set(extract_wikilinks(node.get("body", "")))
        up_list = [t for t in _as_list(node.get("up")) if isinstance(t, str)]

        # L2 — 필수 필드 / type enum
        if not node.get("id"):
            violations.append(_v("L2", "ERROR", stem, "frontmatter 'id' 누락"))
        if not node_type:
            violations.append(_v("L2", "ERROR", stem, "frontmatter 'type' 누락"))
        elif node_type in DEPRECATED_NODE_TYPES:
            violations.append(_v(
                "L2", _new_level("ERROR"), stem,
                f"[layer] 폐기 예정 type '{node_type}' (KDEV-DEC-010 D3)",
            ))
        elif node_type not in ALLOWED_NODE_TYPES:
            violations.append(_v("L2", "ERROR", stem, f"미등록 type '{node_type}'"))

        # L2 — type 별 추가 필수 필드 (KDEV-SPEC-004 §4)
        for field in _REQUIRED_FIELDS.get(node_type or "", ()):
            if not _as_list(node.get(field)):
                violations.append(_v(
                    "L2", _new_level("ERROR"), stem,
                    f"[layer] {node_type} 는 '{field}' 필수",
                ))

        # L1 — 본문 dead link
        for t in body_targets:
            if _resolve(t, nodes, alias_index) is None:
                violations.append(_v("L1", "ERROR", stem, f"dead link 본문 [[{t}]]"))
            else:
                degree[stem] += 1
                degree[_resolve(t, nodes, alias_index)] += 1

        # L1 — up dead link / L3 오버레이 / L4 방향 / L6 archive
        for t in up_list:
            resolved = _resolve(t, nodes, alias_index)
            if resolved is None:
                violations.append(_v("L1", "ERROR", stem, f"dead link up: [[{t}]]"))
                continue
            # L3 — up stem 은 본문 [[]] 에도 있어야 (오버레이 전제)
            if t not in body_targets:
                violations.append(_v("L3", "ERROR", stem, f"up '{t}' 가 본문 [[]] 에 없음"))
            # L4 — 방향 정합 (층 기준, KDEV-DEC-010 D3)
            if node_type == "idea":
                violations.append(_v("L4", "ERROR", stem, "idea 는 up 금지 (휘발)"))
            else:
                target_type = nodes[resolved].get("type")
                src_layer = layer_of(node_type)
                tgt_layer = layer_of(target_type)
                if src_layer and tgt_layer:
                    # 상류(같거나 낮은 층)만 허용. 비교가 종전과 반대 방향이다.
                    if _LAYER_RANK[tgt_layer] > _LAYER_RANK[src_layer]:
                        violations.append(_v(
                            "L4", _new_level("ERROR"), stem,
                            f"[layer] up '{resolved}'({target_type}/{tgt_layer}) 가 하류 — "
                            f"{node_type}/{src_layer} 는 같거나 낮은 층만 up 가능",
                        ))
                elif src_layer and tgt_layer is None:
                    # 층에 속하지 않는 노드는 상류가 될 수 없다 — `idea`(휘발)가 대표 사례다.
                    # 이 분기가 없으면 `idea` 를 up 하는 것을 아무도 못 잡는다.
                    violations.append(_v(
                        "L4", _new_level("ERROR"), stem,
                        f"[layer] up '{resolved}'({target_type}) 는 층에 속하지 않아 "
                        f"상류가 될 수 없다",
                    ))
            # L6 — 활성 노트가 archived 를 up 의존
            if nodes[resolved].get("archived") and not node.get("archived"):
                violations.append(_v("L6", "WARN", stem, f"archived '{resolved}' 를 up 의존"))

    # L5 — orphan. **층마다 의미가 다르다** (KDEV-DEC-010 D5).
    # 종전에는 지식 노드 전체에 같은 WARN 을 매겨 157건이 상시 켜져 있었고, 그러면
    # 경보가 정보를 내지 못한다. 층별로 나눠 `source` 는 위반이 아니라 작업 큐로 집계한다.
    for stem in sorted(nodes):
        layer = layer_of(nodes[stem].get("type"))
        if layer is None or layer == "execution":
            # 층 없음(idea·persona 계열) / 실행층(제품 파이프라인 소관) — 검사 제외
            continue
        if degree.get(stem, 0) > 0:
            continue
        if layer == "source":
            # 위반이 아니다 — "아직 개념으로 정리되지 않은 자료" 지표.
            violations.append(_v(
                "L5", "INFO", stem, "[layer] 미소화 — 아직 개념으로 정리되지 않은 자료",
            ))
        elif layer == "concept":
            # concept 는 up 필수(L2)라 정상 경로로는 여기 도달하지 않는다.
            violations.append(_v(
                "L5", _new_level("ERROR"), stem,
                "[layer] orphan — 출처도 없고 인용되지도 않음",
            ))

    return violations


def unsourced_queue(violations: list[dict]) -> list[str]:
    """미소화 큐 — `source` 층 orphan 목록. 위반이 아니라 정제 작업 후보다.

    KDEV-SPEC-005 의 열람 표면이 이 목록을 그대로 노출한다.
    """
    return [
        v["node"] for v in violations
        if v["rule"] == "L5" and v["level"] == "INFO"
    ]


def _v(rule: str, level: str, node: str, detail: str) -> dict:
    return {"rule": rule, "level": level, "node": node, "detail": detail}


def summarize(violations: list[dict]) -> dict[str, int]:
    """위반 리스트 → {rule: count} + 'ERROR'/'WARN' 합계 (리포트/로그용)."""
    out: dict[str, int] = defaultdict(int)
    for v in violations:
        out[v["rule"]] += 1
        out[v["level"]] += 1
    return dict(out)
