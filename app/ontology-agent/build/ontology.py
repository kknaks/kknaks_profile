"""온톨로지 적재 — `ontology/nodes.csv` · `edges.csv` → `ontology_nodes` · `ontology_edges`.

관계 지식은 프롬프트·코드 상수가 아니라 **데이터**다(S-001). 채택뿐 아니라 기각·보류도
행으로 남는다 — 「왜 그리지 않았나」가 조회 가능해야 같은 질문이 반복되지 않는다.

`lag` 는 원천 문자열을 원형 그대로 적재하고, 도구·API 노출용 일 단위 정수를
`lag_days` 로 병기한다(2026-09-02 코디네이터 확정 — `2w` → 14, 빈 값 → NULL).
"""

from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

from config import sources_for

from .errors import BuildError, NodeIdMismatch, OrphanEdge
from db.connection import atomic
from .spec_contract import (
    EXOGENOUS_NODES,
    EXPECTED_EDGE_COUNT,
    EXPECTED_NODE_COUNT,
    NODE_TYPE_COUNTS,
    SPEC_NODES,
    VERDICT_COUNTS,
    VERDICTS_REQUIRING_RATIONALE,
)

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
LAG_UNIT_DAYS = {"d": 1, "w": 7, "m": 30}
LAG_PATTERN = re.compile(r"^(\d+)([dwm])$")


def lag_days(lag: str | None) -> int | None:
    """`0d`·`7d`·`2w` → 일 단위 정수. 빈 값·해석 불가는 None."""
    if not lag:
        return None
    m = LAG_PATTERN.match(lag.strip())
    if not m:
        return None
    return int(m.group(1)) * LAG_UNIT_DAYS[m.group(2)]


def _read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def load(conn: sqlite3.Connection, *, ontology_dir: Path | None = None) -> dict:
    """정본 CSV → 온톨로지 테이블. 무결성 위반이면 롤백하고 예외를 던진다."""
    odir = ontology_dir or sources_for().ontology_dir
    nodes = _read_csv(odir / "nodes.csv")
    edges = _read_csv(odir / "edges.csv")

    with atomic(conn, "ontology"):
        conn.execute("DELETE FROM ontology_edges")
        conn.execute("DELETE FROM ontology_nodes")
        conn.executemany(
            "INSERT INTO ontology_nodes (node_id, name_ko, node_type, controllable, grain, source) "
            "VALUES (?,?,?,?,?,?)",
            [(n["node_id"], n["name_ko"], n["node_type"], n["controllable"], n["grain"], n["source"])
             for n in nodes],
        )
        conn.executemany(
            "INSERT INTO ontology_edges "
            "(cause, effect, sign, lag, lag_days, edge_kind, confidence, evidence, verdict, rationale) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            [(e["cause"], e["effect"], e["sign"], e["lag"], lag_days(e["lag"]),
              e["edge_kind"], e["confidence"], e["evidence"], e["verdict"], e["rationale"])
             for e in edges],
        )
        result = check(conn)
    return result


def check(conn: sqlite3.Connection) -> dict:
    """온톨로지 무결성 + SPEC-001 §4 25종 1:1 대조 (AC-6). 단독 재실행 가능."""
    nodes = [dict(r) for r in conn.execute("SELECT * FROM ontology_nodes")]
    edges = [dict(r) for r in conn.execute("SELECT * FROM ontology_edges")]
    node_ids = {n["node_id"] for n in nodes}

    # --- 고아 엣지 0 (ORPHAN_EDGE) ---
    orphans = [f"{e['cause']} → {e['effect']}" for e in edges
               if e["cause"] not in node_ids or e["effect"] not in node_ids]
    if orphans:
        raise OrphanEdge(f"고아 엣지 {len(orphans)}건 — 없는 노드를 가리킨다", orphans)

    # --- SPEC-001 §4 25종 1:1 대조 (NODE_ID_MISMATCH) ---
    spec_by_id = {nid: (label, ntype) for nid, label, ntype in SPEC_NODES}
    actual_by_id = {n["node_id"]: (n["name_ko"], n["node_type"]) for n in nodes}
    detail: list[str] = []
    for nid in sorted(spec_by_id.keys() - actual_by_id.keys()):
        detail.append(f"spec 에만 있음: {nid} ({spec_by_id[nid][0]})")
    for nid in sorted(actual_by_id.keys() - spec_by_id.keys()):
        detail.append(f"정본에만 있음: {nid} ({actual_by_id[nid][0]})")
    for nid in sorted(spec_by_id.keys() & actual_by_id.keys()):
        if spec_by_id[nid] != actual_by_id[nid]:
            detail.append(
                f"{nid}: spec {spec_by_id[nid]} vs 정본 {actual_by_id[nid]}"
            )
    if detail:
        raise NodeIdMismatch(
            f"SPEC-001 §4 25종 표와 1:1 대응 실패 {len(detail)}건 — "
            "표를 조용히 맞추지 않는다. spec 을 먼저 고친다",
            detail,
        )

    problems: list[str] = []
    if len(nodes) != EXPECTED_NODE_COUNT:
        problems.append(f"노드 {len(nodes)}행 (기대 {EXPECTED_NODE_COUNT})")
    if len(edges) != EXPECTED_EDGE_COUNT:
        problems.append(f"엣지 {len(edges)}행 (기대 {EXPECTED_EDGE_COUNT})")

    # --- node_id 전건 snake_case ---
    bad_case = [n["node_id"] for n in nodes if not SNAKE_CASE.match(n["node_id"])]
    if bad_case:
        problems.append(f"snake_case 위반 node_id: {bad_case}")

    # --- node_type 분포 ---
    type_counts: dict[str, int] = {}
    for n in nodes:
        type_counts[n["node_type"]] = type_counts.get(n["node_type"], 0) + 1
    if type_counts != NODE_TYPE_COUNTS:
        problems.append(f"node_type 분포 {type_counts} (기대 {NODE_TYPE_COUNTS})")

    # --- 외생 노드는 들어오는 엣지 0 ---
    incoming = [f"{e['cause']} → {e['effect']}" for e in edges if e["effect"] in EXOGENOUS_NODES]
    if incoming:
        problems.append(f"외생 노드에 들어오는 엣지 {len(incoming)}건: {incoming}")

    # --- 판정 분포 + 기각·보류의 사유 필수 ---
    verdicts: dict[str, int] = {}
    for e in edges:
        verdicts[e["verdict"]] = verdicts.get(e["verdict"], 0) + 1
    if verdicts != VERDICT_COUNTS:
        problems.append(f"판정 분포 {verdicts} (기대 {VERDICT_COUNTS})")
    missing_rationale = [
        f"{e['cause']} → {e['effect']} ({e['verdict']})" for e in edges
        if e["verdict"] in VERDICTS_REQUIRING_RATIONALE and not (e["rationale"] or "").strip()
    ]
    if missing_rationale:
        problems.append(f"사유 없는 기각·보류 행 {len(missing_rationale)}건: {missing_rationale}")

    if problems:
        raise BuildError("온톨로지 무결성 위반", problems)

    lag_forms = sorted({(e["lag"] or "", e["lag_days"]) for e in edges})
    return {
        "nodes": len(nodes), "edges": len(edges),
        "orphans": 0, "node_type_counts": type_counts, "verdict_counts": verdicts,
        "lag_forms": lag_forms,
        "spec_1to1": "pass",
    }
