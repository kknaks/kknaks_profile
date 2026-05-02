"""GET /api/activity — 활동 잔디 (spec-02 §3.3). activity.yaml 그대로 분기."""

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
