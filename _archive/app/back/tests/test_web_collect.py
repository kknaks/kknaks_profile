"""웹 본문 수집 — 정적 → 동적 → 최종 실패 (KDEV-BL-007 케이스 3).

`ax-graph` AXKG-SPEC-012 Web Adapter 이식본. 여기서 고정하는 것은 넷이다.

    1. UI(네비·푸터·스크립트)는 본문이 아니다 — 지우고 남는 것이 글이다
    2. 정적이 분량 미달이면 **동적으로 올라간다**
    3. 올라가도 소용없는 실패(paywall·크기·timeout)는 **올라가지 않는다**
    4. 동적 뒤에도 미달이면 **최종 실패다** — 빈 본문으로 요약을 부르지 않는다

네트워크도 브라우저도 쓰지 않는다. fetcher·renderer 를 주입해 검사한다.
"""

from __future__ import annotations

import pytest

from service.knowledge_capture.web import (
    CONTENT_EXTRACT_FAILED,
    DYNAMIC_RENDER_REQUIRED,
    MIN_CONTENT_LENGTH,
    PAYWALL_OR_AUTH_REQUIRED,
    SOURCE_TOO_LARGE,
    UNSUPPORTED_SOURCE_TYPE,
    FetchedPage,
    RenderedPage,
    WebCollectError,
    collect_static,
    collect_web,
    process_document,
)

URL = "https://blog.example.com/post"

BODY = "본문 문장이다. " * 60  # MIN_CONTENT_LENGTH 를 넉넉히 넘긴다


def _page(body: str = BODY, *, title: str = "글 제목", extra: str = "") -> str:
    return f"""<html>
<head><title>{title}</title><meta property="og:title" content="OG 제목"></head>
<body>
  <nav><a href="/a">메뉴 A</a><a href="/b">메뉴 B</a></nav>
  <header>사이트 헤더</header>
  <script>console.log('추적 스크립트')</script>
  <article><p>{body}</p></article>
  {extra}
  <footer>푸터 저작권</footer>
</body></html>"""


def _fetcher(html: str, *, content_type: str = "text/html; charset=utf-8"):
    async def fetch(url: str) -> FetchedPage:
        return FetchedPage(final_url=url, content_type=content_type, html=html)

    return fetch


def _renderer(html: str):
    calls: list[str] = []

    async def render(url: str) -> RenderedPage:
        calls.append(url)
        return RenderedPage(final_url=url, html=html)

    render.calls = calls  # type: ignore[attr-defined]
    return render


class TestExtraction:
    def test_ui_is_not_content(self):
        material = process_document(_page(), URL, allow_dynamic_fallback=True)
        assert "본문 문장이다" in material.content
        for chrome in ("메뉴 A", "사이트 헤더", "추적 스크립트", "푸터 저작권"):
            assert chrome not in material.content

    def test_og_title_wins_over_the_title_tag(self):
        """`<title>` 에는 사이트명이 붙는다. `og:title` 이 글 제목이다."""
        assert process_document(_page(), URL, allow_dynamic_fallback=True).title == "OG 제목"

    def test_repeated_lines_collapse(self):
        """`더보기` 류가 수십 번 반복되면 요약 입력의 절반이 그 줄이 된다."""
        extra = "".join("<p>더보기</p>" for _ in range(30))
        content = process_document(
            _page(extra=extra), URL, allow_dynamic_fallback=True
        ).content
        assert content.count("더보기") == 1


