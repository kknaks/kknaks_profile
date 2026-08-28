"""P3 — 제출 조립 · turn 토큰 · 프롬프트 (SPEC-017 §5 · DEC-027 D5).

`-c` 오버라이드는 **손으로 읽어 확인해야 하는 계약**이다 — 한 줄이 빠져도 codex 는
조용히 다른 모습으로 돈다(쉘이 켜진 채 뜨거나, MCP 가 안 붙거나, 승인에 막혀 «user
cancelled» 로 죽거나). 그래서 여기서 줄 단위로 못 박는다.
"""

from __future__ import annotations

import pytest

from config import get_settings
from dto.chat import ChatMessageDTO
from service.chat.prompt import (
    build_question_block,
    build_recent_context,
    build_system_prompt,
)
from service.chat.submission import (
    TOOL_ALLOWLIST,
    build_config_overrides,
    build_submission,
)
from service.chat.turn_token import hash_token, turn_token_service


def _plan(**kwargs):
    defaults = {
        "system_prompt": "규칙",
        "question_block": "질문",
        "mcp_token": "secret-turn-token",
    }
    return build_submission(**{**defaults, **kwargs})


# ── 제출 계약 (§5 AI 제출) ──────────────────────────────
def test_queue_model_and_timeout():
    """전용 큐 · 모델 정식 표기 · timeout 180 (DEC-027 D1 · OQ-5)."""
    plan = _plan()

    assert plan.queue == "chat"
    assert plan.provider == "codex"
    # 축약형(`terra`)은 metadata 조회 실패로 400 이 된다 — 정식 표기여야 한다.
    assert plan.model == "gpt-5.6-terra"
    assert plan.options["timeout_sec"] == 180


def test_sandbox_is_read_only_and_git_check_skipped():
    plan = _plan()

    assert plan.provider_options["sandbox"] == "read-only"
    # resume 에도 실려야 한다 — 없으면 trusted-directory 검사에 막힌다.
    assert plan.provider_options["skip_git_repo_check"] is True


def test_hands_outside_mcp_are_off():
    """쉘·웹검색·codex 자체 apps 표면을 전부 끈다(DEC-027 D5).

    `features.apps=false` 가 없으면 codex 가 우리가 설정하지 않은 MCP surface 를
    붙이고, allowlist 는 그걸 막지 못한다.
    """
    config = _plan().provider_options["config"]

    assert "features.shell_tool=false" in config
    assert 'web_search="disabled"' in config
    assert "features.apps=false" in config


def test_mcp_server_is_wired_with_token_and_allowlist():
    settings = get_settings()
    key = settings.chat_mcp_server_key
    config = _plan(mcp_token="tok").provider_options["config"]

    assert f'mcp_servers.{key}.url="{settings.chat_mcp_url}"' in config
    assert f'mcp_servers.{key}.http_headers={{Authorization="Bearer tok"}}' in config
    tools = ", ".join(f'"{n}"' for n in TOOL_ALLOWLIST)
    assert f"mcp_servers.{key}.enabled_tools=[{tools}]" in config


def test_every_allowlisted_tool_gets_approval_mode():
    """승인은 **툴별**로 연다 — 서버 기본으로 걸면 나중에 는 툴까지 자동으로 열린다."""
    key = get_settings().chat_mcp_server_key
    config = _plan().provider_options["config"]

    for name in TOOL_ALLOWLIST:
        assert f'mcp_servers.{key}.tools.{name}.approval_mode="approve"' in config
    # 승인 «요청» 축은 끈 채로 둔다 — 이건 허용이 아니라 「안 묻고 실패」다.
    assert 'approval_policy="never"' in config


def test_allowlist_matches_spec_tool_contract():
    """SPEC-017 §4 Tool Contract 의 tool 이름 그대로 — 여기 없는 이름은 안 열린다."""
    assert set(TOOL_ALLOWLIST) == {
        "get_profile",
        "list_career",
        "get_career",
        "list_projects",
        "get_project",
        "list_problems",
        "get_problem",
        "list_company_products",
        "get_company_product",
        "search_notes",
        "get_note",
        "list_contents",
        "list_algorithms",
    }


