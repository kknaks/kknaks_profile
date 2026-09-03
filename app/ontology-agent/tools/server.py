"""FastMCP 도구 서버 — 조회 도구 **정확히 4종**(SPEC-002).

골격은 `app/mcp/app/server.py` 를 그대로 따른다 — FastMCP + Streamable HTTP,
`stateless_http=True`, `Mount("/", streamable_http_app())`, lifespan 명시,
`TransportSecuritySettings`. 같은 조합이 이미 검증됐다(연구 §5.3).

## 이 서버가 하지 않는 일

- **집계** — 골드 View 가 한다. 도구는 이미 계산된 것을 돌려줄 뿐이다(S-002).
- **관계 지식 보유** — 어떤 KPI 가 어떤 KPI 의 원인인지는 코드 상수에 없고
  `ontology_edges` 조회로만 나온다(S-001).
- **자유 SQL** — `sql`·`query`·`path` 류 파라미터가 **표면 자체로 없다**. 거부가 아니라
  부재다(SPEC-002 S-6).
- **쓰기** — 읽기 전용 커넥션으로만 연다.

## 도구 설명을 성의 있게 쓴다

이름·설명·인자 스키마가 모델의 도구 선택 품질을 정한다. 각 docstring 이 세 가지를
말한다 — **무엇을 주나 · 무엇을 안 주나 · 언제 쓰나.**
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from config import settings
from service import allowlist as al
from service import glossary
from service.db import open_serving_db
from service.errors import InvalidRange, QueryError, UnknownTerm
from service.queries import query_kpi as _query_kpi
from service.queries import query_layer as _query_layer
from service.queries import trace_ontology as _trace_ontology

logger = logging.getLogger(__name__)

#: 도구 목록 — 정확히 4종. 자유 SQL·파일·쉘 도구는 0개다(SPEC-002 AC-1).
TOOL_NAMES = ("query_kpi", "query_layer", "trace_ontology", "get_definition")

mcp = FastMCP(
    "ontology",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=settings.mcp_allowed_hosts,
        allowed_origins=settings.mcp_allowed_origins,
    ),
    stateless_http=True,
)


def _fail(exc: QueryError) -> dict:
    """거부를 **모델이 읽을 응답**으로 돌려준다.

    예외를 올리면 문구가 문자열로 뭉개진다. 거부는 정상적인 대화의 일부이므로
    구조를 유지해 허용 목록이 그대로 모델에게 가게 한다(SPEC-002 AC-2).
    """
    logger.info("도구 거부: %s", exc.code)
    return exc.to_tool_payload()


@mcp.tool()
def query_kpi(
    metrics: list[str],
    grain: str,
    start: str,
    end: str,
    include_status: bool = True,
    include_deltas: bool = False,
) -> dict:
    """골드 KPI 조회 — 이미 계산된 집계값을 기간·그레인으로 받는다.

    **주는 것**: 지표별 값 + 상태(양호/주의/경고) + **계산식**과 **상태 경계**.
    계산식이 함께 오므로 답변에 근거를 달 수 있다.
    **안 주는 것**: 원본 행. 그건 `query_layer` 다. 관계·원인도 아니다 — `trace_ontology` 다.

    **언제**: 「추이는?」·「얼마야?」처럼 수치를 묻는 질문. 원인 질문에서도 **전제 확인**을
    먼저 하는 데 쓴다(「8월 매출이 왜 떨어졌어?」 → 정말 떨어졌는지부터 본다).

    `grain` 은 `daily`·`weekly`·`monthly`·`retention_monthly` 이고 각각 골드 View 하나에
    대응한다 — **네가 합산하지 마라.** 주별·월별 값은 이미 만들어져 있다.

    `null` 과 `0` 은 다르다 — `naver_reviews` 의 2026-03-21 이전은 관측 자체가 없어
    `null` 이고, 강남언니 리뷰 없는 주는 실제 `0` 이다. 섞어 읽지 마라.
    """
    try:
        with open_serving_db() as conn:
            return _query_kpi(
                conn, metrics=metrics, grain=grain, start=start, end=end,
                include_status=include_status, include_deltas=include_deltas,
            )
    except QueryError as exc:
        return _fail(exc)


@mcp.tool()
def query_layer(
    layer: str,
    table: str,
    filters: list[dict] | None = None,
    order_by: dict | None = None,
    limit: int = al.DEFAULT_TOOL_LIMIT,
    offset: int = 0,
) -> dict:
    """브론즈·실버 **원본 행** 조회 — 집계가 아니라 실제 행을 봐야 할 때.

    **주는 것**: 마스킹된 행 + `total`(조건에 맞는 전체 건수) + `masked_fields`.
    **안 주는 것**: 개인정보 원값. 이름은 `김○○`, 전화는 `010-****-1234`,
    생년월일은 `1990-**-**` 로만 나온다 — 우회 경로는 없다.

    **언제**: 「그 취소들 원본 보여줘」처럼 근거 행을 제시해야 할 때. 수치 요약이
    필요하면 `query_kpi` 를 써라.

    `limit` 은 1~200 이다. **초과하면 잘라서 주는 게 아니라 거부한다** — 낮춰서 다시 불러라.
    `total` 이 항상 오므로 「N건 중 M건」을 정확히 말할 수 있다.

    필터 필드는 허용 목록 안이어야 한다. 목록 밖 이름(개인정보 원 컬럼 포함)은
    `UNKNOWN_FIELD` 로 거부되고, 거부 응답에 쓸 수 있는 필드 목록이 함께 온다.
    """
    try:
        with open_serving_db() as conn:
            return _query_layer(
                conn, layer=layer, table=table, filters=filters,
                order_by=order_by, limit=limit, offset=offset,
            )
    except QueryError as exc:
        return _fail(exc)


@mcp.tool()
def trace_ontology(
    node: str | None = None,
    direction: str = "both",
    depth: int = 1,
    verdicts: list[str] | None = None,
) -> dict:
    """KPI 사이의 **관계**를 조회한다 — 원인·결과 엣지와 그 판정.

    **주는 것**: 노드·엣지 + **판정**(채택·자동 확정·선언·보류·기각) + 근거·사유 +
    `usable_for_causal_claim`.
    **안 주는 것**: 수치. 값이 필요하면 `query_kpi` 를 이어 불러라.

    **언제**: 「왜」로 시작하는 질문. 관계를 네가 알고 있다고 가정하지 마라 —
    이 도구가 돌려주는 것만이 이 제품이 인정하는 관계다.

    **판정을 반드시 읽어라.** `usable_for_causal_claim: false` 인 엣지(보류·기각)를
    인과 서술에 쓰면 안 된다. 기각 행은 **배제 근거**로만 인용한다 —
    「프로모션 때문 아닌가」에 「기각됐고 사유는 이렇다」로 답하는 것이 옳은 사용이다.

    기본 호출은 채택·자동 확정·선언만 준다. 기각·보류를 보려면 `verdicts` 에 명시해라.
    `observed: false` 인 노드는 데이터가 없는 것이다 — 추측하지 말고 모른다고 답해라.
    """
    try:
        with open_serving_db() as conn:
            return _trace_ontology(
                conn, node=node, direction=direction, depth=depth, verdicts=verdicts,
            )
    except QueryError as exc:
        return _fail(exc)


@mcp.tool()
def get_definition(term: str) -> dict:
    """용어·KPI 컬럼·enum 의 **정의와 계산식**을 조회한다.

    **주는 것**: 정의 · 계산식 · 판정 상태(확정/승계/대기) · 근거 기록 · 관련 컬럼.
    폐쇄 목록(시술 개념 13종)·감성 4값 같은 enum 도 여기서 나온다.
    **안 주는 것**: 값. 수치는 `query_kpi` 다.

    **언제**: 계산식을 답변에 인용하기 전. 「노쇼율」처럼 분모가 헷갈리는 용어는
    지어내지 말고 여기서 확인해라 — 취소가 분모에 들어가는지 아닌지가 여기 적혀 있다.

    없는 용어는 404 와 함께 유사 후보가 온다. 후보를 무한히 비틀지 말고,
    두어 번 안 잡히면 **정의된 용어가 아니다**로 답해라.
    """
    if not isinstance(term, str) or not (1 <= len(term.strip()) <= 100):
        # SPEC-002 Validation — `term` 1~100자
        return _fail(InvalidRange("term 은 1~100자다", allowed=glossary.all_terms()[:10]))
    try:
        return glossary.definition_payload(term)
    except KeyError:
        return _fail(UnknownTerm(
            f"글로서리에 없는 용어: {term!r}", allowed=glossary.suggestions(term)))


# --- ASGI -------------------------------------------------------------------


async def _health(_request):
    return JSONResponse({"status": "ok", "name": "ontology", "tools": len(TOOL_NAMES)})


_streamable_app = mcp.streamable_http_app()


@asynccontextmanager
async def _lifespan(_app):
    # Mount 로 감싸면 inner Starlette 의 lifespan 이 자동 발화하지 않는다(Starlette 알려진
    # 동작) — 명시하지 않으면 POST /mcp 가 「Task group is not initialized」로 죽는다.
    async with mcp.session_manager.run():
        yield


asgi = Starlette(
    routes=[
        Route("/health", _health),
        Mount("/", app=_streamable_app),
    ],
    lifespan=_lifespan,
)
