"""TDD — M4 잡 내부 로직 (외부 API 호출은 stub이라 검증 X)."""

import json
from datetime import date
from pathlib import Path

import pytest
import yaml

from service.jobs.inputs import read_daily_narrative
from service.jobs.llm import (
    _build_prompt,
    summarize_activity,
    validate_llm_response,
)
from service.jobs.upsert import upsert_activity


class _MockTask:
    def __init__(self, result: str):
        self.result = result


class _MockClient:
    """ClaudeClient stand-in — 고정 응답 반환."""

    def __init__(self, response_json: str):
        self._response = response_json

    async def submit(self, **kw) -> str:
        return "task-id"

    async def result(self, task_id: str, **kw) -> _MockTask:
        return _MockTask(self._response)


class TestUpsertIdempotent:
    def test_first_entry_creates_file(self, tmp_path: Path):
        target = tmp_path / "activity.yaml"
        entry = {
            "date": "2026.05.01",
            "count": 3,
            "kind": "note",
            "summary": {"ko": "k", "en": "e"},
        }
        result = upsert_activity(entry, target)
        assert target.exists()
        assert result["totalCount"] == 3
        assert len(result["items"]) == 1

    def test_same_entry_twice_yields_same_result(self, tmp_path: Path):
        target = tmp_path / "activity.yaml"
        entry = {"date": "2026.05.01", "count": 2, "kind": "note", "summary": None}
        r1 = upsert_activity(entry, target)
        r2 = upsert_activity(entry, target)
        assert r1 == r2
        assert len(r2["items"]) == 1

    def test_overwrites_same_date_entry(self, tmp_path: Path):
        target = tmp_path / "activity.yaml"
        upsert_activity(
            {"date": "2026.05.01", "count": 1, "kind": "note", "summary": None},
            target,
        )
        upsert_activity(
            {"date": "2026.05.01", "count": 5, "kind": "study", "summary": None},
            target,
        )
        data = yaml.safe_load(target.read_text())
        assert len(data["items"]) == 1
        assert data["items"][0]["count"] == 5
        assert data["items"][0]["kind"] == "study"

    def test_totalcount_aggregates_across_days(self, tmp_path: Path):
        target = tmp_path / "activity.yaml"
        upsert_activity(
            {"date": "2026.05.01", "count": 3, "kind": "note", "summary": None},
            target,
        )
        upsert_activity(
            {"date": "2026.05.02", "count": 5, "kind": "study", "summary": None},
            target,
        )
        data = yaml.safe_load(target.read_text())
        assert data["totalCount"] == 8

    def test_rolling_365_trims_old_entries(self, tmp_path: Path):
        target = tmp_path / "activity.yaml"
        # 366일 전 entry 박음
        upsert_activity(
            {"date": "2025.04.30", "count": 99, "kind": "note", "summary": None},
            target,
        )
        # 오늘 entry 박으면 366일 전 entry는 트림되어야 함 (window=365)
        upsert_activity(
            {"date": "2026.05.01", "count": 1, "kind": "note", "summary": None},
            target,
        )
        data = yaml.safe_load(target.read_text())
        dates = [e["date"] for e in data["items"]]
        assert "2025.04.30" not in dates  # trimmed
        assert "2026.05.01" in dates


class TestLLMEmpty:
    @pytest.mark.asyncio
    async def test_empty_inputs_yield_null_kind(self):
        # 활동 0 — LLM 호출 skip, client 안 봄
        r = await summarize_activity(date(2026, 5, 1), None, [], [], [], client=_MockClient(""))
        assert r["kind"] is None
        assert r["count"] == 0
        assert r["summary"] is None


class TestLLMValidate:
    def test_kind_fallback_to_none(self):
        # ALLOWED_KINDS 외 값 → None fallback
        r = validate_llm_response(
            {"kind": "rant", "summary": {"ko": "k", "en": "e"}}, expected_count=3
        )
        assert r["kind"] is None
        assert r["count"] == 3

    def test_count_uses_expected_not_llm(self):
        # LLM 응답의 count 무시, expected_count 박음 (idempotent)
        r = validate_llm_response(
            {"kind": "note", "count": 999, "summary": None}, expected_count=2
        )
        assert r["count"] == 2

    def test_invalid_summary_raises(self):
        with pytest.raises(ValueError, match="invalid_summary"):
            validate_llm_response({"kind": "note", "summary": {"ko": "only"}}, expected_count=1)

    def test_null_summary_passes(self):
        r = validate_llm_response({"kind": None, "summary": None}, expected_count=0)
        assert r["summary"] is None


class TestLLMBuildPrompt:
    def test_includes_narrative(self):
        prompt = _build_prompt(
            date(2026, 5, 1), narrative="오늘 한 일", notes=[], contents=[], commits=[]
        )
        assert "오늘 한 일" in prompt

    def test_no_narrative_block_when_missing(self):
        prompt = _build_prompt(date(2026, 5, 1), None, notes=[], contents=[], commits=[])
        assert "미작성" in prompt

    def test_bullets_default_to_no_data(self):
        prompt = _build_prompt(date(2026, 5, 1), None, notes=[], contents=[], commits=[])
        assert "(없음)" in prompt


class TestLLMSummarize:
    @pytest.mark.asyncio
    async def test_call_with_mock_client(self):
        mock_response = json.dumps(
            {"kind": "study", "count": 99, "summary": {"ko": "k", "en": "e"}}
        )
        client = _MockClient(mock_response)

        r = await summarize_activity(
            date(2026, 5, 1),
            narrative=None,
            notes=[{"subject": "n"}],
            contents=[{"subject": "c"}],
            commits=[],
            client=client,
        )
        assert r["kind"] == "study"
        assert r["count"] == 2  # 실 입력 합계, LLM 응답의 99 무시
        assert r["summary"]["ko"] == "k"

    @pytest.mark.asyncio
    async def test_extracts_json_from_codeblock(self):
        # Claude 가 ```json ... ``` 박는 케이스 대응
        mock_response = '```json\n{"kind": "note", "summary": {"ko": "k", "en": "e"}}\n```'
        client = _MockClient(mock_response)

        r = await summarize_activity(
            date(2026, 5, 1), None, [{"subject": "n"}], [], [], client=client
        )
        assert r["kind"] == "note"


class TestDailyNarrativeRead:
    def test_returns_none_when_missing(self):
        assert read_daily_narrative(date(2099, 1, 1)) is None

    def test_returns_body_when_exists(self):
        # M1에서 박은 daily/2026-05-01.md 활용
        body = read_daily_narrative(date(2026, 5, 1))
        assert body is not None
        assert "오늘 한 일" in body
