"""페르소나 yaml/md → 메모리 dict 로드 + spec-01 §6 검증 (부팅 fail-fast)."""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Any

import frontmatter
import yaml

from core.wikilinks import build_graph
from core.graph import build_knowledge_graph, validate_graph

# spec-07 §4 — 알고리즘 md 본문의 `## Data` fenced yaml 블록 추출
ALGO_DATA_BLOCK = re.compile(r"## Data\s*\n+```yaml\n(.*?)\n```", re.DOTALL)

ACTIVITY_WINDOW_DAYS = 365  # spec-01 §4 — 잔디 viz rolling 윈도우


def _normalize_date(d: Any) -> str:
    """multi-format date → 'YYYY.MM.DD'.

    yaml은 ISO date를 datetime.date로 자동 파싱. obsidian/jekyll 스타일
    'YYYY-MM-DD HH:MM:SS +0900' 같은 string도 받음.
    """
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.strftime("%Y.%m.%d")
    s = str(d).strip()
    if not s:
        return ""
    s = s.split()[0]  # 시간 부분 제거
    return s.replace("-", ".")


def _auto_enrich_note(data: dict, path: Path, persona_dir: Path) -> None:
    """notes/ 안의 .md 파일에 type/id/group 자동 채움 (frontmatter에 박혀있으면 그대로)."""
    try:
        rel = path.relative_to(persona_dir)
    except ValueError:
        return
    if not rel.parts or rel.parts[0] != "notes":
        return
    data.setdefault("type", "note")
    data.setdefault("id", path.stem)
    # notes/<group>/<file>.md → group = 부모 폴더명
    if len(rel.parts) >= 3:
        data.setdefault("group", rel.parts[1])
    # 빈 frontmatter도 동작하게 — title/date 없으면 파일에서 추출
    data.setdefault("title", path.stem)
    if "date" not in data:
        # 파일명 prefix가 'YYYY-MM-DD-...'이면 그 날짜, 아니면 빈 문자열
        stem = path.stem
        if len(stem) >= 10 and stem[4] == "-" and stem[7] == "-":
            data["date"] = stem[:10].replace("-", ".")
        else:
            data["date"] = ""

# spec-01 §3 + spec-07 §3 카테고리별 필수 필드
REQUIRED_FIELDS: dict[str, set[str]] = {
    "profile": {"type", "handle", "name", "role", "email", "tagline", "intro", "stack"},
    "career": {"type", "period", "display_order", "title", "org", "summary", "stack"},
    "project": {"type", "id", "title", "summary", "category", "status", "stack"},
    "note": {"type", "id", "title", "date", "group"},
    "content": {"type", "id", "date", "day", "title", "summary", "youtubeId"},
    "daily": {"type", "date"},
    "algorithm": {"type", "id", "title", "date", "source", "difficulty"},
}


class PersonaError(ValueError):
    """페르소나 형식 위반. 부팅 시 fail-fast."""


