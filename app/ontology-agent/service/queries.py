"""조회 구현 — **도구와 API 가 같은 함수를 부른다.**

WORK-002 「Internal Interface Contract」: 화면용 집계 로직을 따로 만들지 않는다.
`/api/kpi/series` 와 도구 `query_kpi` 가 같은 함수를 지나므로 SPEC-003 AC-5(오차 0)가
**대조가 아니라 구조로** 성립한다 — 두 구현이 없으면 어긋날 수 없다.

조회 대상은 전부 `allowlist` 를 지난다. 이 모듈에 브론즈·실버 원 테이블 이름을 쓰지 않는다.
"""

from __future__ import annotations

import re
import sqlite3
from typing import Any

from . import allowlist as al
from .errors import (
    InvalidRange,
    LimitExceeded,
    TooManyFilters,
    UnknownField,
    UnknownMetric,
    UnknownNode,
    UnknownTable,
)

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
#: 식별자로 허용하는 모양. 값은 전부 바인딩 파라미터라 SQL 에 문자열로 박히는 것은
#: allowlist 를 통과한 관계명·컬럼명뿐이고, 그것도 이 패턴을 한 번 더 지난다.
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _ident(name: str) -> str:
    if not _IDENT.match(name):
        raise UnknownField(f"식별자로 쓸 수 없는 이름: {name!r}")
    return name


def _check_date(value: str, label: str) -> str:
    if not isinstance(value, str) or not _DATE.match(value):
        raise InvalidRange(f"{label} 는 YYYY-MM-DD 형식이어야 한다: {value!r}")
    return value


def _check_limit(limit: int) -> int:
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise LimitExceeded(f"limit 은 정수여야 한다: {limit!r}")
    if limit < 1 or limit > al.MAX_LIMIT:
        raise LimitExceeded(
            f"limit 은 1~{al.MAX_LIMIT} 이다(요청 {limit}). "
            "상한을 넘는 요청은 잘라서 주지 않고 거부한다 — 낮춰서 다시 부른다"
        )
    return limit


# --- query_kpi --------------------------------------------------------------


def query_kpi(
    conn: sqlite3.Connection,
    *,
    metrics: list[str],
    grain: str,
    start: str,
    end: str,
    include_status: bool = True,
    include_deltas: bool = False,
) -> dict:
    """골드 View **조회**. 도구가 집계하지 않는다 — grain 마다 View 하나다."""
    if grain not in al.GRAIN_RELATION:
        raise InvalidRange(
            f"grain 은 {list(al.GRAIN_RELATION)} 중 하나다: {grain!r}",
            allowed=list(al.GRAIN_RELATION),
        )
    allowed = al.metrics_of(grain)
    if not metrics or not isinstance(metrics, list):
        raise UnknownMetric("metrics 는 1개 이상이어야 한다", allowed=list(allowed))
    if len(metrics) > al.MAX_METRICS:
        raise UnknownMetric(
            f"metrics 는 최대 {al.MAX_METRICS}개다(요청 {len(metrics)})",
            allowed=list(allowed))
    unknown = [m for m in metrics if m not in allowed]
    if unknown:
        # 목록 밖이 1건이라도 있으면 **전체 거부**다(SPEC-002 Validation).
        raise UnknownMetric(
            f"grain={grain} 에서 조회할 수 없는 지표: {unknown}", allowed=list(allowed))

    _check_date(start, "start")
    _check_date(end, "end")
    if start > end:
        raise InvalidRange(f"start 가 end 보다 뒤다: {start} > {end}")

    relation = al.GRAIN_RELATION[grain]
    key = al.GRAIN_KEY[grain]
    partial_flag = al.GRAIN_PARTIAL_FLAG[grain]

    cols = [_ident(key)] + [_ident(m) for m in metrics]
    if partial_flag:
        cols.append(_ident(partial_flag))
    if include_status:
        cols += [f"{_ident(m)}_status" for m in metrics if _has_column(conn, relation, f"{m}_status")]
    if include_deltas:
        for m in metrics:
            for suffix in ("_dod", "_dod_pct", "_ma7"):
                if _has_column(conn, relation, f"{m}{suffix}"):
                    cols.append(_ident(f"{m}{suffix}"))

    select = ", ".join(f'"{c}"' for c in dict.fromkeys(cols))
    sql = f'SELECT {select} FROM {relation} WHERE "{key}" >= ? AND "{key}" <= ? ORDER BY "{key}"'
    # 월/코호트 그레인은 키가 YYYY-MM 이라 날짜 문자열과 직접 비교하면 경계가 어긋난다.
    lo, hi = (start[:7], end[:7]) if key in ("month", "cohort_month") else (start, end)
    raw = conn.execute(sql, (lo, hi)).fetchall()

    rows = []
    for r in raw:
        d = dict(r)
        row: dict[str, Any] = {"period_key": d[key]}
        if partial_flag:
            row["is_partial"] = bool(d[partial_flag])
        # 관측 없음(None)은 그대로 null 로 흘린다 — 실제 0 과 구분해야 한다(AC-8).
        row["values"] = {m: d.get(m) for m in metrics}
        if include_status:
            status = {m: d[f"{m}_status"] for m in metrics if f"{m}_status" in d}
            row["status"] = {k: v for k, v in status.items() if v is not None}
        if include_deltas:
            row["deltas"] = {
                c: d[c] for c in d
                if c.endswith(("_dod", "_dod_pct", "_ma7"))
            }
        rows.append(row)

    return {
        "grain": grain,
        "period": {"start": start, "end": end},
        "rows": rows,
        "formulas": formulas_for(metrics),
        "status_thresholds": thresholds_for(conn, metrics, relation),
        "source": {"table": relation, "row_count": len(rows)},
    }


