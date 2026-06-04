"""GET /api/notes/* — 그래프 + recent + 상세 + 검색 (spec-02 §3.6-3.9)."""

from collections import Counter

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n, i18n
from utils.meta_helpers import build_meta_groups
from service.search import search_notes

router = APIRouter()


@router.get("/api/notes/graph")
def get_notes_graph():
    """언어 무관 — node title은 ko 기본값 박음 (spec-02 §3.6)."""
    from main import get_data

    data = get_data()
    notes: dict = data.get("notes", {})
    edges = data.get("_edges", [])
    meta_clusters = data.get("_meta", {}).get("notes", {}).get("clusters", [])

    nodes = [
        {
            "id": nid,
            "title": i18n(n.get("title", ""), "ko"),
            "group": n.get("group"),
            "stack": n.get("stack", []) or [],
        }
        for nid, n in notes.items()
    ]

    tag_counts: Counter = Counter()
    stack_counts: Counter = Counter()
    for n in notes.values():
        for tag in n.get("tags", []) or []:
            tag_counts[tag] += 1
        for s in n.get("stack", []) or []:
            stack_counts[s] += 1
    topics = [{"tag": t, "count": c} for t, c in tag_counts.most_common()]
    stacks = [{"name": s, "count": c} for s, c in stack_counts.most_common()]

    return {
        "notes": {
            "totalCount": len(notes),
            "edgeCount": len(edges),
            "graph": {
                "clusters": [
                    {
                        "id": cl["id"],
                        "label": i18n(cl.get("label"), "ko"),
                        "color": cl.get("color"),
                    }
                    for cl in sorted(
                        meta_clusters, key=lambda c: c.get("order", 999)
                    )
                ],
                "nodes": nodes,
                "edges": edges,
            },
            "topics": topics,
            "stacks": stacks,
        }
    }


@router.get("/api/notes/recent")
def get_notes_recent(
    lang: str = Query("ko", pattern="^(ko|en)$"),
    limit: int = Query(5, ge=1, le=100),
):
    from main import get_data

    notes: dict = get_data().get("notes", {})
    sorted_notes = sorted(
        notes.items(), key=lambda kv: kv[1].get("date", ""), reverse=True
    )[:limit]

    response = {
        "notes.recent[]": [
            {
                "id": nid,
                "title": n.get("title"),
                "date": n.get("date"),
                "path": n.get("group", ""),
            }
            for nid, n in sorted_notes
        ]
    }
    return apply_i18n(response, lang)


@router.get("/api/notes/search")
def search(
    q: str = Query(..., min_length=1),
    lang: str = Query("ko", pattern="^(ko|en)$"),
):
    from main import get_data

    notes: dict = get_data().get("notes", {})
    return {"notes.recent[]": search_notes(notes, q, lang)}


@router.get("/api/notes/{note_id}")
def get_note_detail(note_id: str, lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    data = get_data()
    notes: dict = data.get("notes", {})
    backlinks: dict = data.get("_backlinks", {})

    note = notes.get(note_id)
    if not note:
        raise HTTPException(404, f"note not found: {note_id}")

    bl_ids = backlinks.get(note_id, [])
    bl_entries = [
        {"id": bid, "title": notes[bid].get("title")}
        for bid in bl_ids
        if bid in notes  # dead link 무시
    ]

    response = {
        "notes.detail": {
            "id": note_id,
            "title": note.get("title"),
            "date": note.get("date"),
            "tags": note.get("tags", []),
            "stack": note.get("stack", []),
            "body": note.get("body", ""),
            "backlinks": bl_entries,
        }
    }
    return apply_i18n(response, lang)
