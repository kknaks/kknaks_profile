"""P3 — 마스킹 뷰와 표기 형식. SPEC-001 AC-7 (게이트 3).

**이 파일에 PII 원값을 쓰지 않는다.** 표기 검증은 합성 표본으로 하고, 실데이터 검증은
「원값이 나오지 않는다」는 부정 명제로만 한다.
"""

from __future__ import annotations

import sqlite3

import pytest

from build import gates, masking
from build.errors import PiiLeak
from tests.conftest import requires_source

PII_COLUMNS = ("patientName", "phone", "birthday")


def _mask(expr_sql: str, value: str) -> str:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (c TEXT)")
    conn.execute("INSERT INTO t VALUES (?)", (value,))
    return conn.execute(f"SELECT {expr_sql} FROM t").fetchone()[0]


@pytest.mark.parametrize("raw, masked", [
    ("홍길동", "홍○○"),        # 성 1자만 노출
    ("남궁민수", "남○○○"),     # 복성도 규약대로 1자만
    ("김수", "김○"),
])
def test_이름_표기는_성_1자만_남긴다(raw, masked):
    assert _mask(masking.mask_name_sql("c"), raw) == masked


@pytest.mark.parametrize("raw, masked", [
    ("01012345678", "010-****-5678"),   # SPEC-001 표기 형식
    ("0212345678", "021-****-5678"),
    ("", ""),
    ("010", "***"),                     # 가운데가 없어 전체를 덮는다
])
def test_전화_표기는_앞_3자리와_뒤_4자리만_남긴다(raw, masked):
    assert _mask(masking.mask_phone_sql("c"), raw) == masked


@pytest.mark.parametrize("raw, masked", [
    ("19900101", "1990-**-**"),   # 연도만
    ("", ""),
])
def test_생년월일_표기는_연도만_남긴다(raw, masked):
    assert _mask(masking.mask_birthday_sql("c"), raw) == masked


def test_본문_마스킹은_긴_토큰부터_적용한다():
    """짧은 토큰이 먼저 먹으면 긴 이름이 조각나 남는다."""
    sql = masking.mask_body_sql("c", ["김민수", "민수"])
    assert _mask(sql, "김민수 실장님 감사합니다") == "[직원] 실장님 감사합니다"


@requires_source
def test_뷰_4종이_존재한다(built_db):
    views = {r[0] for r in built_db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'view'")}
    assert set(masking.VIEWS) <= views


@requires_source
def test_게이트3_뷰_산출에_원값_0건(built_db):
    result = gates.gate3(built_db)
    assert result["leaks"] == 0
    assert result["vegas_rows"] == 78_216
    assert result["review_rows"] == 1_962


@requires_source
def test_뷰_산출값이_원값_집합과_한_건도_겹치지_않는다(built_db):
    """AC-7 — 전수 대조. 마스킹이 한 행이라도 통과시키면 여기 걸린다."""
    for column in PII_COLUMNS:
        n = built_db.execute(f"""
            SELECT COUNT(*) FROM v_bronze_vegas_reservations v
            JOIN (SELECT DISTINCT "{column}" AS raw FROM bronze_vegas_reservations
                  WHERE "{column}" <> '') d ON v."{column}" = d.raw
        """).fetchone()[0]
        assert n == 0, f"{column} 원값이 뷰로 새어나온다"


@requires_source
def test_chart_no_는_마스킹하지_않는다(built_db):
    """기록 03 확정 — 내부 데모 범위에서 조인·검증 추적성을 우선한다."""
    same = built_db.execute("""
        SELECT COUNT(*) FROM v_bronze_vegas_reservations v
        JOIN (SELECT DISTINCT chartNo AS raw FROM bronze_vegas_reservations
              WHERE chartNo <> '') d ON v.chartNo = d.raw
    """).fetchone()[0]
    assert same > 0


@requires_source
def test_뷰가_authorName_을_대상으로_명시한다(built_db):
    """원천이 이미 마스킹 닉네임이라 값은 그대로지만, 컬럼은 뷰 목록에 남는다."""
    cols = [r[1] for r in built_db.execute("PRAGMA table_info(v_bronze_reviews)")]
    assert "authorName" in cols


@requires_source
def test_마스킹이_풀리면_PII_LEAK_로_실패한다(built_db):
    """뷰를 원 테이블 그대로 바꿔 끼우면 게이트 3 이 잡아야 한다."""
    built_db.execute("DROP VIEW v_bronze_vegas_reservations")
    built_db.execute(
        "CREATE VIEW v_bronze_vegas_reservations AS SELECT * FROM bronze_vegas_reservations")
    try:
        with pytest.raises(PiiLeak) as exc:
            gates.gate3(built_db)
        assert exc.value.code == "PII_LEAK"
    finally:
        masking.build(built_db)  # 세션 공유 픽스처를 원복한다
    assert gates.gate3(built_db)["leaks"] == 0
