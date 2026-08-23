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


@pytest.fixture(scope="session", autouse=True)
def _no_real_slack():
    """테스트가 **진짜 Slack 으로 나가지 못하게** 막는다 (KDEV-WORK-018 P2).

    `service.notify.notify_slack` 은 `SLACK_WEBHOOK_URL` 이 비면 no-op 이다. 그런데
    `.env` 를 통째로 export 한 채 스위트를 돌리면 그 값이 채워지고, `notify_slack` 을
    monkeypatch 하지 않은 테스트들이 **실제 워크스페이스로 메시지를 보낸다.**

    실제로 그렇게 나갔다 — `kknaks/gone CLONE_FAILED` 와 `C-001-test` 같은 픽스처
    내용이 운영 채널에 실렸다. 알림은 부수효과라 테스트가 실패하지 않고, 그래서
    **아무도 모른 채 반복된다.**

    개별 테스트의 monkeypatch 를 대체하지 않는다. 그쪽은 "무엇을 보냈나" 를 검증하고,
    이것은 "밖으로 나가지 않는다" 를 보장한다 — 새 테스트가 patch 를 잊어도 샌 적이
    없어야 한다.
    """
    os.environ["SLACK_WEBHOOK_URL"] = ""
    yield


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


async def isolate_tables(conn, *tables: str) -> None:
    """열려 있는 트랜잭션 안에서 테이블을 비운다 (KDEV-WORK-017 결함 ⑤).

    DB 를 쓰는 테스트들이 **해당 테이블이 비어 있다고 전제하고** 있었다. dev DB 가
    실제로 비어 있는 동안은 통과했지만, e2e 로 `tracked_repos` 13행과 큐 항목이
    들어오자 12건이 깨졌다. **레지스트리가 채워진 것이 정상 운영 상태다** — 그때
    깨지는 테스트는 배포하면 반드시 깨진다.

    호출부의 바깥 트랜잭션이 teardown 에서 롤백되므로 **커밋된 데이터는 안전하다.**
    이 DELETE 도 같이 되돌아간다.

    `conn`(세션이 아니라 커넥션)을 받는 이유는 세션 savepoint 보다 바깥에서 지워야
    테스트가 만드는 savepoint 와 얽히지 않기 때문이다.
    """
    from sqlalchemy import text

    for table in tables:
        await conn.execute(text(f"DELETE FROM {table}"))
