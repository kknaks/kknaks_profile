---
type: decision
id: KDEV-DEC-013
title: "프로세스 경계 — Slack bridge를 back에 흡수"
status: accepted
product: kknaks-dev
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs: []
  works:
    - "[[work-012-slack-bridge-absorb|KDEV-WORK-012]]"
  releases: []
  related:
    - "[[spec-011-slack-knowledge-capture|OKK-SPEC-011]]"
up:
  - process
  - async-io
  - exception-handling
---

# 프로세스 경계 — Slack bridge를 back에 흡수 (ADR-013)

별도 컨테이너로 떠 있는 Slack Socket Mode bridge를 back 프로세스의 lifespan으로 흡수한다. 파일 쓰기·git push 소유권도 함께 back으로 옮겨, 승인 파이프라인의 쓰기 경계를 한 프로세스에 모은다.

> 이 결정은 승인 게이트 파이프라인의 **선행 조건**이다. 현재 bridge 프로세스는 Postgres에 접속할 수 없어, [[decision-011-approval-gate-chain|KDEV-DEC-011]]의 DB 승인 큐에 적재할 방법이 없다.

## Context

- 관련 baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]

### 현재 구조

| 위치 | 정체 |
|---|---|
| `app/back/service/slack_bridge/` | 라이브러리 — `app.py`(Bolt 핸들러) + `runner.py`(오케스트레이션). 설정·I/O는 전부 DI로 주입받는다 |
| `app/slack_bridge/run.py` | composition root — env 조립 후 `AsyncSocketModeHandler` 기동. `sys.path.insert(BACK_DIR)`로 back 모듈을 임포트한다 |
| compose `slack-bridge` 서비스 | `profiles: ["slack-capture"]`, **`Dockerfile.back` 같은 이미지**, `working_dir: /repo/app/back`, `volumes: .:/repo`(쓰기 가능), `depends_on: back` |

### 분리가 사는 게 없다

| 확인 | 결과 |
|---|---|
| 네트워크 격리? | Socket Mode는 **아웃바운드 웹소켓**이다. 공개 URL·포트가 필요 없고 실제로 포트 노출이 0개다 |
| 다른 이미지? | 아니다. `Dockerfile.back` 그대로, 같은 마운트, 같은 `working_dir` |
| 의존성 분리? | 아니다. `slack-bolt>=1.28`·`aiohttp`가 **이미 `app/back/pyproject.toml`에 있다** |
| 리소스 격리? | AI 실행은 worker 컨테이너가 한다(Redis broker 경유). bridge는 웹소켓 리스너 + 조립일 뿐이다 |
| 독립 배포 단위? | 아니다. `depends_on: back`이고 back의 `/admin/reload-data`를 HTTP로 호출한다(`run.py:66`) |
| 분리 근거 문서? | `OKK-SPEC-011` §4의 *"별도 장기 실행 프로세스로 운용한다"* 한 줄뿐. **왜인지는 어디에도 없다** |

back은 `Dockerfile.back`의 `--workers 1`과 `main.py`의 `_check_single_worker()` raise로 **이미 장기 실행 백그라운드(APScheduler)를 in-process로 돌린다**. Socket Mode 핸들러는 성격이 같은 장기 asyncio 루프다.

### 분리 유지비는 실재한다

- `sys.path.insert(BACK_DIR)` 해킹, `service/slack_bridge` ↔ `app/slack_bridge` **이름 충돌**
- env 이중 관리 — 그 증상이 **`DATABASE_URL` 부재**다. 이 프로세스는 Postgres에 붙지 못한다
- repo 쓰기 마운트가 두 곳. worker는 `.:/repo:ro`로 막아뒀는데 bridge만 쓰기 가능이다
- **git push 소유권이 두 프로세스로 쪼개져 있다** — `runner.py:112-114`가 `atomic_write` → `publish()`(=`commit_and_push_with_retry`) → back에 HTTP reload 순으로 직접 수행한다

