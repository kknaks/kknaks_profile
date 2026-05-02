"""GET /api/me — About + Hero + Footer 연락처 (spec-02 §3.2)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n

router = APIRouter()


@router.get("/api/me")
def get_me(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data  # 함수 내 import — circular 회피 (spec-03 §6 패턴)

    data = get_data()
    profile = data.get("profile")
    if not profile:
        raise HTTPException(status_code=503, detail="profile.md not loaded")

    # spec-02 §3.2 응답 스키마
    response = {
        "user": {
            "handle": profile["handle"],
            "name": profile["name"],
            "role": profile["role"],
            "years": profile.get("years"),
            "location": profile.get("location"),
            "focus": profile.get("focus"),
            "email": profile["email"],
            "github": profile.get("github"),
            "linkedin": profile.get("linkedin"),
            "avatarUrl": profile.get("avatarUrl"),
            "tagline": profile["tagline"],
            "intro": profile["intro"],
            "intro2": profile.get("intro2"),
            "stack": profile["stack"],
            "stackShort": profile.get("stackShort"),
            "cards": profile.get("cards", []),
        },
        "hero": profile.get("hero", {}),
        "heroTerminal": profile.get("heroTerminal", []),
        "about": {"subtitle": {"ko": "만드는 사람", "en": "the maker"}},
    }
    return apply_i18n(response, lang)
