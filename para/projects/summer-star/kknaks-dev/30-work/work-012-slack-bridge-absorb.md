---
type: work
id: KDEV-WORK-012
title: "Slack bridge를 back에 흡수 + 쓰기 소유권 정리"
status: done
product: kknaks-dev
work_type: refactor
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-013-slack-bridge-into-backend|KDEV-DEC-013]]"
  specs:
    - "[[spec-007-approval-queue|KDEV-SPEC-007]]"
  works: []
  releases: []
  related:
    - "[[spec-011-slack-knowledge-capture|OKK-SPEC-011]]"
---

# Slack bridge를 back에 흡수 + 쓰기 소유권 정리

별도 컨테이너로 뜨는 Slack Socket Mode 프로세스를 back의 lifespan으로 옮기고, `runner.py`의 파일 쓰기·git push를 **교체 가능한 sink**로 분리한다.

> 만들지 않는 것: 승인 큐·게이트·Apply Executor. 이 work는 **캡처 동작을 바꾸지 않고 실행 위치와 배선만** 옮긴다. 큐 적재로 바꾸는 것은 WORK-014다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-007 (선행 조건 부분)
- Depends on work: 없음
- Parallel work: WORK-013 (concept 층 — 서로 독립)
- Follow-up work: WORK-014 (큐 적재로 sink 교체)
- External dependency: Slack 앱 토큰/봇 토큰 (기존 그대로). 신규 credential 없음

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | main (미커밋 작업트리) |
| Blocker | 없음 |
| Next | WORK-013 concept 층 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·전환 순서 | done |
| Design | — | UI 변경 없음 | — |
| FE | — | 변경 없음 | — |
| BE | kknaks | lifespan 흡수·sink 리팩터·compose | done |
| QA | kknaks | 캡처 회귀 검증 | done (로컬) |
| Ops | kknaks | compose 재기동·env 이관 | **미수행 — 운영 배포 대기** |

## Scope

포함:

- `runner.py`의 영속화(`atomic_write` + `publish()` + 후속 파일 재읽기)를 **`CaptureStore` 양방향 DI**로 통합
- Socket Mode 핸들러를 back lifespan에서 기동/종료
- `app/slack_bridge/run.py` 제거, `sys.path` 해킹 제거
- compose에서 `slack-bridge` 서비스·`slack-capture` 프로필 제거, env를 `back`으로 이관
- `OKK-SPEC-011` §4 Transport 문장 개정

제외:

- 승인 큐 적재 (WORK-014) — 이번엔 store가 **기존과 동일하게 파일을 쓰고 push**한다
- `service/slack_bridge/` 라이브러리 이동·이름 변경 (불필요)
- `app/worker/`·`app/scripts/` 구조 (무변경)
- Slack 진입점·인가·멱등 계약 (무변경)

## Code Surface

- Repo / module: `app/back`, `app/slack_bridge`, compose

| 경로 후보 | 설명 |
|---|---|
| `app/back/service/slack_bridge/runner.py` | sink DI 리팩터. `atomic_write`+`publish`+`reload_data` → `sink(path, rendered)` |
| `app/back/main.py` | lifespan에 Socket Mode task 기동/종료 (`RUN_SCHEDULER` 분기 옆) |
| `app/back/config.py` | `SLACK_*`·`CAPTURE_*`·`ALLOWED_SLACK_*` 접근자 |
| `app/back/service/slack_bridge/app.py` | 변경 없음 (Bolt 핸들러) |
| `app/back/service/slack_bridge/bootstrap.py` | **신규** — `CaptureRuntime` + `supervise_connection`(백오프 재기동) |
| `app/back/service/knowledge_capture/store.py` | **신규** — `CaptureStore` 양방향 계약 |
| `app/back/service/slack_bridge/stores.py` | **신규** — `FileCaptureStore` |
| `app/back/tests/test_capture_supervisor.py` | **신규** — 재기동 supervisor 6건 |
| `.github/workflows/deploy.yml` | **(계획 외)** 죽은 `--profile slack-capture` 분기 제거 |
| `app/slack_bridge/run.py` | **삭제** — 조립 로직은 lifespan으로 |
| `docker-compose.yml` · `docker-compose.local.yml` | `slack-bridge` 서비스 제거, env 이관 |
| `app/back/tests/test_capture_session.py` | sink 주입으로 기존 검증 유지 |
| `products/open-kknaks/20-spec/spec-011-slack-knowledge-capture.md` | §4 Transport 개정 |

