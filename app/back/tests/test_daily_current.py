"""잔디가 `context/*/current.md` 의 「진행 중」을 갱신한다 (KDEV-DEC-022).

여기서 고정하는 것은 넷이다.

    1. 대상 판정은 **코드가** 한다 — 커밋 없는 영역·파일 없음·헤더 바뀜은 빠진다
    2. **목록이다** — 회사·개인사업자 커밋이 하루에 둘 다 있는 것이 보통이다
    3. 갱신안은 **표 본문만** 담는다. 헤더도 다른 섹션도 담기지 않는다
    4. 지금 적혀 있는 표를 모델에게 준다 — 안 주면 어제 남긴 행이 사라진다
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.models import QueueItem
from service import content_format
from service.apply.plan import build_actions, validate_plan
from service.pipeline.collect_common import context_attribution
from service.pipeline.collect_dummy import investigate_payload
from service.pipeline.gates import GateError, GenerationInput
from service.pipeline.stages.daily import DailyStage, current_targets

CURRENT_MD = """# Studio Current

## 목적

여름별컴퍼니의 운영 상태를 관리한다.  <!-- 주석도 사람의 것이다 -->

## 현재 우선순위

| Priority | Project | State |
|---|---|---|
| P0 | kknaks.dev | building |

## 진행 중

| Project | Work | Status | Blocker | Next |
|---|---|---|---|---|
| kknaks.dev | 옛 작업 | in_progress |  | 다음 |
| Wine Log | 운영 정리 | todo |  | 이슈 확인 |

## Blockers

- 아직 없다

## 운영 원칙

- 사람이 쓴다.
"""


class FakeClient:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def submit(self, prompt, *, provider, model, options, max_retries, metadata):
        self.prompts.append(prompt)
        return "okk-daily-1"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "templates" / "persona").mkdir(parents=True)
    for name in ("daily.md", "career.md"):
        (tmp_path / "templates" / "persona" / name).write_text("FORMAT", encoding="utf-8")
    (tmp_path / "templates" / "context").mkdir(parents=True)
    (tmp_path / "templates" / "context" / "current.md").write_text(
        "CURRENT-FORMAT-MARKER", encoding="utf-8"
    )
    (tmp_path / "persona" / "career").mkdir(parents=True)
    (tmp_path / "persona" / "career" / "medisolve-ai.md").write_text(
        "---\ntype: career\nis_current: true\n---\n\n## 무슨 일 하는지\n\n(TBD)\n",
        encoding="utf-8",
    )
    for area in ("company", "studio"):
        (tmp_path / "context" / area).mkdir(parents=True)
        (tmp_path / "context" / area / "current.md").write_text(
            CURRENT_MD, encoding="utf-8"
        )
    content_format.reset_cache()
    yield tmp_path
    content_format.reset_cache()


def _item(note: str = "scenario:normal") -> QueueItem:
    return QueueItem(
        source_kind="daily_commit",
        source_url=None,
        normalized_url=None,
        note=note,
        channel="manual",
        status="in_review",
    )


class _Prep:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload


def _collect(note: str = "scenario:normal") -> dict[str, Any]:
    return investigate_payload(_item(note))


def _request(note: str = "scenario:normal"):
    return GenerationInput(
        item=_item(note),
        gate=None,
        preparation=_Prep(
            {
                "collect": _collect(note),
                "investigate": {"repos": {"MediSolveAIDev/mediness": "조사문"}, "missing": []},
            }
        ),
        previous_payload=None,
        feedback=None,
        session_ref=None,
    )


def _stage(repo: Path) -> DailyStage:
    return DailyStage(
        FakeClient(), repo_root=repo, provider="claude", model=None, work_dir=None
    )


TABLE = "| Project | Work | Status | Blocker | Next |\n|---|---|---|---|---|\n| kknaks.dev | 새 작업 | in_progress |  | 다음 |"


def _reply(currents) -> str:
    return json.dumps(
        {
            "daily": {"summary": {"ko": ["[a/b] 했다"], "en": ["x"]}, "body": "본문"},
            "career": {"changed": False},
            "currents": currents,
            "concepts": [],
        },
        ensure_ascii=False,
    )


class TestContextAttribution:
    """귀속 기준은 `tracked_repos.type` 이다 — career 와 같은 값, 다른 축."""

    def test_commits_split_by_area(self):
        commits = [{"repo": "a/x"}, {"repo": "b/y"}, {"repo": "a/x"}]
        meta = {
            "a/x": {"type": "studio", "product_slug": "kknaks.dev"},
            "b/y": {"type": "company", "product_slug": None},
        }
        assert context_attribution(commits, meta) == {
            "studio": {"kknaks.dev": ["a/x"]},
            "company": {"b/y": ["b/y"]},  # 제품에 안 묶인 레포는 slug 를 쓴다
        }

    def test_unknown_type_is_dropped(self):
        """`personal` 은 커밋 축이 아니다 — 개인 영역은 사람이 쓴다."""
        commits = [{"repo": "a/x"}]
        meta = {"a/x": {"type": "personal", "product_slug": "무언가"}}
        assert context_attribution(commits, meta) == {}


class TestCurrentTargets:
    def test_both_areas_are_targets_on_a_mixed_day(self, repo: Path):
        areas = [t["area"] for t in current_targets(_collect(), repo)]
        assert areas == ["company", "studio"]

    def test_area_without_commits_is_not_a_target(self, repo: Path):
        collect = _collect()
        collect["context_map"] = {"studio": {"kknaks.dev": ["kknaks/kknaks_profile"]}}
        assert [t["area"] for t in current_targets(collect, repo)] == ["studio"]

    def test_missing_file_is_not_created(self, repo: Path):
        """`current.md` 는 사람이 세운 문서다. 없으면 만들지 않는다."""
        (repo / "context" / "studio" / "current.md").unlink()
        assert [t["area"] for t in current_targets(_collect(), repo)] == ["company"]

    def test_renamed_header_drops_the_target_instead_of_failing_the_day(self, repo: Path):
        """사람이 헤더를 바꾼 대가가 **그날 잔디 실패**여서는 안 된다.

        갱신안을 만들어 두면 발행 직전 `CURRENT_SECTION_MISSING` 으로 잔디 전체가
        거부된다 — daily 까지 같이 막힌다. 여기서 조용히 빼는 편이 낫다.
        """
        path = repo / "context" / "studio" / "current.md"
        path.write_text(CURRENT_MD.replace("## 진행 중", "## 지금 하는 일"), encoding="utf-8")
        assert [t["area"] for t in current_targets(_collect(), repo)] == ["company"]

    def test_the_existing_table_is_carried(self, repo: Path):
        """지금 뭐라고 적혀 있는지를 줘야 어제 남긴 `todo` 행이 안 사라진다."""
        target = current_targets(_collect(), repo)[0]
        assert "Wine Log" in target["current_section"]
        assert "## 진행 중" not in target["current_section"]


class TestPromptAndPayload:
    def test_format_comes_from_the_template_not_the_prompt(self, repo: Path):
        prompt = _stage(repo).prompt(_request())
        assert "CURRENT-FORMAT-MARKER" in prompt

    def test_no_target_day_asks_for_an_empty_list(self, repo: Path):
        for area in ("company", "studio"):
            (repo / "context" / area / "current.md").unlink()
        assert "current 대상이 없다" in _stage(repo).prompt(_request())

    def test_payload_carries_the_targets(self, repo: Path):
        payload = _stage(repo).payload(_request())
        assert [t["area"] for t in payload["current_targets"]] == ["company", "studio"]


class TestParse:
    def test_both_areas_survive(self, repo: Path):
        parsed = _stage(repo).parse(
            _reply(
                [
                    {"area": "company", "changed": True, "content": TABLE},
                    {"area": "studio", "changed": True, "content": TABLE},
                ]
            ),
            _request(),
        )
        assert [c["target_path"] for c in parsed["currents"]] == [
            "context/company/current.md",
            "context/studio/current.md",
        ]

    def test_area_outside_targets_is_dropped(self, repo: Path):
        """대상 판정은 코드가 했다 — 모델이 지어낸 영역은 버린다."""
        parsed = _stage(repo).parse(
            _reply([{"area": "personal", "changed": True, "content": TABLE}]),
            _request(),
        )
        assert parsed["currents"] == []

    def test_duplicate_area_keeps_the_first(self, repo: Path):
        parsed = _stage(repo).parse(
            _reply(
                [
                    {"area": "studio", "changed": True, "content": TABLE},
                    {"area": "studio", "changed": True, "content": "| 다른 |\n|---|"},
                ]
            ),
            _request(),
        )
        assert len(parsed["currents"]) == 1
        assert "새 작업" in parsed["currents"][0]["content"]

    def test_header_in_the_body_is_rejected(self, repo: Path):
        """헤더까지 담아 오면 `replace_section` 이 헤더를 한 번 더 넣는다."""
        with pytest.raises(GateError):
            _stage(repo).parse(
                _reply(
                    [{"area": "studio", "changed": True, "content": f"## 진행 중\n\n{TABLE}"}]
                ),
                _request(),
            )

    def test_missing_currents_is_not_an_error(self, repo: Path):
        """옛 초안에는 이 키가 없다 — 재시도가 그것 때문에 실패하면 안 된다."""
        assert _stage(repo).parse(_reply(None), _request())["currents"] == []


class TestPublishBothAreas:
    """계획이 **둘 다** 담는다. 하나만 담으면 그런 날 한쪽이 조용히 안 바뀐다."""

    def _grass(self):
        return {
            "daily": {
                "daily": {},
                "career": {"changed": False},
                "concepts": [],
                "currents": [
                    {
                        "changed": True,
                        "stem": area,
                        "content": TABLE,
                        "target_path": f"context/{area}/current.md",
                    }
                    for area in ("company", "studio")
                ],
            }
        }

    def test_two_actions_are_planned(self, repo: Path):
        actions = build_actions(self._grass(), repo_root=repo)
        assert [a.path for a in actions] == [
            "context/company/current.md",
            "context/studio/current.md",
        ]
        # 사람 소유 섹션은 문자 그대로 남는다.
        assert "<!-- 주석도 사람의 것이다 -->" in actions[0].content
        assert "옛 작업" not in actions[0].content and "새 작업" in actions[0].content

    def test_the_plan_passes_validation(self, repo: Path):
        actions = build_actions(self._grass(), repo_root=repo)
        assert validate_plan(actions, repo_root=repo) == []
