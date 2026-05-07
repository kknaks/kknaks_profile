"""TDD — algorithms write 모듈 (spec-07 §7.1 e + §8.1 today mutation)."""

from __future__ import annotations

import datetime
import re
from pathlib import Path

import frontmatter
import pytest
import yaml

from service.jobs.algorithms.sequence import SequenceItem
from service.jobs.algorithms.write import (
    assemble_md,
    clear_today_flag,
    write_algorithm_md,
)


# ---------- fixtures ----------


def _seq_item(slug: str = "valid-anagram", number: int = 242) -> SequenceItem:
    return SequenceItem(
        slug=slug,
        number=number,
        title="Valid Anagram",
        pattern="Arrays & Hashing",
        difficulty="easy",
    )


def _normalized() -> dict:
    return {
        "slug": "valid-anagram",
        "number": 242,
        "title": "Valid Anagram",
        "difficulty": "easy",
        "tags": ["hash-table", "string", "sorting"],
        "raw_html": "<p>...</p>",
        "params": [{"name": "s", "type": "string"}, {"name": "t", "type": "string"}],
        "params_count": 2,
        "method_name": "isAnagram",
        "return_type": "boolean",
        "cases_input": ['"anagram"\n"nagaram"', '"rat"\n"car"'],
        "code": "class Solution:\n    def isAnagram(self, s, t):\n        return sorted(s) == sorted(t)\n",
        "core_lines": ["        return sorted(s) == sorted(t)"],
    }


def _i18n(ko: str = "ko", en: str = "en") -> dict:
    return {"ko": ko, "en": en}


def _llm_result(cases_n: int = 2) -> dict:
    return {
        "problem": {
            "title": _i18n("Valid Anagram", "Valid Anagram"),
            "statement": _i18n("두 문자열이 애너그램인지", "Whether two strings are anagrams"),
            "constraints": ["1 ≤ s.length ≤ 5e4"],
            "io_outputs": ["true", "false"][:cases_n],
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
                "label": _i18n("정렬·비교", "Sort and compare"),
                "indent": 0,
                "good_line_index": 0,
                "good_why": _i18n("정렬 후 동일 비교", "sort then equal"),
                "distractors": [{"code": "return s == t", "why": _i18n()}],
            }
        ],
        "trace_worked_example": {
            "input_case_index": 0,
            "steps": [_i18n("정렬", "sort"), _i18n("비교", "compare")],
            "answer": "true",
        },
        "solution": {
            "complexity": {"time": "O(n log n)", "space": "O(1)"},
            "followup": [_i18n("Hash counter 로 O(n)", "Hash counter for O(n)")],
        },
    }


TARGET_DATE = datetime.date(2026, 5, 7)


# ---------- assemble_md ----------


