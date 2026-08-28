"""P1 — 세션 쿠키 · 대화 API (SPEC-017 §3 S-1~S-7 · §4 Case Matrix).

여기서 지키는 것 넷: **발급 시점** · **소유권** · **직렬화** · **입력 검증**.
"""

from __future__ import annotations

import pytest
from sqlalchemy import func, select

from config import get_settings
from models import ChatSession
from models.chat import ROLE_ASSISTANT, STATUS_PENDING, ChatMessage

COOKIE = get_settings().chat_cookie_name


async def _session_count(db) -> int:
    return (await db.execute(select(func.count(ChatSession.id)))).scalar_one()


# ── 발급 시점 (DEC-026 D1) ──────────────────────────────
async def test_list_without_cookie_creates_no_session(client, db):
    """사이트를 열어만 본 방문자에게 세션 row 를 만들지 않는다(§3 S-2)."""
    res = await client.get("/api/chat/conversations")

    assert res.status_code == 200
    assert res.json() == {"conversations": []}
    assert COOKIE not in res.cookies
    assert await _session_count(db) == 0


async def test_create_conversation_issues_cookie(client, db):
    """채팅 첫 사용이 발급 시점이다(§3 S-1 2항)."""
    res = await client.post(
        "/api/chat/conversations", json={"question": "FastAPI 실무 경험 있나요?"}
    )

    assert res.status_code == 201
    body = res.json()
    assert body["conversation"]["title"] == "FastAPI 실무 경험 있나요?"
    assert [m["role"] for m in body["messages"]] == ["user", "assistant"]
    assert body["messages"][0]["status"] == "done"
    assert body["messages"][1]["status"] == "pending"
    assert body["messages"][1]["content"] == ""
    assert await _session_count(db) == 1

    cookie = res.headers["set-cookie"]
    assert cookie.startswith(f"{COOKIE}=")
    assert "HttpOnly" in cookie
    assert "SameSite=lax" in cookie
    assert f"Max-Age={get_settings().chat_cookie_max_age_sec}" in cookie


async def test_second_request_reuses_session(client, db):
    """쿠키가 이미 있으면 세션을 새로 만들지 않는다 — row 는 하나로 유지된다(§3 S-5)."""
    first = await client.post("/api/chat/conversations", json={"question": "질문 하나"})
    second = await client.post("/api/chat/conversations", json={"question": "질문 둘"})

    assert second.status_code == 201
    assert await _session_count(db) == 1

    listing = await client.get("/api/chat/conversations")
    titles = [c["title"] for c in listing.json()["conversations"]]
    # 최신순(U-4) — 나중에 만든 것이 먼저다.
    assert titles == ["질문 둘", "질문 하나"]
    assert first.json()["conversation"]["id"] != second.json()["conversation"]["id"]


# ── sliding (§4 「사용(요청)마다 만료 연장」 · S-5 3항) ──
async def test_cookie_is_reissued_on_every_authenticated_response(client, db):
    """서버가 `last_seen_at` 을 미는 것만으로는 부족하다 — **브라우저 만료도** 밀어야
    한다. 그래서 세션이 살아 있는 응답마다 같은 값을 Max-Age 와 함께 다시 굽는다."""
    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    token = created.cookies[COOKIE]
    conversation_id = created.json()["conversation"]["id"]

    for res in (
        await client.get("/api/chat/conversations"),
        await client.get(f"/api/chat/conversations/{conversation_id}"),
        await client.post("/api/chat/conversations", json={"question": "또 질문"}),
    ):
        assert "set-cookie" in res.headers, res.request.url
        # **같은 값**을 다시 심는다 — 세션을 갈아 끼우는 것이 아니라 수명만 민다.
        assert f"{COOKIE}={token}" in res.headers["set-cookie"]
        assert f"Max-Age={get_settings().chat_cookie_max_age_sec}" in res.headers["set-cookie"]

    assert await _session_count(db) == 1


async def test_no_cookie_response_does_not_set_one(client, db):
    """쿠키 없는 조회는 여전히 아무것도 심지 않는다 — 발급 시점 계약(DEC-026 D1)."""
    res = await client.get("/api/chat/conversations")

    assert "set-cookie" not in res.headers
    assert await _session_count(db) == 0


