"""웹 본문 수집 — 정적 → 동적 → 최종 실패 (KDEV-BL-007 케이스 3).

`ax-graph` 의 AXKG-SPEC-012 Web Adapter 를 옮겨 왔다. 이미 도는 코드라 규칙을 새로
정하지 않는다 — 바꾼 것은 이 레포의 `SourceMaterial` 모양에 맞춘 부분뿐이다.

세 단계인 이유는 **실패의 종류가 다르기** 때문이다.

    정적   HTTP GET → HTML. 대부분의 블로그가 여기서 끝난다
    동적   본문이 JS 로 그려지는 페이지. chromium headless 로 렌더한 DOM 을 쓴다
    실패   둘 다 안 되면 **항목을 실패로 남긴다.** 빈 본문으로 요약을 부르지 않는다

종전 `fetch_source` 는 `<태그>` 를 정규식으로 전부 지워 페이지를 통째로 한 덩어리
텍스트로 만들었다. 그러면 네비게이션·푸터·사이드바가 본문에 섞이고, 무엇보다
**JS 로 그리는 페이지가 조용히 「본문 100자」로 성공**한다. 여기서는 그 둘을 가른다.

`ax-graph` 에서 **가져오지 않은 것**은 목록 페이지 취급이다. 저쪽은 링크 후보를
`metadata` 로 돌려주는 소비자가 있어 목록 페이지도 성공으로 쳤는데, 이쪽 파이프라인은
글 한 편을 정리하는 것이 목적이라 그 자리가 없다. 목록 URL 은 분량 미달로 실패한다 —
빈손으로 성공하는 것보다 낫다.
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urljoin

import httpx

from .source import SourceFetchError, SourceMaterial, validate_public_url

#: UI 제거 후 최소 본문 길이. 이보다 짧으면 「본문을 못 찾았다」로 본다.
MIN_CONTENT_LENGTH = 500
MAX_CONTENT_LENGTH = 200_000

MAX_BYTES = 10_000_000
MAX_REDIRECTS = 3
TIMEOUT = 15.0
USER_AGENT = "kknaks-collector/1.0"

NAV_TIMEOUT_MS = 20_000
NETWORKIDLE_TIMEOUT_MS = 8_000
MAX_SCROLLS = 5
SCROLL_WAIT_MS = 600

#: 본문이 아닌 것. 지우고 나서 남는 것이 글이다.
DOM_REMOVE_TAGS = (
    "script", "style", "noscript", "svg", "canvas", "template", "iframe",
    "header", "nav", "footer", "form", "dialog",
    "button", "input", "select", "textarea",
)

#: 「JS 켜라」 안내가 본문 자리를 차지한 페이지 — 동적으로 넘어가야 한다는 신호다.
JS_REQUIRED_MARKERS = (
    "enable javascript",
    "please enable js",
    "javascript is required",
    "자바스크립트를 활성화",
)

#: 로그인·유료 장벽. **동적으로 넘어가도 소용없다** — 브라우저를 띄워도 로그인은 안 된다.
PAYWALL_MARKERS = (
    "sign in to continue",
    "subscribe to read",
    "create a free account to",
    "로그인 후 이용",
    "구독을 해야",
)


class WebCollectError(SourceFetchError):
    """수집 실패. `code` 로 **어느 단계에서 왜** 실패했는지를 남긴다.

    `SourceFetchError` 를 상속하는 이유는 `submit_preparation` 이 수집 실패를
    `except Exception` 으로 받아 `collect_error` 에 문자열로 담기 때문이다 — 계약을
    바꾸지 않고 진단만 더한다.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


CONTENT_FETCH_FAILED = "CONTENT_FETCH_FAILED"
CONTENT_EXTRACT_FAILED = "CONTENT_EXTRACT_FAILED"
DYNAMIC_RENDER_REQUIRED = "DYNAMIC_RENDER_REQUIRED"
DYNAMIC_RENDER_FAILED = "DYNAMIC_RENDER_FAILED"
PAYWALL_OR_AUTH_REQUIRED = "PAYWALL_OR_AUTH_REQUIRED"
SOURCE_TOO_LARGE = "SOURCE_TOO_LARGE"
FETCH_TIMEOUT = "FETCH_TIMEOUT"
UNSUPPORTED_SOURCE_TYPE = "UNSUPPORTED_SOURCE_TYPE"

#: 정적이 이 코드로 실패하면 **동적으로 올라간다.** 나머지는 올라가도 결과가 같다 —
#: paywall 은 브라우저를 띄워도 로그인이 안 되고, 크기 초과는 렌더해도 초과다.
FALLBACK_CODES = frozenset({DYNAMIC_RENDER_REQUIRED, CONTENT_EXTRACT_FAILED})