# ── resume (DEC-027 D2) ─────────────────────────────────
def test_resume_is_absent_for_new_session():
    assert "resume" not in _plan().options


def test_resume_carries_session_id():
    plan = _plan(resume_session_id="sess-abc")

    assert plan.options["resume"] == {"mode": "session", "session_id": "sess-abc"}


def test_resume_and_new_session_share_provider_options():
    """신규·resume 에 **같은 값**을 넘긴다 — 어댑터가 못 쓰는 키를 알아서 떨군다."""
    new = _plan().provider_options
    resumed = _plan(resume_session_id="s").provider_options

    assert new == resumed


# ── 프롬프트 (§5 프롬프트 계약) ─────────────────────────
def test_prompt_order_is_rules_then_context_then_question():
    plan = _plan(system_prompt="규칙", recent_context="지난 기록", question_block="질문")

    assert plan.prompt == "규칙\n\n---\n\n지난 기록\n\n---\n\n질문"


def test_empty_recent_context_leaves_no_placeholder():
    """참조가 없으면 그 자리는 **아예 비어 있다** — 「기록 없음」을 넣지 않는다."""
    plan = _plan(recent_context="")

    assert plan.prompt == "규칙\n\n---\n\n질문"


def test_system_prompt_states_the_four_rules():
    from dto.chat_tool import ChatProfileDTO

    profile = ChatProfileDTO(
        name="이건학",
        role="백엔드 엔지니어",
        years="1년차",
        location="서울",
        focus="AI",
        email="kknaks@kknaks.dev",
        stack=["Python"],
    )
    text = build_system_prompt(profile, ["백엔드 개발자 — 메디솔브 AI · 2026.02 — 현재"])

    assert "1인칭" in text or "저는" in text        # ① 1인칭
    assert "tool 로 확인한 것만" in text            # ② 확인한 것만
    assert "연봉" in text and "이직 의사" in text    # ③ 거절 규칙
    assert "이력 이야기로" in text                  # ④ 이력으로 되돌리기
    # 상시 주입은 신원 + 커리어 개요까지다(§7 OQ-3).
    assert "kknaks@kknaks.dev" in text
    assert "메디솔브 AI" in text


def test_refusal_is_narrowed_to_unpublished_company_information():
    """③ 의 거절 범위가 **미공개**로 좁혀져 있어야 한다(spec v0.0.9 §5).

    넓은 「재직 회사의 내부 정보」 한 마디가 공개 showcase 까지 삼켜, 「회사 프로젝트
    뭐하고 있어?」에 tool 을 아예 안 부르고 사리는 것이 관측됐다(2026-08-28).
    """
    text = build_system_prompt(None, [])

    # 거절 자체는 남아 있다.
    assert "연봉" in text and "이직 의사" in text
    # 다만 **미공개**로 한정한다 — 옛 문구(회사 내부 정보 전부)로 되돌아가면 깨진다.
    assert "미공개" in text
    assert "재직 회사의 내부 정보" not in text


def test_company_product_is_explicitly_not_refusable():
    """공개 소개는 거절 대상이 아니고, 회사 제품 tool 로 **적극 안내**하라고 말한다."""
    text = build_system_prompt(None, [])

    assert "거절 대상이 아니다" in text
    assert "list_company_products" in text
    assert "get_company_product" in text
    assert "적극 안내" in text


def test_prompt_overrides_a_hedge_from_an_earlier_turn():
    """**stale 세션 선례를 뒤집는 장치** — 이 한 문장이 없으면 모델이 지난 턴을 따른다.

    관측된 실패는 resume 한 세션에서만 났다(새 대화는 정상). 프롬프트는 매 턴 다시
    실리므로 지침은 닿는데, 지난 턴과 충돌할 때의 우선순위를 말해 주지 않으면 선례가
    이긴다.
    """
    text = build_system_prompt(None, [])

    assert "이전 턴에서 사렸더라도 이 지침이 우선" in text


