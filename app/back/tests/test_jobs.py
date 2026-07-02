"""TDD — 잔디 잡 내부 로직 (외부 API 호출은 stub).

새 flow (ADR-06): counts deterministic + LLM body+summary → daily/{date}.md write.
"""

import json
from datetime import date
from pathlib import Path

import frontmatter
import pytest

from service.jobs.inputs import read_daily_narrative
from service.jobs.llm import (
    _build_prompt,
    summarize_daily,
    validate_llm_response,
)
from service.jobs.upsert import write_daily


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


class TestWriteDaily:
    def test_creates_file_with_frontmatter_and_body(self, tmp_path: Path):
        path = write_daily(
            date(2026, 5, 2),
            counts={"commit": 3, "note": 0, "study": 0},
            summary={"ko": ["[foo] k"], "en": ["[foo] e"]},
            body="# 한 일\n- x",
            persona_dir=tmp_path,
        )
        assert path.exists()
        post = frontmatter.load(path)
        assert post.metadata["type"] == "daily"
        assert post.metadata["date"] == "2026.05.02"
        assert post.metadata["auto"] is True
        assert post.metadata["counts"] == {"commit": 3, "note": 0, "study": 0}
        assert post.metadata["summary"] == {"ko": ["[foo] k"], "en": ["[foo] e"]}
        assert "# 한 일" in post.content

    def test_idempotent_overwrite(self, tmp_path: Path):
        write_daily(
            date(2026, 5, 2), counts={"commit": 1}, summary=None, body="a",
            persona_dir=tmp_path,
        )
        write_daily(
            date(2026, 5, 2), counts={"commit": 1}, summary=None, body="a",
            persona_dir=tmp_path,
        )
        # 같은 입력 → 같은 결과
        path = tmp_path / "daily" / "2026-05-02.md"
        post = frontmatter.load(path)
        assert post.metadata["counts"] == {"commit": 1}
        assert post.content == "a"

    def test_summary_omitted_when_none(self, tmp_path: Path):
        path = write_daily(
            date(2026, 5, 2), counts={"commit": 0, "note": 0, "study": 0},
            summary=None, body="(활동 없음)",
            persona_dir=tmp_path,
        )
        post = frontmatter.load(path)
        assert "summary" not in post.metadata

    def test_user_authored_protected(self, tmp_path: Path):
        # 본인 작성 (auto:false 또는 미박음) → overwrite skip
        path = tmp_path / "daily" / "2026-05-02.md"
        path.parent.mkdir(parents=True)
        existing = frontmatter.Post(
            content="본인이 박은 narrative", **{"type": "daily", "date": "2026.05.02"}
        )
        path.write_text(frontmatter.dumps(existing), encoding="utf-8")

        # 잡이 overwrite 시도해도 보존
        write_daily(
            date(2026, 5, 2), counts={"commit": 99},
            summary={"ko": ["[foo] k"], "en": ["[foo] e"]},
            body="잡이 박는 본문", persona_dir=tmp_path,
        )
        post = frontmatter.load(path)
        assert post.content == "본인이 박은 narrative"
        assert "auto" not in post.metadata
        assert "counts" not in post.metadata


class TestLLMEmpty:
    @pytest.mark.asyncio
    async def test_empty_inputs_skip_llm(self):
        # 활동 0 — LLM 호출 skip, client 안 봄
        r = await summarize_daily(
            date(2026, 5, 1),
            notes_changes=[], contents_changes=[], commits=[],
            counts={"commit": 0, "note": 0, "study": 0},
            client=_MockClient(""),
        )
        assert r["summary"] is None
        assert r["body"] == "(활동 없음)"


