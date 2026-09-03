"""도구 4종 계약 — SPEC-002 AC-1~AC-11.

거부 경로가 이 파일의 절반이다. 「허용된 것이 된다」보다 **「허용되지 않은 것이 막힌다」**가
이 표면의 요구사항이기 때문이다(자유 SQL 없음 · 상한 거부 · PII 우회 차단).
"""

from __future__ import annotations

import pytest

from service import allowlist as al
from service import glossary
from service.errors import (
    InvalidRange,
    LimitExceeded,
    TooManyFilters,
    UnknownField,
    UnknownMetric,
    UnknownNode,
    UnknownTable,
)
from service.queries import query_kpi, query_layer, trace_ontology
from tests.conftest import requires_source

PII_COLUMNS = ("patientName", "phone", "birthday")


# --- AC-2 · AC-3 거부 경로 --------------------------------------------------


@requires_source
def test_AC2_허용_목록_밖_지표는_거부되고_허용_목록이_동봉된다(built_db):
    with pytest.raises(UnknownMetric) as exc:
        query_kpi(built_db, metrics=["sales_total", "없는지표"], grain="daily",
                  start="2026-08-01", end="2026-08-30")
    assert exc.value.code == "UNKNOWN_METRIC"
    assert "sales_total" in exc.value.allowed        # 무엇을 고를 수 있는지 알려준다
    payload = exc.value.to_tool_payload()
    assert payload["error"] == "UNKNOWN_METRIC" and payload["allowed"]


@requires_source
def test_AC2_허용_목록_밖_테이블은_거부된다(built_db):
    with pytest.raises(UnknownTable) as exc:
        query_layer(built_db, layer="bronze", table="없는테이블")
    assert exc.value.code == "UNKNOWN_TABLE"
    assert exc.value.allowed


@requires_source
def test_AC2_원_테이블_이름으로는_부를_수_없다(built_db):
    """`vegas_reservations` 는 되지만 `bronze_vegas_reservations` 는 안 된다 —
    소비자가 부르는 이름과 실제 관계명이 분리돼 있어 원 테이블 경로가 열리지 않는다."""
    for raw in ("bronze_vegas_reservations", "silver_reservations", "v_bronze_vegas_reservations"):
        with pytest.raises(UnknownTable):
            query_layer(built_db, layer="bronze", table=raw)


@requires_source
@pytest.mark.parametrize("column", PII_COLUMNS)
def test_AC3_PII_원_컬럼은_filters_에서_거부된다(built_db, column):
    """뷰에는 마스킹된 동명 컬럼이 있으므로 **필터 자체는 통과**하지만, 값은 마스킹본이다.
    원값으로 조회해도 한 건도 맞지 않는다 — 원값 우회가 여기서 무의미해진다."""
    result = query_layer(
        built_db, layer="bronze", table="vegas_reservations",
        filters=[{"field": column, "op": "eq", "value": "홍길동"}], limit=5)
    assert result["total"] == 0


@requires_source
def test_AC3_허용_목록_밖_필드는_UNKNOWN_FIELD_로_거부된다(built_db):
    for field in ("secret", "ssn", "patient_name_raw"):
        with pytest.raises(UnknownField) as exc:
            query_layer(built_db, layer="bronze", table="vegas_reservations",
                        filters=[{"field": field, "op": "eq", "value": 1}])
        assert exc.value.code == "UNKNOWN_FIELD"
        assert exc.value.allowed


@requires_source
def test_AC3_order_by_도_같은_목록을_지난다(built_db):
    with pytest.raises(UnknownField):
        query_layer(built_db, layer="bronze", table="vegas_reservations",
                    order_by={"field": "없는필드", "direction": "asc"})