- Domain / schema note: **DB 스키마 변경 없음.** 이번 work는 프로세스 경계만 다룬다.

## Domain / Schema

해당 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-014 | `CaptureStore` | 이 work가 만든 store 지점을 "큐 적재"로 교체한다. `runner.py` 무변경이 목표 |

## Internal Interface Contract

`KnowledgeCaptureRunner`가 주입받는 store 계약을 고정한다. WORK-014가 이 지점만 갈아끼우고 `runner.py` 는 건드리지 않는다.

**확정 계약** (`service/knowledge_capture/store.py`) — 영속화를 **양방향 모두** store 가 소유한다.

```text
class CaptureStore(Protocol):
    async def load_previous(session) -> PreviousCapture
    async def store(artifact)        -> StoreResult

CaptureArtifact  = { path, rendered, document, replace, request }
StoreResult      = { location, stored_ref, warnings }
PreviousCapture  = { markdown, output_override }
```

- **왜 양방향인가**: 스레드 후속 대화는 "이전 초안"을 AI 에 다시 넘겨야 하는데, 그게 어디 있는지는 저장한 쪽만 안다. 쓰기만 추상화하고 읽기를 runner 에 남기면(파일을 직접 `read_text`) 큐 store 로 갈아끼울 때 **runner 를 또 고쳐야 한다.**
- **`stored_ref` 는 불투명 참조다.** 해석하는 것은 store 자신뿐 — 파일 store 는 상대 경로를, 큐 store 는 `queue:<id>` 를 넣는다. 세션에는 `CaptureSession.output_path` 필드로 실린다(이름은 파일 시절 잔재, 의미는 "store 참조").
- **`output_override` 도 store 가 준다.** 후속 대화가 같은 목적지로 다시 쓰게 하는 값인데, 이전에는 runner 가 `Path(session.output_path)` 로 만들었다 — 참조가 경로가 아니면 깨진다.
- 인자를 dataclass 로 둔 이유: 큐 store 는 `path`/`rendered` 외에 **`request`**(채널·스레드·제출자)가 필요하다. 위치 인자였으면 그때 시그니처를 또 바꿔야 한다.
- `location` 은 Slack 회신에 그대로 찍히므로 표시 문구도 store 가 소유한다.

**성립 조건**: `runner.py` 안에 파일시스템 접근이 하나도 없어야 한다. 리팩터 후 `read_text`/`write_text`/`atomic_write`/`is_file` 이 전부 사라진 것을 grep 으로 확인했다.

## Execution

### Phase 1 — sink 리팩터 (동작 무변경)

- **Status**: DONE
- **설명**: 파일 쓰기·push·reload를 하나의 교체 가능한 지점으로 모은다. 이 단계에서는 **동작이 전혀 바뀌지 않아야** 한다.
- **작업**:
  - [x] `KnowledgeCaptureRunner`의 `publish`/`reload_data` 2개 DI를 `sink` 1개로 통합
  - [x] `runner.handle`에서 `atomic_write` 직접 호출 제거 → sink에 위임
  - [x] 기존 동작과 동일한 파일 sink 구현 (`atomic_write` → push → reload)
  - [x] `test_capture_session.py`를 새 sink 시그니처로 갱신
- **검증**:
  - [x] `test_capture_session` 통과 (기존 검증 항목 유지)
  - [x] 전체 테스트 통과
  - [x] sink를 no-op으로 주입하면 파일이 생기지 않음을 테스트로 확인
