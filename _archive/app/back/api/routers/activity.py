"""GET /api/activity — 활동 잔디 (spec-02 §3.3, ADR-06).

`activity` 는 persona_loader 가 daily/*.md frontmatter 들을 derive 한 결과.
items[] 의 각 entry: {date, counts: {commit/note/study}, count: sum(counts), summary: {ko, en} | null}.
"""

from fastapi import APIRouter, Query

from core.i18n import apply_i18n

router = APIRouter()


@router.get("/api/activity")
def get_activity(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    activity = get_data().get("activity", {}) or {}
    response = {
        "activity": {
            "totalCount": activity.get("totalCount", 0),
            "since": activity.get("since"),
            "until": activity.get("until"),
        },
        "activity[]": activity.get("items", []),
    }
    return apply_i18n(response, lang)
