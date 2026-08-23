"""LeetCode GraphQL + neetcode-gh raw fetch — spec-07 §7.1 (a) source fetch + (b) 캐시.

데이터 가공 X. raw 응답 그대로 반환 — 정규화·HTML 파싱은 후속 단계 (c, d) 책임.

cache 인터페이스: Protocol with `get(key) -> str | None` + `set(key, value: str)`.
- 테스트: dict-like wrapper
- 운영: redis client wrapper (spec-03 §11.4 의 redis broker 와 동일 인스턴스)
- 미지정 (None): 항상 fetch (캐시 없음)
"""

from __future__ import annotations

import json
import logging
from typing import Protocol

import httpx

logger = logging.getLogger(__name__)

LEETCODE_GRAPHQL = "https://leetcode.com/graphql/"
NEETCODE_RAW_BASE = (
    "https://raw.githubusercontent.com/neetcode-gh/leetcode/main/python"
)

# spec-07 §7.1 (a) — 한 호출에 회수할 필드 셋
QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    content
    difficulty
    exampleTestcases
    hints
    topicTags {
      name
      slug
    }
    sampleTestCase
    metaData
  }
}
"""

DEFAULT_TIMEOUT = httpx.Timeout(15.0)


class Cache(Protocol):
    """str → str 캐시. None = 미스."""

    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str) -> None: ...


def _cache_key_lc(slug: str) -> str:
    return f"algo:lc:{slug}"


def _cache_key_ng(slug: str, number: int) -> str:
    return f"algo:ng:{number:04d}-{slug}"


class LeetCodeError(Exception):
    """LeetCode GraphQL 응답이 errors 키 또는 question=null."""


async def fetch_leetcode(
    slug: str,
    *,
    cache: Cache | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict:
    """LeetCode GraphQL POST → raw question dict.

    spec-07 §7.1 (a) — 가공 X. content 는 HTML, metaData 는 JSON 문자열 그대로.

    Returns:
        question dict (questionId·title·content·difficulty·exampleTestcases·metaData·...)

    Raises:
        LeetCodeError — slug 미존재 또는 GraphQL errors
        httpx.HTTPError — 네트워크·HTTP 실패
    """
    if cache is not None:
        hit = cache.get(_cache_key_lc(slug))
        if hit is not None:
            logger.debug("cache hit lc %s", slug)
            return json.loads(hit)

    body = {
        "query": QUESTION_QUERY,
        "variables": {"titleSlug": slug},
        "operationName": "questionData",
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (kknaks-profile-fetch)",
    }

    own_client = client is None
    c = client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
    try:
        resp = await c.post(LEETCODE_GRAPHQL, json=body, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    finally:
        if own_client:
            await c.aclose()

    if "errors" in data:
        raise LeetCodeError(f"GraphQL errors for '{slug}': {data['errors']}")
    question = data.get("data", {}).get("question")
    if question is None:
        raise LeetCodeError(f"slug '{slug}' not found (question=null)")

    if cache is not None:
        cache.set(_cache_key_lc(slug), json.dumps(question, ensure_ascii=False))
    return question


async def fetch_neetcode_gh(
    slug: str,
    number: int,
    *,
    cache: Cache | None = None,
    client: httpx.AsyncClient | None = None,
) -> str | None:
    """neetcode-gh raw python solution fetch.

    URL 패턴: `python/{NNNN}-{slug}.py`. 모든 NeetCode 150 솔루션이
    `class Solution: def methodName(self, ...)` 일관 패턴 (spec-07 §7.1 (a)).

    Returns:
        솔루션 코드 string. 404 (slug 미존재) → None — 호출자가 LLM fallback 결정.

    Raises:
        httpx.HTTPError — 네트워크 오류 (404 제외)
    """
    if cache is not None:
        hit = cache.get(_cache_key_ng(slug, number))
        if hit is not None:
            logger.debug("cache hit ng %s", slug)
            return hit

    url = f"{NEETCODE_RAW_BASE}/{number:04d}-{slug}.py"
    headers = {"User-Agent": "kknaks-profile-fetch"}

    own_client = client is None
    c = client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
    try:
        resp = await c.get(url, headers=headers)
    finally:
        if own_client:
            await c.aclose()

    if resp.status_code == 404:
        logger.warning("neetcode-gh 404 for %s (number=%d)", slug, number)
        return None
    resp.raise_for_status()
    code = resp.text

    if cache is not None:
        cache.set(_cache_key_ng(slug, number), code)
    return code


class DictCache:
    """테스트·로컬용 in-memory 캐시. dict-backed."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._store.get(key)

    def set(self, key: str, value: str) -> None:
        self._store[key] = value