@dataclass(frozen=True)
class FetchedPage:
    final_url: str
    content_type: str
    html: str


@dataclass(frozen=True)
class RenderedPage:
    final_url: str
    html: str


#: 테스트가 가짜를 주입한다 — 네트워크도 브라우저도 없이 검사한다.
HtmlFetcher = Callable[[str], Awaitable[FetchedPage]]
PageRenderer = Callable[[str], Awaitable[RenderedPage]]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- 정적 -------------------------------------------------------------------


async def default_html_fetch(
    url: str,
    *,
    timeout: float = TIMEOUT,
    max_bytes: int = MAX_BYTES,
    max_redirects: int = MAX_REDIRECTS,
    transport: httpx.AsyncBaseTransport | None = None,
) -> FetchedPage:
    """리다이렉트를 **직접 따라간다.** 매 홉마다 SSRF 가드를 다시 건다.

    `follow_redirects=True` 로 두면 httpx 가 알아서 따라가고, 그러면 공개 도메인이
    내부 주소로 리다이렉트하는 경로를 검사할 수 없다.

    상한과 `transport` 를 인자로 받는 이유는 **`fetch_source` 가 이미 그 계약을 갖고
    있기** 때문이다. 여기서 하드코딩하면 그 인자를 준 호출자가 조용히 무시당한다.
    """
    current = url
    async with httpx.AsyncClient(
        timeout=timeout, follow_redirects=False, transport=transport
    ) as client:
        for _ in range(max_redirects + 1):
            await validate_public_url(current)
            try:
                async with client.stream(
                    "GET", current, headers={"User-Agent": USER_AGENT}
                ) as response:
                    if response.status_code in {301, 302, 303, 307, 308}:
                        location = response.headers.get("location")
                        if not location:
                            raise WebCollectError(
                                CONTENT_FETCH_FAILED, "redirect 에 location 이 없다"
                            )
                        current = urljoin(current, location)
                        continue
                    response.raise_for_status()
                    chunks: list[bytes] = []
                    size = 0
                    async for chunk in response.aiter_bytes():
                        size += len(chunk)
                        if size > max_bytes:
                            raise WebCollectError(SOURCE_TOO_LARGE, "크기 상한 초과")
                        chunks.append(chunk)
                    return FetchedPage(
                        final_url=current,
                        content_type=response.headers.get("content-type", ""),
                        html=b"".join(chunks).decode(
                            response.encoding or "utf-8", errors="replace"
                        ),
                    )
            except httpx.TimeoutException as exc:
                raise WebCollectError(FETCH_TIMEOUT, "정적 수집 timeout") from exc
            except httpx.HTTPError as exc:
                raise WebCollectError(CONTENT_FETCH_FAILED, "정적 수집 HTTP 실패") from exc
    raise WebCollectError(CONTENT_FETCH_FAILED, "redirect 횟수 초과")


async def collect_static(
    url: str, *, html_fetch: HtmlFetcher | None = None, **limits
) -> SourceMaterial:
    page = await (
        html_fetch(url) if html_fetch is not None else default_html_fetch(url, **limits)
    )
    if "text/html" not in page.content_type.lower():
        raise WebCollectError(
            UNSUPPORTED_SOURCE_TYPE, f"수집기가 없는 content-type: {page.content_type}"
        )
    return process_document(page.html, page.final_url, allow_dynamic_fallback=True)


# --- 동적 -------------------------------------------------------------------


async def default_render(url: str) -> RenderedPage:
    """chromium headless 로 렌더한다. 다운로드·팝업을 막고 시간과 스크롤을 제한한다.

    `playwright` 는 **함수 안에서** import 한다 — 브라우저가 없는 환경(테스트·CI)에서
    모듈을 읽는 것만으로 실패하면 안 된다.
    """
    from playwright.async_api import async_playwright

    await validate_public_url(url)
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            try:
                context = await browser.new_context(accept_downloads=False)
                page = await context.new_page()
                context.on("page", lambda popup: asyncio.ensure_future(popup.close()))
                await page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                try:
                    await page.wait_for_load_state(
                        "networkidle", timeout=NETWORKIDLE_TIMEOUT_MS
                    )
                except Exception:  # noqa: BLE001 — networkidle 미도달은 치명적이지 않다
                    pass
                # 무한 스크롤 페이지에서 본문이 뒤늦게 붙는다. **횟수를 제한한다** —
                # 끝없이 내리면 잡이 안 끝난다.
                for _ in range(MAX_SCROLLS):
                    await page.mouse.wheel(0, 20_000)
                    await page.wait_for_timeout(SCROLL_WAIT_MS)
                return RenderedPage(final_url=page.url, html=await page.content())
            finally:
                await browser.close()
    except WebCollectError:
        raise
    except Exception as exc:  # noqa: BLE001 — 렌더 실패는 상태로 남긴다
        raise WebCollectError(DYNAMIC_RENDER_FAILED, "브라우저 렌더링 실패/timeout") from exc


