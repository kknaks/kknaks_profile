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
progress: 33
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
| Progress | 33% |
| Blocker | 없음 |
| Next | Phase 1 실운영 확인(배포) → Phase 2 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위 확정 | todo |
| Design | kknaks | 진행 표시 규칙 | todo |
| FE | kknaks | 폴링 + 스피너/비활성화 | todo |
| BE | kknaks | 제출/수확 분리 | done (P1) |
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

- 스테이지 실행을 **제출/수확**으로 분리 (`submit` → `status` 폴링 → 결과 파싱·검증)
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

기존 컬럼으로 충분하다 — `ai_tasks.external_task_ref`(task_id) · `status`,
`gates.status=generating`, `gate_revisions.status=drafting`.

- Migration 필요 여부: **불필요**

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

- **Status**: TODO
- **작업**:
  - [ ] `prepare_item` 의 요약 호출을 제출/수확으로
  - [ ] Slack 접수 회신을 "접수됨 — 준비 중" 으로
- **검증**:
  - [ ] 접수 회신이 즉시 온다
  - [ ] 준비 완료 시 `in_review` 로 전이하고 첫 게이트가 열린다
- **완료 증거**: 미작성

### Phase 3 — 화면 (FE)

- **Status**: TODO
- **작업**:
  - [ ] `generating`·`preparing` 이면 자동 폴링(3~5초)
  - [ ] 모든 액션 버튼에 스피너 + 진행 중 문구
  - [ ] 진행 중에는 **삭제 포함 전 버튼 비활성화**
  - [ ] 실패 시 사유와 `재시도` 노출
- **검증**:
  - [ ] 버튼을 눌렀는지 화면만 보고 알 수 있다
  - [ ] 진행 중 삭제가 눌리지 않는다
  - [ ] 폴링이 완료를 감지해 카드가 저절로 열린다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 진행 중이던 항목(#3)이 개편 후에도 이어서 승인된다

## Rollback

되돌리면 다시 타임아웃에 막힌다 — 롤백 대상이 아니라 **고쳐야 하는 결함**이다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 이다.
- [ ] `source_note` → `concept` → `derived` 승인이 끊김 없이 진행된다.
- [ ] 버튼을 눌렀는지 화면만 보고 알 수 있다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- 폴링 주기와 중단 조건(무한 폴링 방지) — 실사용 후 조정한다.
- ~~실행기 큐에 남은 작업의 만료 처리~~ — P1 에서 정했다. 실행 나이가 `capture_timeout_seconds`
  를 넘으면 수확이 `EXECUTION_TIMEOUT` 으로 닫고 `재시도` 를 연다. 무한 `generating` 을 막는 값이다.
- **실행기 결과 TTL 1시간**(open-kknaks `result_ttl` 기본값). 그 안에 수확하지 못하면
  `TASK_NOT_FOUND` 로 실패한다 — 화면이 오래 닫혀 있던 경우에 걸린다. 폴링 주기와 함께 볼 값.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 선행 WORK-015
