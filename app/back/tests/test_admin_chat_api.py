"""어드민 채팅 열람·인사이트 (SPEC-017 §2 U-8 · §4 어드민 응답 계약 · WORK-025 P1).

여기서 지키는 것 넷: **게이트**(admin 아니면 아무것도 안 보인다) · **정렬/페이지 경계** ·
**소유 무관 상세** · **집계 정확성**(빈 날 0 · Top 순서 · last7d 경계).

집계 테스트가 「오늘」을 KST 로 잡는 이유: 서비스가 KST 날짜 경계로 자르기 때문이다
(`service/chat/admin_service.py`). UTC 로 계산하면 한국 시간 오전 9시 이전에 돌릴 때만
초록인 테스트가 된다.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from config import get_settings
from core.security import create_access_token
from models import ChatSession, Profile, User
from models.chat import (
    ROLE_ASSISTANT,
    ROLE_USER,
    STATUS_DONE,
    ChatMessage,
    Conversation,
)

KST = ZoneInfo("Asia/Seoul")


def _now_kst() -> datetime:
    return datetime.now(KST)


# ── 시드 ────────────────────────────────────────────────
async def _new_session(db) -> int:
    row = ChatSession(token_hash=uuid.uuid4().hex)
    db.add(row)
    await db.flush()
    return row.id


async def _new_conversation(db, session_id: int, title: str, created_at: datetime) -> int:
    row = Conversation(session_id=session_id, title=title, created_at=created_at)
    db.add(row)
    await db.flush()
    return row.id


async def _new_message(
    db,
    conversation_id: int,
    *,
    role: str,
    content: str = "",
    created_at: datetime,
    sources: list[dict] | None = None,
    steps: list[dict] | None = None,
) -> int:
    row = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        status=STATUS_DONE,
        content=content,
        created_at=created_at,
        sources=sources,
        steps=steps,
    )
    db.add(row)
    await db.flush()
    return row.id


async def _turn(db, conversation_id: int, question: str, at: datetime, **kw) -> None:
    """질문 + 답변 한 쌍 — 실제 스레드와 같은 모양으로 심는다."""
    await _new_message(db, conversation_id, role=ROLE_USER, content=question, created_at=at)
    await _new_message(
        db,
        conversation_id,
        role=ROLE_ASSISTANT,
        content="답변",
        created_at=at + timedelta(seconds=30),
        **kw,
    )


@pytest.fixture
async def admin(client, db):
    """어드민 쿠키 — 기존 인증 방식(`require_admin`)을 그대로 쓴다."""
    profile = Profile(handle="a", name="a", role="a", email="a@a.a")
    db.add(profile)
    await db.flush()
    user = User(
        username="admin", password_hash="x", system_role="admin", profile_id=profile.id
    )
    db.add(user)
    await db.commit()
    client.cookies.set(
        get_settings().auth_cookie_name,
        create_access_token(username="admin", uid=user.id, role="admin"),
    )
    return user


# ── 게이트 (Pre-deploy Check 「admin 미인증 접근 전부 차단」) ──
@pytest.mark.parametrize(
    "path",
    [
        "/api/admin/chat/conversations",
        "/api/admin/chat/conversations/1",
        "/api/admin/chat/insights",
    ],
)
async def test_admin_chat_requires_admin(client, path):
    res = await client.get(path)

    assert res.status_code == 401


# ── 목록 — 정렬 · 페이지 경계 · 필드 ─────────────────────
async def test_list_is_newest_first_across_sessions(client, db, admin):
    """전 세션의 대화가 한 목록에 최신순으로 온다 — 방문자 목록과 달리 세션을 안 가린다."""
    base = _now_kst()
    a, b = await _new_session(db), await _new_session(db)
    await _new_conversation(db, a, "오래된 질문", base - timedelta(hours=2))
    await _new_conversation(db, b, "중간 질문", base - timedelta(hours=1))
    await _new_conversation(db, a, "최근 질문", base)
    await db.commit()

    res = await client.get("/api/admin/chat/conversations")

    assert res.status_code == 200
    body = res.json()
    assert [i["title"] for i in body["items"]] == ["최근 질문", "중간 질문", "오래된 질문"]
    assert (body["total"], body["page"], body["size"]) == (3, 1, 20)


async def test_list_same_timestamp_falls_back_to_id_desc(client, db, admin):
    """같은 시각이면 id 역순 — 페이지 경계가 요청마다 흔들리지 않게 하는 결정적 정렬."""
    at = _now_kst()
    session_id = await _new_session(db)
    await _new_conversation(db, session_id, "먼저", at)
    await _new_conversation(db, session_id, "나중", at)
    await db.commit()

    res = await client.get("/api/admin/chat/conversations")

    assert [i["title"] for i in res.json()["items"]] == ["나중", "먼저"]


async def test_list_paginates_and_last_page_is_partial(client, db, admin):
    base = _now_kst()
    session_id = await _new_session(db)
    for i in range(5):
        await _new_conversation(db, session_id, f"질문{i}", base - timedelta(minutes=i))
    await db.commit()

    first = (await client.get("/api/admin/chat/conversations?page=1&size=2")).json()
    second = (await client.get("/api/admin/chat/conversations?page=2&size=2")).json()
    third = (await client.get("/api/admin/chat/conversations?page=3&size=2")).json()

    assert [i["title"] for i in first["items"]] == ["질문0", "질문1"]
    assert [i["title"] for i in second["items"]] == ["질문2", "질문3"]
    assert [i["title"] for i in third["items"]] == ["질문4"]
    # total 은 페이지가 아니라 전체다 — 페이저가 이 수로 마지막 페이지를 센다.
    assert {first["total"], second["total"], third["total"]} == {5}
    assert second["page"] == 2 and second["size"] == 2


async def test_list_beyond_last_page_is_empty_not_404(client, db, admin):
    session_id = await _new_session(db)
    await _new_conversation(db, session_id, "하나", _now_kst())
    await db.commit()

    res = await client.get("/api/admin/chat/conversations?page=9&size=20")

    assert res.status_code == 200
    assert res.json() == {"items": [], "total": 1, "page": 9, "size": 20}


async def test_list_rejects_bad_page_params(client, db, admin):
    assert (await client.get("/api/admin/chat/conversations?page=0")).status_code == 422
    assert (await client.get("/api/admin/chat/conversations?size=0")).status_code == 422
    assert (await client.get("/api/admin/chat/conversations?size=101")).status_code == 422


async def test_list_item_carries_count_and_last_message_time(client, db, admin):
    """메시지 수 · 최근 시각은 집계로 붙는다(§4 목록 계약)."""
    started = _now_kst() - timedelta(hours=1)
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "시작 질문", started)
    await _turn(db, conversation_id, "시작 질문", started)
    last_turn_at = started + timedelta(minutes=20)
    await _turn(db, conversation_id, "이어서", last_turn_at)
    await db.commit()

    item = (await client.get("/api/admin/chat/conversations")).json()["items"][0]

    assert item["sessionId"] == session_id
    assert item["messageCount"] == 4
    assert datetime.fromisoformat(item["createdAt"]) == started
    # 마지막 답변(질문 +30초)이 최근 시각이다.
    assert datetime.fromisoformat(item["lastMessageAt"]) == last_turn_at + timedelta(
        seconds=30
    )


# ── 상세 — 소유 무관 ────────────────────────────────────
async def test_detail_reads_any_session_conversation(client, db, admin):
    """방문자 API 라면 404 였을 남의 대화가, admin 에게는 열린다(§4)."""
    at = _now_kst()
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "남의 대화", at)
    sources = [{"type": "career", "slug": "medisolve-1", "title": "메디솔브", "url": "/career"}]
    steps = [{"tool": "list_career", "argsSummary": "", "durationMs": 32, "calledAt": "t"}]
    await _turn(db, conversation_id, "남의 대화", at, sources=sources, steps=steps)
    await db.commit()

    res = await client.get(f"/api/admin/chat/conversations/{conversation_id}")

    assert res.status_code == 200
    body = res.json()
    # 공개 상세와 같은 shape + sessionId(§4). 쿠키 토큰·해시는 어디에도 없다.
    assert body["conversation"] == {
        "id": conversation_id,
        "title": "남의 대화",
        "createdAt": body["conversation"]["createdAt"],
        "sessionId": session_id,
    }
    assert [m["role"] for m in body["messages"]] == ["user", "assistant"]
    assert body["messages"][1]["sources"] == sources
    assert body["messages"][1]["steps"] == [
        {"tool": "list_career", "argsSummary": "", "durationMs": 32, "calledAt": "t"}
    ]


async def test_detail_unknown_id_is_404(client, db, admin):
    res = await client.get("/api/admin/chat/conversations/999999")

    assert res.status_code == 404
    assert res.json()["detail"] == "NOT_FOUND"


# ── 인사이트 ────────────────────────────────────────────
async def test_insights_totals_count_questions_only(client, db, admin):
    at = _now_kst()
    session_id = await _new_session(db)
    first = await _new_conversation(db, session_id, "하나", at)
    second = await _new_conversation(db, session_id, "둘", at - timedelta(minutes=5))
    await _turn(db, first, "질문 A", at)
    await _turn(db, first, "질문 B", at)
    await _turn(db, second, "질문 C", at)
    await db.commit()

    totals = (await client.get("/api/admin/chat/insights")).json()["totals"]

    # 답변(assistant)은 질문 수에 들어가지 않는다 — 6줄이지만 질문은 3개다.
    assert totals == {"conversations": 2, "questions": 3, "last7d": 3}


async def test_insights_last7d_boundary_is_seven_kst_days(client, db, admin):
    """`last7d` 는 오늘 포함 7일치 — 6일 전은 들어가고 7일 전은 빠진다.

    `daily` 마지막 7칸의 합과 같아야 한다(둘이 같은 KST 경계를 쓴다).
    """
    now = _now_kst()
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "경계", now - timedelta(days=8))
    for days in (0, 6, 7, 8):
        await _turn(db, conversation_id, f"{days}일 전", now - timedelta(days=days))
    await db.commit()

    body = (await client.get("/api/admin/chat/insights")).json()

    assert body["totals"]["questions"] == 4
    assert body["totals"]["last7d"] == 2
    assert sum(d["count"] for d in body["daily"][-7:]) == 2


async def test_insights_daily_fills_empty_days_with_zero(client, db, admin):
    """30칸이 빠짐없이 오고, 질문 없는 날은 0 이다(§4 「빈 날 0 포함」)."""
    now = _now_kst()
    today = now.date()
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "일별", now - timedelta(days=40))
    await _turn(db, conversation_id, "오늘", now)
    await _turn(db, conversation_id, "오늘 또", now)
    await _turn(db, conversation_id, "3일 전", now - timedelta(days=3))
    # 창 밖 — 30일 구간(오늘 포함 29일 전까지)에 들어오지 않는다.
    await _turn(db, conversation_id, "40일 전", now - timedelta(days=40))
    await db.commit()

    daily = (await client.get("/api/admin/chat/insights")).json()["daily"]

    assert len(daily) == 30
    assert daily[-1]["date"] == today.isoformat()
    assert daily[0]["date"] == (today - timedelta(days=29)).isoformat()
    # 날짜가 하루씩 연속이다 — 차트의 칸 간격이 곧 시간축이다.
    days = [datetime.fromisoformat(d["date"]).date() for d in daily]
    assert days == [today - timedelta(days=29 - i) for i in range(30)]
    by_day = {d["date"]: d["count"] for d in daily}
    assert by_day[today.isoformat()] == 2
    assert by_day[(today - timedelta(days=3)).isoformat()] == 1
    assert by_day[(today - timedelta(days=1)).isoformat()] == 0
    # 창 밖의 40일 전 질문은 어느 칸에도 새지 않는다.
    assert sum(d["count"] for d in daily) == 3


async def test_insights_recent_questions_are_latest_twenty(client, db, admin):
    now = _now_kst()
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "피드", now - timedelta(hours=30))
    for i in range(25):
        await _turn(db, conversation_id, f"질문 {i}", now - timedelta(hours=25 - i))
    await db.commit()

    feed = (await client.get("/api/admin/chat/insights")).json()["recentQuestions"]

    assert len(feed) == 20
    assert [q["question"] for q in feed] == [f"질문 {i}" for i in range(24, 4, -1)]
    assert feed[0]["conversationId"] == conversation_id
    assert datetime.fromisoformat(feed[0]["askedAt"]) == now - timedelta(hours=1)


async def test_insights_top_sources_are_counted_and_capped(client, db, admin):
    """근거 카드 jsonb 를 전개해 센다 — 많이 읽힌 순 Top 5(§4)."""
    now = _now_kst()
    session_id = await _new_session(db)
    conversation_id = await _new_conversation(db, session_id, "근거", now)

    def source(slug: str, kind: str = "career") -> dict:
        return {"type": kind, "slug": slug, "title": f"{slug} 제목", "url": "/career"}

    # slug → 실릴 횟수. 6종을 심어 Top 5 로 잘리는 것도 본다.
    plan = {"a": 5, "b": 4, "c": 3, "d": 2, "e": 2, "f": 1}
    for slug, times in plan.items():
        for _ in range(times):
            await _turn(db, conversation_id, f"{slug} 질문", now, sources=[source(slug)])
    # 사용자 질문 줄에 sources 가 있어도 세지 않는다 — 근거는 답변의 것이다.
    await _new_message(
        db,
        conversation_id,
        role=ROLE_USER,
        content="잡음",
        created_at=now,
        sources=[source("a")],
    )
    # 다른 유형이지만 slug 가 같은 문서는 다른 줄이다.
    await _turn(db, conversation_id, "제품 질문", now, sources=[source("a", "product")])
    await db.commit()

    top = (await client.get("/api/admin/chat/insights")).json()["topSources"]

    assert len(top) == 5
    assert [(s["type"], s["slug"], s["count"]) for s in top] == [
        ("career", "a", 5),
        ("career", "b", 4),
        ("career", "c", 3),
        # 동수(2)는 type · slug 순으로 갈린다 — 같은 데이터에 같은 Top 이 나온다.
        ("career", "d", 2),
        ("career", "e", 2),
    ]
    assert top[0]["title"] == "a 제목"


async def test_insights_on_empty_db_is_zeroed_not_empty(client, db, admin):
    """데이터가 없어도 30칸은 온다 — 화면이 빈 차트가 아니라 0 인 차트를 그린다."""
    body = (await client.get("/api/admin/chat/insights")).json()

    assert body["totals"] == {"conversations": 0, "questions": 0, "last7d": 0}
    assert body["recentQuestions"] == []
    assert body["topSources"] == []
    assert len(body["daily"]) == 30
    assert {d["count"] for d in body["daily"]} == {0}
