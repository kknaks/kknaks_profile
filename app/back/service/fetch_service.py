"""가져오기 — 비동기 처리(inbox.md Step 3)의 첫 단계. 종류별로 방법만 다르다.

- youtube: 자막(youtube-transcript-api) + 메타(제목·채널·길이 — watch 페이지 파싱,
  실패하면 oEmbed 로 제목·채널만)
- docs · article · blog: **3단계** — 정적(httpx) → 동적(playwright chromium, 필요할
  때만) → 실패. `_archive` 의 knowledge_capture/web.py(ax-graph 이식분)에서 단계
  구조·전환 신호·상수를 가져왔고, **본문 추출은 trafilatura 유지**(태그 제거 방식보다
  추출 품질이 낫다 — 네비·푸터가 안 섞인다).

  정적   GET → trafilatura. 대부분 여기서 끝난다
  동적   JS 마커 또는 본문 500자 미만이면 chromium 렌더 DOM → trafilatura 재추출
  실패   그래도 미달이면 FetchError — 단계·사유 코드가 queue.error 에 남는다

**봇 차단(403 등)·페이월·Cloudflare 챌린지는 그대로 실패다 — 우회하지 않는다**
(발주 결정). UA 위장·프록시·재시도 fallback 을 쌓지 않고, 실패 사유 한 줄을 남긴다.
페이월은 렌더 없이 즉시 실패다 — 브라우저를 띄워도 로그인은 안 되고 비용만 든다.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass

import httpx

from core.exceptions import ValidationError

logger = logging.getLogger(__name__)

# --- 웹 3단계 상수 — 레거시(_archive/…/knowledge_capture/web.py) 값 그대로 -------

#: 추출 본문 최소 길이. 이보다 짧으면 「본문을 못 찾았다」 — 정적이면 동적으로 넘어간다.
#: 목록 페이지도 여기서 걸린다 — 빈손으로 성공하는 것보다 실패가 낫다.
MIN_CONTENT_LENGTH = 500
MAX_CONTENT_LENGTH = 200_000
TIMEOUT = 15.0
USER_AGENT = "kknaks-collector/1.0"  # 정직한 UA — 위장하지 않는다

NAV_TIMEOUT_MS = 20_000
NETWORKIDLE_TIMEOUT_MS = 8_000
MAX_SCROLLS = 5
SCROLL_WAIT_MS = 600

#: 「JS 켜라」 안내가 본문 자리를 차지한 페이지 — 동적으로 넘어가야 한다는 신호.
JS_REQUIRED_MARKERS = (
    "enable javascript",
    "please enable js",
    "javascript is required",
    "자바스크립트를 활성화",
)

#: 로그인·유료 장벽. **동적으로 넘어가도 소용없다** — 렌더 없이 즉시 실패한다.
PAYWALL_MARKERS = (
    "sign in to continue",
    "subscribe to read",
    "create a free account to",
    "로그인 후 이용",
    "구독을 해야",
)

# 실패 사유 코드 — queue.error 한 줄에 [단계:코드] 로 남는다.
CONTENT_FETCH_FAILED = "CONTENT_FETCH_FAILED"
CONTENT_EXTRACT_FAILED = "CONTENT_EXTRACT_FAILED"
DYNAMIC_RENDER_FAILED = "DYNAMIC_RENDER_FAILED"
PAYWALL_OR_AUTH_REQUIRED = "PAYWALL_OR_AUTH_REQUIRED"
FETCH_TIMEOUT = "FETCH_TIMEOUT"


class FetchError(Exception):
    """가져오기 실패 — queue.failed + error 한 줄로 끝난다.

    웹 3단계는 `stage`(static/dynamic)·`code` 를 실어 **어느 단계에서 왜** 실패했는지
    메시지에 남긴다. youtube 경로는 종전대로 사유 한 줄만 쓴다.
    """

    def __init__(self, message: str, *, stage: str | None = None, code: str | None = None) -> None:
        if stage and code:
            message = f"[{stage}:{code}] {message}"
        super().__init__(message)
        self.stage = stage
        self.code = code


@dataclass(frozen=True)
class FetchedSource:
    """AI 초안 프롬프트에 들어가는 원료."""

    text: str                       # 자막 전문 또는 크롤링 본문
    title: str | None = None        # youtube 만
    channel: str | None = None      # youtube 만
    duration: str | None = None     # youtube 만 — M:SS / H:MM:SS
    published_on: str | None = None # youtube 만 — YYYY-MM-DD
    youtube_id: str | None = None   # youtube 만


_YT_ID_PATTERNS = (
    re.compile(r"(?:v=|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})"),
    re.compile(r"youtu\.be/([A-Za-z0-9_-]{11})"),
)


def youtube_id_of(url: str) -> str:
    for pattern in _YT_ID_PATTERNS:
        m = pattern.search(url)
        if m:
            return m.group(1)
    raise ValidationError(f"유튜브 영상 id 를 URL 에서 못 찾음: {url}")


def _format_duration(seconds: int) -> str:
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def _fetch_transcript_sync(video_id: str) -> str:
    """자막 전문 — 한국어 우선, 없으면 영어. sync 라이브러리라 스레드에서 부른다."""
    from youtube_transcript_api import YouTubeTranscriptApi

    fetched = YouTubeTranscriptApi().fetch(video_id, languages=("ko", "en"))
    return " ".join(snippet.text.strip() for snippet in fetched if snippet.text.strip())


async def _fetch_youtube_meta(client: httpx.AsyncClient, video_id: str) -> dict:
    """제목·채널·길이·게시일 — watch 페이지의 ytInitialPlayerResponse 에서 긁는다.

    파싱이 깨지면 oEmbed 로 제목·채널만 채운다 — 길이·게시일은 비워 두고
    게이트 1 에서 사람이 채운다. 메타 부재는 실패가 아니다(자막이 원료다).
    """
    meta: dict = {}
    try:
        res = await client.get(
            f"https://www.youtube.com/watch?v={video_id}", follow_redirects=True
        )
        if res.status_code == 200:
            html = res.text
            m = re.search(r'"videoDetails":\s*{', html)
            if m:
                # videoDetails 객체를 중괄호 짝으로 잘라 json 으로 읽는다
                start = html.index("{", m.start())
                depth, end = 0, start
                for i in range(start, min(start + 200_000, len(html))):
                    if html[i] == "{":
                        depth += 1
                    elif html[i] == "}":
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                details = json.loads(html[start:end])
                meta["title"] = details.get("title")
                meta["channel"] = details.get("author")
                if details.get("lengthSeconds"):
                    meta["duration"] = _format_duration(int(details["lengthSeconds"]))
            pub = re.search(r'"publishDate":\s*"(\d{4}-\d{2}-\d{2})', html)
            if pub:
                meta["published_on"] = pub.group(1)
    except Exception:
        meta = {}

    if not meta.get("title"):
        try:
            res = await client.get(
                "https://www.youtube.com/oembed",
                params={"url": f"https://youtu.be/{video_id}", "format": "json"},
            )
            if res.status_code == 200:
                data = res.json()
                meta["title"] = data.get("title")
                meta["channel"] = data.get("author_name")
        except Exception:
            pass
    return meta


async def _fetch_youtube(url: str) -> FetchedSource:
    video_id = youtube_id_of(url)
    try:
        transcript = await asyncio.to_thread(_fetch_transcript_sync, video_id)
    except Exception as exc:  # 자막 없음·비공개·차단 전부 — 사유 한 줄로 접는다
        raise FetchError(f"자막을 못 가져옴: {type(exc).__name__}") from exc
    if not transcript:
        raise FetchError("자막이 비어 있음")

    async with httpx.AsyncClient(timeout=20) as client:
        meta = await _fetch_youtube_meta(client, video_id)
    return FetchedSource(
        text=transcript,
        title=meta.get("title"),
        channel=meta.get("channel"),
        duration=meta.get("duration"),
        published_on=meta.get("published_on"),
        youtube_id=video_id,
    )


def _extract_body(html: str, url: str) -> str:
    """trafilatura 본문 추출 — 실패는 빈 문자열. 판정(분량·마커)은 호출자가 한다."""
    import trafilatura

    body = trafilatura.extract(html, url=url, include_links=False)
    return (body or "").strip()


def _check_paywall(body: str, html: str, stage: str) -> None:
    """페이월·로그인 장벽이면 즉시 실패 — **동적으로 올라가지 않는다**(레거시 규칙).

    레거시처럼 분량 미달과 함께일 때만 페이월로 본다 — 본문이 충분한데 하단에
    구독 안내가 붙은 정상 글을 오탐으로 떨구지 않기 위해서다.
    """
    if len(body) >= MIN_CONTENT_LENGTH:
        return
    lowered = (body or html).lower()
    if any(m in lowered for m in PAYWALL_MARKERS):
        raise FetchError(
            "로그인/유료 안내가 본문을 대체했다 — 렌더해도 소용없다",
            stage=stage,
            code=PAYWALL_OR_AUTH_REQUIRED,
        )


async def _render_page(url: str) -> str:
    """chromium headless 렌더 — 다운로드·팝업 차단, 시간·스크롤 제한(레거시 값).

    `playwright` 는 **함수 안에서** import 한다 — 브라우저가 없는 환경(테스트·CI)에서
    모듈을 읽는 것만으로 실패하면 안 된다.
    """
    from playwright.async_api import async_playwright

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            try:
                context = await browser.new_context(
                    accept_downloads=False, user_agent=USER_AGENT
                )
                page = await context.new_page()
                context.on("page", lambda popup: asyncio.ensure_future(popup.close()))
                await page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                try:
                    await page.wait_for_load_state(
                        "networkidle", timeout=NETWORKIDLE_TIMEOUT_MS
                    )
                except Exception:  # noqa: BLE001 — networkidle 미도달은 치명적이지 않다
                    pass
                # 무한 스크롤 페이지에서 본문이 뒤늦게 붙는다. 횟수를 제한한다 —
                # 끝없이 내리면 잡이 안 끝난다.
                for _ in range(MAX_SCROLLS):
                    await page.mouse.wheel(0, 20_000)
                    await page.wait_for_timeout(SCROLL_WAIT_MS)
                return await page.content()
            finally:
                await browser.close()
    except Exception as exc:  # noqa: BLE001 — 렌더 실패는 코드로 남긴다
        raise FetchError(
            f"브라우저 렌더링 실패/timeout: {type(exc).__name__}",
            stage="dynamic",
            code=DYNAMIC_RENDER_FAILED,
        ) from exc


async def _fetch_page(url: str) -> FetchedSource:
    """docs·article·blog — 정적(httpx+trafilatura) → 동적(chromium) → 실패.

    동적 전환은 **좁게** 건다: JS 마커 또는 정적 추출 본문 500자 미만일 때만.
    403·페이월·timeout 은 렌더해도 결과가 같다 — chromium 을 띄우지 않고 실패한다.
    """
    # --- 1단계: 정적 ---
    try:
        async with httpx.AsyncClient(
            timeout=TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            res = await client.get(url)
    except httpx.TimeoutException as exc:
        raise FetchError(
            "정적 수집 timeout", stage="static", code=FETCH_TIMEOUT
        ) from exc
    except httpx.HTTPError as exc:
        raise FetchError(
            f"요청 실패: {type(exc).__name__}", stage="static", code=CONTENT_FETCH_FAILED
        ) from exc
    if res.status_code != 200:
        # 403(봇 차단·Cloudflare 챌린지) 포함 — 우회하지 않는다(발주 결정)
        raise FetchError(
            f"본문을 못 가져옴: HTTP {res.status_code}",
            stage="static",
            code=CONTENT_FETCH_FAILED,
        )

    html = res.text
    body = _extract_body(html, url)
    _check_paywall(body, html, "static")

    js_marker = next(
        (m for m in JS_REQUIRED_MARKERS if m in html.lower()), None
    )
    if len(body) >= MIN_CONTENT_LENGTH and not js_marker:
        return FetchedSource(text=body[:MAX_CONTENT_LENGTH])

    # --- 2단계: 동적 — html 페이지가 아니면 렌더해도 소용없다 ---
    content_type = res.headers.get("content-type", "")
    if content_type and "html" not in content_type.lower():
        raise FetchError(
            f"본문 추출 실패 — html 이 아닌 content-type: {content_type}",
            stage="static",
            code=CONTENT_EXTRACT_FAILED,
        )
    reason = (
        f"JS 마커 {js_marker!r}" if js_marker else f"정적 추출 {len(body)}자 < {MIN_CONTENT_LENGTH}"
    )
    logger.info("동적 전환: %s — %s", url, reason)

    rendered = await _render_page(url)
    body = _extract_body(rendered, url)
    _check_paywall(body, rendered, "dynamic")
    if len(body) < MIN_CONTENT_LENGTH:
        raise FetchError(
            f"동적 렌더링 뒤에도 본문 분량 미달({len(body)}자) — 목록/빈 페이지 가능성",
            stage="dynamic",
            code=CONTENT_EXTRACT_FAILED,
        )
    logger.info("동적 렌더 성공: %s — 본문 %d자", url, len(body))
    return FetchedSource(text=body[:MAX_CONTENT_LENGTH])


async def fetch_source(kind: str, url: str) -> FetchedSource:
    """종류별 가져오기 — 흐름은 하나, 방법만 다르다(케이스 1)."""
    if kind == "youtube":
        return await _fetch_youtube(url)
    return await _fetch_page(url)