마지막 항목이 결정적이다. [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D2가 *"AI는 파일과 DB를 직접 건드리지 않는다"*로 정했는데, 현재 bridge는 정확히 그 반대다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[process]] — 별도 컨테이너로 떠 있던 bridge 를 **back 프로세스 안으로** 흡수한다. 경계를 어디에 그을지가 곧 DB 접근 가능 여부를 갈랐다
- [[async-io]] — Socket Mode 를 lifespan 에서 **asyncio task** 로 띄운다 — APScheduler 와 같은 자리·같은 패턴이다
- [[exception-handling]] — 웹소켓 루프의 예외가 **back 전체를 죽이지 않도록** task 를 감싼다. 격리 범위를 정하는 것이 예외 처리의 설계다

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 현행 유지 | 별도 컨테이너 | 변경 0 | Postgres 접속 불가 → 승인 큐 적재 불가. 쓰기 소유권 분산 | 기각 |
| bridge에 DB를 붙여 독립 유지 | `DATABASE_URL` 등 env 추가 | 컨테이너 구조 무변경 | env 이중 관리 심화, 쓰기 소유권은 여전히 두 곳, 이름 충돌·`sys.path` 해킹 잔존 | 기각 |
| **back lifespan으로 흡수** | `RUN_SCHEDULER`와 같은 자리에서 Socket Mode 기동 | DB·Executor·git push가 한 프로세스, env 단일화, 마운트 정리 | back 재시작 시 소켓 재연결, 웹소켓 예외 격리 필요 | **채택** |

## Decision

### D1. Socket Mode를 back lifespan에서 기동한다

- `SLACK_CAPTURE_ENABLED=1`이면 back의 lifespan에서 `AsyncSocketModeHandler`를 asyncio task로 띄우고, shutdown에서 정리한다. **APScheduler와 같은 자리·같은 패턴**이다(`main.py` lifespan의 `config.run_scheduler()` 분기).
- 웹소켓 루프의 예외가 back 전체를 죽이지 않도록 task를 감싼다. 현재 스케줄러 수준의 격리를 적용한다.
- back은 이미 단일 워커로 하드락돼 있으므로(`--workers 1` + `_check_single_worker()`) 중복 연결 문제가 없다. 이는 APScheduler가 이미 지고 있는 제약이고 새로 생기는 제약이 아니다.

### D2. 쓰기 소유권을 back으로 모은다

