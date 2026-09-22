"""골드 빌드 — 실버만 읽어 `gold_*` 5종을 만든다.

`reference/ontology_demo/scripts/build_gold.py` 이식이다. 계산식·파생·상태 경계는 기록 05
그대로이고 입출력만 파일 → DB 로 갈았다.

`gold_kpi_monthly` 만 신설이다(SPEC-001 2026-09-02 확정). 기록 05 가 월 View 를 명세하지
않았으므로 **일별에서 집계한다는 것 외에 새 정의를 만들지 않는다** — 지표 목록·계산식은
`gold_kpi_daily` 의 것을, 집계 방식은 주별(`gold_kpi_weekly`)의 것을 그대로 쓴다.
"""

from __future__ import annotations

import datetime
import sqlite3
from collections import defaultdict

from db.connection import atomic

NAVER_START = "2026-03-21"

# 지표와 나쁜 방향 (low = 낮을수록 나쁨, high = 높을수록 나쁨, None = 상태 없음)
METRICS = [
    ("sales_total", "low"), ("payment_visits", "low"), ("avg_ticket", "low"),
    ("visits", "low"), ("new_patients", "low"), ("revisits", "low"),
    ("reservations", "low"), ("cancels", "high"), ("cancel_rate", "high"),
    ("noshows", "high"), ("noshow_rate", "high"), ("new_churns", "high"),
    ("naver_reviews", None),  # 개입 신호 — 방향이 없어 상태 미부여
    ("new_patients_domestic", "low"),   # 개정 4
    ("foreign_sales_share", "high"),    # 개정 4
]

# 계수형 — 주별·월별에서 그대로 합산한다.
COUNT_METRICS = ["sales_total", "payment_visits", "visits", "new_patients", "revisits",
                 "reservations", "cancels", "noshows", "new_churns"]
# 월별에만 추가로 굴리는 분리 원천(개정 3) — 일별에 있으므로 월 합계도 갖는다.
MONTHLY_EXTRA_COUNTS = ["sales_foreign_est", "visits_foreign_est", "new_patients_foreign_est",
                        "new_patients_domestic"]


def _rows(conn: sqlite3.Connection, table: str) -> list[dict]:
    return [dict(r) for r in conn.execute(f"SELECT * FROM {table}")]


# --- gold_kpi_daily -------------------------------------------------------


def build_daily(resv: list[dict], reviews: list[dict]) -> list[dict]:
    days: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in resv:
        d = days[r["resv_date"]]
        if not r["sales_exception_flag"]:
            d["sales_total"] += r["sales"]
        if r["is_payment_visit"]:
            d["payment_visits"] += 1
        if r["visit_status"] == "내원":
            d["visits"] += 1
        if r["is_new"]:
            d["new_patients"] += 1
        if r["is_revisit"]:
            d["revisits"] += 1
        d["reservations"] += 1
        if r["visit_status"] == "취소":
            d["cancels"] += 1
        if r["visit_status"] == "부도":
            d["noshows"] += 1
        if r["is_new_churn"]:
            d["new_churns"] += 1
        if r["is_foreign_est"]:  # 개정 3 — 외국인 추정 분리
            if not r["sales_exception_flag"]:
                d["sales_foreign_est"] += r["sales"]
            if r["visit_status"] == "내원":
                d["visits_foreign_est"] += 1
            if r["is_new"]:
                d["new_patients_foreign_est"] += 1

    naver: dict[str, int] = defaultdict(int)
    for r in reviews:
        if r["platform"] == "네이버 플레이스":
            naver[r["review_date"]] += 1

    rows = []
    for date in sorted(days):
        d = days[date]
        row: dict = {"date": date}
        for m, _ in METRICS:
            row[m] = d.get(m, 0)
        row["avg_ticket"] = round(d["sales_total"] / d["payment_visits"]) if d["payment_visits"] else ""
        row["cancel_rate"] = round(d["cancels"] / d["reservations"], 4) if d["reservations"] else ""
        denom = d["visits"] + d["noshows"]
        row["noshow_rate"] = round(d["noshows"] / denom, 4) if denom else ""
        # 관측 개시 이전은 0 이 아니라 빈 값(기록 05 승인 4)
        row["naver_reviews"] = naver.get(date, 0) if date >= NAVER_START else ""
        for k in ["sales_foreign_est", "visits_foreign_est", "new_patients_foreign_est"]:
            row[k] = d.get(k, 0)
        row["new_patients_domestic"] = d.get("new_patients", 0) - d.get("new_patients_foreign_est", 0)
        row["foreign_sales_share"] = (round(d.get("sales_foreign_est", 0) / d["sales_total"], 4)
                                      if d.get("sales_total") else "")
        rows.append(row)
    return rows