async def test_session_expires_after_max_age_of_inactivity(client, db):
    """`last_seen_at + 30일` 이 지나면 세션은 없는 것이다 — row 가 영원히 살지 않는다."""
    from datetime import UTC, datetime, timedelta

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    conversation_id = created.json()["conversation"]["id"]

    session_row = (await db.execute(select(ChatSession))).scalars().one()
    session_row.last_seen_at = datetime.now(UTC) - timedelta(
        seconds=get_settings().chat_cookie_max_age_sec + 60
    )
    await db.commit()

    # 쿠키는 그대로 들고 있지만 새 손님과 같다.
    listing = await client.get("/api/chat/conversations")
    assert listing.json() == {"conversations": []}
    assert "set-cookie" not in listing.headers

    detail = await client.get(f"/api/chat/conversations/{conversation_id}")
    assert detail.status_code == 404

    # 그 상태에서 질문하면 **새 세션**이 발급된다(복구가 아니라 새 손님이다).
    again = await client.post("/api/chat/conversations", json={"question": "다시"})
    assert again.status_code == 201
    assert "set-cookie" in again.headers
    assert await _session_count(db) == 2


async def test_session_just_inside_max_age_still_works(client, db):
    """경계 안쪽(30일 - 1분)은 살아 있다 — 컷이 한쪽으로만 치우치지 않게."""
    from datetime import UTC, datetime, timedelta

    await client.post("/api/chat/conversations", json={"question": "질문"})
    session_row = (await db.execute(select(ChatSession))).scalars().one()
    session_row.last_seen_at = datetime.now(UTC) - timedelta(
        seconds=get_settings().chat_cookie_max_age_sec - 60
    )
    await db.commit()

    listing = await client.get("/api/chat/conversations")

    assert len(listing.json()["conversations"]) == 1
    assert "set-cookie" in listing.headers


async def test_title_is_truncated_with_ellipsis(client):
    """제목은 첫 질문에서 따되 50자에서 끊는다(§2 U-4)."""
    question = "가" * 80
    res = await client.post("/api/chat/conversations", json={"question": question})

    title = res.json()["conversation"]["title"]
    assert title == "가" * 50 + "…"


# ── 소유권 (§4 Case Matrix NOT_FOUND) ───────────────────
async def test_other_session_conversation_is_404(client):
    """남의 세션의 대화는 **없는 것과 같은 404** 다 — 존재 여부가 새지 않는다."""
    created = await client.post("/api/chat/conversations", json={"question": "내 질문"})
    conversation_id = created.json()["conversation"]["id"]

    # 다른 방문자 = 쿠키 없음.
    client.cookies.clear()
    res = await client.get(f"/api/chat/conversations/{conversation_id}")

    assert res.status_code == 404
    assert res.json()["detail"] == "NOT_FOUND"


async def test_unknown_conversation_is_404(client):
    await client.post("/api/chat/conversations", json={"question": "질문"})
    res = await client.get("/api/chat/conversations/999999")

    assert res.status_code == 404
    assert res.json()["detail"] == "NOT_FOUND"


async def test_get_conversation_returns_thread(client):
    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    conversation_id = created.json()["conversation"]["id"]

    res = await client.get(f"/api/chat/conversations/{conversation_id}")

    assert res.status_code == 200
    body = res.json()
    assert body["conversation"]["id"] == conversation_id
    assert len(body["messages"]) == 2
    # pending 중에도 계약의 모든 필드가 있다 — FE 가 빈 배열을 그대로 그린다.
    assistant = body["messages"][1]
    assert assistant["sources"] == []
    assert assistant["steps"] == []
    assert "createdAt" in assistant


# ── 직렬화 (§5 · S-7) ───────────────────────────────────
async def test_message_while_pending_is_409(client):
    """pending 이 있는 대화에 질문하면 409 `CONVERSATION_BUSY`."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "이어서 질문"},
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "CONVERSATION_BUSY"


async def test_message_after_done_is_accepted(client, db):
    """직전 답변이 끝났으면 이어서 질문할 수 있다(§3 S-3)."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]

    message = await db.get(ChatMessage, assistant_id)
    message.status = "done"
    message.content = "답변입니다"
    await db.commit()

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "이어서 질문"},
    )

    assert res.status_code == 201
    assert [m["role"] for m in res.json()["messages"]] == ["user", "assistant"]


