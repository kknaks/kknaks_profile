"""pytest 공통 셋업 — 환경변수 + lifespan import 안전성 + 실 persona 격리."""

from __future__ import annotations

import copy
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

# Slack 캡처는 테스트에서 **강제로 끈다** (setdefault 가 아니라 덮어쓴다).
# `.env` 를 source 한 셸에서 테스트를 돌리면 SLACK_CAPTURE_ENABLED=1 이 그대로 들어와,
# TestClient 의 lifespan 이 **실 워크스페이스에 Socket Mode 로 접속하고** 큐 재시도가
# **실 AI 를 호출한다**. 테스트가 외부 서비스에 부수효과를 내면 안 된다.
# 캡처 동작을 검증하는 테스트는 런타임을 직접 조립한다(test_capture_session 등).
os.environ["SLACK_CAPTURE_ENABLED"] = "0"


@pytest.fixture(scope="session")
def _persona_snapshot():
    """실 persona/ 를 **세션당 한 번만** 읽어 원본 스냅샷을 만든다.

    `main.PERSONA_DIR` 은 import 시점에 `config.PERSONA_DIR` 로 바인딩된다. 테스트가
    패치하는 것은 `content_enrich.config.PERSONA_DIR` 이라 여기엔 닿지 않는다 —
    즉 `load_all()` 은 언제 불러도 같은 실 persona 를 읽는다. 그래서 캐시가 성립한다.
    """
    try:
        import main

        main.load_all()
        return copy.deepcopy(main.get_data())
    except Exception:
        return None


@pytest.fixture(autouse=True)
def _reset_persona_data(_persona_snapshot):
    """각 test 전 main._data 를 스냅샷에서 복원한다.

    content_enrich / job 테스트의 monkeypatch 나 `_data` 직접 변형이
    다른 test 로 새는 pollution 차단. main import 안 한 unit test 도 안전 (None 스킵).

    **매번 load_all() 을 부르지 않는다.** 실 persona 재로드는 419개 md 파싱 +
    그래프 빌드 + L1~L6 검증이라 1.3초가 걸린다 — 테스트 355건이면 그것만 8분이다.
    deepcopy 복원은 29ms 로 같은 격리를 47배 싸게 준다.
    """
    if _persona_snapshot is not None:
        import main

        main._data = copy.deepcopy(_persona_snapshot)
    yield
