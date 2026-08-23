"""bare 클론에서 하루치 커밋을 읽는다 (KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1 5~8항).

**git 만 읽는다.** DB 도 Slack 도 모르고, 스테이지 조립은 `pipeline/collect_git.py` 가
한다. 여기서 나오는 것은 SPEC-011 §4 「조사 산출물」의 `commits[]` 한 조각이다.

세 가지가 이 모듈의 존재 이유다.

    전 브랜치   `--all`. default branch 만 보면 실측 17.3%(본인 7.9%)가 빠진다
    중복 제거   `(repo, tree)`. 리베이스가 같은 작업을 새 sha 로 되풀이한다 (실측 163건)
    입력 상한   레포당 32KB · 커밋당 8KB · 커밋 30건. 넘으면 **버린 사실을 남긴다**
"""

from __future__ import annotations

import logging
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import config
from service.pipeline.collect_common import KST, area_for

logger = logging.getLogger("kknaks-back.collect-commits")

#: 레코드/필드 구분자. 커밋 메시지에 무엇이 들어 있어도 파싱이 깨지지 않게 한다 —
#: 개행이나 파이프로 나누면 메시지 본문이 그 자리를 차지할 수 있다.
_RS = "\x1e"
_FS = "\x1f"
_FORMAT = f"{_RS}%H{_FS}%T{_FS}%an <%ae>{_FS}%aI{_FS}%s"


def _run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=config.git_timeout_seconds(),
    )
    if result.returncode != 0:
        logger.warning("git 실패 (%s): %s", " ".join(args[:2]), (result.stderr or "")[:200])
        return ""
    return result.stdout


def _author_args() -> list[str]:
    """`--author` 는 부분매칭이고 여러 개면 OR 다 (SPEC-011 §4 「author 매칭」).

    고정 email 목록을 쓰지 않는다 — identity 는 늘어나고, 목록을 쓰면 **새 identity 가
    조용히 빠진다.** 대신 빠지는 대신 남이 섞일 수 있어서 `identities()` 로 감시한다.
    """
    return [f"--author={p}" for p in config.commit_identity_patterns()]


def window(target: date) -> tuple[str, str]:
    """git 에 넘길 조회 창 — **대상 날짜보다 넓다.**

    `--since`/`--until` 은 **커밋터 날짜**로 거르는데 우리가 세고 싶은 것은 **일한 날**,
    곧 author 날짜다. 리베이스는 커밋터 날짜를 오늘로 바꾸므로 좁게 자르면 며칠 전
    작업이 오늘 것으로 들어오거나 그 반대가 된다. **넓게 받아서 author 날짜로 정확히
    거른다**(`_in_kst_day`).

    ⚠ 창 밖으로 밀려난 리베이스는 여전히 놓친다 — 기본 7일이면 실무에서 충분하다는
    가정이고, 그 가정이 깨지면 `COMMIT_DATE_SLACK_DAYS` 를 늘린다.

    ⚠ `--since` 는 필터가 아니라 **탐색 중단점**이기도 하다. HEAD 자체가 창보다
    오래되면 git 이 거기서 걸음을 멈춰 그 조상들을 아예 보지 않는다. 실제 레포는
    HEAD 가 늘 가장 새 커밋이라 문제되지 않지만, 창을 좁히면 그 가정에 기대게 된다.
    """
    slack = timedelta(days=config.commit_date_slack_days())
    since = datetime.combine(target, datetime.min.time(), KST) - slack
    until = datetime.combine(target + timedelta(days=1), datetime.min.time(), KST) + slack
    return since.isoformat(), until.isoformat()


def _in_kst_day(author_iso: str, target: date) -> bool:
    try:
        return datetime.fromisoformat(author_iso).astimezone(KST).date() == target
    except ValueError:
        return False


def read_commits(
    path: Path, slug: str, target: date, *, rules: tuple[tuple[str, str], ...] | None = None
) -> list[dict[str, Any]]:
    """대상 날짜(KST)의 본인 커밋. 파일 목록과 증감 라인까지 붙인다.

    **머지 커밋은 세지 않는다.** 남의 작업을 내 것으로 들이는 데다 `--numstat` 이
    합쳐진 diff 를 내놓아 증감이 부풀려진다. 머지가 한 일은 그 안의 커밋들이 이미
    말하고 있다.
    """
    since, until = window(target)
    raw = _run(
        [
            "log",
            "--all",
            "--no-merges",
            "--numstat",
            f"--since={since}",
            f"--until={until}",
            *_author_args(),
            f"--pretty=format:{_FORMAT}",
        ],
        path,
    )
    commits: list[dict[str, Any]] = []
    for chunk in raw.split(_RS):
        if not chunk.strip():
            continue
        head, _, rest = chunk.partition("\n")
        parts = head.split(_FS)
        if len(parts) < 5:
            continue
        sha, tree, author, authored, subject = parts[:5]
        if not _in_kst_day(authored, target):
            continue
        files = _numstat(rest)
        commits.append(
            {
                "repo": slug,
                "sha": sha,
                "tree": tree,
                "author": author,
                "authored_at": authored,
                "message": subject,
                "files": files,
                "areas": sorted({area_for(f["path"], rules) for f in files}),
            }
        )
    # 최신 순으로 못박는다 — 상한에 걸려 자를 때 **오래된 것부터** 버려야 하고,
    # git 의 기본 순서(커밋터 날짜)는 리베이스가 흔들어 놓는다.
    commits.sort(key=lambda c: c["authored_at"], reverse=True)
    return commits


