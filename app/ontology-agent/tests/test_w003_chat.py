"""P2 — 채팅 API 와 폴딩 소비자. SPEC-003 채팅 AC-8·AC-10·AC-17.

제출은 하지 않는다(큐 없이 돈다) — 라우터의 백그라운드 태스크를 막고 저장·상태·폴딩만 본다.
"""

from __future__ import annotations

import types

import pytest
from fastapi.testclient import TestClient

from agent import store
from agent.consumer import TurnFolder, fold_one, summarize_args
from config import settings
from tests.conftest import TEST_PASSWORD, requires_source


@pytest.fixture
def chat_client(monkeypatch, tmp_path, built_db_path):
    """제출을 막은 채팅 클라이언트 — 저장소는 임시 파일이다."""
    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "session_cookie_secure", False)

    from agent import runtime

    async def _no_submit(**kwargs):
        return None

    monkeypatch.setattr(runtime, "start_turn", _no_submit)
    import main

    with TestClient(main.app) as c:
        c.post("/api/auth/session", json={"password": TEST_PASSWORD})
        yield c


@pytest.fixture
def chat_store(monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    with store.connect() as conn:
        yield conn


def _event(kind: str, **fields):
    return types.SimpleNamespace(type=kind, **fields)


# --- 저장소 · 상태기계 --------------------------------------------------------


def test_채팅_저장소가_온톨로지_DB_와_다른_파일이다(monkeypatch, tmp_path):
    """재빌드가 대화 기록을 날리지 않게 수명을 분리한다."""
    monkeypatch.setattr(settings, "db_path", tmp_path / "ontology.db")
    monkeypatch.setattr(settings, "chat_db_path", None)
    assert settings.resolved_chat_db_path != settings.resolved_db_path
    assert settings.resolved_chat_db_path.name == "ontology_chat.db"


def test_대화에_pending_은_최대_1이다(chat_store):
    cid = store.create_conversation(chat_store, question="질문")
    assert store.has_pending(chat_store, cid) is False
    store.add_message(chat_store, conversation_id=cid, role=store.ROLE_ASSISTANT,
                      status=store.STATUS_PENDING)
    assert store.has_pending(chat_store, cid) is True


def test_세션_id_는_한_번만_박히고_응답에_안_실린다(chat_store):
    cid = store.create_conversation(chat_store, question="질문")
    store.set_session_id(chat_store, cid, "sess-1")
    store.set_session_id(chat_store, cid, "sess-2")     # 덮지 않는다
    assert store.get_session_id(chat_store, cid) == "sess-1"
    assert "ai_session_id" not in store.get_conversation(chat_store, cid)


# --- 폴딩 멱등 ---------------------------------------------------------------


def test_같은_이벤트를_두_번_넣어도_결과가_같다(chat_store):
    """중복 수신은 예외가 아니라 정상 경로다(재부착 재생)."""
    cid = store.create_conversation(chat_store, question="q")
    mid = store.add_message(chat_store, conversation_id=cid, role=store.ROLE_ASSISTANT,
                            status=store.STATUS_PENDING)
    folder = TurnFolder(mid, cid)

    events = [
        _event("tool_use", tool_use_id="t1", tool_name="query_kpi",
               tool_input={"metrics": ["noshow_rate"], "grain": "weekly"}),
        _event("tool_result", tool_use_id="t1", tool_result={"rows": []}, tool_is_error=False),
    ]
    for event in events:
        fold_one(chat_store, folder, event)
    once = store.get_message(chat_store, mid)["steps"]

    for event in events:                     # 같은 이벤트 재수신
        fold_one(chat_store, folder, event)
    twice = store.get_message(chat_store, mid)["steps"]

    import json

    assert len(json.loads(once)) == 1
    assert len(json.loads(twice)) == 1, "같은 tool_use_id 가 단계를 두 개 만들었다"


def test_result_가_use_보다_먼저_와도_자리를_만든다(chat_store):
    cid = store.create_conversation(chat_store, question="q")
    mid = store.add_message(chat_store, conversation_id=cid, role=store.ROLE_ASSISTANT,
                            status=store.STATUS_PENDING)
    folder = TurnFolder(mid, cid)
    fold_one(chat_store, folder, _event("tool_result", tool_use_id="t9",
                                        tool_result={}, tool_is_error=False))
    fold_one(chat_store, folder, _event("tool_use", tool_use_id="t9",
                                        tool_name="query_kpi", tool_input={}))
    import json

    steps = json.loads(store.get_message(chat_store, mid)["steps"])
    assert len(steps) == 1 and steps[0]["tool"] == "query_kpi"


def test_부분_텍스트가_델타로_누적된다(chat_store):
    cid = store.create_conversation(chat_store, question="q")
    mid = store.add_message(chat_store, conversation_id=cid, role=store.ROLE_ASSISTANT,
                            status=store.STATUS_PENDING)
    folder = TurnFolder(mid, cid)
    for delta in ("8월 ", "매출은 ", "떨어지지 않았습니다."):
        fold_one(chat_store, folder, _event("text", text=delta))
    assert store.get_message(chat_store, mid)["content"] == "8월 매출은 떨어지지 않았습니다."


def test_args_summary_에_필터_값이_실리지_않는다():
    """인자 원문을 그대로 실으면 필터 값이 응답으로 흘러 나간다."""
    summary = summarize_args("query_layer", {
        "layer": "bronze", "table": "vegas_reservations",
        "filters": [{"field": "chartNo", "op": "eq", "value": "비밀차트번호"}]})
    assert "비밀차트번호" not in summary
    assert "필터 1개" in summary
    assert len(summary) <= 120


def test_args_summary_가_지표와_그레인을_남긴다():
    summary = summarize_args("query_kpi", {"metrics": ["noshow_rate"], "grain": "weekly"})
    assert "noshow_rate" in summary and "weekly" in summary


def test_args_summary_가_codex_껍데기를_벗긴다():
    """codex 어댑터는 실제 인자를 `arguments` 안에 넣는다(2.1.2 실측 — 라이브 probe).

    껍데기를 안 벗기면 요약이 도구 이름으로만 떨어진다 — 화면에 「무엇을 물었는지」가
    안 남는다.
    """
    envelope = {
        "id": "item_1", "type": "mcp_tool_call", "server": "ontology",
        "tool": "query_kpi", "status": "in_progress", "result": None, "error": None,
        "arguments": {"metrics": ["noshow_rate"], "grain": "weekly"},
    }
    summary = summarize_args("query_kpi", envelope)
    assert "noshow_rate" in summary and "weekly" in summary
    # 껍데기 키가 요약에 새지 않는다
    assert "mcp_tool_call" not in summary and "in_progress" not in summary


def test_args_summary_가_껍데기_없는_모양도_받는다():
    """어댑터가 모양을 바꿔도 요약이 통째로 죽지 않아야 한다."""
    assert "weekly" in summarize_args("query_kpi", {"grain": "weekly"})
    assert summarize_args("query_kpi", None) == "query_kpi"


def test_실패_마감은_부분_텍스트를_지우지_않는다(chat_store):
    """어디까지 갔는지가 근거다."""
    cid = store.create_conversation(chat_store, question="q")
    mid = store.add_message(chat_store, conversation_id=cid, role=store.ROLE_ASSISTANT,
                            status=store.STATUS_PENDING)
    folder = TurnFolder(mid, cid)
    fold_one(chat_store, folder, _event("text", text="중간까지 쓴 답"))
    folder.finalize_failed(chat_store, store.CODE_AI_TIMEOUT)

    row = store.get_message(chat_store, mid)
    assert row["status"] == store.STATUS_FAILED
    assert row["error_code"] == "AI_TIMEOUT"
    assert row["content"] == "중간까지 쓴 답"


# --- 라우터 ------------------------------------------------------------------


@requires_source
def test_세션_없이_채팅_API_를_부르면_401(built_db_path, monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "demo_password", TEST_PASSWORD)
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "session_cookie_secure", False)
    import main

    with TestClient(main.app) as c:
        assert c.get("/api/chat/conversations").status_code == 401
        assert c.post("/api/chat/conversations", json={"question": "q"}).status_code == 401


