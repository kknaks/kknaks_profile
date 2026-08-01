"""잔디 발행부 확장 (KDEV-WORK-017 P3 / KDEV-SPEC-012·013).

여기서 고정하는 것은 넷이다.

    1. `upsert` 는 파일이 있든 없든 통과한다 — 매일 액션 종류가 갈리지 않는다
    2. `daily`·`career` 는 그래프 검증에서 빠지고 `concept` 는 받는다
    3. 본인이 쓴 daily 를 덮어쓰지 않는다
    4. career 는 **본문만** 바뀐다 — 사람 전용 필드는 건드릴 방법이 없다
"""

from __future__ import annotations

from pathlib import Path

import frontmatter
import pytest

from service.apply.graph_check import check_graph, graph_actions
from service.apply.plan import (
    FileAction,
    build_actions,
    render_career,
    render_daily,
    validate_plan,
)

CAREER_EXISTING = """---
type: career
period: "2026.02 — present"
display_order: 1
is_current: true
title:
  ko: "백엔드 개발자"
org:
  ko: "메디솔브 AI"
summary:
  ko: "요약"
stack:
  - Python
bullets:
  ko:
    - "이력서 문장 1"
---

## 무슨 일 하는지

(TBD — 사용자 채움)
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "persona" / "daily").mkdir(parents=True)
    (tmp_path / "persona" / "career").mkdir(parents=True)
    (tmp_path / "persona" / "career" / "medisolve-ai.md").write_text(
        CAREER_EXISTING, encoding="utf-8"
    )
    return tmp_path


def _gate_payload(**overrides):
    payload = {
        "daily": {
            "date": "2026-08-01",
            "counts": {"commit": 3, "note": 1, "study": 0},
            "summary": {"ko": ["[a/b] 했다"], "en": ["[a/b] did"]},
            "body": "# 한 일\n\n서술",
            "target_path": "persona/daily/2026-08-01.md",
        },
        "career": {"changed": False},
        "concepts": [],
    }
    payload.update(overrides)
    return {"daily": payload}


class TestRenderDaily:
    def test_date_uses_dots_to_match_the_loader(self):
        """로더가 파일명(하이픈)과 대조한다 — 어긋나면 persona 로드 전체가 실패한다."""
        meta = frontmatter.loads(render_daily(_gate_payload()["daily"]["daily"])).metadata
        assert meta["date"] == "2026.08.01"

    def test_counts_and_auto_are_system_owned(self):
        meta = frontmatter.loads(render_daily(_gate_payload()["daily"]["daily"])).metadata
        assert meta["auto"] is True
        assert meta["type"] == "daily"
        assert meta["counts"] == {"commit": 3, "note": 1, "study": 0}

    def test_summary_and_body_pass_through_untouched(self):
        post = frontmatter.loads(render_daily(_gate_payload()["daily"]["daily"]))
        assert post.metadata["summary"]["ko"] == ["[a/b] 했다"]
        assert post.content.strip() == "# 한 일\n\n서술"


class TestRenderCareer:
    def test_existing_frontmatter_survives(self):
        """사람 전용 필드는 **건드릴 방법 자체가 없다** — 본문만 갈아 끼운다."""
        rendered = render_career({"content": "## 무슨 일 하는지\n\n새 서술"}, CAREER_EXISTING)
        meta = frontmatter.loads(rendered).metadata
        assert meta["bullets"]["ko"] == ["이력서 문장 1"]
        assert meta["period"] == "2026.02 — present"
        assert meta["is_current"] is True

    def test_body_is_replaced(self):
        rendered = render_career({"content": "## 무슨 일 하는지\n\n새 서술"}, CAREER_EXISTING)
        assert "새 서술" in frontmatter.loads(rendered).content
        assert "TBD" not in frontmatter.loads(rendered).content


class TestBuildActions:
    def test_daily_is_an_upsert(self, repo):
        """첫 회 생성과 덮어쓰기가 둘 다 정상이다 (SPEC-013)."""
        actions = build_actions(_gate_payload(), repo_root=repo)
        assert [a.action for a in actions] == ["upsert"]
        assert actions[0].path == "persona/daily/2026-08-01.md"
        assert actions[0].note_type == "daily"

    def test_career_is_a_replace_carrying_old_frontmatter(self, repo):
        actions = build_actions(
            _gate_payload(
                career={
                    "changed": True,
                    "stem": "medisolve-ai",
                    "content": "## 무슨 일 하는지\n\n새 서술",
                    "target_path": "persona/career/medisolve-ai.md",
                }
            ),
            repo_root=repo,
        )
        career = next(a for a in actions if a.note_type == "career")
        assert career.action == "replace"
        assert frontmatter.loads(career.content).metadata["bullets"]

    def test_changed_false_makes_no_career_action(self, repo):
        actions = build_actions(_gate_payload(), repo_root=repo)
        assert all(a.note_type != "career" for a in actions)

    def test_concepts_from_the_daily_gate_are_included(self, repo):
        actions = build_actions(
            _gate_payload(
                concepts=[
                    {
                        "stem": "fan-out",
                        "content": "---\ntype: concept\nup: x\n---\n\n본문",
                        "mode": "new",
                        "target_path": "permanent/concept/fan-out.md",
                    }
                ]
            ),
            repo_root=repo,
        )
        assert any(a.note_type == "concept" and a.action == "create" for a in actions)


class TestValidate:
    def _daily_action(self, repo, *, body="본문") -> FileAction:
        payload = _gate_payload()["daily"]["daily"]
        payload["body"] = body
        content = render_daily(payload)
        return FileAction(
            action="upsert",
            path="persona/daily/2026-08-01.md",
            content=content,
            note_type="daily",
            stem="2026-08-01",
            source_gate="daily",
        )

    def test_grass_paths_are_allowed(self, repo):
        assert validate_plan([self._daily_action(repo)], repo_root=repo) == []

    def test_upsert_passes_when_the_file_already_exists(self, repo):
        """같은 날 두 번 승인해도 `ALREADY_EXISTS` 가 나오지 않는다."""
        (repo / "persona" / "daily" / "2026-08-01.md").write_text(
            render_daily(_gate_payload()["daily"]["daily"]), encoding="utf-8"
        )
        assert validate_plan([self._daily_action(repo)], repo_root=repo) == []

    def test_layer_mismatch_is_caught(self, repo):
        action = self._daily_action(repo)
        action.path = "reference/2026-08-01.md"
        rules = {v.rule for v in validate_plan([action], repo_root=repo)}
        assert "LAYER_PATH_MISMATCH" in rules

    def test_user_authored_daily_is_refused(self, repo):
        """접수 뒤에 사람이 직접 쓴 경합을 여기서 잡는다 (SPEC-013 S-6)."""
        (repo / "persona" / "daily" / "2026-08-01.md").write_text(
            "---\ntype: daily\nauto: false\ndate: 2026.08.01\n---\n\n내가 씀",
            encoding="utf-8",
        )
        rules = {v.rule for v in validate_plan([self._daily_action(repo)], repo_root=repo)}
        assert "USER_AUTHORED_DAILY" in rules

    def test_daily_without_auto_key_is_also_the_users(self, repo):
        (repo / "persona" / "daily" / "2026-08-01.md").write_text(
            "---\ntype: daily\ndate: 2026.08.01\n---\n\n옛 파일", encoding="utf-8"
        )
        rules = {v.rule for v in validate_plan([self._daily_action(repo)], repo_root=repo)}
        assert "USER_AUTHORED_DAILY" in rules

    def test_our_own_daily_can_be_overwritten(self, repo):
        (repo / "persona" / "daily" / "2026-08-01.md").write_text(
            "---\ntype: daily\nauto: true\ndate: 2026.08.01\n---\n\n어제 우리가 씀",
            encoding="utf-8",
        )
        assert validate_plan([self._daily_action(repo)], repo_root=repo) == []

    def test_career_losing_required_fields_is_refused(self, repo):
        """로더 필수 필드가 빠지면 persona 로드 전체가 실패한다."""
        action = FileAction(
            action="replace",
            path="persona/career/medisolve-ai.md",
            content="---\ntype: career\n---\n\n## 무슨 일\n\n본문",
            note_type="career",
            stem="medisolve-ai",
            source_gate="daily",
        )
        rules = {v.rule for v in validate_plan([action], repo_root=repo)}
        assert "PROTECTED_FIELD" in rules

    def test_career_replace_needs_an_existing_target(self, repo):
        action = FileAction(
            action="replace",
            path="persona/career/ghost.md",
            content=CAREER_EXISTING,
            note_type="career",
            stem="ghost",
            source_gate="daily",
        )
        rules = {v.rule for v in validate_plan([action], repo_root=repo)}
        assert "TARGET_MISSING" in rules

    def test_daily_does_not_need_up(self, repo):
        """그래프 밖이라 상류가 없다 — `up:` 검사를 받지 않는다."""
        rules = {v.rule for v in validate_plan([self._daily_action(repo)], repo_root=repo)}
        assert "MISSING_UP" not in rules


class TestGraphExclusion:
    def _action(self, note_type: str, path: str, content: str) -> FileAction:
        return FileAction(
            action="upsert",
            path=path,
            content=content,
            note_type=note_type,
            stem="x",
            source_gate="daily",
        )

    def test_daily_and_career_are_not_graph_nodes(self):
        actions = [
            self._action("daily", "persona/daily/a.md", "---\ntype: daily\n---\n"),
            self._action("career", "persona/career/b.md", "---\ntype: career\n---\n"),
            self._action(
                "concept", "permanent/concept/c.md", "---\ntype: concept\nup: x\n---\n"
            ),
        ]
        assert [a.note_type for a in graph_actions(actions)] == ["concept"]

    def test_graph_check_ignores_grass_output(self):
        """얹으면 상류가 없어 고아로 걸린다 — 빼는 것이 사실의 반영이다."""
        actions = [
            self._action("daily", "persona/daily/a.md", "---\ntype: daily\n---\n"),
            self._action("career", "persona/career/b.md", "---\ntype: career\n---\n"),
        ]
        assert check_graph({}, actions) == []
