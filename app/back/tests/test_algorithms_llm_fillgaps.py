"""TDD — algorithms LLM gap-filler (spec-07 §7.1 d)."""

from __future__ import annotations

import json

import pytest

from service.jobs.algorithms.llm_fillgaps import (
    LLMFillError,
    _build_prompt,
    _extract_json,
    _validate_schema,
    fill_gaps,
)


# ---------- fixtures ----------


NORMALIZED_TWO_SUM = {
    "slug": "two-sum",
    "number": 1,
    "title": "Two Sum",
    "difficulty": "easy",
    "tags": ["array", "hash-table"],
    "hints": ["use hash"],
    "raw_html": "<p>Given an array...</p>",
    "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
    "params_count": 2,
    "method_name": "twoSum",
    "return_type": "integer[]",
    "cases_input": ["[2,7,11,15]\n9", "[3,2,4]\n6"],
    "code": "class Solution:\n    def twoSum(self, nums, target):\n        seen = {}\n        for i, n in enumerate(nums):\n            return [seen[n], i]",
    "core_lines": [
        "seen = {}",
        "for i, n in enumerate(nums):",
        "return [seen[n], i]",
    ],
}


def _i18n(ko: str = "한", en: str = "en") -> dict:
    return {"ko": ko, "en": en}


def _valid_response(normalized: dict = NORMALIZED_TWO_SUM) -> dict:
    """schema 통과하는 응답 (테스트 baseline)."""
    cases_n = len(normalized["cases_input"])
    core_n = len(normalized["core_lines"])
    return {
        "problem": {
            "title": _i18n("Two Sum"),
            "statement": _i18n("두 인덱스 합 target", "two indices sum to target"),
            "constraints": ["2 ≤ n ≤ 1e4"],
            "io_outputs": ["[0, 1]"] * cases_n,
        },
        "clarifying_items": [
            {"q": _i18n(), "type": "good", "why": _i18n()},
            {"q": _i18n(), "type": "good", "why": _i18n()},
            {"q": _i18n(), "type": "distractor", "why": _i18n()},
        ],
        "approach_items": [
            {"name": _i18n(), "complexity": "O(n)", "type": "good", "why": _i18n()},
            {"name": _i18n(), "complexity": "O(n²)", "type": "distractor", "why": _i18n()},
            {"name": _i18n(), "complexity": "O(n log n)", "type": "distractor", "why": _i18n()},
        ],
        "logic_slots": [
            {
                "label": _i18n(),
                "indent": 0,
                "good_line_index": 0,  # within core_n=3
                "good_why": _i18n(),
                "distractors": [
                    {"code": "x = []", "why": _i18n()},
                    {"code": "x = ()", "why": _i18n()},
                ],
            },
            {
                "label": _i18n(),
                "indent": 0,
                "good_line_index": 1,
                "good_why": _i18n(),
                "distractors": [{"code": "for n in nums:", "why": _i18n()}],
            },
            {
                "label": _i18n(),
                "indent": 1,
                "good_line_index": 2,
                "good_why": _i18n(),
                "distractors": [{"code": "return seen", "why": _i18n()}],
            },
        ],
        "trace_worked_example": {
            "input_case_index": 0,
            "steps": [_i18n(), _i18n()],
            "answer": "[0, 1]",
        },
        "solution": {
            "complexity": {"time": "O(n)", "space": "O(n)"},
            "followup": [_i18n()],
        },
    }


# ---------- _extract_json ----------


class TestExtractJson:
    def test_raw_json(self):
        assert _extract_json('{"a": 1}') == '{"a": 1}'

    def test_with_code_fence(self):
        text = '```json\n{"a": 1}\n```'
        assert _extract_json(text) == '{"a": 1}'

    def test_with_prose(self):
        text = 'Here is the result:\n{"a": 1}\nDone.'
        assert _extract_json(text) == '{"a": 1}'

    def test_nested_braces(self):
        # 가장 바깥 {} 박스 추출
        text = '{"a": {"b": 1}, "c": 2}'
        assert _extract_json(text) == '{"a": {"b": 1}, "c": 2}'


# ---------- _validate_schema ----------


