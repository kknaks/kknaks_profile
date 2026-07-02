"""pytest 공통 셋업 — 환경변수 + lifespan import 안전성 + 실 persona reload."""

from __future__ import annotations

import os

import pytest

# 테스트 환경에서 APScheduler 비활성화 (main.py lifespan 의 scheduler init 분기 skip).
# main.py 의 `from scheduler import init_scheduler` 가 RUN_SCHEDULER=1 일 때만 발동 — 0 으로 박아 import 자체를 회피.
os.environ.setdefault("RUN_SCHEDULER", "0")
os.environ.setdefault("WEB_CONCURRENCY", "1")
os.environ.setdefault("JOB_GIT_PUSH_DRY_RUN", "1")
# KDEV-WORK-007 — 테스트는 enforce off 가 기본(실-persona load 포함 266 테스트 안정).
# enforcement 메커니즘 테스트는 각자 monkeypatch.setenv("GRAPH_ENFORCE","1") 로 opt-in.
os.environ.setdefault("GRAPH_ENFORCE", "0")


@pytest.fixture(autouse=True)
def _reset_persona_data():
    """각 test 전 main._data 를 실 persona/ 로 reload.

    content_enrich / job 테스트의 monkeypatch (config.PERSONA_DIR=tmp_path) 가
    다른 test 로 새는 pollution 차단. main import 안 한 unit test 도 안전 (try-except).
    """
    try:
        import main

        main.load_all()
    except Exception:
        pass
    yield
