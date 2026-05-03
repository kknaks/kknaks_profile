"""GET /api/print/* — PDF 생성용 raw 데이터 (planning-02 §4).

사이트용 `/api/me`, `/api/career` 등은 `?lang=ko|en` 단일 응답 (adr-02).
print 은 KO+EN 합본 PDF 라 raw `{ko, en}` 객체 그대로 내려줌 — 프론트가 두 언어 모두 렌더.

P1.2 단계: profile + about + career 만. P2 에서 education/awards/skills tiers + projects 추가.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/api/print/resume")
def get_print_resume():
    from main import get_data

    data = get_data()
    profile = data.get("profile")
    if not profile:
        raise HTTPException(status_code=503, detail="profile.md not loaded")

    return {
        "profile": {
            "handle": profile["handle"],
            "name": profile["name"],
            "role": profile["role"],
            "location": profile.get("location"),
            "email": profile["email"],
            "github": profile.get("github"),
            "linkedin": profile.get("linkedin"),
            "tagline": profile["tagline"],   # {ko, en}
        },
        "about": {
            "intro": profile["intro"],       # {ko, en}
            "intro2": profile.get("intro2"), # {ko, en} or None
        },
        "career": [
            {
                "period": c.get("period"),
                "title": c.get("title"),         # {ko, en}
                "org": c.get("org"),             # {ko, en}
                "location": c.get("location"),   # {ko, en} or scalar
                "summary": c.get("summary"),     # {ko, en}
                "stack": c.get("stack", []),
                "is_current": c.get("is_current", False),
            }
            for c in data.get("career", [])
        ],
    }
