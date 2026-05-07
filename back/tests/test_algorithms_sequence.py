"""TDD — algorithms sequence 모듈 (NeetCode 150 source · count · next)."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from service.jobs.algorithms.fetch import DictCache
from service.jobs.algorithms.sequence import (
    CACHE_KEY,
    SequenceItem,
    count_existing_algorithms,
    fetch_neetcode_150,
    get_next,
)


# ---------- helpers ----------


def _mock_client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=5)


SAMPLE_PROBLEMS = [
    {
        "neetcode150": True,
        "blind75": True,
        "problem": "Contains Duplicate",
        "pattern": "Arrays & Hashing",
        "link": "contains-duplicate/",
        "code": "0217-contains-duplicate",
        "difficulty": "Easy",
    },
    {
        "neetcode150": True,
        "blind75": True,
        "problem": "Two Sum",
        "pattern": "Arrays & Hashing",
        "link": "two-sum/",
        "code": "0001-two-sum",
        "difficulty": "Easy",
    },
    {
        # NOT neetcode150 — should be filtered out
        "neetcode150": False,
        "problem": "Some Other Problem",
        "pattern": "Other",
        "link": "other/",
        "code": "9999-other",
        "difficulty": "Hard",
    },
    {
        "neetcode150": True,
        "problem": "House Robber",
        "pattern": "1-D Dynamic Programming",
        "link": "house-robber/",
        "code": "0198-house-robber",
        "difficulty": "Medium",
    },
]


# ---------- SequenceItem.from_raw ----------


class TestFromRaw:
    def test_basic(self):
        it = SequenceItem.from_raw(SAMPLE_PROBLEMS[0])
        assert it.slug == "contains-duplicate"  # trailing / stripped
        assert it.number == 217
        assert it.title == "Contains Duplicate"
        assert it.pattern == "Arrays & Hashing"
        assert it.difficulty == "easy"  # lowercased

    def test_two_sum(self):
        it = SequenceItem.from_raw(SAMPLE_PROBLEMS[1])
        assert it.slug == "two-sum"
        assert it.number == 1
        assert it.difficulty == "easy"

    def test_missing_code_falls_back_to_zero(self):
        raw = {"link": "x/", "problem": "X", "pattern": "Y", "difficulty": "Easy"}
        it = SequenceItem.from_raw(raw)
        assert it.number == 0

    def test_malformed_code(self):
        raw = {"link": "x/", "code": "not-a-number-prefix", "difficulty": "Easy"}
        it = SequenceItem.from_raw(raw)
        # 'not' parse 시 ValueError → 0
        assert it.number == 0


# ---------- fetch_neetcode_150 ----------


class TestFetchNeetCode150:
    @pytest.mark.asyncio
    async def test_filters_neetcode150_only(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=SAMPLE_PROBLEMS)

        async with _mock_client(handler) as client:
            items = await fetch_neetcode_150(client=client)
        # SAMPLE 의 neetcode150=False 1개 제외 → 3개
        assert len(items) == 3
        assert [it.slug for it in items] == ["contains-duplicate", "two-sum", "house-robber"]

    @pytest.mark.asyncio
    async def test_preserves_order(self):
        # 배열 순서 = 학습 순서 — fetch 가 reorder 하지 않음
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=SAMPLE_PROBLEMS)

        async with _mock_client(handler) as client:
            items = await fetch_neetcode_150(client=client)
        assert items[0].slug == "contains-duplicate"
        assert items[2].slug == "house-robber"

    @pytest.mark.asyncio
    async def test_cache_hit_skips_http(self):
        cache = DictCache()
        cached = [
            {
                "slug": "x",
                "number": 1,
                "title": "X",
                "pattern": "P",
                "difficulty": "easy",
            }
        ]
        cache.set(CACHE_KEY, json.dumps(cached))

        call_count = 0

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return httpx.Response(200, json=SAMPLE_PROBLEMS)

        async with _mock_client(handler) as client:
            items = await fetch_neetcode_150(cache=cache, client=client)
        assert len(items) == 1
        assert items[0].slug == "x"
        assert call_count == 0

    @pytest.mark.asyncio
    async def test_cache_miss_then_set(self):
        cache = DictCache()
        call_count = 0

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return httpx.Response(200, json=SAMPLE_PROBLEMS)

        async with _mock_client(handler) as client:
            await fetch_neetcode_150(cache=cache, client=client)
            await fetch_neetcode_150(cache=cache, client=client)
        assert call_count == 1  # 두 번째는 cache hit

    @pytest.mark.asyncio
    async def test_raises_on_5xx(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(503, text="busy")

        async with _mock_client(handler) as client:
            with pytest.raises(httpx.HTTPStatusError):
                await fetch_neetcode_150(client=client)


# ---------- count_existing_algorithms ----------


class TestCountExisting:
    def test_no_dir(self, tmp_path: Path):
        assert count_existing_algorithms(tmp_path) == 0

    def test_empty_dir(self, tmp_path: Path):
        (tmp_path / "algorithms").mkdir()
        assert count_existing_algorithms(tmp_path) == 0

    def test_counts_a_files(self, tmp_path: Path):
        d = tmp_path / "algorithms"
        d.mkdir()
        (d / "A-001-x.md").write_text("---\n---\n")
        (d / "A-002-y.md").write_text("---\n---\n")
        (d / "A-003-z.md").write_text("---\n---\n")
        assert count_existing_algorithms(tmp_path) == 3

    def test_ignores_non_a_files(self, tmp_path: Path):
        d = tmp_path / "algorithms"
        d.mkdir()
        (d / "A-001-x.md").write_text("")
        (d / "_meta.yaml").write_text("")
        (d / "README.md").write_text("")
        (d / "B-001.md").write_text("")
        assert count_existing_algorithms(tmp_path) == 1


# ---------- get_next ----------


class TestGetNext:
    def _items(self) -> list[SequenceItem]:
        return [
            SequenceItem("a", 1, "A", "P", "easy"),
            SequenceItem("b", 2, "B", "P", "easy"),
            SequenceItem("c", 3, "C", "P", "medium"),
        ]

    def test_in_range(self):
        items = self._items()
        assert get_next(items, 0).slug == "a"
        assert get_next(items, 2).slug == "c"

    def test_out_of_range(self):
        items = self._items()
        assert get_next(items, 3) is None
        assert get_next(items, 999) is None

    def test_negative(self):
        items = self._items()
        assert get_next(items, -1) is None

    def test_empty_list(self):
        assert get_next([], 0) is None