- Slack 어댑터는 **이벤트 수신 + AI 초안 생성**까지만 담당한다.
- **파일 쓰기·git commit/push·reload는 Apply Executor가 단독 소유**한다([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D2). `runner.py`의 `atomic_write` + `publish()` + `reload_data()` 3단은 제거되고, 결과는 **승인 큐 적재**로 대체된다.
- `runner.py`가 `publish`/`reload_data`를 DI로 받는 구조는 유지한다 — 주입 대상만 "파일로 쓰고 푸시"에서 "큐에 적재"로 바뀐다. 다만 `atomic_write`는 runner 안에 하드코딩돼 있으므로, **렌더 결과를 그대로 넘기는 단일 sink로 리팩터**한다.
- back에 HTTP로 reload를 호출하던 경로(`run.py:66`)는 **함수 직접 호출**로 단순화된다.

### D3. 디렉토리와 이름을 정리한다

- `app/slack_bridge/run.py`를 제거한다. composition root는 back의 lifespan이 된다.
- `app/back/service/slack_bridge/`(라이브러리)는 **그대로 둔다**. 이름 충돌은 entrypoint 제거로 해소된다.
- `sys.path.insert(BACK_DIR)` 해킹이 사라진다.
- `app/worker/`는 건드리지 않는다 — 자체 `Dockerfile.worker`로 빌드되고 back을 임포트하지 않는 **진짜 독립 프로세스**다. `app/scripts/run_*.py`(수동 dev 러너)도 유지한다.

### D4. compose를 정리한다

- `slack-bridge` 서비스와 `slack-capture` 프로필을 제거한다.
- `SLACK_*`·`CAPTURE_*`·`ALLOWED_SLACK_*` env를 `back` 서비스로 옮긴다. `REDIS_URL`·`RELOAD_TOKEN`·`GH_*`·`JOB_GIT_PUSH_DRY_RUN`은 back에 이미 있으므로 중복이 사라진다.
- `BACKEND_URL`·`REPO_ROOT`는 불필요해진다(같은 프로세스).
- back의 repo 마운트는 **쓰기 가능으로 유지**한다 — Apply Executor가 md를 쓰고 git push를 해야 한다. 없어지는 것은 *두 번째* 쓰기 마운트다.

### D5. `OKK-SPEC-011` §4를 개정한다 (제품 경계 넘음)

- `products/open-kknaks/20-spec/spec-011-slack-knowledge-capture.md` §4 Transport and Entry Point의 *"별도 장기 실행 프로세스로 운용한다"* 를 **"back 프로세스 내 백그라운드 태스크로 운용한다"** 로 개정한다.
- Socket Mode 진입점·인가·멱등성·스레드 세션 계약(§4 나머지)은 **변경하지 않는다.** 전송 계층은 그대로이고 실행 위치만 바뀐다.
- 개정 실행과 open-kknaks 제품의 index·log 갱신은 해당 work에서 수행한다.

### D6. 전환 안전장치

- `SLACK_CAPTURE_ENABLED` 플래그를 유지한다. `0`이면 Socket Mode를 기동하지 않으며, 이는 현재 기본값이다(운영에서 이미 opt-in).
- 전환은 **기존 Slack 캡처 동작을 그대로 옮기는 단계**와 **승인 큐로 배선을 바꾸는 단계**를 분리한다. 전자가 회귀 없이 끝난 뒤 후자를 올린다.
- `app/back/tests/test_capture_session.py`가 `publish`/`reload_data`를 주입해 검증하고 있으므로, sink 리팩터의 회귀 안전망으로 재사용한다.

### 기각

- 현행 별도 컨테이너 유지.
- bridge에 `DATABASE_URL`을 붙여 독립 프로세스로 두는 안.
- `service/slack_bridge` 라이브러리를 옮기거나 이름을 바꾸는 안(불필요).

## Rationale

- **판단 기준**: 이 분리가 무엇을 사는가. 확인한 결과 네트워크·이미지·의존성·리소스·배포 어느 축에서도 사는 게 없고, 문서에도 근거가 없다.
- **흡수가 파이프라인의 선행 조건인 이유**: 승인 큐는 Postgres에 있어야 하는데(미커밋 md는 `reset --hard`에 사라지므로) 현재 bridge는 접속 자체가 불가능하다. 그리고 [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]가 요구하는 "쓰기는 Executor 단독"은 bridge가 직접 push하는 한 성립하지 않는다.
- **전례가 이미 있다**: back은 APScheduler라는 장기 백그라운드 루프를 in-process로 돌리려고 멀티워커를 금지까지 해뒀다. Socket Mode만 컨테이너를 뺄 이유가 없다.
- **리스크**:
  - back 재시작 시 소켓이 끊긴다 → Socket Mode는 자동 재연결이고, 어차피 bridge는 `depends_on: back`이라 지금도 독립 가용성이 없다.
  - 웹소켓 루프 예외가 back에 전파될 수 있다 → task 격리로 처리한다. 스케줄러가 이미 같은 수준으로 살고 있다.
  - back 컨테이너에 Slack 토큰이 추가된다 → 같은 호스트·같은 `.env`이므로 시크릿 표면이 실질적으로 넓어지지 않는다.
  - 멀티워커 전환 시 중복 연결 → APScheduler 때문에 **이미 금지 상태**라 새 제약이 아니다.

## Scope

- In: Socket Mode 실행 위치, 쓰기 소유권 이관, `app/slack_bridge/` 제거, compose 정리, `OKK-SPEC-011` §4 개정 방향, 전환 안전장치.
- Out:
  - 승인 큐 적재 계약 자체 → [[decision-011-approval-gate-chain|KDEV-DEC-011]] / 큐 spec
  - Apply Executor 계약 → [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]
  - `app/worker/`·`app/scripts/` 구조 (무변경)
  - Slack 진입점·인가·멱등성 계약 (무변경)
- 영향을 받는 spec 후보: `OKK-SPEC-011`(§4 개정), 40-architecture/system(프로세스 구성).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 웹소켓 task가 반복 실패할 때 back을 죽일지, 캡처만 비활성화하고 API는 계속 서빙할지 | kknaks | 흡수 work |
| OQ-2 | `slack-capture` 프로필 제거 후, 로컬에서 Slack 없이 개발할 때의 기본값 (`SLACK_CAPTURE_ENABLED=0` 유지로 충분한지) | kknaks | 흡수 work |
| OQ-3 | `app/scripts/run_*.py`의 `sys.path` 해킹도 같이 정리할지 (이번 범위 밖이나 같은 패턴) | kknaks | 후속 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| `OKK-SPEC-011` | update | §4 Transport — "별도 장기 실행 프로세스" → "back 내 백그라운드 태스크". 나머지 §4 계약 무변경 |
| 40-architecture/system | update | 프로세스 구성도(back·worker·redis·postgres), Slack 전송 경로, 쓰기 소유권 경계 |
