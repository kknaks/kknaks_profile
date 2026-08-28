"""back chat-tool 호출 — 이 서버가 하는 일의 전부다.

## 판정을 여기서 하지 않는다

노출(`chat_exposed`)도 turn 토큰 검증도 back 이 한다. 이 서버가 두 번째 게이트가 되면
같은 규칙이 두 곳에 살고, 언젠가 한쪽만 바뀐다. 여기는 **중계와 표기**만 한다.

turn 토큰을 그대로 실어 보내는 것이 곧 검증이다 — back 이 그 요청을 받아 토큰을 보고
데이터를 준다. 왕복 한 번에 인증과 조회가 같이 끝나므로 별도 verify 엔드포인트도,
폐기 캐시도 필요 없다.
"""

from __future__ import annotations

from urllib.parse import quote

import httpx

from app.config import settings
from app.errors import NotFoundError, UnauthorizedError, UpstreamError


def make_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=settings.chat_back_url, timeout=settings.chat_back_timeout_sec
    )


async def get_detail(collection: str, slug: str, token: str) -> dict:
    """상세 조회 — **모델이 준 문자열이 URL 로 흘러가는 유일한 자리**.

    slug 는 모델이 제어한다. 그래서 경로 조립을 호출부에 맡기지 않고 여기 한 곳으로
    모으고, `quote(safe="")` 로 `/` 를 포함한 모든 문자를 이스케이프한다 — 조각 하나가
    URL **문법**이 될 길을 끊는다.

    지금도 뚫리는 경로는 확인되지 않았다(FastAPI 의 `{slug}` 는 `/` 를 매칭하지 않아
    전부 404 로 끝난다). 그래도 닫는 이유는 DEC-027 이 「경계는 지시가 아니라 구조」를
    태도로 잡았기 때문이다 — 안전이 상류 라우팅의 우연에 기대지 않게 한다(리뷰 W5).
    """
    return await get(f"/api/chat-tool/{collection}/{quote(slug, safe='')}", token)


async def get(path: str, token: str, params: dict | None = None) -> dict:
    """chat-tool GET 한 번. 에러는 모델이 읽을 문구로 번역한다.

    ⚠ `path` 는 **우리가 만든 상수**여야 한다. 모델이 준 값이 경로 조각으로 들어가는
    호출은 `get_detail` 을 쓴다.
    """
    async with make_client() as client:
        try:
            resp = await client.get(
                path,
                params={k: v for k, v in (params or {}).items() if v is not None},
                headers={"Authorization": f"Bearer {token}"},
            )
        except httpx.HTTPError as exc:
            raise UpstreamError(f"이력 데이터 서버에 닿지 못했습니다: {exc}") from exc

    if resp.status_code == 401:
        raise UnauthorizedError()
    if resp.status_code == 404:
        raise NotFoundError()
    if resp.status_code >= 400:
        # 본문을 그대로 흘리지 않는다 — 내부 문구가 모델 컨텍스트로 새지 않게.
        raise UpstreamError(f"이력 데이터를 읽지 못했습니다 (status={resp.status_code})")
    try:
        return resp.json()
    except ValueError as exc:
        raise UpstreamError("이력 데이터 응답을 해석하지 못했습니다") from exc