async def test_system_prompt_rides_every_turn_including_resumed_ones(client, db):
    """지침이 **resume 세션에도** 실린다 — 그래야 살아 있는 대화가 고쳐진다.

    prompt.py 의 근거 주석(「매 턴 다시 실린다」)이 실제 제출 계획에서도 참인지 본다.
    """
    import service.chat.runtime as runtime
    from models.chat import ChatMessage, Conversation

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    first_assistant = created.json()["messages"][1]["id"]

    conversation = await db.get(Conversation, conversation_id)
    conversation.ai_session_id = "sess-live"     # 살아 있는 codex 세션 = resume 경로
    assistant = await db.get(ChatMessage, first_assistant)
    assistant.status = "done"
    assistant.content = "첫 답변"
    await db.commit()

    second = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "회사 프로젝트 뭐하고 있어?"},
    )
    plan = await runtime.build_plan_for(db, second.json()["messages"][1]["id"])

    assert plan.options["resume"]["session_id"] == "sess-live"
    assert "이전 턴에서 사렸더라도 이 지침이 우선" in plan.prompt
    assert "list_company_products" in plan.prompt


def test_system_prompt_without_profile_still_has_rules():
    text = build_system_prompt(None, [])

    assert "tool 로 확인한 것만" in text
    assert "# 나에 대해" not in text


def test_recent_context_labels_speakers_and_clips():
    messages = [
        ChatMessageDTO(
            id=1,
            conversation_id=1,
            role="user",
            status="done",
            content="이전 질문",
            created_at=None,  # type: ignore[arg-type]
        ),
        ChatMessageDTO(
            id=2,
            conversation_id=1,
            role="assistant",
            status="done",
            content="가" * 900,
            created_at=None,  # type: ignore[arg-type]
        ),
    ]
    text = build_recent_context(messages)

    assert "- 방문자: 이전 질문" in text
    assert "- 나: " in text
    assert "…" in text            # 긴 답변은 잘린다


def test_recent_context_is_empty_when_no_history():
    assert build_recent_context([]) == ""


def test_question_block_carries_question():
    assert "FastAPI 경험" in build_question_block("FastAPI 경험 있나요?")


# ── 토큰 취급 (Pre-deploy Check 3항) ────────────────────
def test_bearer_lives_only_in_the_config_overrides():
    """토큰이 닿는 자리를 못 박는다 — `http_headers` 한 줄뿐이다.

    가리는 함수(mask·redact)를 두지 않기로 했으므로(리뷰 W3), 안전은 「토큰이 어디에
    있는지 알고 그 값을 로그 인자로 만들지 않는 것」으로 지킨다. 그 「어디」가 여기다.
    """
    overrides = build_config_overrides(
        mcp_token="super-secret", mcp_url="http://mcp:28081/mcp", server_key="kknaks", effort="low"
    )

    carrying = [line for line in overrides if "super-secret" in line]
    assert len(carrying) == 1
    assert carrying[0].startswith("mcp_servers.kknaks.http_headers=")