async def collect_dynamic(url: str, *, render: PageRenderer | None = None) -> SourceMaterial:
    page = await (render or default_render)(url)
    return process_document(page.html, page.final_url, allow_dynamic_fallback=False)


# --- 공통 처리 ---------------------------------------------------------------


def _first_meta(soup, *, prop: str | None = None, name: str | None = None) -> str | None:
    if prop is not None:
        tag = soup.find("meta", attrs={"property": prop})
        if tag and tag.get("content"):
            return str(tag["content"]).strip()
    if name is not None:
        tag = soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return str(tag["content"]).strip()
    return None


def _extract_title(soup) -> str | None:
    og = _first_meta(soup, prop="og:title")
    if og:
        return og
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return None


def _post_process(text: str) -> str:
    """반복 공백을 줄이고 **연속으로 같은 줄을 지운다.**

    UI 를 지우고 남은 텍스트에는 `더보기` 같은 줄이 수십 번 반복된다. 그대로 두면
    요약 입력의 절반이 그 줄이다.
    """
    lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in text.splitlines()]
    out: list[str] = []
    blank_run = 0
    prev: str | None = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_run += 1
            if blank_run <= 1:
                out.append("")
            continue
        blank_run = 0
        if stripped == prev:
            continue
        prev = stripped
        out.append(stripped)
    return "\n".join(out).strip()


def process_document(
    html: str, final_url: str, *, allow_dynamic_fallback: bool
) -> SourceMaterial:
    """DOM 정리 → 본문·제목 추출 → 후처리 → 분량 판정.

    `allow_dynamic_fallback` 이 참이면(정적) 분량 미달을 **동적으로 올라가라는 신호**로
    올린다. 거짓이면(동적) 같은 상황이 최종 실패다.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html or "", "html.parser")

    # 제목은 **UI 를 지우기 전에** 읽는다 — `<head>` 와 헤더에 들어 있다.
    title = _extract_title(soup)

    for tag in soup(list(DOM_REMOVE_TAGS)):
        tag.decompose()

    content = _post_process(soup.get_text(separator="\n"))
    lowered = content.lower()

    if any(m in lowered for m in PAYWALL_MARKERS) and len(content) < MIN_CONTENT_LENGTH:
        # **동적으로 올라가지 않는다.** 브라우저를 띄워도 로그인은 안 된다.
        raise WebCollectError(PAYWALL_OR_AUTH_REQUIRED, "로그인/유료 안내가 본문을 대체했다")

    if len(content) < MIN_CONTENT_LENGTH:
        if not allow_dynamic_fallback:
            raise WebCollectError(
                CONTENT_EXTRACT_FAILED, "동적 렌더링 뒤에도 본문 분량이 미달이다"
            )
        if any(m in lowered for m in JS_REQUIRED_MARKERS) or not soup.find("a", href=True):
            raise WebCollectError(DYNAMIC_RENDER_REQUIRED, "JS 렌더링 없이는 본문이 부족하다")
        raise WebCollectError(CONTENT_EXTRACT_FAILED, "정적 추출 본문 분량이 미달이다")

    return SourceMaterial(
        url=final_url,
        source_type="blog",
        title=title,
        content=content[:MAX_CONTENT_LENGTH],
        accessed_at=_utc_now(),
    )


async def collect_web(
    url: str,
    *,
    html_fetch: HtmlFetcher | None = None,
    render: PageRenderer | None = None,
    **limits,
) -> SourceMaterial:
    """정적 → 동적 → 최종 실패.

    **올라가는 조건을 좁게 둔다.** 정적이 실패했다고 무조건 브라우저를 띄우지 않는다 —
    paywall·크기 초과·timeout 은 렌더해도 결과가 같고, chromium 을 띄우는 비용만 든다.
    """
    try:
        return await collect_static(url, html_fetch=html_fetch, **limits)
    except WebCollectError as exc:
        if exc.code not in FALLBACK_CODES:
            raise
        return await collect_dynamic(url, render=render)

