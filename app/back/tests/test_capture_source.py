from __future__ import annotations

import httpx
import pytest

from service.knowledge_capture import source
from service.knowledge_capture.source import SourceFetchError, fetch_source, validate_public_url


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
