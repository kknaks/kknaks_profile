"""API 계약 — SPEC-003 AC-1~AC-7 · AC-11 · AC-13~AC-16.

앱 전체를 TestClient 로 띄우고 **실제 DB 를 서빙**한다. 세션 게이트가 전 API 앞에 서므로
쿠키 없는 호출이 401 인지부터 본다 — 게이트가 라우터 하나에만 걸려 있으면 여기서 드러난다.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from config import settings
from tests.conftest import TEST_PASSWORD, requires_source

#: 세션이 필요한 전 엔드포인트. 새 라우터가 늘면 여기 더해 401 검사를 함께 받는다.
GUARDED = (
    "/api/layers/bronze/tables",
    "/api/layers/bronze/vegas_reservations",
    "/api/layers/gold/gold_kpi_daily/lineage",
    "/api/kpi/cards",
    "/api/kpi/series?metrics=visits&grain=daily&start=2026-08-01&end=2026-08-05",
    "/api/graph",
    "/api/forecast",
)


# --- AC-1 · AC-2 접속 게이트 -------------------------------------------------


@requires_source
@pytest.mark.parametrize("path", GUARDED)
def test_AC1_세션_없이_부른_모든_API_가_401_NO_SESSION(client, path):
    r = client.get(path)
    assert r.status_code == 401
    assert r.json() == {"detail": "NO_SESSION"}


@requires_source
def test_AC1_게이트를_통과하면_재입력_없이_전_API_가_열린다(auth_client):
    for path in GUARDED:
        assert auth_client.get(path).status_code == 200, path


@requires_source
def test_틀린_비밀번호는_401_INVALID_PASSWORD(client):
    r = client.post("/api/auth/session", json={"password": "틀린값"})
    assert r.status_code == 401
    assert r.json()["detail"] == "INVALID_PASSWORD"


@requires_source
def test_세션_확인_엔드포인트(client):
    assert client.get("/api/auth/session").status_code == 401
    client.post("/api/auth/session", json={"password": TEST_PASSWORD})
    assert client.get("/api/auth/session").json() == {"ok": True}


@requires_source
def test_AC2_비밀번호_값이_응답_어디에도_없다(auth_client):
    for path in ("/api/auth/session", *GUARDED):
        body = auth_client.get(path).text
        assert TEST_PASSWORD not in body, path


@requires_source
def test_env_미주입이면_인증이_명시적으로_거부된다(client, monkeypatch):
    """기본값이 없다는 것이 「아무나 들어온다」가 되면 게이트가 아니다."""
    monkeypatch.setattr(settings, "demo_password", "")
    r = client.post("/api/auth/session", json={"password": ""})
    assert r.status_code in (422, 503)


@requires_source
def test_세션_쿠키가_httponly_이고_이름이_계약대로다(client):
    r = client.post("/api/auth/session", json={"password": TEST_PASSWORD})
    cookie = r.headers["set-cookie"]
    assert "ontology_demo_sid=" in cookie
    assert "HttpOnly" in cookie
    assert "samesite=lax" in cookie.lower()
    assert "Max-Age=2592000" in cookie          # 30일
    # 세션 값에 비밀번호가 실리지 않는다 — 만료 + HMAC 뿐이다
    assert TEST_PASSWORD not in cookie


@requires_source
def test_rate_limit_계정_표면이_없다(auth_client):
    """DEC-005 D2 — 두지 않기로 확정. 시도 횟수 제한도 없다."""
    paths = {r.path for r in auth_client.app.routes if hasattr(r, "path")}
    assert not any("login" in p or "account" in p or "user" in p for p in paths)
    for _ in range(12):
        assert auth_client.post(
            "/api/auth/session", json={"password": "틀린값"}).status_code == 401


# --- AC-3 · AC-4 · AC-11 · AC-16 계층 조회 -----------------------------------


@requires_source
def test_AC3_브론즈_응답이_마스킹_표기로만_온다(auth_client):
    r = auth_client.get("/api/layers/bronze/vegas_reservations?limit=50")
    body = r.json()
    assert body["masked_fields"] == ["patientName", "phone", "birthday"]
    assert body["view"].startswith("v_")
    for row in body["rows"]:
        assert "○" in row["patientName"]
        assert row["birthday"] == "" or row["birthday"].endswith("-**-**")


@requires_source
def test_AC11_상한_초과_limit_이_거부되고_total_이_전체를_드러낸다(auth_client):
    assert auth_client.get(
        "/api/layers/bronze/vegas_reservations?limit=201").status_code == 400
    body = auth_client.get("/api/layers/bronze/vegas_reservations?limit=10").json()
    assert body["total"] == 78216 and body["returned"] == 10


@requires_source
def test_AC16_tables_가_flows_to_와_source_group_을_싣는다(auth_client):
    body = auth_client.get("/api/layers/bronze/tables").json()
    by_name = {t["table"]: t for t in body["tables"]}
    assert by_name["vegas_reservations"]["source_group"] == "vegas"
    assert by_name["reviews"]["source_group"] == "review"
    assert by_name["nexus_branches"]["source_group"] == "nexus"
    assert by_name["vegas_reservations"]["flows_to"][0]["table"] == "reservations"
    assert by_name["vegas_reservations"]["masked"] is True

    # 컬럼 계약이 없는 테이블만 사유를 갖는다 — 그 외는 null 이라 화면이 구분할 수 있다
    assert by_name["nexus_branches"]["columns_note"]
    assert by_name["vegas_reservations"]["columns_note"] is None


@requires_source
def test_columns_note_는_계약_없는_테이블에만_붙는다(auth_client):
    gold = {t["table"]: t for t in auth_client.get("/api/layers/gold/tables").json()["tables"]}
    assert gold["gold_promo_calendar"]["columns_note"]
    assert gold["gold_kpi_daily"]["columns_note"] is None


@requires_source
def test_AC4_AC16_lineage_가_rule_id_gate_downstream_is_provisional_을_싣는다(auth_client):
    body = auth_client.get("/api/layers/gold/gold_kpi_daily/lineage").json()
    cols = {c["column"]: c for c in body["columns"]}
    noshow = cols["noshow_rate"]
    assert noshow["formula"] == "부도 ÷ (내원 + 부도)"
    assert noshow["gate"]
    assert noshow["source_columns"]
    assert noshow["downstream"]
    assert noshow["is_provisional"] is False
    assert "rule_id" in noshow                 # 골드는 규칙 ID 가 없어 null 이다
    assert noshow["rule_id"] is None
    assert noshow["status_thresholds"]["direction"] == "높을수록 나쁨"
    assert body["note_ref"]


@requires_source
def test_AC16_is_provisional_과_null_이_구분된다(auth_client):
    """미확정(관찰 60일 미확보)과 관측 없음은 다른 축이다."""
    body = auth_client.get(
        "/api/layers/gold/gold_retention_monthly/lineage").json()
    cols = {c["column"]: c for c in body["columns"]}
    assert cols["retention_rate"]["is_provisional"] is True
    assert cols["cohort_month"]["is_provisional"] is False


@requires_source
def test_없는_테이블은_404_UNKNOWN_TABLE(auth_client):
    r = auth_client.get("/api/layers/bronze/없는테이블")
    assert r.status_code == 404 and r.json()["detail"] == "UNKNOWN_TABLE"


@requires_source
def test_없는_필드_필터는_400_UNKNOWN_FIELD(auth_client):
    r = auth_client.get(
        '/api/layers/bronze/vegas_reservations?filters=[{"field":"secret","op":"eq","value":1}]')
    assert r.status_code == 400 and r.json()["detail"] == "UNKNOWN_FIELD"


@requires_source
def test_빈_결과가_에러가_아니라_200_빈_배열이다(auth_client):
    r = auth_client.get(
        '/api/layers/bronze/vegas_reservations?filters=[{"field":"chartNo","op":"eq","value":"없음"}]')
    assert r.status_code == 200
    assert r.json()["rows"] == [] and r.json()["total"] == 0


# --- AC-5 · AC-13 KPI --------------------------------------------------------


@requires_source
def test_AC5_series_값이_도구_query_kpi_와_오차_0(auth_client, built_db):
    """같은 함수를 지나므로 구조적으로 같다 — 그래도 계약으로 고정한다."""
    from service.queries import query_kpi

    api = auth_client.get(
        "/api/kpi/series?metrics=sales_total&metrics=visits&grain=daily"
        "&start=2026-08-01&end=2026-08-30").json()
    tool = query_kpi(built_db, metrics=["sales_total", "visits"], grain="daily",
                     start="2026-08-01", end="2026-08-30")
    assert api["rows"] == tool["rows"]
    assert api["source"] == tool["source"]


@requires_source
def test_AC13_cards_가_계약_필드를_전부_싣는다(auth_client):
    body = auth_client.get("/api/kpi/cards").json()
    assert body["period"] == "2026-08"
    assert body["has_next_period"] is False
    assert body["has_prev_period"] is True      # 기간 스테퍼 이전 화살표 근거
    assert body["window_days"] == 7
    card = next(c for c in body["cards"] if c["metric"] == "sales_total")
    for key in ("grain", "dod", "dod_pct", "unit", "format", "spark",
                "node_id", "thresholds", "direction", "alert_days", "node_state"):
        assert key in card, key
    assert len(card["spark"]) == 7
    assert card["node_id"] == "sales_total"


@requires_source
def test_AC13_카드마다_자기_그레인을_싣는다(auth_client):
    """일별 카드 행에 주별 지표(유기 신호)가 섞이므로 카드가 그레인을 갖는다."""
    cards = {c["metric"]: c for c in auth_client.get("/api/kpi/cards").json()["cards"]}
    assert cards["sales_total"]["grain"] == "daily"
    assert cards["gu_reviews"]["grain"] == "weekly"


@requires_source
def test_naver_reviews_카드는_상태를_갖지_않는다(auth_client):
    cards = {c["metric"]: c for c in auth_client.get("/api/kpi/cards").json()["cards"]}
    naver = cards["naver_reviews"]
    assert naver["status"] is None and naver["node_state"] is None
    assert naver["thresholds"] is None


@requires_source
def test_기간_스테퍼가_과거_기간에서_양방향으로_그려진다(auth_client):
    body = auth_client.get("/api/kpi/cards?period=2026-03").json()
    assert body["has_prev_period"] is True and body["has_next_period"] is True
    first = auth_client.get("/api/kpi/cards?period=2026-01").json()
    assert first["has_prev_period"] is False


@requires_source
def test_없는_지표는_400_UNKNOWN_METRIC(auth_client):
    r = auth_client.get(
        "/api/kpi/series?metrics=없는지표&grain=daily&start=2026-08-01&end=2026-08-05")
    assert r.status_code == 400 and r.json()["detail"] == "UNKNOWN_METRIC"


# --- AC-6 · AC-14 그래프 -----------------------------------------------------


@requires_source
def test_AC6_AC14_graph_가_계약_필드를_싣는다(auth_client):
    body = auth_client.get("/api/graph").json()
    assert len(body["nodes"]) == 25
    assert len(body["edges"]) == 21               # 기본 = 채택·자동 확정·선언
    assert body["counts"]["기각"] == 3

    edge = next(e for e in body["edges"] if e["edge_id"] == "cancel_rate__reservations")
    assert edge["kind"] == "causal" and edge["verdict"] == "채택"
    assert edge["note"] and edge["evidence"]
    assert edge["lag"] == "0d" and edge["lag_days"] == 0

    node = next(n for n in body["nodes"] if n["node_id"] == "reservations")
    assert node["source"]                          # 인스펙터 「원본 데이터 보기」 목적지
    assert node["node_state"] in ("정상", "관찰", "알림")


@requires_source
def test_AC6_기본_호출에_보류_기각이_오지_않는다(auth_client):
    body = auth_client.get("/api/graph").json()
    assert not [e for e in body["edges"] if e["verdict"] in ("보류", "기각")]
    explicit = auth_client.get("/api/graph?verdicts=기각").json()
    assert len(explicit["edges"]) == 3
    assert all(e["usable_for_causal_claim"] is False for e in explicit["edges"])


@requires_source
def test_AC6_미관측_노드는_observed_false(auth_client):
    body = auth_client.get("/api/graph").json()
    unobserved = [n for n in body["nodes"] if not n["observed"]]
    assert [n["node_id"] for n in unobserved] == ["foreign_inflow_channel"]


@requires_source
def test_AC14_lag_days_가_2w_를_14_로_병기한다(auth_client):
    body = auth_client.get("/api/graph").json()
    edge = next(e for e in body["edges"] if e["edge_id"] == "gu_reviews__new_patients")
    assert edge["lag"] == "2w" and edge["lag_days"] == 14


@requires_source
def test_노드_상태가_카드와_같은_기준으로_온다(auth_client):
    cards = {c["metric"]: c for c in auth_client.get("/api/kpi/cards").json()["cards"]}
    nodes = {n["node_id"]: n for n in auth_client.get("/api/graph").json()["nodes"]}
    for metric in ("sales_total", "cancel_rate", "new_patients"):
        assert nodes[metric]["node_state"] == cards[metric]["node_state"], metric
        assert nodes[metric]["alert_days"] == cards[metric]["alert_days"], metric


# --- AC-7 · AC-15 예보 -------------------------------------------------------


@requires_source
def test_AC7_AC15_forecast_가_확정_엣지_2건을_준다(auth_client):
    body = auth_client.get("/api/forecast").json()
    assert body["as_of"] == "2026-08-30"
    assert len(body["forecasts"]) == 2

    first = body["forecasts"][0]
    assert first["title"] == "예약 위험"
    assert first["edge"]["edge_id"] == "cancel_rate__reservations"
    assert first["edge"]["confidence"] == "중간"
    assert first["edge"]["lag"] == "0d" and first["edge"]["lag_days"] == 0
    assert "r=−0.583" in first["edge"]["evidence"]
    assert first["message"] and first["evidence"]

    second = body["forecasts"][1]
    assert second["edge"]["edge_id"] == "gu_reviews__new_patients"
    assert second["edge"]["confidence"] == "낮음"
    assert second["edge"]["lag"] == "2w" and second["edge"]["lag_days"] == 14
    assert "n=30" in second["edge"]["evidence"]
    assert "신뢰도 낮음" in second["note"]        # 낮은 신뢰도를 함께 준다


@requires_source
def test_AC15_예보_수치가_하드코딩이_아니라_DB_파생이다(auth_client, built_db):
    """엣지 행을 지우면 그 예보가 사라져야 한다 — 문장이 코드에 박혀 있지 않다는 증거."""
    from service import monitoring

    body = monitoring.forecast(built_db)
    assert len(body["forecasts"]) == 2
    built_db.execute("DELETE FROM ontology_edges WHERE cause = 'gu_reviews'")
    try:
        assert len(monitoring.forecast(built_db)["forecasts"]) == 1
    finally:
        built_db.rollback()


# --- AC-12 · 기타 -------------------------------------------------------------


@requires_source
def test_AC12_응답_어디에도_실시간_표기가_없다(auth_client):
    """데이터는 일 1회 갱신이다(DEC-005 D4)."""
    for path in GUARDED:
        assert "실시간" not in auth_client.get(path).text, path


@requires_source
def test_백엔드가_static_페이지를_내보내지_않는다(client):
    """백은 API 서버다(DEC-004 D3)."""
    paths = [r.path for r in client.app.routes if hasattr(r, "path")]
    assert not any(p.startswith("/static") for p in paths)
    assert all(p.startswith(("/api", "/health", "/openapi", "/docs", "/redoc"))
               for p in paths), paths


@requires_source
def test_빌드_표식이_없는_DB_는_서빙되지_않는다(monkeypatch, tmp_path):
    """실패 빌드를 정상처럼 서빙하지 않는다 — 빈 골드를 「데이터 없음」으로 오독하지 않게."""
    import sqlite3

    from db.schema import bootstrap

    path = tmp_path / "unbuilt.db"
    conn = sqlite3.connect(path)
    bootstrap(conn)
    conn.commit()
    conn.close()

    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", path)
    monkeypatch.setattr(settings, "session_cookie_secure", False)
    import main

    with TestClient(main.app) as c:
        c.post("/api/auth/session", json={"password": TEST_PASSWORD})
        r = c.get("/api/kpi/cards")
        assert r.status_code == 503
        assert r.json()["detail"] == "SOURCE_UNAVAILABLE"
        assert c.get("/api/meta/build").json()["built"] is False