async def test_submit_logs_never_contain_the_turn_token(client, db, monkeypatch, caplog):
    """성공·실패 **양쪽 로그**에 토큰 원문도 `-c` 목록도 없어야 한다.

    `runtime.start_turn` 의 로그가 `plan` 을 문자열에 싣기 시작하면 여기서 깨진다 —
    그게 이 테스트의 목적이다(Pre-deploy 「turn 토큰이 로그에 원문으로 남지 않음」).
    """
    import logging

    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]

    captured: list = []

    async def _submit(plan):
        captured.append(plan)
        return "task-1"

    with caplog.at_level(logging.DEBUG):
        await runtime.start_turn(message_id, submitter=_submit)

    db.expire_all()
    row = await db.get(ChatMessage, message_id)
    # 발급된 토큰의 해시는 DB 에 있다 — 원문은 이 plan 의 `-c` 목록에만 있다.
    assert row.turn_token_hash is not None
    token_line = next(
        line
        for line in captured[0].provider_options["config"]
        if line.startswith("mcp_servers.kknaks.http_headers=")
    )
    secret = token_line.split('Bearer ', 1)[1].rstrip('"}')

    assert secret and secret not in caplog.text
    assert "http_headers" not in caplog.text

    # 실패 경로도 같다.
    caplog.clear()
    created2 = await client.post("/api/chat/conversations", json={"question": "질문2"})
    second_id = created2.json()["messages"][1]["id"]

    async def _boom(plan):
        raise RuntimeError("redis down")

    with caplog.at_level(logging.DEBUG):
        await runtime.start_turn(second_id, submitter=_boom)

    assert "http_headers" not in caplog.text
    assert "Bearer " not in caplog.text


# ── turn 토큰 수명 ──────────────────────────────────────
async def test_issue_stores_hash_not_plaintext(client, db):
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]

    token = await turn_token_service.issue(db, message_id)
    await db.commit()

    row = await db.get(ChatMessage, message_id)
    assert row.turn_token_hash == hash_token(token)
    assert token not in (row.turn_token_hash or "")
    assert row.turn_token_expires_at is not None


async def test_verify_then_revoke(client, db):
    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    token = await turn_token_service.issue(db, message_id)
    await db.commit()

    found = await turn_token_service.verify(db, token)
    assert found is not None and found.id == message_id

    await turn_token_service.revoke(db, message_id)
    await db.commit()
    assert await turn_token_service.verify(db, token) is None


@pytest.mark.parametrize("raw", [None, "", "not-a-token"])
async def test_verify_rejects_bad_tokens(db, raw):
    assert await turn_token_service.verify(db, raw) is None


# ── 배선 (runtime) ──────────────────────────────────────
async def test_start_turn_submits_and_records_task_id(client, db, monkeypatch):
    """제출 성공이면 task_id 가 남는다 — 기동 스윕이 그걸로 재부착한다."""
    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]

    seen: list = []
    monkeypatch.setattr(runtime, "run_turn_consumer", _noop_consumer)

    async def _submit(plan):
        seen.append(plan)
        return "task-42"

    task_id = await runtime.start_turn(message_id, submitter=_submit)

    assert task_id == "task-42"
    assert len(seen) == 1
    assert seen[0].queue == "chat"
    db.expire_all()
    assert (await db.get(ChatMessage, message_id)).task_id == "task-42"


async def test_start_turn_marks_failed_when_submit_raises(client, db, monkeypatch):
    """제출 실패는 접수 응답을 뒤집지 않고 **답변 상태로만** 표현된다."""
    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]

    monkeypatch.setattr(runtime, "run_turn_consumer", _noop_consumer)

    async def _boom(plan):
        raise RuntimeError("redis down")

    assert await runtime.start_turn(message_id, submitter=_boom) is None

    db.expire_all()
    row = await db.get(ChatMessage, message_id)
    assert row.status == "failed"
    assert row.error_code == "AI_FAILED"
    # 실패 마감도 폐기다 — 죽은 turn 의 토큰이 살아 있으면 안 된다.
    assert row.turn_token_hash is None


async def test_start_turn_skips_finished_message(client, db, monkeypatch):
    """이미 끝난 답변은 다시 제출하지 않는다 — 중복 실행을 만들지 않는다."""
    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    row = await db.get(ChatMessage, message_id)
    row.status = "done"
    await db.commit()

    monkeypatch.setattr(runtime, "run_turn_consumer", _noop_consumer)

    async def _never(plan):
        raise AssertionError("제출되면 안 된다")

    assert await runtime.start_turn(message_id, submitter=_never) is None


