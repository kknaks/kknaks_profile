"""GET /api/contents, /api/contents/{id} — 스터디 영상+교안 (spec-02 §3.10-3.11)."""

import re

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n

router = APIRouter()


@router.get("/api/contents")
def get_contents(
    lang: str = Query("ko", pattern="^(ko|en)$"),
    limit: int = Query(5, ge=1, le=100),
):
    from main import get_data

    items = get_data().get("contents", [])  # 이미 id desc 정렬
    response = {
        "contents": {
            "subtitle": {"ko": "매일 업로드 · 영상 + 교안", "en": "Daily — video + notes"},
            "intro": {
                "ko": "매일 한 편씩 — 영상을 보고 교안을 정리합니다.",
                "en": "Once a day — record a video and write a doc.",
            },
            "totalCount": len(items),
        },
        "contents[]": [
            {
                "id": c.get("id"),
                "date": c.get("date"),
                "day": c.get("day"),
                "title": c.get("title"),
                "youtubeId": c.get("youtubeId"),
                "duration": c.get("duration"),
                "summary": c.get("summary"),
                "tags": c.get("tags", []),
            }
            for c in items[:limit]
        ],
    }
    return apply_i18n(response, lang)


@router.get("/api/contents/{content_id}")
def get_content_detail(content_id: str, lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    items = get_data().get("contents", [])
    idx = next((i for i, c in enumerate(items) if c.get("id") == content_id), None)
    if idx is None:
        raise HTTPException(404, f"content not found: {content_id}")

    item = items[idx]
    body = item.get("body", "")
    concept = _extract_section(body, "개념") or _extract_section(body, "Concept")
    example = _extract_section(body, "적용 예시") or _extract_section(body, "Example")

    # items는 id desc 정렬 — index 0이 최신.
    # newer = idx-1 (더 최신), older = idx+1 (더 옛날)
    newer = items[idx - 1] if idx > 0 else None
    older = items[idx + 1] if idx + 1 < len(items) else None

    response = {
        "contents.detail": {
            "id": item.get("id"),
            "date": item.get("date"),
            "day": item.get("day"),
            "title": item.get("title"),
            "summary": item.get("summary"),
            "youtubeId": item.get("youtubeId"),
            "duration": item.get("duration"),
            "speaker": item.get("speaker"),
            "tags": item.get("tags", []),
            "concept": concept,
            "example": example,
            "newer": {"id": newer["id"], "title": newer["title"]} if newer else None,
            "older": {"id": older["id"], "title": older["title"]} if older else None,
        }
    }
    return apply_i18n(response, lang)


def _extract_section(body: str, heading_ko: str) -> list[str]:
    """본문에서 `## {heading}` 섹션 추출 → 불릿 리스트.

    spec-01 §3.5 — contents 본문 컨벤션 (## 개념, ## 적용 예시).
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(heading_ko)}\s*$(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(body or "")
    if not m:
        return []
    section = m.group(1).strip()
    # 불릿 라인만 (- 시작) 추출
    bullets = []
    for line in section.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets
