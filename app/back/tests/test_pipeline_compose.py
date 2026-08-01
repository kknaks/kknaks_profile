"""취합 스테이지 (KDEV-WORK-017 P2 / KDEV-SPEC-012).

여기서 고정하는 것은 넷이다.

    1. 형식은 `templates/persona/` 에서 실려 온다 — 프롬프트에 복사돼 있지 않다
    2. `counts` 는 코드가 넣는다 — AI 출력의 숫자를 쓰지 않는다
    3. career 는 **결정적으로** 빠진다 — 대상이 없으면 AI 를 부르기도 전에
    4. 대상이 없는데 AI 가 career 를 지어내면 버린다
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.models import QueueItem
from service import content_format
from service.pipeline.collect_dummy import investigate_payload
from service.pipeline.stages.compose import (
    BODY_HARD_LIMIT,
    AgentCompose,
    build_prompt,
    career_targets,
)


class FakeClient:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def submit(self, prompt, *, provider, model, options, max_retries, metadata):
        self.prompts.append(prompt)
        return "okk-compose-1"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """템플릿과 career 문서를 갖춘 최소 레포."""
    (tmp_path / "templates" / "persona").mkdir(parents=True)
    (tmp_path / "templates" / "persona" / "daily.md").write_text(
        "DAILY-FORMAT-MARKER", encoding="utf-8"
    )
    (tmp_path / "templates" / "persona" / "career.md").write_text(
        "CAREER-FORMAT-MARKER", encoding="utf-8"
    )
    (tmp_path / "persona" / "career").mkdir(parents=True)
    (tmp_path / "persona" / "career" / "medisolve-ai.md").write_text(
        "---\ntype: career\nis_current: true\n---\n\n## 무슨 일 하는지\n\n(TBD)\n",
        encoding="utf-8",
    )
    (tmp_path / "persona" / "career" / "quantus.md").write_text(
        "---\ntype: career\nis_current: false\n---\n\n## 무슨 일 하는지\n\n끝난 곳\n",
        encoding="utf-8",
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
        status="preparing",
    )


def _prior(note: str = "scenario:normal", **extra: Any) -> dict[str, Any]:
    prior = {
        "collect": investigate_payload(_item(note)),
        "investigate": {"repos": {"MediSolveAIDev/mediness": "조사문"}, "missing": []},
    }
    prior.update(extra)
    return prior


def _stage(client, repo: Path) -> AgentCompose:
    return AgentCompose(
        client, provider="claude", model=None, work_dir=None, repo_root=repo
    )


class TestCareerTargets:
    def test_current_company_target_is_selected(self, repo):
        targets = career_targets(_prior()["collect"], repo)
        assert [t["stem"] for t in targets] == ["medisolve-ai"]

    def test_studio_only_day_has_no_target(self, repo):
        """`type=studio` 만 커밋한 날은 career 갱신안이 없다 (SPEC-012 AC)."""
        assert career_targets(_prior("scenario:studio_only")["collect"], repo) == []

    def test_not_current_career_is_skipped(self, repo):
        """끝난 재직 기간을 오늘 커밋으로 고치지 않는다."""
        collect = {"career_map": {"quantus": ["MediSolveAIDev/mediness"]}}
        assert career_targets(collect, repo) == []

    def test_missing_file_is_skipped(self, repo):
        collect = {"career_map": {"ghost": ["r"]}}
        assert career_targets(collect, repo) == []


class TestPrompt:
    def test_format_is_loaded_from_templates_not_copied(self, repo):
        """형식 명세가 프롬프트에 **복사돼 있지 않다** — 파일에서 실려 온다."""
        prompt = build_prompt(
            collect=_prior()["collect"],
            investigate=_prior()["investigate"],
            targets=career_targets(_prior()["collect"], repo),
            repo_root=repo,
        )
        assert "DAILY-FORMAT-MARKER" in prompt
        assert "CAREER-FORMAT-MARKER" in prompt

    def test_prompt_forbids_ai_counting(self, repo):
        prompt = build_prompt(
            collect=_prior()["collect"],
            investigate={},
            targets=[],
            repo_root=repo,
        )
        assert "counts" in prompt and "코드가 채운다" in prompt

    def test_existing_career_body_travels_as_input(self, repo):
        """전문 교체라 기존 본문을 줘야 한다 — 없으면 append 가 된다."""
        prompt = build_prompt(
            collect=_prior()["collect"],
            investigate={},
            targets=career_targets(_prior()["collect"], repo),
            repo_root=repo,
        )
        assert "current_body" in prompt

    def test_no_target_tells_the_model_to_return_null(self, repo):
        prompt = build_prompt(
            collect=_prior("scenario:studio_only")["collect"],
            investigate={},
            targets=[],
            repo_root=repo,
        )
        assert "null" in prompt


class TestParse:
    def _reply(self, **overrides) -> str:
        data = {
            "daily": {
                "summary": {"ko": ["[a/b] 했다"], "en": ["[a/b] did"]},
                "body": "본문",
            },
            "career": {"changed": True, "stem": "medisolve-ai", "content": "## 무슨 일\n\n새 서술"},
            "concepts": [],
        }
        data.update(overrides)
        return json.dumps(data, ensure_ascii=False)

    def test_counts_come_from_collect_not_the_model(self, repo):
        stage = _stage(FakeClient(), repo)
        prior = _prior(compose_targets=["medisolve-ai"])
        reply = self._reply(
            daily={
                "summary": {"ko": [], "en": []},
                "body": "본문",
                "counts": {"commit": 999, "note": 999, "study": 999},
            }
        )

        piece = stage.parse({"r": reply}, item=_item(), prior=prior)

        assert piece["compose"]["daily"]["counts"] == prior["collect"]["counts"]
        assert piece["compose"]["daily"]["counts"]["commit"] == 3

    def test_body_over_the_hard_limit_is_cut(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = self._reply(
            daily={"summary": {"ko": [], "en": []}, "body": "가" * (BODY_HARD_LIMIT + 500)}
        )
        piece = stage.parse({"r": reply}, item=_item(), prior=_prior())
        assert len(piece["compose"]["daily"]["body"]) == BODY_HARD_LIMIT

    def test_blank_summary_lines_are_dropped(self, repo):
        """활동이 0인 카테고리는 줄이 없어야 한다 — 빈 줄이 셀 카드에 뜬다."""
        stage = _stage(FakeClient(), repo)
        reply = self._reply(
            daily={"summary": {"ko": ["[a] 있음", "  "], "en": ["[a] yes"]}, "body": "b"}
        )
        piece = stage.parse({"r": reply}, item=_item(), prior=_prior())
        assert piece["compose"]["daily"]["summary"]["ko"] == ["[a] 있음"]

    def test_career_is_dropped_when_there_was_no_target(self, repo):
        """대상이 없는데 모델이 지어내면 버린다."""
        stage = _stage(FakeClient(), repo)
        prior = _prior(compose_targets=[])
        piece = stage.parse({"r": self._reply()}, item=_item(), prior=prior)
        assert piece["compose"]["career"] == {"changed": False}

    def test_career_for_an_unlisted_stem_is_dropped(self, repo):
        stage = _stage(FakeClient(), repo)
        prior = _prior(compose_targets=["someone-else"])
        piece = stage.parse({"r": self._reply()}, item=_item(), prior=prior)
        assert piece["compose"]["career"] == {"changed": False}

    def test_career_survives_when_the_target_matches(self, repo):
        stage = _stage(FakeClient(), repo)
        prior = _prior(compose_targets=["medisolve-ai"])
        piece = stage.parse({"r": self._reply()}, item=_item(), prior=prior)
        assert piece["compose"]["career"]["changed"] is True
        assert piece["compose"]["career"]["stem"] == "medisolve-ai"

    def test_changed_false_is_a_normal_answer(self, repo):
        stage = _stage(FakeClient(), repo)
        prior = _prior(compose_targets=["medisolve-ai"])
        piece = stage.parse(
            {"r": self._reply(career={"changed": False})}, item=_item(), prior=prior
        )
        assert piece["compose"]["career"] == {"changed": False}

    def test_concepts_without_content_are_dropped(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = self._reply(
            concepts=[
                {"stem": "ok", "title": "T", "content": "본문", "mode": "supplement"},
                {"stem": "empty", "title": "T", "content": "   "},
                "쓰레기",
            ]
        )
        piece = stage.parse({"r": reply}, item=_item(), prior=_prior())
        assert [c["stem"] for c in piece["compose"]["concepts"]] == ["ok"]
        assert piece["compose"]["concepts"][0]["mode"] == "supplement"

    def test_fenced_json_is_accepted(self, repo):
        stage = _stage(FakeClient(), repo)
        piece = stage.parse(
            {"r": f"```json\n{self._reply()}\n```"}, item=_item(), prior=_prior()
        )
        assert piece["compose"]["daily"]["body"] == "본문"

    def test_non_json_fails_loudly(self, repo):
        stage = _stage(FakeClient(), repo)
        with pytest.raises(RuntimeError):
            stage.parse({"r": "그냥 산문"}, item=_item(), prior=_prior())

    def test_bad_summary_shape_fails(self, repo):
        """로더가 {ko, en} list[str] 을 강제한다 — 여기서 막지 않으면 발행 뒤에 터진다."""
        stage = _stage(FakeClient(), repo)
        reply = self._reply(daily={"summary": {"ko": "문자열", "en": []}, "body": "b"})
        with pytest.raises(ValueError):
            stage.parse({"r": reply}, item=_item(), prior=_prior())


class TestSubmit:
    async def test_target_list_is_recorded_at_submit(self, repo):
        client = FakeClient()
        submission = await _stage(client, repo).submit(item=_item(), prior=_prior())
        assert submission.payload["compose_targets"] == ["medisolve-ai"]
        assert len(submission.task_refs) == 1

    async def test_studio_only_day_records_no_target(self, repo):
        client = FakeClient()
        submission = await _stage(client, repo).submit(
            item=_item("scenario:studio_only"), prior=_prior("scenario:studio_only")
        )
        assert submission.payload["compose_targets"] == []
