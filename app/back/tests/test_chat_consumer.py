"""P4 — 이벤트 폴딩 · 멱등 · 마감 (SPEC-017 §5 소비자 폴딩 / DEC-027 D6).

**중복 수신이 정상 경로다** — 브로커가 Redis Stream 이라 재부착하면 처음부터 전부 다시
온다. 그래서 이 파일의 중심 질문은 하나다: 「같은 이벤트를 두 번 받아도 같은 결과인가」.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from models.chat import STATUS_DONE, STATUS_FAILED
from repository.chat_repo import chat_repository
from service.chat.consumer import (
    CODE_AI_FAILED,
    CODE_AI_TIMEOUT,
    TurnFolder,
    _close_from_task,
    _fold_one,
    extract_sources,
    summarize_args,
)


def event(kind: str, **fields):
    """StreamEvent 흉내 — 소비자는 `getattr` 로만 읽는다."""
    base = {
        "type": kind,
        "text": None,
        "session_id": None,
        "tool_use_id": None,
        "tool_name": None,
        "tool_input": None,
        "tool_result": None,
        "tool_is_error": None,
    }
    return SimpleNamespace(**{**base, **fields})


def mcp_result(item: dict) -> str:
    """MCP 봉투 — tool 의 dict 가 `content[].text` 안에 **이중 인코딩**돼 온다."""
    import json

    inner = json.dumps({"content": [{"type": "text", "text": "…"}], "structured": {"item": item}})
    return json.dumps({"content": [{"type": "text", "text": inner}], "isError": False})


@pytest.fixture
async def turn(client, db):
    """pending 답변 하나 + 그 folder."""
    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    conversation_id = created.json()["conversation"]["id"]
    message = await chat_repository.get_message(db, message_id)
    return SimpleNamespace(
        id=message_id,
        conversation_id=conversation_id,
        folder=TurnFolder(message),
    )


async def _reload(db, message_id):
    db.expire_all()
    return await chat_repository.get_message(db, message_id)


# ── text 누적 ───────────────────────────────────────────
async def test_text_accumulates(db, turn):
    for delta in ("저는 ", "FastAPI 를 ", "썼습니다"):
        await _fold_one(db, turn.folder, event("text", text=delta))
    await db.commit()

    assert (await _reload(db, turn.id)).content == "저는 FastAPI 를 썼습니다"


async def test_replay_resets_text_before_reaccumulating(db, turn):
    """재생을 그냥 두면 텍스트가 두 배가 된다 — 그래서 첫 글자에서 비운다."""
    await _fold_one(db, turn.folder, event("text", text="안녕"))
    await db.commit()

    turn.folder.begin_replay()
    await _fold_one(db, turn.folder, event("text", text="안녕"))
    await db.commit()

    assert (await _reload(db, turn.id)).content == "안녕"


async def test_replay_does_not_clear_text_until_it_arrives(db, turn):
    """붙는 시점에는 아직 안 지운다 — 지우는 것은 다시 쌓을 것이 실제로 왔을 때다."""
    await _fold_one(db, turn.folder, event("text", text="이전 조각"))
    await db.commit()

    turn.folder.begin_replay()

    assert (await _reload(db, turn.id)).content == "이전 조각"


async def test_replay_with_dead_stream_keeps_partial_text(db, turn):
    """**재생인데 스트림이 죽어 이벤트가 0건** — 기존 부분 텍스트가 살아남아야 한다(W10).

    「실패 마감은 부분 텍스트를 지우지 않는다」(`finalize`)가 재생 경로에서도 참이어야
    한다. 예전에는 붙자마자 비워서 마감 시점에 이미 빈 문자열이었다.
    """
    await _fold_one(db, turn.folder, event("text", text="방문자가 이미 읽은 글자"))
    await db.commit()

    turn.folder.begin_replay()
    # 이벤트가 하나도 오지 않는다 — 태스크도 사라졌다.
    await _close_from_task(db, turn.folder, None)
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.status == STATUS_FAILED
    assert message.content == "방문자가 이미 읽은 글자"
    assert message.error_code == CODE_AI_TIMEOUT


async def test_replay_with_tool_events_but_no_text_keeps_partial_text(db, turn):
    """text 가 아닌 이벤트만 재생돼도 초기화는 걸리지 않는다 — 트리거는 text 하나다."""
    await _fold_one(db, turn.folder, event("text", text="이전 조각"))
    await db.commit()

    turn.folder.begin_replay()
    await _fold_one(
        db, turn.folder, event("tool_use", tool_use_id="c1", tool_name="get_career", tool_input={})
    )
    await db.commit()

    assert (await _reload(db, turn.id)).content == "이전 조각"


async def test_empty_text_delta_is_ignored(db, turn):
    await _fold_one(db, turn.folder, event("text", text=""))
    await db.commit()

    assert (await _reload(db, turn.id)).content == ""


# ── init → ai_session_id ────────────────────────────────
async def test_init_pins_ai_session_id(db, turn):
    await _fold_one(db, turn.folder, event("init", session_id="sess-1"))
    await db.commit()

    conversation = await chat_repository.get_conversation(db, turn.conversation_id)
    assert conversation.ai_session_id == "sess-1"


async def test_init_without_session_id_is_noop(db, turn):
    await _fold_one(db, turn.folder, event("init", session_id=None))
    await db.commit()

    conversation = await chat_repository.get_conversation(db, turn.conversation_id)
    assert conversation.ai_session_id is None


# ── tool 단계 멱등 ──────────────────────────────────────
async def test_tool_use_is_idempotent_by_tool_use_id(db, turn):
    """같은 `tool_use_id` 가 두 번 와도 줄은 하나다 — 재생이 화면을 복제하지 않는다."""
    call = event(
        "tool_use",
        tool_use_id="call_1",
        tool_name="kknaks__list_career",
        tool_input={"id": "item_4", "type": "mcp_tool_call", "arguments": {}},
    )
    await _fold_one(db, turn.folder, call)
    await _fold_one(db, turn.folder, call)
    await db.commit()

    steps = (await _reload(db, turn.id)).steps
    assert len(steps) == 1
    # 서버 접두사는 떼고 기록한다 — 화면·근거 판정이 접두사에 흔들리지 않게.
    assert steps[0]["tool"] == "list_career"


async def test_tool_result_updates_the_same_step(db, turn):
    await _fold_one(
        db,
        turn.folder,
        event("tool_use", tool_use_id="c1", tool_name="get_career", tool_input={"slug": "a-1"}),
    )
    await _fold_one(
        db,
        turn.folder,
        event("tool_result", tool_use_id="c1", tool_result=mcp_result({}), tool_is_error=False),
    )
    await db.commit()

    steps = (await _reload(db, turn.id)).steps
    assert len(steps) == 1
    assert steps[0]["status"] == "done"
    assert isinstance(steps[0]["durationMs"], int)


async def test_duplicate_tool_result_keeps_first_duration(db, turn):
    """이미 잰 값은 다시 재지 않는다 — 재수신이 그것을 더 정확하게 만들지 않는다."""
    await _fold_one(
        db, turn.folder, event("tool_use", tool_use_id="c1", tool_name="get_career", tool_input={})
    )
    result = event("tool_result", tool_use_id="c1", tool_result=mcp_result({}), tool_is_error=False)
    await _fold_one(db, turn.folder, result)
    await db.commit()
    first = (await _reload(db, turn.id)).steps[0]["durationMs"]

    await _fold_one(db, turn.folder, result)
    await db.commit()

    assert (await _reload(db, turn.id)).steps[0]["durationMs"] == first


async def test_replay_does_not_record_duration(db, turn):
    """재생의 시간차는 「툴이 걸린 시간」이 아니라 「스트림을 읽은 시간」이다."""
    turn.folder.begin_replay()
    await _fold_one(
        db, turn.folder, event("tool_use", tool_use_id="c1", tool_name="get_career", tool_input={})
    )
    await _fold_one(
        db,
        turn.folder,
        event("tool_result", tool_use_id="c1", tool_result=mcp_result({}), tool_is_error=False),
    )
    await db.commit()

    assert (await _reload(db, turn.id)).steps[0]["durationMs"] is None


async def test_tool_error_marks_step_failed(db, turn):
    await _fold_one(
        db, turn.folder, event("tool_use", tool_use_id="c1", tool_name="get_note", tool_input={})
    )
    await _fold_one(
        db, turn.folder, event("tool_result", tool_use_id="c1", tool_result="{}", tool_is_error=True)
    )
    await db.commit()

    assert (await _reload(db, turn.id)).steps[0]["status"] == "failed"


async def test_orphan_tool_result_is_ignored(db, turn):
    """짝 없는 결과는 줄을 만들지 않는다 — 없는 호출을 그리지 않는다."""
    await _fold_one(
        db, turn.folder, event("tool_result", tool_use_id="ghost", tool_result="{}", tool_is_error=False)
    )
    await db.commit()

    assert (await _reload(db, turn.id)).steps == []


async def test_thinking_and_cost_are_dropped(db, turn):
    await _fold_one(db, turn.folder, event("thinking", text="음..."))
    await _fold_one(db, turn.folder, event("cost"))
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.content == ""
    assert message.steps == []


# ── 근거 카드 (§3 S-9 2항) ──────────────────────────────
async def test_sources_come_from_document_tools_only(db, turn):
    """목록 tool 은 훑기만 한 것이다 — 「읽었다」고 말하지 않는다."""
    item = {"type": "career", "slug": "medisolve-ai-1", "title": "백엔드 개발자", "url": "/career"}
    await _fold_one(
        db, turn.folder, event("tool_use", tool_use_id="c1", tool_name="list_career", tool_input={})
    )
    await _fold_one(
        db,
        turn.folder,
        event("tool_result", tool_use_id="c1", tool_result=mcp_result(item), tool_is_error=False),
    )
    await db.commit()

    assert (await _reload(db, turn.id)).sources == []


async def test_sources_are_deduped_across_repeat_reads(db, turn):
    item = {"type": "career", "slug": "medisolve-ai-1", "title": "백엔드 개발자", "url": "/career"}
    for index in (1, 2):
        await _fold_one(
            db,
            turn.folder,
            event("tool_use", tool_use_id=f"c{index}", tool_name="get_career", tool_input={}),
        )
        await _fold_one(
            db,
            turn.folder,
            event(
                "tool_result",
                tool_use_id=f"c{index}",
                tool_result=mcp_result(item),
                tool_is_error=False,
            ),
        )
    await db.commit()

    sources = (await _reload(db, turn.id)).sources
    assert sources == [item]


async def test_company_product_read_becomes_a_source_card(db, turn):
    """회사 제품 showcase 를 읽은 것도 **실제로 읽은 것**이다(spec v0.0.9).

    카드의 `url` 은 **`/career`** — 제품 전용 페이지는 없지만 그 제품이 속한 회사
    경력이 그려지는 표면이다. 화살표가 있는 카드는 눌려야 한다(owner 판정).
    """
    item = {
        "type": "company_product",
        "slug": "mediness",
        "title": "Mediness",
        "url": "/career",
    }
    await _fold_one(
        db,
        turn.folder,
        event("tool_use", tool_use_id="c1", tool_name="get_company_product", tool_input={}),
    )
    await _fold_one(
        db,
        turn.folder,
        event(
            "tool_result",
            tool_use_id="c1",
            tool_result=mcp_result(item),
            tool_is_error=False,
        ),
    )
    await db.commit()

    sources = (await _reload(db, turn.id)).sources
    assert sources == [item]
    assert sources[0]["url"] == "/career"


async def test_company_product_list_makes_no_card(db, turn):
    """목록 tool 은 훑기만 한 것이라 여전히 카드를 만들지 않는다."""
    item = {
        "type": "company_product",
        "slug": "mediness",
        "title": "Mediness",
        "url": "/career",
    }
    await _fold_one(
        db,
        turn.folder,
        event("tool_use", tool_use_id="c1", tool_name="list_company_products", tool_input={}),
    )
    await _fold_one(
        db,
        turn.folder,
        event(
            "tool_result",
            tool_use_id="c1",
            tool_result=mcp_result(item),
            tool_is_error=False,
        ),
    )
    await db.commit()

    assert (await _reload(db, turn.id)).sources == []


def test_company_product_url_is_derived_when_tool_omits_it():
    """tool 이 url 을 안 실어도 카드가 링크를 잃지 않는다 — 유형으로 파생한다.

    파생값의 정본은 `core/chat_slugs.public_url` 한 곳이다. tool 응답이 싣고 오는 값과
    같아야 하므로(둘이 갈리면 같은 카드가 두 모양이 된다) 여기서 함께 잠근다.
    """
    payload = str(
        {"structured": {"item": {"type": "company_product", "slug": "linky", "title": "Linky"}}}
    )

    sources = extract_sources("get_company_product", payload)

    assert sources == [
        {"type": "company_product", "slug": "linky", "title": "Linky", "url": "/career"}
    ]


def test_extract_sources_handles_python_repr():
    """codex 어댑터가 dict 를 `str()` 로 넘기는 경로 — `json.loads` 는 여기서 실패한다."""
    payload = str({"structured": {"item": {"type": "note", "slug": "n1", "title": "노트"}}})

    sources = extract_sources("get_note", payload)

    assert sources == [
        {"type": "note", "slug": "n1", "title": "노트", "url": "/notes/n1"}
    ]


def test_extract_sources_returns_empty_on_garbage():
    """못 읽으면 빈 리스트다 — 추측으로 메우지 않는다."""
    assert extract_sources("get_note", "not json at all") == []
    assert extract_sources("get_note", None) == []
    assert extract_sources("get_note", mcp_result({"type": "note"})) == []  # slug 없음


# ── 인자 요약 (§5 «인자 원문을 그대로 노출하지 않는다») ──
def test_summarize_args_opens_the_item_envelope():
    """봉투를 그대로 요약하면 화면에 `id=item_4 · type=mcp_tool_call` 이 찍힌다."""
    envelope = {
        "id": "item_4",
        "type": "mcp_tool_call",
        "server": "kknaks",
        "tool": "get_career",
        "arguments": {"slug": "medisolve-ai-3"},
    }

    assert summarize_args(envelope) == "medisolve-ai-3"


def test_summarize_args_joins_multiple_arguments():
    envelope = {"type": "mcp_tool_call", "tool": "search_notes", "arguments": {"query": "fastapi", "limit": 5}}

    assert summarize_args(envelope) == "query=fastapi · limit=5"


def test_summarize_args_drops_none_and_clips():
    assert summarize_args({"arguments": {"query": "a", "dir": None}}) == "a"
    assert len(summarize_args({"arguments": {"query": "가" * 500}})) <= 120
    assert summarize_args({"arguments": {}}) == ""
    assert summarize_args(None) == ""


def test_summarize_args_never_leaks_envelope_keys():
    envelope = {"id": "item_9", "type": "mcp_tool_call", "server": "kknaks", "tool": "list_career"}

    summary = summarize_args(envelope)

    assert "item_9" not in summary
    assert "mcp_tool_call" not in summary


# ── 마감 ────────────────────────────────────────────────
async def test_done_replaces_partial_text_with_result(db, turn):
    await _fold_one(db, turn.folder, event("text", text="부분"))
    await db.commit()

    await _close_from_task(
        db, turn.folder, SimpleNamespace(status="done", exit_code=0, result="최종 본문")
    )
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.status == STATUS_DONE
    assert message.content == "최종 본문"
    assert message.error_code is None
    # 마감이 곧 폐기다 — 토큰 해시가 남지 않는다.
    from models.chat import ChatMessage

    assert (await db.get(ChatMessage, turn.id)).turn_token_hash is None


async def test_failure_keeps_partial_text(db, turn):
    """방문자가 이미 읽은 글자를 사후에 뺏지 않는다."""
    await _fold_one(db, turn.folder, event("text", text="여기까지 썼는데"))
    await db.commit()

    await _close_from_task(
        db, turn.folder, SimpleNamespace(status="failed", exit_code=1, result=None, error="boom")
    )
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.status == STATUS_FAILED
    assert message.content == "여기까지 썼는데"
    assert message.error_code == CODE_AI_FAILED


async def test_vanished_task_is_timeout(db, turn):
    """태스크가 사라졌다(스트림 만료·소멸) — 실패와 code 로 구분한다(§4 Case Matrix)."""
    await _close_from_task(db, turn.folder, None)
    await db.commit()

    assert (await _reload(db, turn.id)).error_code == CODE_AI_TIMEOUT


async def test_nonzero_exit_is_failure_even_when_status_done(db, turn):
    await _close_from_task(
        db, turn.folder, SimpleNamespace(status="done", exit_code=3, result="쓰레기")
    )
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.status == STATUS_FAILED
    assert message.content == ""


async def test_close_is_noop_on_already_finished_message(db, turn):
    """이미 끝난 메시지의 완료 이벤트 재수신은 무시한다."""
    await _close_from_task(
        db, turn.folder, SimpleNamespace(status="done", exit_code=0, result="첫 마감")
    )
    await db.commit()

    await _close_from_task(
        db, turn.folder, SimpleNamespace(status="failed", exit_code=1, result=None, error="늦은 실패")
    )
    await db.commit()

    message = await _reload(db, turn.id)
    assert message.status == STATUS_DONE
    assert message.content == "첫 마감"


# ── 기동 스윕 ───────────────────────────────────────────
async def test_recover_fails_turns_that_never_submitted(client, db):
    """제출 전에 서버가 재시작됐다 — 재생할 스트림이 없으므로 실패로 마감한다."""
    from service.chat.consumer import recover_pending_turns

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]

    handled = await recover_pending_turns()

    assert handled == 1
    message = await _reload(db, message_id)
    assert message.status == STATUS_FAILED
    assert message.error_code == CODE_AI_FAILED


async def test_recover_reattaches_when_task_id_exists(client, db, monkeypatch):
    """task_id 가 있으면 실패로 접지 않고 **재부착**한다."""
    import service.chat.runtime as runtime
    from service.chat.consumer import recover_pending_turns

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    await chat_repository.update_message(db, message_id, {"task_id": "task-1"})
    await db.commit()

    spawned: list[tuple[int, str]] = []
    monkeypatch.setattr(
        runtime,
        "spawn_consumer",
        lambda *, message_id, task_id: spawned.append((message_id, task_id)),
    )

    handled = await recover_pending_turns()

    assert handled == 1
    assert spawned == [(message_id, "task-1")]
    # 재부착 대상은 pending 으로 남는다 — 소비자가 마감한다.
    assert (await _reload(db, message_id)).status == "pending"
