"""FastAPI 앱 팩토리 — 조립만 한다. 로직 없음.

여기서 하는 일 세 가지뿐이다: 미들웨어(CORS) · 예외 핸들러 · 라우터 등록.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from core.exceptions import register_exception_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="kknaks-back", docs_url="/docs")

    # 쿠키 인증(credentials: include)이라 origin 을 * 로 열 수 없다.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # 라우터 등록 — 층이 생길 때마다 여기 한 줄씩 는다.
    from api.algorithm_router import admin_router as algorithm_admin_router
    from api.auth_router import router as auth_router
    from api.career_router import admin_router as career_admin_router
    from api.company_router import admin_router as company_admin_router
    from api.content_router import admin_router as content_admin_router
    from api.education_router import admin_router as education_admin_router
    from api.note_router import admin_router as note_admin_router
    from api.problem_router import admin_router as problem_admin_router
    from api.product_router import admin_router as product_admin_router
    from api.profile_router import admin_router as profile_admin_router
    from api.profile_router import router as profile_router
    from api.project_router import admin_router as project_admin_router
    from api.site_router import admin_router as site_admin_router
    from api.site_router import router as site_router

    app.include_router(auth_router)
    app.include_router(profile_router)
    app.include_router(profile_admin_router)
    app.include_router(site_router)
    app.include_router(site_admin_router)
    app.include_router(company_admin_router)
    app.include_router(career_admin_router)
    app.include_router(education_admin_router)
    app.include_router(product_admin_router)
    app.include_router(problem_admin_router)
    app.include_router(project_admin_router)
    app.include_router(algorithm_admin_router)
    app.include_router(note_admin_router)
    app.include_router(content_admin_router)

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True}

    return app


app = create_app()
