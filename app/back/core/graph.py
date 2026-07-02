"""지식그래프 — products 포함 노드/엣지(type,dir)/백링크 + L1~L6 검증 (report-only).

KDEV-SPEC-002 §4 (그래프 스키마) · KDEV-SPEC-004 (검증 게이트 L1~L6) 구현.
KDEV-WORK-001. **report-only**: 검증은 위반 리스트를 반환만 하고 절대 raise 하지 않는다.
enforcement(ERROR 차단/fail-fast/pre-commit/CI)는 WORK-007 범위.

노드 식별자 = 파일명 stem (spec-002 §4). 노드 dict 기대 키:
    type, title, body, up(list[str]), aliases(list[str]), id, archived(bool).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from core.wikilinks import extract_wikilinks

# spec-002 §4 + spec-001/007 (persona) + products frontmatter type 합집합.
# report-only 단계라 넉넉히 허용 — 미등록 type 만 L2 로 보고.
ALLOWED_NODE_TYPES: set[str] = {
    # zettel (spec-002 §4)
    "idea", "reference", "permanent", "post", "product",
    # persona (spec-001/007)
    "profile", "career", "project", "note", "content", "daily", "algorithm",
    # products
    "baseline", "decision", "spec", "work", "release", "runbook", "bugfix",
}

# L5 orphan 대상 — zettel 지식 노드만 (decision-003 node type 중 idea 제외).
# daily·algorithm·career·note·spec·work 등은 그래프 연결 의무가 없어 orphan 검사 제외
# (KDEV-WORK-002 Phase 3, KDEV-SPEC-004 §4).
KNOWLEDGE_NODE_TYPES: set[str] = {"reference", "permanent", "post", "product"}

# L4 방향 정합 — 위계 rank (높을수록 상류). up 타겟 rank >= source rank 여야 함.
# idea 는 어떤 것도 up 할 수 없다 (rank 0 + 별도 가드).
_TYPE_RANK: dict[str, int] = {
    "idea": 0, "daily": 0,
    "note": 1, "content": 1, "post": 1, "project": 1, "career": 1, "profile": 1,
    "work": 2, "release": 2, "runbook": 2, "bugfix": 2, "algorithm": 1,
    "spec": 3, "decision": 3,
    "reference": 4, "permanent": 4, "baseline": 4, "product": 4,
}


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
      "nodes":     [{"id": stem, "type", "title", "archived"}],
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
    L4 방향 정합         ERROR  up 타겟이 상류(rank↑), idea up 금지
    L5 orphan            WARN   엣지 0 노드
    L6 archive 참조      WARN   활성 노트가 archived 를 up 의존
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
        elif node_type not in ALLOWED_NODE_TYPES:
            violations.append(_v("L2", "ERROR", stem, f"미등록 type '{node_type}'"))

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
            # L4 — 방향 정합
            if node_type == "idea":
                violations.append(_v("L4", "ERROR", stem, "idea 는 up 금지"))
            else:
                src_rank = _TYPE_RANK.get(node_type, 1)
                tgt_rank = _TYPE_RANK.get(nodes[resolved].get("type"), 1)
                if tgt_rank < src_rank:
                    violations.append(_v(
                        "L4", "ERROR", stem,
                        f"up '{resolved}'({nodes[resolved].get('type')}) 가 "
                        f"하류 — 상류만 up 가능",
                    ))
            # L6 — 활성 노트가 archived 를 up 의존
            if nodes[resolved].get("archived") and not node.get("archived"):
                violations.append(_v("L6", "WARN", stem, f"archived '{resolved}' 를 up 의존"))

    # L5 — orphan (resolve 된 엣지가 in/out 모두 0). 지식 노드만 대상.
    for stem in sorted(nodes):
        if nodes[stem].get("type") not in KNOWLEDGE_NODE_TYPES:
            continue
        if degree.get(stem, 0) == 0:
            violations.append(_v("L5", "WARN", stem, "orphan (엣지 0개)"))

    return violations


def _v(rule: str, level: str, node: str, detail: str) -> dict:
    return {"rule": rule, "level": level, "node": node, "detail": detail}


def summarize(violations: list[dict]) -> dict[str, int]:
    """위반 리스트 → {rule: count} + 'ERROR'/'WARN' 합계 (리포트/로그용)."""
    out: dict[str, int] = defaultdict(int)
    for v in violations:
        out[v["rule"]] += 1
        out[v["level"]] += 1
    return dict(out)
