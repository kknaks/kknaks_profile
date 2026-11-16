"""P4 — 실버·골드 빌드 이식과 월 View. SPEC-001 AC-3 · AC-4 · AC-5 · AC-6b."""

from __future__ import annotations

import sqlite3

import pytest

from build import gold, silver
from build.errors import EnumViolation, NegativeAmount
from build.spec_contract import REBUILD_ROWCOUNTS
from tests.conftest import requires_source


@requires_source
@pytest.mark.parametrize("table", [
    "silver_reservations", "silver_reviews", "silver_catalog",
    "silver_promotions", "silver_branch_alias", "silver_mappings",
    "gold_kpi_daily", "gold_kpi_weekly", "gold_promo_calendar",
])
def test_산출_행수가_기록_04_05_와_일치한다(built_db, table):
    got = built_db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    assert got == REBUILD_ROWCOUNTS[table]


@requires_source
def test_행수_대사_수식이_성립한다(built_db):
    """브론즈 = 실버 + 필터 제외 + 중복 제거 (기록 04 게이트 1)."""
    bronze = built_db.execute("SELECT COUNT(*) FROM bronze_vegas_reservations").fetchone()[0]
    silver_rows = built_db.execute("SELECT COUNT(*) FROM silver_reservations").fetchone()[0]
    assert bronze == 78_216
    assert silver_rows == 75_479
    assert bronze - silver_rows == 2_737  # 완전 동일 중복, 필터 제외 0


@requires_source
def test_AC3_전_일자에서_신환더하기재진이_총내원과_같다(built_db):
    bad = built_db.execute(
        "SELECT COUNT(*) FROM gold_kpi_daily WHERE new_patients + revisits <> visits"
    ).fetchone()[0]
    assert bad == 0
    assert built_db.execute("SELECT COUNT(*) FROM gold_kpi_daily").fetchone()[0] == 235


@requires_source
def test_결측일_행이_없다(built_db):
    n = built_db.execute(
        "SELECT COUNT(*) FROM gold_kpi_daily WHERE date = '2026-02-17'").fetchone()[0]
    assert n == 0


@requires_source
@pytest.mark.parametrize("metric", ["sales_total", "visits", "new_patients", "payment_visits",
                                    "revisits", "reservations", "cancels", "noshows"])
def test_AC4_주별_합계가_일별_합계와_같다(built_db, metric):
    daily = built_db.execute(f"SELECT SUM({metric}) FROM gold_kpi_daily").fetchone()[0]
    weekly = built_db.execute(f"SELECT SUM({metric}) FROM gold_kpi_weekly").fetchone()[0]
    assert weekly == daily


@requires_source
@pytest.mark.parametrize("metric", ["sales_total", "visits", "new_patients", "payment_visits",
                                    "revisits", "reservations", "cancels", "noshows"])
def test_AC6b_월별_합계가_일별_합계와_같다(built_db, metric):
    daily = built_db.execute(f"SELECT SUM({metric}) FROM gold_kpi_daily").fetchone()[0]
    monthly = built_db.execute(f"SELECT SUM({metric}) FROM gold_kpi_monthly").fetchone()[0]
    assert monthly == daily


@requires_source
def test_AC6b_비율형은_월_합계에서_재계산한다(built_db):
    """일별 평균이 아니다 — 분모 크기를 무시하면 값이 뭉개진다(기록 05 3.2 준용)."""
    for row in built_db.execute(
        "SELECT month, sales_total, payment_visits, avg_ticket, cancels, reservations, "
        "cancel_rate, noshows, visits, noshow_rate FROM gold_kpi_monthly"
    ):
        assert row["avg_ticket"] == round(row["sales_total"] / row["payment_visits"])
        assert row["cancel_rate"] == round(row["cancels"] / row["reservations"], 4)
        assert row["noshow_rate"] == round(row["noshows"] / (row["visits"] + row["noshows"]), 4)


@requires_source
def test_AC6b_월_View_에_부분_월_플래그가_있다(built_db):
    rows = list(built_db.execute(
        "SELECT month, days_observed, is_partial_month FROM gold_kpi_monthly ORDER BY month"))
    assert len(rows) == 8
    # 기간 경계가 걸린 1월(01-07 시작)·8월(08-30 종료), 결측일이 있는 2월이 부분 월이다
    partial = {r["month"] for r in rows if r["is_partial_month"]}
    assert partial == {"2026-01", "2026-02", "2026-08"}


@requires_source
def test_월별_그레인이_달력_월_1행이다(built_db):
    months = [r[0] for r in built_db.execute("SELECT month FROM gold_kpi_monthly ORDER BY month")]
    assert months == sorted(set(months))
    assert months == ["2026-01", "2026-02", "2026-03", "2026-04",
                      "2026-05", "2026-06", "2026-07", "2026-08"]


@requires_source
def test_일별_활성_개수류_컬럼이_없다(built_db):
    """1차 폐기 원인 3 방어 — 프로모션은 이벤트 단위로만 산출한다."""
    banned = [r[1] for r in built_db.execute("PRAGMA table_info(gold_kpi_daily)")
              if "active" in r[1].lower()]
    assert banned == []


@requires_source
def test_개입_신호는_관측_개시_이전이_0_이_아니라_빈_값이다(built_db):
    """기록 05 승인 4 — 0 으로 두면 시차 상관에 가짜 계단이 생긴다."""
    before = built_db.execute(
        "SELECT COUNT(*) FROM gold_kpi_daily WHERE date < '2026-03-21' "
        "AND naver_reviews IS NOT NULL").fetchone()[0]
    assert before == 0
    after = built_db.execute(
        "SELECT COUNT(*) FROM gold_kpi_daily WHERE date >= '2026-03-21' "
        "AND naver_reviews IS NULL").fetchone()[0]
    assert after == 0