def add_derived(rows: list[dict]) -> tuple[list[dict], dict[str, tuple]]:
    """직전 존재 행 기준 dod/dod_pct/ma7 + 전 기간 백분위 상태(기록 05 승인 1·3)."""
    bounds: dict[str, tuple] = {}
    for m, bad in METRICS:
        series = [r[m] for r in rows]
        for i, r in enumerate(rows):
            cur = r[m]
            prev = rows[i - 1][m] if i > 0 else ""
            if cur == "" or prev == "":
                r[f"{m}_dod"] = r[f"{m}_dod_pct"] = ""
            else:
                r[f"{m}_dod"] = round(cur - prev, 4)
                r[f"{m}_dod_pct"] = round((cur - prev) / prev, 4) if prev else ""
            window = [v for v in series[max(0, i - 6):i + 1] if v != ""]
            r[f"{m}_ma7"] = round(sum(window) / len(window), 2) if window else ""
        if bad is None:
            continue
        vals = sorted(v for v in series if v != "")
        if not vals:
            continue

        def pct(p: float, _vals=vals) -> float:
            return _vals[min(len(_vals) - 1, int(len(_vals) * p))]

        if bad == "low":
            warn, alert = pct(0.25), pct(0.10)

            def judge(v, _w=warn, _a=alert):
                return "경고" if v <= _a else ("주의" if v <= _w else "양호")
        else:
            warn, alert = pct(0.75), pct(0.90)

            def judge(v, _w=warn, _a=alert):
                return "경고" if v >= _a else ("주의" if v >= _w else "양호")

        for r in rows:
            r[f"{m}_status"] = judge(r[m]) if r[m] != "" else ""
        bounds[m] = (bad, warn, alert)
    return rows, bounds


# --- gold_kpi_weekly ------------------------------------------------------


def build_weekly(daily: list[dict], reviews: list[dict]) -> list[dict]:
    weeks: dict[tuple, dict] = defaultdict(lambda: defaultdict(int))
    meta: dict[tuple, str] = {}
    for r in daily:
        d = datetime.date.fromisoformat(r["date"])
        iso = d.isocalendar()
        key = (iso[0], iso[1])
        w = weeks[key]
        for m in COUNT_METRICS:
            w[m] += r[m]
        if r["naver_reviews"] != "":
            w["naver_reviews"] += r["naver_reviews"]
            w["_naver_obs"] = 1
        w["_days"] = w.get("_days", 0) + 1
        meta.setdefault(key, (d - datetime.timedelta(days=d.weekday())).isoformat())

    # 유기 신호 — 강남언니만. 리뷰 없는 주의 0 은 결측이 아니라 실제 0 (기록 03 1장)
    gu: dict[tuple, dict] = defaultdict(lambda: {"gu_reviews": 0, "gu_positive": 0, "gu_negative": 0})
    win_min, win_max = daily[0]["date"], daily[-1]["date"]
    for r in reviews:
        if r["platform"] != "강남언니" or not (win_min <= r["review_date"] <= win_max):
            continue
        d = datetime.date.fromisoformat(r["review_date"])
        iso = d.isocalendar()
        g = gu[(iso[0], iso[1])]
        g["gu_reviews"] += 1
        if r["sentiment"] == "긍정":
            g["gu_positive"] += 1
        elif r["sentiment"] == "부정":
            g["gu_negative"] += 1

    rows = []
    for key in sorted(weeks):
        w = weeks[key]
        row = {"iso_year": key[0], "iso_week": key[1], "week_start": meta[key],
               "is_partial_week": int(w["_days"] < 7)}
        for m in COUNT_METRICS:
            row[m] = w[m]
        # 비율형은 일별 평균이 아니라 주 합계에서 재계산 (기록 05 3.2)
        row["avg_ticket"] = round(w["sales_total"] / w["payment_visits"]) if w["payment_visits"] else ""
        row["cancel_rate"] = round(w["cancels"] / w["reservations"], 4) if w["reservations"] else ""
        denom = w["visits"] + w["noshows"]
        row["noshow_rate"] = round(w["noshows"] / denom, 4) if denom else ""
        row["naver_reviews"] = w["naver_reviews"] if w.get("_naver_obs") else ""
        row.update(gu.get(key, {"gu_reviews": 0, "gu_positive": 0, "gu_negative": 0}))
        rows.append(row)
    return rows


# --- gold_kpi_monthly (신설) ----------------------------------------------


