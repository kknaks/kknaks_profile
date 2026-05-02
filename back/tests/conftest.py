"""pytest 공통 셋업 — 환경변수 + lifespan import 안전성."""

from __future__ import annotations

import os

# 테스트 환경에서 APScheduler 비활성화 (main.py lifespan 의 scheduler init 분기 skip).
# main.py 의 `from scheduler import init_scheduler` 가 RUN_SCHEDULER=1 일 때만 발동 — 0 으로 박아 import 자체를 회피.
os.environ.setdefault("RUN_SCHEDULER", "0")
os.environ.setdefault("WEB_CONCURRENCY", "1")
os.environ.setdefault("JOB_GIT_PUSH_DRY_RUN", "1")
