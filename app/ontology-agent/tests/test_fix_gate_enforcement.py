"""검수 FAIL 3건의 회귀 테스트 — F1 계층 경계 · F2 이전 DB 유지 · F3 정합률 차단력.

게이트는 **탐지**가 아니라 **차단**이어야 한다. 이 파일은 세 건이 다시 풀리지 않도록
「실패를 주입하면 실제로 막히는가」를 고정한다.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from build import gates, gold, silver
from build.__main__ import main
from build.errors import AgreementBelowThreshold, RebuildMismatch
from config import settings
from tests.conftest import requires_source

BUILD_SRC = Path(__file__).resolve().parents[1] / "build"


# --- F1. 골드가 브론즈를 직접 읽지 않는다 --------------------------------


def test_F1_골드_소스에_브론즈_조회가_없다():
    """SPEC-001 §4 — 상위 계층은 바로 아래 계층만 읽는다. 사람 눈이 아니라 테스트로 고정한다."""
    source = (BUILD_SRC / "gold.py").read_text(encoding="utf-8")
    offenders = [
        line.strip() for line in source.splitlines()
        if "bronze_" in line and not line.lstrip().startswith("#")
    ]
    assert offenders == [], f"골드가 브론즈를 읽는다: {offenders}"


@requires_source
def test_F1_프로모션_구성이_실버_source_id_로_이어진다(built_db):
    """실버가 원천 내부 id 를 보존해야 골드가 브론즈 없이 구성 사슬을 잇는다."""
    filled = built_db.execute(
        "SELECT COUNT(*) FROM silver_promotions WHERE source_id IS NOT NULL AND source_id <> ''"
    ).fetchone()[0]
    assert filled == 73

    # 구성 특성 4컬럼이 실제로 채워졌는가 — source_id 가 끊기면 전부 NULL 이 된다
    composed = built_db.execute(
        "SELECT COUNT(*) FROM gold_promo_calendar WHERE n_products IS NOT NULL"
    ).fetchone()[0]
    assert composed > 0
    assert built_db.execute("SELECT COUNT(*) FROM gold_promo_calendar").fetchone()[0] == 57


@requires_source
def test_F1_수정_후에도_기존_CSV_산출물과_동일하다(built_db):
    """식별자 보존은 값을 바꾸지 않는다 — 이식 등가가 유지되는지 셀 단위로 확인한다."""
    assert gates.csv_parity(built_db)["diffs"] == 0


# --- F2. 게이트 실패 시 이전 DB 유지 --------------------------------------


def _daily_rows(path: Path) -> int:
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT COUNT(*) FROM gold_kpi_daily").fetchone()[0]
    finally:
        conn.close()


@pytest.fixture
def prior_db(tmp_path) -> Path:
    """정상 빌드 1회로 「이전 DB 상태」를 만든 뒤, 구분 가능한 표지를 남긴다.

    같은 원천에서 재빌드하면 결과가 같아 「유지됐는지 채택됐는지」를 가릴 수 없다.
    그래서 일별 테이블을 100행으로 깎아 둔다 — 롤백되면 100, 채택되면 235 다.
    """
    if not (settings.data_dir / "bronze" / "vegas").is_dir():
        pytest.skip("원천 데이터 없음")
    path = tmp_path / "prior.db"
    assert main(["all", "--db", str(path)]) == 0
    assert _daily_rows(path) == 235

    conn = sqlite3.connect(path)
    conn.execute("DELETE FROM gold_kpi_daily WHERE date NOT IN "
                 "(SELECT date FROM gold_kpi_daily ORDER BY date LIMIT 100)")
    conn.commit()
    conn.close()
    assert _daily_rows(path) == 100
    return path


@requires_source
def test_F2_게이트2_실패하면_이전_DB_가_그대로_남는다(prior_db, monkeypatch):
    """`REBUILD_MISMATCH` → 「산출물 미채택, 이전 DB 유지」(SPEC-001 Case Matrix)."""
    wrong = dict(gates.REBUILD_TOTALS)
    wrong["매출 합(예외 1건 제외)"] = 1  # 실측과 어긋나게 만들어 게이트 2 를 실패시킨다
    monkeypatch.setattr(gates, "REBUILD_TOTALS", wrong)

    assert main(["all", "--db", str(prior_db)]) == 1
    assert _daily_rows(prior_db) == 100, "게이트가 실패했는데 새 산출물이 채택됐다"


@requires_source
def test_F2_게이트3_실패하면_이전_DB_가_그대로_남는다(prior_db, monkeypatch):
    """`PII_LEAK` 도 같은 규율 — 게이트 실패는 채택을 막는다."""
    from build import masking

    original = masking.view_ddl  # 패치 전 원본을 잡아 둔다(자기 호출이면 무한 재귀다)

    def leaky_view_ddl(conn):
        # vegas 뷰만 마스킹 없는 원 테이블 통과로 바꿔 끼운다 → 게이트 3 이 잡아야 한다
        return [
            "DROP VIEW IF EXISTS v_bronze_vegas_reservations",
            "CREATE VIEW v_bronze_vegas_reservations AS "
            "SELECT * FROM bronze_vegas_reservations",
        ] + [s for s in original(conn) if "vegas" not in s]

    monkeypatch.setattr(masking, "view_ddl", leaky_view_ddl)

    assert main(["all", "--db", str(prior_db)]) == 1
    assert _daily_rows(prior_db) == 100


@requires_source
def test_F2_전건_통과하면_산출물이_채택된다(prior_db):
    """롤백만 하고 채택을 못 하면 그것대로 고장이다 — 반대 방향도 고정한다."""
    assert main(["all", "--db", str(prior_db)]) == 0
    assert _daily_rows(prior_db) == 235


@requires_source
def test_F2_실버_fail_fast_도_이전_상태를_남긴다(prior_db):
    """오염 표본으로 실버가 멈추면 골드까지 통째로 되감긴다."""
    conn = sqlite3.connect(prior_db)
    conn.execute(
        "INSERT INTO bronze_vegas_reservations "
        "(branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        " sales, receipt, visitCount, visitStatus) "
        "VALUES ('세라미크의원 강남','20260301','TEST','합성표본','','','미지정',0,0,1,'노쇼')"
    )
    conn.commit()
    conn.close()

    assert main(["silver", "--db", str(prior_db)]) == 1
    assert _daily_rows(prior_db) == 100


# --- F3. 강남언니 정합률 게이트의 차단력 ----------------------------------


@pytest.fixture
def low_agreement_scoring(tmp_path) -> Path:
    """정합률만 미달로 만드는 채점 산출물.

    실제 산출물에서 `predicted_score` 만 0.5 로 덮는다 — 근거 문장·개념은 그대로라
    다른 검증(근거 실존·폐쇄 목록)은 통과하고 **정합률만** 무너진다.
    """
    src = settings.data_dir / "silver" / "_scoring"
    if not src.is_dir():
        pytest.skip("채점 산출물 없음")
    dst = tmp_path / "_scoring"
    dst.mkdir()
    for fp in sorted(src.glob("output_batch_*.json")):
        items = json.loads(fp.read_text(encoding="utf-8"))
        for item in items:
            if item.get("predicted_score") is not None:
                item["predicted_score"] = 0.5
        (dst / fp.name).write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    return dst


@requires_source
def test_F3_정합률_미달이면_빌드가_중단된다(built_db, low_agreement_scoring):
    """이식 원본 `reviews_finalize.py:117` 의 `sys.exit(2)` 동등물이 살아 있는가."""
    with pytest.raises(AgreementBelowThreshold) as exc:
        silver.build_reviews(built_db, scoring_dir=low_agreement_scoring)
    assert exc.value.code == "AGREEMENT_BELOW_THRESHOLD"
    assert "정합률 미달" in exc.value.message
    built_db.rollback()


@requires_source
def test_F3_정합률_미달_표본에서_CLI_가_exit_1_로_끝난다(
    tmp_path, low_agreement_scoring, monkeypatch
):
    """출력만 하는 게이트는 게이트가 아니다 — exit code 로 막히는지 실증한다."""
    # 원천을 그대로 두고 채점 산출물만 바꿔 끼운 데이터 디렉토리를 만든다
    fake = tmp_path / "data"
    (fake / "silver").mkdir(parents=True)
    for name in ("bronze", "ontology"):
        (fake / name).symlink_to(settings.data_dir / name)
    for csv_file in settings.data_dir.glob("*.csv"):
        (fake / csv_file.name).symlink_to(csv_file)
    (fake / "silver" / "_scoring").symlink_to(low_agreement_scoring)
    monkeypatch.setattr(settings, "data_dir", fake)

    # `all` 로 돌려야 브론즈가 먼저 적재된다 — 실버는 브론즈를 읽는다
    path = tmp_path / "fail.db"
    assert main(["all", "--db", str(path)]) == 1
    # 채택되지 않았으므로 골드는 아예 생기지 않는다
    conn = sqlite3.connect(path)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert "gold_kpi_daily" not in tables


@requires_source
def test_F3_정상_산출물에서는_정합률이_기준을_넘는다(built_db):
    """기록 04 게이트 6 — 427/511 = 83.6% ≥ 80%."""
    result = silver.build_reviews(built_db)
    assert result["gu_match"] == 427
    assert result["gu_total"] == 511
    assert result["gu_agreement"] >= result["gu_threshold"]


# --- 경고 수정분 회귀 ------------------------------------------------------


@requires_source
def test_W1_게이트3_보고_수치가_실제_스캔과_일치한다(built_db):
    result = gates.gate3(built_db)
    assert result["value_scanned_views"] + result["schema_checked_views"] == result["views_scanned"]


def test_W2_대조_불일치_로그에_셀_원값이_없다(tmp_path, monkeypatch):
    """`silver_reservations.staff` 는 직원 실명이다 — 위치만 남긴다."""
    data = tmp_path / "data"
    (data / "silver").mkdir(parents=True)
    (data / "silver" / "silver_branch_alias.csv").write_text(
        "alias,branch_code,branch_pk\n비밀표기,CERAMIQUE-GN-001,2\n", encoding="utf-8")

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE silver_branch_alias (alias, branch_code, branch_pk)")
    conn.execute("INSERT INTO silver_branch_alias VALUES ('다른표기','CERAMIQUE-GN-001','2')")
    monkeypatch.setattr(
        gates, "CSV_PARITY_PAIRS",
        [("silver/silver_branch_alias.csv", "silver_branch_alias")])

    with pytest.raises(RebuildMismatch) as exc:
        gates.csv_parity(conn, data_dir=data)
    rendered = exc.value.render()
    assert "비밀표기" not in rendered and "다른표기" not in rendered
    assert "silver_branch_alias[행 0].alias" in rendered


def test_W7_1자_이름도_마스킹된다():
    """성만 남기면 1자 이름은 원값 그대로가 된다 — 통째로 덮는다."""
    from build.masking import mask_name_sql

    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (c TEXT)")
    conn.executemany("INSERT INTO t VALUES (?)", [("김",), ("김수",), ("",)])
    got = [r[0] for r in conn.execute(f"SELECT {mask_name_sql('c')} FROM t")]
    assert got == ["○", "김○", ""]


@requires_source
def test_W8_알_수_없는_지점_표기는_코드를_남기고_멈춘다(built_db):
    from build.errors import UnknownBranch

    built_db.execute(
        "INSERT INTO bronze_vegas_reservations "
        "(branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        " sales, receipt, visitCount, visitStatus) "
        "VALUES ('없는지점','20260301','TEST','합성표본','','','미지정',0,0,1,'내원')"
    )
    try:
        with pytest.raises(UnknownBranch) as exc:
            silver.build_reservations(built_db)
        assert exc.value.code == "UNKNOWN_BRANCH"
    finally:
        built_db.rollback()


def test_W9_원천_경로_규약이_한_곳이다(tmp_path):
    """`data_dir` 오버라이드가 전 경로에 일관되게 먹는지 — SoT 가 둘이면 여기서 갈린다."""
    from config import sources_for

    src = sources_for(tmp_path)
    assert src.vegas_dir == tmp_path / "bronze" / "vegas"
    assert src.nexus_dir == tmp_path / "bronze" / "nexus"
    assert src.scoring_dir == tmp_path / "silver" / "_scoring"
    assert src.ontology_dir == tmp_path / "ontology"


@requires_source
def test_W3_리텐션_관찰_종료일이_데이터에서_유도된다(built_db):
    """상수가 아니라 마지막 예약일 기준 — 창이 늘어도 조용히 틀리지 않는다."""
    resv = [dict(r) for r in built_db.execute(
        "SELECT resv_date, chart_no, is_new, is_revisit, is_foreign_est FROM silver_reservations")]
    rows = gold.build_retention(resv)
    assert [r["cohort_month"] for r in rows][-1] == "2026-08"
    # 마지막 두 코호트는 60일 관찰 미확보 → 부분 코호트
    assert rows[-1]["is_partial_cohort"] == 1
    assert rows[-2]["is_partial_cohort"] == 1

    # 창을 하루로 줄이면 판정이 따라 움직인다(상수였다면 고정된 채로 남는다)
    shrunk = [r for r in resv if r["resv_date"] <= "2026-03-01"]
    rows2 = gold.build_retention(shrunk)
    assert all(r["is_partial_cohort"] == 1 for r in rows2[-2:])