def _has_column(conn: sqlite3.Connection, relation: str, column: str) -> bool:
    cols = _relation_columns(conn, relation)
    return column in cols


#: 키에 **DB 경로**를 넣는다. 관계명만으로 캐시하면 서로 다른 DB(테스트의 임시 DB ·
#: 재빌드본)를 오가는 프로세스에서 앞선 스키마가 남아 오염된다.
_COLUMN_CACHE: dict[tuple[str, str], tuple[str, ...]] = {}


def _db_key(conn: sqlite3.Connection) -> str:
    row = conn.execute("PRAGMA database_list").fetchone()
    return row[2] if row else ""


def _relation_columns(conn: sqlite3.Connection, relation: str) -> tuple[str, ...]:
    key = (_db_key(conn), relation)
    cached = _COLUMN_CACHE.get(key)
    if cached is None:
        cached = tuple(r[1] for r in conn.execute(f"PRAGMA table_info({relation})"))
        _COLUMN_CACHE[key] = cached
    return cached


def reset_column_cache() -> None:
    _COLUMN_CACHE.clear()
    al.reset_field_cache()


def formulas_for(metrics: list[str]) -> list[dict]:
    from .glossary import formula_of

    out = []
    for m in metrics:
        f = formula_of(m)
        if f:
            out.append(f)
    return out


def thresholds_for(
    conn: sqlite3.Connection, metrics: list[str], relation: str
) -> list[dict]:
    """상태 경계 — 빌드가 산출한 `_status` 컬럼에서 역산한다.

    경계값을 코드 상수로 두지 않는다. 빌드가 전 기간 백분위로 매번 산정하므로
    (기록 05 승인 1) 상수를 두면 재빌드 때 조용히 어긋난다.
    """
    from .glossary import direction_of

    out = []
    for m in metrics:
        if m in al.NO_STATUS_METRICS:
            continue  # 방향 없는 개입 변수 — 상태 없음
        status_col = f"{m}_status"
        if not _has_column(conn, relation, status_col):
            continue
        direction = direction_of(m)
        bounds = _status_bounds(conn, relation, m, status_col, direction)
        if bounds:
            out.append({"metric": m, "direction": direction,
                        **bounds, "method": "전 기간 백분위 25%/10%"})
    return out


def _status_bounds(
    conn: sqlite3.Connection, relation: str, metric: str, status_col: str, direction: str
) -> dict | None:
    agg = "MIN" if direction == "높을수록 나쁨" else "MAX"
    row = conn.execute(
        f'SELECT {agg}(CASE WHEN "{status_col}" = \'주의\' THEN "{metric}" END) AS warn, '
        f'{agg}(CASE WHEN "{status_col}" = \'경고\' THEN "{metric}" END) AS alert '
        f"FROM {relation}"
    ).fetchone()
    if row is None or (row["warn"] is None and row["alert"] is None):
        return None
    return {"주의": row["warn"], "경고": row["alert"]}


# --- query_layer ------------------------------------------------------------