def load_persona(persona_dir: Path) -> dict[str, Any]:
    """persona/ 전체 로드 → in-memory dict. 위반 시 PersonaError raise.

    Returns dict with keys:
        profile        (single dict)
        career         (list, sorted by display_order asc)
        projects       (list)
        notes          (dict: id → note dict, 위키링크 lookup용)
        contents       (list, sorted by id desc)
        daily          (list, sorted by date desc)
        activity       (dict, may be empty)
        _meta          (dict)
        _edges         (list of {source, target}) — persona notes only (/api/notes/graph 계약)
        _backlinks     (dict: target_id → [source_id, ...]) — persona notes only
        _nodes         (dict: stem → node) — notes + products 결합 (지식그래프, KDEV-SPEC-002)
        _graph         (dict: nodes/edges[type,dir]/backlinks) — _graph.json 형태
        _graph_violations (list of {rule, level, node, detail}) — L1~L6 (report-only)
    """
    if not persona_dir.is_dir():
        raise PersonaError(f"persona dir not found: {persona_dir}")

    meta_path = persona_dir / "_meta.yaml"
    meta: dict = (
        yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        if meta_path.exists()
        else {}
    )

    profile_path = persona_dir / "profile.md"
    profile = _load_md(profile_path, persona_dir) if profile_path.exists() else None

    career = _load_dir(persona_dir / "career", persona_dir)
    career.sort(key=lambda c: c.get("display_order", 999))

    projects = _load_dir(persona_dir / "projects", persona_dir)
    notes_list = _load_dir(persona_dir / "notes", persona_dir, recursive=True)
    contents = _load_dir(persona_dir / "contents", persona_dir)
    contents.sort(key=lambda c: c.get("id", ""), reverse=True)
    daily = _load_dir(persona_dir / "daily")
    daily.sort(key=lambda d: d.get("date", ""), reverse=True)

    algorithms = _load_algorithms_dir(persona_dir / "algorithms", persona_dir)
    algorithms.sort(key=lambda a: a.get("date", ""), reverse=True)

    # notes는 dict로 (위키링크 id 조회 용도)
    notes: dict[str, dict] = {n["id"]: n for n in notes_list}

    # spec-01 §4 — activity 는 daily/*.md frontmatter 집계 derive (activity.yaml 폐지, ADR-06)
    activity = _derive_activity(daily)

    data: dict[str, Any] = {
        "profile": profile,
        "career": career,
        "projects": projects,
        "notes": notes,
        "contents": contents,
        "daily": daily,
        "algorithms": algorithms,
        "activity": activity,
        "_meta": meta,
    }

    validate_persona(data)

    edges, backlinks = build_graph(notes)
    data["_edges"] = edges
    data["_backlinks"] = backlinks

    # KDEV-WORK-001 — products 포함 지식그래프 + L1~L6 검증 (report-only, 절대 raise X).
    # persona 로드/notes 라우트와 분리된 신규 키. 실패해도 부팅 영향 없게 best-effort.
    try:
        products_dir = persona_dir.parent / "products"
        nodes, duplicate_stems = _build_graph_nodes(notes, products_dir)
        data["_nodes"] = nodes
        data["_graph"] = build_knowledge_graph(nodes)
        data["_graph_violations"] = validate_graph(nodes, duplicate_stems)
    except Exception as e:  # noqa: BLE001 — report-only, 부팅 차단 금지
        data["_nodes"] = {}
        data["_graph"] = {"nodes": [], "edges": [], "backlinks": {}}
        data["_graph_violations"] = []
        data["_graph_error"] = f"{type(e).__name__}: {e}"

    return data


def _build_graph_nodes(
    notes: dict[str, dict],
    products_dir: Path,
) -> tuple[dict[str, dict], list[dict]]:
    """persona notes + products `*.md` → stem→node dict + 중복 stem 위반 리스트.

    노드 식별자 = 파일명 stem (KDEV-SPEC-002 §4). 같은 stem 이 두 곳이면
    L2(SSOT 중복) 위반으로 수집하고 첫 항목을 유지(report-only).
    """
    nodes: dict[str, dict] = {}
    origin: dict[str, str] = {}  # stem → 출처 라벨 (중복 진단용)
    duplicates: list[dict] = []

    def _add(stem: str, node: dict, label: str) -> None:
        if stem in nodes:
            duplicates.append({
                "rule": "L2",
                "level": "ERROR",
                "node": stem,
                "detail": f"중복 stem '{stem}' — {origin[stem]} 와 {label} (SSOT 유일 위반)",
            })
            return
        nodes[stem] = node
        origin[stem] = label

    # persona notes (stem == id, spec-01 §6.1 강제됨)
    for nid, n in notes.items():
        _add(nid, {
            "id": n.get("id", nid),
            "type": n.get("type", "note"),
            "title": n.get("title"),
            "body": n.get("body", ""),
            "up": n.get("up"),
            "aliases": n.get("aliases"),
            "archived": bool(n.get("archived", False)),
        }, "persona/notes")

    # products/**/*.md
    if products_dir.is_dir():
        for p in sorted(products_dir.glob("**/*.md")):
            node = _load_product_node(p)
            _add(p.stem, node, str(p.relative_to(products_dir.parent)))

    return nodes, duplicates


def _load_product_node(path: Path) -> dict:
    """products `*.md` → 그래프 노드 dict (stem 은 호출부에서 path.stem)."""
    post = frontmatter.load(path)
    meta = dict(post.metadata)
    archived = (
        "_archive" in path.parts
        or meta.get("status") == "archived"
        or meta.get("archived") is True
    )
    return {
        "id": meta.get("id"),
        "type": meta.get("type"),
        "title": meta.get("title"),
        "body": post.content,
        "up": meta.get("up"),
        "aliases": meta.get("aliases"),
        "archived": archived,
        "_path": path,
    }


