"""모니터링 표면 — KPI 카드 · 그래프 · 예보.

화면이 숫자를 만들지 않도록 서버가 전부 준다(SPEC-003 §4). 카피(`title`·`message`)도
서버가 만든다 — 근거 추적 앱이라 문장을 FE 에 흩지 않는다.

**예보의 수치·신뢰도·lag 는 전부 DB 파생이다.** 기록 07 정본값은 `ontology_edges` 에
들어 있고 여기서 조회해 쓴다 — 코드에 하드코딩하지 않는다(SPEC-003 AC-15).
"""

from __future__ import annotations

import datetime
import sqlite3

from . import allowlist as al
from . import glossary
from .errors import InvalidRange
from .queries import _edge_id, _edge_payload, _node_payload, _relation_columns

#: 카드에 세우는 지표와 순서. 기록 05 2.2 지표 중 화면이 읽는 것들이다.
CARD_METRICS: tuple[tuple[str, str], ...] = (
    ("sales_total", "daily"),
    ("payment_visits", "daily"),
    ("avg_ticket", "daily"),
    ("visits", "daily"),
    ("new_patients", "daily"),
    ("revisits", "daily"),
    ("reservations", "daily"),
    ("cancel_rate", "daily"),
    ("noshow_rate", "daily"),
    ("new_churns", "daily"),
    ("new_patients_domestic", "daily"),
    ("foreign_sales_share", "daily"),
    ("naver_reviews", "daily"),
    ("gu_reviews", "weekly"),          # 유기 신호는 주 단위다 — 카드가 자기 그레인을 싣는다
)

ALERT_STATUSES = ("주의", "경고")


def _months(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute(
        "SELECT DISTINCT substr(date, 1, 7) AS m FROM gold_kpi_daily ORDER BY m")]


def kpi_cards(
    conn: sqlite3.Connection, *, period: str | None = None, window_days: int = 7
) -> dict:
    """KPI 카드 — 최근 `window_days` 의 상태 빈도로 노드 상태를 함께 낸다."""
    if not isinstance(window_days, int) or isinstance(window_days, bool) or window_days < 1:
        raise InvalidRange(f"window_days 는 1 이상 정수다: {window_days!r}")
    months = _months(conn)
    if not months:
        return {"as_of": None, "period": None, "window_days": window_days,
                "has_prev_period": False, "has_next_period": False, "cards": []}
    if period is None:
        period = months[-1]
    elif period not in months:
        raise InvalidRange(f"데이터에 없는 기간: {period!r}", allowed=months)

    idx = months.index(period)
    as_of = conn.execute(
        "SELECT MAX(date) FROM gold_kpi_daily WHERE substr(date, 1, 7) = ?", (period,)
    ).fetchone()[0]

    cards = []
    for metric, grain in CARD_METRICS:
        card = _card(conn, metric, grain, period, as_of, window_days)
        if card:
            cards.append(card)
    return {
        "as_of": as_of,
        "period": period,
        "window_days": window_days,
        # 기간 스테퍼 — 양쪽 화살표 비활성 근거를 서버가 준다
        "has_prev_period": idx > 0,
        "has_next_period": idx < len(months) - 1,
        "cards": cards,
    }


