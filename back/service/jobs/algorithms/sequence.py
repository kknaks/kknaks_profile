"""NeetCode 150 시퀀스 — neetcode-gh `.problemSiteData.json` source.

옵션 B (planning §4.8 / 사용자 결정) — 외부 JSON 자동 동기. 하드코드 X.
- 일자 잡 시작 시 fetch (cache 박혀있으면 hit)
- 배열 순서 = 학습 순서 (Arrays & Hashing → Two Pointers → ... → Bit Manipulation)
- 다음 풀 항목 index = `count_existing_algorithms(persona_dir)` (옵션 γ — 시드 정합 자동)
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx

from .fetch import Cache, DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)

PROBLEM_SITE_DATA_URL = (
    "https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json"
)
CACHE_KEY = "algo:nc150:list"


@dataclass
class SequenceItem:
    """NeetCode 150 의 한 항목 — sequence.py 가 노출하는 단위."""

    slug: str
    number: int
    title: str
    pattern: str
    difficulty: str

    @classmethod
    def from_raw(cls, raw: dict) -> "SequenceItem":
        """`.problemSiteData.json` entry → SequenceItem.

        raw 의 `link` (e.g. 'contains-duplicate/') 끝의 `/` 제거.
        `code` (e.g. '0217-contains-duplicate') 첫 토큰 = LeetCode number.
        """
        slug = (raw.get("link") or "").rstrip("/")
        code = raw.get("code", "")
        number_str = code.split("-", 1)[0] if "-" in code else ""
        try:
            number = int(number_str)
        except ValueError:
            number = 0
        return cls(
            slug=slug,
            number=number,
            title=raw.get("problem", ""),
            pattern=raw.get("pattern", ""),
            difficulty=(raw.get("difficulty") or "").lower(),
        )


async def fetch_neetcode_150(
    *,
    cache: Cache | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[SequenceItem]:
    """neetcode-gh `.problemSiteData.json` → SequenceItem 150 (배열 순서 = 학습 순서).

    캐시 hit 시 외부 fetch X. 미스 시 fetch + neetcode150=True 필터 + cache set.

    Raises:
        httpx.HTTPError — 네트워크·HTTP 실패
        json.JSONDecodeError — 응답이 JSON 아님
    """
    if cache is not None:
        hit = cache.get(CACHE_KEY)
        if hit is not None:
            logger.debug("cache hit nc150")
            data = json.loads(hit)
            return [SequenceItem(**d) for d in data]

    own_client = client is None
    c = client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
    try:
        resp = await c.get(PROBLEM_SITE_DATA_URL, headers={"User-Agent": "kknaks-profile-fetch"})
        resp.raise_for_status()
        all_problems = resp.json()
    finally:
        if own_client:
            await c.aclose()

    items = [SequenceItem.from_raw(p) for p in all_problems if p.get("neetcode150")]
    logger.info("fetched NeetCode 150: %d items", len(items))

    if cache is not None:
        cache.set(CACHE_KEY, json.dumps([asdict(it) for it in items]))

    return items


def count_existing_algorithms(persona_dir: Path) -> int:
    """persona/algorithms/A-*.md 파일 수 (옵션 γ — 다음 next_index 결정).

    잡이 박을 다음 항목 = `NEETCODE_150[count_existing_algorithms(persona_dir)]`.
    수동 시드 N 개 + 자동 잡 누적이 자연스럽게 이어짐.
    """
    algos = persona_dir / "algorithms"
    if not algos.is_dir():
        return 0
    return sum(1 for _ in algos.glob("A-*.md"))


def get_next(items: list[SequenceItem], idx: int) -> SequenceItem | None:
    """idx 위치 항목 — 범위 외 (음수·150+) → None.

    잡 호출자: idx = count_existing_algorithms(persona_dir).
    """
    if 0 <= idx < len(items):
        return items[idx]
    return None
