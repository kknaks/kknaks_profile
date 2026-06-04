"""GET /api/algorithms, /api/algorithms/{id} — 알고리즘 트레이서 (spec-07, planning-03)."""

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n

router = APIRouter()


def _list_row(a: dict) -> dict:
    """목록 페이지용 한 행 (요약 데이터만)."""
    problem = a.get("problem") or {}
    return {
        "id": a.get("id"),
        "date": a.get("date"),
        "day": a.get("day"),
        "title": a.get("title"),
        "summary": problem.get("statement"),
        "difficulty": a.get("difficulty"),
        "source": a.get("source"),
        "tags": a.get("tags", []),
    }


@router.get("/api/algorithms")
def get_algorithms(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    items = get_data().get("algorithms", [])  # 이미 date desc 정렬
    today_item = next((a for a in items if a.get("today") is True), None)

    response = {
        "algorithms": {
            "subtitle": {
                "ko": "neetcode 150 · 키보드 없는 코딩 면접 도장",
                "en": "neetcode 150 · subway dojo for coding interviews",
            },
            "intro": {
                "ko": "해외 코딩 면접 4단계 (Clarifying → Approach → Trace → Solution) 를 손가락으로 굴리는 도장. 매일 1문제.",
                "en": "Daily dojo for the four stages of foreign coding interviews. One problem a day.",
            },
            "totalCount": len(items),
            "today": _list_row(today_item) if today_item else None,
        },
        "algorithms[]": [_list_row(a) for a in items],
    }
    return apply_i18n(response, lang)


@router.get("/api/algorithms/{algo_id}")
def get_algorithm_detail(algo_id: str, lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    items = get_data().get("algorithms", [])
    idx = next((i for i, a in enumerate(items) if a.get("id") == algo_id), None)
    if idx is None:
        raise HTTPException(404, f"algorithm not found: {algo_id}")

    item = items[idx]
    # items 는 date desc 정렬 — index 0 이 최신.
    # newer = idx-1 (더 최신), older = idx+1 (더 옛날) — contents 와 동일 패턴
    newer = items[idx - 1] if idx > 0 else None
    older = items[idx + 1] if idx + 1 < len(items) else None

    response = {
        "algorithms.detail": {
            "id": item.get("id"),
            "date": item.get("date"),
            "day": item.get("day"),
            "title": item.get("title"),
            "difficulty": item.get("difficulty"),
            "source": item.get("source"),
            "tags": item.get("tags", []),
            "problem": item.get("problem"),
            "clarifying": item.get("clarifying"),
            "approach": item.get("approach"),
            "logic": item.get("logic"),
            "trace": item.get("trace"),
            "solution": item.get("solution"),
            "newer": {"id": newer["id"], "title": newer["title"]} if newer else None,
            "older": {"id": older["id"], "title": older["title"]} if older else None,
        }
    }
    return apply_i18n(response, lang)
