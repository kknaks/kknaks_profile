"""WORK-002 검수 지적의 회귀 테스트 — 「다시 풀리면 여기서 잡힌다」.

각 테스트가 리포트의 항목 번호를 달고 있다. 고친 것이 아니라 **다시 못 풀리게 한 것**이
이 파일의 목적이다.
"""

from __future__ import annotations

import sqlite3

import pytest
from fastapi.testclient import TestClient

from config import settings
from service import allowlist as al
from service import glossary
from service.queries import trace_ontology
from tests.conftest import TEST_PASSWORD, requires_source


# --- F1. source_group 은 브론즈 전용 ----------------------------------------


def test_F1_실버_골드_온톨로지는_source_group_이_없다():
    """SPEC-003 v0.0.8 §4 — 허용값은 vegas·review·nexus 이고 **실버·골드는 null**.

    실버에 실으면 FE 가 칩을 3개로 접어(`source_group ?? table`) 계층 탭 카운트 6과
    어긋난다. 2단 구조는 브론즈에만 규정됐다(SPEC-004 U-13).
    """
    for layer in ("silver", "gold", "ontology"):
        offenders = [(t.table, t.source_group) for t in al.tables_of(layer) if t.source_group]
        assert offenders == [], f"{layer} 에 source_group 이 실렸다: {offenders}"


def test_F1_브론즈만_source_group_을_갖고_허용값_안이다():
    groups = {t.table: t.source_group for t in al.tables_of("bronze")}
    assert groups["vegas_reservations"] == "vegas"
    assert groups["reviews"] == "review"
    assert all(g == "nexus" for t, g in groups.items() if t.startswith("nexus_"))
    assert set(groups.values()) <= {"vegas", "review", "nexus"}
    assert all(groups.values()), "브론즈는 전 테이블이 원천 축을 갖는다"


@requires_source
def test_F1_API_응답에서도_실버_골드가_null_이다(auth_client):
    for layer in ("silver", "gold"):
        tables = auth_client.get(f"/api/layers/{layer}/tables").json()["tables"]
        assert tables, layer
        assert all(t["source_group"] is None for t in tables), (
            f"{layer} 응답에 source_group 이 실렸다: "
            f"{[(t['table'], t['source_group']) for t in tables if t['source_group']]}")


# --- W4. 비밀번호 미주입 시 세션 위조 ----------------------------------------


def test_W4_비밀번호_미주입이면_어떤_토큰도_검증되지_않는다(monkeypatch):
    """미주입이면 서명 키가 `sha256(b"ontology-demo-session|")` 라는 **레포에 적힌 상수**가 된다.

    발급 경로는 503 으로 막혀 있지만 검증 경로가 뚫려 있으면 발급이 필요 없다 —
    누구나 오프라인에서 유효한 토큰을 만들어 전 조회 API 를 연다.
    """
    from api import deps

    monkeypatch.setattr(settings, "demo_password", "정상비밀번호")
    forged = deps.issue_session()
    assert deps.verify_session(forged) is True          # 비번이 있을 때는 유효

    monkeypatch.setattr(settings, "demo_password", "")
    assert deps.verify_session(forged) is False
    # 공개 상수 키로 새로 만든 토큰도 통하지 않는다
    assert deps.verify_session(deps.issue_session()) is False


@requires_source
def test_W4_env_미주입_상태에서는_전_API_가_닫힌다(built_db_path, monkeypatch):
    """정상 세션을 받아 둔 뒤 env 가 사라져도 그 쿠키로 조회가 되면 안 된다."""
    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "session_cookie_secure", False)
    import main

    with TestClient(main.app) as c:
        assert c.post("/api/auth/session", json={"password": TEST_PASSWORD}).status_code == 200
        assert c.get("/api/kpi/cards").status_code == 200

        monkeypatch.setattr(settings, "demo_password", "")   # env 미주입 사고
        assert c.get("/api/kpi/cards").status_code == 401
        assert c.get("/api/auth/session").status_code == 401


# --- W5. 단계 단독 실행이 남기는 stale 표식 ----------------------------------


@requires_source
def test_W5_단계_단독_실행은_빌드_표식을_무효화한다(built_db_path, tmp_path):
    """게이트 없이 골드를 다시 쓴 뒤에도 표식이 「1,2,3 통과」라고 말하면
    **표식이 거짓을 말하는 유일한 경로**가 된다."""
    import shutil

    from build.__main__ import main as build_main
    from db.connection import BuildIncomplete, build_stamp, connect_ro

    path = tmp_path / "staged.db"
    shutil.copy(built_db_path, path)

    conn = sqlite3.connect(path)
    assert build_stamp(conn) is not None, "복제본에 표식이 있어야 전제가 성립한다"
    conn.close()

    assert build_main(["gold", "--db", str(path)]) == 0

    conn = sqlite3.connect(path)
    try:
        assert build_stamp(conn) is None, "단계 단독 실행 뒤에도 표식이 남았다"
    finally:
        conn.close()
    with pytest.raises(BuildIncomplete):
        connect_ro(path)


@requires_source
def test_W5_게이트_단독_재실행은_표식을_건드리지_않는다(built_db_path, tmp_path):
    """게이트는 읽기만 한다 — WORK-005 전건 재실행이 표식을 날리면 안 된다."""
    import shutil

    from build.__main__ import main as build_main
    from db.connection import build_stamp

    path = tmp_path / "gated.db"
    shutil.copy(built_db_path, path)
    for stage in ("gate1", "gate2", "gate3"):
        assert build_main([stage, "--db", str(path)]) == 0

    conn = sqlite3.connect(path)
    try:
        assert build_stamp(conn) is not None, f"{stage} 가 표식을 지웠다"
    finally:
        conn.close()


