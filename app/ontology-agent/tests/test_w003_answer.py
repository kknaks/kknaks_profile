"""P3 — 답변 객체 파싱·검증. SPEC-005 §4 Validation · **게이트 5**.

위반 케이스를 전건 거부하는지가 이 파일의 요구사항이다 — 통과 케이스만 보면
「검증기가 있다」는 사실만 확인되고 「막는다」는 확인되지 않는다.
"""

from __future__ import annotations

import json

import pytest

from agent.answer import (
    AnswerSchemaError,
    EvidenceError,
    extract_answer_object,
    validate,
    validate_evidence,
    validate_schema,
)
from tests.conftest import requires_source


def _minimal(**overrides) -> dict:
    obj = {
        "answer": "8월 노쇼율은 5.0% 입니다.",
        "premise_correction": {"corrected": False},
        "used_edges": [],
        "citations": [],
    }
    obj.update(overrides)
    return obj


# --- 파싱 -------------------------------------------------------------------


def test_json_펜스에서_객체를_꺼낸다():
    text = '본문입니다.\n\n```json\n{"answer": "네", "premise_correction": {"corrected": false}}\n```'
    assert extract_answer_object(text)["answer"] == "네"


def test_펜스가_여러_개면_마지막_것을_쓴다():
    text = ('```json\n{"answer": "첫번째"}\n```\n중간\n'
            '```json\n{"answer": "마지막", "premise_correction": {"corrected": false}}\n```')
    assert extract_answer_object(text)["answer"] == "마지막"


def test_펜스가_없어도_균형_잡힌_객체를_찾는다():
    """모델이 펜스를 빠뜨리는 것은 흔하고, 그것 하나로 답변을 버리는 것은 과하다."""
    text = '설명 문장.\n{"answer": "펜스 없음", "premise_correction": {"corrected": false}}'
    assert extract_answer_object(text)["answer"] == "펜스 없음"


def test_본문에_중괄호가_있어도_객체를_찾는다():
    text = ('여는 괄호 { 가 본문에 있습니다.\n'
            '```json\n{"answer": "정상", "premise_correction": {"corrected": false}}\n```')
    assert extract_answer_object(text)["answer"] == "정상"


@pytest.mark.parametrize("text", ["", "   ", "JSON 이 없는 순수 텍스트 답변입니다."])
def test_객체가_없으면_스키마_위반이다(text):
    with pytest.raises(AnswerSchemaError):
        extract_answer_object(text)


# --- 스키마 -----------------------------------------------------------------


def test_최소_객체가_통과한다():
    validate_schema(_minimal())


@pytest.mark.parametrize("missing", ["answer", "premise_correction", "used_edges", "citations"])
def test_필수_필드가_빠지면_거부한다(missing):
    obj = _minimal()
    del obj[missing]
    with pytest.raises(AnswerSchemaError) as exc:
        validate_schema(obj)
    assert missing in exc.value.render()


def test_premise_correction_은_교정이_없어도_존재해야_한다():
    """필드가 없는 것과 「교정이 없다」는 다른 사실이다."""
    with pytest.raises(AnswerSchemaError):
        validate_schema(_minimal(premise_correction=None))
    validate_schema(_minimal(premise_correction={"corrected": False}))


def test_corrected_true_면_세_필드가_필수다():
    with pytest.raises(AnswerSchemaError) as exc:
        validate_schema(_minimal(premise_correction={"corrected": True}))
    rendered = exc.value.render()
    for key in ("claimed", "actual", "restated_question"):
        assert key in rendered
    validate_schema(_minimal(premise_correction={
        "corrected": True, "claimed": "떨어졌다", "actual": "올랐다",
        "restated_question": "왜 버텼나"}))


def test_used_edges_는_생략이_아니라_빈_배열이다():
    with pytest.raises(AnswerSchemaError):
        validate_schema(_minimal(used_edges=None))


def test_followups_상한은_3개다():
    validate_schema(_minimal(followups=["a", "b", "c"]))
    with pytest.raises(AnswerSchemaError):
        validate_schema(_minimal(followups=["a", "b", "c", "d"]))


def test_citations_에_source_삼요소가_없으면_거부한다():
    with pytest.raises(AnswerSchemaError) as exc:
        validate_schema(_minimal(citations=[
            {"claim": "매출", "value": 1, "source": {"tool": "query_kpi"}}]))
    assert "source.table" in exc.value.render()


# --- 게이트 5-② used_edges ⊆ 확정 --------------------------------------------


@requires_source
def test_G5_확정_엣지는_통과한다(built_db):
    obj = _minimal(used_edges=[{
        "edge_id": "payment_visits__sales_total", "from": "payment_visits",
        "to": "sales_total", "verdict": "자동 확정", "role": "매출 경로"}])
    report = validate_evidence(built_db, obj)
    assert report.used_edges_checked == 1