def _card(
    conn: sqlite3.Connection, metric: str, grain: str,
    period: str, as_of: str, window_days: int,
) -> dict | None:
    relation = al.GRAIN_RELATION[grain]
    cols = _relation_columns(conn, relation)
    if metric not in cols:
        return None
    key = al.GRAIN_KEY[grain]
    has_status = f"{metric}_status" in cols

    # 일별은 날짜, 주별은 주 시작일 — 둘 다 앞 7자가 `YYYY-MM` 이라 같은 절로 그 달을 고른다
    where, params = f'substr("{key}", 1, 7) = ?', (period,)

    select = [f'"{key}"', f'"{metric}"']
    for extra in (f"{metric}_status", f"{metric}_dod", f"{metric}_dod_pct"):
        if extra in cols:
            select.append(f'"{extra}"')
    rows = conn.execute(
        f"SELECT {', '.join(select)} FROM {relation} WHERE {where} ORDER BY \"{key}\"", params
    ).fetchall()
    if not rows:
        return None

    last = rows[-1]
    values = [r[metric] for r in rows]
    observed = [v for v in values if v is not None]
    # 미관측 카드는 스파크라인을 그리지 않는다 — null 이지 0 이 아니다
    spark = values[-7:] if observed else None

    status = last[f"{metric}_status"] if has_status else None
    alert_days = (
        sum(1 for r in rows[-window_days:] if r[f"{metric}_status"] in ALERT_STATUSES)
        if has_status else 0
    )
    unit, fmt = glossary.unit_of(metric)
    direction = glossary.direction_of(metric)
    card = {
        "metric": metric,
        "label": glossary.label_of(metric),
        "grain": grain,
        "latest": last[metric],
        "unit": unit,
        "format": fmt,
        "dod": last[f"{metric}_dod"] if f"{metric}_dod" in last.keys() else None,
        "dod_pct": last[f"{metric}_dod_pct"] if f"{metric}_dod_pct" in last.keys() else None,
        "spark": spark,
        "status": status,
        "alert_days": alert_days,
        "node_state": node_state(alert_days),
        "node_id": metric,
        "thresholds": _thresholds(conn, relation, metric, direction) if has_status else None,
        "direction": direction,
    }
    if metric in al.NO_STATUS_METRICS:
        # 방향 없는 개입 변수 — 상태 축을 아예 주지 않는다(SPEC-003 §4)
        card["status"] = None
        card["node_state"] = None
        card["alert_days"] = None
        card["thresholds"] = None
    return card


def node_state(alert_days: int | None) -> str | None:
    """알림 ≥3 · 관찰 ≥1 · 정상 0 (SPEC-003 OQ-5). 그래프 노드 색과 같은 기준이다."""
    if alert_days is None:
        return None
    if alert_days >= 3:
        return "알림"
    if alert_days >= 1:
        return "관찰"
    return "정상"


def _thresholds(
    conn: sqlite3.Connection, relation: str, metric: str, direction: str | None
) -> dict | None:
    agg = "MIN" if direction == "높을수록 나쁨" else "MAX"
    row = conn.execute(
        f'SELECT {agg}(CASE WHEN "{metric}_status" = \'주의\' THEN "{metric}" END) AS warn, '
        f'{agg}(CASE WHEN "{metric}_status" = \'경고\' THEN "{metric}" END) AS alert '
        f"FROM {relation}"
    ).fetchone()
    if row is None or (row["warn"] is None and row["alert"] is None):
        return None
    return {"주의": row["warn"], "경고": row["alert"]}


# --- 그래프 -----------------------------------------------------------------


def graph(
    conn: sqlite3.Connection, *, verdicts: list[str] | None = None,
    as_of: str | None = None, window_days: int = 7,
) -> dict:
    """노드·엣지 + 노드 상태. 노드 상태색 기준은 `/api/kpi/cards` 와 **같은 규칙**이다."""
    verdicts = list(verdicts) if verdicts else list(al.DEFAULT_VERDICTS)
    unknown = [v for v in verdicts if v not in al.VERDICTS]
    if unknown:
        raise InvalidRange(f"알 수 없는 판정: {unknown}", allowed=list(al.VERDICTS))

    as_of = as_of or conn.execute("SELECT MAX(date) FROM gold_kpi_daily").fetchone()[0]
    states = _node_states(conn, as_of, window_days)

    nodes = []
    for row in conn.execute("SELECT * FROM ontology_nodes"):
        payload = _node_payload(row)
        state = states.get(payload["node_id"])
        payload["node_state"] = state["node_state"] if state else None
        payload["alert_days"] = state["alert_days"] if state else None
        nodes.append(payload)

    placeholders = ",".join("?" * len(verdicts))
    edges = [
        _edge_payload(row)          # `note`·`reason` 구분은 `_edge_payload` 가 갖는다
        for row in conn.execute(
            f"SELECT * FROM ontology_edges WHERE verdict IN ({placeholders})", verdicts)
    ]

    counts: dict[str, int] = {}
    for r in conn.execute("SELECT verdict, COUNT(*) AS n FROM ontology_edges GROUP BY verdict"):
        counts[r["verdict"]] = r["n"]

    return {"as_of": as_of, "nodes": nodes, "edges": edges, "counts": counts}


