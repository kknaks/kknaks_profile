"""FastAPI 앱 — 부팅 시 페르소나 로드 + 라우터 등록 (spec-02, ADR-01)."""

from __future__ import annotations

import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any

# kknaks-back.* 로거가 컨테이너 stdout 으로 흐르게 — uvicorn 기본 설정만으론 묻힘
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

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
        "persona loaded: %d career, %d projects, %d notes, %d contents, %d daily, %d algorithms",
        len(_data["career"]),
        len(_data["projects"]),
        len(_data["notes"]),
        len(_data["contents"]),
        len(_data["daily"]),
        len(_data.get("algorithms", [])),
    )
    _report_graph(_data)


def _report_graph(data: dict[str, Any]) -> None:
    """KDEV-WORK-001 — 지식그래프 산출(_graph.json) + L1~L6 검증 리포트.

    **report-only**: 위반은 로그로만 출력, 부팅 차단 안 함. write 실패해도 무시.
    """
    from core.graph import summarize

    graph = data.get("_graph") or {"nodes": [], "edges": [], "backlinks": {}}
    violations = data.get("_graph_violations") or []
    if data.get("_graph_error"):
        logger.warning("graph build error (report-only): %s", data["_graph_error"])

    logger.info(
        "knowledge graph: %d nodes, %d edges (report-only)",
        len(graph["nodes"]),
        len(graph["edges"]),
    )
    if violations:
        counts = summarize(violations)
        logger.warning(
            "graph validation (report-only, WORK-002 작업목록): %s",
            ", ".join(f"{k}={v}" for k, v in sorted(counts.items())),
        )

    # _graph.json best-effort write — 읽기전용 FS 등 실패는 무시 (부팅 영향 0)
    try:
        out = config.graph_json_path()
        out.write_text(
            json.dumps(graph, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        logger.info("wrote %s", out)
    except Exception as e:  # noqa: BLE001
        logger.warning("could not write _graph.json (ignored): %s", e)


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
        logger.info(
            "APScheduler started — daily-activity (09:05 KST) + neetcode-canonical (23:00 UTC)"
        )
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
    algorithms,
    career,
    contents,
    me,
    notes,
    print as print_router,
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
app.include_router(algorithms.router)
app.include_router(print_router.router)
app.include_router(admin_reload.router)

# 정적 자산 서빙 — persona/assets/<category>/... 를 /assets/* 로 노출 (spec-01 §2.5, spec-02 §2)
app.mount(
    "/assets",
    StaticFiles(directory=PERSONA_DIR / "assets", check_dir=False),
    name="assets",
)

# DeskDeck(헬퍼 DeskDeckHelper) DMG 다운로드 — repo 루트 downloads/ 를 /download/* 로 노출 (mac-remote RB-001 §배포)
app.mount(
    "/download",
    StaticFiles(directory=PERSONA_DIR.parent / "downloads", check_dir=False),
    name="download",
)
