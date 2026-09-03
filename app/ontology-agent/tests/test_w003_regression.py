"""P4 — 회귀 3본과 **게이트 4·5**. SPEC-005 §6 R-1~R-3 · AC-보조 1.

## 두 층으로 나눠 둔 이유

LLM 을 부르는 회귀는 큐·워커·codex 가 다 서 있어야 돌고, 그게 없는 환경에서는
**skip 이 아니라 아무것도 검증되지 않는다.** 그래서 같은 기준값을 두 번 쓴다:

1. **기준값 계층**(`test_R*_기준값...`) — LLM 없이 DB 만으로 SPEC-005 의 실측 기준을
   재현한다. 항상 돈다. 회귀가 겨눌 과녁이 실제로 데이터에 있는지부터 고정한다.
2. **라이브 계층**(`test_R*_라이브`) — `ONTOLOGY_LIVE_REGRESSION=1` 일 때만 돈다.
   실제로 질문을 넣고 답변 객체를 단언한다.

과녁이 틀리면 라이브가 통과해도 의미가 없다. 1이 2의 전제다.

## 판정은 사람 눈이 아니라 단언이다 (OQ-3 확정)

**수치는 정확 일치, 서술은 키워드 포함.** 문구 완전 일치를 요구하지 않는다 —
같은 사실을 다르게 쓴 답변을 실패로 만들면 회귀가 카피 검사가 된다.
"""

from __future__ import annotations

import json
import os
import time

import pytest

from agent import store
from agent.answer import CAUSAL_VERDICTS, validate
from config import settings
from service import glossary
from tests.conftest import TEST_PASSWORD, requires_source

LIVE = os.environ.get("ONTOLOGY_LIVE_REGRESSION") == "1"
requires_live = pytest.mark.skipif(
    not LIVE, reason="라이브 회귀 — redis + codex 워커 + ONTOLOGY_LIVE_REGRESSION=1 필요")

#: R-1 기대 — SPEC-005 §6. (주 시작일, 노쇼율, 부도, 내원)
R1_WEEKS = [
    ("2026-08-03", 0.0534, 54, 958),
    ("2026-08-10", 0.0476, 46, 921),
    ("2026-08-17", 0.0523, 53, 961),
    ("2026-08-24", 0.0499, 56, 1066),
]
#: 상태 경계 — 주의 7.14% · 경고 8.7%. 전 주 「양호」여야 한다.
R1_WARN, R1_ALERT = 0.0714, 0.087

#: R-2 기대 — 8월 매출은 **떨어지지 않았다**. 실제로 떨어진 것은 내원과 예약이다.
R2_VISITS_JUL, R2_VISITS_AUG = 5428, 4196
R2_RESERVATIONS_JUL, R2_RESERVATIONS_AUG = 9057, 6852

LIVE_TIMEOUT_SEC = 240
POLL_INTERVAL_SEC = 2


# --- 기준값 계층 — LLM 없이 과녁을 고정한다 ---------------------------------


@requires_source
def test_R1_기준값_주별_노쇼율이_기록_08_실측과_일치한다(built_db):
    """회귀가 겨눌 값이 DB 에 실제로 있는지부터 고정한다."""
    for week_start, rate, noshows, visits in R1_WEEKS:
        row = built_db.execute(
            "SELECT noshow_rate, noshows, visits FROM gold_kpi_weekly WHERE week_start = ?",
            (week_start,)).fetchone()
        assert row is not None, f"{week_start} 주 행이 없다"
        assert row["noshows"] == noshows
        assert row["visits"] == visits
        assert abs(row["noshow_rate"] - rate) < 1e-9
        # 노쇼율 = 부도 ÷ (내원 + 부도) — 취소는 분모에서 제외한다
        assert abs(row["noshow_rate"] - noshows / (visits + noshows)) < 5e-5


@requires_source
def test_R1_기준값_전_주가_양호_구간이다(built_db):
    for week_start, rate, _, _ in R1_WEEKS:
        assert rate < R1_WARN, f"{week_start} 가 주의 경계를 넘는다"
        assert rate < R1_ALERT