class TestLLMValidate:
    def test_valid_response_passes(self):
        r = validate_llm_response(
            {
                "summary": {"ko": ["[a] x", "[notes] y"], "en": ["[a] X", "[notes] Y"]},
                "body": "# 한 일\n- x",
            }
        )
        assert r["summary"] == {
            "ko": ["[a] x", "[notes] y"],
            "en": ["[a] X", "[notes] Y"],
        }
        assert r["body"] == "# 한 일\n- x"

    def test_empty_summary_lists_pass(self):
        # 활동 분포 0 인 카테고리만 있을 때 빈 list 도 허용 (spec-03 §3.3)
        r = validate_llm_response(
            {"summary": {"ko": [], "en": []}, "body": "x"}
        )
        assert r["summary"] == {"ko": [], "en": []}

    def test_invalid_summary_missing_keys_raises(self):
        with pytest.raises(ValueError, match="invalid_summary"):
            validate_llm_response({"summary": {"ko": ["only"]}, "body": "x"})

    def test_legacy_str_summary_raises(self):
        # 새 spec 은 list[str] — 레거시 str 은 LLM 출력에서 reject
        with pytest.raises(ValueError, match="invalid_summary_ko_not_list_str"):
            validate_llm_response(
                {"summary": {"ko": "k", "en": "e"}, "body": "x"}
            )

    def test_summary_list_with_non_str_raises(self):
        with pytest.raises(ValueError, match="invalid_summary_ko_not_list_str"):
            validate_llm_response(
                {"summary": {"ko": ["ok", 123], "en": ["ok"]}, "body": "x"}
            )

    def test_invalid_body_raises(self):
        with pytest.raises(ValueError, match="invalid_body"):
            validate_llm_response(
                {"summary": {"ko": ["k"], "en": ["e"]}, "body": 123}
            )

    def test_body_truncated_when_too_long(self):
        long_body = "x" * 1000
        r = validate_llm_response(
            {"summary": {"ko": ["k"], "en": ["e"]}, "body": long_body}
        )
        assert len(r["body"]) <= 700  # BODY_HARD_LIMIT (600) + truncation suffix
        assert "(truncated)" in r["body"]


class TestLLMBuildPrompt:
    def test_includes_counts(self):
        prompt = _build_prompt(
            date(2026, 5, 2),
            notes_changes=[], contents_changes=[], commits=[],
            counts={"commit": 5, "note": 2, "study": 1},
        )
        assert "commits: 5" in prompt
        assert "notes:   2" in prompt
        assert "study:   1" in prompt

    def test_empty_blocks_show_no_data(self):
        prompt = _build_prompt(
            date(2026, 5, 2),
            notes_changes=[], contents_changes=[], commits=[],
            counts={"commit": 0, "note": 0, "study": 0},
        )
        assert "(없음)" in prompt

    def test_includes_note_body(self):
        prompt = _build_prompt(
            date(2026, 5, 2),
            notes_changes=[
                {"path": "reference/py/x.md", "frontmatter": {"id": "x", "title": "X"}, "body": "본문 abc"}
            ],
            contents_changes=[], commits=[],
            counts={"commit": 0, "note": 1, "study": 0},
        )
        assert "[x]" in prompt
        assert "본문 abc" in prompt

    def test_includes_commit_msg(self):
        prompt = _build_prompt(
            date(2026, 5, 2),
            notes_changes=[], contents_changes=[],
            commits=[{"repo": "kknaks/foo", "msg": "fix: bar"}],
            counts={"commit": 1, "note": 0, "study": 0},
        )
        assert "[kknaks/foo]" in prompt
        assert "fix: bar" in prompt


class TestLLMSummarize:
    @pytest.mark.asyncio
    async def test_call_with_mock_client(self):
        mock_response = json.dumps(
            {
                "summary": {"ko": ["[notes] k"], "en": ["[notes] e"]},
                "body": "# 한 일\n- x",
            }
        )
        client = _MockClient(mock_response)

        r = await summarize_daily(
            date(2026, 5, 2),
            notes_changes=[{"path": "reference/py/x.md", "frontmatter": {"id": "x"}, "body": "n"}],
            contents_changes=[],
            commits=[],
            counts={"commit": 0, "note": 1, "study": 0},
            client=client,
        )
        assert r["summary"]["ko"] == ["[notes] k"]
        assert "# 한 일" in r["body"]

    @pytest.mark.asyncio
    async def test_extracts_json_from_codeblock(self):
        # Claude 가 ```json ... ``` 박는 케이스 대응
        mock_response = (
            '```json\n{"summary": {"ko": ["[study] k"], "en": ["[study] e"]}, "body": "x"}\n```'
        )
        client = _MockClient(mock_response)

        r = await summarize_daily(
            date(2026, 5, 2),
            notes_changes=[],
            contents_changes=[{"path": "persona/contents/C-001.md", "frontmatter": {"id": "C-001"}, "body": "c"}],
            commits=[],
            counts={"commit": 0, "note": 0, "study": 1},
            client=client,
        )
        assert r["summary"] == {"ko": ["[study] k"], "en": ["[study] e"]}


class TestDailyNarrativeRead:
    def test_returns_none_when_missing(self):
        assert read_daily_narrative(date(2099, 1, 1)) is None

    def test_returns_body_when_exists(self):
        # M1에서 박은 daily/2026-05-01.md 활용
        body = read_daily_narrative(date(2026, 5, 1))
        assert body is not None
        assert "오늘 한 일" in body
