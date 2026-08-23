"""더미 커밋 조사 (KDEV-WORK-017 P2 / KDEV-SPEC-011 §4).

여기서 고정하는 것은 둘이다.

    1. **계약을 통째로 낸다** — 키가 하나라도 빠지면 P5 교체가 `collect` 밖으로 번진다
    2. 집계는 진짜다 — 지어내는 것은 `commits[]` 뿐이고 영역·counts·귀속은 실물 코드다
"""

from __future__ import annotations

import pytest

from core.models import QueueItem
from service.pipeline.collect_dummy import (
    SCENARIOS,
    DummyCollect,
    area_for,
    career_attribution,
    decompose,
    has_activity,
    investigate_payload,
    pick_scenario,
    target_date,
)

#: SPEC-011 §4 「Data Contract — 조사 산출물」 이 요구하는 키 전부.
CONTRACT_KEYS = {
    "commits",
    "areas",
    "career_map",
    "counts",
    "truncated",
    "failures",
    "identities",
}


def _item(note: str = "", normalized_url: str | None = None) -> QueueItem:
    return QueueItem(
        source_kind="daily_commit",
        source_url=None,
        normalized_url=normalized_url,
        note=note,
        channel="manual",
        status="received",
    )


class TestContract:
    @pytest.mark.parametrize("name", sorted(SCENARIOS))
    def test_every_scenario_emits_the_whole_contract(self, name):
        """시나리오가 무엇이든 계약은 온전하다 — 하류가 진짜와 구분하지 못해야 한다."""
        payload = investigate_payload(_item(f"scenario:{name}"))
        assert CONTRACT_KEYS <= set(payload)

    def test_commit_entries_carry_every_field(self):
        payload = investigate_payload(_item("scenario:normal"))
        for commit in payload["commits"]:
            assert {"repo", "sha", "tree", "message", "files", "areas"} <= set(commit)
            for f in commit["files"]:
                assert {"path", "added", "deleted"} <= set(f)


class TestAggregation:
    def test_area_rules_follow_the_spec(self):
        assert area_for("app/back/service/x.py") == "backend"
        assert area_for("app/front/src/App.tsx") == "frontend"
        assert area_for("products/kknaks-dev/log.md") == "docs"
        assert area_for("README.md") == "docs"
        assert area_for("docker-compose.yml") == "infra"
        assert area_for("Dockerfile.back") == "infra"
        assert area_for("weird/path.bin") == "other"

    def test_a_commit_spanning_areas_is_counted_in_each(self):
        """SPEC-011 — 영역마다 계상한다. 그래서 counts["commit"] 과 합계가 다르다."""
        commits = [
            {
                "repo": "r",
                "files": [
                    {"path": "app/back/a.py", "added": 10, "deleted": 1},
                    {"path": "README.md", "added": 2, "deleted": 0},
                ],
            }
        ]
        areas = decompose(commits)
        assert areas["backend"]["commits"] == 1
        assert areas["docs"]["commits"] == 1
        assert sum(a["commits"] for a in areas.values()) != len(commits)

    def test_same_area_twice_in_one_commit_counts_once(self):
        commits = [
            {
                "repo": "r",
                "files": [
                    {"path": "app/back/a.py", "added": 3, "deleted": 0},
                    {"path": "app/back/b.py", "added": 4, "deleted": 2},
                ],
            }
        ]
        areas = decompose(commits)
        assert areas["backend"] == {"commits": 1, "added": 7, "deleted": 2}

    def test_counts_come_from_code_not_ai(self):
        payload = investigate_payload(_item("scenario:normal"))
        assert payload["counts"]["commit"] == len(payload["commits"])


class TestCareerAttribution:
    def test_company_commits_map_to_a_real_career_stem(self):
        payload = investigate_payload(_item("scenario:normal"))
        assert list(payload["career_map"]) == ["medisolve-ai"]

    def test_studio_only_produces_no_career_target(self):
        """`type=studio` 만 커밋한 날은 career 갱신안이 없다 (SPEC-012 AC)."""
        payload = investigate_payload(_item("scenario:studio_only"))
        assert payload["career_map"] == {}
        assert payload["counts"]["commit"] == 1

    def test_attribution_ignores_unknown_repos(self):
        assert career_attribution([{"repo": "someone/else", "files": []}]) == {}


class TestScenarios:
    def test_partial_failure_keeps_commits_and_records_the_failure(self):
        payload = investigate_payload(_item("scenario:partial_failure"))
        assert payload["commits"]
        assert payload["failures"][0]["code"] == "FETCH_FAILED"

    def test_all_failed_has_no_commits_but_still_has_activity(self):
        """전 레포가 실패해도 노트가 있으면 진행한다 (SPEC-011 S-5 3항)."""
        payload = investigate_payload(_item("scenario:all_failed"))
        assert payload["commits"] == []
        assert len(payload["failures"]) == 4
        assert has_activity(payload)

    def test_truncated_records_the_cap_hit(self):
        """조용히 잘리면 그날 서술이 왜 얕은지 알 수 없다 (SPEC-011 S-3 3항)."""
        payload = investigate_payload(_item("scenario:truncated"))
        assert payload["truncated"]["MediSolveAIDev/mediness"]["diff_bytes"] == 32768

    def test_empty_is_no_activity(self):
        payload = investigate_payload(_item("scenario:empty"))
        assert not has_activity(payload)

    def test_unknown_scenario_falls_back_to_normal(self):
        assert pick_scenario(_item("scenario:does_not_exist")) == "normal"
        assert pick_scenario(_item("")) == "normal"


class TestTargetDate:
    def test_synthetic_key_decides_the_date(self):
        assert target_date(_item(normalized_url="daily:2026-07-29")) == "2026-07-29"

    def test_without_a_key_it_falls_back_to_yesterday(self):
        assert target_date(_item()) is not None


class TestStageContract:
    async def test_collect_submits_nothing_to_the_executor(self):
        """조사는 생성이 아니다 — 실행기 큐에 넣지 않는다."""
        submission = await DummyCollect().submit(item=_item("scenario:normal"), prior={})
        assert submission.task_refs == []
        assert submission.error_code is None
        assert set(submission.payload["collect"]) >= CONTRACT_KEYS

    async def test_no_activity_blocks_the_stage(self):
        submission = await DummyCollect().submit(item=_item("scenario:empty"), prior={})
        assert submission.error_code == "NO_ACTIVITY"