@requires_source
def test_R1_기준값_query_kpi_가_노쇼율_계산식을_함께_준다(built_db):
    """R-1 라이브의 ③ 경로가 **실제로 존재하는지**부터 고정한다.

    「도구가 계산식을 줬다」를 통과 근거로 인정하려면 도구가 정말 주는지가 먼저다.
    이게 깨지면 라이브 단언이 조용히 무조건 통과가 된다(WORK-005).
    """
    from service.queries import query_kpi

    payload = query_kpi(built_db, metrics=["noshow_rate"], grain="weekly",
                        start="2026-08-01", end="2026-08-30")
    formulas = {f["metric"]: f for f in payload["formulas"]}
    assert "noshow_rate" in formulas, f"계산식이 없다: {payload['formulas']}"
    formula = formulas["noshow_rate"]["formula"]
    # 취소가 분모에서 빠진다는 것이 이 계산식의 요점이다(기록 03 1장)
    assert "부도" in formula and "내원" in formula, formula
    assert formulas["noshow_rate"]["glossary_ref"]


@requires_source
def test_R2_기준값_8월_매출은_떨어지지_않았다(built_db):
    """전제 교정의 근거 — 이 값이 뒤집히면 R-2 시나리오 자체가 성립하지 않는다."""
    rows = {
        r["month"]: r["sales_total"] for r in built_db.execute(
            "SELECT month, sales_total FROM gold_kpi_monthly WHERE month IN ('2026-07','2026-08')")
    }
    jul, aug = rows["2026-07"], rows["2026-08"]
    assert aug > jul, "8월 매출이 7월보다 낮다 — 전제 교정 시나리오가 깨진다"
    growth = (aug - jul) / jul
    assert 0.25 <= growth <= 0.30, f"7→8월 증가율 {growth:.1%} (기대 +27% 부근)"
    assert 3.6e8 <= aug <= 3.7e8, f"8월 매출 {aug:,} (기대 3.69억 부근)"


@requires_source
def test_R2_기준값_실제로_떨어진_것은_내원과_예약이다(built_db):
    rows = {
        r["month"]: r for r in built_db.execute(
            "SELECT month, visits, reservations FROM gold_kpi_monthly "
            "WHERE month IN ('2026-07','2026-08')")
    }
    assert rows["2026-07"]["visits"] == R2_VISITS_JUL
    assert rows["2026-08"]["visits"] == R2_VISITS_AUG
    assert rows["2026-07"]["reservations"] == R2_RESERVATIONS_JUL
    assert rows["2026-08"]["reservations"] == R2_RESERVATIONS_AUG


@requires_source
def test_R2_기준값_인용할_확정_엣지가_존재한다(built_db):
    """`used_edges` 에 실릴 후보가 DB 에 확정 판정으로 있어야 한다."""
    expected = {
        "payment_visits__sales_total": "자동 확정",
        "cancel_rate__reservations": "채택",
        "naver_reviews__reservations": "채택",
    }
    for edge_id, verdict in expected.items():
        cause, effect = edge_id.split("__")
        row = built_db.execute(
            "SELECT verdict FROM ontology_edges WHERE cause = ? AND effect = ?",
            (cause, effect)).fetchone()
        assert row is not None, f"{edge_id} 엣지가 없다"
        assert row["verdict"] == verdict
        assert row["verdict"] in CAUSAL_VERDICTS


@requires_source
def test_R3_기준값_8월_취소_원본이_20행_이상_있고_마스킹된다(built_db):
    """드릴다운이 가리킬 행이 실제로 있고, 뷰가 이미 가리고 있는지."""
    total = built_db.execute(
        "SELECT COUNT(*) FROM v_bronze_vegas_reservations "
        "WHERE visitStatus = '취소' AND resvDate LIKE '202608%'").fetchone()[0]
    assert total >= 20

    rows = built_db.execute(
        "SELECT patientName, phone, birthday, resvDate, visitStatus "
        "FROM v_bronze_vegas_reservations "
        "WHERE visitStatus = '취소' AND resvDate LIKE '202608%' LIMIT 20").fetchall()
    assert len(rows) == 20
    for row in rows:
        assert row["visitStatus"] == "취소"
        assert row["resvDate"].startswith("202608")
        assert "○" in row["patientName"]
        assert row["phone"] == "" or "*" in row["phone"]
        assert row["birthday"] == "" or row["birthday"].endswith("-**-**")


# --- 라이브 계층 — 실제로 LLM 을 부른다 --------------------------------------


@pytest.fixture
def live_client(monkeypatch, tmp_path, built_db_path):
    from fastapi.testclient import TestClient

    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "live_chat.db")
    monkeypatch.setattr(settings, "session_cookie_secure", False)
    import main

    with TestClient(main.app) as c:
        c.post("/api/auth/session", json={"password": TEST_PASSWORD})
        yield c


