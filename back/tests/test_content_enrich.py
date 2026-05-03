"""TDD — content enrich 잡 내부 로직 (외부 호출은 monkeypatch 로 mock)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import frontmatter
import pytest

from service.jobs import content_enrich
from service.jobs.content_enrich import (
    _build_prompt,
    _compute_day_index,
    _enrich_one,
    format_duration,
    mark_error,
    merge_frontmatter,
    run_content_enrich_job,
    scan_pending_contents,
    validate_llm_response,
    write_enriched,
)


def _write_md(path: Path, **meta) -> None:
    body = meta.pop("_body", "")
    post = frontmatter.Post(content=body, **meta)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")


# ───────────────────────────────────────────────────────────────────────
# 외부 호출 mock — yt-dlp / youtube-transcript-api / open-kknaks 모두 차단
# ───────────────────────────────────────────────────────────────────────

class _DummyBroker:
    async def connect(self): pass
    async def close(self): pass


class _DummyClient:
    def __init__(self, broker=None): self.broker = broker


@pytest.fixture
def mock_external(monkeypatch):
    def _meta(youtube_id):
        return {
            "title": f"mock-{youtube_id}",
            "description": "mock desc",
            "duration_s": 1122,
            "channel": "kknaks",
            "tags": ["python"],
            "thumbnail": "",
            "upload_date": "20260502",
        }

    def _transcript(youtube_id):
        return f"mock transcript for {youtube_id}"

    async def _summarize(youtube_id, metadata, transcript, user_intent, client):
        return {
            "title": {"ko": f"제목-{youtube_id}", "en": f"title-{youtube_id}"},
            "summary": {"ko": "요약 한 줄", "en": "one-line summary"},
            "tags": ["#mock", "#test"],
            "concept": [
                "[mock] 핵심 개념 1",
                "[mock] 핵심 개념 2",
                "[mock] 핵심 개념 3",
                "[mock] 핵심 개념 4",
            ],
            "body": (
                "## 개요\n[mock] 본문 가짜 내용 길이 충족용 텍스트.\n\n"
                "## 배경 / 사전 지식\n[mock]\n\n"
                "## 핵심 개념\n[mock]\n\n"
                "## 작동 원리\n[mock]\n\n"
                "## 코드 예시\n```python\nx = 1\n```\n\n"
                "## 함정·실수\n[mock]\n\n"
                "## 베스트 프랙티스\n[mock]\n\n"
                "## 참고\n(영상 내 명시 없음)\n"
            ),
            "kind": "study",
        }

    monkeypatch.setattr(content_enrich, "extract_metadata", _meta)
    monkeypatch.setattr(content_enrich, "extract_transcript", _transcript)
    monkeypatch.setattr(content_enrich, "summarize_content", _summarize)
    monkeypatch.setattr(content_enrich, "RedisBroker", lambda **kw: _DummyBroker())
    monkeypatch.setattr(content_enrich, "ClaudeClient", _DummyClient)


# ───────────────────────────────────────────────────────────────────────
# 순수 함수 (외부 의존 없음)
# ───────────────────────────────────────────────────────────────────────

class TestScanPending:
    def test_returns_only_pending(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001-a.md", id="C-001", type="content", youtubeId="a", status="pending")
        _write_md(d / "C-002-b.md", id="C-002", type="content", youtubeId="b", status="published")
        _write_md(d / "C-003-c.md", id="C-003", type="content", youtubeId="c", status="error")

        result = scan_pending_contents(d)
        assert [p.name for p in result] == ["C-001-a.md"]

    def test_returns_empty_when_no_pending(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001.md", id="C-001", type="content", youtubeId="x", status="published")
        assert scan_pending_contents(d) == []

    def test_ignores_non_C_files(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "README.md", status="pending")
        assert scan_pending_contents(d) == []


class TestFormatDuration:
    @pytest.mark.parametrize("seconds, expected", [
        (60, "1:00"),
        (1122, "18:42"),
        (3725, "1:02:05"),
        (0, "0:00"),
    ])
    def test_format(self, seconds: int, expected: str):
        assert format_duration(seconds) == expected


class TestComputeDayIndex:
    def test_empty_dir_returns_1(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        assert _compute_day_index(d) == 1

    def test_picks_max_plus_one(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001.md", id="C-001", type="content", day="Day 03")
        _write_md(d / "C-002.md", id="C-002", type="content", day="Day 05")
        _write_md(d / "C-003.md", id="C-003", type="content", day="Day 02")
        assert _compute_day_index(d) == 6


class TestValidateLLMResponse:
    @pytest.fixture
    def good(self) -> dict:
        return {
            "title": {"ko": "t", "en": "t"},
            "summary": {"ko": "s", "en": "s"},
            "tags": ["#a", "#b"],
            "concept": ["c1", "c2", "c3", "c4"],
            "body": "## 개념\n" + "x" * 60,
            "kind": "study",
        }

    def test_passes_good(self, good: dict):
        assert validate_llm_response(good) is good

    def test_rejects_missing_title(self, good: dict):
        good["title"] = {"ko": "t"}
        with pytest.raises(ValueError, match="invalid_title"):
            validate_llm_response(good)

    def test_rejects_non_hash_tag(self, good: dict):
        good["tags"] = ["fastapi"]
        with pytest.raises(ValueError, match="invalid_tags"):
            validate_llm_response(good)

    def test_rejects_short_body(self, good: dict):
        good["body"] = "short"
        with pytest.raises(ValueError, match="invalid_body"):
            validate_llm_response(good)

    def test_unknown_kind_falls_back_to_study(self, good: dict):
        good["kind"] = "rant"
        out = validate_llm_response(good)
        assert out["kind"] == "study"


class TestMergeFrontmatter:
    def test_preserves_user_input(self):
        user = {"id": "C-005", "type": "content", "youtubeId": "abc", "status": "pending", "intent": "강조점"}
        llm = {
            "title": {"ko": "T", "en": "T"},
            "summary": {"ko": "S", "en": "S"},
            "tags": ["#x"], "concept": ["c1", "c2"], "body": "...", "kind": "study",
        }
        meta = {"duration_s": 60, "channel": "ch"}

        out = merge_frontmatter(user, llm, meta, date(2026, 5, 2), day_index=5, transcript_available=True)
        assert out["id"] == "C-005"
        assert out["type"] == "content"
        assert out["youtubeId"] == "abc"
        assert out["intent"] == "강조점"
        assert out["status"] == "published"

    def test_llm_title_overrides_user_stub(self):
        # commit df677fa 이후 정책 — LLM 응답이 user stub 갈아엎음 (setdefault → assign).
        # user 가 박은 값 보존하려면 enrich 후 published 상태에서 별도 수정.
        user = {
            "id": "C-005", "type": "content", "youtubeId": "abc", "status": "pending",
            "title": {"ko": "USER", "en": "USER"},
        }
        llm = {
            "title": {"ko": "LLM", "en": "LLM"},
            "summary": {"ko": "s", "en": "s"},
            "tags": ["#x"], "concept": ["c1", "c2"], "body": "...", "kind": "study",
        }
        meta = {"duration_s": 60, "channel": "ch"}

        out = merge_frontmatter(user, llm, meta, date(2026, 5, 2), day_index=1, transcript_available=False)
        assert out["title"]["ko"] == "LLM"

    def test_clears_error_fields_on_republish(self):
        user = {
            "id": "C-005", "type": "content", "youtubeId": "abc", "status": "pending",
            "error_reason": "stale", "errored_at": "2026-05-01T00:00:00+09:00",
        }
        llm = {
            "title": {"ko": "t", "en": "t"}, "summary": {"ko": "s", "en": "s"},
            "tags": ["#x"], "concept": ["c1", "c2"], "body": "...", "kind": "study",
        }
        meta = {"duration_s": 60, "channel": "ch"}

        out = merge_frontmatter(user, llm, meta, date(2026, 5, 2), day_index=1, transcript_available=False)
        assert "error_reason" not in out
        assert "errored_at" not in out


class TestWriteAndMarkError:
    def test_write_then_scan_skips(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        path = d / "C-001.md"
        _write_md(path, id="C-001", type="content", youtubeId="x", status="pending")

        new_meta = {"id": "C-001", "type": "content", "youtubeId": "x", "status": "published"}
        write_enriched(path, new_meta, "## 개념\n본문")

        assert scan_pending_contents(d) == []

    def test_mark_error_sets_status_and_reason(self, tmp_path: Path):
        d = tmp_path / "contents"
        d.mkdir()
        path = d / "C-001.md"
        _write_md(path, id="C-001", type="content", youtubeId="x", status="pending")

        mark_error(path, reason="ValueError")

        post = frontmatter.load(path)
        assert post.metadata["status"] == "error"
        assert post.metadata["error_reason"] == "ValueError"
        assert "errored_at" in post.metadata
        assert scan_pending_contents(d) == []


class TestBuildPrompt:
    """프롬프트 빌드 — 외부 호출 의존 없음."""

    def test_includes_metadata(self):
        prompt = _build_prompt(
            metadata={"title": "T", "channel": "C", "duration_s": 1122, "tags": ["python"], "description": "desc"},
            transcript=None,
            user_intent=None,
        )
        assert "T" in prompt
        assert "1122s" in prompt

    def test_intent_added_when_provided(self):
        prompt = _build_prompt(
            metadata={"title": "T", "channel": "C", "duration_s": 60, "tags": [], "description": ""},
            transcript=None,
            user_intent="강조점이다",
        )
        assert "강조점이다" in prompt

    def test_no_transcript_block_when_missing(self):
        prompt = _build_prompt(
            metadata={"title": "T", "channel": "C", "duration_s": 60, "tags": [], "description": ""},
            transcript=None,
            user_intent=None,
        )
        assert "자막 없음" in prompt

    def test_transcript_truncated_at_8000(self):
        long = "가" * 10000
        prompt = _build_prompt(
            metadata={"title": "T", "channel": "C", "duration_s": 60, "tags": [], "description": ""},
            transcript=long,
            user_intent=None,
        )
        # 8000 자만 포함, 그 뒤는 잘림
        assert "가" * 8000 in prompt
        assert "가" * 9000 not in prompt


# ───────────────────────────────────────────────────────────────────────
# orchestrator (외부 호출 monkeypatch)
# ───────────────────────────────────────────────────────────────────────

class TestEnrichOne:
    @pytest.mark.asyncio
    async def test_pending_to_published(self, tmp_path: Path, mock_external):
        d = tmp_path / "contents"
        d.mkdir()
        path = d / "C-001-test.md"
        _write_md(path, id="C-001", type="content", youtubeId="abc", status="pending")

        await _enrich_one(path, d, _DummyClient())

        post = frontmatter.load(path)
        assert post.metadata["status"] == "published"
        assert post.metadata["youtubeId"] == "abc"
        assert "title" in post.metadata
        assert "summary" in post.metadata
        assert "concept" in post.metadata
        assert isinstance(post.metadata["concept"], list) and len(post.metadata["concept"]) >= 2
        assert "## 개요" in post.content

    @pytest.mark.asyncio
    async def test_missing_youtube_id_raises(self, tmp_path: Path, mock_external):
        d = tmp_path / "contents"
        d.mkdir()
        path = d / "C-001-broken.md"
        _write_md(path, id="C-001", type="content", status="pending")

        with pytest.raises(ValueError, match="missing_youtubeId"):
            await _enrich_one(path, d, _DummyClient())


class TestRunJob:
    @pytest.mark.asyncio
    async def test_returns_zero_when_no_pending(self, tmp_path: Path, monkeypatch, mock_external):
        monkeypatch.setattr(content_enrich.config, "PERSONA_DIR", tmp_path)
        (tmp_path / "contents").mkdir()
        _write_md(
            tmp_path / "contents" / "C-001.md",
            id="C-001", type="content", youtubeId="x", status="published",
        )
        assert await run_content_enrich_job(client=_DummyClient(), dry_run_push=True) == 0

    @pytest.mark.asyncio
    async def test_processes_pending(self, tmp_path: Path, monkeypatch, mock_external):
        monkeypatch.setattr(content_enrich.config, "PERSONA_DIR", tmp_path)
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001-a.md", id="C-001", type="content", youtubeId="a", status="pending")
        _write_md(d / "C-002-b.md", id="C-002", type="content", youtubeId="b", status="pending")

        result = await run_content_enrich_job(client=_DummyClient(), dry_run_push=True)
        assert result == 2

        # 두 번째 실행은 모두 published 라 0
        assert await run_content_enrich_job(client=_DummyClient(), dry_run_push=True) == 0

    @pytest.mark.asyncio
    async def test_marks_error_on_missing_youtube_id(self, tmp_path: Path, monkeypatch, mock_external):
        monkeypatch.setattr(content_enrich.config, "PERSONA_DIR", tmp_path)
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001-broken.md", id="C-001", type="content", status="pending")

        result = await run_content_enrich_job(client=_DummyClient(), dry_run_push=True)
        assert result == 0

        post = frontmatter.load(d / "C-001-broken.md")
        assert post.metadata["status"] == "error"
        assert "missing_youtubeId" in post.metadata["error_reason"]

    @pytest.mark.asyncio
    async def test_self_contained_broker_when_no_client(self, tmp_path: Path, monkeypatch, mock_external):
        """client=None 일 때 함수가 자체 broker connect/close — mock_external 의 RedisBroker/ClaudeClient 활용."""
        monkeypatch.setattr(content_enrich.config, "PERSONA_DIR", tmp_path)
        d = tmp_path / "contents"
        d.mkdir()
        _write_md(d / "C-001-a.md", id="C-001", type="content", youtubeId="a", status="pending")

        result = await run_content_enrich_job(client=None, dry_run_push=True)
        assert result == 1
