"""TDD — neetcode_canonical_job orchestrator (5단계 통합)."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest

from service.jobs.algorithms.sequence import SequenceItem


# ---------- helpers ----------


def _seq_item(slug: str = "valid-anagram", number: int = 242) -> SequenceItem:
    return SequenceItem(
        slug=slug,
        number=number,
        title="Valid Anagram",
        pattern="Arrays & Hashing",
        difficulty="easy",
    )


SAMPLE_QUESTION = {
    "questionId": "242",
    "questionFrontendId": "242",
    "title": "Valid Anagram",
    "titleSlug": "valid-anagram",
    "content": "<p>Given two strings...</p>",
    "difficulty": "Easy",
    "exampleTestcases": '"anagram"\n"nagaram"\n"rat"\n"car"',
    "topicTags": [{"name": "Hash Table", "slug": "hash-table"}, {"name": "String", "slug": "string"}],
    "metaData": '{"name": "isAnagram", "params": [{"name": "s", "type": "string"}, {"name": "t", "type": "string"}], "return": {"type": "boolean"}}',
}

SAMPLE_CODE = """class Solution:
    def isAnagram(self, s, t):
        return sorted(s) == sorted(t)
"""


def _i18n(ko="ko", en="en") -> dict:
    return {"ko": ko, "en": en}


def _llm_response() -> dict:
    return {
        "problem": {
            "title": _i18n("Valid Anagram", "Valid Anagram"),
            "statement": _i18n("애너그램", "anagram"),
            "constraints": ["1 ≤ s.length ≤ 5e4"],
            "io_outputs": ["true", "false"],
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
                "label": _i18n("정렬·비교", "sort-compare"),
                "indent": 0,
                "good_line_index": 0,
                "good_why": _i18n(),
                "distractors": [{"code": "return s == t", "why": _i18n()}],
            },
            {
                "label": _i18n("Step 2", "Step 2"),
                "indent": 0,
                "good_line_index": 0,
                "good_why": _i18n(),
                "distractors": [{"code": "return False", "why": _i18n()}],
            },
            {
                "label": _i18n("Step 3", "Step 3"),
                "indent": 1,
                "good_line_index": 0,
                "good_why": _i18n(),
                "distractors": [{"code": "return True", "why": _i18n()}],
            },
        ],
        "trace_worked_example": {
            "input_case_index": 0,
            "steps": [_i18n(), _i18n()],
            "answer": "true",
        },
        "solution": {
            "complexity": {"time": "O(n log n)", "space": "O(1)"},
            "followup": [_i18n()],
        },
    }


@pytest.fixture
def mock_external(monkeypatch, tmp_path: Path):
    """fetch / commit_and_push / notify_slack / load_all monkeypatch."""
    from service.jobs.algorithms import main as job_main
    from service.jobs.algorithms import sequence as seq_mod
    from service.jobs.algorithms import fetch as fetch_mod

    # _meta + minimum profile so load_persona doesn't fail
    (tmp_path / "_meta.yaml").write_text(
        "projects:\n  categories: []\nnotes:\n  clusters: []\n", encoding="utf-8"
    )

    # NeetCode 150
    items = [
        _seq_item("contains-duplicate", 217),
        _seq_item("valid-anagram", 242),
    ]

    async def fake_fetch_seq(*, cache=None, client=None):
        return items

    async def fake_fetch_lc(slug, *, cache=None, client=None):
        return SAMPLE_QUESTION

    async def fake_fetch_ng(slug, number, *, cache=None, client=None):
        return SAMPLE_CODE

    monkeypatch.setattr(job_main, "fetch_neetcode_150", fake_fetch_seq)
    monkeypatch.setattr(job_main, "fetch_leetcode", fake_fetch_lc)
    monkeypatch.setattr(job_main, "fetch_neetcode_gh", fake_fetch_ng)

    # commit_and_push — no-op
    pushes = []

    def fake_push(*, paths, message, dry_run):
        pushes.append({"paths": list(paths), "message": message, "dry_run": dry_run})
        return {"pushed": not dry_run}

    monkeypatch.setattr(job_main, "commit_and_push_with_retry", fake_push)

    # notify_slack — capture
    slack_calls = []

    async def fake_notify(text):
        slack_calls.append(text)

    monkeypatch.setattr(job_main, "notify_slack", fake_notify)

    # load_all — no-op (실 main.load_all 은 file system 의존)
    import sys

    class _FakeMain:
        @staticmethod
        def load_all():
            pass

    monkeypatch.setitem(sys.modules, "main", _FakeMain)

    return {
        "tmp_path": tmp_path,
        "pushes": pushes,
        "slack": slack_calls,
        "items": items,
    }


# ---------- mock client ----------


import json


class _MockTask:
    def __init__(self, result: str):
        self.result = result


class _MockClient:
    def __init__(self, response: dict):
        self._response = json.dumps(response)

    async def submit(self, **kw):
        return "task-id"

    async def result(self, task_id, **kw):
        return _MockTask(self._response)


# ---------- run_neetcode_canonical_job ----------


class TestRun:
    @pytest.mark.asyncio
    async def test_happy_path_writes_md(self, mock_external):
        from service.jobs.algorithms.main import run_neetcode_canonical_job

        client = _MockClient(_llm_response())
        result = await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        # idx=0 (no existing) → A-001 = contains-duplicate
        assert result["a_id"] == "A-001"
        assert result["slug"] == "contains-duplicate"
        # 파일 박힘
        path = mock_external["tmp_path"] / "algorithms" / "A-001-contains-duplicate.md"
        assert path.exists()

    @pytest.mark.asyncio
    async def test_idx_advances_with_existing_seed(self, mock_external):
        # 시드 1개 미리 박혀있으면 → idx=1, A-002 = valid-anagram
        algos = mock_external["tmp_path"] / "algorithms"
        algos.mkdir(parents=True, exist_ok=True)
        (algos / "A-001-x.md").write_text(
            "---\nid: A-001\ntype: algorithm\ntitle: { ko: x, en: x }\ndate: '2026-05-06'\n"
            "source: { platform: leetcode, number: 1, slug: x, url: u }\n"
            "difficulty: easy\ntoday: true\n---\n## Data\n\n```yaml\nfoo: bar\n```\n"
        )

        from service.jobs.algorithms.main import run_neetcode_canonical_job

        client = _MockClient(_llm_response())
        result = await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        assert result["a_id"] == "A-002"
        assert result["slug"] == "valid-anagram"

    @pytest.mark.asyncio
    async def test_today_mutation(self, mock_external):
        # 시드 today=true → 잡 후 false 로 갱신 + 새 파일 today=true
        algos = mock_external["tmp_path"] / "algorithms"
        algos.mkdir(parents=True, exist_ok=True)
        (algos / "A-001-x.md").write_text(
            "---\nid: A-001\ntype: algorithm\ntitle: { ko: x, en: x }\ndate: '2026-05-06'\n"
            "source: { platform: leetcode, number: 1, slug: x, url: u }\n"
            "difficulty: easy\ntoday: true\n---\n## Data\n\n```yaml\nfoo: bar\n```\n"
        )

        from service.jobs.algorithms.main import run_neetcode_canonical_job
        import frontmatter

        client = _MockClient(_llm_response())
        await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        # A-001 today → false
        post = frontmatter.load(algos / "A-001-x.md")
        assert post.metadata["today"] is False
        # A-002 today → true
        new = next(p for p in algos.glob("A-002-*.md"))
        post2 = frontmatter.load(new)
        assert post2.metadata["today"] is True

    @pytest.mark.asyncio
    async def test_slack_notify_on_success(self, mock_external):
        from service.jobs.algorithms.main import run_neetcode_canonical_job

        client = _MockClient(_llm_response())
        await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        slack = mock_external["slack"]
        assert len(slack) == 1
        assert "algorithm 잡" in slack[0]
        assert "A-001" in slack[0]
        assert "contains-duplicate" in slack[0]
        assert "dry-run" in slack[0]

    @pytest.mark.asyncio
    async def test_sequence_end(self, mock_external, monkeypatch):
        # 시퀀스 끝 도달 → skip + slack
        from service.jobs.algorithms import main as job_main

        async def empty_seq(*, cache=None, client=None):
            return []  # 시퀀스 텅 빔 → idx=0 도 None

        monkeypatch.setattr(job_main, "fetch_neetcode_150", empty_seq)

        from service.jobs.algorithms.main import run_neetcode_canonical_job

        client = _MockClient(_llm_response())
        result = await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        assert result["skipped"] is True
        assert result["reason"] == "sequence_end"
        slack = mock_external["slack"]
        assert any("시퀀스 완료" in s for s in slack)

    @pytest.mark.asyncio
    async def test_slack_on_failure(self, mock_external, monkeypatch):
        # LLM 실패 → :x: slack + raise
        from service.jobs.algorithms import main as job_main
        from service.jobs.algorithms.llm_fillgaps import LLMFillError

        class _BoomClient:
            async def submit(self, **kw):
                return "task-id"

            async def result(self, task_id, **kw):
                return _MockTask("not json at all")

        from service.jobs.algorithms.main import run_neetcode_canonical_job

        with pytest.raises(LLMFillError):
            await run_neetcode_canonical_job(
                client=_BoomClient(),
                target_date=datetime.date(2026, 5, 7),
                persona_dir=mock_external["tmp_path"],
                dry_run_push=True,
            )
        slack = mock_external["slack"]
        assert any(":x:" in s and "algorithm 잡 실패" in s for s in slack)

    @pytest.mark.asyncio
    async def test_commit_paths_includes_cleared(self, mock_external):
        # 시드 + today=true → 잡 후 commit paths 에 두 파일 모두
        algos = mock_external["tmp_path"] / "algorithms"
        algos.mkdir(parents=True, exist_ok=True)
        (algos / "A-001-x.md").write_text(
            "---\nid: A-001\ntype: algorithm\ntitle: { ko: x, en: x }\ndate: '2026-05-06'\n"
            "source: { platform: leetcode, number: 1, slug: x, url: u }\n"
            "difficulty: easy\ntoday: true\n---\n## Data\n\n```yaml\nfoo: bar\n```\n"
        )

        from service.jobs.algorithms.main import run_neetcode_canonical_job

        client = _MockClient(_llm_response())
        await run_neetcode_canonical_job(
            client=client,
            target_date=datetime.date(2026, 5, 7),
            persona_dir=mock_external["tmp_path"],
            dry_run_push=True,
        )
        pushes = mock_external["pushes"]
        assert len(pushes) == 1
        push = pushes[0]
        assert push["dry_run"] is True
        assert push["message"] == "chore: algorithm A-002 valid-anagram"
        # 새 파일 + 갱신된 A-001 둘 다 paths 에
        assert len(push["paths"]) == 2
        names = [Path(p).name for p in push["paths"]]
        assert "A-002-valid-anagram.md" in names
        assert "A-001-x.md" in names