- **완료 증거**:
  - 신규 `service/knowledge_capture/store.py` — `CaptureStore` Protocol + `CaptureArtifact` / `StoreResult` / `PreviousCapture` / `EMPTY_PREVIOUS`.
  - 신규 `service/slack_bridge/stores.py` `FileCaptureStore` — 흡수 이전 동작(`atomic_write` → push → reload + 후속 시 파일 재읽기)을 그대로 옮김. `publish`/`reload_data` 는 계속 주입받아 테스트가 fake 를 넣는다. 경로 이탈은 빈 결과로 차단하고, **파일이 사라져도 목적지는 유지**한다(같은 노트를 계속 갱신하는 것이 스레드 후속의 의도).
  - `runner.py` — 생성자 인자 `publish`/`reload_data` → `store` 하나로 교체. **파일시스템 접근 2곳 제거**: 이전 초안 `read_text` → `store.load_previous()`, `Path(session.output_path)` → `previous.output_override`.
  - 신규 테스트 2건 — ① `test_runner_with_queue_store_writes_nothing`: 큐 store 주입 시 **`tmp_path.rglob("*.md") == []`**(파일 0개), 세션에 `queue:1` 참조가 실림 ② `test_queue_store_follow_up_reads_previous_from_store`: 후속 대화의 이전 초안이 **store 에서** 공급되고(프롬프트에 직전 본문 포함), 파일 없이도 같은 목적지로 `replace=True` 갱신됨. WORK-014 가 `runner.py` 를 건드리지 않고 갈아끼울 수 있음을 증명한다.
  - 전체 스위트 **318 passed** (`.venv/bin/python -m pytest -q`, 5분 30초).

### Phase 2 — back lifespan 흡수

- **Status**: DONE
- **설명**: Socket Mode를 back 프로세스 안에서 기동한다. APScheduler와 같은 자리·같은 패턴.
- **작업**:
  - [x] `config.py`에 Slack/캡처 env 접근자 추가
  - [x] `main.py` lifespan에서 `SLACK_CAPTURE_ENABLED=1`이면 Socket Mode를 asyncio task로 기동
  - [x] shutdown에서 task 정리 (broker·redis 연결 포함)
  - [x] 웹소켓 루프 예외를 task 안에서 격리 (예외가 back을 죽이지 않게)
  - [x] **(추가) 루프 재기동 supervisor** — 격리만 하고 복구를 안 넣으면 흡수 전 대비 회귀
  - [x] `reload_backend()` HTTP 호출 → `reload_data()` 직접 호출로 교체
  - [x] `app/slack_bridge/` 삭제
- **검증**:
  - [x] `SLACK_CAPTURE_ENABLED=0`으로 back이 정상 부팅하고 기존 API가 동작
  - [ ] ~~`SLACK_CAPTURE_ENABLED=1`에서 Slack 멘션 → 노트 생성 → 커밋까지 기존과 동일하게 동작~~ — **미검증**(실 Slack 토큰 필요, Pre-deploy 로 이관)
  - [x] 웹소켓 강제 종료 시 back API가 계속 응답
  - [ ] ~~back 재시작 후 Socket Mode가 자동 재연결~~ — **미검증**(실 연결 필요, Slack SDK 내장 동작에 의존)
  - [x] **(추가) 루프가 죽어도 back 재시작 없이 스스로 복구된다** — supervisor 테스트 6건
