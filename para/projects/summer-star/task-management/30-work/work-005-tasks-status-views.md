---
type: work
id: WORK-005
title: "내 업무 — 상태 전이 · 완료 게이트 단일 엔드포인트 · 리스트/칸반"
status: todo
product: "task-management"
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-06
updated_at: 2026-09-06
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-002]
  decisions: [DEC-002]
  specs: [SPEC-004]
  works: [WORK-003, WORK-004]
  releases: []
  related: [DEC-001, DEC-005]
---

# 내 업무 — 상태 전이 · 완료 게이트 단일 엔드포인트 · 리스트/칸반

**업무를 완료까지 보내고, 리스트와 칸반을 오간다.** 완료는 그냥 되지 않는다 — 세 진입점이 **같은 엔드포인트 하나**를 지나고 서비스가 판정한다. 업무 생성·상세 편집은 만들지 않는다(WORK-004).

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-002
- Covers spec: **SPEC-004**(내 업무 — 상태 전이 · 완료 게이트 · 리스트/칸반)
- Depends on work: **WORK-004**(`task` 도메인 · `task_service` · 상세 드로어 · `TaskDetailBody` · `DrawerFrame` · `StatusDot` · 상세 헤더의 상태 컨트롤 자리) · **WORK-003**(동적 유형 목록 — 유형 탭이 이 목록을 그린다)
- Parallel work: 없음
- Follow-up work: **WORK-008**(회의록의 「업무 갱신」이 **네 번째 진입점**으로 이 엔드포인트를 지난다) · 캘린더 그룹(취소·삭제된 업무를 캘린더에서 거른다)
- **External dependency**: **코드 레포는 별도다** — `github.com/kknaks/task_management`. 그 밖의 외부 의존은 없다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-004 미완 |
| Next | Phase 1 — 상태 전이 · 완료 게이트 · 실행취소 · 소프트 딜리트 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-004 §6 Acceptance 18개 대조 | todo |
| Design |  | 상태 팝오버 · 칸반 DnD 규격 · 취소/삭제 모달 · 빈 상태 3종 · 지연 뱃지 · 스켈레톤 | todo |
| FE |  | 리스트·칸반 · 세 진입점 · DnD · 토스트/실행취소 · 필터·정렬·기간 쿼리 | todo |
| BE |  | **상태 전이 전용 엔드포인트**(게이트·전이 그래프·로그) · 실행취소 · 목록 조회·집계 · 소프트 딜리트 | todo |
| QA |  | Phase 검증(앱 창 E2E) · **세 진입점 동일 요청 실측** · 정적 검사 | todo |
| Ops |  | 해당 없음(신규 env 없음) | todo |

## Scope

포함:

- **상태 전이 전용 엔드포인트** — 전이 그래프 검사 + **완료 게이트 판정** + `task_log` 한 줄(같은 트랜잭션)
- **실행취소**(마지막 전이 되돌리기 + 그 로그 삭제, 4초 제한) · **소프트 딜리트**
- 목록 조회 — 기간·유형·상태·프로젝트 필터 · 정렬 3종 · 페이지네이션 · **`typeCounts` 집계** · 파생값(`dDay`·`isOverdue`·`overdueDays`·`memoCount`·`todoProgress`)
- **세 진입점** — 리스트 상태 셀 팝오버 · 상세 헤더 드롭다운 · **칸반 DnD**
- 취소 모달(600, 사유 칩 4 + 로그 기록 체크) · 삭제 확인 모달(600) · 카드/행 **컨텍스트 메뉴**
- **리스트 뷰**(컬럼 5 · 유형 탭 · 페이지네이션) · **칸반 뷰**(4컬럼 · DnD) · 뷰 전환(`?view=`)
- 필터·정렬·기간 스테퍼 · **빈 상태 3종** · **지연 뱃지** · **스켈레톤**
- 완료 토스트 + 실행취소 · 거부 토스트 + 「결과 입력」 유도(WORK-004 의 카드로 스크롤·포커스)
- 내 업무 영역 반응형(1280~1439 메모 컬럼 숨김 · 칸반 320 고정 + 가로 스크롤)

