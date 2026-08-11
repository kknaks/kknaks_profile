"""Safe source detection and bounded HTTP extraction."""

from __future__ import annotations

import asyncio
import html
import ipaddress
import json
import re
import socket
from datetime import datetime, timezone
from io import BytesIO
from dataclasses import asdict, dataclass
from urllib.parse import parse_qs, urljoin, urlparse

import httpx

URL_RE = re.compile(r"https?://[^\s<>()]+")
TAG_RE = re.compile(r"<(?:script|style)[^>]*>.*?</(?:script|style)>|<[^>]+>", re.I | re.S)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


class SourceFetchError(ValueError):
    pass


@dataclass(frozen=True)
class SourceMaterial:
    url: str
    source_type: str
    title: str | None
    content: str
    accessed_at: str

    def to_dict(self) -> dict:
        return asdict(self)


def find_urls(text: str) -> list[str]:
    """본문에서 URL 을 뽑는다.

    Slack 은 링크를 `<https://example.com|example.com>` 으로 감싸 보낸다. `>` 는
    정규식이 거르지만 **`|` 뒤의 표시 텍스트는 URL 에 그대로 붙는다** — 그러면
    `watch?v=ID|youtube.com/...` 이 되어 영상 ID 파싱이 실패하고, 유튜브가
    `blog` 로 판정돼 파이프라인 정의를 못 찾는다(게이트가 안 열린다).

    `|` 는 URL 에서 퍼센트 인코딩돼야 하는 문자라 잘라도 안전하다.
    """
    urls = []
    for match in URL_RE.findall(text or ""):
        urls.append(match.split("|", 1)[0].rstrip(".,;!?"))
    return urls


def detect_source_type(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    path = urlparse(url).path.lower()
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}:
        return "youtube"
    if host in {"doi.org", "arxiv.org"} or path.endswith(".pdf"):
        return "paper"
    return "blog"


async def validate_public_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise SourceFetchError("only absolute HTTP(S) URLs are allowed")
    try:
        addresses = await asyncio.to_thread(
            socket.getaddrinfo, parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)
        )
    except socket.gaierror as exc:
        raise SourceFetchError("source host cannot be resolved") from exc
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise SourceFetchError("source resolves to a private or non-global address")


async def fetch_source(
    url: str,
    *,
    timeout: float = 15,
    max_bytes: int = 10_000_000,
    max_redirects: int = 3,
    transport: httpx.AsyncBaseTransport | None = None,
) -> SourceMaterial:
    if detect_source_type(url) == "youtube":
        return await _fetch_youtube(url)
    if detect_source_type(url) == "blog":
        # 글·문서는 **정적 → 동적 → 최종 실패**를 탄다 (KDEV-BL-007 케이스 3).
        # 아래 경로는 태그를 정규식으로 전부 지워 페이지를 한 덩어리로 만들기 때문에
        # JS 로 그리는 페이지가 조용히 "본문 100자" 로 성공한다. `paper`(PDF)는
        # 스트리밍 추출이라 그대로 아래를 쓴다.
        from .web import collect_web

        return await collect_web(
            url,
            timeout=timeout,
            max_bytes=max_bytes,
            max_redirects=max_redirects,
            transport=transport,
        )
    current = url
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=False,
        transport=transport,
    ) as client:
        for _ in range(max_redirects + 1):
            await validate_public_url(current)
            async with client.stream("GET", current, headers={"User-Agent": "kknaks-capture/1.0"}) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    location = response.headers.get("location")
                    if not location:
                        raise SourceFetchError("redirect without location")
                    current = urljoin(current, location)
                    continue
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                is_pdf = "application/pdf" in content_type and detect_source_type(current) == "paper"
                if "text/" not in content_type and "json" not in content_type and not is_pdf:
                    raise SourceFetchError(f"unsupported content type: {content_type}")
                chunks: list[bytes] = []
                size = 0
                async for chunk in response.aiter_bytes():
                    size += len(chunk)
                    if size > max_bytes:
                        raise SourceFetchError("source exceeds size limit")
                    chunks.append(chunk)
                raw_bytes = b"".join(chunks)
                if is_pdf:
                    text = await asyncio.to_thread(_extract_pdf_text, raw_bytes)
                    if len(text) < 100:
                        raise SourceFetchError("paper PDF has insufficient extractable text")
                    return SourceMaterial(
                        url=current,
                        source_type="paper",
                        title=None,
                        content=text[:200_000],
                        accessed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    )
                raw = raw_bytes.decode(response.encoding or "utf-8", errors="replace")
                title_match = TITLE_RE.search(raw)
                title = html.unescape(TAG_RE.sub(" ", title_match.group(1))).strip() if title_match else None
                text = html.unescape(TAG_RE.sub(" ", raw))
                text = re.sub(r"\s+", " ", text).strip()
                if len(text) < 100:
                    raise SourceFetchError("source has insufficient readable content")
                return SourceMaterial(
                    url=current,
                    source_type=detect_source_type(current),
                    title=title,
                    content=text[:200_000],
                    accessed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                )
    raise SourceFetchError("too many redirects")


def _youtube_id(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host == "youtu.be":
        value = parsed.path.strip("/").split("/")[0]
    elif parsed.path.startswith("/shorts/"):
        value = parsed.path.split("/", 3)[2]
    else:
        value = parse_qs(parsed.query).get("v", [""])[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", value):
        raise SourceFetchError("invalid YouTube URL")
    return value


async def _fetch_youtube(url: str) -> SourceMaterial:
    await validate_public_url(url)
    youtube_id = _youtube_id(url)

    def load() -> tuple[dict, str | None]:
        from service.jobs.content_enrich import extract_metadata, extract_transcript

        return extract_metadata(youtube_id), extract_transcript(youtube_id)

    try:
        metadata, transcript = await asyncio.to_thread(load)
    except Exception as exc:
        raise SourceFetchError("YouTube metadata/transcript fetch failed") from exc
    if not transcript or len(transcript.strip()) < 100:
        raise SourceFetchError("YouTube transcript is unavailable or too short")
    title = str(metadata.get("title") or "").strip() or None
    header = {
        "video_id": youtube_id,
        "channel": metadata.get("channel"),
        "duration_s": metadata.get("duration_s"),
        "upload_date": metadata.get("upload_date"),
    }
    return SourceMaterial(
        url=f"https://www.youtube.com/watch?v={youtube_id}",
        source_type="youtube",
        title=title,
        content=json.dumps(header, ensure_ascii=False) + "\n\n" + transcript[:200_000],
        accessed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def _extract_pdf_text(raw: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(raw))
    return "\n\n".join((page.extract_text() or "").strip() for page in reader.pages).strip()