@requires_source
def test_W5_all_은_표식을_다시_찍는다(built_db_path, tmp_path):
    """무효화만 하고 복구가 안 되면 그것대로 고장이다 — 반대 방향도 고정한다."""
    import shutil

    from build.__main__ import main as build_main
    from db.connection import build_stamp

    path = tmp_path / "rebuild.db"
    shutil.copy(built_db_path, path)
    assert build_main(["gold", "--db", str(path)]) == 0
    assert build_main(["all", "--db", str(path)]) == 0

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        stamp = build_stamp(conn)
        assert stamp is not None and stamp["gates_passed"] == "1,2,3"
    finally:
        conn.close()


# --- W3. /api/meta/build 가 세션 뒤에 있다 -----------------------------------


@requires_source
def test_W3_meta_build_도_세션을_요구한다(client):
    """AC-1 「세션 없이 부른 **모든** API 가 401」의 예외를 늘리지 않는다.

    `auth_client` 는 `client` 를 그대로 로그인시켜 돌려주므로 둘을 함께 받으면
    안 된다 — 같은 객체라 미인증 검사가 성립하지 않는다.
    """
    assert client.get("/api/meta/build").status_code == 401
    client.post("/api/auth/session", json={"password": TEST_PASSWORD})
    assert client.get("/api/meta/build").json()["built"] is True


# --- W6. get_definition 이 enum 13종 전부에 닿는다 ---------------------------


@pytest.mark.parametrize("key", sorted(glossary.ENUMS))
def test_W6_enum_13종이_전부_조회된다(key):
    """SPEC-002 OQ-5 — 「글로서리 판정 표 + KPI 컬럼 + **enum**」.

    예전에는 Term 의 **첫 별칭**이 ENUMS 키와 같을 때만 실려 13종 중 2종만 닿았다.
    """
    payload = glossary.definition_payload(key)
    assert payload["enum_values"] == glossary.ENUMS[key]
    assert payload["definition"], f"{key} 에 설명이 없다"
    assert payload["source_note"]


def test_W6_한글_용어로_물어도_enum_이_함께_온다():
    assert glossary.definition_payload("리뷰 감성")["enum_values"] == glossary.ENUMS["sentiment"]
    assert glossary.definition_payload("시술 개념")["enum_values"] == \
        glossary.ENUMS["procedure_concept"]


def test_W6_enum_키가_유사_후보에도_뜬다():
    assert "visit_status" in glossary.suggestions("visit")


# --- W7. note 와 reason 이 배타적이다 ----------------------------------------


@requires_source
def test_W7_기각_보류_엣지는_note_가_비고_reason_만_온다(built_db):
    """둘 다 `rationale` 에서 나오므로 같이 채우면 인스펙터가 같은 문장을 두 번 찍는다."""
    result = trace_ontology(built_db, verdicts=["기각", "보류"])
    assert len(result["edges"]) == 6
    for edge in result["edges"]:
        assert edge["reason"], edge["edge_id"]
        assert edge["note"] is None, f"{edge['edge_id']} 에서 note 와 reason 이 겹친다"


@requires_source
def test_W7_채택_엣지는_note_만_오고_reason_은_비어_있다(built_db):
    result = trace_ontology(built_db)
    assert result["edges"]
    for edge in result["edges"]:
        assert edge["reason"] is None
    assert any(e["note"] for e in result["edges"])


# --- nit 6. sign 이 정본 원형(U+2212)이다 ------------------------------------


@requires_source
def test_nit6_음의_부호가_유니코드_마이너스_원형이다(built_db):
    """ASCII '-' 와 눈으로는 같아 보여서 어긋나도 드러나지 않는 자리다(spec 경고)."""
    result = trace_ontology(built_db, verdicts=list(al.VERDICTS))
    signs = {e["sign"] for e in result["edges"] if e["sign"]}
    assert "−" in signs, f"U+2212 가 없다: {signs!r}"
    assert "-" not in signs, "ASCII 하이픈으로 치환됐다"


# --- nit 4. term 길이 검증 ---------------------------------------------------


def test_nit4_term_상한을_넘으면_거부된다():
    from tools.server import get_definition

    assert get_definition("가" * 101)["error"] == "INVALID_RANGE"
    assert get_definition("   ")["error"] == "INVALID_RANGE"
    assert get_definition("노쇼율")["term"] == "노쇼율"


# --- nit 2. horizon 은 일 단위 ------------------------------------------------


@requires_source
def test_nit2_forecast_horizon_이_일_단위다(built_db):
    from service import monitoring

    forecasts = monitoring.forecast(built_db)["forecasts"]
    horizons = {f["edge"]["edge_id"]: f["horizon"] for f in forecasts}
    assert horizons["cancel_rate__reservations"] == "0d"
    # lag 는 정본 원형 "2w" 를 유지하되 horizon 은 일 단위로 낸다
    assert horizons["gu_reviews__new_patients"] == "14d"
    lags = {f["edge"]["edge_id"]: f["edge"]["lag"] for f in forecasts}
    assert lags["gu_reviews__new_patients"] == "2w"


@requires_source
def test_nit3_message_에_동시점_재서술이_없다(built_db):
    from service import monitoring

    for f in monitoring.forecast(built_db)["forecasts"]:
        assert "동시점" not in f["message"]