async def test_db_enforces_single_pending_assistant(client, db):
    """앱 검사가 새도 **DB 가 막는다** — partial unique index 가 최종 방어선이다."""
    from sqlalchemy.exc import IntegrityError

    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    conversation_id = created.json()["conversation"]["id"]

    db.add(
        ChatMessage(
            conversation_id=conversation_id,
            role=ROLE_ASSISTANT,
            status=STATUS_PENDING,
            content="",
        )
    )
    with pytest.raises(IntegrityError):
        await db.commit()
    await db.rollback()


async def test_race_past_the_app_check_still_answers_409(client, db, monkeypatch):
    """**두 겹이 같은 답을 준다** — DB 방어선에 걸린 요청도 409 다(리뷰 W2).

    동시 요청을 진짜로 만들 수는 없으니 앱 검사를 멀게 해서 그 갈래를 직접 연다:
    pending 이 이미 있는데 `pending_count` 가 0 을 보고하는 상태 = 두 요청이 검사를
    나란히 통과한 순간과 같다. 예전에는 이 갈래가 **500** 이었다.
    """
    from repository.chat_repo import ChatRepository

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]

    async def _blind(self, session, conversation_id):  # noqa: ARG001
        return 0

    monkeypatch.setattr(ChatRepository, "pending_count", _blind)

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "동시에 들어온 질문"},
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "CONVERSATION_BUSY"


async def test_losing_race_leaves_no_orphan_user_message(client, db, monkeypatch):
    """409 로 접힌 요청은 질문 줄도 남기지 않는다 — 트랜잭션이 통째로 롤백된다."""
    from repository.chat_repo import ChatRepository

    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]

    async def _blind(self, session, conversation_id):  # noqa: ARG001
        return 0

    monkeypatch.setattr(ChatRepository, "pending_count", _blind)
    await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "동시에 들어온 질문"},
    )
    monkeypatch.undo()

    detail = await client.get(f"/api/chat/conversations/{conversation_id}")
    contents = [m["content"] for m in detail.json()["messages"]]
    assert "동시에 들어온 질문" not in contents
    assert len(detail.json()["messages"]) == 2


# ── 재시도 (§3 S-8 3항 · spec v0.0.5) ───────────────────
async def _finish_assistant(db, message_id: int):
    """pending 을 done 으로 — 그래야 같은 대화에 이어서 질문할 수 있다."""
    message = await db.get(ChatMessage, message_id)
    message.status = "done"
    message.content = "답변"
    await db.commit()


async def _fail_assistant(db, message_id: int, *, content: str = "여기까지 썼는데"):
    message = await db.get(ChatMessage, message_id)
    message.status = "failed"
    message.content = content
    message.error_code = "AI_FAILED"
    message.steps = [{"toolUseId": "c1", "tool": "list_career", "argsSummary": "", "calledAt": "x"}]
    message.sources = [{"type": "career", "slug": "a-1", "title": "t", "url": "/career"}]
    await db.commit()


async def test_retry_revives_the_same_message(client, db):
    """새 줄을 만들지 않는다 — 스레드에 같은 질문이 두 번 보이지 않는다."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]
    await _fail_assistant(db, assistant_id)

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
    )

    assert res.status_code == 200
    message = res.json()["message"]
    assert message["id"] == assistant_id          # 같은 줄이다
    assert message["status"] == "pending"
    # 지난 시도의 흔적은 전부 지워진다.
    assert message["content"] == ""
    assert message["steps"] == []
    assert message["sources"] == []

    detail = await client.get(f"/api/chat/conversations/{conversation_id}")
    assert len(detail.json()["messages"]) == 2    # user + assistant 그대로


async def test_retry_resubmits_the_same_message(client, db):
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]
    await _fail_assistant(db, assistant_id)
    client.submitted.clear()

    await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
    )

    assert client.submitted == [assistant_id]


@pytest.mark.parametrize("status", ["pending", "done"])
async def test_retry_of_non_failed_message_is_404(client, db, status):
    """failed 가 아닌 줄은 재시도 대상이 아니다."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]
    if status == "done":
        message = await db.get(ChatMessage, assistant_id)
        message.status = "done"
        await db.commit()

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "NOT_FOUND"


