#!/usr/bin/env python3
"""개념 파일 ↔ area.md §3.4 맵 정합 검사기 (rules/rules.md 가 규칙 정본).

두 모드:
  --staged  (pre-commit 기본) 이 커밋에 올라오는 개념 파일만 검사한다.
            추가/이동된 개념은 staged 맵에 행이 있어야 하고,
            삭제/이동된 옛 stem 은 staged 맵에서 빠져 있어야 한다.
            기존 rot 는 막지 않는다 — 새 rot 만 막는다(백필 강제 금지).
  --all     전수 감사. 파일 ↔ 맵 양방향 + 번호 연속성까지 본다.
            백필 검증·CI 용. pre-commit 에는 걸지 않는다.

맵 행 형식: | <번호> | `<영역>` | `<stem>` | <설명> |  |
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAP_PATH = "para/areas/area.md"
CONCEPT_RE = re.compile(r"^para/areas/concept/([a-z]+)/([A-Za-z0-9._-]+)\.md$")
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*`([a-z]+)`\s*\|\s*`([^`]+)`\s*\|")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    ).stdout


def parse_map(text: str) -> dict[str, tuple[int, str]]:
    """stem → (번호, 영역). §3.4 표의 행만 줍는다."""
    rows: dict[str, tuple[int, str]] = {}
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if m:
            rows[m.group(3)] = (int(m.group(1)), m.group(2))
    return rows


def staged_mode() -> int:
    status = git("diff", "--cached", "--name-status", "-M")
    added: list[tuple[str, str]] = []    # (area, stem) — 맵에 있어야 함
    removed: list[tuple[str, str]] = []  # (area, stem) — 맵에서 빠져야 함
    for line in status.splitlines():
        parts = line.split("\t")
        code = parts[0]
        if code.startswith("R") and len(parts) == 3:
            for path, bucket in ((parts[1], removed), (parts[2], added)):
                m = CONCEPT_RE.match(path)
                if m:
                    bucket.append((m.group(1), m.group(2)))
        elif code in ("A", "D") and len(parts) == 2:
            m = CONCEPT_RE.match(parts[1])
            if m:
                (added if code == "A" else removed).append((m.group(1), m.group(2)))

    if not added and not removed:
        return 0  # 이 커밋에 개념 증감 없음 — 검사할 것 없음

    rows = parse_map(git("show", f":{MAP_PATH}"))
    errors: list[str] = []
    for area, stem in added:
        if stem not in rows:
            errors.append(
                f"개념 추가됨 `{area}/{stem}` — {MAP_PATH} §3.4 맵에 행이 없다. 한 줄 더하고 다시 커밋."
            )
        elif rows[stem][1] != area:
            errors.append(
                f"`{stem}` 의 맵 영역(`{rows[stem][1]}`)과 파일 위치(`{area}/`)가 다르다."
            )
    for area, stem in removed:
        # 이동(R)이면 added 쪽에서 새 위치를 이미 검사했다 — 같은 stem 이 남아 있으면 정상.
        if any(s == stem for _, s in added):
            continue
        if stem in rows:
            errors.append(
                f"개념 삭제됨 `{area}/{stem}` — 맵에 행이 남아 있다({rows[stem][0]}번). 행을 지우고 다시 커밋."
            )

    for e in errors:
        print(f"  ✗ {e}", file=sys.stderr)
    return 1 if errors else 0


def all_mode() -> int:
    rows = parse_map(Path(MAP_PATH).read_text())
    files: dict[str, str] = {}  # stem → area
    for p in Path("para/areas/concept").glob("*/*.md"):
        files[p.stem] = p.parent.name

    errors: list[str] = []
    for stem, area in sorted(files.items()):
        if stem not in rows:
            errors.append(f"파일만 있음: `{area}/{stem}` — 맵에 행 없음")
        elif rows[stem][1] != area:
            errors.append(f"영역 불일치: `{stem}` 맵=`{rows[stem][1]}` 파일=`{area}/`")
    for stem, (num, area) in sorted(rows.items(), key=lambda x: x[1][0]):
        if stem not in files:
            errors.append(f"맵에만 있음: {num}번 `{area}/{stem}` — 파일 없음")

    nums = sorted(num for num, _ in rows.values())
    for prev, cur in zip(nums, nums[1:]):
        if cur != prev + 1:
            errors.append(f"번호 불연속: {prev} 다음이 {cur}")

    for e in errors:
        print(f"  ✗ {e}", file=sys.stderr)
    print(f"[check-concept-map --all] 파일 {len(files)} · 맵 행 {len(rows)} · 위반 {len(errors)}")
    return 1 if errors else 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--staged"
    root = git("rev-parse", "--show-toplevel").strip()
    if not root:
        print("git 저장소가 아니다", file=sys.stderr)
        return 2
    import os

    os.chdir(root)
    if mode == "--all":
        return all_mode()
    return staged_mode()


if __name__ == "__main__":
    sys.exit(main())