- **완료 증거**:
  - `config.py` +10 접근자: `repo_root`·`slack_capture_enabled`·`slack_bot_token`·`slack_app_token`·`allowed_slack_users`/`_channels`(fail-closed CSV)·`capture_namespace`/`_provider`/`_model`/`_work_dir`/`_timeout_seconds`.
  - 신규 `service/slack_bridge/bootstrap.py` `CaptureRuntime` — `start()`/`stop()` 로 broker·redis·Socket Mode task 수명을 lifespan 에 묶는다. `_run_forever` 가 웹소켓 예외를 흡수해 back 으로 전파시키지 않는다.
  - `main.py` lifespan 재구성 — 중첩 `try/yield/finally` 를 풀어 `sched`/`capture` 를 나란히 두고 단일 `finally` 에서 정리. APScheduler 분기 바로 옆에 캡처를 배치.
  - HTTP reload 제거 — 종전 `run.py` 의 `POST /admin/reload-data` 왕복이 `from main import reload_data` 직접 호출로 대체됨. `RELOAD_TOKEN`·`BACKEND_URL` 이 캡처 경로에서 불필요해짐.
  - git 작업은 blocking 이라 `asyncio.to_thread` 로 감쌈(event loop 비차단).
  - `app/slack_bridge/` 삭제 → `sys.path.insert(BACK_DIR)` 해킹과 `service/slack_bridge` ↔ `app/slack_bridge` 이름 충돌 동시 해소.
  - **부팅 3종 실측**(`lifespan` 직접 구동): ① `ENABLED=0` → `Slack capture disabled` 로그 + lifespan 정상 진입/종료 ② `ENABLED=1` + 토큰 없음 → `SLACK_BOT_TOKEN/SLACK_APP_TOKEN missing — skip` 경고 + 정상 부팅 ③ `ENABLED=1` + 가짜 토큰 + 도달 불가 redis → `기동 실패 — 캡처만 비활성화하고 API 는 계속 서빙` ERROR 로그 후 **lifespan 정상 진입/종료**. 세 경우 모두 API 서빙이 유지됨을 확인 — DEC-013 OQ-1 의 채택안(캡처만 비활성화)이 실제로 동작한다. supervisor 추가 후 재실측해도 동일.

#### 루프 재기동 supervisor (리뷰 중 발견한 회귀 수정)

격리를 넣으면서 **복구 경로를 같이 없앤 것**을 리뷰에서 발견했다.

| | 흡수 전 | 격리만 넣은 상태 | supervisor 추가 후 |
|---|---|---|---|
| 루프가 죽으면 | 예외가 `asyncio.run` 까지 전파 → 프로세스 종료 | `_run_forever` 가 삼킴 | supervisor 가 잡음 |
| 그 다음 | compose `restart: unless-stopped` → 컨테이너 재시작 → **캡처 복구** | task 만 끝나고 **캡처는 죽은 채 방치** | 백오프 후 **자동 재기동** |

`supervise_connection(connect, close=..., sleep=..., now=...)` 을 순수 함수로 분리해 주입 가능하게 만들었다 — 실제 대기 없이 백오프 수열을 검증하기 위해서다.

- 백오프 5s → 10s → 20s … 상한 300s, 연속 10회 실패 시 포기(토큰 폐기처럼 재시도로 안 풀리는 상황에서 Slack API 를 무한히 두드리지 않기 위해)
- **포기하면 Slack 으로 알린다.** 기존 `service/notify.py` `notify_slack` 재사용 — `SLACK_WEBHOOK_URL` 미설정이면 no-op 이라 추가 설정이 필요 없다. 기동 실패(`start()` 예외)도 같은 "조용히 죽는 경로"라 함께 알린다
- `healthy_seconds`(60s) 이상 붙어 있었으면 백오프를 초기화한다 — 몇 시간 뒤의 단발 끊김이 과거 이력 때문에 5분씩 기다리지 않게
- **핸들러는 재기동마다 새로 만든다** — 죽은 핸들러 재사용은 이전 소켓의 잔여 상태를 물고 들어간다
- 취소(shutdown)는 재기동 대상이 아니라 그대로 전파 → lifespan 이 정상 종료
- 신규 테스트 `tests/test_capture_supervisor.py` **9건**: 백오프 수열·포기 임계 / 장시간 연결 후 백오프 초기화 / 취소 전파 / 재기동 간 핸들러 정리 / 정리 실패가 재기동을 막지 않음 / 예외 없는 조용한 반환도 끊김으로 처리 / **포기 시 1회 알림** / **알림 실패가 supervisor 를 깨지 않음** / **정상 shutdown 은 알리지 않음**(장애가 아니므로)

