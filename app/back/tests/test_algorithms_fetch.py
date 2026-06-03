"""TDD — algorithms fetch 모듈 (spec-07 §7.1 a, b)."""

from __future__ import annotations

import json

import httpx
import pytest

from service.jobs.algorithms.fetch import (
    DictCache,
    LeetCodeError,
    fetch_leetcode,
    fetch_neetcode_gh,
)


# ---------- helpers ----------


def _mock_client(handler) -> httpx.AsyncClient:
    transport = httpx.MockTransport(handler)
    return httpx.AsyncClient(transport=transport, timeout=5)


def _lc_response(question: dict | None) -> httpx.Response:
    return httpx.Response(200, json={"data": {"question": question}})


def _lc_error_response() -> httpx.Response:
    return httpx.Response(200, json={"errors": [{"message": "rate limited"}]})


SAMPLE_QUESTION = {
    "questionId": "1",
    "questionFrontendId": "1",
    "title": "Two Sum",
    "titleSlug": "two-sum",
    "content": "<p>Given an array...</p>",
    "difficulty": "Easy",
    "exampleTestcases": "[2,7,11,15]\n9\n[3,2,4]\n6",
    "hints": ["use hash"],
    "topicTags": [{"name": "Array", "slug": "array"}, {"name": "Hash Table", "slug": "hash-table"}],
    "sampleTestCase": "[2,7,11,15]\n9",
    "metaData": '{"name": "twoSum", "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}], "return": {"type": "integer[]"}}',
}


# ---------- fetch_leetcode ----------


class TestFetchLeetCode:
    @pytest.mark.asyncio
    async def test_returns_question_dict(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            assert req.url.path == "/graphql/"
            body = json.loads(req.content)
            assert body["variables"]["titleSlug"] == "two-sum"
            return _lc_response(SAMPLE_QUESTION)

        async with _mock_client(handler) as client:
            q = await fetch_leetcode("two-sum", client=client)
        assert q["questionId"] == "1"
        assert q["title"] == "Two Sum"
        assert "<p>" in q["content"]  # raw HTML 그대로
        assert q["metaData"].startswith("{")  # JSON string 그대로

    @pytest.mark.asyncio
    async def test_raises_on_question_null(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return _lc_response(None)

        async with _mock_client(handler) as client:
            with pytest.raises(LeetCodeError, match="not found"):
                await fetch_leetcode("nonexistent", client=client)

    @pytest.mark.asyncio
    async def test_raises_on_graphql_errors(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return _lc_error_response()

        async with _mock_client(handler) as client:
            with pytest.raises(LeetCodeError, match="GraphQL errors"):
                await fetch_leetcode("two-sum", client=client)

    @pytest.mark.asyncio
    async def test_raises_on_5xx(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="server down")

        async with _mock_client(handler) as client:
            with pytest.raises(httpx.HTTPStatusError):
                await fetch_leetcode("two-sum", client=client)

    @pytest.mark.asyncio
    async def test_cache_hit_skips_http(self):
        cache = DictCache()
        cache.set("algo:lc:two-sum", json.dumps(SAMPLE_QUESTION))

        call_count = 0

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return _lc_response(SAMPLE_QUESTION)

        async with _mock_client(handler) as client:
            q = await fetch_leetcode("two-sum", cache=cache, client=client)
        assert q["title"] == "Two Sum"
        assert call_count == 0  # 캐시 hit 으로 HTTP 안 침

    @pytest.mark.asyncio
    async def test_cache_miss_then_set(self):
        cache = DictCache()
        call_count = 0

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return _lc_response(SAMPLE_QUESTION)

        async with _mock_client(handler) as client:
            await fetch_leetcode("two-sum", cache=cache, client=client)
            # 두 번째 호출은 캐시 hit
            await fetch_leetcode("two-sum", cache=cache, client=client)
        assert call_count == 1


# ---------- fetch_neetcode_gh ----------


SAMPLE_CODE = """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevMap = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
"""


class TestFetchNeetCodeGh:
    @pytest.mark.asyncio
    async def test_returns_code_string(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            assert req.url.path.endswith("/python/0001-two-sum.py")
            return httpx.Response(200, text=SAMPLE_CODE)

        async with _mock_client(handler) as client:
            code = await fetch_neetcode_gh("two-sum", 1, client=client)
        assert code is not None
        assert "class Solution" in code

    @pytest.mark.asyncio
    async def test_returns_none_on_404(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(404, text="not found")

        async with _mock_client(handler) as client:
            code = await fetch_neetcode_gh("nonexistent", 9999, client=client)
        assert code is None

    @pytest.mark.asyncio
    async def test_raises_on_5xx(self):
        async def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(503, text="busy")

        async with _mock_client(handler) as client:
            with pytest.raises(httpx.HTTPStatusError):
                await fetch_neetcode_gh("two-sum", 1, client=client)

    @pytest.mark.asyncio
    async def test_cache_hit(self):
        cache = DictCache()
        cache.set("algo:ng:0001-two-sum", SAMPLE_CODE)
        call_count = 0

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return httpx.Response(200, text="ANOTHER")

        async with _mock_client(handler) as client:
            code = await fetch_neetcode_gh("two-sum", 1, cache=cache, client=client)
        assert code == SAMPLE_CODE
        assert call_count == 0

    @pytest.mark.asyncio
    async def test_url_pattern_zero_padded(self):
        # 198 → "0198-house-robber"
        captured_url = ""

        async def handler(req: httpx.Request) -> httpx.Response:
            nonlocal captured_url
            captured_url = str(req.url)
            return httpx.Response(200, text=SAMPLE_CODE)

        async with _mock_client(handler) as client:
            await fetch_neetcode_gh("house-robber", 198, client=client)
        assert "/python/0198-house-robber.py" in captured_url