제외:

- 업무 생성·상세 편집·첨부·연관업무 → **WORK-004**
- 캘린더 표시·드래그 → 캘린더 그룹(기한을 바꾸면 일정이 파생된다는 사실은 WORK-004 가 이미 세웠다)
- **회의록에서 오는 상태 변경 요청** → **WORK-008**. 이 work 는 **그 요청이 지날 엔드포인트 하나**만 만든다
- 업무 복원 — **v1 에 없다**(DEC-004 §4)
- 업무 목록 검색 — v1 에 없다(SPEC-003 §7)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `app/back/service/task_service.py` | **`change_status()` 하나** — 전이 그래프 · 완료 게이트 · 로그. **상태를 쓰는 유일한 함수**(§Internal Interface Contract) |
| `app/back/service/task_service.py` (계속) | `undo_last_status()` · `soft_delete()` · `list_tasks()`(필터·정렬·페이지·집계) |
| `app/back/repository/task_repository.py` | 목록 쿼리(**`schedule` 조인 없이 `due_date` 인덱스만**) · 집계 · 마지막 로그 조회 |
| `app/back/core/exceptions.py` | `TaskCompletionBlockedError` · `InvalidStatusTransitionError` · `UndoNotAvailableError` 추가(BE §8-2 계층 그대로) |
| `app/back/api/task_router.py` | `GET /api/tasks` · **`PATCH /api/tasks/{id}/status`** · `POST /api/tasks/{id}/status/undo` · `DELETE /api/tasks/{id}` |
| `app/back/schemas/task.py` · `dto/task.py` | 목록 항목·전이 요청 dto. **일반 `PATCH` 스키마에 `status` 필드를 두지 않는다** |
| `app/back/tests/test_task_status.py` · `test_task_list.py` | BE §12 필수 테스트 1·2 + 목록·집계 |
| `app/front/src/features/tasks/hooks/useTasksViewParams.ts` | WORK-004 가 만든 훅에 `view`·기간·필터·정렬 파싱을 **덧붙인다**(FE §1-2) |
| `app/front/src/features/tasks/hooks/useTasksQuery.ts` · `useTaskStatus.ts` | 목록 쿼리 · **전이 뮤테이션 하나**(세 진입점이 공유) |
| `app/front/src/features/tasks/components/TaskListView.tsx` · `TaskKanbanView.tsx` | P-18 / P-19 |
| `app/front/src/features/tasks/components/TaskRow.tsx` · `TaskCard.tsx` | 행 52px / 카드 w320 |
| `app/front/src/features/tasks/components/StatusPopover.tsx` | **리스트 셀 · 상세 드롭다운 공용**(SPEC-004 U-3) |
| `app/front/src/features/tasks/components/TaskContextMenu.tsx` | 우클릭 팝오버 220(행·카드 공용) |
| `app/front/src/features/tasks/components/CancelModal.tsx` | 취소 모달 600 — `ConfirmModal`(WORK-002) 프레임 위에 사유 칩 슬롯 |
| `app/front/src/features/tasks/components/KanbanBoard.tsx` · `KanbanColumn.tsx` · `useKanbanDnd.ts` | DnD 규격(고스트·플레이스홀더·드롭 가능/불가·놓은 뒤 로딩) |
| `app/front/src/features/tasks/components/OverdueBadge.tsx` · `TaskSkeleton.tsx` | 지연 뱃지 · 스켈레톤 |
| `app/front/src/components/shared/PeriodStepper.tsx` · `UnderlineTabs.tsx` · `FilterChipBar.tsx` · `DataTable.tsx` | 공용(두 영역 이상이 쓴다 — 회의록 목록이 `PeriodStepper` 를 재사용한다) |
| `app/front/src/app/(app)/tasks/layout.tsx` · `page.tsx` | 헤더 + 기간 스테퍼 + 뷰 토글 + 「새 업무」 / 리스트·칸반 분기 |
| `app/front/src/lib/api/queryKeys.ts` | `['tasks','list',{view,filters,period}]` 등록 |

