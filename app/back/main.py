"""FastAPI 앱 팩토리 — 조립만 한다. 로직 없음.

여기서 하는 일 세 가지뿐이다: 미들웨어(CORS) · 예외 핸들러 · 라우터 등록.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from core.exceptions import register_exception_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    # 잔디 스케줄러 — 매일 KST 08:00 전체 수집(케이스 6·7). 가벼운 asyncio 루프.
    from service.collect_service import collect_service

    # persona 스케줄러 — 매일 KST 08:10 프로필·역할 persona md(DB 파생) 재렌더.
    from service.persona_service import persona_service

    tasks = [
        asyncio.create_task(collect_service.run_scheduler()),
        asyncio.create_task(persona_service.run_scheduler()),
    ]
    try:
        yield
    finally:
        for task in tasks:
            task.cancel()
        for task in tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="kknaks-back", docs_url="/docs", lifespan=_lifespan)

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
    from api.activity_router import router as activity_router
    from api.algorithm_router import admin_router as algorithm_admin_router
    from api.algorithm_router import router as algorithm_router
    from api.asset_router import router as asset_router
    from api.auth_router import router as auth_router
    from api.career_router import admin_router as career_admin_router
    from api.career_router import router as career_router
    from api.commit_router import admin_router as commit_admin_router
    from api.company_router import admin_router as company_admin_router
    from api.content_router import admin_router as content_admin_router
    from api.content_router import router as content_router
    from api.daily_router import admin_router as daily_admin_router
    from api.education_router import admin_router as education_admin_router
    from api.gate_router import admin_router as gate_admin_router
    from api.git_token_router import admin_router as git_token_admin_router
    from api.github_router import admin_router as github_admin_router
    from api.note_router import admin_router as note_admin_router
    from api.note_router import router as note_router
    from api.persona_router import admin_router as persona_admin_router
    from api.problem_router import admin_router as problem_admin_router
    from api.product_router import admin_router as product_admin_router
    from api.profile_router import admin_router as profile_admin_router
    from api.profile_router import router as profile_router
    from api.project_router import admin_router as project_admin_router
    from api.project_router import router as project_router
    from api.queue_router import admin_router as queue_admin_router
    from api.repo_router import admin_router as repo_admin_router
    from api.site_router import admin_router as site_admin_router
    from api.site_router import router as site_router

    app.include_router(auth_router)
    app.include_router(asset_router)
    app.include_router(profile_router)
    app.include_router(profile_admin_router)
    app.include_router(site_router)
    app.include_router(site_admin_router)
    app.include_router(activity_router)
    app.include_router(commit_admin_router)
    app.include_router(daily_admin_router)
    app.include_router(company_admin_router)
    app.include_router(career_router)
    app.include_router(career_admin_router)
    app.include_router(education_admin_router)
    app.include_router(product_admin_router)
    app.include_router(problem_admin_router)
    app.include_router(project_router)
    app.include_router(project_admin_router)
    app.include_router(algorithm_router)
    app.include_router(algorithm_admin_router)
    app.include_router(note_router)
    app.include_router(note_admin_router)
    app.include_router(content_router)
    app.include_router(content_admin_router)
    app.include_router(queue_admin_router)
    app.include_router(gate_admin_router)
    app.include_router(repo_admin_router)
    app.include_router(git_token_admin_router)
    app.include_router(github_admin_router)
    app.include_router(persona_admin_router)

    @app.get("/api/health")
    async def health() -> dict:
        return {"ok": True}

    return app


app = create_app()
