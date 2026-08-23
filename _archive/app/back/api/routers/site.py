"""GET /api/site — 사이트 전역 (footer/version 등). _meta.yaml/site에서 추출 (spec-02 §3.1)."""

from fastapi import APIRouter, HTTPException, Query

from core.i18n import apply_i18n

router = APIRouter()


@router.get("/api/site")
def get_site(lang: str = Query("ko", pattern="^(ko|en)$")):
    from main import get_data

    meta = get_data().get("_meta", {})
    site = meta.get("site")
    if not site:
        raise HTTPException(503, "site meta not loaded")
    files = site.get("files", {})
    response = {
        "site": {
            "footerTagline": site.get("footerTagline"),
            "location": site.get("location"),
            "version": site.get("version"),
            "uptime": site.get("uptime"),
            "year": site.get("year"),
        },
        "files": {
            "resumeLabel": files.get("resumeLabel"),
            "portfolioLabel": files.get("portfolioLabel"),
        },
    }
    return apply_i18n(response, lang)
