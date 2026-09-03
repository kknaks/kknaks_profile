"""P2 — 브론즈 적재와 **게이트 1**(행수 대사). SPEC-001 AC-1."""

from __future__ import annotations

import pytest

from build import load_bronze
from build.errors import BronzeRowcountMismatch
from tests.conftest import requires_source

# SPEC-001 §4 브론즈 표의 원본 행수. 전부 기록 02 실사값이다.
EXPECTED_ROWS = {
    "bronze_vegas_reservations": 78_216,
    "bronze_reviews": 1_962,   # csv 파서 기준 — wc -l 은 2,118 이 나온다
    "bronze_nexus_branches": 3,
    "bronze_nexus_categories": 157,
    "bronze_nexus_category_translations_ko": 128,
    "bronze_nexus_procedure_groups": 2_154,
    "bronze_nexus_procedure_products_ko": 2_996,
    "bronze_nexus_procedure_group_product_mappings": 5_632,
    "bronze_nexus_event_procedure_groups": 1_769,
    "bronze_nexus_event_procedure_products_ko": 2_179,
    "bronze_nexus_event_procedure_group_product_mappings": 3_199,
    "bronze_nexus_procedure_packages_ko": 323,
    "bronze_nexus_promotions_v1": 24,
    "bronze_nexus_promotion_v2s": 287,
    "bronze_nexus_promotion_v2_event_group_mappings": 858,
    "bronze_nexus_promotion_v2_group_mappings": 0,
}


@requires_source
def test_게이트1_전_테이블_오차_0(built_db):
    recon = load_bronze.gate1(built_db)
    assert set(recon) == set(EXPECTED_ROWS)
    for table, want in EXPECTED_ROWS.items():
        source_rows, loaded_rows = recon[table]
        assert source_rows == want, f"{table} 원본 행수가 SPEC-001 표와 다르다"
        assert loaded_rows == want, f"{table} 적재 행수 불일치"


@requires_source
def test_리뷰는_csv_파서_기준으로_센다(built_db):
    """셀 안에 개행이 있어 라인 수로 세면 2,118 이 나온다 — 파서 기준 1,962 여야 한다."""
    assert built_db.execute("SELECT COUNT(*) FROM bronze_reviews").fetchone()[0] == 1_962


@requires_source
def test_결측일_행이_생기지_않는다(built_db):
    """2026-02-17 은 원천 파일 자체가 없다 — 0 으로 채우지 않는다(기록 03)."""
    n = built_db.execute(
        "SELECT COUNT(*) FROM bronze_vegas_reservations WHERE resvDate = '20260217'"
    ).fetchone()[0]
    assert n == 0
    days = built_db.execute(
        "SELECT COUNT(DISTINCT resvDate) FROM bronze_vegas_reservations"
    ).fetchone()[0]
    assert days == 235


@requires_source
def test_원천이_모자라면_BRONZE_ROWCOUNT_MISMATCH_로_중단한다(built_db):
    """한 테이블에서 행을 지워 원천과 어긋나게 만들면 게이트 1 이 잡아야 한다."""
    built_db.execute("DELETE FROM bronze_nexus_branches WHERE rowid = 1")
    try:
        with pytest.raises(BronzeRowcountMismatch) as exc:
            load_bronze.gate1(built_db)
        assert exc.value.code == "BRONZE_ROWCOUNT_MISMATCH"
        assert any("bronze_nexus_branches" in d for d in exc.value.detail)
    finally:
        built_db.rollback()  # 세션 공유 픽스처를 원복한다
    assert built_db.execute("SELECT COUNT(*) FROM bronze_nexus_branches").fetchone()[0] == 3


@requires_source
def test_브론즈는_원형이다_값_변환이_없다(built_db):
    """resvDate 는 YYYYMMDD 원형 그대로 — 형식 표준화조차 실버의 몫이다."""
    row = built_db.execute(
        "SELECT resvDate, sales, visitCount FROM bronze_vegas_reservations LIMIT 1"
    ).fetchone()
    assert len(row["resvDate"]) == 8 and row["resvDate"].isdigit()
    # vegas 는 JSON 이라 숫자 타입이 원형에 포함된다
    assert isinstance(row["sales"], int)
    assert isinstance(row["visitCount"], int)
