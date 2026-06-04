"""GET /api/projects — 프로젝트 (spec-02 §3.5). categories는 _meta + 자동 count."""

from fastapi import APIRouter, Query

from core.i18n import apply_i18n
from utils.meta_helpers import build_meta_groups

router = APIRouter()


@router.get("/api/projects")
def get_projects(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    data = get_data()
    # spec-01 §3.3 — visible: false 박힌 항목은 사이트 미표시 (잔디 잡 추적은 별도 — extract_tracked_repos 가 다 봄)
    items = [p for p in data.get("projects", []) if p.get("visible", True)]
    meta_categories = data.get("_meta", {}).get("projects", {}).get("categories", [])

    response = {
        "projects": {
            "subtitle": {"ko": "혼자 만든 것들", "en": "Things I built alone"},
            "totalCount": len(items),
            "categories": build_meta_groups(meta_categories, items, "category", lang),
        },
        "projects[]": [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "summary": p.get("summary"),
                "category": p.get("category"),
                "status": p.get("status"),
                "date": p.get("date"),
                "stack": p.get("stack", []),
                "thumbnail": p.get("thumbnail"),
                "links": p.get("links", {}),
                "body": p.get("body"),
            }
            for p in items
        ],
    }
    return apply_i18n(response, lang)
