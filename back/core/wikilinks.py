"""위키링크 [[id]] 파싱 + 그래프/백링크 인덱스 빌더 (spec-02 §4.2)."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Iterable

WIKILINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")


def extract_wikilinks(body: str) -> list[str]:
    """본문에서 [[id]] 모두 추출 (중복 보존, 등장 순서)."""
    return WIKILINK_RE.findall(body or "")


def build_graph(notes: dict[str, dict]) -> tuple[list[dict], dict[str, list[str]]]:
    """notes(id→note dict, 'body' 키 보유) → (edges, backlinks).

    edges: [{"source": id, "target": id}, ...] — 등장한 모든 [[…]] (중복 제거).
    backlinks: target_id → [source_id, ...] (정렬됨).
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
