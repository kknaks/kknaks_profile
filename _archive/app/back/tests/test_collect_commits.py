"""진짜 커밋 조사 (KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1 5~8항).

**진짜 git 위에서 돈다.** tmp 에 레포를 만들고 커밋을 심는다 — 조사 코드의 값어치는
`git log` 출력을 실제로 파싱하는 데 있어서, 가짜 출력을 넣으면 아무것도 검증되지 않는다.

여기서 고정하는 것 다섯.

    1. **전 브랜치** — feature 브랜치에만 있는 커밋이 잡힌다 (실측 17.3%)
    2. **author 날짜로 거른다** — 리베이스가 커밋터 날짜를 옮겨도 일한 날이 안 밀린다
    3. **tree 중복 제거** — 체리픽이 하루 작업을 부풀리지 않는다 (실측 163건)
    4. **머지 제외** — 남의 작업을 내 것으로 들이지 않는다
    5. **상한** — 넘으면 자르되 **자른 사실을 남긴다**
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest

from service.jobs.collect_commits import (
    collect_repo,
    dedupe_by_tree,
    identities,
    limit_commits,
    read_commits,
)

TARGET = date(2026, 7, 29)
#: KST 09:00 — 경계에서 하루가 밀리지 않는지 함께 본다.
WHEN = "2026-07-29T09:00:00+09:00"


def _git(*args: str, cwd: Path, env: dict | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True, env=env
    )
    return result.stdout.strip()


def _commit(repo: Path, name: str, body: str, *, when: str = WHEN, who: str = "kknaks") -> None:
    target = repo / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    _git("add", "-A", cwd=repo)
    _git(
        "-c", f"user.name={who}",
        "-c", f"user.email={who}@example.com",
        "commit",
        "--date", when,
        "-m", f"{name} 작업",
        cwd=repo,
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_COMMITTER_DATE": when,
            "GIT_COMMITTER_NAME": who,
            "GIT_COMMITTER_EMAIL": f"{who}@example.com",
            "HOME": str(repo.parent),
        },
    )


@pytest.fixture(autouse=True)
def patterns(monkeypatch):
    monkeypatch.setenv("COMMIT_IDENTITY_PATTERNS", "kknaks")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    path = tmp_path / "src"
    path.mkdir()
    _git("init", "-q", "-b", "main", ".", cwd=path)
    _commit(path, "app/back/api.py", "x = 1\n")
    return path


class TestReadCommits:
    def test_a_feature_branch_commit_is_found(self, repo):
        """default branch 만 보면 실측 17.3% 가 빠진다 — `--all` 이 그 이유다."""
        _git("checkout", "-q", "-b", "feature/x", cwd=repo)
        _commit(repo, "app/front/page.tsx", "export default 1\n")
        _git("checkout", "-q", "main", cwd=repo)

        found = read_commits(repo, "o/r", TARGET)
        assert {c["message"] for c in found} == {
            "app/back/api.py 작업",
            "app/front/page.tsx 작업",
        }

    def test_someone_elses_commit_is_excluded(self, repo):
        _commit(repo, "other.py", "y = 2\n", who="somebody")
        assert [c["message"] for c in read_commits(repo, "o/r", TARGET)] == [
            "app/back/api.py 작업"
        ]

    def test_another_day_is_excluded(self, repo):
        """조회 창 **안**의 다른 날. 창이 자르는 게 아니라 author 날짜가 자른다."""
        _commit(repo, "old.py", "z = 3\n", when="2026-07-28T09:00:00+09:00")
        assert [c["message"] for c in read_commits(repo, "o/r", TARGET)] == [
            "app/back/api.py 작업"
        ]

    def test_the_kst_day_boundary_holds(self, repo):
        """UTC 로 보면 전날인 시각. **KST 로 세야 그날 일이다.**"""
        _commit(repo, "late.py", "a = 1\n", when="2026-07-29T00:30:00+09:00")
        _commit(repo, "next.py", "b = 1\n", when="2026-07-30T00:30:00+09:00")
        messages = {c["message"] for c in read_commits(repo, "o/r", TARGET)}
        assert "late.py 작업" in messages
        assert "next.py 작업" not in messages

    def test_a_rebased_commit_keeps_its_author_day(self, repo):
        """**커밋터 날짜가 아니라 author 날짜로 센다.**

        리베이스는 커밋터 날짜를 오늘로 바꾼다. 그것으로 거르면 지난주 작업이
        오늘 것으로 들어오고, 잔디 칸이 실제로 일한 날과 어긋난다.
        """
        (repo / "r.py").write_text("q = 1\n", encoding="utf-8")
        _git("add", "-A", cwd=repo)
        _git(
            "-c", "user.name=kknaks", "-c", "user.email=kknaks@example.com",
            "commit", "--date", WHEN, "-m", "리베이스된 작업",
            cwd=repo,
            env={
                "PATH": "/usr/bin:/bin",
                # 커밋터는 사흘 뒤 — 리베이스가 만든 상황이다.
                "GIT_COMMITTER_DATE": "2026-08-01T11:00:00+09:00",
                "GIT_COMMITTER_NAME": "kknaks",
                "GIT_COMMITTER_EMAIL": "kknaks@example.com",
                "HOME": str(repo.parent),
            },
        )
        assert "리베이스된 작업" in {c["message"] for c in read_commits(repo, "o/r", TARGET)}

    def test_a_merge_commit_is_excluded(self, repo):
        """머지는 남의 작업을 내 것으로 들이고 증감을 부풀린다."""
        _git("checkout", "-q", "-b", "feature/y", cwd=repo)
        _commit(repo, "f.py", "m = 1\n")
        _git("checkout", "-q", "main", cwd=repo)
        _commit(repo, "g.py", "n = 1\n")
        _git(
            "-c", "user.name=kknaks", "-c", "user.email=kknaks@example.com",
            "merge", "--no-ff", "-m", "머지함", "feature/y",
            cwd=repo,
        )
        assert "머지함" not in {c["message"] for c in read_commits(repo, "o/r", TARGET)}

    def test_files_and_areas_come_along(self, repo):
        commit = read_commits(repo, "o/r", TARGET)[0]
        assert commit["files"] == [{"path": "app/back/api.py", "added": 1, "deleted": 0}]
        assert commit["areas"] == ["backend"]
        assert commit["tree"] and commit["sha"]

    def test_repo_rules_beat_the_global_default(self, repo):
        """레포별 예외가 전역보다 먼저 이겨야 예외 노릇을 한다."""
        rules = (("app/back/*", "mobile"), ("*.md", "docs"))
        assert read_commits(repo, "o/r", TARGET, rules=rules)[0]["areas"] == ["mobile"]


class TestIdentities:
    def test_only_matching_identities_are_reported(self, repo):
        _commit(repo, "other.py", "k = 1\n", who="somebody")
        assert identities(repo, TARGET) == ["kknaks <kknaks@example.com>"]


class TestDedupe:
    def test_the_same_tree_counts_once(self):
        """체리픽·리베이스가 같은 내용을 새 sha 로 되풀이한다 (실측 163건)."""
        commits = [
            {"repo": "o/r", "tree": "t1", "sha": "a"},
            {"repo": "o/r", "tree": "t1", "sha": "b"},
            {"repo": "o/r", "tree": "t2", "sha": "c"},
        ]
        assert [c["sha"] for c in dedupe_by_tree(commits)] == ["a", "c"]

    def test_the_same_tree_in_another_repo_is_kept(self):
        """키는 `(repo, tree)` 다 — 빈 커밋 등으로 레포가 겹칠 수 있다."""
        commits = [
            {"repo": "o/a", "tree": "t1", "sha": "a"},
            {"repo": "o/b", "tree": "t1", "sha": "b"},
        ]
        assert len(dedupe_by_tree(commits)) == 2


class TestLimits:
    def test_over_the_cap_keeps_the_newest(self, monkeypatch):
        monkeypatch.setenv("COMMIT_MAX_PER_REPO", "2")
        commits = [{"sha": s} for s in "abcde"]
        kept, dropped = limit_commits(commits)
        assert [c["sha"] for c in kept] == ["a", "b"]  # 이미 최신 순으로 정렬돼 있다
        assert dropped == 3

    def test_under_the_cap_drops_nothing(self, monkeypatch):
        monkeypatch.setenv("COMMIT_MAX_PER_REPO", "9")
        assert limit_commits([{"sha": "a"}]) == ([{"sha": "a"}], 0)


class TestCollectRepo:
    def test_a_normal_day_has_no_truncation(self, repo):
        commits, truncated = collect_repo(repo, "o/r", TARGET)
        assert len(commits) == 1
        assert truncated is None
        assert commits[0]["diff"]  # 본문이 붙는다 — 조사 품질의 핵심 입력이다

    def test_a_big_diff_is_cut_but_recorded(self, repo, monkeypatch):
        """**조용히 잘리면 그날 서술이 왜 얕은지 알 수 없다** (SPEC-011 S-3 3항)."""
        monkeypatch.setenv("COMMIT_DIFF_BYTES_PER_COMMIT", "200")
        _commit(repo, "big.py", "\n".join(f"line {i}" for i in range(500)))

        commits, truncated = collect_repo(repo, "o/r", TARGET)
        big = next(c for c in commits if c["message"].startswith("big.py"))
        assert big["diff_truncated"] is True
        assert truncated and truncated["diff_bytes"] > 0
        # 파일명·증감은 남는다 — 무엇을 건드렸는지는 사라지면 안 된다.
        assert big["files"][0]["path"] == "big.py"
        assert big["files"][0]["added"] == 500

    def test_the_commit_cap_is_recorded_too(self, repo, monkeypatch):
        monkeypatch.setenv("COMMIT_MAX_PER_REPO", "1")
        _commit(repo, "second.py", "s = 1\n")
        commits, truncated = collect_repo(repo, "o/r", TARGET)
        assert len(commits) == 1
        assert truncated and truncated["commits"] == 1

    def test_dedupe_runs_before_the_cap(self, repo, monkeypatch):
        """**순서가 중요하다.** 리베이스 163건이 상한 30건을 먼저 잡아먹으면
        실제 작업이 잘려 나간다."""
        monkeypatch.setenv("COMMIT_MAX_PER_REPO", "2")
        # 같은 tree 를 만드는 커밋 둘 — 되돌렸다가 다시 넣는다.
        _commit(repo, "app/back/api.py", "x = 2\n")
        _commit(repo, "app/back/api.py", "x = 1\n")  # 최초 상태 = 같은 tree
        _commit(repo, "real.py", "real = 1\n")

        commits, _ = collect_repo(repo, "o/r", TARGET)
        trees = [c["tree"] for c in commits]
        assert len(trees) == len(set(trees))