def _ask(client, question: str) -> dict:
    """질문을 넣고 `done`/`failed` 까지 2초 간격으로 폴링한다(SPEC-003 폴링 계약)."""
    created = client.post("/api/chat/conversations", json={"question": question})
    assert created.status_code == 201, created.text
    conversation_id = created.json()["conversation"]["id"]

    started = time.monotonic()
    while time.monotonic() - started < LIVE_TIMEOUT_SEC:
        body = client.get(f"/api/chat/conversations/{conversation_id}").json()
        assistant = body["messages"][-1]
        if assistant["status"] != "pending":
            assistant["_elapsed_sec"] = round(time.monotonic() - started, 1)
            return assistant
        time.sleep(POLL_INTERVAL_SEC)
    raise AssertionError(f"{LIVE_TIMEOUT_SEC}초 안에 마감되지 않았다")


def _done(assistant: dict) -> dict:
    assert assistant["status"] == "done", (
        f"status={assistant['status']} error_code={assistant.get('error_code')} "
        f"content={assistant.get('content', '')[:400]}")
    result = assistant["result"]
    assert result is not None, "done 인데 result 가 없다"
    return result


@requires_source
@requires_live
def test_R1_라이브_현황_질문(live_client, built_db):
    """「최근 4주 노쇼율 추이는?」 — 주별 4행 · `used_edges` 빈 배열 · 계산식 인용."""
    assistant = _ask(live_client, "최근 4주 노쇼율 추이는?")
    result = _done(assistant)
    validate(built_db, result)               # 게이트 5 를 그대로 태운다

    # 온톨로지를 타지 않는 질문이다 — 골드 View 단독으로 답이 나온다
    assert result["used_edges"] == [], f"현황 질문인데 엣지를 밟았다: {result['used_edges']}"

    # 수치는 정확 일치 — 주별 값이 인용에 실려야 한다
    cited = {c["value"] for c in result["citations"]}
    weekly_rates = {rate for _, rate, _, _ in R1_WEEKS}
    assert weekly_rates & cited, f"주별 노쇼율이 인용에 없다: {sorted(cited)[:8]}"

    # 서술은 키워드 포함(OQ-3) — 문구 완전 일치를 요구하지 않는다
    answer = result["answer"]
    assert "노쇼" in answer

    # 「계산식이 답변 앞에 있었나」 — 경로가 **셋**이다. 한 표현만 고집하면 같은 사실을
    # 다르게 쓴 답변을 실패로 만들고 회귀가 카피 검사가 된다.
    #
    # ③이 WORK-005 에서 추가됐다. `query_kpi` 응답은 `formulas[]` 를 **항상** 싣는데
    # (service/queries.py `formulas_for`), 단언이 ①②만 봐서 「도구가 계산식을 줬고
    # 모델이 그걸 읽고 답했다」를 통과시키지 못했다 — 라이브 R-1 실측에서 이 자리만
    # 어긋났다(2026-09-03). 모델이 계산식을 본문에 재진술할지는 문장 선택의 문제이지
    # 근거 무결성의 문제가 아니다. 근거 무결성은 게이트 5-①(citations 재조회)이 본다.
    formula_in_answer = any(k in answer for k in ("부도", "내원", "÷", "분모"))
    asked_definition = any(s.get("tool") == "get_definition" for s in assistant["steps"])
    # ③ 계산식이 실린 `query_kpi` 응답을 실제로 받았는가 — `args_summary` 에 지표명이
    #    남으므로(consumer.summarize_args) 어느 지표를 물었는지로 판정한다.
    formula_from_tool = bool(glossary.formula_of("noshow_rate")) and any(
        s.get("tool") == "query_kpi" and "noshow_rate" in (s.get("args_summary") or "")
        for s in assistant["steps"])
    assert formula_in_answer or asked_definition or formula_from_tool, (
        "계산식이 답변 앞에 한 번도 오지 않았다 — 본문에도 없고 get_definition 도 안 불렀고 "
        "noshow_rate 로 query_kpi 를 부르지도 않았다\n"
        f"answer={answer[:300]}\nsteps={[s.get('args_summary') for s in assistant['steps']]}")

    print(f"\n[R-1] {assistant['_elapsed_sec']}초 · 도구 {len(assistant['steps'])}회 "
          f"· 인용 {len(result['citations'])}건 · 계산식(본문 {formula_in_answer} / "
          f"get_definition {asked_definition} / query_kpi 응답 {formula_from_tool})")