@requires_source
@pytest.mark.parametrize("edge_id,verdict", [
    ("promo_event__sales_total", "기각"),
    ("new_churns__new_patients", "보류"),
])
def test_G5_보류_기각을_used_edges_에_넣으면_거부한다(built_db, edge_id, verdict):
    """보류·기각은 `excluded_edges` 로만 간다(SPEC-005 §4)."""
    cause, effect = edge_id.split("__")
    obj = _minimal(used_edges=[{
        "edge_id": edge_id, "from": cause, "to": effect, "verdict": verdict}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "확정 엣지가 아니다" in exc.value.render()


@requires_source
def test_G5_존재하지_않는_엣지를_지어내면_거부한다(built_db):
    """관계를 데이터에서 가져왔다면 있을 수 없는 값이다."""
    obj = _minimal(used_edges=[{
        "edge_id": "sales_total__noshow_rate", "from": "sales_total",
        "to": "noshow_rate", "verdict": "채택"}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "존재하지 않는 엣지" in exc.value.render()


@requires_source
def test_G5_edge_id_와_from_to_가_어긋나면_거부한다(built_db):
    obj = _minimal(used_edges=[{
        "edge_id": "payment_visits__sales_total", "from": "avg_ticket",
        "to": "sales_total", "verdict": "자동 확정"}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "어긋난다" in exc.value.render()


@requires_source
def test_G5_판정_표기를_바꿔_적으면_거부한다(built_db):
    obj = _minimal(used_edges=[{
        "edge_id": "payment_visits__sales_total", "from": "payment_visits",
        "to": "sales_total", "verdict": "채택"}])   # 정본은 「자동 확정」
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "정본과 다르다" in exc.value.render()


# --- 게이트 5-① citations 재조회 ---------------------------------------------


@requires_source
def test_G5_citations_가_DB_재조회와_일치하면_통과한다(built_db):
    row = built_db.execute(
        "SELECT month, sales_total FROM gold_kpi_monthly WHERE month = '2026-08'").fetchone()
    obj = _minimal(citations=[{
        "claim": "8월 매출 3.69억", "value": row["sales_total"],
        "metric": "sales_total", "grain": "monthly",
        "period": {"start": "2026-08-01", "end": "2026-08-31"}, "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_kpi_monthly", "column": "sales_total"}}])
    report = validate_evidence(built_db, obj)
    assert report.citations_checked == 1
    assert report.citation_matches[0]["rule"] == "single_row"


@requires_source
def test_G5_추정치를_만들면_재조회에서_걸린다(built_db):
    """곱셈으로 만든 수치는 DB 어디에도 없다 — 정량 추정 금지가 여기서 실효를 갖는다."""
    obj = _minimal(citations=[{
        "claim": "리뷰 10건이면 신환 약 37명", "value": 37_000_000_123,
        "metric": "sales_total", "grain": "monthly",
        "period": {"start": "2026-08-01", "end": "2026-08-31"}, "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_kpi_monthly", "column": "sales_total"}}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "재조회 불일치" in exc.value.render()


@requires_source
def test_G5_일별_합계도_인용으로_인정된다(built_db):
    total = built_db.execute(
        "SELECT SUM(sales_total) AS s FROM gold_kpi_daily "
        "WHERE date >= '2026-08-01' AND date <= '2026-08-31'").fetchone()["s"]
    obj = _minimal(citations=[{
        "claim": "8월 매출 합", "value": total, "metric": "sales_total", "grain": "daily",
        "period": {"start": "2026-08-01", "end": "2026-08-31"}, "row_count": 30,
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    assert validate_evidence(built_db, obj).citation_matches[0]["rule"] == "sum"


@requires_source
def test_G5_문자열_수치는_거부한다(built_db):
    """「3.69억」은 재조회 대조가 성립하지 않는다 — 반올림 표기는 claim 에만."""
    obj = _minimal(citations=[{
        "claim": "8월 매출", "value": "3.69억", "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_kpi_monthly", "column": "sales_total"}}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "숫자여야 한다" in exc.value.render()


@requires_source
def test_G5_허용_목록_밖_출처는_거부한다(built_db):
    """원 테이블을 출처로 적으면 뷰 경유 규칙이 무너진다."""
    obj = _minimal(citations=[{
        "claim": "행", "value": 1, "row_count": 1,
        "source": {"tool": "query_layer", "table": "bronze_vegas_reservations",
                   "column": "sales"}}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "허용 목록 밖 출처" in exc.value.render()


@requires_source
def test_G5_없는_컬럼을_출처로_적으면_거부한다(built_db):
    obj = _minimal(citations=[{
        "claim": "값", "value": 1, "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "없는컬럼"}}])
    with pytest.raises(EvidenceError):
        validate_evidence(built_db, obj)


# --- drilldown · PII ---------------------------------------------------------


@requires_source
def test_드릴다운은_마스킹_뷰_산출이어야_한다(built_db):
    obj = _minimal(drilldown={
        "layer": "bronze", "table": "vegas_reservations",
        "view": "bronze_vegas_reservations",      # 원 테이블 — 거부
        "rows": [], "total": 0,
        "masked_fields": ["patientName", "phone", "birthday"]})
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "마스킹 뷰가 아니다" in exc.value.render()


@requires_source
def test_드릴다운_masked_fields_누락을_거부한다(built_db):
    obj = _minimal(drilldown={
        "layer": "bronze", "table": "vegas_reservations",
        "view": "v_bronze_vegas_reservations", "rows": [], "total": 0,
        "masked_fields": ["patientName"]})
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "masked_fields 누락" in exc.value.render()


@requires_source
def test_G3_답변에_PII_원값이_있으면_거부한다(built_db):
    """마스킹 문자 유무가 아니라 **원값 존재**로 판정한다 — 오탐이 안 나게."""
    raw = built_db.execute(
        "SELECT patientName FROM bronze_vegas_reservations "
        "WHERE length(patientName) >= 2 LIMIT 1").fetchone()[0]
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, _minimal(answer=f"{raw} 님의 예약입니다."))
    assert "실명 원값 노출" in exc.value.render()


@requires_source
def test_마스킹_표기는_통과한다(built_db):
    validate_evidence(built_db, _minimal(
        answer="김○○ 님(010-****-1234)의 예약입니다."))


@requires_source
def test_드릴다운_행에_원값이_있으면_거부한다(built_db):
    raw = built_db.execute(
        "SELECT phone FROM bronze_vegas_reservations WHERE length(phone) >= 8 LIMIT 1"
    ).fetchone()[0]
    obj = _minimal(drilldown={
        "layer": "bronze", "table": "vegas_reservations",
        "view": "v_bronze_vegas_reservations", "total": 1,
        "masked_fields": ["patientName", "phone", "birthday"],
        "rows": [{"phone": raw}]})
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "전화 원값 노출" in exc.value.render()


@requires_source
def test_validate_는_스키마와_근거를_모두_본다(built_db):
    with pytest.raises(AnswerSchemaError):
        validate(built_db, {"answer": "본문만 있다"})
    report = validate(built_db, _minimal())
    assert report.pii_scanned_fields >= 1


@requires_source
def test_SPEC005_예시_객체가_구조상_통과한다(built_db):
    """spec §4 의 예시를 실데이터 값으로 채워 전 필드를 한 번에 태운다."""
    row = built_db.execute(
        "SELECT sales_total FROM gold_kpi_monthly WHERE month = '2026-08'").fetchone()
    obj = {
        "answer": "8월 매출은 떨어지지 않았습니다.",
        "premise_correction": {
            "corrected": True, "claimed": "8월 매출이 떨어졌다",
            "actual": "8월 매출 3.69억", "restated_question": "내원·예약은 왜 떨어졌나"},
        "used_edges": [
            {"edge_id": "payment_visits__sales_total", "from": "payment_visits",
             "to": "sales_total", "verdict": "자동 확정", "sign": "0",
             "lag": None, "lag_days": None, "role": "매출이 버틴 경로"},
            {"edge_id": "cancel_rate__reservations", "from": "cancel_rate",
             "to": "reservations", "verdict": "채택", "sign": "−", "lag": "0d",
             "lag_days": 0, "confidence": "중간", "role": "예약 하락 원인 후보"},
        ],
        "excluded_edges": [
            {"edge_id": "promo_event__sales_total", "from": "promo_event",
             "to": "sales_total", "verdict": "기각", "reason": "효과 미검출"}],
        "citations": [{
            "claim": "8월 매출 3.69억", "value": row["sales_total"],
            "metric": "sales_total", "grain": "monthly",
            "period": {"start": "2026-08-01", "end": "2026-08-31"}, "row_count": 1,
            "source": {"tool": "query_kpi", "table": "gold_kpi_monthly",
                       "column": "sales_total"}}],
        "followups": ["그 취소들 원본을 보여줘"],
        "unknowns": [{"topic": "외국인 유입 채널", "reason": "미관측 노드"}],
    }
    report = validate(built_db, obj)
    assert report.used_edges_checked == 2
    assert report.citations_checked == 1
    assert json.dumps(obj, ensure_ascii=False)      # 직렬화 가능해야 응답에 실린다
