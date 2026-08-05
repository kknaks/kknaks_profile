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


def twin_basenames(all_notes: dict[str, dict]) -> dict[str, list[str]]:
    """stem 이 같은 레포 내 다른 `.md` 를 찾는다.

    `notes()` 의 skip 목록에 든 디렉토리(`templates/` 등)는 링크 해산 대상이
    아니지만 **옵시디언은 그것도 본다.** `resources/concept/reference.md` 와
    `templates/knowledge/reference.md` 처럼 부딪히면 `[[reference]]` 가 어느
    쪽으로 풀릴지 모호해진다 — 검사기가 링크는 통과시켜도 옵시디언에서 깨지는
    자리라 별도로 잡는다.
    """
    skip = {".git", "node_modules", ".venv", "__pycache__"}
    out: dict[str, list[str]] = {}
    for p in ROOT.rglob("*.md"):
        if any(s in p.parts for s in skip):
            continue
        if p.stem not in all_notes:
            continue
        rel = str(p.relative_to(ROOT))
        known = str(all_notes[p.stem]["path"])
        if rel != known:
            out.setdefault(p.stem, []).append(rel)
    return out


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else None
    all_notes = notes()

    # 링크가 풀리는 이름: stem + aliases
    resolvable = set(all_notes)
    for n in all_notes.values():
        resolvable.update(listfield(n["fm"], "aliases"))

    twins = twin_basenames(all_notes)

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
        links = set(LINK.findall(FENCE.sub("", body)))
        ups = listfield(fm, "up")
        targets = links | set(ups)
        for t in sorted(targets):
            if t.strip() not in resolvable:
                bad.append(f"L1 dead link  {stem} → [[{t.strip()}]]")

        if field(fm, "type") != "concept":
            continue
        if not ups:
            bad.append(f"출처 누락      {stem} → up: 비어 있음")

        # L3 — `up:` 은 본문 링크의 부분집합이어야 한다(오버레이). 본문이 엣지의 단일
        # 소스이고 `up:` 은 그중 계보인 것을 마킹하는 것이므로, 본문에 없는 `up:` 은
        # 계보를 주장하면서 근거를 대지 않는 상태다. 개념 성장 때 「출처」줄 추가를
        # 빠뜨리면 정확히 이 모양이 되고, 링크는 살아 있어 L1 으로는 안 잡힌다.
        for u in ups:
            if u.strip() not in links:
                bad.append(f"L3 up 미기재    {stem} → up: {u.strip()} 이 본문 [[]] 에 없음")

        # 옵시디언은 basename 으로 링크를 푼다. skip 목록(templates 등) 밖의
        # 같은 이름 파일과 부딪히면 [[stem]] 이 어느 쪽인지 모호해진다 —
        # 링크 해산 범위에는 넣지 않으면서 이름 충돌만 잡는다.
        for other in twins.get(stem, ()):
            bad.append(f"이름 충돌      {stem} ↔ {other} (옵시디언에서 [[{stem}]] 이 모호)")

    label = f"{target} 묶음" if target else "resources/ 전체"
    print(f"{label} — 노트 {len(scope)}건, 위반 {len(bad)}건")
    for b in bad:
        print(f"  {b}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
