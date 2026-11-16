"""WORK-005 P1 — 게이트 1~5 전건 재실행과 **PII 전면 스캔**.

각 WP 가 자기 게이트를 통과했더라도, 합쳐 놓은 상태에서 다시 돌려야 배포 가능
여부를 말할 수 있다. 이 파일이 그 「한 번의 실행」이다.

## 게이트 배치

| 게이트 | 무엇 | 어디 |
|---|---|---|
| 1 | 브론즈 행수 대사 | 여기(`test_게이트1_*`) — `load_bronze.gate1` 직접 호출 |
| 2 | 빌드 재현 대조 | 여기(`test_게이트2_*`) — `gates.gate2` + `csv_parity` |
| 3 | 마스킹 뷰 원값 0건 | 여기(`test_게이트3_*`) — `gates.gate3` |
| 3+ | **표면 전수 PII 스캔** | 여기(`test_PII_*`) — API·MCP·채팅·로그 |
| 4 | 회귀 3본 | `test_w003_regression.py` — 기준값 계층은 항상, 라이브는 플래그 |
| 5 | 근거 무결성 ①②③ | `test_w003_answer.py` + 라이브 회귀의 `validate()` |

## PII 스캔이 값을 뒤지는 방향

needle 수만 6만 건이라 「원값을 응답에서 찾는다」로 짜면 못 돈다. 방향을 뒤집어
**응답의 문자열 잎을 전부 뽑아 원값 집합에 있는지 조회한다**(O(1)). 마스킹된 값은
정의상 원값과 같을 수 없으므로 집합 적중이 곧 유출이다.

**리포트에 원값을 쓰지 않는다.** 실패 메시지는 건수와 위치(표면·경로·키)만 남긴다 —
게이트 리포트가 새로운 유출 경로가 되면 안 된다.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from pathlib import Path

import pytest

from build import gates, load_bronze
from build.masking import staff_names
from build.spec_contract import (
    BRONZE_VISITS,
    REBUILD_ROWCOUNTS,
    REBUILD_TOTALS,
    VISIT_DEDUP_DELTA,
)
from service import allowlist as al
from service import glossary
from tests.conftest import requires_source

# --- 게이트 1~3 전건 재실행 -------------------------------------------------


@requires_source
def test_게이트1_브론즈_16테이블_대사_오차_0(built_db):
    """AC-1 — 원천을 다시 세어 적재본과 대조한다. 오차 0."""
    recon = load_bronze.gate1(built_db)
    assert len(recon) == 16, f"브론즈 테이블 16종이 아니라 {len(recon)}종"
    for table, (src, got) in recon.items():
        assert src == got, f"{table}: 원본 {src:,} vs 적재 {got:,}"
    print(f"\n[게이트 1] {len(recon)}테이블 오차 0 "
          f"· vegas {recon['bronze_vegas_reservations'][1]:,}행")


@requires_source
def test_게이트2_빌드_재현_수치가_SPEC_대조값과_정확히_일치한다(built_db):
    """AC-2 — 완료 증거의 수치를 그대로 단언한다."""
    result = gates.gate2(built_db)
    measured = result["measured"]

    assert measured["매출 합(예외 1건 제외)"] == 2_615_555_218
    assert measured["결제 내원"] == 5_428
    assert measured["신환"] == 3_447
    assert measured["총 내원(실버 기준)"] == 47_537
    assert measured["gold_kpi_daily 행수"] == 235

    # 계약 표와도 대조 — 위 리터럴이 표에서 떨어져 나가지 않게
    for name, want in REBUILD_TOTALS.items():
        assert measured[name] == want
    for table, want in REBUILD_ROWCOUNTS.items():
        assert measured[f"{table} 행수"] == want
    assert measured["브론즈 내원 대사(실버 + 내원 중복)"] == BRONZE_VISITS
    assert measured["총 내원(실버 기준)"] + VISIT_DEDUP_DELTA == BRONZE_VISITS

    parity = gates.csv_parity(built_db)
    assert parity["diffs"] == 0, f"기존 CSV 산출물과 {parity['diffs']}셀 불일치"

    print(f"\n[게이트 2] 대조 {result['checks']}항 전항 일치 · 매출 "
          f"{measured['매출 합(예외 1건 제외)']:,} · 결제 내원 {measured['결제 내원']:,} "
          f"· 신환 {measured['신환']:,} · 내원 {measured['총 내원(실버 기준)']:,} "
          f"· 일별 {measured['gold_kpi_daily 행수']}행 "
          f"· CSV {parity['tables']}테이블 {parity['cells']:,}셀 불일치 {parity['diffs']}건")


@requires_source
def test_게이트3_마스킹_뷰_원값_검출_0건(built_db):
    """AC-7 — 뷰 4종(값 대조 2 · 스키마 검사 2)에서 원값 0건."""
    result = gates.gate3(built_db)
    assert result["leaks"] == 0
    assert result["views_scanned"] == 4
    print(f"\n[게이트 3] 원값 {result['leaks']}건 "
          f"· vegas {result['vegas_rows']:,}행 · 리뷰 {result['review_rows']:,}행 전수")


# --- PII 전면 스캔 ----------------------------------------------------------

#: 마스킹 대상 컬럼 — 키 이름으로 잡히는 자리는 표기 규약까지 본다.
PII_KEYS = ("patientName", "phone", "birthday")

#: SPEC-001 §4 표기 규약. 빈 문자열은 원천이 비어 있던 자리다.
MASK_PATTERNS = {
    "patientName": re.compile(r"^$|^.○+$|^○$"),
    "phone": re.compile(r"^$|^.{3}-\*{4}-.{4}$|^\*+$"),
    "birthday": re.compile(r"^$|^\d{4}-\*\*-\*\*$"),
}

#: 본문 스캔 하한 — 이보다 짧은 문자열에 실명 사전을 부분 일치시키면 라벨·용어가 걸린다.
BODY_MIN_LEN = 20


@pytest.fixture(scope="module")
def auth_client_session(tmp_path_factory, built_db_path):
    """세션 통과 클라이언트 하나를 모듈 내내 공유한다 — 표면 전수 순회를 세 번 돌지 않는다.

    제출은 막는다. PII 스캔이 보는 것은 저장·조회 표면이지 LLM 왕복이 아니다
    (라이브 답변은 게이트 4·5 회귀가 본다).
    """
    from fastapi.testclient import TestClient

    from agent import runtime
    from config import settings
    from tests.conftest import TEST_PASSWORD

    chat_db = tmp_path_factory.mktemp("w005") / "chat.db"
    saved = (settings.demo_password, settings.db_path, settings.chat_db_path,
             settings.session_cookie_secure, runtime.start_turn)

    async def _no_submit(**kwargs):
        return None

    settings.demo_password = TEST_PASSWORD
    settings.db_path = built_db_path
    settings.chat_db_path = chat_db
    settings.session_cookie_secure = False
    runtime.start_turn = _no_submit
    import main

    try:
        with TestClient(main.app) as c:
            r = c.post("/api/auth/session", json={"password": TEST_PASSWORD})
            assert r.status_code == 200
            yield c
    finally:
        (settings.demo_password, settings.db_path, settings.chat_db_path,
         settings.session_cookie_secure, runtime.start_turn) = saved


#: 이름 needle 겹침 상한. 이 수를 넘으면 「뺐더니 스캔이 무력해진 것」과
#: 「원래 안 겹치는 것」을 구분할 수 없어 게이트가 게이트가 아니게 된다.
MAX_NAME_COLLISIONS = 10


def _distinct(conn, table: str, column: str) -> set[str]:
    return {
        r[0] for r in conn.execute(
            f'SELECT DISTINCT "{column}" FROM {table} '
            f'WHERE "{column}" IS NOT NULL AND "{column}" <> ""')
    }


def _name_collisions(conn, names: set[str]) -> dict[str, list[str]]:
    """마스킹 대상이 **아닌** 관계에 원래 있는 글자열 → 그 위치.

    「환자명이 마스킹을 뚫고 나왔다」와 「같은 글자열이 마스터 데이터에 원래 있다」를
    값만 보고는 구분할 수 없다. 그래서 후자를 needle 에서 빼되, **어디서 겹쳤는지를
    남기고 건수에 상한을 둔다** — 조용히 빼면 스캔이 스스로를 갉아먹는다.
    """
    collisions: dict[str, list[str]] = {}
    for layer in al.LAYERS:
        for spec in al.tables_of(layer):
            if "patientName" in spec.masked_fields:
                continue
            for _, column, ctype, *_ in conn.execute(f"PRAGMA table_info({spec.relation})"):
                if "CHAR" not in ctype.upper() and "TEXT" not in ctype.upper() and ctype:
                    continue
                for hit in _distinct(conn, spec.relation, column) & names:
                    collisions.setdefault(hit, []).append(f"{spec.relation}.{column}")
    return collisions


@pytest.fixture(scope="session")
def raw_pii(built_db) -> dict:
    """원값 집합. **이 픽스처 밖으로 값을 흘리지 않는다** — 건수와 위치만 로그에 나간다.

    `staff`·`authorName` 은 마스킹 대상이 아니다(SPEC-001 §4 — 작성자명은 원천이 이미
    닉네임, 담당자명은 PII 컬럼이 아니다). 환자명과 글자열이 겹칠 수 있어 needle 에서
    빼 둔다 — 안 빼면 정상 응답이 유출로 잡힌다. 같은 이유로 마스킹 대상이 아닌
    관계와 겹치는 이름도 뺀다(`_name_collisions`).
    """
    names = {n for n in _distinct(built_db, "bronze_vegas_reservations", "patientName")
             if len(n) >= 2}
    names -= _distinct(built_db, "bronze_vegas_reservations", "staff")
    names -= _distinct(built_db, "bronze_reviews", "authorName")

    collisions = _name_collisions(built_db, names)
    assert len(collisions) <= MAX_NAME_COLLISIONS, (
        f"이름 needle 이 마스킹 밖 관계와 {len(collisions)}종 겹친다 — 스캔이 무력해진다\n"
        + "\n".join(f"  {loc}" for locs in collisions.values() for loc in locs))

    needles = {
        "patientName": names - set(collisions),
        "phone": {p for p in _distinct(built_db, "bronze_vegas_reservations", "phone")
                  if len(p) >= 8},
        "birthday": {b for b in _distinct(built_db, "bronze_vegas_reservations", "birthday")
                     if len(b) >= 8},
        # 리뷰 본문에서 `[직원]` 으로 덮여야 하는 실명 사전
        "staff_tokens": set(staff_names(built_db)),
        "name_collisions": collisions,
    }
    where = sorted({loc for locs in collisions.values() for loc in locs})
    print(f"\n[PII needle] 이름 {len(needles['patientName']):,}종 · 전화 "
          f"{len(needles['phone']):,}종 · 생년월일 {len(needles['birthday']):,}종 "
          f"· 실명 사전 {len(needles['staff_tokens'])}종\n"
          f"[PII needle] 마스킹 밖 겹침 {len(collisions)}종 제외 — {where}")
    return needles


def _leaves(node, path: str = "$"):
    """JSON 트리의 (경로, 키, 문자열값) 잎 전부."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _leaves(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _leaves(value, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, path.rsplit(".", 1)[-1].split("[")[0], node


def scan(payload, needles: dict, surface: str) -> list[str]:
    """한 응답의 유출 목록. **원값은 담지 않는다** — 표면·경로·키만."""
    leaks: list[str] = []
    for path, key, value in _leaves(payload):
        if key in PII_KEYS and not MASK_PATTERNS[key].match(value):
            leaks.append(f"{surface} {path}: {key} 표기 규약 위반")
        if value in needles["phone"]:
            leaks.append(f"{surface} {path}: 전화 원값")
        if value in needles["birthday"]:
            leaks.append(f"{surface} {path}: 생년월일 원값")
        if value in needles["patientName"]:
            leaks.append(f"{surface} {path}: 환자명 원값")
        if len(value) >= BODY_MIN_LEN:
            for token in needles["staff_tokens"]:
                if token in value:
                    leaks.append(f"{surface} {path}: 직원 실명 토큰 잔존")
                    break
    return leaks


def _json(response) -> dict:
    assert response.status_code == 200, f"{response.request.url} → {response.status_code}"
    return response.json()


@pytest.fixture(scope="module")
def api_surfaces(auth_client_session) -> list[tuple[str, dict]]:
    """스캔 대상 **API 표면 전수**. 하나라도 빠지면 스캔이 스캔이 아니다.

    - 인증: `GET /api/auth/session`
    - 메타: `GET /api/meta/build`
    - 모니터링: `/api/kpi/cards` · `/api/kpi/series` · `/api/graph` · `/api/forecast`
    - 계층: 4계층 `tables` + **허용 목록 전 테이블**의 rows · lineage
    - 채팅: 목록 + 대화 상세(생성 직후 pending 1건)
    """
    client = auth_client_session
    surfaces: list[tuple[str, dict]] = [
        ("GET /api/auth/session", _json(client.get("/api/auth/session"))),
        ("GET /api/meta/build", _json(client.get("/api/meta/build"))),
        ("GET /api/kpi/cards", _json(client.get("/api/kpi/cards"))),
        ("GET /api/kpi/series", _json(client.get(
            "/api/kpi/series?metrics=sales_total&metrics=noshow_rate&grain=daily"
            "&start=2026-08-01&end=2026-08-30&include_deltas=true"))),
        ("GET /api/graph", _json(client.get("/api/graph"))),
        ("GET /api/forecast", _json(client.get("/api/forecast"))),
    ]
    for layer in al.LAYERS:
        surfaces.append((f"GET /api/layers/{layer}/tables",
                         _json(client.get(f"/api/layers/{layer}/tables"))))
        for spec in al.tables_of(layer):
            base = f"/api/layers/{layer}/{spec.table}"
            surfaces.append((f"GET {base} (limit 200)",
                             _json(client.get(f"{base}?limit={al.MAX_LIMIT}"))))
            surfaces.append((f"GET {base}/lineage", _json(client.get(f"{base}/lineage"))))

    created = client.post("/api/chat/conversations", json={"question": "PII 스캔용 질문"})
    assert created.status_code == 201
    conversation_id = created.json()["conversation"]["id"]
    surfaces.append(("GET /api/chat/conversations", _json(client.get("/api/chat/conversations"))))
    surfaces.append((f"GET /api/chat/conversations/{{id}}",
                     _json(client.get(f"/api/chat/conversations/{conversation_id}"))))
    return surfaces


@requires_source
def test_PII_API_표면_전수에_원값이_없다(api_surfaces, raw_pii):
    leaks: list[str] = []
    for name, payload in api_surfaces:
        leaks += scan(payload, raw_pii, name)
    assert not leaks, f"API 표면 원값 검출 {len(leaks)}건:\n" + "\n".join(leaks[:20])
    print(f"\n[PII · API] {len(api_surfaces)}표면 원값 0건")


@requires_source
def test_PII_스캔이_열거한_API_표면에_빠진_라우트가_없다(api_surfaces):
    """「표면 목록이 빠짐없이 열거돼 있다」를 앱 라우트 표와 대조한다.

    스캔 목록을 손으로 적어 두면 라우트가 늘어난 날 조용히 구멍이 생긴다.
    """
    import main

    routed = {
        (method, route.path)
        for route in main.app.routes
        for method in getattr(route, "methods", set())
        if route.path.startswith("/api") and method in ("GET", "POST")
    }
    # 스캔이 실제로 부른 경로 — 경로 파라미터는 템플릿으로 되돌려 비교한다
    scanned = set()
    for name, _ in api_surfaces:
        method, path = name.split(" ", 1)
        path = path.split(" (")[0].split("?")[0]
        scanned.add((method, path))

    #: 스캔에서 뺀 라우트와 사유. 「안 봤다」가 아니라 「이래서 안 본다」를 적는다.
    excluded = {
        ("POST", "/api/auth/session"): "세션 발급 — 응답에 데이터가 없다(스캔 대상은 GET)",
        ("DELETE", "/api/auth/session"): "세션 파기 — 본문이 없다",
        ("POST", "/api/chat/conversations"): "생성은 픽스처가 부르고 결과를 GET 으로 스캔한다",
        ("POST", "/api/chat/conversations/{conversation_id}/messages"):
            "이어 질문 — 응답 shape 가 대화 상세와 같다",
        ("POST", "/api/chat/conversations/{conversation_id}/messages/{message_id}/retry"):
            "재시도 — 응답 shape 가 대화 상세와 같다",
    }
    template = {
        ("GET", "/api/layers/{layer}/tables"),
        ("GET", "/api/layers/{layer}/{table}"),
        ("GET", "/api/layers/{layer}/{table}/lineage"),
        ("GET", "/api/chat/conversations/{conversation_id}"),
    }
    covered = scanned | set(excluded) | template
    missing = {
        (m, p) for (m, p) in routed
        if (m, p) not in covered and not p.startswith("/api/layers/")
        and not p.startswith("/api/chat/conversations/")
    }
    assert not missing, f"스캔 목록에 없는 라우트: {sorted(missing)}"


@requires_source
def test_PII_MCP_도구_4종_응답에_원값이_없다(built_db_path, monkeypatch, raw_pii):
    """도구는 워커가 부르는 표면이라 API 게이트 뒤에 있지 않다 — 따로 스캔한다."""
    from config import settings

    monkeypatch.setattr(settings, "db_path", built_db_path)
    import tools.server as server

    payloads: list[tuple[str, dict]] = [
        ("query_kpi(daily)", server.query_kpi(
            metrics=["sales_total", "visits", "noshow_rate"], grain="daily",
            start="2026-08-01", end="2026-08-30", include_deltas=True)),
        ("trace_ontology(all)", server.trace_ontology(
            direction="both", depth=2,
            verdicts=["채택", "자동 확정", "선언", "보류", "기각"])),
    ]
    for layer in ("bronze", "silver"):
        for spec in al.tables_of(layer):
            payloads.append((f"query_layer({layer}.{spec.table})", server.query_layer(
                layer=layer, table=spec.table, limit=al.MAX_LIMIT)))
    for term in glossary.all_terms():
        payloads.append((f"get_definition({term})", server.get_definition(term)))

    leaks: list[str] = []
    for name, payload in payloads:
        leaks += scan(payload, raw_pii, name)
    assert not leaks, f"MCP 도구 원값 검출 {len(leaks)}건:\n" + "\n".join(leaks[:20])
    print(f"\n[PII · MCP] 도구 4종 {len(payloads)}호출 원값 0건")


@requires_source
def test_PII_드릴다운_경로가_마스킹_표기만_돌려준다(built_db_path, monkeypatch, raw_pii):
    """R-3 이 밟는 길 — 8월 취소 원본 20행. 에이전트 답변의 `drilldown` 이 이 결과다."""
    from config import settings

    monkeypatch.setattr(settings, "db_path", built_db_path)
    import tools.server as server

    payload = server.query_layer(
        layer="bronze", table="vegas_reservations",
        filters=[{"field": "visitStatus", "op": "eq", "value": "취소"}], limit=20)
    rows = payload["rows"]
    assert len(rows) == 20
    assert not scan(payload, raw_pii, "drilldown")
    for row in rows:
        assert "○" in row["patientName"] or row["patientName"] == ""
        assert row["phone"] == "" or "*" in row["phone"]
        assert row["birthday"] == "" or row["birthday"].endswith("-**-**")
    print(f"\n[PII · 드릴다운] {len(rows)}행 마스킹 표기 · 원값 0건")


@requires_source
def test_PII_채팅_저장소에_원값이_없다(auth_client_session, raw_pii):
    """답변 본문·단계·결과가 앉는 자리. 라이브 답변도 같은 행에 저장된다."""
    from agent import store

    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM messages")]
        conversations = [dict(r) for r in conn.execute("SELECT * FROM conversations")]
    assert rows, "스캔할 메시지가 없다 — 픽스처가 대화를 만들지 않았다"
    leaks = scan(rows, raw_pii, "chat.messages") + scan(conversations, raw_pii, "chat.conversations")
    assert not leaks, f"채팅 저장소 원값 검출 {len(leaks)}건:\n" + "\n".join(leaks[:20])
    print(f"\n[PII · 채팅] 대화 {len(conversations)}건 · 메시지 {len(rows)}건 원값 0건")


#: 마스킹 대상이 **아닌** 자리에 환자명과 같은 글자열이 앉아 있는 알려진 위치.
#: 여기 없는 자리가 새로 겹치면 실패한다 — 상한(10)만 두면 새 겹침이 조용히 들어온다.
#:
#: 분류(값은 적지 않는다):
#: - `bronze_nexus_branches.representative_name` — 지점 대표자명(사업자 마스터).
#:   마스킹 대상이 아니다. 환자 목록에 같은 이름이 있어 겹친다.
#: - `silver_catalog.name` · `gold_promo_calendar.title` ·
#:   `bronze_nexus_*.name`/`title`/`prefix`/`subtitle` · `silver_promotions.title`
#:   — 시술·프로모션 이름의 **테스트 레코드**. 환자명에도 같은 테스트 값이 있다.
#:
#: ~~`v_silver_reservations.chart_no`~~ — 차트번호 자리에 이름 문자열이 들어간 원천 오염
#: 1건이었다. **needle 예외로 두지 않고 게이트 3 위반으로 판정해 고쳤다**(WORK-005) —
#: 뷰가 숫자 아닌 차트번호를 `[비정형]`으로 덮는다. 그래서 이 자리는 목록에 없다.
KNOWN_NAME_COLLISION_SITES = {
    "bronze_nexus_branches.representative_name",
    "bronze_nexus_category_translations_ko.name",
    "bronze_nexus_event_procedure_groups.name",
    "bronze_nexus_event_procedure_products_ko.name",
    "bronze_nexus_promotion_v2s.prefix",
    "bronze_nexus_promotion_v2s.subtitle",
    "bronze_nexus_promotion_v2s.title",
    "gold_promo_calendar.title",
    "silver_catalog.name",
    "silver_promotions.title",
}


@requires_source
def test_PII_마스킹_밖_이름_겹침이_알려진_자리_밖으로_늘지_않았다(raw_pii):
    """needle 에서 뺀 자리를 고정한다 — 뺀 것이 늘면 스캔이 스스로를 갉아먹는다."""
    sites = {loc for locs in raw_pii["name_collisions"].values() for loc in locs}
    assert sites == KNOWN_NAME_COLLISION_SITES, (
        f"새 겹침 {sorted(sites - KNOWN_NAME_COLLISION_SITES)} · "
        f"사라진 겹침 {sorted(KNOWN_NAME_COLLISION_SITES - sites)}")


@requires_source
def test_PII_로그에_원값이_남지_않는다(built_db_path, monkeypatch, caplog, capfd, raw_pii):
    """게이트·도구·거부 경로가 내보내는 출력 전부 — `logging` 과 **stdout 리포트** 둘 다.

    게이트 리포트는 `print` 로 컨테이너 stdout 에 나간다. 배포 로그가 곧 이 문자열이라
    `caplog` 만 보면 실제 로그의 절반을 안 본 것이 된다. 그래서 **빌드 CLI 를 그대로
    태우고**(배포에서 사람이 부르는 진입점) 파일 서술자 수준에서 받아 낸다 —
    `capsys` 는 `report(stream=sys.stdout)` 처럼 임포트 시점에 묶인 참조를 놓친다.
    """
    from build.__main__ import main as build_main
    from config import settings

    monkeypatch.setattr(settings, "db_path", built_db_path)
    import tools.server as server

    caplog.set_level(logging.DEBUG)
    capfd.readouterr()  # 픽스처가 찍어 둔 앞선 출력은 버린다
    for stage in ("gate1", "gate2", "gate3"):
        assert build_main([stage, "--db", str(built_db_path)]) == 0
    # 거부 경로도 로그를 찍는다(`_fail`) — 그쪽도 본다
    server.query_layer(layer="bronze", table="vegas_reservations",
                       filters=[{"field": "patientName", "op": "eq", "value": "무엇이든"}])
    server.get_definition("없는용어")

    captured = capfd.readouterr()
    assert captured.out, "게이트 CLI 가 아무것도 찍지 않았다 — 스캔할 로그가 없다"
    text = "\n".join(
        [record.getMessage() for record in caplog.records] + [captured.out, captured.err])
    hits = [
        kind for kind in ("phone", "birthday", "patientName")
        if any(needle in text for needle in raw_pii[kind])
    ]
    assert not hits, f"로그에 원값 잔존: {hits}"
    print(f"\n[PII · 로그] logging {len(caplog.records)}레코드 + 게이트 CLI stdout "
          f"{len(captured.out):,}자 원값 0건")


@requires_source
def test_비밀번호가_응답과_쿠키_어디에도_없다(auth_client_session, api_surfaces):
    """배포 전 체크리스트 6 — 값이 응답·쿠키 어디에도 없다.

    레포·문서 쪽은 `test_w002_ac8_view_only.py` 의 정적 게이트와 `.env.example`
    (키만 적고 값을 적지 않는다)가 맡는다.
    """
    from tests.conftest import TEST_PASSWORD

    for name, payload in api_surfaces:
        assert TEST_PASSWORD not in json.dumps(payload, ensure_ascii=False, default=str), name
    # 쿠키에도 원문이 없다 — 서명 키만 파생한다(`api/deps._signing_key`)
    cookie = auth_client_session.cookies.get("ontology_demo_sid")
    assert cookie and TEST_PASSWORD not in cookie


# --- P3 배포 구성 -----------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSE_PATH = REPO_ROOT / "app" / "back" / "docker-compose.yml"
ENV_EXAMPLE_PATH = Path(__file__).resolve().parents[1] / ".env.example"


def _compose() -> dict:
    import yaml

    return yaml.safe_load(COMPOSE_PATH.read_text(encoding="utf-8"))


def _env_example_keys() -> set[str]:
    """주석 처리된 키도 센다 — 「적혀 있다」가 계약이지 「활성화됐다」가 아니다."""
    keys = set()
    for line in ENV_EXAMPLE_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.lstrip("# ").strip()
        if "=" in stripped and stripped.split("=", 1)[0].isupper():
            keys.add(stripped.split("=", 1)[0])
    return keys


def test_env_example_가_설정_전_키를_적는다():
    """설정이 늘었는데 배포 문서가 안 늘면 배포하는 사람이 그 키의 존재를 모른다."""
    from config import Settings

    want = {f"ONTOLOGY_{name.upper()}" for name in Settings.model_fields}
    have = _env_example_keys()
    assert not (want - have), f".env.example 에 없는 설정 키: {sorted(want - have)}"
    # 설정에 없는 키를 적어 두면 「주입했는데 안 먹는다」가 된다. 테스트 스위치만 예외다.
    assert not (have - want - {"ONTOLOGY_LIVE_REGRESSION"}), \
        f"설정에 없는 키: {sorted(have - want - {'ONTOLOGY_LIVE_REGRESSION'})}"


def test_env_example_에_값이_적혀_있지_않다():
    """배포 전 체크리스트 6 — 비밀번호가 레포·문서 어디에도 없다."""
    filled = [
        line for line in ENV_EXAMPLE_PATH.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("#") and "=" in line and line.split("=", 1)[1].strip()
    ]
    assert not filled, f".env.example 에 값이 적혀 있다: {filled}"


def test_compose_가_온톨로지_서빙_2종을_띄운다():
    services = _compose()["services"]
    assert "ontology-mcp" in services and "ontology-api" in services
    # 워커는 WORK-003 이 이미 올려 뒀다 — 셋이 한 세트다
    assert "ontology-worker" in services


def test_compose_가_기존_서비스를_건드리지_않았다():
    """DEC-005 · Pre-deploy Check — 포트폴리오 사이트와 기존 워커가 그대로여야 한다."""
    services = _compose()["services"]
    for name in ("postgres", "redis", "back", "worker", "mcp", "chat-worker"):
        assert name in services, f"기존 서비스 {name} 가 사라졌다"
    # 기존 워커의 큐가 온톨로지와 겹치면 서로의 태스크를 집어 간다
    assert services["worker"]["environment"]["AI_QUEUE"] == "default"
    assert services["chat-worker"]["environment"]["AI_QUEUE"] == "chat"
    assert services["ontology-worker"]["environment"]["AI_QUEUE"] == "ontology"


def test_compose_가_MCP_포트를_열지_않는다():
    """도구 서버는 자기 인증이 없다(SPEC-002 Out of scope) — 열리면 무인증 조회 표면이다."""
    mcp = _compose()["services"]["ontology-mcp"]
    assert "ports" not in mcp, "MCP 포트가 노출됐다 — 비밀번호 없이 브론즈 행이 읽힌다"


def test_compose_가_MCP_ALLOWED_HOSTS_를_명시_주입한다():
    """기본값 `["*"]` 는 보호를 무력화하면서 동작하지도 않는다 — 명시가 계약이다."""
    env = _compose()["services"]["ontology-mcp"]["environment"]
    hosts = env["ONTOLOGY_MCP_ALLOWED_HOSTS"]
    assert hosts and "*" not in hosts, f"명시 주입이 아니다: {hosts}"
    assert "ontology-mcp" in hosts


def test_compose_가_DB_를_읽기_전용으로만_붙인다():
    """서빙은 읽기만 한다. 쓰기가 가능하면 게이트를 안 거친 변경이 들어올 길이 생긴다."""
    for name in ("ontology-mcp", "ontology-api"):
        mounts = [v for v in _compose()["services"][name]["volumes"] if "/data/db" in v]
        assert mounts, f"{name} 에 DB 볼륨이 없다"
        for mount in mounts:
            assert mount.endswith(":ro"), f"{name} DB 마운트가 읽기 전용이 아니다: {mount}"


def test_compose_가_비밀번호_값을_적지_않는다():
    """값은 `.env` 로만 온다 — compose 는 레포에 커밋되는 파일이다."""
    text = COMPOSE_PATH.read_text(encoding="utf-8")
    assert "ONTOLOGY_DEMO_PASSWORD:" not in text and "ONTOLOGY_DEMO_PASSWORD=" not in text


def test_dockerignore_가_DB_를_이미지_밖으로_뺀다():
    """`.gitignore` 는 커밋만 막는다 — `COPY . .` 는 막지 않는다."""
    patterns = {
        line.strip() for line in
        (Path(__file__).resolve().parents[1] / ".dockerignore").read_text(
            encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    assert {".data/", "*.db", ".env"} <= patterns, f"이미지에 PII 가 실릴 수 있다: {patterns}"


# --- P3 교차 오리진 왕복 (Phase 3 검증 「CORS·쿠키 포함」) ---------------------

#: 테스트가 쓰는 프론트 오리진. **설정값에서 가져온다** — CORS 미들웨어는 앱을
#: 만들 때 목록을 한 번 읽고 붙잡으므로, 나중에 `settings` 를 바꿔 봐야 안 먹는다
#: (배포 오리진은 프로세스 기동 전 `ONTOLOGY_ALLOWED_ORIGINS` 로 주입한다).
def _front_origin() -> str:
    from config import settings

    return settings.allowed_origins[0]


@pytest.fixture
def cross_origin_client(monkeypatch, tmp_path, built_db_path):
    """배포 형태 그대로 — 프론트 오리진이 API 오리진과 다르고 쿠키가 Secure 다."""
    from fastapi.testclient import TestClient

    from config import settings
    from tests.conftest import TEST_PASSWORD

    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "cors_chat.db")
    monkeypatch.setattr(settings, "session_cookie_secure", True)
    import main

    with TestClient(main.app, base_url="https://ontology-api.kknaks.cloud") as c:
        yield c


@requires_source
def test_교차_오리진_프리플라이트가_통과한다(cross_origin_client):
    """이게 막히면 화면이 API 를 **한 번도** 못 부른다 — 게이트 화면부터 죽는다."""
    r = cross_origin_client.options(
        "/api/auth/session",
        headers={"Origin": _front_origin(), "Access-Control-Request-Method": "POST",
                 "Access-Control-Request-Headers": "content-type"})
    assert r.status_code == 200, r.text
    assert r.headers["access-control-allow-origin"] == _front_origin()
    assert r.headers["access-control-allow-credentials"] == "true"


@requires_source
def test_목록_밖_오리진은_허용_헤더를_받지_못한다(cross_origin_client):
    r = cross_origin_client.options(
        "/api/kpi/cards",
        headers={"Origin": "https://not-ours.example", "Access-Control-Request-Method": "GET"})
    assert "access-control-allow-origin" not in r.headers


@requires_source
def test_교차_오리진_세션_쿠키가_SameSite_None_Secure_로_나간다(cross_origin_client):
    """`Lax` 면 교차 사이트 요청에 쿠키가 실리지 않아 게이트 통과가 무의미해진다."""
    from tests.conftest import TEST_PASSWORD

    r = cross_origin_client.post(
        "/api/auth/session", json={"password": TEST_PASSWORD}, headers={"Origin": _front_origin()})
    assert r.status_code == 200
    set_cookie = r.headers["set-cookie"].lower()
    assert "samesite=none" in set_cookie, set_cookie
    assert "secure" in set_cookie and "httponly" in set_cookie, set_cookie
    assert r.headers["access-control-allow-origin"] == _front_origin()


@requires_source
def test_교차_오리진_왕복_1건이_성립한다(cross_origin_client):
    """게이트 통과 → 조회까지 **쿠키를 달고** 한 바퀴 — Phase 3 완료 증거."""
    from tests.conftest import TEST_PASSWORD

    assert cross_origin_client.get(
        "/api/kpi/cards", headers={"Origin": _front_origin()}).status_code == 401
    cross_origin_client.post(
        "/api/auth/session", json={"password": TEST_PASSWORD}, headers={"Origin": _front_origin()})
    r = cross_origin_client.get("/api/kpi/cards", headers={"Origin": _front_origin()})
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == _front_origin()
    assert r.json()["cards"]


def test_로컬_http_에서는_SameSite_가_Lax_로_내려간다(monkeypatch):
    """`None` 은 `Secure` 를 요구한다 — http 로컬에서 그대로 두면 쿠키가 버려진다."""
    from config import settings

    monkeypatch.setattr(settings, "session_cookie_secure", False)
    assert settings.session_cookie_samesite == "lax"
    monkeypatch.setattr(settings, "session_cookie_secure", True)
    assert settings.session_cookie_samesite == "none"


def test_CORS_오리진에_와일드카드가_없다():
    """`allow_credentials=True` 와 `*` 는 브라우저가 함께 받지 않는다 — 조용히 다 막힌다."""
    from config import settings

    assert "*" not in settings.allowed_origins
