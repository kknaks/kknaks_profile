"""GET /api/print/* — PDF 생성용 raw 데이터 (planning-02 §4).

사이트용 `/api/me`, `/api/career` 등은 `?lang=ko|en` 단일 응답 (adr-02).
print 은 KO+EN 합본 PDF 라 raw `{ko, en}` 객체 그대로 내려줌 — 프론트가 두 언어 모두 렌더.

P2: profile + skills tiers + education + awards + career bullets + projects 케이스 스터디.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()


def _profile_block(profile: dict) -> dict:
    return {
        "handle": profile["handle"],
        "name": profile["name"],
        "role": profile["role"],
        "location": profile.get("location"),
        "email": profile["email"],
        "github": profile.get("github"),
        "linkedin": profile.get("linkedin"),
        "tagline": profile["tagline"],
    }


@router.get("/api/print/resume")
def get_print_resume():
    from main import get_data

    data = get_data()
    profile = data.get("profile")
    if not profile:
        raise HTTPException(status_code=503, detail="profile.md not loaded")

    return {
        "profile": _profile_block(profile),
        "about": {
            "intro": profile["intro"],       # {ko, en}
            "intro2": profile.get("intro2"), # {ko, en} or None
        },
        "skills": profile.get("skills"),     # {primary[], secondary[], learning[]} or None
        "education": profile.get("education", []),  # [{period, degree, org, loc, note}]
        "awards":    profile.get("awards", []),     # [{period, title, note}]
        "career": [
            {
                "period": c.get("period"),
                "title": c.get("title"),         # {ko, en}
                "org": c.get("org"),             # {ko, en}
                "location": c.get("location"),   # {ko, en} or scalar
                "summary": c.get("summary"),     # {ko, en}
                "stack": c.get("stack", []),
                "bullets": c.get("bullets"),     # {ko: [], en: []} or None
                "is_current": c.get("is_current", False),
            }
            for c in data.get("career", [])
        ],
    }


@router.get("/api/print/portfolio")
def get_print_portfolio():
    from main import get_data

    data = get_data()
    profile = data.get("profile")
    if not profile:
        raise HTTPException(status_code=503, detail="profile.md not loaded")

    visible_projects = [p for p in data.get("projects", []) if p.get("visible", True)]
    return {
        "profile": _profile_block(profile),
        "projects": [
            {
                "id": p.get("id"),
                "code": p.get("code") or _slug_from_repo(p.get("links", {}).get("repo")),
                "title": p.get("title"),
                "summary": p.get("summary"),
                "category": p.get("category"),
                "status": p.get("status"),
                "date": p.get("date"),
                "stack": p.get("stack", []),
                "links": p.get("links", {}),
                "thumbnail": p.get("thumbnail"),
                "problem": p.get("problem"),
                "approach": p.get("approach"),
                "impact": p.get("impact"),
                "learnings": p.get("learnings"),
                "troubles": p.get("troubles", []),
            }
            for p in visible_projects
        ],
    }


def _slug_from_repo(repo: str | None) -> str:
    """github.com/owner/repo → repo. None/없음 → ''."""
    if not repo:
        return ""
    return repo.rsplit("/", 1)[-1]