- Domain / schema note: **마이그레이션 없음.** WORK-004 가 만든 `task`·`task_log` 를 그대로 쓴다. `status`·`cancel_reason`·`deleted_at` 은 이미 있다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `task` | `status` · `cancel_reason` · `deleted_at` 을 이 work 가 처음 쓴다 |
| `task_log` | 전이마다 한 줄. **실행취소는 그 줄을 지운다** |

- 상태 / invariant: `domains/task.md` **T-4**(상태 4종 · 「지연」은 컬럼이 아니다) · **T-5**(완료 게이트) · **T-6**(전이 그래프 · 완료→취소 불가) · **T-7**(`cancel_reason` 은 취소일 때만) · **T-8**(전이 = 로그 한 줄, 같은 트랜잭션) · **T-11**(소프트 딜리트, 자식은 안 지운다) · `system/README.md` **§흐름 ②**
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: **`undo_not_available` 코드와 실행취소 엔드포인트**가 아키텍처 §8-2·§10 에 없다(SPEC-004 S004-OQ-1) — 구현은 SPEC-004 §4 를 따르고 표 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-008** | **`PATCH /api/tasks/{id}/status`** 와 그 뒤의 `task_service.change_status()` | 회의록의 「업무 갱신」이 상태를 완료로 보낼 때 **이 하나를 지난다** — 회의록 쪽에 판정 코드를 두지 않는다(BE §8-3) |
| 캘린더 그룹 | 상태 값·취소 표시 규약 · `schedule` 조회에서 취소·삭제분 제외 | 캘린더 점선 칩이 취소 상태를 그린다 |
| WORK-004 | 「결과자료 · 완료 결과」 카드의 **유도 진입 훅** | 거부 토스트의 「결과 입력」이 그 훅을 부른다 — 이 work 가 소비하고, 컴포넌트는 WORK-004 가 소유한다 |

## Internal Interface Contract

외부 계약(엔드포인트·요청/응답·검증·에러)은 **SPEC-004 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **완료 게이트는 단일 판정이다** | `task_service.change_status(task_id, status, cancel_reason?, log_cancel_reason?)` **하나**가 전이 그래프와 완료 게이트를 판정한다. **`task.status` 를 대입하는 코드는 이 함수 안에만 있다.** 리스트 셀·상세 드롭다운·칸반 DnD·(WORK-008 의) 회의록 요청이 **전부 `PATCH /api/tasks/{id}/status` 하나**로 들어온다 |
| **일반 `PATCH` 에 상태를 섞지 않는다** | `TaskUpdateDTO` 에 `status` 필드가 **없다**. `PATCH /api/tasks/{id}` 로 `status` 를 보내면 **422 `validation_error`** 다 — 게이트를 우회하는 경로를 스키마 층에서 막는다(BE §10) |
| 게이트 판정식 | `deliverable 첨부 ≥ 1` **또는** `completion_result` 가 공백 제거 후 1자 이상. 미충족이면 **`TaskCompletionBlockedError`(422)** 이고 **행이 바뀌지 않는다** |
| 전이 그래프 | `todo→in_progress\|done\|cancelled` · `in_progress→done\|todo\|cancelled` · `done→in_progress` · `cancelled→todo`. **`done→cancelled` 불가** → `InvalidStatusTransitionError`(409) |
| 로그와 실행취소 | 전이 성공은 **`task_log` 한 줄과 같은 트랜잭션**(T-8). `undo` 는 ① 마지막 로그가 상태 전이이고 ② 그 뒤 다른 변경이 없고 ③ **4초 이내**일 때만 되며, **직전 상태 복원 + 그 로그 삭제**를 한 트랜잭션에서 한다. 아니면 `UndoNotAvailableError`(409) |
| 파생 「지연」 | **저장하지 않는다.** 조회 시 `due_date < 오늘` + 상태가 `done`·`cancelled` 아님으로 계산해 `isOverdue`·`overdueDays` 로 내려준다(T-4 · G-7). **화면이 다시 계산하지 않는다** |
| `typeCounts` | **기간 + 상태·프로젝트 필터는 반영하고 유형 탭 자신은 반영하지 않는다**(SPEC-004 §4 — 탭 숫자가 탭을 누를 때마다 흔들리지 않게) |
| 목록 쿼리 | 기본 정렬 `due_asc` 이고 **기한 없는 업무는 맨 아래**(NULLS LAST). **`schedule` 을 조인하지 않는다** — `task (account_id, due_date NULLS LAST)` 인덱스만 탄다(DEC-005 §3 개정의 목적) |
| 프론트 전이 뮤테이션 | `useTaskStatus()` **훅 하나**를 세 진입점이 공유한다. 화면마다 호출을 만들지 않는다 — 요청 본문·에러 분기·토스트가 갈리면 「같은 판정」이 화면에서만 깨진다 |
| 낙관적 갱신 | **하지 않는다.** 완료 게이트·전이 그래프가 거부할 수 있다(FE §3-4). 칸반은 **드래그 고스트가 즉각성을 주고**, 놓은 뒤 응답까지 그 자리를 로딩(불투명도 0.6)으로 유지한다 |
| 드롭 차단 vs 서버 판정 | 전이 그래프로 막히는 컬럼은 **드롭 자체를 막는다**(흐림 + `not-allowed`). **완료 컬럼은 드롭을 허용하고 게이트가 서버에서 판정한다** — 결과자료 유무를 화면이 미리 판단해 막으면 서버와 어긋난다(SPEC-004 §5) |
| 조건은 쿼리에 있다 | 기간·유형·상태·프로젝트·정렬·뷰가 전부 `?` 에 남는다(FE §1-2). **컴포넌트가 자체 상태로 들고 있지 않는다** |
| 무효화 | 전이·삭제 뒤 `['tasks', …]` 를 다시 읽는다. **기한이 바뀐 게 아니면 `['schedules']` 를 건드리지 않는다**(FE §3-3 표) |

