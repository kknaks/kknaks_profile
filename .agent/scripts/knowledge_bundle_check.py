#!/usr/bin/env python3
"""resources/ 묶음 검사 — 개념 노트의 dead link 와 별칭 규칙만 본다.

`validate_graph` 는 전체 레포 L1~L6 을 보지만 부팅에서 부르는 곳이 없고(KDEV 208be61
에서 그래프 표면 제거), 실데이터를 그대로 넣으면 daily·버전 디렉토리에서 잡음이 크게
난다. 스터디 노트 이관은 **한 출처 묶음이 닫혔는지**만 알면 되므로 그 범위만 검사한다.

    python3 .agent/scripts/knowledge_bundle_check.py [출처_stem]

출처 stem 을 주면 그 묶음(출처 + 그것을 `up:` 하는 개념)만, 안 주면 resources/ 전체.
종료코드 0 = 통과, 1 = 위반.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[\[([^\]|#]+)")
FENCE = re.compile(r"```.*?```|`[^`]*`", re.S)


def notes() -> dict[str, dict]:
    """레포 전체의 frontmatter 노트. 링크 타겟은 resources/ 밖에도 있을 수 있다."""
    skip = {".git", "node_modules", ".venv", "__pycache__", "inbox", "templates"}
    out: dict[str, dict] = {}
    for p in ROOT.rglob("*.md"):
        if any(s in p.parts for s in skip) or not p.name.endswith(".md"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---\n"):
            continue
        _, fm, body = text.split("---", 2)
        out[p.stem] = {"fm": fm, "body": body, "path": p.relative_to(ROOT)}
    return out


def field(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None


def listfield(fm: str, key: str) -> list[str]:
    m = re.search(rf"^{key}:\s*\n((?:\s+-\s+.*\n)+)", fm, re.M)
    if m:
        return [ln.strip()[2:].strip().strip("\"'") for ln in m.group(1).splitlines()]
    inline = field(fm, key)
    if inline and inline.startswith("["):
        return [x.strip().strip("\"'") for x in inline[1:-1].split(",") if x.strip()]
    return []


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else None
    all_notes = notes()

    # 링크가 풀리는 이름: stem + aliases
    resolvable = set(all_notes)
    for n in all_notes.values():
        resolvable.update(listfield(n["fm"], "aliases"))

    scope = {
        stem: n
        for stem, n in all_notes.items()
        if str(n["path"]).startswith("resources/") and n["path"].name != "README.md"
    }
    if target:
        scope = {
            stem: n
            for stem, n in scope.items()
            if stem == target or target in listfield(n["fm"], "up")
        }
        if not scope:
            print(f"묶음 없음: {target}")
            return 1

    bad: list[str] = []
    for stem, n in sorted(scope.items()):
        fm, body = n["fm"], n["body"]
        targets = set(LINK.findall(FENCE.sub("", body))) | set(listfield(fm, "up"))
        for t in sorted(targets):
            if t.strip() not in resolvable:
                bad.append(f"L1 dead link  {stem} → [[{t.strip()}]]")

        if field(fm, "type") != "concept":
            continue
        if not listfield(fm, "up"):
            bad.append(f"출처 누락      {stem} → up: 비어 있음")

    label = f"{target} 묶음" if target else "resources/ 전체"
    print(f"{label} — 노트 {len(scope)}건, 위반 {len(bad)}건")
    for b in bad:
        print(f"  {b}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