def query_layer(
    conn: sqlite3.Connection,
    *,
    layer: str,
    table: str,
    filters: list[dict] | None = None,
    order_by: dict | None = None,
    limit: int = al.DEFAULT_TOOL_LIMIT,
    offset: int = 0,
) -> dict:
    """마스킹 뷰·PII 없는 테이블 행 조회. 원 테이블 경로는 존재하지 않는다."""
    spec = al.resolve(layer, table)
    if spec is None:
        raise UnknownTable(
            f"조회할 수 없는 대상: layer={layer!r} table={table!r}",
            allowed=[{"layer": t.layer, "table": t.table} for t in al.TABLES.values()],
        )
    fields = al.fields_of(conn, spec)
    limit = _check_limit(limit)
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        raise InvalidRange(f"offset 은 0 이상 정수다: {offset!r}")

    filters = filters or []
    if len(filters) > al.MAX_FILTERS:
        raise TooManyFilters(f"필터는 최대 {al.MAX_FILTERS}개다(요청 {len(filters)})")

    where, params = _build_where(filters, fields, spec)
    order_sql = _build_order(order_by, fields)

    total = conn.execute(
        f"SELECT COUNT(*) FROM {spec.relation}{where}", params
    ).fetchone()[0]
    raw = conn.execute(
        f"SELECT * FROM {spec.relation}{where}{order_sql} LIMIT ? OFFSET ?",
        (*params, limit, offset),
    ).fetchall()

    return {
        "layer": layer,
        "table": table,
        "view": spec.relation,
        "total": total,                      # 항상 실어 「더 있다」가 드러나게 한다
        "returned": len(raw),
        "offset": offset,
        "masked_fields": list(spec.masked_fields),
        "columns": list(fields),
        "rows": [dict(r) for r in raw],
        "source_note": "마스킹 뷰 경유 — 원 테이블 직접 조회 경로 없음",
    }


def _build_where(
    filters: list[dict], fields: tuple[str, ...], spec: al.TableSpec
) -> tuple[str, list]:
    clauses: list[str] = []
    params: list = []
    for f in filters:
        if not isinstance(f, dict):
            raise UnknownField(f"필터는 {{field, op, value}} 객체다: {f!r}")
        field = f.get("field")
        op = f.get("op", "eq")
        value = f.get("value")
        if field not in fields:
            # 목록 밖 이름을 막는다. **PII 원 컬럼명은 여기서 걸리지 않는다** —
            # 마스킹 뷰가 별칭을 원본과 같게 주므로(`... AS "patientName"`) 세 이름은
            # 허용 목록 안에 있고 필터를 통과한다. 원값 우회가 성립하지 않는 이유는
            # 「이름이 없어서」가 아니라 **값이 마스킹본이라 한 건도 안 맞아서**다
            # (`tests/test_w002_tools.py` 의 total == 0 이 그것을 실증한다).
            # 뷰가 원 테이블을 가린다는 보장은 AC-8 정적 게이트 + 뷰 SELECT 목록이 진다.
            raise UnknownField(
                f"조회할 수 없는 필드: {field!r}", allowed=list(fields))
        if op not in al.FILTER_OPS:
            raise UnknownField(f"지원하지 않는 연산자: {op!r}", allowed=list(al.FILTER_OPS))
        col = f'"{_ident(field)}"'
        if op == "eq":
            clauses.append(f"{col} = ?"); params.append(value)
        elif op == "ne":
            clauses.append(f"{col} <> ?"); params.append(value)
        elif op == "gte":
            clauses.append(f"{col} >= ?"); params.append(value)
        elif op == "lte":
            clauses.append(f"{col} <= ?"); params.append(value)
        elif op == "in":
            values = list(value) if isinstance(value, (list, tuple)) else [value]
            if not values:
                raise UnknownField("in 필터의 value 가 비었다")
            clauses.append(f"{col} IN ({','.join('?' * len(values))})")
            params.extend(values)
        elif op == "between":
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                raise InvalidRange("between 은 [시작, 끝] 두 값이다")
            clauses.append(f"{col} BETWEEN ? AND ?"); params.extend(value)
        elif op == "contains":
            if field in spec.masked_fields and field not in ("body", "authorName"):
                raise UnknownField(f"contains 를 쓸 수 없는 필드: {field!r}")
            clauses.append(f"{col} LIKE ?"); params.append(f"%{value}%")
    return (f" WHERE {' AND '.join(clauses)}" if clauses else "", params)


def _build_order(order_by: dict | None, fields: tuple[str, ...]) -> str:
    if not order_by:
        return ""
    field = order_by.get("field")
    if field not in fields:
        raise UnknownField(f"정렬할 수 없는 필드: {field!r}", allowed=list(fields))
    direction = str(order_by.get("direction", "asc")).lower()
    if direction not in ("asc", "desc"):
        raise InvalidRange(f"direction 은 asc·desc 다: {direction!r}")
    return f' ORDER BY "{_ident(field)}" {direction.upper()}'


# --- trace_ontology ---------------------------------------------------------


def _edge_id(cause: str, effect: str) -> str:
    """안정 식별자 — 형식은 `<from>__<to>`(밑줄 2개, SPEC-003 §4)."""
    return f"{cause}__{effect}"


#: 사유(`reason`)가 필수인 판정. 「왜 그리지 않았나」가 조회 가능해야 같은 질문이
#: 반복되지 않는다(SPEC-002 AC-5). 채택 엣지의 설명은 `reason` 이 아니라 `note` 다.
_REASON_VERDICTS = frozenset({"기각", "보류"})