async def test_retry_of_user_message_is_404(client, db):
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    user_id = created.json()["messages"][0]["id"]

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{user_id}/retry"
    )

    assert res.status_code == 404


async def test_retry_of_unknown_message_is_404(client):
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/999999/retry"
    )

    assert res.status_code == 404


async def test_retry_of_message_from_another_conversation_is_404(client, db):
    """메시지 id 는 맞지만 그 대화의 것이 아니다 — 대화 경계를 넘지 않는다."""
    first = await client.post("/api/chat/conversations", json={"question": "첫 대화"})
    second = await client.post("/api/chat/conversations", json={"question": "둘째 대화"})
    stray_id = first.json()["messages"][1]["id"]
    await _fail_assistant(db, stray_id)

    res = await client.post(
        f"/api/chat/conversations/{second.json()['conversation']['id']}"
        f"/messages/{stray_id}/retry"
    )

    assert res.status_code == 404


async def test_retry_in_another_session_is_404(client, db):
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]
    await _fail_assistant(db, assistant_id)

    client.cookies.clear()
    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
    )

    assert res.status_code == 404


async def test_retry_while_another_answer_is_pending_is_409(client, db):
    """대화에 pending 이 있으면 재시도도 막힌다 — 직렬화는 재시도에도 적용된다."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    first_assistant = created.json()["messages"][1]["id"]
    await _fail_assistant(db, first_assistant)

    # 그 대화에 새 질문 → 새 pending 이 생긴다.
    await client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json={"question": "둘째 질문"},
    )

    res = await client.post(
        f"/api/chat/conversations/{conversation_id}/messages/{first_assistant}/retry"
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "CONVERSATION_BUSY"


# ── 입력 검증 (§4 Validation) ───────────────────────────
@pytest.mark.parametrize(
    ("question", "code"),
    [
        ("", "EMPTY_QUESTION"),
        ("   \n\t ", "EMPTY_QUESTION"),
        ("가" * 1001, "QUESTION_TOO_LONG"),
    ],
)
async def test_question_validation(client, question, code):
    res = await client.post("/api/chat/conversations", json={"question": question})

    assert res.status_code == 422
    assert res.json()["detail"] == code


async def test_question_at_limit_is_accepted(client):
    """1,000자는 통과한다 — 경계가 「이하」다."""
    res = await client.post("/api/chat/conversations", json={"question": "가" * 1000})

    assert res.status_code == 201


async def test_question_is_trimmed(client):
    res = await client.post("/api/chat/conversations", json={"question": "  질문  "})

    assert res.json()["messages"][0]["content"] == "질문"


# ── 제출 배선 ───────────────────────────────────────────
async def test_pending_message_is_queued_for_submission(client):
    """만들어진 pending assistant 가 제출 대기에 걸린다.

    ⚠ **이 테스트는 fix2 의 결함을 못 잡았다.** conftest 가 `start_turn` 을 통째로
    갈아 끼워 id 만 받아 적으므로, 그 시점에 row 가 **다른 세션에서 보이는지**는
    아무도 확인하지 않았다. 실제 배선을 재는 것은 아래 `..._sees_committed_rows` 다.
    """
    created = await client.post("/api/chat/conversations", json={"question": "질문"})

    assert client.submitted == [created.json()["messages"][1]["id"]]


async def _fail_and_retry_setup(client, db):
    """retry 경로를 재려면 failed assistant 가 하나 있어야 한다."""
    created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
    conversation_id = created.json()["conversation"]["id"]
    assistant_id = created.json()["messages"][1]["id"]
    await _fail_assistant(db, assistant_id)
    return conversation_id, assistant_id


@pytest.mark.parametrize("path", ["create", "add_message", "retry"])
async def test_submission_wiring_sees_committed_rows(client, db, monkeypatch, path):
    """**제출이 걸리는 순간 row 가 다른 세션에서 보여야 한다** (fix2 — e2e 실측 결함).

    `start_turn` 은 요청 세션이 아니라 **새 세션**으로 메시지를 다시 읽는다. 라우터가
    커밋하기 전에 큐잉하면 그 조회가 None 을 받아 「제출 대상이 아니다」로 조용히
    건너뛰고, 대화는 **영구 pending** 이 된다(2026-08-28 로컬 compose 실측).

    그래서 여기서는 id 만 받아 적지 않고 **진짜로 새 세션에서 읽어 본다** — 이것이
    프로덕션에서 깨진 바로 그 불변식이다.
    """
    import api.chat_router as chat_router
    from core.db import SessionLocal
    from repository.chat_repo import chat_repository

    seen: list = []

    async def _checking_start_turn(message_id: int) -> None:
        # 요청 세션이 아닌 **독립 세션** — 커밋되지 않았으면 여기서 안 보인다.
        async with SessionLocal() as fresh:
            seen.append(await chat_repository.get_message(fresh, message_id))

    # 셋업(대화 생성)도 제출을 걸므로 **재는 것은 셋업이 끝난 뒤부터**다.
    if path == "add_message":
        created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
        conversation_id = created.json()["conversation"]["id"]
        await _finish_assistant(db, created.json()["messages"][1]["id"])
    elif path == "retry":
        conversation_id, assistant_id = await _fail_and_retry_setup(client, db)

    monkeypatch.setattr(chat_router, "start_turn", _checking_start_turn)

    if path == "create":
        await client.post("/api/chat/conversations", json={"question": "질문"})
    elif path == "add_message":
        await client.post(
            f"/api/chat/conversations/{conversation_id}/messages",
            json={"question": "이어서 질문"},
        )
    else:
        await client.post(
            f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
        )

    assert len(seen) == 1, f"{path}: 제출이 걸리지 않았다"
    assert seen[0] is not None, f"{path}: 큐잉 시점에 row 가 커밋돼 있지 않다"
    assert seen[0].status == "pending"


@pytest.mark.parametrize("path", ["create", "add_message", "retry"])
async def test_router_commits_before_queueing(client, db, monkeypatch, path):
    """순서 자체를 못 박는다 — 커밋이 `add_task` **앞**이어야 한다.

    위 테스트가 불변식을 재고, 이 테스트는 그 불변식을 **무엇으로** 지키는지를 잠근다.
    teardown 의 commit 에 기대는 구현으로 되돌아가면 여기서 깨진다.
    """
    from fastapi import BackgroundTasks
    from sqlalchemy.ext.asyncio import AsyncSession

    events: list[str] = []
    real_commit = AsyncSession.commit
    real_add_task = BackgroundTasks.add_task

    async def _spy_commit(self):
        events.append("commit")
        await real_commit(self)

    def _spy_add_task(self, func, *args, **kwargs):
        events.append("add_task")
        return real_add_task(self, func, *args, **kwargs)

    if path == "add_message":
        created = await client.post("/api/chat/conversations", json={"question": "첫 질문"})
        conversation_id = created.json()["conversation"]["id"]
        await _finish_assistant(db, created.json()["messages"][1]["id"])
    elif path == "retry":
        conversation_id, assistant_id = await _fail_and_retry_setup(client, db)

    # 준비가 끝난 뒤부터 잰다 — 위 셋업의 커밋이 섞이지 않게.
    monkeypatch.setattr(AsyncSession, "commit", _spy_commit)
    monkeypatch.setattr(BackgroundTasks, "add_task", _spy_add_task)

    if path == "create":
        await client.post("/api/chat/conversations", json={"question": "질문"})
    elif path == "add_message":
        await client.post(
            f"/api/chat/conversations/{conversation_id}/messages",
            json={"question": "이어서 질문"},
        )
    else:
        await client.post(
            f"/api/chat/conversations/{conversation_id}/messages/{assistant_id}/retry"
        )

    assert "add_task" in events, f"{path}: 제출이 걸리지 않았다"
    assert "commit" in events, f"{path}: 커밋이 없다"
    assert events.index("commit") < events.index("add_task"), (
        f"{path}: 커밋보다 큐잉이 먼저다 — {events}"
    )