def _days_in_month(year: int, month: int) -> int:
    nxt = datetime.date(year + month // 12, month % 12 + 1, 1)
    return (nxt - datetime.date(year, month, 1)).days


def build_monthly(daily: list[dict]) -> list[dict]:
    """달력 월 1행. 계수형은 월 합계, **비율형은 월 합계에서 재계산**(주별과 같은 규칙).

    부분 월 플래그는 주별의 `is_partial_week` 와 같은 기준이다 — 그 달의 달력일수만큼
    일별 행이 존재하지 않으면 부분 월이다. 기간 경계가 걸린 달(2026-01·2026-08)과
    결측일이 있는 달(2026-02)이 여기 걸린다.
    """
    months: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    metrics = COUNT_METRICS + MONTHLY_EXTRA_COUNTS
    for r in daily:
        m = months[r["date"][:7]]
        for k in metrics:
            m[k] += r[k]
        if r["naver_reviews"] != "":
            m["naver_reviews"] += r["naver_reviews"]
            m["_naver_obs"] = 1
        m["_days"] = m.get("_days", 0) + 1

    rows = []
    for key in sorted(months):
        mo = months[key]
        year, month = int(key[:4]), int(key[5:])
        row: dict = {"month": key, "month_start": f"{key}-01",
                     "is_partial_month": int(mo["_days"] < _days_in_month(year, month)),
                     "days_observed": mo["_days"]}
        for k in metrics:
            row[k] = mo[k]
        row["avg_ticket"] = round(mo["sales_total"] / mo["payment_visits"]) if mo["payment_visits"] else ""
        row["cancel_rate"] = round(mo["cancels"] / mo["reservations"], 4) if mo["reservations"] else ""
        denom = mo["visits"] + mo["noshows"]
        row["noshow_rate"] = round(mo["noshows"] / denom, 4) if denom else ""
        row["foreign_sales_share"] = (round(mo["sales_foreign_est"] / mo["sales_total"], 4)
                                      if mo["sales_total"] else "")
        row["naver_reviews"] = mo["naver_reviews"] if mo.get("_naver_obs") else ""
        rows.append(row)
    return rows


# --- gold_promo_calendar --------------------------------------------------


def build_promo(conn: sqlite3.Connection, promos: list[dict]) -> list[dict]:
    """프로모션 1건 = 이벤트 1행(생존만). 「일별 활성 개수」류 컬럼을 만들지 않는다."""
    mappings = _rows(conn, "silver_mappings")
    catalog = _rows(conn, "silver_catalog")
    prod_price = {}
    for c in catalog:
        if (c["entity_type"] == "product" and c["line_type"] == "event"
                and not c["is_deleted"] and c["regular_price"] and c["discounted_price"]
                and float(c["regular_price"]) > 0):
            prod_price[c["id"]] = (float(c["regular_price"]), float(c["discounted_price"]))
    g2p: dict[str, list[str]] = defaultdict(list)
    p2g: dict[str, list[str]] = defaultdict(list)
    for m in mappings:
        if m["map_type"] == "event_group_product":
            g2p[m["parent_id"]].append(m["child_id"])
        elif m["map_type"] == "promo_v2_event_group":
            p2g[m["parent_id"]].append(m["child_id"])

    # v2 구성 사슬(프로모 → 이벤트 그룹 → 상품)의 출발점. 실버가 원천 내부 id 를
    # `source_id` 로 보존하므로 **실버만 읽고** 이을 수 있다 — 골드는 브론즈를 읽지 않는다.
    v2rows = [p for p in promos if p["promo_version"] == "v2" and not p["is_deleted"]]
    comp = {}
    for r in v2rows:
        prices = []
        for gid in p2g.get(r["source_id"], []):
            for pid in g2p.get(gid, []):
                if pid in prod_price:
                    prices.append(prod_price[pid])
        if prices:
            discs = sorted(d for _, d in prices)
            rates = [1 - d / reg for reg, d in prices]
            comp[(r["code"], r["benefit_start"])] = {
                "n_products": len(prices),
                "avg_discount_rate": round(sum(rates) / len(rates), 3),
                "avg_discounted_price": round(sum(discs) / len(discs)),
                "median_discounted_price": round(discs[len(discs) // 2]),
            }

    rows = []
    for p in promos:
        if p["is_deleted"]:
            continue
        row = {"promo_version": p["promo_version"], "code": p["code"], "title": p["title"],
               "benefit_start": p["benefit_start"], "benefit_end": p["benefit_end"],
               "display_start": p["display_start"], "display_end": p["display_end"],
               "n_products": "", "avg_discount_rate": "", "avg_discounted_price": "",
               "median_discounted_price": ""}
        if p["promo_version"] == "v2":
            c = comp.get((p["code"], p["benefit_start"]))
            if c:
                row.update(c)
        rows.append(row)
    return rows


# --- gold_retention_monthly -----------------------------------------------


def build_retention(resv: list[dict]) -> list[dict]:
    """월 신환 코호트 재방문 전환율(60일) + 외국인 추정 분해 (기록 05 4b · 개정 2·3)."""
    first: dict[str, str] = {}
    foreign: set[str] = set()
    for r in resv:
        if r["is_new"] and r["chart_no"]:
            first.setdefault(r["chart_no"], r["resv_date"])
            if r["is_foreign_est"]:
                foreign.add(r["chart_no"])
    ret: set[str] = set()
    for r in resv:
        cn = r["chart_no"]
        if cn in first and r["is_revisit"]:
            d0 = datetime.date.fromisoformat(first[cn])
            d1 = datetime.date.fromisoformat(r["resv_date"])
            if 0 < (d1 - d0).days <= 60:
                ret.add(cn)
    # 관찰 창의 끝 = 데이터의 마지막 예약일. 원본은 2026-08-30 을 상수로 박았는데
    # (`build_gold.py:252`) 창이 늘면 `is_partial_cohort` 가 조용히 틀린다 — 값은 같고
    # 규칙 재해석이 아니므로 데이터에서 유도한다.
    END = datetime.date.fromisoformat(max(r["resv_date"] for r in resv))
    coh: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for cn, d in first.items():
        c = coh[d[:7]]
        c[0] += 1
        if cn in ret:
            c[1] += 1
        if cn not in foreign:
            c[2] += 1
            if cn in ret:
                c[3] += 1
    rows = []
    for m in sorted(coh):
        size, kept, dsize, dkept = coh[m]
        y, mo = int(m[:4]), int(m[5:])
        month_end = datetime.date(y + mo // 12, mo % 12 + 1, 1) - datetime.timedelta(days=1)
        partial = (END - month_end).days < 60  # 월말 신환까지 60일 관찰 미확보
        rows.append({"cohort_month": m, "cohort_size": size, "retained_60d": kept,
                     "retention_rate": round(kept / size, 3) if size else "",
                     "domestic_cohort_size": dsize, "domestic_retained_60d": dkept,
                     "domestic_retention_rate": round(dkept / dsize, 3) if dsize else "",
                     "foreign_est_share": round((size - dsize) / size, 3) if size else "",
                     "is_partial_cohort": int(partial)})
    return rows


# --- 산출 ------------------------------------------------------------------


def write_table(conn: sqlite3.Connection, table: str, rows: list[dict]) -> int:
    """지표 × 파생으로 컬럼이 불어나므로 산출 행에서 DDL 을 만든다.

    타입 선언을 비워 SQLite 의 동적 타입을 그대로 쓴다 — 파이썬 값이 왜곡 없이 들어간다.
    빈 값 sentinel `""` 는 NULL 로 내린다(「관측 없음」과 「0」의 구분을 유지).
    """
    cols = list(rows[0].keys())
    conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.execute(f"CREATE TABLE {table} (" + ", ".join(f'"{c}"' for c in cols) + ")")
    conn.executemany(
        f"INSERT INTO {table} VALUES (" + ",".join("?" * len(cols)) + ")",
        [tuple(None if r[c] == "" else r[c] for c in cols) for r in rows],
    )
    return len(rows)


def build(conn: sqlite3.Connection) -> dict:
    resv = _rows(conn, "silver_reservations")
    reviews = _rows(conn, "silver_reviews")
    promos = _rows(conn, "silver_promotions")

    daily, bounds = add_derived(build_daily(resv, reviews))
    weekly = build_weekly(daily, reviews)
    monthly = build_monthly(daily)
    promo = build_promo(conn, promos)
    retention = build_retention(resv)

    with atomic(conn, "gold"):
        counts = {
            "gold_kpi_daily": write_table(conn, "gold_kpi_daily", daily),
            "gold_kpi_weekly": write_table(conn, "gold_kpi_weekly", weekly),
            "gold_kpi_monthly": write_table(conn, "gold_kpi_monthly", monthly),
            "gold_promo_calendar": write_table(conn, "gold_promo_calendar", promo),
            "gold_retention_monthly": write_table(conn, "gold_retention_monthly", retention),
        }
    return {"counts": counts, "status_bounds": bounds}