def _node_states(
    conn: sqlite3.Connection, as_of: str | None, window_days: int
) -> dict[str, dict]:
    """노드별 최근 창 알림 일수. KPI 카드와 같은 산정식을 쓴다."""
    if as_of is None:
        return {}
    cols = _relation_columns(conn, "gold_kpi_daily")
    metrics = [c[: -len("_status")] for c in cols if c.endswith("_status")]
    if not metrics:
        return {}
    select = ", ".join(f'"{m}_status"' for m in metrics)
    rows = conn.execute(
        f'SELECT {select} FROM gold_kpi_daily WHERE date <= ? ORDER BY date DESC LIMIT ?',
        (as_of, window_days),
    ).fetchall()
    out = {}
    for m in metrics:
        if m in al.NO_STATUS_METRICS:
            continue
        alert_days = sum(1 for r in rows if r[f"{m}_status"] in ALERT_STATUSES)
        out[m] = {"alert_days": alert_days, "node_state": node_state(alert_days)}
    return out


# --- 예보 -------------------------------------------------------------------

#: 코드화하는 확정 엣지 2건(BASE-001 구현 순서 5). **수치는 여기 없다** — 엣지 행에서 읽는다.
FORECAST_RULES: tuple[dict, ...] = (
    {
        "rule": "취소율 → 예약",
        "cause": "cancel_rate",
        "effect": "reservations",
        "title": "예약 위험",
        "trigger_metric": "cancel_rate",
        "trigger_text": "취소율이 경고 구간에 머무름",
    },
    {
        "rule": "강남언니 리뷰 → 신환",
        "cause": "gu_reviews",
        "effect": "new_patients",
        "title": "신환 위험",
        "trigger_metric": "gu_reviews",
        "trigger_grain": "weekly",
        "trigger_text": "유기 리뷰가 최근 구간에 거의 0",
    },
)


def forecast(conn: sqlite3.Connection, *, window_days: int = 30) -> dict:
    as_of = conn.execute("SELECT MAX(date) FROM gold_kpi_daily").fetchone()[0]
    out = []
    for rule in FORECAST_RULES:
        row = conn.execute(
            "SELECT * FROM ontology_edges WHERE cause = ? AND effect = ?",
            (rule["cause"], rule["effect"]),
        ).fetchone()
        if row is None:
            continue  # 엣지가 없으면 예보도 없다 — 문장을 지어내지 않는다
        edge = _edge_payload(row)
        grain = rule.get("trigger_grain", "daily")
        evidence = _trigger_evidence(conn, rule["trigger_metric"], grain, as_of, window_days)
        risk = _risk(evidence.get("status"), edge["confidence"])
        item = {
            "rule": rule["rule"],
            "title": rule["title"],
            "message": _message(rule, edge, evidence),
            "edge": {
                "edge_id": edge["edge_id"], "from": edge["from"], "to": edge["to"],
                "verdict": edge["verdict"], "sign": edge["sign"],
                "lag": edge["lag"], "lag_days": edge["lag_days"],
                "confidence": edge["confidence"], "evidence": edge["evidence"],
            },
            "trigger": rule["trigger_text"],
            "target": rule["effect"],
            # `horizon` 은 **일 단위**다(SPEC-003 §4 예시 `"0d"`·`"14d"`) — 정본 원형을
            # 그대로 흘리는 `lag`(`"2w"`)와 다른 필드다. `lag_days` 에서 만든다.
            "horizon": f"{edge['lag_days']}d" if edge["lag_days"] is not None else "0d",
            "risk": risk,
            "evidence": [evidence["payload"]] if evidence.get("payload") else [],
        }
        if edge["confidence"] == "낮음":
            n = _sample_note(edge["evidence"])
            item["note"] = f"신뢰도 낮음{n} — 단독 근거로 쓰지 않는다"
        out.append(item)
    return {"as_of": as_of, "forecasts": out}


