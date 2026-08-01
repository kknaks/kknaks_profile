"""`daily` 게이트 스테이지 (KDEV-WORK-017 P2 / KDEV-SPEC-012·013).

여기서 고정하는 것은 넷이다.

    1. 형식은 `templates/persona/` 에서 실려 온다 — 프롬프트에 복사돼 있지 않다
    2. `counts` 는 코드가 넣는다 — AI 출력의 숫자를 쓰지 않는다
    3. career 는 **결정적으로** 빠진다 — 대상 판정이 모델 출력보다 앞선다
    4. 대상이 아닌데 모델이 career 를 지어내면 버린다
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.models import QueueItem
from service import content_format
from service.pipeline.collect_dummy import investigate_payload
from service.pipeline.gates import GateError, GenerationInput
from service.pipeline.stages.daily import BODY_HARD_LIMIT, DailyStage, career_targets


class FakeClient:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    async def submit(self, prompt, *, provider, model, options, max_retries, metadata):
        self.prompts.append(prompt)
        return "okk-daily-1"


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
        status="in_review",
    )


class _Prep:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload


def _prep_payload(note: str = "scenario:normal") -> dict[str, Any]:
    return {
        "collect": investigate_payload(_item(note)),
        "investigate": {"repos": {"MediSolveAIDev/mediness": "조사문"}, "missing": []},
    }


def _request(note: str = "scenario:normal", *, feedback=None, previous=None):
    return GenerationInput(
        item=_item(note),
        gate=None,
        preparation=_Prep(_prep_payload(note)),
        previous_payload=previous,
        feedback=feedback,
        session_ref=None,
    )


def _stage(client, repo: Path) -> DailyStage:
    return DailyStage(client, repo_root=repo, provider="claude", model=None, work_dir=None)


def _reply(**overrides) -> str:
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


class TestCareerTargets:
    def test_current_company_target_is_selected(self, repo):
        assert [t["stem"] for t in career_targets(_prep_payload()["collect"], repo)] == [
            "medisolve-ai"
        ]

    def test_studio_only_day_has_no_target(self, repo):
        """`type=studio` 만 커밋한 날은 career 갱신안이 없다 (SPEC-012 AC)."""
        collect = _prep_payload("scenario:studio_only")["collect"]
        assert career_targets(collect, repo) == []

    def test_not_current_career_is_skipped(self, repo):
        """끝난 재직 기간을 오늘 커밋으로 고치지 않는다."""
        assert career_targets({"career_map": {"quantus": ["r"]}}, repo) == []

    def test_missing_file_is_skipped(self, repo):
        assert career_targets({"career_map": {"ghost": ["r"]}}, repo) == []


class TestPrompt:
    def test_format_is_loaded_from_templates_not_copied(self, repo):
        """형식 명세가 프롬프트에 **복사돼 있지 않다** — 파일에서 실려 온다."""
        prompt = _stage(FakeClient(), repo).prompt(_request())
        assert "DAILY-FORMAT-MARKER" in prompt
        assert "CAREER-FORMAT-MARKER" in prompt

    def test_prompt_forbids_ai_counting(self, repo):
        assert "코드가 채운다" in _stage(FakeClient(), repo).prompt(_request())

    def test_no_target_tells_the_model_to_return_null(self, repo):
        prompt = _stage(FakeClient(), repo).prompt(_request("scenario:studio_only"))
        assert "null" in prompt


class TestPayload:
    def test_existing_career_body_travels_as_input(self, repo):
        """전문 교체라 기존 본문을 줘야 한다 — 없으면 append 가 된다."""
        payload = _stage(FakeClient(), repo).payload(_request())
        assert payload["career_targets"][0]["current_body"].strip().startswith("##")

    def test_repo_reports_come_from_investigate(self, repo):
        payload = _stage(FakeClient(), repo).payload(_request())
        assert payload["repo_reports"] == {"MediSolveAIDev/mediness": "조사문"}

    def test_feedback_and_previous_draft_travel_on_regeneration(self, repo):
        """재생성은 조사를 다시 돌리지 않고 서술만 다시 만든다 (SPEC-013 S-3)."""
        request = _request(feedback="회사 서술을 덜어내라", previous={"daily": {}})
        payload = _stage(FakeClient(), repo).payload(request)
        assert payload["feedback"] == "회사 서술을 덜어내라"
        assert payload["previous_draft"] == {"daily": {}}
        # 조사 결과가 그대로 실린다 — 다시 돌지 않았다는 뜻이다.
        assert payload["repo_reports"]

    def test_studio_only_day_carries_no_career_target(self, repo):
        payload = _stage(FakeClient(), repo).payload(_request("scenario:studio_only"))
        assert payload["career_targets"] == []


class TestParse:
    def test_counts_come_from_collect_not_the_model(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = _reply(
            daily={
                "summary": {"ko": [], "en": []},
                "body": "본문",
                "counts": {"commit": 999, "note": 999, "study": 999},
            }
        )
        assert stage.parse(reply, _request())["daily"]["counts"]["commit"] == 3

    def test_the_collection_status_reaches_the_screen(self, repo):
        """조사가 온전했는지는 **승인 화면이 보는 payload** 에 있어야 한다.

        프롬프트에는 이미 실려 있었지만(`payload()`), 사람이 보는 것은 `parse()` 의
        결과다. 여기 없으면 서술이 얕을 때 자료 부족인지 그날 일이 적어서인지
        구분할 방법이 없다.
        """
        stage = _stage(FakeClient(), repo)
        request = _request()
        request.preparation.payload["investigate"] = {
            "repos": {"a/one": "조사문"},
            "missing": ["b/two"],
        }
        request.preparation.payload["collect"]["failures"] = [
            {"repo": "c/three", "code": "FETCH_FAILED", "message": "권한 없음"}
        ]
        request.preparation.payload["collect"]["truncated"] = {"a/one": {"commits": 30}}

        collection = stage.parse(_reply(), request)["collection"]
        assert collection["done"] == 1
        assert collection["total"] == 2  # 조사한 것 + 결과가 안 온 것
        assert collection["missing"] == ["b/two"]
        assert collection["failed"][0]["repo"] == "c/three"
        assert "a/one" in collection["truncated"]

    def test_a_clean_run_still_carries_the_status(self, repo):
        """빠진 것이 없어도 값은 온다 — 화면이 "전부 조사됨" 을 그릴 수 있어야 한다."""
        collection = _stage(FakeClient(), repo).parse(_reply(), _request())["collection"]
        assert collection == {
            "done": 1,
            "total": 1,
            "missing": [],
            "failed": [],
            "truncated": {},
        }

    def test_body_over_the_hard_limit_is_cut(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = _reply(
            daily={"summary": {"ko": [], "en": []}, "body": "가" * (BODY_HARD_LIMIT + 500)}
        )
        assert len(stage.parse(reply, _request())["daily"]["body"]) == BODY_HARD_LIMIT

    def test_blank_summary_lines_are_dropped(self, repo):
        """활동이 0인 카테고리는 줄이 없어야 한다 — 빈 줄이 셀 카드에 뜬다."""
        stage = _stage(FakeClient(), repo)
        reply = _reply(
            daily={"summary": {"ko": ["[a] 있음", "  "], "en": ["[a] yes"]}, "body": "b"}
        )
        assert stage.parse(reply, _request())["daily"]["summary"]["ko"] == ["[a] 있음"]

    def test_paths_are_assembled_by_the_system(self, repo):
        """경로를 모델에 맡기지 않는다 — allowlist 밖으로 쓰는 계획이 나온다."""
        payload = _stage(FakeClient(), repo).parse(_reply(), _request())
        date = payload["daily"]["date"]
        assert payload["daily"]["target_path"] == f"persona/daily/{date}.md"
        assert payload["career"]["target_path"] == "persona/career/medisolve-ai.md"

    def test_career_is_dropped_when_there_was_no_target(self, repo):
        """대상이 없는데 모델이 지어내면 버린다."""
        stage = _stage(FakeClient(), repo)
        assert stage.parse(_reply(), _request("scenario:studio_only"))["career"] == {
            "changed": False
        }

    def test_career_for_an_unlisted_stem_is_dropped(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = _reply(career={"changed": True, "stem": "quantus", "content": "x"})
        assert stage.parse(reply, _request())["career"] == {"changed": False}

    def test_career_survives_when_the_target_matches(self, repo):
        career = _stage(FakeClient(), repo).parse(_reply(), _request())["career"]
        assert career["changed"] is True and career["stem"] == "medisolve-ai"

    def test_changed_false_is_a_normal_answer(self, repo):
        stage = _stage(FakeClient(), repo)
        assert stage.parse(_reply(career={"changed": False}), _request())["career"] == {
            "changed": False
        }

    def test_concepts_without_content_are_dropped(self, repo):
        stage = _stage(FakeClient(), repo)
        reply = _reply(
            concepts=[
                {"stem": "ok", "title": "T", "content": "---\ntype: concept\ntitle: T\naliases:\n  - t\nup:\n  - parent\n---\n\n본문", "mode": "supplement"},
                {"stem": "empty", "title": "T", "content": "   "},
                "쓰레기",
            ]
        )
        concepts = stage.parse(reply, _request())["concepts"]
        assert [c["stem"] for c in concepts] == ["ok"]
        assert concepts[0]["mode"] == "supplement"
        assert concepts[0]["target_path"] == "permanent/concept/ok.md"

    def test_fenced_json_is_accepted(self, repo):
        stage = _stage(FakeClient(), repo)
        assert stage.parse(f"```json\n{_reply()}\n```", _request())["daily"]["body"] == "본문"

    def test_non_json_fails_loudly(self, repo):
        with pytest.raises(GateError):
            _stage(FakeClient(), repo).parse("그냥 산문", _request())

    def test_bad_summary_shape_fails(self, repo):
        """로더가 {ko, en} list[str] 을 강제한다 — 여기서 막지 않으면 발행 뒤에 터진다."""
        stage = _stage(FakeClient(), repo)
        reply = _reply(daily={"summary": {"ko": "문자열", "en": []}, "body": "b"})
        with pytest.raises(GateError):
            stage.parse(reply, _request())


class TestSubmit:
    async def test_submit_sends_prompt_and_material(self, repo):
        client = FakeClient()
        task_id = await _stage(client, repo).submit(_request())
        assert task_id == "okk-daily-1"
        assert "DAILY-FORMAT-MARKER" in client.prompts[0]
        assert "current_body" in client.prompts[0]

    def test_concept_mode_matches_the_youtube_gate(self, repo):
        """`create` 여야 한다 — `new` 면 승인 화면의 ConceptList 가 잘못 렌더한다.

        같은 컴포넌트를 재사용하므로 두 게이트가 같은 값을 써야 하고, 발행부의
        create/replace 분기도 그 규약 위에 있다.
        """
        stage = _stage(FakeClient(), repo)
        reply = _reply(
            concepts=[{"stem": "s", "title": "T", "content": "---\ntype: concept\ntitle: T\naliases:\n  - t\nup:\n  - parent\n---\n\n본문", "mode": "new"}]
        )
        assert stage.parse(reply, _request())["concepts"][0]["mode"] == "create"