class TestAssembleMd:
    def test_frontmatter_keys(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        assert post.metadata["id"] == "A-002"
        assert post.metadata["type"] == "algorithm"
        assert post.metadata["date"] == "2026-05-07"
        assert post.metadata["day"] == "Day 02"
        assert post.metadata["difficulty"] == "easy"
        assert post.metadata["tags"] == ["hash-table", "string", "sorting"]
        assert post.metadata["today"] is True
        assert post.metadata["status"] == "draft"
        assert post.metadata["visible"] is True

    def test_source_block(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item("valid-anagram", 242),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        src = post.metadata["source"]
        assert src["platform"] == "leetcode"
        assert src["number"] == 242
        assert src["slug"] == "valid-anagram"
        assert src["url"] == "https://leetcode.com/problems/valid-anagram/"
        assert src["curated_in"] == ["neetcode150"]

    def test_data_block_parses(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        body = post.content
        m = re.search(r"## Data\s*\n+```yaml\n(.*?)\n```", body, re.DOTALL)
        assert m, "## Data yaml block not found"
        data = yaml.safe_load(m.group(1))
        # 6 top-level keys
        assert set(data.keys()) == {
            "problem",
            "clarifying",
            "approach",
            "logic",
            "trace",
            "solution",
        }

    def test_problem_io_pairs(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(cases_n=2),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        m = re.search(r"## Data\s*\n+```yaml\n(.*?)\n```", post.content, re.DOTALL)
        data = yaml.safe_load(m.group(1))
        io = data["problem"]["io"]
        assert len(io) == 2
        assert io[0] == {"input": '"anagram"\n"nagaram"', "output": "true"}
        assert io[1] == {"input": '"rat"\n"car"', "output": "false"}

    def test_logic_good_code_resolved(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        m = re.search(r"## Data\s*\n+```yaml\n(.*?)\n```", post.content, re.DOTALL)
        data = yaml.safe_load(m.group(1))
        slot = data["logic"]["slots"][0]
        assert slot["options"][0]["type"] == "good"
        # core_lines[0] = "        return sorted(s) == sorted(t)" → lstrip
        assert slot["options"][0]["code"] == "return sorted(s) == sorted(t)"
        # distractor 그대로
        assert slot["options"][1]["type"] == "distractor"
        assert slot["options"][1]["code"] == "return s == t"

    def test_trace_code_split_into_lines(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        m = re.search(r"## Data\s*\n+```yaml\n(.*?)\n```", post.content, re.DOTALL)
        data = yaml.safe_load(m.group(1))
        code = data["trace"]["code"]
        assert isinstance(code, list)
        assert code[0] == "class Solution:"
        assert any("def isAnagram" in line for line in code)

    def test_trace_worked_example(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
        )
        post = frontmatter.loads(md)
        m = re.search(r"## Data\s*\n+```yaml\n(.*?)\n```", post.content, re.DOTALL)
        data = yaml.safe_load(m.group(1))
        twe = data["trace"]["worked_example"]
        assert twe["input"] == '"anagram"\n"nagaram"'
        assert twe["answer"] == "true"
        assert len(twe["steps"]) == 2

    def test_today_false_param(self):
        md = assemble_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
            today=False,
        )
        post = frontmatter.loads(md)
        assert post.metadata["today"] is False


# ---------- write_algorithm_md (file IO) ----------


class TestWriteAlgorithmMd:
    def test_creates_file_at_correct_path(self, tmp_path: Path):
        path = write_algorithm_md(
            a_id="A-002",
            sequence_item=_seq_item("valid-anagram", 242),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
            persona_dir=tmp_path,
        )
        assert path == tmp_path / "algorithms" / "A-002-valid-anagram.md"
        assert path.exists()

    def test_creates_algorithms_dir(self, tmp_path: Path):
        # algorithms/ 가 없어도 자동 생성
        assert not (tmp_path / "algorithms").exists()
        write_algorithm_md(
            a_id="A-002",
            sequence_item=_seq_item(),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
            persona_dir=tmp_path,
        )
        assert (tmp_path / "algorithms").is_dir()

    def test_persona_loader_round_trip(self, tmp_path: Path):
        """써놓은 md 가 persona_loader 로 다시 읽혀서 spec-07 통과해야 함."""
        # 먼저 _meta.yaml + 최소 profile (loader 가 요구)
        from service.persona_loader import load_persona

        (tmp_path / "_meta.yaml").write_text(
            "projects:\n  categories: []\nnotes:\n  clusters: []\n", encoding="utf-8"
        )
        write_algorithm_md(
            a_id="A-002",
            sequence_item=_seq_item("valid-anagram", 242),
            normalized=_normalized(),
            llm_result=_llm_result(),
            target_date=TARGET_DATE,
            persona_dir=tmp_path,
        )
        data = load_persona(tmp_path)
        algos = data["algorithms"]
        assert len(algos) == 1
        a = algos[0]
        assert a["id"] == "A-002"
        # ## Data merge 됐는지
        assert "problem" in a
        assert "clarifying" in a
        assert "logic" in a
        assert a["logic"]["format"] == "slot"


# ---------- clear_today_flag ----------


class TestClearTodayFlag:
    def _seed(self, root: Path, items: list[tuple[str, str, bool]]) -> list[Path]:
        algos = root / "algorithms"
        algos.mkdir(parents=True, exist_ok=True)
        paths = []
        for a_id, slug, today in items:
            p = algos / f"{a_id}-{slug}.md"
            post = frontmatter.Post(
                content=f"# {slug}\n\n## Data\n\n```yaml\nfoo: bar\n```\n",
                **{
                    "id": a_id,
                    "type": "algorithm",
                    "title": {"ko": slug, "en": slug},
                    "date": "2026-05-01",
                    "source": {
                        "platform": "leetcode",
                        "number": 1,
                        "slug": slug,
                        "url": f"https://x/{slug}",
                    },
                    "difficulty": "easy",
                    "tags": ["array"],
                    "today": today,
                },
            )
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            paths.append(p)
        return paths

    def test_no_dir(self, tmp_path: Path):
        assert clear_today_flag(tmp_path) == []

    def test_flips_today_true_to_false(self, tmp_path: Path):
        paths = self._seed(
            tmp_path,
            [("A-001", "x", True), ("A-002", "y", False), ("A-003", "z", True)],
        )
        changed = clear_today_flag(tmp_path)
        # 2 개 갱신 (A-001, A-003)
        assert len(changed) == 2
        for p in paths:
            post = frontmatter.load(p)
            assert post.metadata["today"] is False

    def test_except_path_skipped(self, tmp_path: Path):
        paths = self._seed(
            tmp_path,
            [("A-001", "x", True), ("A-002", "y", True)],
        )
        # 두번째는 건너뜀 (= 방금 박은 새 파일)
        changed = clear_today_flag(tmp_path, except_path=paths[1])
        assert paths[0] in changed
        assert paths[1] not in changed
        # paths[1] 의 today 는 그대로 true
        post = frontmatter.load(paths[1])
        assert post.metadata["today"] is True
