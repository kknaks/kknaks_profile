"""URL 정규화와 입력 종류 판별 (KDEV-WORK-014 Phase 2 / KDEV-SPEC-007).

정규화의 목적은 하나다 — **같은 자료가 두 번 큐에 쌓이지 않게** 하는 것.
그래서 폭이 곧 정확도다.

- 너무 좁으면(원문 그대로 비교) `youtu.be/X` 와 `watch?v=X&t=120s` 가 다른 자료가 되어
  같은 영상이 두 번 정리된다.
- 너무 넓으면(쿼리 전부 제거) `blog.com/?p=1` 과 `blog.com/?p=2` 가 같은 글이 되어
  **다른 자료가 조용히 합쳐진다.** 이쪽이 더 위험하다 — 사라진 걸 알아채기 어렵다.

그래서 층을 나눈다.
- **유튜브는 영상 ID 만** 남긴다. ID 가 자료의 정체성 전부이고, 나머지(`t`·`list`·`si`)는
  재생 위치나 유입 경로라 자료를 바꾸지 않는다.
- **그 외는 추적 파라미터만** 떼고 나머지 쿼리는 보존한다. 어떤 쿼리가 식별자인지
  일반적으로 알 수 없으므로, 지우는 쪽이 아니라 남기는 쪽을 기본값으로 둔다.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

#: 유입 경로 추적용 — 자료의 정체성과 무관하다.
TRACKING_PARAMS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "utm_id",
        "fbclid",
        "gclid",
        "igshid",
        "mkt_tok",
        "ref",
        "ref_src",
        "referrer",
        "si",
        "spm",
        "source",
    }
)

YOUTUBE_HOSTS = frozenset(
    {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"}
)

_VIDEO_ID_RE = re.compile(r"[A-Za-z0-9_-]{6,20}")
_DEFAULT_PORTS = {"http": 80, "https": 443}


def youtube_video_id(url: str) -> str | None:
    """유튜브 영상 ID. 유튜브가 아니거나 ID 를 못 찾으면 `None`."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in YOUTUBE_HOSTS:
        return None

    path = parsed.path or ""
    if host == "youtu.be":
        value = path.strip("/").split("/")[0]
    elif path.startswith(("/shorts/", "/embed/", "/live/")):
        parts = [p for p in path.split("/") if p]
        value = parts[1] if len(parts) > 1 else ""
    else:
        value = dict(parse_qsl(parsed.query)).get("v", "")

    return value if _VIDEO_ID_RE.fullmatch(value) else None


def normalize_url(url: str | None) -> str | None:
    """중복 판정용 정규 형태. 판정할 수 없으면 `None` (= 중복 검사 대상 아님).

    `None` 을 돌려주는 편이 틀린 키를 만드는 것보다 낫다 — 정규화에 실패한 URL 끼리
    우연히 같은 키가 되면 서로 다른 자료가 합쳐진다.
    """
    if not url or not url.strip():
        return None

    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None

    video_id = youtube_video_id(url)
    if video_id:
        # 호스트·경로 형태(youtu.be / shorts / watch)가 달라도 같은 영상은 같은 키.
        return f"youtube:{video_id}"

    host = parsed.hostname.lower()
    if host.startswith("www."):
        host = host[4:]
    netloc = host
    if parsed.port and parsed.port != _DEFAULT_PORTS.get(parsed.scheme):
        netloc = f"{host}:{parsed.port}"

    path = parsed.path or "/"
    if len(path) > 1:
        path = path.rstrip("/") or "/"

    kept = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in TRACKING_PARAMS]
    # 파라미터 순서는 자료를 바꾸지 않는다 — 정렬해 같은 키로 모은다.
    query = urlencode(sorted(kept))

    # fragment 는 문서 내 위치라 자료의 정체성이 아니다.
    return urlunparse((parsed.scheme, netloc, path, "", query, ""))


def detect_source_kind(url: str | None) -> str:
    """`source_kind` — 파이프라인 정의를 고르는 키 (SPEC-007 Data Contract).

    URL 이 없으면 `manual` 이다. `commit`·`schedule` 은 URL 에서 판별되지 않고
    해당 잡이 직접 지정한다.
    """
    if not url:
        return "manual"
    if youtube_video_id(url):
        return "youtube"
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return "manual"
    # 논문·PDF 도 "URL 을 받아 본문을 수집해 요약한다" 는 점에서 블로그와 같은 경로를 탄다.
    # 별도 파이프라인이 필요해지면 그때 정의를 추가한다(스키마 변경 불필요 — DEC-011 D2).
    return "blog"
