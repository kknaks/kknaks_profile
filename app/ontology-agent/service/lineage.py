"""계층 목록과 컬럼 계보 — 「이 컬럼이 어느 브론즈에서 어떤 규칙으로 왔는가」.

근거 기록 참조는 계층마다 정해져 있다 — 브론즈 → 기록 02 · 실버 → 04 · 골드 → 05 ·
그래프 → 07 (BASE-001 화면 표). 화면이 이 값으로 「문서가 앱의 설명서」를 만든다.
"""

from __future__ import annotations

import sqlite3

from . import allowlist as al
from . import glossary
from .errors import UnknownTable
from .queries import _relation_columns

NOTE_REF_BY_LAYER = {
    "bronze": "기록 02 브론즈 실사",
    "silver": "기록 04 실버 빌드",
    "gold": "기록 05 골드 KPI",
    "ontology": "기록 07 온톨로지",
}

#: 파생 컬럼 접미어 — 지표 본체의 계보를 물려받되 자기 설명을 단다(기록 05 2.3).
_DERIVED_SUFFIX = {
    "_dod": ("전일 대비 변화량", "직전 **존재 행** 기준(결측일은 건너뛴다)"),
    "_dod_pct": ("전일 대비 변화율", "직전 존재 행 기준. 직전 값이 0이면 null"),
    "_ma7": ("7일 이동평균", "직전 7개 존재 행 평균"),
    "_status": ("상태(양호·주의·경고)", "전 기간 백분위 — 나쁜 방향 하위 25% 주의 · 10% 경고"),
}


def layer_tables(conn: sqlite3.Connection, layer: str) -> dict:
    if layer not in al.LAYERS:
        raise UnknownTable(f"알 수 없는 계층: {layer!r}", allowed=list(al.LAYERS))
    tables = []
    for spec in al.tables_of(layer):
        row_count = conn.execute(f"SELECT COUNT(*) FROM {spec.relation}").fetchone()[0]
        tables.append({
            "table": spec.table,
            "view": spec.relation,
            "row_count": row_count,
            "masked": spec.masked,
            "masked_fields": list(spec.masked_fields),
            # 원천 축 — 화면의 2단 칩(vegas · review · nexus)이 이 값으로 갈린다.
            # 계층 하나에 원천이 셋이라 테이블 이름만으로는 갈리지 않는다.
            "source_group": spec.source_group or None,
            # 컬럼 계약이 없는 테이블은 그 사유를 준다 —
            # 화면이 「없다」와 「아직 안 적었다」를 구분할 수 있게(그 외는 null)
            "columns_note": spec.columns_note,
            "note_ref": spec.note_ref or NOTE_REF_BY_LAYER.get(layer, ""),
            "flows_to": [dict(f) for f in spec.flows_to],
        })
    return {"layer": layer, "tables": tables}


def lineage(conn: sqlite3.Connection, layer: str, table: str) -> dict:
    spec = al.resolve(layer, table)
    if spec is None:
        raise UnknownTable(
            f"조회할 수 없는 대상: layer={layer!r} table={table!r}",
            allowed=[{"layer": t.layer, "table": t.table} for t in al.TABLES.values()],
        )
    columns = _relation_columns(conn, spec.relation)
    downstream_map = _downstream(spec)
    out = []
    for column in columns:
        out.append(_column_lineage(conn, spec, column, downstream_map))
    return {"layer": layer, "table": table, "view": spec.relation,
            "note_ref": spec.note_ref or NOTE_REF_BY_LAYER.get(layer, ""),
            "columns": out}


def _downstream(spec: al.TableSpec) -> list[dict]:
    return [dict(f) for f in spec.flows_to]


def _column_lineage(
    conn: sqlite3.Connection, spec: al.TableSpec, column: str, downstream: list[dict]
) -> dict:
    base, suffix = _split_derived(column)
    term = glossary.lookup(base)

    payload: dict = {
        "column": column,
        "formula": None,
        "note": None,
        # 실버 컬럼의 글로서리 규칙 ID. 체계의 SoT 는 기록 03·04 이고 API 는 실어 나른다.
        # 아직 규칙 ID 가 부여되지 않은 컬럼은 null 이다(골드도 null).
        "rule_id": None,
        "gate": None,
        "source_columns": [],
        "downstream": downstream if suffix is None else [],
        "is_provisional": _is_provisional(spec, column),
        "note_ref": spec.note_ref or NOTE_REF_BY_LAYER.get(spec.layer, ""),
        "status_thresholds": None,
    }
    if term is not None:
        payload["formula"] = term.formula
        payload["note"] = term.note
        payload["gate"] = term.gate
        payload["source_columns"] = list(term.source_columns)
        payload["note_ref"] = term.source_note
        if term.direction:
            th = _thresholds(conn, spec.relation, base)
            if th:
                payload["status_thresholds"] = {"direction": term.direction, **th}
    if suffix is not None:
        label, note = _DERIVED_SUFFIX[suffix]
        payload["formula"] = f"{glossary.label_of(base)} — {label}"
        payload["note"] = note
        payload["source_columns"] = [f"{spec.relation}.{base}"]
        payload["status_thresholds"] = None
    if spec.masked_fields and column in spec.masked_fields:
        payload["note"] = (payload["note"] or "") + (
            " · 마스킹 뷰 경유 — 원값은 이 표면으로 나오지 않는다").strip()
    return payload


def _split_derived(column: str) -> tuple[str, str | None]:
    for suffix in _DERIVED_SUFFIX:
        if column.endswith(suffix):
            return column[: -len(suffix)], suffix
    return column, None


def _is_provisional(spec: al.TableSpec, column: str) -> bool:
    """아직 확정되지 않은 값인가 — `null`(관측 없음)과 구분되는 축이다.

    부분 코호트·부분 주·부분 월 플래그를 가진 테이블의 값 컬럼이 여기 걸린다.
    """
    flag = {
        "gold_retention_monthly": "is_partial_cohort",
        "gold_kpi_weekly": "is_partial_week",
        "gold_kpi_monthly": "is_partial_month",
    }.get(spec.relation)
    if flag is None:
        return False
    return column not in (flag, al.GRAIN_KEY.get(spec.table, ""), "month_start",
                          "week_start", "iso_year", "iso_week", "days_observed",
                          "cohort_month")


def _thresholds(conn: sqlite3.Connection, relation: str, metric: str) -> dict | None:
    cols = _relation_columns(conn, relation)
    if f"{metric}_status" not in cols:
        return None
    direction = glossary.direction_of(metric)
    agg = "MIN" if direction == "높을수록 나쁨" else "MAX"
    row = conn.execute(
        f'SELECT {agg}(CASE WHEN "{metric}_status" = \'주의\' THEN "{metric}" END) AS warn, '
        f'{agg}(CASE WHEN "{metric}_status" = \'경고\' THEN "{metric}" END) AS alert '
        f"FROM {relation}"
    ).fetchone()
    if row is None or (row["warn"] is None and row["alert"] is None):
        return None
    return {"주의": row["warn"], "경고": row["alert"]}