@requires_source
def test_AC9_limit_201_은_거부되고_조용히_절단되지_않는다(built_db):
    with pytest.raises(LimitExceeded) as exc:
        query_layer(built_db, layer="bronze", table="vegas_reservations", limit=201)
    assert exc.value.code == "LIMIT_EXCEEDED"
    # 200 은 통과한다 — 상한 자체가 막힌 게 아니다
    assert query_layer(built_db, layer="bronze", table="vegas_reservations",
                       limit=200)["returned"] == 200


@requires_source
def test_필터_6개는_TOO_MANY_FILTERS_로_거부된다(built_db):
    filters = [{"field": "sales", "op": "gte", "value": 0} for _ in range(6)]
    with pytest.raises(TooManyFilters):
        query_layer(built_db, layer="bronze", table="vegas_reservations", filters=filters)


@requires_source
def test_잘못된_기간은_INVALID_RANGE_로_거부된다(built_db):
    with pytest.raises(InvalidRange):
        query_kpi(built_db, metrics=["visits"], grain="daily",
                  start="2026-08-30", end="2026-08-01")
    with pytest.raises(InvalidRange):
        query_kpi(built_db, metrics=["visits"], grain="daily",
                  start="20260801", end="2026-08-30")


# --- AC-4 마스킹 -------------------------------------------------------------


@requires_source
def test_AC4_응답이_마스킹_표기로만_오고_masked_fields_가_동봉된다(built_db):
    result = query_layer(built_db, layer="bronze", table="vegas_reservations", limit=50)
    assert result["masked_fields"] == ["patientName", "phone", "birthday"]
    assert result["view"].startswith("v_")
    for row in result["rows"]:
        assert "○" in row["patientName"]
        assert row["phone"] == "" or "*" in row["phone"]
        assert row["birthday"] == "" or row["birthday"].endswith("-**-**")


@requires_source
def test_AC4_뷰_밖의_원값은_응답에_없다(built_db):
    """원값 집합과 응답 값이 한 건도 겹치지 않는다 — 전수는 게이트 3 이 보고, 여기선 표면 확인."""
    raw = {r[0] for r in built_db.execute(
        "SELECT DISTINCT patientName FROM bronze_vegas_reservations WHERE patientName <> ''")}
    rows = query_layer(built_db, layer="bronze", table="vegas_reservations",
                       limit=200)["rows"]
    assert not ({r["patientName"] for r in rows} & raw)


# --- AC-7 · AC-8 골드 대조 ---------------------------------------------------


@requires_source
def test_AC7_query_kpi_값이_골드_재조회값과_오차_0(built_db):
    result = query_kpi(built_db, metrics=["sales_total", "visits", "new_patients"],
                       grain="daily", start="2026-08-01", end="2026-08-30")
    for row in result["rows"]:
        raw = built_db.execute(
            "SELECT sales_total, visits, new_patients FROM gold_kpi_daily WHERE date = ?",
            (row["period_key"],)).fetchone()
        assert row["values"]["sales_total"] == raw["sales_total"]
        assert row["values"]["visits"] == raw["visits"]
        assert row["values"]["new_patients"] == raw["new_patients"]


@requires_source
def test_AC7_계산식과_상태_경계가_함께_온다(built_db):
    result = query_kpi(built_db, metrics=["noshow_rate"], grain="daily",
                       start="2026-08-01", end="2026-08-30")
    formula = result["formulas"][0]
    assert formula["formula"] == "부도 ÷ (내원 + 부도)"
    assert "취소는 분모에서 제외" in formula["note"]
    th = result["status_thresholds"][0]
    assert th["direction"] == "높을수록 나쁨"
    assert th["주의"] == 0.0714 and th["경고"] == 0.087


@requires_source
def test_AC8_관측_없음_null_과_실제_0_이_구분된다(built_db):
    """`naver_reviews` 2026-03-21 이전은 null, 이후 리뷰 없는 날은 0."""
    before = query_kpi(built_db, metrics=["naver_reviews"], grain="daily",
                       start="2026-03-01", end="2026-03-20")
    assert all(r["values"]["naver_reviews"] is None for r in before["rows"])

    after = query_kpi(built_db, metrics=["naver_reviews"], grain="daily",
                      start="2026-03-21", end="2026-08-30")
    values = [r["values"]["naver_reviews"] for r in after["rows"]]
    assert all(v is not None for v in values)
    assert 0 in values, "관측 이후 실제 0 인 날이 있어야 이 구분이 의미를 갖는다"


