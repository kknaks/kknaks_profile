"""채용담당자 채팅 MCP 서버 — tool 13종 (KDEV-SPEC-017 §4 Tool Contract / DEC-027 D5).

## 프레임워크 선택 (WORK-023 Open Issue)

공식 `mcp` SDK 의 **FastMCP + Streamable HTTP** 를 쓴다. 근거는 「같은 조합이 이미
검증됐다」다 — 레퍼런스(`harness_works/mediness-app/mcp`)가 codex 의
`-c mcp_servers.<key>.url` + `http_headers` Bearer 로 이 transport 를 물려 돌고 있고,
`enabled_tools`·`tools.<name>.approval_mode` 같은 codex 쪽 손잡이가 그 조합 기준으로
실측됐다. 다른 프레임워크를 고르면 그 실측치가 전부 다시 재야 하는 값이 된다.

**stateless_http=True** 인 이유: 세션에 얹을 상태가 없다(전부 back 소유). stateful 이면
세션이 프로세스 메모리에 살아 배포마다 증발하고, 살아 있던 session id 로 온 요청이
SDK 계층에서 404 를 맞는다.

## 이 서버가 하지 않는 일

- **토큰 검증** — 헤더가 아예 없는 호출만 여기서 막는다. 유효성은 back 이 본다
  (`back_client.py` 머리 주석). 게이트를 두 곳에 두지 않는다.
- **노출 판정** — `chat_exposed` 는 back 이 매 호출 DB 에서 본다(DEC-027 D4).
- **slug → 경로 해석** — back 이 한다. 여기로 경로가 흐르는 길 자체가 없다.

## tool 설명을 성의 있게 쓴다

이름·설명·인자 스키마가 모델의 tool 선택 품질을 정한다([[ai-agent]]). 그래서 각
docstring 이 세 가지를 말한다 — **무엇을 주나 · 무엇을 안 주나 · 다음에 무엇을 하나**.
「종료 조건」을 적는 것도 같은 이유다: 안 잡히는 것을 말만 바꿔 반복하는 것이 이 구조의
기본 실패 모드다.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from contextvars import ContextVar

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from app import back_client
from app.config import settings
from app.errors import McpError, UnauthorizedError
from app.render import render_doc, render_list, render_profile

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

#: 이 요청의 turn 토큰. 미들웨어가 세팅하고 tool 이 읽는다. **로그로 나가지 않는다.**
current_token: ContextVar[str] = ContextVar("current_token", default="")

mcp = FastMCP(
    "kknaks",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=settings.allowed_hosts,
        allowed_origins=settings.allowed_origins,
    ),
    stateless_http=True,
)


def _token() -> str:
    token = current_token.get()
    if not token:
        raise UnauthorizedError()
    return token


async def _get(path: str, params: dict | None = None) -> dict:
    """chat-tool 한 번. 실패는 로그에 남기고 **모델이 읽을 문구로** 올려 보낸다.

    FastMCP 가 tool 예외를 `str(exc)` 로 실어 주므로 `McpError` 의 문구가 그대로
    모델에게 간다 — 그래서 `errors.py` 의 문장이 사람 대상이 아니라 모델 대상이다.
    """
    try:
        return await back_client.get(path, _token(), params)
    except McpError as exc:
        logger.info("tool 실패: %s code=%s", path, exc.code)
        raise


async def _get_detail(collection: str, slug: str) -> dict:
    """상세 조회 — **slug 를 f-string 으로 경로에 붙이지 않는다**.

    slug 는 모델이 준 값이라 URL 이스케이프를 거쳐야 한다. 조립을 `back_client` 한
    곳에 두는 이유는 여기서 잊을 수 없게 하려는 것이다(리뷰 W5).
    """
    try:
        return await back_client.get_detail(collection, slug, _token())
    except McpError as exc:
        # slug 는 로그에 안 찍는다 — 모델이 준 임의 문자열이다.
        logger.info("tool 실패: %s 상세 code=%s", collection, exc.code)
        raise


# ── 프로필 ──────────────────────────────────────────────
@mcp.tool()
async def get_profile() -> dict:
    """이건학의 신원 한 벌 — 이름 · 직함 · 연차 · 위치 · focus · 주요 스택 · 이메일.

    **주는 것**: 「이 사람이 누구인가」에 답할 최소 사실.
    **안 주는 것**: 경력·프로젝트 내용. 그건 `list_career` · `list_projects` 다.

    **언제**: 시스템 프롬프트의 요약이 낡아 보이거나, 연락처·연차처럼 정확한 값을
    말해야 할 때. 매 답변마다 부를 필요는 없다."""
    return render_profile(await _get("/api/chat-tool/profile"))


# ── career ─────────────────────────────────────────────
@mcp.tool()
async def list_career() -> dict:
    """직장 경력 목록 — 기간 · 직함 · 조직 · 한 줄 요약. **노출 승인된 역할만** 나온다.

    **주는 것**: 각 역할의 `slug` 와 요약.
    **안 주는 것**: 역할 상세. 그건 `get_career(slug)` 다.

    **사슬**: 여기서 얻은 `slug` 를 `get_career` 에 그대로 넣는다.
    **비어 있으면**: 승인된 경력이 없는 것이다 — 기록에 없다고 답한다. 다른 tool 로
    우회해 경력을 유추하지 않는다."""
    return render_list("경력", await _get("/api/chat-tool/careers"))


@mcp.tool()
async def get_career(slug: str) -> dict:
    """역할 하나의 상세 — 맡은 일 · 기간 · 조직 · 스택.

    **`slug`**: `list_career` 가 준 값을 그대로 쓴다(`<회사>-<번호>` 꼴). 지어내지 않는다.
    **안 주는 것**: 회사 내부 업무 상세 · 비공개 프로젝트.
    **404 면**: 그 역할은 존재하지 않는다. 다른 slug 를 추측해 다시 부르지 않는다."""
    return render_doc(await _get_detail("careers", slug))


# ── project ────────────────────────────────────────────
@mcp.tool()
async def list_projects() -> dict:
    """개인 프로젝트 목록 — 제목 · 요약 · 스택 · 상태. **노출 승인된 것만** 나온다.

    회사에서 만든 제품이 아니라 **혼자 만든 것**이다. 회사 일은 `list_career` ·
    `list_problems` 쪽이다.

    **사슬**: `slug` → `get_project(slug)` 로 showcase 본문을 읽는다."""
    return render_list("개인 프로젝트", await _get("/api/chat-tool/projects"))


@mcp.tool()
async def get_project(slug: str) -> dict:
    """프로젝트 하나의 showcase 본문 — 무엇을 왜 만들었고 어떻게 굴러가는지.

    **`slug`**: `list_projects` 가 준 값 그대로.
    **안 주는 것**: 스펙 문서 · 환경설정 · 배포 구성 · 코드. 그건 공개 범위 밖이다 —
    물어보면 「공개하지 않는다」고 답한다."""
    return render_doc(await _get_detail("projects", slug))


# ── problem ────────────────────────────────────────────
@mcp.tool()
async def list_problems() -> dict:
    """실무에서 **푼 문제** 목록 — 어느 회사·역할에서 무엇을 풀었나.

    이력의 알맹이다. 「어떤 어려움을 겪었나」 · 「무엇을 개선했나」 · 「트러블슈팅
    경험」류 질문은 여기서 시작한다.

    **사슬**: `slug`(`problem-<번호>`) → `get_problem(slug)` 로 어떻게 풀었는지 읽는다."""
    return render_list("해결한 문제", await _get("/api/chat-tool/problems"))


@mcp.tool()
async def get_problem(slug: str) -> dict:
    """문제 하나의 상세 — 무엇이 문제였고 어떻게 풀었나.

    **`slug`**: `list_problems` 가 준 값 그대로.
    **안 주는 것**: 승인 전 문제 · 사내 시스템 내부 정보."""
    return render_doc(await _get_detail("problems", slug))


# ── company product ────────────────────────────────────
@mcp.tool()
async def list_company_products() -> dict:
    """**회사에서 만든 제품** 목록 — 재직 중인 회사와 전 회사의 제품 전부.

    「회사에서 무슨 일을 했나」 · 「어떤 서비스를 만들어 봤나」 · 「실무 경험」류 질문의
    출발점이다. **`list_projects`(혼자 만든 개인 프로젝트)와 다른 것**이니 둘을 섞지 마라 —
    회사 일을 물으면 이 tool 이다.

    **주는 것**: 제품별 `slug` · 어느 회사·어느 역할에서 만들었나 · 요약 · 스택 · 상태.
    **사슬**: `slug` → `get_company_product(slug)` 로 제품 소개 본문을 읽는다.
    **비어 있으면**: 노출 승인된 제품이 없는 것이다 — 기록에 없다고 답한다."""
    return render_list("회사 제품", await _get("/api/chat-tool/company-products"))


@mcp.tool()
async def get_company_product(slug: str) -> dict:
    """회사 제품 하나의 소개 본문 — 무엇을 만들었고 어떤 문제를 풀었는지.

    **`slug`**: `list_company_products` 가 준 값 그대로.
    **안 주는 것**: 작업 회고(`log/`) · 내부 스펙 · 배포 구성 등 회사 내부 기록. 공개된
    제품 소개까지가 범위다 — 더 물으면 「공개하지 않는다」고 답한다."""
    return render_doc(await _get_detail("company-products", slug))


# ── note · content · algorithm ─────────────────────────
@mcp.tool()
async def search_notes(query: str | None = None) -> dict:
    """공개 학습노트 검색 — 제목 · 요약 · 태그를 훑는다.

    **주는 것**: 「이 기술을 공부한 기록이 있나」의 답.
    **안 주는 것**: 개인 지식 저장소(resources · persona) 전체. 공개 등록된 노트만이다.

    **사슬**: `slug` → `get_note(slug)` 로 본문을 읽는다.
    **종료 조건**: 같은 주제를 말만 바꿔 두어 번 검색해 안 잡히면 **기록에 그 내용이
    없는 것**이다. 검색어를 더 비틀지 말고 없다고 답한다."""
    return render_list("학습노트", await _get("/api/chat-tool/notes", {"query": query}))


@mcp.tool()
async def get_note(slug: str) -> dict:
    """학습노트 하나의 본문.

    **`slug`**: `search_notes` 가 준 값 그대로."""
    return render_doc(await _get_detail("notes", slug))


@mcp.tool()
async def list_contents() -> dict:
    """공개 영상·교안 목록 — 만든 콘텐츠가 있는지 물을 때.

    목록뿐이다. 각 항목의 본문을 읽는 tool 은 없다 — 제목·요약까지가 공개 범위다."""
    return render_list("영상·교안", await _get("/api/chat-tool/contents"))


@mcp.tool()
async def list_algorithms() -> dict:
    """공개 알고리즘 풀이 목록 — 제목 · 난이도 · 출처 플랫폼.

    코딩테스트 준비 여부를 묻는 질문에 쓴다. 목록뿐이고 풀이 본문은 주지 않는다."""
    return render_list("알고리즘 풀이", await _get("/api/chat-tool/algorithms"))


# ── ASGI ───────────────────────────────────────────────
_EXEMPT_PATHS = frozenset({"/health"})


async def _health(_request):
    # 11 + 회사 제품 2종(spec v0.0.8).
    return JSONResponse({"status": "ok", "name": "kknaks", "tools": 13})


class TurnTokenMiddleware(BaseHTTPMiddleware):
    """`Authorization: Bearer <turn token>` → ContextVar.

    **검증하지 않는다** — 헤더가 없는 호출만 막는다(DEC-027 D5 「토큰 없는 호출을
    거부한다」). 유효성은 back 이 chat-tool 요청에서 본다. 여기서 한 번 더 보면
    같은 규칙이 두 곳에 살고 언젠가 한쪽만 바뀐다.
    """

    async def dispatch(self, request, call_next):
        if request.url.path in _EXEMPT_PATHS:
            return await call_next(request)
        header = request.headers.get("authorization", "")
        if not header.lower().startswith("bearer "):
            return JSONResponse(
                {"error": {"code": "UNAUTHORIZED", "message": "turn 토큰이 없습니다"}},
                status_code=401,
            )
        token = header[7:].strip()
        if not token:
            return JSONResponse(
                {"error": {"code": "UNAUTHORIZED", "message": "turn 토큰이 비어 있습니다"}},
                status_code=401,
            )
        reset = current_token.set(token)
        try:
            return await call_next(request)
        finally:
            current_token.reset(reset)


_streamable_app = mcp.streamable_http_app()


@asynccontextmanager
async def _lifespan(_app):
    # inner Starlette 의 자체 lifespan 은 Mount 로 감싸면 자동 발화하지 않는다
    # (Starlette 알려진 동작) — 여기서 명시하지 않으면 POST /mcp 가
    # 「Task group is not initialized」로 죽는다.
    async with mcp.session_manager.run():
        yield


asgi = Starlette(
    routes=[
        Route("/health", _health),
        # Streamable HTTP — SDK 기본 경로가 /mcp 다. 제출부의 `chat_mcp_url` 과 짝이다.
        Mount("/", app=_streamable_app),
    ],
    lifespan=_lifespan,
    middleware=[Middleware(TurnTokenMiddleware)],
)
