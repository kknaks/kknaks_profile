#!/usr/bin/env python3
"""
persona/_map.md 빌드 스크립트 (spec-04 §3).

트리거:
- git pre-commit hook (사용자 PC, 옵시디언 갱신용 — spec-04 §5)
- 백엔드 부팅 (홈서버, 메모리 dict와 동시 빌드 — spec-04 §6)
- 수동 실행 (디버깅)

멱등 — timestamp 외엔 결정적 출력.

사용:
    python3 app/scripts/build_persona_map.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

try:
    import frontmatter
except ImportError:
    sys.stderr.write(
        "error: python-frontmatter 미설치. `uv pip install python-frontmatter` 또는 `pip install python-frontmatter`\n"
    )
    sys.exit(1)


REPO = Path(__file__).resolve().parents[2]
PERSONA = REPO / "persona"
MAP_PATH = PERSONA / "_map.md"
META_PATH = PERSONA / "_meta.yaml"
KST = timezone(timedelta(hours=9))
WIKILINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")


def _load_dir(category: str, recursive: bool = False) -> list:
    """persona/<category>/*.md (또는 **/*.md) 모두 frontmatter.load. path 정보도 보존.

    notes 는 recursive — 폴더 구조 (notes/<group>/<file>.md) 지원.
    notes 의 경우 frontmatter 에 type/id/group 안 박혀있어도 자동 추출:
      - id = 파일명 stem
      - group = 부모 폴더명 (notes/<group>/<file>.md 일 때)
    """
    dir_path = PERSONA / category
    if not dir_path.is_dir():
        return []
    pattern = "**/*.md" if recursive else "*.md"
    posts = []
    for md_path in sorted(dir_path.glob(pattern)):
        post = frontmatter.load(md_path)
        post.path = md_path  # type: ignore[attr-defined]
        # notes 자동 추출 (frontmatter 비어있어도 동작)
        if category == "notes":
            post.metadata.setdefault("id", md_path.stem)
            rel = md_path.relative_to(dir_path)
            if len(rel.parts) >= 2:
                post.metadata.setdefault("group", rel.parts[0])
            post.metadata.setdefault("title", md_path.stem)
        posts.append(post)
    return posts


def _i18n_label(node, lang: str = "ko") -> str:
    """{ko: "...", en: "..."} → ko 추출. scalar는 그대로."""
    if isinstance(node, dict) and lang in node:
        return node[lang]
    if isinstance(node, dict) and "ko" in node:
        return node["ko"]
    return str(node) if node is not None else ""


def _header(profile, careers, projects, notes, contents, dailies) -> str:
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    total = (
        (1 if profile else 0)
        + len(careers)
        + len(projects)
        + len(notes)
        + len(contents)
        + len(dailies)
    )
    return (
        f"# persona/_map.md\n\n"
        f"> 자동 생성 (build_persona_map.py, {now_kst}). 수동 편집 X.\n\n"
        f"_총 {total} 파일 "
        f"(profile {1 if profile else 0} / career {len(careers)} / "
        f"projects {len(projects)} / notes {len(notes)} / "
        f"contents {len(contents)} / daily {len(dailies)})_"
    )


def _section_profile(profile) -> str:
    if not profile:
        return "## profile\n\n(없음)"
    m = profile.metadata
    name = m.get("name", "(이름 미설정)")
    role = m.get("role", "")
    return f"## profile\n\n- [[profile]] {name} — {role}"


def _section_careers(careers: list) -> str:
    lines = ["## career (display_order 오름차순)"]
    if not careers:
        lines.append("\n(없음)")
        return "\n".join(lines)
    sorted_careers = sorted(
        careers, key=lambda c: c.metadata.get("display_order", 999)
    )
    for c in sorted_careers:
        m = c.metadata
        slug = c.path.stem
        org = _i18n_label(m.get("org", ""))
        period = m.get("period", "")
        lines.append(f"- [[career/{slug}]] {org} ({period})")
    return "\n".join(lines)


def _section_projects(projects: list, meta: dict) -> str:
    cat_counts = Counter(p.metadata.get("category", "") for p in projects)
    cat_summary = " · ".join(
        f"{cat['id']} {cat_counts.get(cat['id'], 0)}"
        for cat in sorted(
            meta.get("projects", {}).get("categories", []),
            key=lambda c: c.get("order", 999),
        )
    )
    lines = [f"## projects ({cat_summary or 'no categories'})"]
    if not projects:
        lines.append("\n(없음)")
        return "\n".join(lines)
    sorted_projects = sorted(
        projects,
        key=lambda p: (p.metadata.get("category", ""), p.metadata.get("date", "")),
        reverse=True,
    )
    for p in sorted_projects:
        m = p.metadata
        slug = p.path.stem
        title = _i18n_label(m.get("title", ""))
        cat = m.get("category", "")
        status = m.get("status", "")
        lines.append(f"- [[projects/{slug}]] {title} ({cat} · {status})")
    return "\n".join(lines)


def _section_notes(notes: list, meta: dict) -> str:
    grp_counts = Counter(n.metadata.get("group", "") for n in notes)
    grp_summary = " · ".join(
        f"{cl['id']} {grp_counts.get(cl['id'], 0)}"
        for cl in sorted(
            meta.get("notes", {}).get("clusters", []),
            key=lambda c: c.get("order", 999),
        )
    )
    lines = [f"## notes ({grp_summary or 'no clusters'})"]
    if not notes:
        lines.append("\n(없음)")
        return "\n".join(lines)
    sorted_notes = sorted(
        notes,
        key=lambda n: (n.metadata.get("group", ""), n.metadata.get("id", "")),
    )
    for n in sorted_notes:
        m = n.metadata
        slug = n.path.stem
        title = _i18n_label(m.get("title", ""))
        grp = m.get("group", "")
        date = m.get("date", "")
        lines.append(f"- [[notes/{slug}]] {title} ({grp} · {date})")
    return "\n".join(lines)


def _section_contents(contents: list) -> str:
    lines = [f"## contents (총 {len(contents)}개)"]
    if not contents:
        lines.append("\n(없음)")
        return "\n".join(lines)
    sorted_contents = sorted(
        contents, key=lambda c: c.metadata.get("id", ""), reverse=True
    )
    for c in sorted_contents:
        m = c.metadata
        slug = c.path.stem
        title = _i18n_label(m.get("title", ""))
        day = m.get("day", "")
        date = m.get("date", "")
        lines.append(f"- [[contents/{slug}]] {day} — {title} ({date})")
    return "\n".join(lines)


def _section_dailies(dailies: list, limit: int = 10) -> str:
    lines = [f"## daily (총 {len(dailies)}개, 최근 {limit})"]
    if not dailies:
        lines.append("\n(없음)")
        return "\n".join(lines)
    sorted_dailies = sorted(
        dailies, key=lambda d: d.metadata.get("date", ""), reverse=True
    )[:limit]
    for d in sorted_dailies:
        slug = d.path.stem
        date = d.metadata.get("date", "")
        lines.append(f"- [[daily/{slug}]] ({date})")
    return "\n".join(lines)


def _section_graph(notes: list) -> str:
    """노트 그래프 — 본문 [[id]] + frontmatter `links: [...]` 합침."""
    edges_by_source: dict[str, set[str]] = defaultdict(set)
    for n in notes:
        nid = n.metadata.get("id", n.path.stem)
        for target in WIKILINK_RE.findall(n.content):
            edges_by_source[nid].add(target)
        for target in n.metadata.get("links", []) or []:
            if target and target != nid:
                edges_by_source[nid].add(target)
    lines = ["## 위키링크 그래프 (notes)"]
    if not edges_by_source:
        lines.append("\n(위키링크 없음)")
        return "\n".join(lines)
    for source in sorted(edges_by_source):
        targets = ", ".join(sorted(edges_by_source[source]))
        lines.append(f"- {source} → {targets}")
    return "\n".join(lines)


def _section_backlinks(notes: list) -> str:
    """백링크 인덱스 — 본문 [[id]] + frontmatter `links: [...]` 둘 다 역인덱스."""
    backlinks: dict[str, set[str]] = defaultdict(set)
    for n in notes:
        nid = n.metadata.get("id", n.path.stem)
        for target in WIKILINK_RE.findall(n.content):
            backlinks[target].add(nid)
        for target in n.metadata.get("links", []) or []:
            if target and target != nid:
                backlinks[target].add(nid)
    lines = ["## 백링크 인덱스 (notes)"]
    if not backlinks:
        lines.append("\n(백링크 없음)")
        return "\n".join(lines)
    for target in sorted(backlinks):
        sources = ", ".join(sorted(backlinks[target]))
        lines.append(f"- {target}: ← {sources}")
    return "\n".join(lines)


def build_persona_map() -> str:
    """persona/_map.md 를 빌드해서 디스크에 박고, 박힌 내용을 반환."""
    if not PERSONA.is_dir():
        sys.stderr.write(f"error: {PERSONA} 디렉토리 없음\n")
        sys.exit(1)

    profile_path = PERSONA / "profile.md"
    profile = frontmatter.load(profile_path) if profile_path.exists() else None
    careers = _load_dir("career")
    projects = _load_dir("projects")
    notes = _load_dir("notes", recursive=True)
    contents = _load_dir("contents")
    dailies = _load_dir("daily")

    meta: dict = {}
    if META_PATH.exists():
        meta = yaml.safe_load(META_PATH.read_text(encoding="utf-8")) or {}

    sections = [
        _header(profile, careers, projects, notes, contents, dailies),
        _section_profile(profile),
        _section_careers(careers),
        _section_projects(projects, meta),
        _section_notes(notes, meta),
        _section_contents(contents),
        _section_dailies(dailies),
        _section_graph(notes),
        _section_backlinks(notes),
    ]

    output = "\n\n".join(sections) + "\n"
    MAP_PATH.write_text(output, encoding="utf-8")
    return output


if __name__ == "__main__":
    build_persona_map()
    print(f"built: {MAP_PATH.relative_to(REPO)}")