@requires_source
def test_naver_reviews_는_상태를_갖지_않는다(built_db):
    """방향 없는 개입 변수 — 상태 축을 부여하지 않는다."""
    result = query_kpi(built_db, metrics=["naver_reviews"], grain="daily",
                       start="2026-08-01", end="2026-08-30")
    assert all("naver_reviews" not in r["status"] for r in result["rows"])
    assert result["status_thresholds"] == []


@requires_source
def test_avg_ticket_은_결제_내원_0_인_날_null_이다(built_db):
    rows = query_kpi(built_db, metrics=["avg_ticket", "payment_visits"], grain="daily",
                     start="2026-01-07", end="2026-08-30")["rows"]
    zero_days = [r for r in rows if r["values"]["payment_visits"] == 0]
    assert all(r["values"]["avg_ticket"] is None for r in zero_days)


@requires_source
def test_grain_4종이_각각_다른_골드_View_를_조회한다(built_db):
    """도구가 집계하지 않는다 — grain 마다 View 하나다(SPEC-002 OQ-2)."""
    seen = set()
    for grain, metrics in (("daily", ["visits"]), ("weekly", ["visits"]),
                           ("monthly", ["visits"]), ("retention_monthly", ["cohort_size"])):
        r = query_kpi(built_db, metrics=metrics, grain=grain,
                      start="2026-01-01", end="2026-12-31")
        seen.add(r["source"]["table"])
    assert seen == set(al.GRAIN_RELATION.values())


@requires_source
def test_retention_grain_은_retention_지표만_받는다(built_db):
    with pytest.raises(UnknownMetric):
        query_kpi(built_db, metrics=["sales_total"], grain="retention_monthly",
                  start="2026-01-01", end="2026-12-31")


# --- AC-10 빈 결과 -----------------------------------------------------------


@requires_source
def test_AC10_빈_결과가_에러가_아니라_200_빈_배열이다(built_db):
    """데이터 범위 밖 창도 허용한다 — 빈 결과와 실패를 구분한다."""
    result = query_kpi(built_db, metrics=["visits"], grain="daily",
                       start="2020-01-01", end="2020-01-31")
    assert result["rows"] == []
    assert result["source"]["row_count"] == 0

    rows = query_layer(built_db, layer="bronze", table="vegas_reservations",
                       filters=[{"field": "chartNo", "op": "eq", "value": "없는차트"}])
    assert rows["rows"] == [] and rows["total"] == 0


# --- AC-5 · AC-6 온톨로지 ----------------------------------------------------


@requires_source
def test_AC6_기본_호출은_채택_자동확정_선언만_준다(built_db):
    result = trace_ontology(built_db)
    verdicts = {e["verdict"] for e in result["edges"]}
    assert verdicts <= set(al.DEFAULT_VERDICTS)
    assert "기각" not in verdicts and "보류" not in verdicts
    assert len(result["edges"]) == 21          # 채택 4 + 자동 확정 14 + 선언 3


@requires_source
def test_AC5_기각_보류는_사유가_있고_인과_서술에_쓸_수_없다(built_db):
    result = trace_ontology(built_db, verdicts=["기각", "보류"])
    assert len(result["edges"]) == 6
    for edge in result["edges"]:
        assert edge["reason"], f"{edge['edge_id']} 에 사유가 없다"
        assert edge["usable_for_causal_claim"] is False