@requires_source
def test_개입_신호에는_상태_컬럼을_주지_않는다(built_db):
    """방향(좋음/나쁨)이 없는 개입 변수다(SPEC-001 §4)."""
    cols = [r[1] for r in built_db.execute("PRAGMA table_info(gold_kpi_daily)")]
    assert "naver_reviews_status" not in cols
    assert "sales_total_status" in cols


@requires_source
def test_AC5_enum_밖_visit_status_는_빌드를_중단시킨다(built_db):
    """오염 표본을 브론즈에 주입하면 실버 빌드가 실제로 멈춰야 한다(경고가 아니다)."""
    built_db.execute(
        "INSERT INTO bronze_vegas_reservations "
        "(branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        " sales, receipt, visitCount, visitStatus) "
        "VALUES ('세라미크의원 강남','20260301','TEST','합성표본','','','미지정',0,0,1,'노쇼')"
    )
    try:
        with pytest.raises(EnumViolation) as exc:
            silver.build_reservations(built_db)
        assert exc.value.code == "ENUM_VIOLATION"
    finally:
        built_db.rollback()


@requires_source
def test_AC5_음수_금액은_빌드를_중단시킨다(built_db):
    built_db.execute(
        "INSERT INTO bronze_vegas_reservations "
        "(branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        " sales, receipt, visitCount, visitStatus) "
        "VALUES ('세라미크의원 강남','20260301','TEST','합성표본','','','미지정',-1,0,1,'내원')"
    )
    try:
        with pytest.raises(NegativeAmount) as exc:
            silver.build_reservations(built_db)
        assert exc.value.code == "NEGATIVE_AMOUNT"
    finally:
        built_db.rollback()


@requires_source
def test_AC5_오염_표본에서_CLI_가_exit_1_로_끝난다(built_db, tmp_path):
    """게이트 실패는 exit code ≠ 0 이다(SPEC-001 Internal Interface Contract)."""
    from build.__main__ import main

    path = tmp_path / "tainted.db"
    target = sqlite3.connect(path)
    built_db.backup(target)
    target.execute(
        "INSERT INTO bronze_vegas_reservations "
        "(branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        " sales, receipt, visitCount, visitStatus) "
        "VALUES ('세라미크의원 강남','20260301','TEST','합성표본','','','미지정',0,0,1,'노쇼')"
    )
    target.commit()
    target.close()

    assert main(["silver", "--db", str(path)]) == 1


@requires_source
def test_실버에_PII_원값_컬럼이_없다(built_db):
    """patientName·phone 미반입, birthday 는 age_band 로만(기록 03 3장)."""
    cols = [r[1] for r in built_db.execute("PRAGMA table_info(silver_reservations)")]
    assert "patientName" not in cols
    assert "phone" not in cols
    assert "birthday" not in cols
    assert "age_band" in cols
    assert "is_foreign_est" in cols  # 판정은 브론즈, 실버는 플래그만


@requires_source
def test_실버_enum_이_허용값_안에_있다(built_db):
    statuses = {r[0] for r in built_db.execute(
        "SELECT DISTINCT visit_status FROM silver_reservations")}
    assert statuses <= {"내원", "취소", "부도"}
    sentiments = {r[0] for r in built_db.execute(
        "SELECT DISTINCT sentiment FROM silver_reviews")}
    assert sentiments <= {"긍정", "중립", "부정", "판정불가"}
    directions = {r[0] for r in built_db.execute(
        "SELECT DISTINCT outstanding_direction FROM silver_reservations")}
    assert directions <= {"미수", "수납 선행", ""}


@requires_source
def test_predicted_score_는_0_5_단위다(built_db):
    bad = built_db.execute(
        "SELECT COUNT(*) FROM silver_reviews WHERE predicted_score IS NOT NULL "
        "AND (predicted_score < 0.5 OR predicted_score > 5 "
        "     OR predicted_score * 2 <> CAST(predicted_score * 2 AS INTEGER))"
    ).fetchone()[0]
    assert bad == 0


@requires_source
def test_AC9_골드에서_실버_브론즈까지_드릴다운이_이어진다(built_db):
    """임의의 골드 KPI 값 1건 → 실버 행 집합 → 브론즈 원형 행."""
    day = built_db.execute(
        "SELECT date, payment_visits FROM gold_kpi_daily WHERE payment_visits > 0 LIMIT 1"
    ).fetchone()
    silver_rows = built_db.execute(
        "SELECT chart_no, resv_date FROM silver_reservations "
        "WHERE resv_date = ? AND is_payment_visit = 1", (day["date"],)
    ).fetchall()
    assert len(silver_rows) == day["payment_visits"]

    ymd = day["date"].replace("-", "")
    bronze_rows = built_db.execute(
        "SELECT COUNT(*) FROM v_bronze_vegas_reservations "
        "WHERE resvDate = ? AND chartNo = ?", (ymd, silver_rows[0]["chart_no"])
    ).fetchone()[0]
    assert bronze_rows >= 1  # 실버 행 → 브론즈 원형(마스킹 뷰 경유)


@requires_source
def test_리텐션_코호트_합이_실버_신환과_일치한다(built_db):
    coh = built_db.execute("SELECT SUM(cohort_size) FROM gold_retention_monthly").fetchone()[0]
    new = built_db.execute(
        "SELECT COUNT(DISTINCT chart_no) FROM silver_reservations "
        "WHERE is_new = 1 AND chart_no <> ''").fetchone()[0]
    assert coh == new
