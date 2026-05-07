"""TDD — algorithms normalize 모듈 (spec-07 §7.1 c)."""

from __future__ import annotations

import pytest

from service.jobs.algorithms.normalize import (
    _extract_core_lines,
    _split_testcases,
    normalize_question,
)


# ---------- _split_testcases ----------


class TestSplitTestcases:
    def test_two_params(self):
        # two-sum: nums + target, 3 cases
        raw = "[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6"
        result = _split_testcases(raw, 2)
        assert result == ["[2,7,11,15]\n9", "[3,2,4]\n6", "[3,3]\n6"]

    def test_one_param(self):
        # contains-duplicate: nums only, 3 cases
        raw = "[1,2,3,1]\n[1,2,3,4]\n[1,1,1,3,3,4,3,2,4,2]"
        result = _split_testcases(raw, 1)
        assert result == ["[1,2,3,1]", "[1,2,3,4]", "[1,1,1,3,3,4,3,2,4,2]"]

    def test_string_params(self):
        # valid-anagram: s + t (with quotes), 2 cases
        raw = '"anagram"\n"nagaram"\n"rat"\n"car"'
        result = _split_testcases(raw, 2)
        assert result == ['"anagram"\n"nagaram"', '"rat"\n"car"']

    def test_partial_chunk_dropped(self):
        # 5 줄 / params_count=2 → 마지막 1 줄 drop (incomplete)
        raw = "a\nb\nc\nd\ne"
        result = _split_testcases(raw, 2)
        assert result == ["a\nb", "c\nd"]

    def test_empty_raw(self):
        assert _split_testcases("", 2) == []

    def test_zero_params_count(self):
        assert _split_testcases("a\nb", 0) == []


# ---------- _extract_core_lines ----------


TWO_SUM_CODE = """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevMap = {}  # val -> index

        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
"""


HOUSE_ROBBER_CODE = """class Solution:
    def rob(self, nums: List[int]) -> int:
        rob1, rob2 = 0, 0

        for n in nums:
            temp = max(n + rob1, rob2)
            rob1 = rob2
            rob2 = temp
        return rob2
"""


class TestExtractCoreLines:
    def test_two_sum_class_body(self):
        lines = _extract_core_lines(TWO_SUM_CODE)
        # signature·class line 제외, 본체만. blank 제외.
        assert any("prevMap = {}" in l for l in lines)
        assert any("for i, n in enumerate(nums):" in l for l in lines)
        assert any("return [prevMap[diff], i]" in l for l in lines)
        assert not any("class Solution" in l for l in lines)
        assert not any("def twoSum" in l for l in lines)

    def test_house_robber_class_body(self):
        lines = _extract_core_lines(HOUSE_ROBBER_CODE)
        assert any("rob1, rob2 = 0, 0" in l for l in lines)
        assert any("return rob2" in l for l in lines)

    def test_no_blank_lines(self):
        lines = _extract_core_lines(TWO_SUM_CODE)
        assert all(l.strip() for l in lines)

    def test_comment_only_lines_dropped(self):
        code = """class Solution:
    def f(self):
        # this is a comment
        x = 1
        return x
"""
        lines = _extract_core_lines(code)
        assert any("x = 1" in l for l in lines)
        # 주석 only 라인 제외
        assert not any(l.strip().startswith("#") for l in lines)

    def test_empty_code(self):
        assert _extract_core_lines("") == []
        assert _extract_core_lines("   \n  ") == []

    def test_syntax_error(self):
        # broken Python — fallback to []
        assert _extract_core_lines("class Solution\n    def f(self) return 1") == []

    def test_no_class_solution_falls_back_to_top_level_def(self):
        code = """def two_sum(nums, target):
    seen = {}
    return seen
"""
        lines = _extract_core_lines(code)
        assert any("seen = {}" in l for l in lines)
        assert any("return seen" in l for l in lines)


# ---------- normalize_question (integration) ----------


SAMPLE_QUESTION = {
    "questionId": "1",
    "questionFrontendId": "1",
    "title": "Two Sum",
    "titleSlug": "two-sum",
    "content": "<p>Given an array...</p><pre>Input: nums = [2,7,11,15]\nOutput: [0,1]</pre>",
    "difficulty": "Easy",
    "exampleTestcases": "[2,7,11,15]\n9\n[3,2,4]\n6",
    "hints": ["use hash"],
    "topicTags": [{"name": "Array", "slug": "array"}, {"name": "Hash Table", "slug": "hash-table"}],
    "metaData": '{"name": "twoSum", "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}], "return": {"type": "integer[]"}}',
}


class TestNormalizeQuestion:
    def test_basic_fields(self):
        n = normalize_question(SAMPLE_QUESTION, TWO_SUM_CODE)
        assert n["slug"] == "two-sum"
        assert n["number"] == 1
        assert n["title"] == "Two Sum"
        assert n["difficulty"] == "easy"  # lowercased
        assert n["tags"] == ["array", "hash-table"]
        assert n["hints"] == ["use hash"]
        assert n["raw_html"].startswith("<p>")
        assert n["method_name"] == "twoSum"
        assert n["return_type"] == "integer[]"

    def test_params_count_and_split(self):
        n = normalize_question(SAMPLE_QUESTION, TWO_SUM_CODE)
        assert n["params_count"] == 2
        assert n["cases_input"] == ["[2,7,11,15]\n9", "[3,2,4]\n6"]

    def test_core_lines_extracted(self):
        n = normalize_question(SAMPLE_QUESTION, TWO_SUM_CODE)
        assert len(n["core_lines"]) > 0
        assert any("prevMap = {}" in l for l in n["core_lines"])

    def test_code_none_fallback(self):
        # neetcode-gh 누락 (404) → core_lines 빈 list
        n = normalize_question(SAMPLE_QUESTION, None)
        assert n["code"] is None
        assert n["core_lines"] == []
        # 다른 필드는 정상
        assert n["slug"] == "two-sum"
        assert n["params_count"] == 2

    def test_invalid_metadata_falls_back(self):
        broken = {**SAMPLE_QUESTION, "metaData": "not-json"}
        n = normalize_question(broken, TWO_SUM_CODE)
        assert n["params_count"] == 0
        assert n["cases_input"] == []  # params_count=0 이라 split 못함