def validate_persona(data: dict[str, Any]) -> None:
    """spec-01 §6.1 강제 검증. 위반 시 PersonaError raise."""
    meta = data.get("_meta", {})

    if data["profile"] is not None:
        _check_required(data["profile"], "profile", "profile.md")

    for c in data["career"]:
        _check_required(c, "career", _path_label(c))

    for p in data["projects"]:
        _check_required(p, "project", _path_label(p))

    project_categories = {
        cat["id"] for cat in meta.get("projects", {}).get("categories", [])
    }
    for p in data["projects"]:
        if project_categories and p.get("category") not in project_categories:
            raise PersonaError(
                f"projects/{_path_label(p)}: category '{p.get('category')}' "
                f"not in _meta.yaml/projects.categories"
            )

    note_clusters = {
        cl["id"] for cl in meta.get("notes", {}).get("clusters", [])
    }
    for nid, n in data["notes"].items():
        _check_required(n, "note", f"notes/{nid}.md")
        # spec-01 §6.1: notes id == 파일 slug
        path: Path = n["_path"]
        if path.stem != nid:
            raise PersonaError(
                f"notes/{path.name}: frontmatter id '{nid}' != filename slug '{path.stem}'"
            )
        if note_clusters and n.get("group") not in note_clusters:
            raise PersonaError(
                f"notes/{path.name}: group '{n.get('group')}' "
                f"not in _meta.yaml/notes.clusters"
            )

    for c in data["contents"]:
        _check_required(c, "content", _path_label(c))
        # spec-01 §6.1: contents id (C-005) == 파일 prefix (C-005-...)
        path: Path = c["_path"]
        cid = c["id"]
        if not path.stem.startswith(f"{cid}-"):
            raise PersonaError(
                f"contents/{path.name}: id '{cid}' must be prefix of filename"
            )

    for d in data["daily"]:
        _check_required(d, "daily", _path_label(d))
        # spec-01 §6.1: daily date == 파일명 (점→하이픈 변환 후)
        path: Path = d["_path"]
        date_iso = str(d["date"]).replace(".", "-")
        if path.stem != date_iso:
            raise PersonaError(
                f"daily/{path.name}: date '{d['date']}' must match filename '{path.stem}'"
            )
        # spec-01 §6.1 — auto:true 면 counts (dict) + summary ({ko,en}) 모두 박혀야 함
        if d.get("auto") is True:
            counts = d.get("counts")
            if not isinstance(counts, dict):
                raise PersonaError(
                    f"daily/{path.name}: auto=true requires 'counts' dict"
                )
            summary = d.get("summary")
            if summary is not None:
                if not (
                    isinstance(summary, dict) and "ko" in summary and "en" in summary
                ):
                    raise PersonaError(
                        f"daily/{path.name}: auto=true 'summary' must be null or {{ko, en}}"
                    )
                # spec-03 §3.3 — 새 entry 는 list[str], 레거시 entry 는 str. 둘 다 통과.
                for k in ("ko", "en"):
                    v = summary[k]
                    if isinstance(v, list):
                        if not all(isinstance(x, str) for x in v):
                            raise PersonaError(
                                f"daily/{path.name}: summary.{k} list 의 모든 항목이 str 이어야 함"
                            )
                    elif not isinstance(v, str):
                        raise PersonaError(
                            f"daily/{path.name}: summary.{k} 는 str (legacy) 또는 list[str] 이어야 함"
                        )

    # spec-07 §2-3 — algorithms 검증
    valid_platforms = {"leetcode"}
    valid_quiz_formats = {"slot"}  # MVP — adr-08
    today_count = 0
    for a in data.get("algorithms", []):
        _check_required(a, "algorithm", _path_label(a))
        path: Path = a["_path"]
        aid = a["id"]
        # spec-07 §2: id (A-NNN) == 파일 prefix (A-NNN-...)
        if not path.stem.startswith(f"{aid}-"):
            raise PersonaError(
                f"algorithms/{path.name}: id '{aid}' must be prefix of filename"
            )
        # type 리터럴
        if a.get("type") != "algorithm":
            raise PersonaError(
                f"algorithms/{path.name}: type must be 'algorithm', got '{a.get('type')}'"
            )
        # source.platform enum
        src = a.get("source", {})
        if not isinstance(src, dict) or src.get("platform") not in valid_platforms:
            raise PersonaError(
                f"algorithms/{path.name}: source.platform must be one of {sorted(valid_platforms)}"
            )
        # logic.format enum (MVP slot only — ADR-08)
        logic = a.get("logic")
        if logic is not None:
            if not isinstance(logic, dict):
                raise PersonaError(f"algorithms/{path.name}: logic must be a dict")
            fmt = logic.get("format")
            if fmt not in valid_quiz_formats:
                raise PersonaError(
                    f"algorithms/{path.name}: logic.format must be one of {sorted(valid_quiz_formats)} (MVP), got '{fmt}'"
                )
        # today 는 0개 또는 1개 — spec-07 §3
        if a.get("today") is True:
            today_count += 1
    if today_count > 1:
        raise PersonaError(
            f"algorithms/: 'today: true' 항목이 여러 개 ({today_count}개) — 1개만 허용 (spec-07 §3)"
        )


