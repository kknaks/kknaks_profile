"""TDD — M4 잡 내부 로직 (외부 API 호출은 stub이라 검증 X)."""

from datetime import date
from pathlib import Path

import pytest
import yaml

from service.jobs.inputs import read_daily_narrative
from service.jobs.llm import summarize_activity
from service.jobs.upsert import upsert_activity


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


class TestLLMStub:
    def test_empty_inputs_yield_null_kind(self):
        r = summarize_activity(date(2026, 5, 1), None, [], [], [])
        assert r["kind"] is None
        assert r["count"] == 0

    def test_count_is_sum_of_three_categories(self):
        r = summarize_activity(
            date(2026, 5, 1),
            narrative="some narrative",  # narrative는 count 제외 (spec-03 §3.2)
            notes=[{"subject": "a"}, {"subject": "b"}],
            contents=[{"subject": "c"}],
            commits=[{"msg": "d"}, {"msg": "e"}],
        )
        assert r["count"] == 5

    def test_kind_priority_study_over_note(self):
        r = summarize_activity(
            date(2026, 5, 1), None, notes=[{"subject": "n"}], contents=[{"subject": "s"}], commits=[]
        )
        assert r["kind"] == "study"

    def test_returns_i18n_summary(self):
        r = summarize_activity(
            date(2026, 5, 1), None, notes=[], contents=[], commits=[{"msg": "c"}]
        )
        assert "ko" in r["summary"] and "en" in r["summary"]


class TestDailyNarrativeRead:
    def test_returns_none_when_missing(self):
        assert read_daily_narrative(date(2099, 1, 1)) is None

    def test_returns_body_when_exists(self):
        # M1에서 박은 daily/2026-05-01.md 활용
        body = read_daily_narrative(date(2026, 5, 1))
        assert body is not None
        assert "오늘 한 일" in body
