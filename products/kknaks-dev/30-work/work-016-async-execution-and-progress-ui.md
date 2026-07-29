---
type: work
id: KDEV-WORK-016
title: "비동기 실행 + 진행 표시 UI"
status: in_progress
product: kknaks-dev
work_type: refactor
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 90
created_at: 2026-07-29
updated_at: 2026-07-29
tags:
  - product/kknaks-dev
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
    - "[[spec-009-gate-feedback|KDEV-SPEC-009]]"
    - "[[spec-007-approval-queue|KDEV-SPEC-007]]"
  works:
    - "[[work-015-youtube-chain-and-executor|KDEV-WORK-015]]"
  releases: []
  related: []
---

# 비동기 실행 + 진행 표시 UI

AI 호출을 사용자 요청 안에서 기다리지 않게 하고, 화면이 진행 상태를 말하게 한다.

> 만들지 않는 것: 새 게이트 종류, 발행 로직 변경. **실행 방식과 표시**만 바꾼다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-009(실행 계약) · KDEV-SPEC-008(승인 응답)
- Depends on work: WORK-015
- External dependency: open-kknaks `submit`/`status`/`result`

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner | kknaks |
| Status | in_progress |
| Progress | 90% |
| Blocker | 없음 |
| Next | 배포 → 실운영 확인 (항목 #3 완주) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위 확정 | todo |
| Design | kknaks | 진행 표시 규칙 | done |
| FE | kknaks | 폴링 + 스피너/비활성화 | done |
| BE | kknaks | 제출/수확 분리 | done (P1·P2) |
| QA | kknaks | 취소·중복·재시작 시나리오 | todo |
| Ops | kknaks | 실운영 확인 | todo |

## 배경 — 실운영에서 막혔다

`source_note` 승인이 **한 번도 성공하지 못했다.** 로그에 `OPTIONS` 만 남고 `POST` 가
없었고, DB 에는 아무 흔적이 없었다.

원인은 승인 요청이 **다음 게이트의 AI 호출까지 기다리는** 구조였다. 30~60초가 걸리는데
앞단 프록시가 먼저 끊고, 그러면 FastAPI 가 요청을 취소하며 **트랜잭션이 롤백돼 승인
자체가 사라진다.** 사용자는 여러 번 눌러도 진행이 안 되는 것만 본다.

`route` 승인은 우연히 통과했다 — 그 다음 제안(source_note)이 제때 끝났기 때문이다.
concept 는 레포를 읽어 더 느려서 매번 끊겼다.

**스피너로 해결되지 않는다.** 요청 자체가 완료될 수 없는 구조였다.

## Scope

포함:

- 스테이지 실행을 **제출/수확**으로 분리 (`submit` → 완료 대기 → 결과 파싱·검증)
- **대기를 요청 밖으로** — 수집(HTTP)까지 포함해 요청에는 동기 실행을 남기지 않는다
- 승인·준비 재시도·재생성이 **즉시 응답**
- 게이트 조회 시 수확 (멱등)
- 화면 폴링 + 스피너 + 진행 중 비활성화
- 진행 중 삭제 차단

제외:

- 게이트 종류·발행 로직 변경
- 실행기(open-kknaks) 자체 변경

## Code Surface

| 경로 | 설명 |
|---|---|
| `app/back/service/pipeline/stages/*.py` | `result()` 대기 제거 → `submit` 까지만 |
| `app/back/service/pipeline/gates.py` | 제출/수확 분리 |
| `app/back/service/pipeline/prepare.py` | 준비도 같은 방식 |
| `app/back/api/routers/queue.py` | 승인 즉시 응답, 조회 시 수확 |
| `app/front/.../queue/page.tsx` | 폴링 |
| `app/front/components/admin/queue-gate.tsx` | 스피너·비활성화 |

## Domain / Schema

게이트 쪽은 기존 컬럼으로 충분했다 — `ai_tasks.external_task_ref`(task_id) · `status`,
`gates.status=generating`, `gate_revisions.status=drafting`.

**준비 쪽은 아니었다.** `item_preparations.status` 가 `succeeded`·`failed` 뿐이라
*"수집은 끝났고 요약이 아직 큐에 있는"* 구간을 담을 자리가 없었다. 그 행이 없으면
수집 결과를 어디에도 두지 못해 **back 재시작 시 수확할 재료가 사라진다.**
게이트 버전의 `drafting` 과 같은 자리를 만든다.

- Migration 필요 여부: **P1 불필요 · P2 필요** — `0006_preparation_running`
  (`ck_item_preparations_status` 에 `running` 추가). 컨테이너 기동 시
  `entrypoint.sh` 가 `alembic upgrade head` 를 돌리므로 배포에 별도 절차는 없다.

## Execution

### Phase 1 — 제출/수확 분리 (BE)

- **Status**: DONE (코드·테스트) / 실운영 확인 대기
- **작업**:
  - [x] 스테이지에서 `result()` 대기 제거 — `submit` 이 낸 `task_id` 반환
  - [x] `AITask` 에 `external_task_ref` + `running` 저장하고 커밋
  - [x] 수확 함수 — `status(task_id)` 확인 → 완료면 결과 파싱·검증 → `reviewable`
  - [x] 수확은 **멱등** (폴링 겹쳐도 두 번 채워지지 않음)
  - [x] 실패는 `AITask=failed` · `Gate=failed` + 기록 보존
- **검증**:
  - [ ] 승인 응답이 1초 안에 끝난다 — **실운영 측정은 배포 후**
  - [x] 게이트 조회를 두 번 해도 revision 이 하나만 생긴다
  - [x] back 재시작 후에도 진행 중 작업을 이어 수확한다
- **완료 증거**:
  - 새 파일 `app/back/service/pipeline/executor.py` — `Execution`·`poll_execution`·`AgentStage`.
    제출/폴링 절차를 한 곳에 두고, 스테이지는 `prompt`·`payload`·`parse` 셋만 채운다.
  - `gates.py`: `_generate` → `_submit`(제출까지) + `harvest`(수확). 수확은 `drafting`
    버전을 `FOR UPDATE` 로 잡아 폴링이 겹쳐도 한 번만 채운다.
  - `queue.py`: `GET /items/{id}/gates` 가 진행 중 게이트를 수확한다. 실행기에 못 닿아도
    목록은 그대로 내려간다.
  - 스테이지 계약이 callable → `StageRunner`(submit·poll·parse) 로 바뀌었다.
    `Generator` 타입과 `generator=` 인자는 전부 `StageRunner`·`runner=` 로 대체.
  - 테스트 605 passed / 3 skipped. 새 테스트: `test_prepare_success_opens_route_gate`(제출만),
    `test_harvest_fills_the_proposal`, `test_harvest_is_idempotent`,
    `test_running_execution_changes_nothing`, `test_harvest_resumes_after_restart`,
    `test_regeneration_responds_before_the_new_version_exists`,
    `test_submit_failure_is_a_state_not_an_exception`, `test_generating_gate_cannot_be_approved`.

### Phase 2 — 준비 단계도 비동기 (BE)

- **Status**: DONE (코드·테스트) / 실운영 확인 대기
- **작업**:
  - [x] `prepare_item` 의 요약 호출을 제출/수확으로
  - [x] Slack 접수 회신을 "접수됨 — 준비 중" 으로
- **검증**:
  - [x] 접수 회신이 즉시 온다 — 요약을 기다리지 않는다 (수집 시간은 남는다, 아래 주석)
  - [x] 준비 완료 시 `in_review` 로 전이하고 첫 게이트가 열린다
- **완료 증거**:
  - `prepare_item` → `submit_preparation`(수집 + 요약 제출) + `harvest_preparation`(수확).
    수집 결과는 `running` 준비 버전에 **제출 시점에 저장**된다 — 그래야 재시작 뒤에도
    수확할 재료가 남는다.
  - `flow.py` 가 `start_preparation` / `harvest_preparation` 둘로 갈렸다.
    "준비가 끝나면 첫 게이트가 열린다" 는 이제 **수확 쪽**에 있다.
  - `AgentSummarizer` 도 `submit`·`poll`·`parse` 로 나뉜다. 게이트 스테이지와 입력이
    달라(`GenerationInput` 이 없다) 같은 기반 클래스에 넣지 않고 폴링만 공유한다.
  - 수확 지점 셋: `GET /items` · `GET /items/{id}` · `GET /items/{id}/gates`.
    게이트 목록도 **준비부터** 본다 — 준비 중인 항목은 게이트가 없어서, 건너뛰면
    그 화면만 보는 사람은 영영 진행되지 않는다.
  - `QueueIntakeRunner` 에서 `runner`(route 제안기) 인자를 뺐다. 첫 게이트를 여는 것이
    수확 쪽으로 갔으므로 접수 경로에는 더 이상 쓰이지 않는다 — 죽은 인자는 남기지 않는다.
  - 실패 코드를 뭉뚱그리지 않는다. `TASK_NOT_FOUND` 와 `EXECUTION_TIMEOUT` 은 사람이
    할 일이 다르다.
  - 611 passed / 3 skipped. 신규 `TestAsyncPreparation` 6건(제출만·수확+첫 게이트·
    진행 중 무변화·멱등·재시작 후 수확·실패는 같은 버전을 닫는다).

> **수집(`fetch`)은 여전히 제출 경로 안에서 돈다.** AI 가 아니라 HTTP 이고 상한이 15초라
> 실행기 큐에 넣을 대상이 아니라고 봤다. 접수 회신은 그만큼 늦는다 — Slack 은 먼저
> `⏳ 큐에 넣는 중입니다` 를 띄우므로 체감은 가려지지만, 실측해서 오래 걸리면 다시 본다.

### Phase 2.5 — 대기를 요청 밖으로 (BE)

> 발주에 없던 단계다. P1·P2 는 실행을 제출/수확으로 갈랐지만 **수확을 화면 조회에만
> 걸어 두었다.** 그러면 아무도 화면을 안 여는 시간대에 실행기 결과가 만료돼(보관 1시간)
> 이미 끝난 요약을 다시 돌려야 한다. owner 지적으로 잡았다.
>
> 처음에 주기 스케줄러를 제안했는데 그건 잘못이었다. 실행기는 **완료를 알려 준다** —
> 실행 중 결과 스트림에 이벤트를 흘리고, 클라이언트가 블로킹 read 로 기다리다 깨어난다.
> 원래 코드의 `await client.result(task_id)` 는 버릴 것이 아니라 **요청 밖으로 옮길
> 것**이었다. 폴링할 이유가 없다.

- **Status**: DONE (코드·테스트) / 실운영 확인 대기
- **작업**:
  - [x] `PipelineDriver` — 항목 하나를 요청 밖에서 민다 (`service/pipeline/driver.py`)
  - [x] `await_execution` — 실행기 스트림으로 완료 대기 (폴링 아님)
  - [x] 수집(`fetch`)도 드라이버로 — 요청에는 동기 실행이 남지 않는다
  - [x] 접수·재시도·승인·재생성이 커밋 뒤 드라이버에 넘긴다 (`runtime.follow`)
  - [x] 부팅 복구 — 진행 중이던 항목을 다시 따라붙는다 (`recover`)
  - [x] 조회 시 수확은 **안전망으로 유지**
- **검증**:
  - [x] 접수 하나로 수집 → 요약 → 첫 게이트 제안까지 간다
  - [x] 게이트가 열리면 멈춘다 — 승인 없이 다음 스테이지로 넘어가지 않는다
  - [x] 재시작해도 이어붙는다
  - [x] 드라이버가 터져도 예외가 새어 나오지 않고 상태로 남는다
- **완료 증거**:
  - `driver.py` — 항목당 태스크 하나, 최대 걸음 수 상한, 예외는 삼키고 로그.
    수확 지점이 셋이 됐다: **드라이버(주)** · 조회 시(안전망) · 부팅 복구.
  - `executor.await_execution`(대기) 와 `poll_execution`(조회) 이 같은 `read_execution`
    을 공유한다 — 상태 해석이 두 벌이 되면 조용히 갈라진다.
  - Slack 접수는 이제 **행만 만든다.** 수집도 요약도 하지 않아 회신이 즉시 나간다.
  - `POST /items/{id}/prepare` 도 다시 대기줄에 세우기만 한다(`received`).
  - `runtime.follow` 가 `async` 인 것은 테스트가 인라인으로 밀어 결정적으로 검증하기
    위해서다. 실 드라이버는 태스크만 만들고 즉시 돌아온다.
  - 618 passed / 3 skipped. 신규 `test_pipeline_driver.py` 7건.

### Phase 3 — 화면 (FE)

- **Status**: DONE (코드) / 실운영 확인 대기
- **작업**:
  - [x] `generating`·`preparing` 이면 자동 폴링(4초)
  - [x] 모든 액션 버튼에 스피너 + 진행 중 문구
  - [x] 진행 중에는 **삭제 포함 전 버튼 비활성화**
  - [x] 실패 시 사유와 `재시도` 노출
- **검증**:
  - [x] 버튼을 눌렀는지 화면만 보고 알 수 있다 (코드 기준 — 육안은 배포 후)
  - [x] 진행 중 삭제가 눌리지 않는다 — `locked` 에 `running` 포함
  - [ ] 폴링이 완료를 감지해 카드가 저절로 열린다 — **실운영 확인 필요**
- **완료 증거**:
  - **두 가지 「진행 중」을 분리했다.** `busy`(내 요청이 나가 있는 1초 남짓)와
    서버 상태(`preparing`·`generating`, 30~60초)는 다른 것이다. 섞으면 "버튼이 안
    먹은 것"과 "AI 가 도는 것"이 같은 모양이 되어 사람이 다시 누른다.
  - 종전 문구가 이제 거짓이 됐다 — 「승인 중… 다음 단계를 만드는 중입니다 (최대 1분)」,
    「이 창을 닫지 마세요」. 요청은 1초 안에 끝나고 **창을 닫아도 서버가 계속 민다.**
    문구를 사실에 맞췄다.
  - 폴링은 `setTimeout` 체인이다. `setInterval` 은 응답이 늦으면 요청을 쌓는다.
    진행 중인 것이 없으면 아예 돌지 않는다.
  - **폴링 주기가 진행 속도를 정하지 않는다.** 서버(드라이버)가 스스로 밀기 때문에
    4초는 "화면이 얼마나 빨리 따라붙는가"일 뿐이다. P2.5 전이었다면 이 값이 곧
    파이프라인 속도였다.
  - `준비 재시도` 버튼을 `prepare_failed` 에서만 띄운다 — `received` 는 드라이버가
    자동으로 집어간다.
  - `npm run build` green, `tsc --noEmit` green. **FE 자동 테스트는 없다**(테스트 러너
    미설치) — 화면 동작은 배포 후 육안 확인이 유일한 검증이다.

## Pre-deploy Check

- [ ] 진행 중이던 항목(#3)이 개편 후에도 이어서 승인된다
- [x] 마이그레이션 `0006` 은 `entrypoint.sh` 의 `alembic upgrade head` 가 자동 적용한다
- [x] 부팅 시 `PipelineDriver.recover()` 가 진행 중이던 항목을 다시 따라붙는다

## Rollback

되돌리면 다시 타임아웃에 막힌다 — 롤백 대상이 아니라 **고쳐야 하는 결함**이다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 이다.
- [ ] `source_note` → `concept` → `derived` 승인이 끊김 없이 진행된다.
- [ ] 버튼을 눌렀는지 화면만 보고 알 수 있다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- ~~수확 지점이 화면뿐이다~~ — P2.5 에서 드라이버가 주 경로가 됐다. 화면 조회는
  안전망으로 남는다.

- 폴링 주기와 중단 조건(무한 폴링 방지) — 실사용 후 조정한다.
- ~~실행기 큐에 남은 작업의 만료 처리~~ — P1 에서 정했다. 실행 나이가 `capture_timeout_seconds`
  를 넘으면 수확이 `EXECUTION_TIMEOUT` 으로 닫고 `재시도` 를 연다. 무한 `generating` 을 막는 값이다.
- **실행기 결과 TTL 1시간**(open-kknaks `result_ttl` 기본값, 워커 CLI 에 노브 없음).
  드라이버가 완료 즉시 수확하므로 정상 경로에서는 닿지 않는다. **back 이 1시간 넘게
  죽어 있다가 뜨면** 그 사이 끝난 실행은 잃는다 — 재시도로 푼다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-015