@requires_source
def test_대화를_만들면_user_done_과_assistant_pending_이_생긴다(chat_client):
    body = chat_client.post(
        "/api/chat/conversations", json={"question": "최근 4주 노쇼율 추이는?"}).json()
    roles = [(m["role"], m["status"]) for m in body["messages"]]
    assert roles == [("user", "done"), ("assistant", "pending")]
    assert body["conversation"]["title"].startswith("최근 4주")
    assert body["messages"][1]["error_code"] is None
    assert body["messages"][1]["steps"] == []


@requires_source
@pytest.mark.parametrize("question,code,status", [
    ("", "EMPTY_QUESTION", 422),
    ("   ", "EMPTY_QUESTION", 422),
    ("가" * 1001, "QUESTION_TOO_LONG", 422),
])
def test_질문_검증(chat_client, question, code, status):
    r = chat_client.post("/api/chat/conversations", json={"question": question})
    assert r.status_code == status and r.json()["detail"] == code


@requires_source
def test_1000자는_통과한다(chat_client):
    assert chat_client.post(
        "/api/chat/conversations", json={"question": "가" * 1000}).status_code == 201


@requires_source
def test_pending_있는_대화에_질문하면_409_CONVERSATION_BUSY(chat_client):
    cid = chat_client.post(
        "/api/chat/conversations", json={"question": "첫 질문"}).json()["conversation"]["id"]
    r = chat_client.post(f"/api/chat/conversations/{cid}/messages", json={"question": "둘째"})
    assert r.status_code == 409 and r.json()["detail"] == "CONVERSATION_BUSY"