class TestValidateSchema:
    def test_accepts_valid(self):
        # 예외 X
        _validate_schema(_valid_response(), NORMALIZED_TWO_SUM)

    def test_rejects_missing_top_key(self):
        bad = _valid_response()
        del bad["problem"]
        with pytest.raises(ValueError, match="missing top-level keys"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_problem_title_not_i18n(self):
        bad = _valid_response()
        bad["problem"]["title"] = "just a string"
        with pytest.raises(ValueError, match="title"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_io_outputs_length_mismatch(self):
        bad = _valid_response()
        bad["problem"]["io_outputs"] = ["only one"]  # cases_input has 2
        with pytest.raises(ValueError, match="io_outputs length"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_clarifying_too_few(self):
        bad = _valid_response()
        bad["clarifying_items"] = [bad["clarifying_items"][0]]  # only 1
        with pytest.raises(ValueError, match="clarifying_items"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_invalid_type_enum(self):
        bad = _valid_response()
        bad["clarifying_items"][0]["type"] = "neutral"
        with pytest.raises(ValueError, match="type"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_logic_slot_index_out_of_range(self):
        bad = _valid_response()
        bad["logic_slots"][0]["good_line_index"] = 99  # core_n=3
        with pytest.raises(ValueError, match="good_line_index"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_logic_slot_negative_index(self):
        bad = _valid_response()
        bad["logic_slots"][0]["good_line_index"] = -1
        with pytest.raises(ValueError, match="good_line_index"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_rejects_trace_input_case_index_out_of_range(self):
        bad = _valid_response()
        bad["trace_worked_example"]["input_case_index"] = 99
        with pytest.raises(ValueError, match="input_case_index"):
            _validate_schema(bad, NORMALIZED_TWO_SUM)

    def test_logic_slots_skipped_when_no_core_lines(self):
        # core_lines 비었을 때 (neetcode-gh 누락) → logic_slots 길이 검증 스킵
        normalized_no_code = {**NORMALIZED_TWO_SUM, "core_lines": [], "code": None}
        valid = _valid_response()
        valid["logic_slots"] = []  # empty OK
        _validate_schema(valid, normalized_no_code)


# ---------- _build_prompt ----------


class TestBuildPrompt:
    def test_includes_required_sections(self):
        p = _build_prompt(NORMALIZED_TWO_SUM)
        # 핵심 섹션 모두 포함
        for keyword in [
            "two-sum",
            "Two Sum",
            "easy",
            "array",
            "<p>Given",  # raw HTML
            "class Solution",  # code
            "[0] seen = {}",  # core_lines indexed
            "[0] [2,7,11,15]",  # cases indexed
            "JSON",
            "good_line_index",
            "input_case_index",
        ]:
            assert keyword in p, f"prompt missing keyword: {keyword!r}"

    def test_handles_missing_code(self):
        n = {**NORMALIZED_TWO_SUM, "code": None, "core_lines": []}
        p = _build_prompt(n)
        assert "(missing" in p

    def test_design_branch_in_prompt(self):
        n = {
            **NORMALIZED_TWO_SUM,
            "is_design": True,
            "classname": "MinStack",
            "methods": [
                {"name": "push", "params": [{"name": "val", "type": "integer"}]},
                {"name": "pop", "params": []},
                {"name": "top", "params": []},
                {"name": "getMin", "params": []},
            ],
            "params_count": 2,
        }
        p = _build_prompt(n)
        assert "DESIGN PROBLEM" in p
        assert "systemdesign" in p
        assert "MinStack" in p
        assert "push" in p and "getMin" in p
        # 일반 분기의 'params=2' 라벨은 design에서 노출되지 않아야 함 (오해 방지)
        assert "params=2)" not in p

    def test_non_design_omits_design_note(self):
        n = {**NORMALIZED_TWO_SUM, "is_design": False}
        p = _build_prompt(n)
        assert "DESIGN PROBLEM" not in p
        assert "params=2)" in p  # 일반 분기 라벨


# ---------- fill_gaps integration (mock client) ----------


class _MockTask:
    def __init__(self, result: str):
        self.result = result


class _MockClient:
    """ClaudeClient 대체 — 미리 박은 응답 list 를 순서대로 반환."""

    def __init__(self, responses: list[str]):
        self._responses = list(responses)
        self.submit_calls = 0

    async def submit(self, **kw) -> str:
        self.submit_calls += 1
        return f"task-{self.submit_calls}"

    async def result(self, task_id: str, **kw) -> _MockTask:
        if not self._responses:
            return _MockTask("")
        return _MockTask(self._responses.pop(0))


@pytest.mark.asyncio
async def test_fill_gaps_returns_parsed_dict():
    valid = _valid_response()
    client = _MockClient([json.dumps(valid)])
    result = await fill_gaps(NORMALIZED_TWO_SUM, client=client)
    assert "problem" in result
    assert result["problem"]["title"]["ko"] == "Two Sum"
    assert client.submit_calls == 1


@pytest.mark.asyncio
async def test_fill_gaps_retries_on_invalid():
    invalid = json.dumps({"missing": "everything"})
    valid = json.dumps(_valid_response())
    client = _MockClient([invalid, valid])
    result = await fill_gaps(NORMALIZED_TWO_SUM, client=client)
    assert "problem" in result
    assert client.submit_calls == 2  # 1차 실패 + 재시도 성공


@pytest.mark.asyncio
async def test_fill_gaps_raises_after_all_retries():
    invalid = json.dumps({"missing": "everything"})
    client = _MockClient([invalid, invalid, invalid])
    with pytest.raises(LLMFillError, match="2회 실패"):
        await fill_gaps(NORMALIZED_TWO_SUM, client=client)


@pytest.mark.asyncio
async def test_fill_gaps_handles_json_with_prose():
    # LLM 가 prose 섞어 응답 → _extract_json 으로 추출
    valid = _valid_response()
    raw = f"Sure, here's the JSON:\n```json\n{json.dumps(valid)}\n```\nDone."
    client = _MockClient([raw])
    result = await fill_gaps(NORMALIZED_TWO_SUM, client=client)
    assert "problem" in result


# ---------- design problem branch (systemdesign) ----------


NORMALIZED_MIN_STACK = {
    "slug": "min-stack",
    "number": 155,
    "title": "Min Stack",
    "difficulty": "medium",
    "tags": ["stack", "design"],
    "hints": [],
    "raw_html": "<p>Design a stack...</p>",
    "params": [],
    "params_count": 2,
    "method_name": "MinStack",
    "return_type": "design",
    "is_design": True,
    "classname": "MinStack",
    "methods": [
        {"name": "push", "params": [{"name": "val", "type": "integer"}]},
        {"name": "pop", "params": []},
        {"name": "top", "params": []},
        {"name": "getMin", "params": []},
    ],
    "cases_input": [
        '["MinStack","push","push","push","getMin","pop","top","getMin"]\n'
        "[[],[-2],[0],[-3],[],[],[],[]]"
    ],
    "code": "class MinStack:\n    def __init__(self):\n        self.stack = []\n",
    "core_lines": [
        "        self.stack = []",
        "        self.minStack = []",
        "        self.stack.append(val)",
        "        val = min(val, self.minStack[-1] if self.minStack else val)",
        "        self.minStack.append(val)",
        "        self.stack.pop()",
        "        self.minStack.pop()",
        "        return self.stack[-1]",
        "        return self.minStack[-1]",
    ],
}


def _valid_design_response() -> dict:
    """Min Stack 형태의 schema 통과 응답 — 1 case, op 시퀀스 io_outputs."""
    core_n = len(NORMALIZED_MIN_STACK["core_lines"])
    return {
        "problem": {
            "title": _i18n("최소값 스택", "Min Stack"),
            "statement": _i18n("최소값을 상수 시간에", "min in O(1)"),
            "constraints": ["-2^31 ≤ val ≤ 2^31 - 1"],
            "io_outputs": ["[null, null, null, null, -3, null, 0, -2]"],
        },
        "clarifying_items": [
            {"q": _i18n(), "type": "good", "why": _i18n()},
            {"q": _i18n(), "type": "good", "why": _i18n()},
            {"q": _i18n(), "type": "distractor", "why": _i18n()},
        ],
        "approach_items": [
            {"name": _i18n(), "complexity": "O(1) per op", "type": "good", "why": _i18n()},
            {"name": _i18n(), "complexity": "O(n) getMin", "type": "distractor", "why": _i18n()},
            {"name": _i18n(), "complexity": "O(n) push", "type": "distractor", "why": _i18n()},
        ],
        "logic_slots": [
            {
                "label": _i18n("초기화"),
                "indent": 0,
                "good_line_index": 0,
                "good_why": _i18n(),
                "distractors": [{"code": "self.stack = None", "why": _i18n()}],
            },
            {
                "label": _i18n("push: 새 min 계산"),
                "indent": 0,
                "good_line_index": 3,
                "good_why": _i18n(),
                "distractors": [{"code": "val = max(val, self.minStack[-1])", "why": _i18n()}],
            },
            {
                "label": _i18n("getMin"),
                "indent": 0,
                "good_line_index": core_n - 1,  # last line
                "good_why": _i18n(),
                "distractors": [{"code": "return min(self.stack)", "why": _i18n()}],
            },
        ],
        "trace_worked_example": {
            "input_case_index": 0,
            "steps": [_i18n(), _i18n(), _i18n()],
            "answer": "[null, null, null, null, -3, null, 0, -2]",
        },
        "solution": {
            "complexity": {"time": "O(1) per op", "space": "O(n)"},
            "followup": [_i18n()],
        },
    }


class TestDesignSchema:
    def test_validates_design_response(self):
        # design 분기 — cases=1, op-list io_outputs 통과
        _validate_schema(_valid_design_response(), NORMALIZED_MIN_STACK)

    def test_rejects_io_outputs_count_mismatch_for_design(self):
        bad = _valid_design_response()
        bad["problem"]["io_outputs"] = ["[null]", "[null,-3]"]  # 2 != 1 case
        with pytest.raises(ValueError, match="io_outputs length"):
            _validate_schema(bad, NORMALIZED_MIN_STACK)


@pytest.mark.asyncio
async def test_fill_gaps_design_problem():
    client = _MockClient([json.dumps(_valid_design_response())])
    result = await fill_gaps(NORMALIZED_MIN_STACK, client=client)
    assert result["problem"]["title"]["en"] == "Min Stack"
    assert result["trace_worked_example"]["answer"].startswith("[null,")