def _derive_activity(daily_list: list[dict]) -> dict:
    """daily/*.md frontmatter → 잔디 viz 응답 (spec-01 §4, ADR-06).

    `count` (single) 는 `sum(counts.values())` 로 derive — 프론트 잔디 색 강도 호환.
    rolling 365 윈도우 — today 기준 cutoff 이전 entry 는 viz 에서 제외 (디스크 파일은 keep).
    """
    if not daily_list:
        return {"totalCount": 0, "since": None, "until": None, "items": []}

    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=ACTIVITY_WINDOW_DAYS - 1)
    cutoff_str = cutoff.strftime("%Y.%m.%d")

    items: list[dict] = []
    for d in sorted(daily_list, key=lambda x: x.get("date", "")):
        date_str = d.get("date", "")
        if not date_str or date_str < cutoff_str:
            continue
        counts = d.get("counts") if isinstance(d.get("counts"), dict) else {}
        items.append(
            {
                "date": date_str,
                "counts": counts,
                "count": sum(counts.values()) if counts else 0,
                "summary": d.get("summary"),
            }
        )

    if not items:
        return {"totalCount": 0, "since": None, "until": None, "items": []}

    return {
        "since": items[0]["date"],
        "until": items[-1]["date"],
        "totalCount": sum(i["count"] for i in items),
        "items": items,
    }


def _load_md(path: Path, persona_dir: Path | None = None) -> dict:
    """단일 md 파일 → dict (frontmatter + 'body' + '_path' + auto enrich).

    notes/ 안의 파일은 type/id/group 자동 채움.
    date는 multi-format 파싱 후 'YYYY.MM.DD' 정규화.
    tags 단일 string은 list로 정규화.
    """
    post = frontmatter.load(path)
    data = dict(post.metadata)
    data["body"] = post.content
    data["_path"] = path

    if persona_dir is not None:
        _auto_enrich_note(data, path, persona_dir)

    if "date" in data:
        data["date"] = _normalize_date(data["date"])

    if "tags" in data and isinstance(data["tags"], str):
        data["tags"] = [data["tags"]]

    return data


def _load_dir(
    dir_path: Path,
    persona_dir: Path | None = None,
    recursive: bool = False,
) -> list[dict]:
    if not dir_path.is_dir():
        return []
    pattern = "**/*.md" if recursive else "*.md"
    return [_load_md(p, persona_dir) for p in sorted(dir_path.glob(pattern))]


def _load_algorithms_dir(dir_path: Path, persona_dir: Path) -> list[dict]:
    """algorithms/ 전용 — frontmatter + 본문 `## Data` yaml 블록 → 합쳐서 단일 dict.

    spec-07 §4: 본문 = `## Data` 헤딩 + fenced yaml 1개. 6 최상위 키
    (problem, clarifying, approach, logic, trace, solution).
    """
    if not dir_path.is_dir():
        return []
    items: list[dict] = []
    for p in sorted(dir_path.glob("*.md")):
        item = _load_md(p, persona_dir)
        body = item.pop("body", "")

        m = ALGO_DATA_BLOCK.search(body)
        if not m:
            raise PersonaError(f"algorithms/{p.name}: ## Data yaml block missing (spec-07 §4)")

        try:
            data = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            raise PersonaError(f"algorithms/{p.name}: ## Data yaml parse error: {e}")
        if not isinstance(data, dict):
            raise PersonaError(f"algorithms/{p.name}: ## Data must be a dict, got {type(data).__name__}")

        # 6 최상위 키 (problem, clarifying, approach, logic, trace, solution) 를 item 에 merge.
        # frontmatter 와 ## Data 키는 disjoint 가정 (spec-07 §3 vs §5).
        item.update(data)
        items.append(item)
    return items


def _check_required(obj: dict, kind: str, label: str) -> None:
    required = REQUIRED_FIELDS.get(kind, set())
    missing = required - set(obj.keys())
    if missing:
        raise PersonaError(
            f"{label}: missing required field(s) for {kind}: {sorted(missing)}"
        )


def _path_label(obj: dict) -> str:
    path = obj.get("_path")
    return path.name if path else "(unknown)"
