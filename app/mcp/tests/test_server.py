"""MCP 서버 — tool 카탈로그 · 토큰 게이트 · 중계 (SPEC-017 §4 Tool Contract).

여기서 지키는 것 셋:
1. **tool 이름이 spec 그대로다** — 제출부의 allowlist 와 갈리면 아무 tool 도 안 열린다.
2. **토큰 없는 호출은 못 들어온다**(DEC-027 D5).
3. **중계만 한다** — 판정은 back 이 하고, back 의 404 는 「없는 문서」로 번역된다.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from app import back_client, server
from app.config import settings
from app.errors import NotFoundError, UnauthorizedError, UpstreamError

#: SPEC-017 §4 Tool Contract 의 tool 이름 그대로. back 의
#: `service/chat/submission.py:TOOL_ALLOWLIST` 와 **같은 집합**이어야 한다 —
#: 갈리면 codex 의 `enabled_tools` 가 없는 이름을 가리켜 그 tool 이 안 열린다.
EXPECTED_TOOLS = {
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


async def test_tool_names_match_spec():
    names = {tool.name for tool in await server.mcp.list_tools()}

    assert names == EXPECTED_TOOLS


async def test_every_tool_has_a_description():
    """설명이 모델의 tool 선택 품질을 정한다 — 빈 설명을 두지 않는다."""
    for tool in await server.mcp.list_tools():
        assert tool.description, f"{tool.name} 에 설명이 없다"
        assert len(tool.description) > 40, f"{tool.name} 의 설명이 너무 짧다"


async def test_detail_tools_take_slug_only():
    """인자는 slug 뿐이다 — 경로 인자가 없다(DEC-027 D3)."""
    by_name = {tool.name: tool for tool in await server.mcp.list_tools()}

    for name in ("get_career", "get_project", "get_problem", "get_note", "get_company_product"):
        properties = by_name[name].inputSchema.get("properties", {})
        assert set(properties) == {"slug"}


async def test_list_tools_take_no_arguments():
    by_name = {tool.name: tool for tool in await server.mcp.list_tools()}

    for name in (
        "list_career", "list_projects", "list_problems",
        "list_company_products", "list_contents", "list_algorithms",
    ):
        assert by_name[name].inputSchema.get("properties", {}) == {}


# ── 토큰 게이트 ─────────────────────────────────────────
@pytest.mark.parametrize(
    "headers",
    [
        {},                                   # 헤더 없음
        {"Authorization": "Bearer "},         # 빈 토큰
        {"Authorization": "Basic abc"},       # 다른 스킴
    ],
)
async def test_mcp_endpoint_rejects_requests_without_bearer(headers):
    transport = httpx.ASGITransport(app=server.asgi)
    async with httpx.AsyncClient(transport=transport, base_url="http://mcp") as client:
        res = await client.post("/mcp", headers=headers, json={})

    assert res.status_code == 401
    assert res.json()["error"]["code"] == "UNAUTHORIZED"


async def test_health_is_exempt_from_auth():
    transport = httpx.ASGITransport(app=server.asgi)
    async with httpx.AsyncClient(transport=transport, base_url="http://mcp") as client:
        res = await client.get("/health")

    assert res.status_code == 200
    assert res.json()["tools"] == len(EXPECTED_TOOLS)


# ── back 중계 ───────────────────────────────────────────
@respx.mock
async def test_get_forwards_bearer_and_returns_json():
    route = respx.get(f"{settings.chat_back_url}/api/chat-tool/careers").mock(
        return_value=httpx.Response(200, json={"items": [], "count": 0})
    )

    body = await back_client.get("/api/chat-tool/careers", "tok-1")

    assert body == {"items": [], "count": 0}
    assert route.calls.last.request.headers["authorization"] == "Bearer tok-1"


@respx.mock
async def test_none_params_are_dropped():
    """`query=None` 을 그대로 실으면 back 이 문자열 «None» 으로 검색한다."""
    route = respx.get(f"{settings.chat_back_url}/api/chat-tool/notes").mock(
        return_value=httpx.Response(200, json={"items": [], "count": 0})
    )

    await back_client.get("/api/chat-tool/notes", "tok", {"query": None, "limit": 5})

    assert "query" not in route.calls.last.request.url.params
    assert route.calls.last.request.url.params["limit"] == "5"


@respx.mock
@pytest.mark.parametrize(
    ("slug", "expected"),
    [
        ("medisolve-ai-3", "/api/chat-tool/careers/medisolve-ai-3"),
        # `/` 가 경로 구분자가 되지 않는다 — 조각 하나로 남는다.
        ("../../admin/users", "/api/chat-tool/careers/..%2F..%2Fadmin%2Fusers"),
        ("a/b", "/api/chat-tool/careers/a%2Fb"),
        # `?` 가 쿼리 시작이 되지 않는다.
        ("a?x=1", "/api/chat-tool/careers/a%3Fx%3D1"),
        ("한글 slug", "/api/chat-tool/careers/%ED%95%9C%EA%B8%80%20slug"),
    ],
)
async def test_detail_slug_is_url_encoded(slug, expected):
    """모델이 준 slug 가 **URL 문법이 되지 않는다**(리뷰 W5).

    조립을 back_client 한 곳에 모았으므로 tool 마다 잊을 자리가 없다.
    """
    route = respx.get(url__startswith=settings.chat_back_url).mock(
        return_value=httpx.Response(200, json={"item": {}})
    )

    await back_client.get_detail("careers", slug, "tok")

    assert route.calls.last.request.url.raw_path.decode() == expected


@respx.mock
async def test_404_becomes_actionable_not_found():
    """모델이 읽는 문구다 — 「다른 slug 를 추측하지 마라」까지 말한다."""
    respx.get(f"{settings.chat_back_url}/api/chat-tool/careers/x").mock(
        return_value=httpx.Response(404)
    )

    with pytest.raises(NotFoundError) as exc:
        await back_client.get("/api/chat-tool/careers/x", "tok")

    assert "추측" in exc.value.message


@respx.mock
async def test_401_becomes_unauthorized():
    respx.get(f"{settings.chat_back_url}/api/chat-tool/careers").mock(
        return_value=httpx.Response(401)
    )

    with pytest.raises(UnauthorizedError):
        await back_client.get("/api/chat-tool/careers", "tok")


@respx.mock
async def test_server_error_does_not_leak_back_body():
    """back 의 내부 문구가 모델 컨텍스트로 새지 않는다."""
    respx.get(f"{settings.chat_back_url}/api/chat-tool/careers").mock(
        return_value=httpx.Response(500, text="Traceback: secret internal detail")
    )

    with pytest.raises(UpstreamError) as exc:
        await back_client.get("/api/chat-tool/careers", "tok")

    assert "secret internal detail" not in exc.value.message


@respx.mock
async def test_network_failure_is_upstream_error():
    respx.get(f"{settings.chat_back_url}/api/chat-tool/careers").mock(
        side_effect=httpx.ConnectError("refused")
    )

    with pytest.raises(UpstreamError):
        await back_client.get("/api/chat-tool/careers", "tok")


# ── 표기 (render) ───────────────────────────────────────
def test_detail_render_carries_item_for_source_cards():
    """상세는 `structured.item` 을 실어야 한다 — 소비자가 여기서 근거 카드를 뽑는다."""
    from app.render import render_doc

    out = render_doc({"item": {"type": "career", "slug": "a-1", "title": "백엔드", "body": "본문"}})

    assert out["structured"]["item"]["slug"] == "a-1"
    assert "본문" in out["content"][0]["text"]


def test_list_render_carries_items_not_item():
    """목록은 `items` 다 — 훑기만 한 것을 「읽었다」고 말하지 않는다."""
    from app.render import render_list

    out = render_list("경력", {"items": [{"title": "백엔드", "slug": "a-1"}]})

    assert "item" not in out["structured"]
    assert "`a-1`" in out["content"][0]["text"]


def test_empty_list_tells_the_model_to_say_no_record():
    from app.render import render_list

    out = render_list("경력", {"items": []})

    assert "기록에 없다고" in out["content"][0]["text"]


def test_doc_without_body_says_so():
    from app.render import render_doc

    out = render_doc({"item": {"title": "제목", "summary": "요약"}})

    assert "상세 본문이 없습니다" in out["content"][0]["text"]


def test_profile_render_is_not_a_source_card():
    """프로필은 문서가 아니다 — `item` 이 아니라 `profile` 로 실어 카드가 안 생긴다."""
    from app.render import render_profile

    out = render_profile({"item": {"name": "이건학", "role": "백엔드", "email": "a@b.c"}})

    assert "item" not in out["structured"]
    assert out["structured"]["profile"]["name"] == "이건학"