def _edge_payload(row: sqlite3.Row) -> dict:
    verdict = row["verdict"]
    rationale = row["rationale"] or None
    return {
        "edge_id": _edge_id(row["cause"], row["effect"]),
        "from": row["cause"],
        "to": row["effect"],
        "sign": row["sign"] or None,
        "lag": row["lag"] or None,          # 정본 문자열 원형 — 재서술하지 않는다
        "lag_days": row["lag_days"],        # 일 단위 정수 병기 (2w → 14, 빈 값 → null)
        "kind": row["edge_kind"],
        "verdict": verdict,
        "confidence": row["confidence"] or None,
        "evidence": row["evidence"] or None,
        # `reason` 은 **배제 사유** 전용이다 — 채택 엣지에 채우면 「기각 사유가 있다」로 읽힌다
        "reason": rationale if verdict in _REASON_VERDICTS else None,
        # `note` 는 사람이 읽는 설명이고 `reason` 과 **별개 필드**다(SPEC-003 §4).
        # `ontology_edges` 의 텍스트 컬럼이 `rationale` 하나뿐이라 둘의 원천이 같다 —
        # 그래서 **배타적으로** 싣는다. 둘 다 채우면 기각·보류에서 `note == reason` 이 되고
        # 인스펙터가 두 필드를 각각 렌더해 같은 문장이 두 번 찍힌다(검수 W7).
        "note": None if verdict in _REASON_VERDICTS else rationale,
        # 보류·기각은 인과 서술에 쓰지 않는다 — 조회는 되지만 사용은 막는다
        "usable_for_causal_claim": verdict in al.CAUSAL_VERDICTS,
    }


def _node_payload(row: sqlite3.Row) -> dict:
    node_type = row["node_type"]
    return {
        "node_id": row["node_id"],
        "name": row["name_ko"],
        "node_type": node_type,
        "controllable": str(row["controllable"]).lower() == "true",
        "grain": row["grain"],
        "source": row["source"],
        # 미관측 노드 — 화면의 `?` 표시와 답변의 「모른다」가 여기서 온다
        "observed": node_type != "unobserved",
    }


def trace_ontology(
    conn: sqlite3.Connection,
    *,
    node: str | None = None,
    direction: str = "both",
    depth: int = 1,
    verdicts: list[str] | None = None,
) -> dict:
    if direction not in ("in", "out", "both"):
        raise InvalidRange(f"direction 은 in·out·both 다: {direction!r}",
                           allowed=["in", "out", "both"])
    if not isinstance(depth, int) or isinstance(depth, bool) or not (1 <= depth <= al.MAX_DEPTH):
        raise InvalidRange(f"depth 는 1~{al.MAX_DEPTH} 이다: {depth!r}")
    verdicts = list(verdicts) if verdicts else list(al.DEFAULT_VERDICTS)
    unknown = [v for v in verdicts if v not in al.VERDICTS]
    if unknown:
        raise InvalidRange(f"알 수 없는 판정: {unknown}", allowed=list(al.VERDICTS))

    all_nodes = {r["node_id"]: r for r in conn.execute("SELECT * FROM ontology_nodes")}
    placeholders = ",".join("?" * len(verdicts))
    all_edges = conn.execute(
        f"SELECT * FROM ontology_edges WHERE verdict IN ({placeholders})", verdicts
    ).fetchall()

    if node is None:
        nodes = list(all_nodes.values())
        edges = all_edges
    else:
        start = _resolve_node(node, all_nodes)
        frontier = {start}
        seen = {start}
        picked: list[sqlite3.Row] = []
        for _ in range(depth):
            nxt: set[str] = set()
            for e in all_edges:
                if direction in ("out", "both") and e["cause"] in frontier:
                    picked.append(e); nxt.add(e["effect"])
                if direction in ("in", "both") and e["effect"] in frontier:
                    picked.append(e); nxt.add(e["cause"])
            frontier = nxt - seen
            seen |= nxt
            if not frontier:
                break
        edges = list({(e["cause"], e["effect"]): e for e in picked}.values())
        nodes = [all_nodes[n] for n in seen if n in all_nodes]

    counts: dict[str, int] = {}
    for r in conn.execute("SELECT verdict, COUNT(*) AS n FROM ontology_edges GROUP BY verdict"):
        counts[r["verdict"]] = r["n"]

    return {
        "nodes": [_node_payload(n) for n in nodes],
        "edges": [_edge_payload(e) for e in edges],
        "counts": counts,
    }


def _resolve_node(node: str, all_nodes: dict) -> str:
    """`node_id` 또는 한글 이름 둘 다 받는다(SPEC-002 OQ-4)."""
    if node in all_nodes:
        return node
    for nid, row in all_nodes.items():
        if row["name_ko"] == node:
            return nid
    raise UnknownNode(f"알 수 없는 노드: {node!r}", allowed=sorted(all_nodes))
