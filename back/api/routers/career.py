"""GET /api/career — 경력 (spec-02 §3.4). career.* 메타는 자동 집계 + _meta 보강."""

from fastapi import APIRouter, Query

from core.i18n import apply_i18n

router = APIRouter()


@router.get("/api/career")
def get_career(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    data = get_data()
    items = data.get("career", [])
    meta = data.get("_meta", {}).get("career", {})
    total_roles = len(items)
    response = {
        "career": {
            "subtitle": {
                "ko": f"{total_roles}개 역할",
                "en": f"{total_roles} role" + ("s" if total_roles != 1 else ""),
            },
            "totalRoles": f"{total_roles} role" + ("s" if total_roles != 1 else ""),
            "totalYears": meta.get("totalYears"),
            "focus": meta.get("focus"),
        },
        "career[]": [
            {
                "period": c.get("period"),
                "title": c.get("title"),
                "org": c.get("org"),
                "location": c.get("location"),
                "summary": c.get("summary"),
                "stack": c.get("stack", []),
                "is_current": c.get("is_current", False),
                "body": c.get("body"),
            }
            for c in items
        ],
    }
    return apply_i18n(response, lang)
