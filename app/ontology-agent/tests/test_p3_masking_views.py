"""P3 — 마스킹 뷰와 표기 형식. SPEC-001 AC-7 (게이트 3).

**이 파일에 PII 원값을 쓰지 않는다.** 표기 검증은 합성 표본으로 하고, 실데이터 검증은
「원값이 나오지 않는다」는 부정 명제로만 한다.
"""

from __future__ import annotations

import sqlite3

import pytest

from build import gates, masking
from build.errors import PiiLeak
from build.masking import CHART_NO_TOKEN
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
def test_숫자_chart_no_는_마스킹하지_않는다(built_db):
    """기록 03 확정 — 내부 데모 범위에서 조인·검증 추적성을 우선한다.

    단, 그 추적성은 **숫자일 때만** 성립한다 — 아래 비정형 규칙이 그 예외다.
    """
    same = built_db.execute("""
        SELECT COUNT(*) FROM v_bronze_vegas_reservations v
        JOIN (SELECT DISTINCT chartNo AS raw FROM bronze_vegas_reservations
              WHERE chartNo <> '' AND chartNo NOT GLOB '*[^0-9]*') d ON v.chartNo = d.raw
    """).fetchone()[0]
    assert same > 0


@requires_source
def test_숫자가_아닌_chart_no_는_비정형_으로_덮인다(built_db):
    """WORK-005 — 차트번호 자리에 숫자가 아닌 것이 앉아 있으면 그건 차트번호가 아니다.

    실측 1건이 이름 문자열이었다. 무엇인지 모르는 값을 소비자 표면으로 내보내지 않는다.
    **브론즈 뷰와 실버 뷰 둘 다** 본다 — 한쪽만 덮으면 다른 쪽으로 같은 값이 샌다.
    """
    for view, column, source, raw_column in (
        ("v_bronze_vegas_reservations", "chartNo",
         "bronze_vegas_reservations", "chartNo"),
        ("v_silver_reservations", "chart_no", "silver_reservations", "chart_no"),
    ):
        polluted = built_db.execute(
            f"SELECT COUNT(*) FROM {source} "
            f"WHERE \"{raw_column}\" <> '' AND \"{raw_column}\" GLOB '*[^0-9]*'"
        ).fetchone()[0]
        assert polluted > 0, f"{source} 에 비정형 차트번호가 없다 — 회귀가 겨눌 과녁이 없다"

        # 뷰에는 원값이 없고, 같은 수만큼 토큰이 있다
        leaked = built_db.execute(
            f"SELECT COUNT(*) FROM {view} "
            f"WHERE \"{column}\" <> '' AND \"{column}\" <> ? "
            f"AND \"{column}\" GLOB '*[^0-9]*'", (CHART_NO_TOKEN,)).fetchone()[0]
        assert leaked == 0, f"{view}.{column} 로 비정형 원값이 {leaked}행 샌다"

        masked = built_db.execute(
            f"SELECT COUNT(*) FROM {view} WHERE \"{column}\" = ?",
            (CHART_NO_TOKEN,)).fetchone()[0]
        assert masked == polluted, f"{view}: 오염 {polluted}행인데 토큰 {masked}행"

    # 토큰은 길이도 남기지 않는다 — 길이가 곧 힌트다
    assert CHART_NO_TOKEN == "[비정형]"


@requires_source
def test_비정형_chart_no_가_남아_있으면_게이트3_가_막는다(built_db):
    """탐지만 하고 채택을 막지 못하면 게이트가 아니다 — 뷰를 원본으로 갈아 끼워 본다."""
    built_db.execute("DROP VIEW v_silver_reservations")
    built_db.execute(
        "CREATE VIEW v_silver_reservations AS SELECT * FROM silver_reservations")
    try:
        with pytest.raises(PiiLeak) as exc:
            gates.gate3(built_db)
        assert exc.value.code == "PII_LEAK"
        assert any("chart_no" in line for line in exc.value.detail), exc.value.detail
    finally:
        masking.build(built_db)   # 다음 테스트를 위해 되돌린다


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