## Execution

### Phase 1 — 상태 전이 · 완료 게이트 · 실행취소 · 소프트 딜리트 (백엔드)

- **Status**: TODO
- **설명**: **이 work 의 핵심이 여기 있다.** 화면 없이 `curl` 로 전이·게이트·되돌리기·삭제가 돌아야 한다. 판정이 한 곳에 모여 있는지를 이 Phase 에서 못박지 않으면, 이후 세 진입점과 회의록이 각자 규칙을 갖게 된다.
- **작업**:
  - [ ] `core/exceptions.py` — `TaskCompletionBlockedError`(422 `task_completion_blocked`) · `InvalidStatusTransitionError`(409) · `UndoNotAvailableError`(409). **`persist_changes` 는 켜지 않는다**(실패가 쓰기를 뜻하지 않는다 — BE §7)
  - [ ] `task_service.change_status()` — **전이 그래프 검사 → 완료 게이트 판정 → 상태 쓰기 + `task_log` INSERT**(한 트랜잭션). 취소면 `cancel_reason` 필수 + `logCancelReason` 기본 참
  - [ ] `task_service.undo_last_status()` — 조건 3개 검사 → 직전 상태 복원 + **그 전이 로그 삭제**
  - [ ] `task_service.soft_delete()` — `deleted_at` 만 채운다. **자식 행을 지우지 않는다**(T-11). `schedule` 행은 그대로 두고 조회에서 원본 조인으로 거른다(§3-3)
  - [ ] `api/task_router.py` — `PATCH /{id}/status` · `POST /{id}/status/undo` · `DELETE /{id}`
  - [ ] **`TaskUpdateDTO` 와 일반 `PATCH` 스키마에서 `status` 를 제거**(있다면). 보내면 422 가 되게 한다
  - [ ] `tests/test_task_status.py` — BE §12 필수 **1**(게이트 거부 시 상태 불변) · **2**(완료→취소 409) + 실행취소 3조건 + 삭제 후 목록 제외
