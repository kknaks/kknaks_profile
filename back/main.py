"""FastAPI 앱 — 부팅 시 페르소나 로드 + 라우터 등록 (spec-02, ADR-01)."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import config
from service.persona_loader import load_persona

logger = logging.getLogger("kknaks-back")

PERSONA_DIR = config.PERSONA_DIR

# 글로벌 메모리 캐시 (spec-03 §6 패턴 — 잡이 `from main import load_all`로 reload 셀프 호출)
_data: dict[str, Any] = {}


def load_all() -> None:
    """페르소나 reload. 멱등 — 같은 입력이면 같은 결과."""
    global _data
    _data = load_persona(PERSONA_DIR)
    logger.info(
        "persona loaded: %d career, %d projects, %d notes, %d contents, %d daily",
        len(_data["career"]),
        len(_data["projects"]),
        len(_data["notes"]),
        len(_data["contents"]),
        len(_data["daily"]),
    )


def get_data() -> dict[str, Any]:
    """라우터에서 메모리 dict 접근."""
    return _data


def _check_single_worker() -> None:
    """spec-03 §1.2 — multi-worker 시 APScheduler 다중 발동 위험 차단."""
    workers = config.web_concurrency()
    if workers > 1:
        raise RuntimeError(
            f"Multi-worker deployment 금지 — APScheduler가 {workers}번 발동 위험 "
            f"(spec-03 §1.2). single-worker로 띄우거나 distributed lock 적용."
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _check_single_worker()
    load_all()

    # APScheduler 시작 (spec-03 §1.1). 테스트에서는 RUN_SCHEDULER=0으로 skip
    if config.run_scheduler():
        from service.scheduler import init_scheduler

        sched = init_scheduler()
        sched.start()
        logger.info("APScheduler started — daily-activity at 00:05 KST")
        try:
            yield
        finally:
            sched.shutdown(wait=False)
    else:
        logger.info("APScheduler disabled (RUN_SCHEDULER=0)")
        yield


app = FastAPI(
    title="kknaks.dev API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — client component fetch (browser) 대응. dev/운영 origin 허용.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # dev
        "http://localhost:3000",
        "http://localhost:48000",
        # 운영
        "https://profile.kknaks.cloud",
        "https://profile-api.kknaks.cloud",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers (지연 import로 circular 회피)
from api.admin import reload as admin_reload  # noqa: E402
from api.routers import (  # noqa: E402
    activity,
    career,
    contents,
    me,
    notes,
    projects,
    site,
)

app.include_router(site.router)
app.include_router(me.router)
app.include_router(activity.router)
app.include_router(career.router)
app.include_router(projects.router)
app.include_router(notes.router)
app.include_router(contents.router)
app.include_router(admin_reload.router)

# 정적 자산 서빙 — persona/assets/<category>/... 를 /assets/* 로 노출 (spec-01 §2.5, spec-02 §2)
app.mount(
    "/assets",
    StaticFiles(directory=PERSONA_DIR / "assets", check_dir=False),
    name="assets",
)
