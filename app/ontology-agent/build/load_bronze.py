"""브론즈 적재 — 원천 3종 → `bronze_*` 16테이블. **원형 그대로, 값 변환 없음.**

원형 보존이 이 제품의 근거 추적 전체를 떠받친다. 적재기는 컬럼을 지우지도 값을 고치지도
않는다 — 형식 표준화조차 실버의 몫이다.

게이트 1(행수 대사)은 적재와 같은 트랜잭션 안에서 돈다. 한 테이블이라도 어긋나면
롤백해 **부분 적재를 남기지 않는다**(SPEC-001 S-1.3).
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

from config import sources_for

from .errors import BronzeRowcountMismatch
from db.connection import atomic
from db.schema import (
    NEXUS_COLUMNS,
    REVIEW_HEADER_MAP,
    VEGAS_COLUMNS,
    bootstrap,
)

# 리뷰 CSV 는 셀 안에 개행이 있어 `wc -l` 로 세면 2,118 이 나온다.
# 대사는 **csv 파서 기준**으로만 한다(SPEC-001 §4 부기).
csv.field_size_limit(10_000_000)


def _insert_many(conn: sqlite3.Connection, table: str, columns: list[str], rows: list[tuple]) -> None:
    placeholders = ",".join("?" * len(columns))
    cols = ",".join(f'"{c}"' for c in columns)
    conn.executemany(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", rows)


def read_vegas(vegas_dir: Path) -> list[dict]:
    """일별 JSON 을 파일명 순으로 읽는다. 결측일(2026-02-17)은 파일이 없어 행이 생기지 않는다."""
    rows: list[dict] = []
    for fp in sorted(vegas_dir.glob("2026*.json")):
        with open(fp, encoding="utf-8") as f:
            rows.extend(json.load(f))
    return rows


def read_reviews(csv_path: Path) -> list[dict]:
    with open(csv_path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_nexus(nexus_dir: Path, name: str) -> list[dict]:
    with open(nexus_dir / f"{name}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load(conn: sqlite3.Connection, *, data_dir: Path | None = None) -> dict[str, tuple[int, int]]:
    """원천 → 브론즈 적재 + 게이트 1. 반환은 테이블별 (원본 행수, 적재 행수).

    실패 시 롤백하고 `BRONZE_ROWCOUNT_MISMATCH` 를 던진다.
    """
    src = sources_for(data_dir)
    bootstrap(conn)
    recon: dict[str, tuple[int, int]] = {}

    with atomic(conn, "bronze"):
        # --- vegas (원천 JSON — 타입이 원형에 포함된다) ---
        vegas_cols = [c for c, _ in VEGAS_COLUMNS]
        vegas_rows = read_vegas(src.vegas_dir)
        conn.execute("DELETE FROM bronze_vegas_reservations")
        _insert_many(
            conn, "bronze_vegas_reservations", vegas_cols,
            [tuple(r[c] for c in vegas_cols) for r in vegas_rows],
        )
        recon["bronze_vegas_reservations"] = (len(vegas_rows), _count(conn, "bronze_vegas_reservations"))

        # --- 리뷰 CSV (한글 헤더 → 브론즈 식별자. 값은 그대로) ---
        review_rows = read_reviews(src.reviews_csv)
        review_cols = [c for _, c in REVIEW_HEADER_MAP]
        conn.execute("DELETE FROM bronze_reviews")
        _insert_many(
            conn, "bronze_reviews", review_cols,
            [tuple(r[src] for src, _ in REVIEW_HEADER_MAP) for r in review_rows],
        )
        recon["bronze_reviews"] = (len(review_rows), _count(conn, "bronze_reviews"))

        # --- nexus 14종 ---
        for name, cols in NEXUS_COLUMNS.items():
            table = f"bronze_nexus_{name}"
            rows = read_nexus(src.nexus_dir, name)
            conn.execute(f"DELETE FROM {table}")
            _insert_many(conn, table, cols, [tuple(r[c] for c in cols) for r in rows])
            recon[table] = (len(rows), _count(conn, table))

        # --- 게이트 1 — 원본 행수 = 테이블 행수, 전 테이블 오차 0 ---
        mismatched = [
            f"{t}: 원본 {src:,} vs 적재 {got:,} (오차 {got - src:+,})"
            for t, (src, got) in recon.items() if src != got
        ]
        if mismatched:
            raise BronzeRowcountMismatch(
                f"행수 대사 불일치 {len(mismatched)}건 — 부분 적재를 남기지 않고 중단한다",
                mismatched,
            )

    return recon


def _count(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def gate1(conn: sqlite3.Connection, *, data_dir: Path | None = None) -> dict[str, tuple[int, int]]:
    """게이트 1 단독 재실행 — 원천을 다시 세어 적재본과 대조한다(WORK-005 가 쓴다)."""
    src = sources_for(data_dir)

    recon = {
        "bronze_vegas_reservations": (
            len(read_vegas(src.vegas_dir)), _count(conn, "bronze_vegas_reservations"),
        ),
        "bronze_reviews": (len(read_reviews(src.reviews_csv)), _count(conn, "bronze_reviews")),
    }
    for name in NEXUS_COLUMNS:
        table = f"bronze_nexus_{name}"
        recon[table] = (len(read_nexus(src.nexus_dir, name)), _count(conn, table))

    mismatched = [
        f"{t}: 원본 {src:,} vs 적재 {got:,} (오차 {got - src:+,})"
        for t, (src, got) in recon.items() if src != got
    ]
    if mismatched:
        raise BronzeRowcountMismatch(f"행수 대사 불일치 {len(mismatched)}건", mismatched)
    return recon


def report(recon: dict[str, tuple[int, int]], stream=sys.stdout) -> None:
    """대사표 — 행수만 찍는다. PII 원값을 로그에 남기지 않는다."""
    print("게이트 1 — 브론즈 행수 대사", file=stream)
    for table, (src, got) in recon.items():
        mark = "OK" if src == got else "MISMATCH"
        print(f"  {table:<52} 원본 {src:>7,} = 적재 {got:>7,}  {mark}", file=stream)
    print(f"  전 {len(recon)}테이블 오차 0 — 통과", file=stream)