- **검증**:
  - [ ] 결과자료도 완료 결과도 없는 업무에 `{"status":"done"}` 을 보내면 **422 `task_completion_blocked`** 이고 **DB 의 상태가 그대로**다
  - [ ] 결과자료를 1건 붙이면 같은 요청이 **200** 이고 로그에 「상태 … → 완료」가 생긴다. 결과자료를 지우고 완료 결과만 적어도 **똑같이 200** 이다(둘 중 하나)
  - [ ] 완료 상태에서 `{"status":"cancelled"}` 는 **409 `invalid_status_transition`**
  - [ ] 취소를 사유 없이 보내면 **422**, 완료 상태에 `cancelReason` 을 얹어 보내도 **거부**된다(T-7)
  - [ ] 완료 직후 `undo` 는 **200 + 직전 상태 복원**이고 **그 전이 로그가 사라진다**. 5초 뒤 `undo` 는 **409 `undo_not_available`**
  - [ ] `DELETE` 후 목록에서 빠지지만 **DB 에 행과 자식이 남아 있다**
  - [ ] **`PATCH /api/tasks/{id}` 에 `{"status":"done"}` 을 보내면 422 `validation_error`** 다(게이트 우회 경로가 스키마에서 막힌다)
  - [ ] **정적 검사**: `TaskCompletionBlockedError` 를 던지는 곳이 **1곳**, `task` 의 `status` 에 값을 대입하는 코드가 **`change_status()` 안에만** 있다(grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 목록 조회 · 필터 · 정렬 · 집계 (백엔드)

- **Status**: TODO
- **설명**: 리스트와 칸반이 **같은 응답**을 본다. 두 뷰에 쿼리를 따로 만들지 않는다 — 칸반은 같은 목록을 상태로 나눠 그릴 뿐이다.
- **작업**:
  - [ ] `repository/task_repository.py` — 기간(`from`·`to`, UTC 경계) · `workTypeId` · `status` · `projectId` · 정렬 3종 · 페이지네이션. **기한 없는 업무는 생성일 기준 달에 속하고 기본 정렬 맨 아래**(T-1-a)
  - [ ] 파생값 — `dDay` · `isOverdue` · `overdueDays` · `memoCount` · `todoProgress`
  - [ ] `typeCounts` — **유형 탭 자신은 반영하지 않는 집계**
  - [ ] `GET /api/tasks` + `TaskListResponse`(`items`·`total`·`page`·`size`·`typeCounts`)
  - [ ] `tests/test_task_list.py` + **실행 계획 확인**(BE §12 5-a)
- **검증**:
  - [ ] 기본 호출이 **이번 달**을 주고, `from`·`to` 로 지난달을 부르면 그 달만 온다
  - [ ] 유형 탭 필터를 걸어도 **`typeCounts` 의 숫자가 바뀌지 않고**, 상태 필터를 걸면 **바뀐다**
  - [ ] 기한 없는 업무가 `due_asc` 에서 **맨 아래**에 온다
  - [ ] 기한이 어제인 진행중 업무에 `isOverdue: true` · `overdueDays: 1` 이 실려 오고, 완료로 보내면 **`false`** 가 된다
  - [ ] 소프트 딜리트된 업무가 **응답에 없다**
  - [ ] **정적 검사(실측)**: `EXPLAIN` 결과에 **`schedule` 이 등장하지 않는다**(BE §12 5-a — 출력을 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — 리스트 뷰 · 상태 팝오버 · 컨텍스트 메뉴 · 취소/삭제 모달 · 완료 토스트

- **Status**: TODO
- **설명**: **앱 창에서 업무를 완료까지 보내는** 단계. 세 진입점 중 둘(리스트 셀 · 상세 드롭다운)이 여기서 붙고, 셋째(칸반 DnD)는 Phase 4 에서 **같은 훅**에 연결된다.
- **작업**:
  - [ ] `useTasksViewParams` 에 기간·유형·상태·프로젝트·정렬·뷰 파싱 추가 · `useTasksQuery` · **`useTaskStatus()` 전이 훅 하나**
  - [ ] `tasks/layout.tsx` — 타이틀 + **기간 스테퍼**(항상 노출) + 뷰 토글(**선택은 `#F4F5FF`+`#4B52A8`**, Ink 아님) + 정렬·필터 + 「새 업무」
  - [ ] **유형 탭**(전체 + 동적 유형, 선택 밑줄 `#1E1E1E` — **화면당 Ink 는 이 축 하나뿐**)
  - [ ] `TaskListView` — 컬럼 5(업무명 flex · 유형 170 · 상태 140 · 기한 200 · 메모 120) · 행 52 · 하단 카운트 + 페이지네이션
  - [ ] `StatusPopover` — 항목 4 + 구분선, 현재 값 배경, **전이 불가 항목 비활성 + 캡션**. **상세 헤더 드롭다운에도 같은 컴포넌트를 붙인다**(WORK-004 가 비활성으로 그려 둔 자리)
  - [ ] `TaskContextMenu` 220 — 행 우클릭. 「열기」/상태 4/「삭제」. **행 끝에 `⋯` 를 따로 두지 않는다**
  - [ ] `CancelModal` 600 — 사유 칩 4 + 직접 입력 + 「취소 사유를 로그에 기록」(기본 켜짐). 팝오버를 **먼저 닫고** 연다
  - [ ] 삭제 확인 모달 600 — `ConfirmModal` 재사용, 경고 슬롯 「**v1 에는 복원 화면이 없습니다.**」
  - [ ] 완료 토스트(400×56 · 4초 · 「실행취소」) · **거부 토스트**(6초 · 「결과 입력」 → WORK-004 카드로 스크롤·포커스)
  - [ ] 빈 상태 3종 · 지연 뱃지 · 스켈레톤 · 필터 칩 「필터 n ✕」
  - [ ] 반응형 — 1280~1439 **메모 컬럼 숨김**
- **검증**:
  - [ ] 리스트 상태 셀에서 「진행중」을 고르면 셀이 바뀌고 상세 로그에 「**상태 시작전 → 진행중**」이 생긴다
  - [ ] 결과 없는 업무를 **리스트 셀**에서 완료로 보내면 상태가 그대로이고 「**완료하려면 결과자료 1건 또는 완료 결과가 필요합니다**」가 뜬다
  - [ ] 같은 업무를 **상세 드롭다운**에서 완료로 보내도 **같은 문구로 거부**된다
  - [ ] **네트워크 탭 실측**: 두 진입점이 낸 요청이 **같은 경로(`PATCH /api/tasks/{id}/status`)·같은 본문**이다(캡처를 완료 증거에)
  - [ ] 거부 토스트의 「**결과 입력**」을 누르면 그 업무 상세가 열리고 **완료 결과 입력에 포커스**가 잡힌다
  - [ ] 완료 결과를 적은 뒤 완료로 보내면 완료되고 「완료 처리했습니다 · 실행취소」가 **4초** 뜬다
  - [ ] **실행취소**를 누르면 직전 상태로 돌아가고 **완료 로그도 사라진다**. 4초 뒤 시도하면 「되돌릴 수 있는 시간이 지났습니다」
  - [ ] 진행중에서 「취소」를 고르면 **취소 모달(600)** 이 뜨고, 사유 없이는 「업무 취소」가 눌리지 않는다. 취소하면 제목에 **취소선**이 생기고 **목록에 남는다**
  - [ ] 행 우클릭 → 「삭제」 → 모달에 「**v1 에는 복원 화면이 없습니다**」가 보이고, 삭제하면 목록에서 **사라진다**
  - [ ] 기한이 지난 진행중 업무에 「**n일 지남**」이 붉게 보이고 상태 셀은 「진행중」 그대로다
  - [ ] 유형 탭 + 상태 필터를 함께 걸면 **둘 다 만족하는 것만** 남고, 없으면 「조건에 맞는 업무가 없습니다 · 필터 지우기」가 보인다
  - [ ] 첫 로딩에 **스켈레톤**이 뜨고, 필터를 바꿀 때는 **이전 결과가 유지된 채** 진행 표시만 뜬다
  - [ ] **서버를 내린 채** 목록을 열면 **빈 목록이 아니라** 실패 표시 + 「다시 시도」다. 「다시 시도」는 **요청을 한 번만** 보낸다(네트워크 탭)
  - [ ] 창을 1280~1439 로 줄이면 **메모 컬럼이 숨는다**
  - [ ] **정적 검사**: 화면당 `--tm-ink` 를 쓰는 컴포넌트가 **유형 탭 하나**다(뷰 토글이 Ink 를 쓰지 않는다 — FE §5-2. grep 결과를 완료 증거에)
- **완료 증거**: 미작성

### Phase 4 — 칸반 뷰 · DnD · 뷰 전환

- **Status**: TODO
- **설명**: 세 번째 진입점을 **같은 훅에** 붙인다. DnD 는 새 경로가 아니라 같은 요청의 다른 조작 방식이다 — 여기서 규칙이 갈리면 게이트가 화면에서만 깨진다.
- **작업**:
  - [ ] `KanbanBoard`·`KanbanColumn`·`TaskCard` — 4컬럼(시작전/진행중/완료/취소) · 컬럼 `#F9FAFB` r16 · 카드 w320 r8
  - [ ] 완료 컬럼 헤더 「8월 12」 + 하단 캡션, 취소 컬럼 카드에 취소일·사유
  - [ ] `useKanbanDnd` — 고스트(그림자만, **회전 없음**) · 원래 자리 **점선 플레이스홀더**(`#C9D1FB`/`#F8FAFF`) · 드롭 가능 컬럼(`#F1F2FE` + `#7181F8` 테두리 + 삽입 가이드선) · **드롭 불가 컬럼 불투명도 0.5 + `not-allowed` + 툴팁**
  - [ ] 놓은 직후 **로딩 유지**(카드 불투명도 0.6) → 응답 후 이동. 실패면 **원위치** + 사유 토스트
  - [ ] 카드 우클릭 → `TaskContextMenu`(Phase 3 것 재사용) · 시작전·진행중 컬럼 하단 「업무 추가」 점선 버튼(**상태는 항상 시작전**)
  - [ ] 뷰 토글 — `?view=list|board`, **기간·유형 조건 유지**
  - [ ] 칸반 헤더 필터는 **프로젝트**(상태 필터를 두지 않는다 — 컬럼이 이미 상태 축)
  - [ ] 빈 컬럼 「없음」 캡션 · 칸반 스켈레톤(컬럼마다 카드 3)
  - [ ] 반응형 — 1280~1439 **컬럼 320 고정 + 가로 스크롤**(리스트로 자동 전환하지 않는다)
- **검증**:
  - [ ] 「시작전」 카드를 잡으면 **고스트**가 따라오고 원래 자리에 **점선 플레이스홀더**가 남는다. 카드가 기울어지지 않는다
  - [ ] 「진행중」 컬럼 위에서 컬럼이 선택 색이 되고 **삽입 가이드선**이 보인다. 놓으면 **잠깐 로딩**이었다가 들어간다
  - [ ] 결과 없는 업무를 **완료 컬럼으로 끌어 놓으면** 카드가 **원래 컬럼으로 돌아가고** Phase 3 과 **같은 문구**의 거부 토스트가 뜬다
  - [ ] **네트워크 탭 실측**: DnD 가 낸 요청이 리스트 셀·상세 드롭다운과 **같은 경로·같은 본문**이다 — 세 진입점 캡처 3장을 완료 증거에 나란히 붙인다
  - [ ] 완료 카드를 **취소 컬럼으로 끌면 놓이지 않고** 툴팁이 이유를 알린다. 우클릭 메뉴의 「취소」도 **비활성**이다
  - [ ] 「칸반」으로 바꿔도 **기간·유형 조건이 유지**되고 **새로고침해도 그대로**다
  - [ ] 칸반 「업무 추가」로 만든 업무의 상태가 **항상 「시작전」**이다(완료 컬럼에서 열어도 마찬가지)
  - [ ] 창을 1280~1439 로 줄이면 컬럼이 **320 고정 + 가로 스크롤**이고 **리스트로 바뀌지 않는다**
  - [ ] **정적 검사**: `PATCH /api/tasks/{id}/status` 를 호출하는 곳이 **`useTaskStatus.ts` 하나**다(세 진입점이 훅 하나를 공유하는 것의 증명 — grep 결과를 완료 증거에)
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 신규 env 가 없다
- [ ] 목록·전이 응답에 **다른 계정의 업무가 섞이지 않는다**(남의 업무는 404)
- [ ] **삭제가 소프트**이고 하드 삭제 경로가 없다. 복원 엔드포인트도 없다(DEC-004 §4)
- [ ] 실행취소가 **로그를 지우는 유일한 경로**다 — 다른 곳에서 `task_log` 를 DELETE 하지 않는다

## Rollback

- **스키마 변경이 없다** — 되돌릴 마이그레이션이 없다. 잘못 바뀐 상태는 전이로 되돌리고, 소프트 딜리트된 행은 DB 에 남아 있다
- **백엔드**: `PATCH /{id}/status` · `undo` · `DELETE` 라우트를 걷어내면 표면이 사라진다. **그 순간 화면의 세 진입점이 전부 실패 토스트가 된다**(부분적으로 도는 상태가 없다 — 의도한 결과다)
- **프론트**: 브랜치 폐기. `/tasks` 는 WORK-004 의 임시 진입 화면으로 돌아간다 — **WORK-004 의 그 화면을 지우지 않은 채 이 work 를 얹는다**
- 부분 revert 시: Phase 4 만 되돌리면 리스트 뷰와 두 진입점은 그대로 돈다(뷰 토글에서 칸반을 감춘다). **Phase 1 은 단독으로 되돌리지 않는다** — WORK-008 이 이 엔드포인트에 의존한다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-004 §6 Acceptance 18개 항목이 전부 확인**됐다.
- [ ] **세 진입점이 같은 요청을 낸다는 실측 캡처 3장**이 완료 증거에 있다.
- [ ] 정적 검사 4종(상태 대입 격리 · 게이트 예외 단일 · 전이 호출 단일 · Ink 하나) 결과가 완료 증거에 붙어 있다.
- [ ] BE §12 필수 테스트 **1(완료 게이트)·2(전이 그래프)** 와 FE §11 필수 테스트 **1(게이트 시 셀 불변)** 이 통과한다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- ~~**`undo_not_available` 코드와 실행취소 엔드포인트가 아키텍처 §8-2·§10 에 없다**(SPEC-004 S004-OQ-1)~~ → **닫힘(2026-09-06)**. 코디가 §8-2 에 `undo_not_available`(409, 조건 3개와 4초 근거 포함)을, §10 에 `/status/undo` 와 **일반 PATCH 로 상태를 못 보내는 스키마 강제**를 올렸다. 4초는 완료 토스트 수명과 맞춘 spec 값이다
- **뷰 전환 색·칸반 헤더 필터·정렬 옵션 3종·`typeCounts` 정의가 spec 판단이다**(S004-OQ-2~5). 디자인 원본(07-list-kanban) 정정과 DEC-002 갱신이 필요하다
- **완료 게이트의 네 번째 진입점(회의록)은 WORK-008 이 붙인다.** 이 work 는 엔드포인트와 판정만 세우고, 우회하지 않는지를 **WORK-008 이 검증 항목으로** 확인한다
- **취소된 업무가 캘린더·겹침 검사에서 빠지는 것**은 WORK-004 의 `schedule_service` 가 이미 처리하는 조건이다. 이 work 에서 상태가 처음 `cancelled` 로 갈 수 있게 되므로 **그 경로가 실제로 도는지는 캘린더 그룹에서 다시 확인**해야 한다
- **업무 복원 화면을 만들지 않았다**(DEC-004 §4). 실수로 지운 업무는 DB 에는 남지만 사용자가 되살릴 방법이 없다

## Related

- SPEC: SPEC-004 (frontmatter `links.specs`)
- Work: WORK-004 (선행) · WORK-008 (후속 — 같은 엔드포인트를 소비한다)
