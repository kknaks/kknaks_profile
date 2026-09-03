"""게이트 2(빌드 재현)와 게이트 3(마스킹 뷰 PII).

게이트 1(브론즈 행수 대사)은 적재와 한 트랜잭션이라 `load_bronze` 가 갖는다.
전부 단독 재실행 가능하다 — WORK-005 전건 재실행이 이 인터페이스를 그대로 부른다.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from config import settings

from .errors import PiiLeak, RebuildMismatch
from .spec_contract import (
    BRONZE_VISITS,
    MISSING_DAY,
    REBUILD_ROWCOUNTS,
    REBUILD_TOTALS,
    VISIT_DEDUP_DELTA,
)


def _one(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> int:
    value = conn.execute(sql, params).fetchone()[0]
    return 0 if value is None else value


def gate2(conn: sqlite3.Connection) -> dict:
    """DB 기반 재빌드 산출물이 기존 CSV 산출물과 같은가 — 대조값 전항 일치 (AC-2)."""
    checks: list[tuple[str, int, int]] = [
        ("매출 합(예외 1건 제외)",
         _one(conn, "SELECT SUM(sales_total) FROM gold_kpi_daily"),
         REBUILD_TOTALS["매출 합(예외 1건 제외)"]),
        ("결제 내원",
         _one(conn, "SELECT SUM(payment_visits) FROM gold_kpi_daily"),
         REBUILD_TOTALS["결제 내원"]),
        ("신환",
         _one(conn, "SELECT SUM(new_patients) FROM gold_kpi_daily"),
         REBUILD_TOTALS["신환"]),
        ("총 내원(실버 기준)",
         _one(conn, "SELECT SUM(visits) FROM gold_kpi_daily"),
         REBUILD_TOTALS["총 내원(실버 기준)"]),
    ]
    for table, want in REBUILD_ROWCOUNTS.items():
        checks.append((f"{table} 행수", _one(conn, f"SELECT COUNT(*) FROM {table}"), want))

    # 실버 재집계와 골드가 같은가 — 대조값과 별개로 계층 간 일치도 본다
    checks.append((
        "실버 재집계 매출",
        _one(conn, "SELECT SUM(sales) FROM silver_reservations WHERE sales_exception_flag = 0"),
        REBUILD_TOTALS["매출 합(예외 1건 제외)"],
    ))
    # 브론즈 내원과의 대사 — 47,537 + 내원 중복 65 = 47,602
    checks.append((
        "브론즈 내원 대사(실버 + 내원 중복)",
        _one(conn, "SELECT SUM(visits) FROM gold_kpi_daily") + VISIT_DEDUP_DELTA,
        BRONZE_VISITS,
    ))
    # 주별·월별 합계 = 일별 합계 (AC-4 · AC-6b)
    for grain, table in (("주별", "gold_kpi_weekly"), ("월별", "gold_kpi_monthly")):
        for metric in ("sales_total", "visits", "new_patients", "payment_visits"):
            checks.append((
                f"{grain} {metric} 합 = 일별",
                _one(conn, f"SELECT SUM({metric}) FROM {table}"),
                _one(conn, f"SELECT SUM({metric}) FROM gold_kpi_daily"),
            ))

    failed = [f"{name}: 실측 {got:,} vs 기대 {want:,} (오차 {got - want:+,})"
              for name, got, want in checks if got != want]

    # 결측일 행 없음 (AC-2)
    if _one(conn, "SELECT COUNT(*) FROM gold_kpi_daily WHERE date = ?", (MISSING_DAY,)):
        failed.append(f"결측일 {MISSING_DAY} 행이 존재한다 (0 채움 금지)")
    # 전 일자 신환 + 재진 = 총 내원 (AC-3)
    bad_days = _one(
        conn,
        "SELECT COUNT(*) FROM gold_kpi_daily WHERE new_patients + revisits <> visits",
    )
    if bad_days:
        failed.append(f"신환 + 재진 ≠ 총 내원 인 일자 {bad_days}건 (기대 0)")
    # 「일별 활성 개수」류 파생 컬럼 금지 (기록 05 게이트 4)
    banned = [r[1] for r in conn.execute("PRAGMA table_info(gold_kpi_daily)")
              if "active" in r[1].lower()]
    if banned:
        failed.append(f"일별 활성 개수류 컬럼 {banned} (기대 0건)")

    if failed:
        raise RebuildMismatch(
            f"재현 대조 불일치 {len(failed)}건 — 산출물을 채택하지 않는다", failed)

    return {
        "checks": len(checks),
        "measured": {name: got for name, got, _ in checks},
        # OQ-3 — 기록에 행수가 없어 빌드 실측으로 확정한다
        "gold_kpi_monthly": _one(conn, "SELECT COUNT(*) FROM gold_kpi_monthly"),
        "gold_retention_monthly": _one(conn, "SELECT COUNT(*) FROM gold_retention_monthly"),
    }


# 기존 CSV 산출물 ↔ DB 테이블 짝 (게이트 2 의 「재빌드 = 기존 산출물」 대조)
CSV_PARITY_PAIRS: list[tuple[str, str]] = [
    ("silver/silver_reservations.csv", "silver_reservations"),
    ("silver/silver_reviews.csv", "silver_reviews"),
    ("silver/silver_catalog.csv", "silver_catalog"),
    ("silver/silver_promotions.csv", "silver_promotions"),
    ("silver/silver_mappings.csv", "silver_mappings"),
    ("silver/silver_branch_alias.csv", "silver_branch_alias"),
    ("gold/gold_kpi_daily.csv", "gold_kpi_daily"),
    ("gold/gold_kpi_weekly.csv", "gold_kpi_weekly"),
    ("gold/gold_promo_calendar.csv", "gold_promo_calendar"),
    ("gold/gold_retention_monthly.csv", "gold_retention_monthly"),
]


def _cell_equal(csv_value: str, db_value) -> bool:
    """CSV 문자열과 DB 값의 동치 — bool 표기(True/1)·수치 표기(5.0/5) 차이를 흡수한다."""
    if db_value is None:
        db_value = ""
    if isinstance(db_value, (int, float)) and not isinstance(db_value, bool):
        if csv_value in ("True", "False"):
            return (csv_value == "True") == bool(db_value)
        try:
            return float(csv_value) == float(db_value)
        except ValueError:
            return False
    return str(csv_value) == str(db_value)


def csv_parity(conn: sqlite3.Connection, *, data_dir: Path | None = None) -> dict:
    """DB 재빌드 산출물이 기존 CSV 산출물과 **셀 단위로** 같은가.

    게이트 2 의 대조값(합계·행수)보다 강한 검사다 — 합계가 맞아도 행 배치가 다를 수
    있으므로, 이식이 실제로 같은 산출을 내는지는 전 셀 대조로만 증명된다.
    기존 CSV 는 레포 밖 원천에 있으므로 이 검사는 원천이 있을 때만 돈다.
    """
    dd = data_dir or settings.data_dir
    failed: list[str] = []
    checked = 0
    for csv_name, table in CSV_PARITY_PAIRS:
        path = dd / csv_name
        if not path.exists():
            failed.append(f"{table}: 기존 산출물 없음 ({csv_name})")
            continue
        with open(path, encoding="utf-8") as f:
            ref = list(csv.DictReader(f))
        db = [dict(r) for r in conn.execute(f"SELECT * FROM {table}")]
        if len(ref) != len(db):
            failed.append(f"{table}: 행수 CSV {len(ref):,} vs DB {len(db):,}")
            continue
        cols = [c for c in ref[0] if c in db[0]]
        missing = [c for c in ref[0] if c not in db[0]]
        if missing:
            failed.append(f"{table}: DB 에 없는 컬럼 {missing}")
        # 불일치는 **위치만** 남긴다. 셀 원값을 찍으면 `silver_reservations.staff`(직원 실명)
        # 같은 값이 로그로 흘러나온다 — spec PII 목록 밖이라 위반은 아니나 경계가 어긋난다.
        diffs = [
            f"{table}[행 {i}].{c}"
            for i, (a, b) in enumerate(zip(ref, db))
            for c in cols if not _cell_equal(a[c], b[c])
        ]
        checked += len(db) * len(cols)
        if diffs:
            failed.append(f"{table}: 셀 불일치 {len(diffs):,}건 — 위치 예: {diffs[:3]}")

    if failed:
        raise RebuildMismatch(
            f"기존 CSV 산출물과 불일치 {len(failed)}건 — 산출물을 채택하지 않는다", failed)
    return {"tables": len(CSV_PARITY_PAIRS), "cells": checked, "diffs": 0}


def gate3(conn: sqlite3.Connection) -> dict:
    """마스킹 뷰 산출에 원값 검색 0건 (AC-7).

    뷰 4종을 전부 본다 — 브론즈 뷰 2종은 값을 전수 대조하고, 실버 뷰 2종은 애초에
    원값 컬럼이 없어야 하므로 **스키마**를 검사한다(실버 PII 미반입이 계약이다).
    로그에는 위반 **건수와 위치**만 남긴다 — 원값을 리포트에 쓰지 않는다.
    """
    leaks: list[str] = []
    for column in ("patientName", "phone", "birthday"):
        # 뷰 산출값이 **원값 집합의 어느 값과도 같지 않아야** 한다.
        # 뷰는 rowid 를 갖지 않으므로 행 짝짓기 대신 값 집합으로 대조한다 — 마스킹이
        # 한 행이라도 통과시키면 그 산출값이 원값 집합에 그대로 걸린다.
        n = _one(conn, f"""
            SELECT COUNT(*) FROM v_bronze_vegas_reservations v
            JOIN (
                SELECT DISTINCT "{column}" AS raw FROM bronze_vegas_reservations
                WHERE "{column}" <> '' AND "{column}" IS NOT NULL
            ) d ON v."{column}" = d.raw
        """)
        if n:
            leaks.append(f"v_bronze_vegas_reservations.{column}: 원값 노출 {n:,}행")
        # 원값이 마스킹 문자를 이미 갖고 있으면 위 대조가 무력해진다 — 전제 확인
        n = _one(conn, f"""
            SELECT COUNT(*) FROM bronze_vegas_reservations
            WHERE instr("{column}", '○') > 0 OR instr("{column}", '*') > 0
        """)
        if n:
            leaks.append(f"bronze_vegas_reservations.{column}: 원값에 마스킹 문자 포함 {n:,}행 "
                         "— 값 집합 대조의 전제가 깨진다")

    # 표기 형식 — 마스킹된 행이 규약 형식을 지키는가
    bad_name = _one(conn, """
        SELECT COUNT(*) FROM v_bronze_vegas_reservations
        WHERE patientName <> '' AND patientName NOT LIKE '_○%'
    """)
    if bad_name:
        leaks.append(f"이름 표기 규약(성 1자 + ○) 위반 {bad_name:,}행")
    bad_birthday = _one(conn, """
        SELECT COUNT(*) FROM v_bronze_vegas_reservations
        WHERE birthday <> '' AND birthday NOT LIKE '____-**-**'
    """)
    if bad_birthday:
        leaks.append(f"생년월일 표기 규약(연도만) 위반 {bad_birthday:,}행")
    bad_phone = _one(conn, """
        SELECT COUNT(*) FROM v_bronze_vegas_reservations
        WHERE phone <> '' AND phone NOT LIKE '%-****-%' AND phone NOT LIKE '%*%'
    """)
    if bad_phone:
        leaks.append(f"전화 표기 규약 위반 {bad_phone:,}행")

    # 리뷰 본문 — 실명 사전 잔존 0건
    from .masking import staff_names

    for name in staff_names(conn):
        n = _one(conn, "SELECT COUNT(*) FROM v_bronze_reviews WHERE instr(body, ?) > 0", (name,))
        if n:
            # 잔존한 실명은 로그에 남기지 않는다 — 건수만
            leaks.append(f"v_bronze_reviews.body: 직원 실명 토큰 잔존 {n:,}행")

    # 실버 뷰 2종 — 원값 컬럼이 아예 없어야 한다(기록 03 3장 미반입 규칙)
    for view in ("v_silver_reservations", "v_silver_reviews"):
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({view})")}
        exposed = cols & {"patientName", "phone", "birthday"}
        if exposed:
            leaks.append(f"{view}: 원값 컬럼 노출 {sorted(exposed)}")

    if leaks:
        raise PiiLeak(f"마스킹 뷰에서 원값 검출 {len(leaks)}건 — 배포 차단", leaks)

    return {
        "views_scanned": 4,          # 브론즈 2종 값 대조 + 실버 2종 스키마 검사
        "value_scanned_views": 2,
        "schema_checked_views": 2,
        "vegas_rows": _one(conn, "SELECT COUNT(*) FROM v_bronze_vegas_reservations"),
        "review_rows": _one(conn, "SELECT COUNT(*) FROM v_bronze_reviews"),
        "leaks": 0,
    }