**부팅 실패(config·인증)는 재시도하지 않는다.** 토큰이 틀렸거나 broker 에 못 붙는 건 재시도로 안 풀리므로 `start()` 에서 한 번 잡고 끝낸다. 재기동은 **연결이 한 번 성립한 뒤 끊긴 경우**만 대상이다.

### Phase 3 — compose·문서 정리

- **Status**: DONE
- **설명**: 컨테이너와 문서에서 별도 프로세스 흔적을 걷어낸다.
- **작업**:
  - [x] `docker-compose.yml`·`docker-compose.local.yml`에서 `slack-bridge` 서비스 제거
  - [x] `SLACK_*`·`CAPTURE_*`·`ALLOWED_SLACK_*`를 `back` 서비스로 이관
  - [x] `BACKEND_URL` 제거 (`REPO_ROOT` 는 캡처 경로 조립에 계속 필요해 `back` 으로 이관)
  - [x] `.env.example` 갱신
  - [x] `OKK-SPEC-011` §4의 *"별도 장기 실행 프로세스로 운용한다"* → *"back 프로세스 내 백그라운드 태스크로 운용한다"*
  - [x] open-kknaks 제품의 `20-spec/README.md`·`log.md` 갱신
  - [x] **(계획 외 발견) `.github/workflows/deploy.yml` 의 `--profile slack-capture` 분기 제거**
- **검증**:
  - [x] `docker compose config --services` 결과가 **postgres·redis·back·worker 4개**뿐 (두 compose 파일 모두)
  - [ ] ~~운영 환경에서 Slack 캡처 1건 e2e 성공~~ — **미수행**(운영 배포 필요, Pre-deploy 로 이관)
  - [x] `products/open-kknaks` hook green (warnings 0 / errors 0)
- **완료 증거**:
  - compose 2개에서 `slack-bridge` 서비스와 `profiles: ["slack-capture"]` 제거. 캡처 env 11종을 `back` 으로 이관(`NAMESPACE`·`SLACK_CAPTURE_ENABLED`·`SLACK_BOT_TOKEN`·`SLACK_APP_TOKEN`·`ALLOWED_SLACK_USERS`·`ALLOWED_SLACK_CHANNELS`·`CAPTURE_PROVIDER`·`CAPTURE_MODEL`·`CAPTURE_WORK_DIR`·`CAPTURE_TIMEOUT_SECONDS`·`REPO_ROOT`). `RELOAD_TOKEN`·`GH_*`·`JOB_GIT_PUSH_DRY_RUN` 은 back 에 이미 있어 중복이 사라짐.
  - **계획에 없던 발견** — `.github/workflows/deploy.yml` 이 `.env` 의 `SLACK_CAPTURE_ENABLED` 값을 보고 `--profile slack-capture` 로 컨테이너를 올리거나 내리고 있었다. 그대로 뒀으면 배포가 존재하지 않는 서비스를 참조해 실패했을 것이다. 단순 `docker compose up -d --build back redis worker` 로 바꾸고, 흡수 이전 배포에서 남아 있을 컨테이너를 정리하는 `docker rm -f kknaks-slack-bridge || true` 를 1회성 안전망으로 추가.
  - `OKK-SPEC-011` §4 개정 + 개정 근거 주석(분리가 사는 것 5축 부재 / 유지비 5종) 삽입. `links.decisions` 에 KDEV-DEC-013, `links.specs` 에 KDEV-SPEC-007 연결. §4 나머지 계약은 무변경 명시.
  - `products/` 전체 hook green.

## Pre-deploy Check

- [x] `SLACK_CAPTURE_ENABLED` 기본값이 `0`이라 기존 운영에 영향 없음을 확인 (compose·`.env.example` 모두 `0`)
- [x] Slack 토큰이 `back` 서비스 env로 정확히 이관됨 (누락 시 부팅은 되고 캡처만 비활성 — 부팅 실측 ②로 확인)
- [x] repo 쓰기 마운트가 `back`에 유지됨 (`.:/repo`, worker 만 `:ro`)
- [ ] **운영 배포 시 확인** — 기존 `kknaks-slack-bridge` 컨테이너가 내려가고 중복 연결이 없음 (deploy.yml 의 `docker rm -f` 가 처리하나 첫 배포에서 눈으로 확인 필요)
- [ ] **운영 배포 시 확인** — `SLACK_CAPTURE_ENABLED=1` 환경에서 Slack 멘션 1건 e2e (노트 생성 → 커밋 → reload)