def _numstat(block: str) -> list[dict[str, Any]]:
    """`--numstat` 블록 → `[{path, added, deleted}]`.

    바이너리는 `-` 로 나온다 — 0 으로 세되 파일은 남긴다. 무엇을 건드렸는지는
    증감이 없어도 서술에 쓰인다.
    """
    files: list[dict[str, Any]] = []
    for line in block.splitlines():
        cols = line.split("\t")
        if len(cols) != 3:
            continue
        added, deleted, name = cols
        files.append(
            {
                "path": name.strip(),
                "added": 0 if added == "-" else int(added or 0),
                "deleted": 0 if deleted == "-" else int(deleted or 0),
            }
        )
    return files


def identities(path: Path, target: date) -> list[str]:
    """그날 패턴에 걸린 `name <email>` 목록 — drift 판정용 (SPEC-011 S-2).

    **패턴에 걸린 것만 본다.** 남의 커밋은 애초에 안 들어오므로 여기 뜨는 미등록
    identity 는 "내 것인데 등록을 안 했다" 이거나 "패턴이 너무 넓어 남을 물었다"
    둘 중 하나다. 어느 쪽이든 사람이 봐야 한다.
    """
    since, until = window(target)
    raw = _run(
        [
            "log",
            "--all",
            "--no-merges",
            f"--since={since}",
            f"--until={until}",
            *_author_args(),
            "--pretty=format:%an <%ae>",
        ],
        path,
    )
    return sorted({line.strip() for line in raw.splitlines() if line.strip()})


def dedupe_by_tree(commits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """`(repo, tree)` 중복 제거 (SPEC-011 §4 — 실측 163건).

    리베이스·체리픽은 **같은 내용**을 새 sha 로 되풀이한다. sha 로 세면 하루 작업이
    부풀고, 그 숫자가 그대로 잔디 칸과 요약에 들어간다.
    """
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for commit in commits:
        key = (str(commit.get("repo")), str(commit.get("tree")))
        if key in seen:
            continue
        seen.add(key)
        out.append(commit)
    return out


def attach_diffs(path: Path, commits: list[dict[str, Any]]) -> dict[str, int]:
    """커밋마다 diff 본문을 붙이고 상한을 적용한다 (SPEC-011 S-3).

    **파일명·증감 라인은 절대 버리지 않는다.** 버리는 것은 본문뿐이고, 그래야
    "무엇을 건드렸는지" 는 남은 채 "어떻게 고쳤는지" 만 사라진다.

    상한에 걸린 사실을 돌려준다 — **조용히 잘리면 그날 서술이 왜 얕은지 알 수 없다.**
    """
    per_commit = config.commit_diff_bytes_per_commit()
    per_repo = config.commit_diff_bytes_per_repo()
    used = 0
    hit = {"diff_bytes": 0, "commits": 0}

    for commit in commits:
        if used >= per_repo:
            hit["commits"] += 1
            continue
        body = _run(["show", "--format=", "--no-color", str(commit["sha"])], path)
        raw = body.encode("utf-8")
        budget = min(per_commit, per_repo - used)
        if len(raw) > budget:
            commit["diff"] = raw[:budget].decode("utf-8", errors="ignore")
            commit["diff_truncated"] = True
            hit["diff_bytes"] += len(raw) - budget
            used += budget
        else:
            commit["diff"] = body
            used += len(raw)
    return hit


def limit_commits(commits: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """커밋 수 상한. 넘으면 **최신 순으로** 남기고 버린 수를 돌려준다."""
    cap = config.commit_max_per_repo()
    if len(commits) <= cap:
        return commits, 0
    return commits[:cap], len(commits) - cap


def collect_repo(
    path: Path, slug: str, target: date, *, rules: tuple[tuple[str, str], ...] | None = None
) -> tuple[list[dict[str, Any]], dict[str, int] | None]:
    """레포 하나의 하루치. 조사 → 중복 제거 → 상한 → diff.

    순서가 중요하다. **중복 제거를 상한보다 먼저** 한다 — 리베이스 163건이 상한
    30건을 통째로 잡아먹으면 실제 작업이 잘려 나간다.
    """
    commits = dedupe_by_tree(read_commits(path, slug, target, rules=rules))
    commits, dropped = limit_commits(commits)
    hit = attach_diffs(path, commits)
    hit["commits"] += dropped
    truncated = hit if (hit["diff_bytes"] or hit["commits"]) else None
    return commits, truncated
