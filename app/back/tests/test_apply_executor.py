"""Apply Executor — 계획·검증·원자적 발행 (KDEV-WORK-015 P4 / KDEV-SPEC-010).

여기가 처음으로 레포에 파일이 생기는 지점이라, 이 파일의 검증은 두 가지에 집중한다.

1. **거부되면 파일이 하나도 안 생긴다** — 부분 적용은 링크가 깨진 채 origin 에 남는다.
2. **실패하면 원래 상태로 되돌아온다** — 로컬에만 남은 커밋은 다음 `/admin/reload` 의
   `git reset --hard origin/main` 이 조용히 지운다.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from service.apply.git import head_ref, publish_atomic, rollback
from service.apply.graph_check import check_graph, virtual_nodes
from service.apply.plan import FileAction, build_actions, validate_plan

REFERENCE_MD = """---
type: reference
title: 샘플 자료
date: 2026-07-28
---

# 샘플 자료

- [[sample-concept]] — 개념
"""

CONCEPT_MD = """---
type: concept
title: 샘플 개념
aliases:
  - 샘플
up:
  - 2026-07-28-sample-source
---

# 샘플 개념

## 출처

- [[2026-07-28-sample-source]] — 출처
"""


def _action(**kw) -> FileAction:
    base = dict(
        action="create",
        path="resources/source/2026-07-28-sample-source.md",
        content=REFERENCE_MD,
        note_type="reference",
        stem="2026-07-28-sample-source",
        source_gate="source_note",
    )
    return FileAction(**{**base, **kw})


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "resources/source").mkdir(parents=True)
    (tmp_path / "resources/concept").mkdir(parents=True)
    return tmp_path


class TestBuildActions:
    def test_assembles_from_approved_gates(self):
        actions = build_actions(
            {
                "source_note": {
                    "filename_stem": "2026-07-28-a-b",
                    "content": REFERENCE_MD,
                    "target_path": "resources/source/2026-07-28-a-b.md",
                },
                "concept": {
                    "concepts": [
                        {
                            "stem": "c-one",
                            "mode": "create",
                            "content": CONCEPT_MD,
                            "target_path": "resources/concept/c-one.md",
                            "excluded": False,
                        },
                        {
                            "stem": "c-two",
                            "mode": "supplement",
                            "content": CONCEPT_MD,
                            "target_path": "resources/concept/c-two.md",
                            "excluded": False,
                        },
                    ]
                },
            }
        )
        assert [a.source_gate for a in actions] == ["source_note", "concept", "concept"]
        assert [a.action for a in actions] == ["create", "create", "replace"]

    def test_excluded_concept_is_dropped(self):
        """승인 화면에서 뺀 것이 계획에도 없어야 한다."""
        actions = build_actions(
            {
                "concept": {
                    "concepts": [
                        {
                            "stem": "kept",
                            "mode": "create",
                            "content": CONCEPT_MD,
                            "target_path": "resources/concept/kept.md",
                            "excluded": False,
                        },
                        {
                            "stem": "dropped",
                            "mode": "create",
                            "content": CONCEPT_MD,
                            "target_path": "resources/concept/dropped.md",
                            "excluded": True,
                        },
                    ]
                }
            }
        )
        assert [a.stem for a in actions] == ["kept"]


class TestPathAllowlist:
    @pytest.mark.parametrize(
        "path",
        [
            "app/back/main.py",
            ".github/workflows/deploy.yml",
            "../outside.md",
            "/etc/passwd.md",
            "resources/source/../../escape.md",
            "products/kknaks-dev/log.md",
        ],
    )
    def test_outside_allowlist_rejected(self, repo, path):
        """경로 조립에 버그가 있어도 발행이 코드나 워크플로를 건드리지 못하게 한다."""
        violations = validate_plan([_action(path=path)], repo_root=repo)
        assert violations and violations[0].rule in ("PATH_NOT_ALLOWED", "PATH_SHAPE")

    def test_non_markdown_rejected(self, repo):
        assert validate_plan([_action(path="resources/source/x.txt")], repo_root=repo)

    def test_duplicate_path_in_one_publish_rejected(self, repo):
        violations = validate_plan([_action(), _action()], repo_root=repo)
        assert any(v.rule == "DUPLICATE_PATH" for v in violations)


class TestLayerPathMatch:
    def test_concept_outside_concept_dir_rejected(self, repo):
        """개념이 `resources/source/` 에 들어가면 로더가 다른 타입으로 읽는다."""
        violations = validate_plan(
            [_action(path="resources/source/x.md", content=CONCEPT_MD, note_type="concept")],
            repo_root=repo,
        )
        assert any(v.rule == "LAYER_PATH_MISMATCH" for v in violations)

    def test_permanent_in_concept_dir_rejected(self, repo):
        violations = validate_plan(
            [
                _action(
                    path="resources/concept/x.md",
                    content="---\ntype: permanent\nup:\n  - a\n---\n[[a]]",
                    note_type="permanent",
                    stem="x",
                )
            ],
            repo_root=repo,
        )
        assert any(v.rule == "LAYER_PATH_MISMATCH" for v in violations)

    def test_unknown_type_rejected(self, repo):
        violations = validate_plan(
            [_action(content="---\ntype: 몰라\n---\n본문", note_type="몰라")], repo_root=repo
        )
        assert any(v.rule == "UNKNOWN_TYPE" for v in violations)


class TestContentFilename:
    """교안은 `{id}-{slug}.md` 여야 한다 (spec-01 §6.1).

    **어기면 파일 하나가 거부되는 데서 끝나지 않는다** — 로더가 예외를 던져
    persona 로드 전체가 실패하고, 사이트는 옛 데이터를 계속 서빙한다.
    실제로 `C-023.md` 가 그렇게 나가서 콘텐츠 갱신이 멈췄다. 이 가드는 그 재발을 막는다.
    """

    def _content(self, path: str, content_id: str = "C-001"):
        return _action(
            path=path,
            content=f"---\ntype: content\nid: {content_id}\ntitle: T\n---\n본문",
            note_type="content",
            stem=path.rsplit("/", 1)[-1][:-3],
        )

    def test_bare_id_filename_rejected(self, repo):
        violations = validate_plan([self._content("persona/contents/C-001.md")], repo_root=repo)
        assert any(v.rule == "CONTENT_FILENAME" for v in violations)

    def test_id_prefixed_filename_accepted(self, repo):
        violations = validate_plan(
            [self._content("persona/contents/C-001-database-guide.md")], repo_root=repo
        )
        assert not [v for v in violations if v.rule == "CONTENT_FILENAME"]

    def test_mismatched_id_rejected(self, repo):
        """파일명 번호와 frontmatter id 가 다르면 로더가 못 읽는다."""
        violations = validate_plan(
            [self._content("persona/contents/C-002-guide.md", content_id="C-001")],
            repo_root=repo,
        )
        assert any(v.rule == "CONTENT_FILENAME" for v in violations)

    def test_missing_id_rejected(self, repo):
        violations = validate_plan(
            [
                _action(
                    path="persona/contents/C-001-guide.md",
                    content="---\ntype: content\ntitle: T\n---\n본문",
                    note_type="content",
                    stem="C-001-guide",
                )
            ],
            repo_root=repo,
        )
        assert any(v.rule == "MISSING_CONTENT_ID" for v in violations)


class TestUpAndDuplicates:
    def test_concept_without_up_rejected(self, repo):
        content = CONCEPT_MD.replace("up:\n  - 2026-07-28-sample-source\n", "")
        violations = validate_plan(
            [
                _action(
                    path="resources/concept/x.md",
                    content=content,
                    note_type="concept",
                    stem="x",
                )
            ],
            repo_root=repo,
        )
        assert any(v.rule == "MISSING_UP" for v in violations)

    def test_creating_over_existing_file_rejected(self, repo):
        (repo / "resources/source/2026-07-28-sample-source.md").write_text("기존", encoding="utf-8")
        violations = validate_plan([_action()], repo_root=repo)
        assert any(v.rule == "ALREADY_EXISTS" for v in violations)

    def test_stem_already_in_graph_rejected(self, repo):
        violations = validate_plan(
            [_action()], repo_root=repo, known_stems={"2026-07-28-sample-source"}
        )
        assert any(v.rule == "STEM_TAKEN" for v in violations)

    def test_replacing_missing_file_rejected(self, repo):
        """초안 이후 대상이 사라진 경우 — stale."""
        violations = validate_plan(
            [
                _action(
                    action="replace",
                    path="resources/concept/gone.md",
                    content=CONCEPT_MD,
                    note_type="concept",
                    stem="gone",
                )
            ],
            repo_root=repo,
        )
        assert any(v.rule == "TARGET_MISSING" for v in violations)

    def test_empty_plan_rejected(self, repo):
        assert any(v.rule == "EMPTY_PLAN" for v in validate_plan([], repo_root=repo))

    def test_valid_plan_passes(self, repo):
        actions = [
            _action(),
            _action(
                path="resources/concept/sample-concept.md",
                content=CONCEPT_MD,
                note_type="concept",
                stem="sample-concept",
                source_gate="concept",
            ),
        ]
        assert validate_plan(actions, repo_root=repo) == []


class TestVirtualGraph:
    def _actions(self):
        return [
            _action(),
            _action(
                path="resources/concept/sample-concept.md",
                content=CONCEPT_MD,
                note_type="concept",
                stem="sample-concept",
                source_gate="concept",
            ),
        ]

    def test_current_nodes_are_not_mutated(self):
        current: dict[str, dict] = {}
        virtual_nodes(current, self._actions())
        assert current == {}

    def test_valid_pair_passes(self):
        assert check_graph({}, self._actions()) == []

    def test_broken_wikilink_is_blocked(self):
        """깨진 링크가 origin 에 나가면 사람이 손으로 고쳐야 한다."""
        broken = _action(content=REFERENCE_MD.replace("sample-concept", "missing-note"))
        violations = check_graph({}, [broken])
        assert any(v.rule.startswith("GRAPH_L1") for v in violations)

    def test_prose_brackets_are_not_links(self):
        """`[[없는노트]]` 처럼 stem 규약에 안 맞는 것은 **산문**이지 링크가 아니다.

        `core/wikilinks.py` 의 `STEM_RE` 가 ASCII 로 시작하는 stem 만 링크로 본다 —
        산문 오탐을 막는 장치다. 여기서 그걸 링크로 세면 멀쩡한 문장이 dead link 가 된다.
        """
        prose = _action(content=REFERENCE_MD.replace("[[sample-concept]]", "[[없는 노트]]"))
        assert check_graph({}, [prose]) == []

    def test_concept_without_source_is_blocked(self):
        """`up:` 대상이 없으면 L1 이 잡는다 — 계보가 거짓이 된다."""
        lonely = _action(
            path="resources/concept/x.md", content=CONCEPT_MD, note_type="concept", stem="x"
        )
        assert check_graph({}, [lonely])

    def test_warnings_do_not_block(self):
        """WARN·INFO 로 발행을 막으면 아무것도 못 내보낸다 — 미소화 큐는 정상이다."""
        only_reference = _action(content="---\ntype: reference\ntitle: T\n---\n본문")
        assert check_graph({}, [only_reference]) == []


@pytest.fixture
def git_repo_with_dirs(tmp_path: Path) -> Path:
    """실 git 레포 + 발행 대상 디렉토리."""

    def run(*args):
        subprocess.run(args, cwd=tmp_path, check=True, capture_output=True)

    run("git", "init", "-b", "main")
    run("git", "config", "user.email", "t@example.com")
    run("git", "config", "user.name", "t")
    (tmp_path / "resources/source").mkdir(parents=True)
    (tmp_path / "resources/concept").mkdir(parents=True)
    (tmp_path / "seed.md").write_text("seed", encoding="utf-8")
    run("git", "add", "-A")
    run("git", "commit", "-m", "seed")
    return tmp_path


class TestAtomicGit:
    @pytest.fixture
    def git_repo(self, tmp_path: Path) -> Path:
        def run(*args):
            subprocess.run(args, cwd=tmp_path, check=True, capture_output=True)

        run("git", "init", "-b", "main")
        run("git", "config", "user.email", "t@example.com")
        run("git", "config", "user.name", "t")
        (tmp_path / "seed.md").write_text("seed", encoding="utf-8")
        run("git", "add", "-A")
        run("git", "commit", "-m", "seed")
        return tmp_path

    def test_dry_run_does_not_commit(self, git_repo):
        before = head_ref(git_repo)
        (git_repo / "new.md").write_text("x", encoding="utf-8")
        outcome = publish_atomic(["new.md"], "msg", repo_root=git_repo, dry_run=True)
        assert outcome.ok and outcome.dry_run
        assert head_ref(git_repo) == before

    def test_rollback_restores_head_and_removes_new_files(self, git_repo):
        """커밋 전 실패든 후든 origin 상태로 돌아와야 한다.

        `reset --hard` 는 untracked 를 지우지 않으므로 `clean -fd` 까지 해야 한다 —
        안 하면 다음 발행에서 `ALREADY_EXISTS` 로 막힌다.
        """
        before = head_ref(git_repo)
        (git_repo / "leftover.md").write_text("x", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=git_repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "half"], cwd=git_repo, check=True, capture_output=True
        )
        assert head_ref(git_repo) != before

        rollback(git_repo, before)

        assert head_ref(git_repo) == before
        assert not (git_repo / "leftover.md").exists()

    def test_untracked_file_is_cleaned(self, git_repo):
        before = head_ref(git_repo)
        (git_repo / "never-committed.md").write_text("x", encoding="utf-8")
        rollback(git_repo, before)
        assert not (git_repo / "never-committed.md").exists()

    def test_push_failure_leaves_no_local_commit(self, git_repo, monkeypatch):
        """로컬에만 남은 커밋은 다음 `/admin/reload` 가 조용히 지운다 — 남기면 안 된다."""
        monkeypatch.setattr(
            "config.bot_identity",
            lambda: {"user": "u", "token": "t", "email": "e@example.com"},
        )
        before = head_ref(git_repo)
        (git_repo / "will-fail.md").write_text("x", encoding="utf-8")

        # origin 이 없으므로 fetch 에서 실패한다.
        outcome = publish_atomic(
            ["will-fail.md"], "msg", repo_root=git_repo, dry_run=False
        )

        assert not outcome.ok
        assert head_ref(git_repo) == before
        assert not (git_repo / "will-fail.md").exists()

    def test_missing_identity_is_reported_not_crashed(self, git_repo, monkeypatch):
        monkeypatch.setattr("config.bot_identity", lambda: None)
        outcome = publish_atomic(["seed.md"], "msg", repo_root=git_repo, dry_run=False)
        assert not outcome.ok and outcome.error_code == "BOT_IDENTITY_MISSING"


# --- DB 까지 태운 발행 --------------------------------------------------------

import config
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as _c:
        _c.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False


@pytest.fixture
async def db():
    engine = create_async_engine(config.database_url())
    conn = await engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


@pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")
class TestApplyItem:
    async def _item_with_gates(self, db, repo: Path, *, concept_content=CONCEPT_MD):
        from core.models import Gate, GateRevision, QueueItem
        from service.pipeline import intake

        created = await intake(db, source_url="https://youtu.be/applytest1", source_kind="youtube")
        item = await db.get(QueueItem, created.item_id)
        item.status = "in_review"
        await db.flush()

        for stage, no, payload in (
            (
                "source_note",
                4,
                {
                    "filename_stem": "2026-07-28-sample-source",
                    "content": REFERENCE_MD,
                    "target_path": "resources/source/2026-07-28-sample-source.md",
                },
            ),
            (
                "concept",
                5,
                {
                    "concepts": [
                        {
                            "stem": "sample-concept",
                            "mode": "create",
                            "content": concept_content,
                            "target_path": "resources/concept/sample-concept.md",
                            "excluded": False,
                        }
                    ]
                },
            ),
        ):
            gate = Gate(item_id=item.id, stage_name=stage, stage_no=no, status="approved")
            db.add(gate)
            await db.flush()
            revision = GateRevision(
                gate_id=gate.id, version=1, status="approved", payload=payload
            )
            db.add(revision)
            await db.flush()
            gate.approved_revision_id = revision.id
        await db.flush()
        return item

    async def test_publishes_everything_in_one_commit(self, db, git_repo_with_dirs):
        from service.apply import apply_item

        repo = git_repo_with_dirs
        item = await self._item_with_gates(db, repo)
        before = head_ref(repo)

        outcome = await apply_item(
            db, item, repo_root=repo, current_nodes={}, dry_run=True
        )

        assert outcome.ok, outcome.violations or outcome.error_message
        # dry_run 이라 커밋은 안 되지만 파일은 작업트리에 쓰인다.
        assert (repo / "resources/source/2026-07-28-sample-source.md").exists()
        assert (repo / "resources/concept/sample-concept.md").exists()
        assert head_ref(repo) == before
        assert item.status == "published"

    async def test_rejected_plan_writes_nothing(self, db, git_repo_with_dirs):
        """부분 적용은 링크가 깨진 채 origin 에 남는다 — 하나라도 걸리면 전부 안 쓴다."""
        from service.apply import apply_item

        repo = git_repo_with_dirs
        broken = CONCEPT_MD.replace("up:\n  - 2026-07-28-sample-source\n", "")
        item = await self._item_with_gates(db, repo, concept_content=broken)

        outcome = await apply_item(
            db, item, repo_root=repo, current_nodes={}, dry_run=True
        )

        assert outcome.status == "rejected"
        assert any(v["rule"] == "MISSING_UP" for v in outcome.violations)
        # reference 는 멀쩡했지만 그것도 안 쓴다.
        assert not (repo / "resources/source/2026-07-28-sample-source.md").exists()
        assert not (repo / "resources/concept/sample-concept.md").exists()
        assert item.status == "publish_failed"

    async def test_retry_reuses_plan_without_ai(self, db, git_repo_with_dirs):
        """발행 재시도는 AI 를 다시 부르지 않는다 — 저장된 계획으로 다시 쓴다(DEC-012 D5)."""
        from core.models import ApplyPlan, ApplyResult
        from service.apply import apply_item, latest_plan

        repo = git_repo_with_dirs
        broken = CONCEPT_MD.replace("up:\n  - 2026-07-28-sample-source\n", "")
        item = await self._item_with_gates(db, repo, concept_content=broken)
        await apply_item(db, item, repo_root=repo, current_nodes={}, dry_run=True)

        plan = await latest_plan(db, item.id)
        assert plan is not None
        # 게이트를 손대지 않고 계획만 고쳐 재시도한다 — 생성기는 호출되지 않는다.
        plan.file_actions = [
            {
                "action": "create",
                "path": "resources/source/2026-07-28-sample-source.md",
                "content": REFERENCE_MD,
                "note_type": "reference",
                "stem": "2026-07-28-sample-source",
                "source_gate": "source_note",
            },
            {
                "action": "create",
                "path": "resources/concept/sample-concept.md",
                "content": CONCEPT_MD,
                "note_type": "concept",
                "stem": "sample-concept",
                "source_gate": "concept",
            },
        ]
        await db.flush()

        outcome = await apply_item(
            db, item, repo_root=repo, current_nodes={}, dry_run=True, plan=plan
        )
        assert outcome.ok
        # 계획은 새로 만들어지지 않는다.
        plans = (await db.scalars(select(ApplyPlan).where(ApplyPlan.item_id == item.id))).all()
        assert len(plans) == 1
        # 실패 기록은 지워지지 않는다.
        results = (
            await db.scalars(select(ApplyResult).where(ApplyResult.item_id == item.id))
        ).all()
        assert [r.status for r in results] == ["rejected", "succeeded"]

    async def test_commit_message_lists_what_went_out(self, db, git_repo_with_dirs):
        from service.apply.executor import approved_payloads, commit_message
        from service.apply.plan import build_actions

        item = await self._item_with_gates(db, git_repo_with_dirs)
        actions = build_actions(await approved_payloads(db, item.id))
        message = commit_message(item, actions)

        assert message.startswith(f"knowledge: publish item #{item.id}")
        assert "concept:1" in message and "reference:1" in message
        assert "resources/source/2026-07-28-sample-source.md" in message
        assert "https://youtu.be/applytest1" in message