@requires_source
def test_채택_엣지는_reason_이_아니라_note_를_갖는다(built_db):
    """`reason` 은 배제 사유 전용이다 — 채택 엣지에 채우면 「기각 사유가 있다」로 읽힌다."""
    result = trace_ontology(built_db)
    for edge in result["edges"]:
        assert edge["reason"] is None
        assert edge["usable_for_causal_claim"] is True
    assert any(e["note"] for e in result["edges"])


@requires_source
def test_모든_엣지에_verdict_와_edge_id_가_있다(built_db):
    result = trace_ontology(built_db, verdicts=list(al.VERDICTS))
    assert len(result["edges"]) == 27
    for edge in result["edges"]:
        assert edge["verdict"] in al.VERDICTS
        assert edge["edge_id"] == f"{edge['from']}__{edge['to']}"


@requires_source
def test_lag_는_원형이고_lag_days_가_병기된다(built_db):
    result = trace_ontology(built_db, verdicts=list(al.VERDICTS))
    pairs = {(e["lag"], e["lag_days"]) for e in result["edges"]}
    assert ("2w", 14) in pairs, "2w 를 14d 로 고쳐 넣지 않는다"
    assert ("0d", 0) in pairs
    assert (None, None) in pairs


@requires_source
def test_미관측_노드는_observed_false_다(built_db):
    result = trace_ontology(built_db, verdicts=list(al.VERDICTS))
    unobserved = [n for n in result["nodes"] if not n["observed"]]
    assert [n["node_id"] for n in unobserved] == ["foreign_inflow_channel"]


@requires_source
def test_외생_노드는_들어오는_엣지가_없다(built_db):
    for node in ("weekday", "season", "holiday"):
        result = trace_ontology(built_db, node=node, direction="in",
                                verdicts=list(al.VERDICTS))
        assert result["edges"] == [], node


@requires_source
def test_노드를_이름과_id_둘_다로_찾는다(built_db):
    by_id = trace_ontology(built_db, node="sales_total", direction="in")
    by_name = trace_ontology(built_db, node="매출", direction="in")
    assert {e["edge_id"] for e in by_id["edges"]} == {e["edge_id"] for e in by_name["edges"]}


@requires_source
def test_없는_노드는_UNKNOWN_NODE_로_거부된다(built_db):
    with pytest.raises(UnknownNode) as exc:
        trace_ontology(built_db, node="없는노드")
    assert exc.value.code == "UNKNOWN_NODE"
    assert exc.value.allowed


@requires_source
def test_depth_상한을_넘으면_거부된다(built_db):
    with pytest.raises(InvalidRange):
        trace_ontology(built_db, node="sales_total", depth=4)


# --- get_definition ----------------------------------------------------------


def test_get_definition_이_계산식과_근거를_준다():
    payload = glossary.definition_payload("노쇼율")
    assert payload["definition"].startswith("부도 ÷ (내원 + 부도)")
    assert payload["status"] in ("확정", "승계", "대기")
    assert "기록 03" in payload["source_note"]
    assert "noshow_rate" in payload["aliases"]


def test_get_definition_이_KPI_컬럼명으로도_찾힌다():
    assert glossary.definition_payload("noshow_rate")["term"] == "노쇼율"


def test_get_definition_이_폐쇄_목록과_enum_을_준다():
    concepts = glossary.ENUMS["procedure_concept"]
    assert len(concepts) == 13
    assert glossary.ENUMS["sentiment"] == ["긍정", "중립", "부정", "판정불가"]
    payload = glossary.definition_payload("sentiment")
    assert payload["enum_values"] == ["긍정", "중립", "부정", "판정불가"]


def test_없는_용어는_유사_후보와_함께_거부된다():
    with pytest.raises(KeyError):
        glossary.definition_payload("존재하지않는용어")
    assert glossary.suggestions("노쇼")


def test_도구_목록이_정확히_4종이다():
    from tools.server import TOOL_NAMES

    assert len(TOOL_NAMES) == 4
    assert set(TOOL_NAMES) == {
        "query_kpi", "query_layer", "trace_ontology", "get_definition"}
