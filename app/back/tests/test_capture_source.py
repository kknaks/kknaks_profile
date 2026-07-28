from __future__ import annotations

import httpx
import pytest

from service.knowledge_capture import source
from service.knowledge_capture.source import SourceFetchError, fetch_source, validate_public_url, find_urls


@pytest.mark.asyncio
async def test_private_url_rejected():
    with pytest.raises(SourceFetchError, match="non-global"):
        await validate_public_url("http://127.0.0.1/private")


@pytest.mark.asyncio
async def test_html_fetch_is_bounded_and_readable(monkeypatch):
    async def allow(_url):
        return None

    monkeypatch.setattr(source, "validate_public_url", allow)
    transport = httpx.MockTransport(lambda request: httpx.Response(
        200,
        headers={"content-type": "text/html; charset=utf-8"},
        text="<html><title>Example</title><body>" + ("useful text " * 20) + "</body></html>",
    ))
    material = await fetch_source("https://example.com/post", transport=transport)
    assert material.source_type == "blog"
    assert material.title == "Example"
    assert "useful text" in material.content
    assert material.accessed_at


@pytest.mark.asyncio
async def test_redirect_target_is_revalidated(monkeypatch):
    seen = []

    async def record(url):
        seen.append(url)

    monkeypatch.setattr(source, "validate_public_url", record)

    def handler(request):
        if request.url.path == "/start":
            return httpx.Response(302, headers={"location": "/final"})
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text="<title>Final</title><body>" + ("content " * 30) + "</body>",
        )

    await fetch_source("https://example.com/start", transport=httpx.MockTransport(handler))
    assert seen == ["https://example.com/start", "https://example.com/final"]


@pytest.mark.asyncio
async def test_oversized_source_rejected(monkeypatch):
    async def allow(_url):
        return None

    monkeypatch.setattr(source, "validate_public_url", allow)
    transport = httpx.MockTransport(lambda request: httpx.Response(
        200,
        headers={"content-type": "text/plain"},
        content=b"x" * 101,
    ))
    with pytest.raises(SourceFetchError, match="size limit"):
        await fetch_source("https://example.com/large", max_bytes=100, transport=transport)


class TestSlackLinkFormatting:  # noqa: E301
    """Slack 은 링크를 `<url|표시텍스트>` 로 감싸 보낸다 (운영에서 실제로 터진 버그)."""

    def test_pipe_display_text_is_stripped(self):
        text = "<https://www.youtube.com/watch?v=ZVuHZ2Fjkl4|youtube.com/watch?v=ZVuHZ2Fjkl4>"
        assert find_urls(text) == ["https://www.youtube.com/watch?v=ZVuHZ2Fjkl4"]

    def test_youtube_is_detected_after_stripping(self):
        """이걸 놓치면 유튜브가 `blog` 로 판정돼 파이프라인 정의를 못 찾는다."""
        from service.pipeline import detect_source_kind, normalize_url

        url = find_urls("<https://www.youtube.com/watch?v=ZVuHZ2Fjkl4|보기>")[0]
        assert detect_source_kind(url) == "youtube"
        assert normalize_url(url) == "youtube:ZVuHZ2Fjkl4"

    def test_plain_url_unaffected(self):
        assert find_urls("보라 https://youtu.be/abc12345678 여기") == [
            "https://youtu.be/abc12345678"
        ]