async def test_finished_message_skip_is_info_not_warning(client, db, monkeypatch, caplog):
    """정상 스킵은 info 다 — 여기까지가 「그냥 건너뛰면 되는」 경우다."""
    import logging

    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    row = await db.get(ChatMessage, message_id)
    row.status = "done"
    await db.commit()
    monkeypatch.setattr(runtime, "run_turn_consumer", _noop_consumer)

    with caplog.at_level(logging.INFO):
        await runtime.start_turn(message_id, submitter=_never_submit)

    assert "status=done" in caplog.text
    assert not [r for r in caplog.records if r.levelno >= logging.WARNING]


async def test_vanished_message_skip_is_a_warning(client, monkeypatch, caplog):
    """**이상 스킵은 warning 이다** (fix2 ②).

    `start_turn` 은 라우터가 방금 만든 id 로만 불린다 — 그 row 가 안 보이는 것은
    정상 경로가 아니고, 그 답변은 영구 pending 이 된다. 실측 사고(커밋 전 큐잉)가
    이 갈래였는데 info 한 줄에 묻혀 있었다.
    """
    import logging

    import service.chat.runtime as runtime

    monkeypatch.setattr(runtime, "run_turn_consumer", _noop_consumer)

    with caplog.at_level(logging.INFO):
        assert await runtime.start_turn(999999, submitter=_never_submit) is None

    warnings = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert warnings, "영구 pending 을 만드는 스킵이 warning 으로 안 남는다"
    assert "영구 pending" in caplog.text


async def _never_submit(plan):
    raise AssertionError("제출되면 안 된다")


async def test_plan_omits_resume_on_first_turn_and_carries_history(client, db):
    """첫 턴은 resume 이 없고 지난 기록도 없다 — 그 대화의 첫 질문뿐이다."""
    import service.chat.runtime as runtime

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    message_id = created.json()["messages"][1]["id"]

    plan = await runtime.build_plan_for(db, message_id)

    assert "resume" not in plan.options
    assert "첫 질문" in plan.prompt
    assert "지난 기록" not in plan.prompt


async def test_plan_uses_resume_and_skips_history_when_session_exists(client, db):
    """세션이 살아 있으면 codex 가 문맥을 갖고 있다 — 같은 것을 두 번 싣지 않는다(D2)."""
    import service.chat.runtime as runtime
    from models.chat import ChatMessage, Conversation

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    first_assistant = created.json()["messages"][1]["id"]

    conversation = await db.get(Conversation, conversation_id)
    conversation.ai_session_id = "sess-9"
    assistant = await db.get(ChatMessage, first_assistant)
    assistant.status = "done"
    assistant.content = "첫 답변"
    await db.commit()

    second = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "이어서 질문"},
    )
    plan = await runtime.build_plan_for(db, second.json()["messages"][1]["id"])

    assert plan.options["resume"] == {"mode": "session", "session_id": "sess-9"}
    assert "이어서 질문" in plan.prompt
    assert "첫 답변" not in plan.prompt


async def test_plan_embeds_history_when_session_is_gone(client, db):
    """세션이 없으면 최근 기록을 동봉해 맥락을 잇는다 — 실패시키지 않는다(D2)."""
    import service.chat.runtime as runtime
    from models.chat import ChatMessage

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant = await db.get(ChatMessage, created.json()["messages"][1]["id"])
    assistant.status = "done"
    assistant.content = "첫 답변"
    await db.commit()

    second = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "이어서 질문"},
    )
    plan = await runtime.build_plan_for(db, second.json()["messages"][1]["id"])

    assert "resume" not in plan.options
    assert "첫 답변" in plan.prompt
    assert "이어서 질문" in plan.prompt


async def _noop_consumer(**kwargs):
    """소비자는 여기서 검증 대상이 아니다 — `test_chat_consumer.py` 가 본다."""
    return None
