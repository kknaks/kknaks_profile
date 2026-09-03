"""P5 — 온톨로지 적재와 **게이트 2**(빌드 재현). SPEC-001 AC-2 · AC-6."""

from __future__ import annotations

import pytest

from build import gates, ontology
from build.errors import NodeIdMismatch, OrphanEdge, RebuildMismatch
from build.spec_contract import (
    EXOGENOUS_NODES,
    REBUILD_ROWCOUNTS,
    REBUILD_TOTALS,
    SPEC_NODES,
    VERDICT_COUNTS,
)
from tests.conftest import requires_source


# --- 게이트 2 — 빌드 재현 -------------------------------------------------


@requires_source
def test_게이트2_대조값_전항_일치(built_db):
    result = gates.gate2(built_db)
    for name, want in REBUILD_TOTALS.items():
        assert result["measured"][name] == want
    for table, want in REBUILD_ROWCOUNTS.items():
        assert built_db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == want


@requires_source
def test_게이트2_는_DB_재빌드가_기존_CSV_산출물과_셀_단위로_같음을_증명한다(built_db):
    """합계가 맞아도 행 배치가 다를 수 있다 — 이식의 등가는 전 셀 대조로만 증명된다."""
    result = gates.csv_parity(built_db)
    assert result["diffs"] == 0
    assert result["tables"] == 10
    assert result["cells"] > 1_000_000


@requires_source
def test_게이트2_는_대조값이_어긋나면_REBUILD_MISMATCH_로_실패한다(built_db):
    built_db.execute("UPDATE gold_kpi_daily SET new_patients = new_patients + 1 "
                     "WHERE date = (SELECT MIN(date) FROM gold_kpi_daily)")
    try:
        with pytest.raises(RebuildMismatch) as exc:
            gates.gate2(built_db)
        assert exc.value.code == "REBUILD_MISMATCH"
    finally:
        built_db.rollback()
    gates.gate2(built_db)  # 원복 확인


@requires_source
def test_브론즈_내원과_실버_내원이_중복_65_로_대사된다(built_db):
    """47,537 + 내원 중복 65 = 47,602 (기록 05 5장)."""
    silver_visits = built_db.execute(
        "SELECT SUM(visits) FROM gold_kpi_daily").fetchone()[0]
    bronze_visits = built_db.execute(
        "SELECT COUNT(*) FROM bronze_vegas_reservations WHERE visitStatus = '내원'"
    ).fetchone()[0]
    assert silver_visits == 47_537
    assert bronze_visits == 47_602
    assert bronze_visits - silver_visits == 65


# --- AC-6 — 온톨로지 무결성 ----------------------------------------------


@requires_source
def test_AC6_노드_25_엣지_27_고아_0(built_db):
    result = ontology.check(built_db)
    assert result["nodes"] == 25
    assert result["edges"] == 27
    assert result["orphans"] == 0


@requires_source
def test_AC6_node_id_가_SPEC_001_25종_표와_1대1_대응한다(built_db):
    """어긋나면 적재를 실패시키고 어긋난 id·라벨을 보고한다 — 표를 조용히 맞추지 않는다."""
    assert ontology.check(built_db)["spec_1to1"] == "pass"

    actual = {(r["node_id"], r["name_ko"], r["node_type"]) for r in built_db.execute(
        "SELECT node_id, name_ko, node_type FROM ontology_nodes")}
    assert actual == set(SPEC_NODES)


@requires_source
def test_AC6_node_id_는_전건_snake_case_다(built_db):
    ids = [r[0] for r in built_db.execute("SELECT node_id FROM ontology_nodes")]
    assert all(ontology.SNAKE_CASE.match(i) for i in ids), ids


@requires_source
def test_AC6_외생_노드는_들어오는_엣지가_0_이다(built_db):
    placeholders = ",".join("?" * len(EXOGENOUS_NODES))
    n = built_db.execute(
        f"SELECT COUNT(*) FROM ontology_edges WHERE effect IN ({placeholders})",
        tuple(EXOGENOUS_NODES),
    ).fetchone()[0]
    assert n == 0


@requires_source
def test_AC6_기각과_보류_행에_사유가_있다(built_db):
    """「왜 그리지 않았나」가 조회 가능해야 같은 질문이 반복되지 않는다."""
    rows = list(built_db.execute(
        "SELECT cause, effect, rationale FROM ontology_edges "
        "WHERE verdict IN ('기각', '보류')"))
    assert len(rows) == 6
    assert all((r["rationale"] or "").strip() for r in rows)


@requires_source
def test_AC6_판정_분포가_계약과_같다(built_db):
    got: dict[str, int] = {}
    for r in built_db.execute("SELECT verdict FROM ontology_edges"):
        got[r[0]] = got.get(r[0], 0) + 1
    assert got == VERDICT_COUNTS


@requires_source
def test_고아_엣지를_주입하면_ORPHAN_EDGE_로_실패한다(built_db):
    built_db.execute(
        "INSERT INTO ontology_edges (cause, effect, edge_kind, verdict) "
        "VALUES ('sales_total', '없는_노드', 'causal', '채택')")
    try:
        with pytest.raises(OrphanEdge) as exc:
            ontology.check(built_db)
        assert exc.value.code == "ORPHAN_EDGE"
        assert any("없는_노드" in d for d in exc.value.detail)
    finally:
        built_db.rollback()
    assert ontology.check(built_db)["orphans"] == 0


@requires_source
def test_spec_표와_어긋나면_NODE_ID_MISMATCH_로_실패한다(built_db):
    built_db.execute("UPDATE ontology_nodes SET name_ko = '뒤바뀐 라벨' WHERE node_id = 'visits'")
    try:
        with pytest.raises(NodeIdMismatch) as exc:
            ontology.check(built_db)
        assert exc.value.code == "NODE_ID_MISMATCH"
        assert any("visits" in d for d in exc.value.detail)
    finally:
        built_db.rollback()


# --- lag 표기 -------------------------------------------------------------


def test_lag_는_원형_보존이고_lag_days_를_병기한다():
    """`2w` 를 `14d` 로 고쳐 넣지 않는다 — 원형은 그대로 두고 정수만 병기한다."""
    assert ontology.lag_days("0d") == 0
    assert ontology.lag_days("7d") == 7
    assert ontology.lag_days("2w") == 14
    assert ontology.lag_days("60d") == 60
    assert ontology.lag_days("") is None
    assert ontology.lag_days(None) is None


@requires_source
def test_적재된_lag_이_원천_문자열_그대로다(built_db):
    forms = {r[0] for r in built_db.execute("SELECT DISTINCT lag FROM ontology_edges")}
    assert "2w" in forms, "2w 를 14d 로 고쳐 넣지 않는다"
    pairs = {(r["lag"], r["lag_days"]) for r in built_db.execute(
        "SELECT DISTINCT lag, lag_days FROM ontology_edges")}
    assert ("2w", 14) in pairs
    assert ("", None) in pairs