@requires_source
def test_없는_대화는_404_NOT_FOUND(chat_client):
    assert chat_client.get("/api/chat/conversations/없는id").status_code == 404
    r = chat_client.post("/api/chat/conversations/없는id/messages", json={"question": "q"})
    assert r.status_code == 404 and r.json()["detail"] == "NOT_FOUND"


@requires_source
def test_폴링_응답에서_content_와_steps_가_자란다(chat_client, monkeypatch, tmp_path):
    """`pending` 동안 화면이 볼 것이 있어야 한다 — 스피너만 도는 구간을 만들지 않는다."""
    created = chat_client.post(
        "/api/chat/conversations", json={"question": "q"}).json()
    cid = created["conversation"]["id"]
    mid = created["messages"][1]["id"]

    first = chat_client.get(f"/api/chat/conversations/{cid}").json()["messages"][1]
    assert first["content"] == "" and first["steps"] == []

    with store.connect() as conn:
        folder = TurnFolder(mid, cid)
        fold_one(conn, folder, _event("text", text="8월 매출은 "))
        fold_one(conn, folder, _event("tool_use", tool_use_id="t1", tool_name="query_kpi",
                                      tool_input={"metrics": ["sales_total"]}))

    grown = chat_client.get(f"/api/chat/conversations/{cid}").json()["messages"][1]
    assert grown["content"] == "8월 매출은 "
    assert len(grown["steps"]) == 1 and grown["steps"][0]["tool"] == "query_kpi"
    assert grown["status"] == "pending"


@requires_source
def test_retry_가_실패_답변을_되살린다(chat_client):
    created = chat_client.post(
        "/api/chat/conversations", json={"question": "되살릴 질문"}).json()
    cid, mid = created["conversation"]["id"], created["messages"][1]["id"]

    with store.connect() as conn:
        store.update_message(conn, mid, {
            "status": store.STATUS_FAILED, "error_code": "AI_TIMEOUT",
            "content": "실패 전 부분 텍스트"})

    r = chat_client.post(f"/api/chat/conversations/{cid}/messages/{mid}/retry")
    assert r.status_code == 201
    revived = r.json()["messages"][1]
    assert revived["status"] == "pending"
    assert revived["error_code"] is None
    assert revived["content"] == ""       # 다시 세므로 실패 흔적은 지운다


@requires_source
def test_pending_인_답변은_retry_할_수_없다(chat_client):
    created = chat_client.post("/api/chat/conversations", json={"question": "q"}).json()
    cid, mid = created["conversation"]["id"], created["messages"][1]["id"]
    r = chat_client.post(f"/api/chat/conversations/{cid}/messages/{mid}/retry")
    assert r.status_code == 409


@requires_source
def test_대화_목록이_최신순이다(chat_client):
    for q in ("첫째", "둘째", "셋째"):
        chat_client.post("/api/chat/conversations", json={"question": q})
    titles = [c["title"] for c in chat_client.get("/api/chat/conversations").json()["conversations"]]
    assert titles[0] == "셋째"