## Rollback

- Phase 2까지 되돌리려면 `app/slack_bridge/run.py`와 compose 서비스를 복구하고 `SLACK_CAPTURE_ENABLED=0`으로 back의 흡수 경로를 끈다.
- Phase 1의 sink 리팩터는 동작이 동일하므로 단독 revert 불필요. 되돌려도 캡처 기능에 영향 없음.
- DB 변경이 없어 migration revert 절차가 없다.

## Done Criteria

- [x] 모든 Phase가 `DONE`이다.
- [x] Slack 캡처가 흡수 전과 동일하게 동작한다(테스트 318 passed · 운영 e2e 는 배포 대기).
- [x] `app/slack_bridge/`와 `slack-bridge` 서비스가 존재하지 않는다.
- [x] store 교체만으로 "파일 쓰기" ↔ "큐 적재"를 바꿀 수 있는 구조가 됐다 (runner 에 파일시스템 접근 0).
- [x] `OKK-SPEC-011` §4가 개정됐다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- ~~웹소켓 task가 반복 실패할 때 back을 종료할지 캡처만 비활성화할지(KDEV-DEC-013 OQ-1).~~ **해소** — **캡처만 비활성화하고 API는 계속 서빙**으로 구현했다. `CaptureRuntime.start()` 가 기동 실패를 잡아 로그만 남기고 `False` 를 반환하며, `_run_forever` 가 루프 예외를 흡수한다. 부팅 3종 실측으로 확인.
- ~~`slack-capture` 프로필 제거 후 로컬 개발 기본값(KDEV-DEC-013 OQ-2).~~ **해소** — `SLACK_CAPTURE_ENABLED=0` 유지로 충분하다. 값이 `1`이어도 토큰이 없으면 경고 후 skip 하므로 로컬에서 별도 조치가 필요 없다.
- ~~**(신규)** 캡처 루프가 한 번 죽으면 프로세스 재시작 전까지 복구되지 않는다.~~ **해소** — 리뷰에서 흡수 전 대비 **회귀**임이 확인돼(컨테이너 `restart` 에 얹혀 있던 복구가 사라짐) `supervise_connection` 백오프 재기동을 넣었다. 위 Phase 2 완료 증거 참조.
- ~~**(잔여)** 연속 10회 실패로 supervisor 가 포기한 뒤에는 back 재시작 전까지 캡처가 죽어 있다. 알림 연동은 넣지 않았다.~~ **해소** — `notify_slack` 이 이미 있고 `SLACK_WEBHOOK_URL` 미설정 시 no-op 이라 미룰 이유가 없었다. **포기 시 + 기동 실패 시** 둘 다 알린다. 알림 임계 정책(몇 회 실패에 알릴지)은 여전히 DEC-012 OQ-4 와 함께 볼 사안이지만, "조용히 죽는 경로"는 여기서 막았다.
- ~~**(신규)** 캡처 세션 TTL 7일과 `stored_path` 의 관계 — WORK-014 에서 store 가 파일을 안 만들면 스레드 후속의 `existing_markdown` 재읽기가 성립하지 않는다.~~ **해소** — 이건 미래 과제가 아니라 **sink 분리가 덜 된 것**이었다. runner 에 파일 전제가 두 군데(`read_text`, `Path(output_path)`) 남아 있어 WORK-014 가 결국 runner 를 고쳐야 했다. `CaptureStore` 를 양방향(`load_previous` + `store`)으로 닫아 runner 에서 파일시스템 접근을 전부 걷어냈다. 큐 store 는 draft payload 를 돌려주면 되고 runner 는 무변경이다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 후속 WORK-014