def _sample_note(evidence: str | None) -> str:
    if evidence and "n=" in evidence:
        n = evidence.split("n=", 1)[1].split()[0].strip(")·,")
        return f"(표본 {n})"
    return ""


def _trigger_evidence(
    conn: sqlite3.Connection, metric: str, grain: str, as_of: str, window_days: int
) -> dict:
    relation = al.GRAIN_RELATION[grain]
    cols = _relation_columns(conn, relation)
    if metric not in cols:
        return {}
    key = al.GRAIN_KEY[grain]
    start = (
        datetime.date.fromisoformat(as_of) - datetime.timedelta(days=window_days)
    ).isoformat()
    lo = start[:7] if key in ("month", "cohort_month") else start
    hi = as_of[:7] if key in ("month", "cohort_month") else as_of
    status_col = f"{metric}_status"
    select = f'"{key}", "{metric}"' + (f', "{status_col}"' if status_col in cols else "")
    rows = conn.execute(
        f'SELECT {select} FROM {relation} WHERE "{key}" >= ? AND "{key}" <= ? ORDER BY "{key}"',
        (lo, hi),
    ).fetchall()
    if not rows:
        return {}
    values = [r[metric] for r in rows if r[metric] is not None]
    if not values:
        return {}
    avg = sum(values) / len(values)
    status = rows[-1][status_col] if status_col in cols else None
    return {
        "status": status,
        "payload": {
            "metric": metric,
            "value": round(avg, 4),
            "period": {"start": rows[0][key], "end": rows[-1][key]},
        },
    }


def _risk(status: str | None, confidence: str | None) -> str:
    """트리거 지표의 상태와 엣지 신뢰도를 함께 본다(SPEC-003 OQ-6)."""
    if status == "경고":
        return "알림"
    if status == "주의":
        return "관찰" if confidence == "낮음" else "알림"
    if confidence == "낮음":
        return "알림"
    return "관찰"


def _message(rule: dict, edge: dict, evidence: dict) -> str:
    """서버가 만드는 카피 — 근거 추적 앱이라 문장을 FE 에 흩지 않는다."""
    cause_label = glossary.label_of(edge["from"])
    effect_label = glossary.label_of(edge["to"])
    # 시차 0 이면 시점 구절을 아예 넣지 않는다 — SPEC-003 §4 예시 문장도 그렇다.
    # 「동시점」 같은 표현을 만들지 않는 편이 lag 재서술 금지 규율과도 결이 맞는다.
    days = edge["lag_days"] or 0
    horizon = "" if days == 0 else f"{days}일 뒤 "

    payload = evidence.get("payload") or {}
    value = payload.get("value")
    unit, fmt = glossary.unit_of(edge["from"])
    if fmt == "percent" and value is not None:
        shown = f"{value:.1%}"
    elif value is not None:
        shown = f"{value:,.1f}{unit or ''}" if isinstance(value, float) else f"{value}{unit or ''}"
    else:
        shown = None
    # 조사(이/가) 문제를 피하려고 주어를 명사구로 둔다 — 「취소율이(가)」 같은 자국을 남기지 않는다
    head = (f"최근 구간 {cause_label} 평균은 {shown}입니다"
            if shown is not None else f"최근 구간 {cause_label}를 봅니다")

    # 부호와 무관하게 **결과 쪽 하락**이 위험 신호다 — 양(+)이면 원인 감소가, 음(−)이면
    # 원인 증가가 하락을 부른다. 트리거 문구가 그 방향을 이미 담고 있다.
    return (
        f"{head}. 채택 엣지 「{cause_label} → {effect_label} ({edge['sign'] or '?'})」 기준으로 "
        f"{horizon}{effect_label} 하락이 예상됩니다."
    )