class TestEscalation:
    async def test_static_is_enough_for_a_plain_article(self):
        render = _renderer(_page())
        material = await collect_web(URL, html_fetch=_fetcher(_page()), render=render)

        assert "본문 문장이다" in material.content
        assert render.calls == []  # 브라우저를 띄우지 않았다

    async def test_short_static_escalates_to_the_browser(self):
        """JS 로 그리는 페이지 — 정적 HTML 에는 껍데기만 있다."""
        shell = "<html><head><title>x</title></head><body><div id='root'></div></body></html>"
        render = _renderer(_page())

        material = await collect_web(URL, html_fetch=_fetcher(shell), render=render)

        assert render.calls == [URL]
        assert "본문 문장이다" in material.content

    async def test_javascript_notice_escalates(self):
        notice = (
            "<html><head><title>x</title></head><body>"
            "<p>Please enable JavaScript to view this site.</p>"
            "<a href='/x'>홈</a></body></html>"
        )
        render = _renderer(_page())
        await collect_web(URL, html_fetch=_fetcher(notice), render=render)
        assert render.calls == [URL]

    async def test_paywall_does_not_escalate(self):
        """브라우저를 띄워도 로그인은 안 된다 — chromium 을 띄우는 비용만 든다."""
        wall = (
            "<html><head><title>x</title></head><body>"
            "<p>Subscribe to read the full story</p></body></html>"
        )
        render = _renderer(_page())

        with pytest.raises(WebCollectError) as exc:
            await collect_web(URL, html_fetch=_fetcher(wall), render=render)

        assert exc.value.code == PAYWALL_OR_AUTH_REQUIRED
        assert render.calls == []

    async def test_size_limit_does_not_escalate(self):
        async def fetch(url: str) -> FetchedPage:
            raise WebCollectError(SOURCE_TOO_LARGE, "크기 상한 초과")

        render = _renderer(_page())
        with pytest.raises(WebCollectError) as exc:
            await collect_web(URL, html_fetch=fetch, render=render)

        assert exc.value.code == SOURCE_TOO_LARGE
        assert render.calls == []

    async def test_still_short_after_rendering_is_the_final_failure(self):
        """빈 본문으로 요약을 부르지 않는다 — 항목이 실패로 남는 편이 낫다."""
        shell = "<html><head><title>x</title></head><body><div id='root'></div></body></html>"

        with pytest.raises(WebCollectError) as exc:
            await collect_web(URL, html_fetch=_fetcher(shell), render=_renderer(shell))

        assert exc.value.code == CONTENT_EXTRACT_FAILED
        assert "동적" in exc.value.message


class TestStaticGuards:
    async def test_non_html_is_refused(self):
        with pytest.raises(WebCollectError) as exc:
            await collect_static(URL, html_fetch=_fetcher("x", content_type="image/png"))
        assert exc.value.code == UNSUPPORTED_SOURCE_TYPE

    def test_the_threshold_is_the_documented_one(self):
        """상수를 테스트가 다시 적지 않는다 — 값이 바뀌면 같이 움직여야 한다."""
        # 링크 텍스트(`링크` + 줄바꿈)도 본문에 들어가므로 그만큼 여유를 둔다.
        short = "가" * (MIN_CONTENT_LENGTH - 5)
        with pytest.raises(WebCollectError) as exc:
            process_document(
                f"<html><body><p>{short}</p><a href='/x'>링크</a></body></html>",
                URL,
                allow_dynamic_fallback=True,
            )
        assert exc.value.code == CONTENT_EXTRACT_FAILED

        ok = "가" * MIN_CONTENT_LENGTH
        material = process_document(
            f"<html><body><p>{ok}</p></body></html>", URL, allow_dynamic_fallback=True
        )
        assert len(material.content) == MIN_CONTENT_LENGTH


class TestRouting:
    async def test_blog_urls_go_through_the_new_path(self, monkeypatch):
        """`fetch_source` 가 글 URL 을 이 경로로 보낸다 — 종전 정규식 경로가 아니다."""
        from service.knowledge_capture import source as source_mod

        called: list[str] = []

        async def fake(url, **kwargs):
            called.append(url)
            return process_document(_page(), url, allow_dynamic_fallback=True)

        monkeypatch.setattr("service.knowledge_capture.web.collect_web", fake)
        material = await source_mod.fetch_source(URL)

        assert called == [URL]
        assert material.source_type == "blog"