@requires_source
@requires_live
def test_R2_라이브_원인_질문과_전제_교정(live_client, built_db):
    """「8월 매출이 왜 떨어졌어?」 — 전제부터 바로잡아야 한다."""
    assistant = _ask(live_client, "8월 매출이 왜 떨어졌어?")
    result = _done(assistant)
    validate(built_db, result)

    pc = result["premise_correction"]
    assert pc["corrected"] is True, "8월 매출은 떨어지지 않았다 — 전제를 교정해야 한다"
    for key in ("claimed", "actual", "restated_question"):
        assert pc[key].strip()

    # 확정 엣지만 — 보류·기각은 used_edges 에 없다(validate 가 이미 막지만 명시한다)
    assert result["used_edges"], "원인 질문인데 엣지를 밟지 않았다(게이트 5 위반)"
    for edge in result["used_edges"]:
        assert edge["verdict"] in CAUSAL_VERDICTS

    # 근거 수치가 실제로 실렸는가 — 8월 매출이 인용에 있어야 한다
    aug = built_db.execute(
        "SELECT sales_total FROM gold_kpi_monthly WHERE month = '2026-08'").fetchone()[0]
    assert aug in {c["value"] for c in result["citations"]}, "8월 매출이 인용에 없다"

    print(f"\n[R-2] {assistant['_elapsed_sec']}초 · 엣지 {len(result['used_edges'])} "
          f"· 인용 {len(result['citations'])}건 · 교정 {pc['actual'][:60]}")


@requires_source
@requires_live
def test_R3_라이브_드릴다운(live_client, built_db):
    """「8월 취소 원본 20건 보여줘」 — 20행 · 전 행 8월/취소 · 마스킹 표기."""
    assistant = _ask(live_client, "8월 취소 원본 20건 보여줘")
    result = _done(assistant)
    validate(built_db, result)

    drill = result.get("drilldown")
    assert drill is not None, "드릴다운 질문인데 drilldown 이 없다"
    assert drill["view"] == "v_bronze_vegas_reservations"
    assert set(drill["masked_fields"]) >= {"patientName", "phone", "birthday"}

    rows = drill["rows"]
    assert len(rows) == 20, f"20행이 아니라 {len(rows)}행"
    for row in rows:
        assert row.get("visitStatus") == "취소"
        assert str(row.get("resvDate", "")).startswith(("202608", "2026-08"))
        assert "○" in str(row.get("patientName", ""))

    print(f"\n[R-3] {assistant['_elapsed_sec']}초 · {len(rows)}행 · total {drill['total']}")


@requires_source
@requires_live
def test_게이트5_라이브_답변에_추정치가_없다(live_client, built_db):
    """도구가 주지 않은 수치를 만들면 `citations` 재조회가 성립하지 않는다."""
    assistant = _ask(live_client, "8월 매출이 왜 떨어졌어?")
    result = _done(assistant)
    report = validate(built_db, result)
    assert report.citations_checked == len(result["citations"])
    for match in report.citation_matches:
        assert match["rule"] in ("single_row", "sum", "row_value")
    print("\n[게이트 5] 재조회 대조표:\n" +
          json.dumps(report.citation_matches, ensure_ascii=False, indent=2))


@requires_source
@requires_live
def test_라이브_폴링_중_본문과_단계가_자란다(live_client):
    """`pending` 동안 화면이 볼 것이 있어야 한다(SPEC-003 AC-8)."""
    created = live_client.post(
        "/api/chat/conversations", json={"question": "최근 4주 노쇼율 추이는?"})
    conversation_id = created.json()["conversation"]["id"]

    grew = False
    started = time.monotonic()
    while time.monotonic() - started < LIVE_TIMEOUT_SEC:
        assistant = live_client.get(
            f"/api/chat/conversations/{conversation_id}").json()["messages"][-1]
        if assistant["status"] == "pending" and (assistant["content"] or assistant["steps"]):
            grew = True
        if assistant["status"] != "pending":
            break
        time.sleep(POLL_INTERVAL_SEC)
    assert grew, "pending 동안 content·steps 가 한 번도 자라지 않았다"


def test_저장소_스키마가_result_를_객체로_돌려준다(monkeypatch, tmp_path):
    """`result` 는 문자열이 아니라 파싱된 객체로 나가야 FE 가 칩을 그린다."""
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)
        store.update_message(conn, mid, {
            "status": store.STATUS_DONE,
            "result": {"answer": "본문", "used_edges": [{"edge_id": "a__b"}]}})
        message = store.list_messages(conn, cid)[0]
    assert isinstance(message["result"], dict)
    assert message["result"]["used_edges"][0]["edge_id"] == "a__b"
