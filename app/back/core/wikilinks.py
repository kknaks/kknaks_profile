"""위키링크 파싱 + persona 그래프/백링크 빌더.

spec-02(notes) 계승 + KDEV-SPEC-002 §4 (그래프 스키마) 확장:
본문 `[[stem]]` / `[[stem|alias]]` / `[[folder/stem]]` 를 모두 동일 stem 으로 파싱한다.

여기서는 persona notes 용 `build_graph`(엣지 {source,target}) 와 `dead_links` 를 유지한다
(=/api/notes/graph 계약 불변). products 까지 포함한 type/dir 엣지 + L1~L6 검증은
`core.graph` 로 분리한다.
"""

from __future__ import annotations

import re
from collections import defaultdict

# 본문 `[[...]]` — 내부에 `]`/개행만 금지, alias(`|`)·경로(`/`)·대문자 허용.
# 내부 형태 검증은 _parse_target() 이 STEM_RE 로 한다 (산문 오탐 방지).
WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+?)\]\]")

# 파싱된 stem 의 허용 문자 — 영숫자 시작, 이후 영숫자/`_`/`.`/`-`. 공백 불가.
STEM_RE = re.compile(r"^[A-Za-z0-9][\w.\-]*$")

# KDEV-WORK-002 Phase 1 — 코드 영역 검출. 문법 설명용으로 적은 코드블록/인라인
# 내부의 `[[stem]]` 은 엣지가 아니다 (L1 prose 오탐 해소, KDEV-SPEC-002 §5).
# fenced 를 먼저 지우고(여러 줄·info-string 포함), 그 다음 인라인 span 을 지운다.
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def _strip_code(body: str) -> str:
    """fenced(``` ```)·inline(` `) 코드 영역을 공백으로 치환.

    공백으로 치환해 양옆 텍스트가 붙지 않게 한다 (경계 보존). 코드 밖의
    실제 `[[]]` 링크는 그대로 남는다.
    """
    body = FENCED_CODE_RE.sub(" ", body)
    body = INLINE_CODE_RE.sub(" ", body)
    return body


def _parse_target(raw: str) -> str | None:
    """`[[...]]` 내부 raw → 대상 stem.

    `stem|alias` → alias 표시는 버리고 stem. `folder/stem` → 마지막 경로 세그먼트.
    형태가 stem 규약(STEM_RE)에 안 맞으면 None (산문 `[[Foo Bar]]` 등 무시).
    """
    target = raw.split("|", 1)[0].strip()  # alias 표시 제거
    target = target.split("/")[-1].strip()  # 경로형 → 파일명 stem
    if not target or not STEM_RE.match(target):
        return None
    return target


def extract_wikilinks(body: str) -> list[str]:
    """본문에서 `[[...]]` 모두 추출 → stem 리스트 (중복 보존, 등장 순서).

    `[[stem]]`·`[[stem|alias]]`·`[[folder/stem]]` 모두 stem 으로 정규화.
    코드블록/인라인 코드 안의 `[[]]` 는 제외 (KDEV-WORK-002 Phase 1).
    """
    out: list[str] = []
    for raw in WIKILINK_RE.findall(_strip_code(body or "")):
        stem = _parse_target(raw)
        if stem is not None:
            out.append(stem)
    return out


def build_graph(notes: dict[str, dict]) -> tuple[list[dict], dict[str, list[str]]]:
    """persona notes(id→note dict, 'body' 보유) → (edges, backlinks).

    edges: [{"source": id, "target": id}, ...] — 본문 `[[…]]` (중복 제거).
    backlinks: target_id → [source_id, ...] (정렬됨).

    NOTE: /api/notes/graph 계약 유지를 위해 엣지 shape 는 {source,target} 그대로.
    products 포함 + type/dir 엣지는 `core.graph.build_knowledge_graph`.
    """
    edges_set: set[tuple[str, str]] = set()
    backlinks: dict[str, set[str]] = defaultdict(set)

    for note_id, note in notes.items():
        body = note.get("body", "")
        for target_id in extract_wikilinks(body):
            edges_set.add((note_id, target_id))
            backlinks[target_id].add(note_id)
        # frontmatter `links: [...]` (옵시디언 vault [[]] 외 명시적 박음)
        for target_id in note.get("links", []) or []:
            if target_id and target_id != note_id:
                edges_set.add((note_id, target_id))
                backlinks[target_id].add(note_id)

    edges = [{"source": s, "target": t} for s, t in sorted(edges_set)]
    backlinks_sorted = {k: sorted(v) for k, v in sorted(backlinks.items())}
    return edges, backlinks_sorted


def dead_links(notes: dict[str, dict]) -> list[tuple[str, str]]:
    """타깃이 notes에 없는 [[…]] 링크들. (source_id, target_id) 튜플 리스트."""
    note_ids = set(notes.keys())
    dead: list[tuple[str, str]] = []
    for note_id, note in notes.items():
        for target_id in extract_wikilinks(note.get("body", "")):
            if target_id not in note_ids:
                dead.append((note_id, target_id))
    return dead
