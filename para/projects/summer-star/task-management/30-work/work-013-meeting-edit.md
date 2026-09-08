---
type: work
id: WORK-013
title: "편집 · 정리 — payload 드로어 둘 · 칩 둘 갈래 · 자리 유지 · 모달 420 · 유형 설명"
status: done
product: "task-management"
work_type: refactor
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-07
updated_at: 2026-09-07
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-003]
  decisions: [DEC-003, DEC-001]
  specs: [SPEC-008, SPEC-002]
  works: [WORK-003, WORK-008, WORK-012]
  releases: []
  related: [SPEC-003, SPEC-004, DEC-002, WORK-004]
---

# 편집 · 정리 — payload 드로어 둘 · 칩 둘 갈래 · 자리 유지 · 모달 420 · 유형 설명

**「줄에 값을 붙이는 것」과 「업무를 만드는 것」이 갈린다.** 지금은 드로어가 열리면 곧바로 업무가 생기거나(`newTask`) 줄에 저장된 값이 요청이 된다. 이 work 가 끝나면 회의록은 **자기 payload 드로어 둘**을 갖고, **편집 모드 「저장」은 줄에 `payload` 만** 붙이며, **보기 모드 「넣기」만** 업무를 만들거나 바꾼다. 줄 종류 전환이 사라지고, 지운 자리는 그대로 남으며, 확인 모달은 **420 한 문장**이 된다.

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — **MF-13 · 14 · 21 · 25 · 36 · 60 · 61 · 62 · 63 · 64(정정) · 65 · 66 · 67**. 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 #9(편집) · #10(액션 → 업무)
- Covers spec
  - **SPEC-008 U-3 헤더 「편집」 진입 · 줄 버튼 자리** · **U-6**(액션 「업무 생성」 · 업무 「업무 갱신」 · 「갱신 완료」 · dot · 모드별 푸터) · **U-7**(편집 모드 — 종류 셀렉터 **없음** · 안건 추가·삭제 **없음** · 「제거」 + **420 한 문장** · **안건별 추가 칩 넷이 둘로 갈린다**) · **U-8**(줄 추가 드로어 — **논의 · 결정 전용** · 세그먼트 2값) · **U-9**(업무 payload 드로어 — 헤더 업무 셀렉터 + 변경분 일곱) · **U-10**(액션 payload 드로어 — 안건 고정 + 생성분 일곱)
  - **SPEC-008 §4 API Contract** — `POST …/lines`(**`newTask` 없음** · `payload`·`taskId` 는 `action`·`task` 줄에만) · `PATCH …/lines/{lineId}`(**`kind` 안 받음**) · `DELETE …/lines/{lineId}`(**자리 유지**) · `POST …/lines/{lineId}/task` · **`PATCH …/lines/{lineId}/task`(본문 있음 · ①~⑧)** · **§4 Validation** 의 `content`·`kind`·`taskId`·`payload`·「업무 갱신 본문」·「`/task` POST 본문」 행 · **§4 Case Matrix** 의 `validation_error`·`invalid_status_transition`·`task_completion_blocked`(**여기서 나지 않는다**) 행
  - **SPEC-008 §5 구현 규칙** — payload 드로어는 회의록 것 · 한 푸터에 둘 · AI/사람 분기 금지 · `payload` 저장은 `task_service` 미호출 · 낙관적 갱신 자리 · 확인 모달 `size:"light"`
  - **SPEC-002 §4** `description`(유형 설명 — 인라인 행 · 0~200자 · `null` 허용 · 기본 유형도 수정 가능) · **U-3 · U-4** 인라인 행/목록 행
  - **DEC-001 §3**(v1 편집 범위) · **DEC-003 §5**(CRUD) · **ERD M-14 · M-14-a · M-20 · A-12** · **FE §2 규칙 8 · §6 · §6-2** · **BE §12 8-b · 8-c**
- Depends on work: **WORK-012**(리비전 `0008` 이 `payload` 컬럼을 만든다 · `MergedSummary` 다섯 · 최종이 `payload` 를 채운다) · WORK-008(현행 편집 구현) · WORK-003(유형 설정 화면)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: 없음(회의록 재작업 그룹의 마지막 기능 WP). **WORK-014 는 독립**이지만 `AgendaLineTree.tsx` 를 함께 만진다 — **013 을 먼저 머지**한다
- **External dependency**
  - **새 시안이 없다**(MF-67). payload 드로어 둘의 **시각 규격은 이미 만들어진 업무 드로어**(`TaskCreateDrawer` · `TaskDetailDrawer`)의 부품을 **가리켜 조립**한다 — 드로어 840 · 헤더 72 · 푸터 76 · 스크림, 입력 · 셀렉터 · 일정(시작~종료) · 할일 체크리스트 · 메모 · 완료 결과 블록
  - ⛔ **`features/tasks` 의 두 드로어를 수정하지 않는다.** 회의록용 슬롯 prop 을 더하면 반려(FE §2 규칙 8)
  - `RelationPopover`(업무 화면 부품 · 드로어 아님)는 **그대로 재사용**하고 **단일 선택 prop 하나**만 더한다

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 |
| Next | Phase 1 — 스키마 층(`payload` 두 모양 · `kind` 제거 · `newTask` 제거) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-008 §6 AC 의 편집·드로어 관련 14항목 대조 | todo |
| Design |  | **시안 없음** — 두 드로어가 업무 드로어 부품 규격을 그대로 가리키는지 확인만 | — |
| FE |  | Phase 3~5 | todo |
| BE |  | Phase 1~2 | todo |
| QA |  | `payload` 저장에 업무 변화 0 · `done` 422 · `kind` 422 · `newTask` 422 · 논의·결정에 payload 422 · 자리 유지 · 업무 탭 드로어 무변화 | todo |
| Ops |  | 리비전 `0009` · 시드 문구 2건 | todo |

## Scope

포함:

- **`POST …/lines` 재정의** — `newTask` **폐기**. `payload`(와 업무 줄의 `taskId`)를 **`kind ∈ {action, task}` 에만** 받는다(논의·결정에 오면 `422`). **`task_service` 를 부르지 않는다** — 업무는 안 생긴다
- **`PATCH …/lines/{lineId}` 재정의** — `content` · `payload` · `taskId`(업무 줄만). **`kind` 를 받지 않는다**(MF-60 — 스키마 층 422)
- **`payload` 두 모양** — 액션 줄 생성분 `{title, workTypeId?, projectId?, startDate?, dueDate?, description?, todos[]}`(`title` 필수 · `workTypeId` **`null` 허용**) · 업무 줄 변경분 `{dueDate?, status?, note?, todos?, relatedTaskIds?, projectId?, completionResult?}`(**`status ∈ {todo, in_progress}` — `done`·`cancelled` 는 스키마 층 422**)
- **`DELETE …/lines/{lineId}`** — 그 행 하나만 하드 삭제, **`order_index` 를 당기지 않는다**(MF-36)
- **`PATCH …/lines/{lineId}/task` 가 본문을 받는다** — `taskId` 필수 + 변경분. 서버가 한 트랜잭션에서 ①~⑧(상태 · 기한 · 프로젝트 · 메모 · 할일 · 연관 · 완료 결과 · 줄 갱신)
- **`meeting_task_link_service.add_task_line()` 폐기**(`newTask` 갈래가 사라졌다)
- **리비전 `0009`** — `work_type.description text NULL` + **시드 문구 2건**(개인 업무 · 문서·보고. **미팅·회의는 빈 값** — OQ-11 SPEC 대로)
- **프론트 payload 드로어 둘** — `CreateTaskFromLineDrawer.tsx`(→ 액션 payload) · `LinkTaskDrawer.tsx`(→ 업무 payload)를 **수정**한다(폐기 아님). 필드 = `payload` 키 · `prefill` + **`submitMode:"save"|"insert"`** · **인라인 자동 저장 없음** · 푸터 버튼 **둘**(취소 + 하나)
- **편집 모드 정리** — 종류 셀렉터 폐기 · 안건 추가·삭제 버튼 없음(현행 확인) · **추가 칩 둘 갈래**(논의·결정 → 줄 추가 드로어 / 연관 업무·액션 아이템 → payload 드로어 **바로**) · 「제거」 → **`ConfirmModal size:"light"` 420 · 한 문장**
- **유형 설명 필드** — 설정 인라인 추가 행 · 목록 행 인라인 편집(SPEC-002 U-3 · U-4)
- 테스트 — BE §12 **8-b**(자리 유지) · **8-c**(`done` 뒷문 없음) · FE §11(드로어 · 모달 · 자동 저장 실패)

제외:

- **최종 회의록이 `payload` 를 채우는 것** → WORK-012(선행). 이 work 는 **사람이 채우는 길**과 **넣는 길**을 연다
- **`payload` 컬럼 · `MergedSummary` 다섯** → WORK-012 의 리비전 `0008`
- **업무 탭 드로어 · 업무 도메인 규칙** — 손대지 않는다. 상태 전이 · 완료 게이트 판정은 `task_service` 가 이미 갖고 있다
- **breadcrumb · 「←」 · 헤더 순서 · 미리보기 패널** → WORK-014
- **줄 순서 변경 · 안건 삭제 · 줄 종류 전환 · 되돌리기** — 만들지 않는다(MF-36 · 60 · 62 · SPEC-008 U-7)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back` · `app/front`

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/alembic/versions/0009_work_type_description.py` | **신규** | `down_revision = "0008_meeting_payload_terms"`. `work_type.description text NULL` + **기본 유형 2건 UPDATE**(개인 업무 「혼자 처리하는 실무. 개발·수정·확인 등」 · 문서·보고 「산출물이 문서인 것. 기획서·보고서·회의록 정리」). **미팅·회의는 건드리지 않는다** |
| `app/back/models/account.py` `WorkType` | 수정 | `description: Mapped[str \| None]` |
| `app/back/seed/seed.py` | 수정 | `_DefaultWorkType` 에 설명 — 위 2건 + 미팅·회의 `None` |
| `app/back/schemas/setting.py` · `dto/setting.py` · `service/work_type_service.py` | 수정 | `description` 생성·수정·응답. **0~200자 · 줄바꿈 불가 · `null` 허용.** 기본 유형 3종도 `description` 은 바꿀 수 있다 |
| `app/back/schemas/meeting.py` `PendingChange` | **폐기 → 대체** | **`TaskLinePayload`(신규)** — 변경분 일곱 · `status: Literal["todo","in_progress"] \| None`(`done`·`cancelled` 는 스키마 층 422) · `extra="forbid"` |
| 〃 `ActionLinePayload` | **신규** | 생성분 일곱 · `title` 1~200 필수 · `workTypeId` **`null` 허용** · `todos[]` 각 1~200 · `extra="forbid"` |
| 〃 `LineNewTask` | 수정(용도 축소) | **`POST …/lines/{id}/task` 본문 전용**으로 남긴다(`newTask` 갈래는 사라진다). 규칙은 SPEC-003 `POST /api/tasks` 그대로 |
| 〃 `TaskUpdateBody` | **신규** | `PATCH …/lines/{id}/task` 본문 — `taskId` 필수 + 변경분 일곱(`TaskLinePayload` 와 **같은 키·같은 규칙**) |
| 〃 `LineCreate` | 수정 | **`new_task` 필드 삭제.** `payload: ActionLinePayload \| TaskLinePayload \| None` + `task_id`. `kind` 로 모양을 고른다 — 논의·결정에 실리면 `422` |
| 〃 `LineUpdate` | 수정 | **`kind` 필드 삭제**(MF-60). `content` · `payload` · `task_id` |
| 〃 `LineItem` | 수정 | `pending_change` → `payload`(WORK-012 가 이미 이름을 바꿨다 — 여기서는 두 모양 문서화만) |
| `app/back/service/meeting_edit_service.py` `add_line()` | 수정 | `new_task` 분기 · `content = task.title` 덮어쓰기 **삭제**(본문은 사람이 적은 것이다). `payload`·`task_id` 는 `action`·`task` 줄에만 · `content` 는 **네 종류 모두 필수** · `task_id` 는 `task` 줄에만(본인의 삭제 안 된 업무) |
| 〃 `update_line()` | 수정 | **`kind` 전환 분기 전부 삭제.** `content` · `payload` · `task_id` 만 쓴다. **`task_service` 를 부르지 않는다** |
| 〃 `delete_line()` | 수정 | `meeting_line_repository.delete_line(meeting_id, line_id)` — **`agenda_id`·`order_index` 인자 제거**(당김 없음) |
| `app/back/repository/meeting_line_repository.py` `delete_line()` | 수정 | 뒤 줄 `order_index` UPDATE **삭제**. `next_order_index` 는 **`max+1`** 이어야 한다(구멍이 있어도 — 현행 확인) |
| `app/back/service/meeting_task_link_service.py` `add_task_line()` | **폐기** | `newTask` 갈래가 없다 |
| 〃 `apply_pending_change()` → **`apply_task_update()`** | 수정(전면) | **본문을 받는다**(`TaskUpdateBody`). 한 트랜잭션 ① `status` 가 있고 현재와 **다르면** `task_service.change_status()`(같으면 건너뜀) ② `dueDate` ③ `projectId` ④ `note`(메모 **새 항목**) ⑤ `todos`(할일 **추가**) ⑥ `relatedTaskIds`(연관 **추가** · 양방향) ⑦ `completionResult`(덮어쓴다) ⑧ 줄의 `task_id = taskId` · `payload = NULL`. 변경분 0개도 받는다(⑧ 만) |
| 〃 `_stored_change()` | **폐기** | 줄의 저장값을 요청으로 쓰지 않는다 — 사람이 드로어에서 고친 값이 요청이다 |
| 〃 `create_task_from_line()` | 수정(최소) | 그 줄이 `kind='action'` · `task_id` 없음 확인은 그대로. **`content` 를 업무 제목으로 덮어쓰지 않는다** — 줄 본문은 남는다 |
| `app/back/api/meeting_router.py` | 수정 | `PATCH …/lines/{lineId}/task` 가 **본문을 받는다**. 나머지 경로 동일 |
| `app/back/tests/test_meeting_edit.py` · `test_meeting_task_link.py` · `test_work_type.py` | 수정 | 아래 검증 |
| `app/front/src/features/meetings/components/CreateTaskFromLineDrawer.tsx` | **수정(전면 · 폐기 아님)** | **액션 payload 드로어**(U-10) — 안건(맨 위 고정 · 읽기 전용) · 제목 · 유형(필수 · `null` 이면 빈 채로) · 프로젝트 · **계획 시작 ~ 종료** · 설명 · 할일. `prefill`(줄의 `payload`) · `submitMode`. 「회의에서 반영」 표시. **참고자료·연관·첨부·로그·「시작 상태」 없음** |
| 〃 `LinkTaskDrawer.tsx` | **수정(전면 · 폐기 아님)** | **업무 payload 드로어**(U-9) — 헤더 제목 자리가 **업무 셀렉터**(`RelationPopover` 단일 선택) · 본문은 변경분 일곱(내용 · 기한 · 상태(**「완료」·「취소」 없음**) · 진행 메모 · 할일 추가 · 연관 업무 · 프로젝트 · 완료 결과). **업무 미선택이면 본문 비활성.** 「업무 연결」 같은 앞 단계 **없음** |
| 〃 `openMeetingDrawers.tsx` | 수정 | 두 드로어의 열기 함수 시그니처 — `prefill` · `submitMode` · `agendaId` · `line \| null` · 콜백 |
| 〃 `components/LineTaskButton.tsx` | 수정 | 액션 「업무 생성」 / 업무 「업무 갱신」 / 넣기 뒤 「**갱신 완료**」 비활성 · **`payload` 있으면 dot** · 툴팁(변경분 · `status` 가 현재와 같으면 뺀다) |
| 〃 `components/MeetingDetailBody.tsx`(L231~290 부근) | 수정 | 추가 칩 **둘 갈래** — 「+ 논의」·「+ 결정」 → `openAddLineDrawer` / 「+ 연관 업무」·「+ 액션 아이템」 → **payload 드로어 바로**(`submitMode:"save"`). 줄 버튼은 보기 모드 `"insert"` · 편집 모드 `"save"` |
| 〃 `components/LineKindSelector.tsx` | **폐기** | 줄 종류 전환이 없다(MF-60) |
| 〃 `components/LineRow.tsx` | 수정 | `LineKindSelector` import·렌더 삭제 · `onChangeKind` prop 삭제. 라벨은 항상 라벨 |
| 〃 `components/AgendaLineTree.tsx` | 수정 | `onChangeKind` prop · 전달 삭제 |
| 〃 `components/AddLineDrawer.tsx` | 수정 | 종류 세그먼트 **2값**(논의 \| 결정). 「업무」·「액션」 값 삭제. 근거 구간 입력 없음(현행 확인) · 캡션 「비워두면 …AI가 채웁니다」 제거 |
| 〃 `components/LineDeleteModal.tsx` | 수정 | `size:"light"` · 요약 **「되돌릴 수 없습니다.」 한 문장** · **`warning` 슬롯 삭제**(업무 줄이어도 같다) |
| 〃 `components/shared/ConfirmModal.tsx` | 수정 | `size?: "heavy" \| "light"` — `heavy`(기본) 600 · `light` **420**(제목 18/600 + 요약 13/400 + 취소/확인 h32 · **헤더 72 · 푸터 76 없음** · `warning` 슬롯 받지 않음) |
| 〃 `lib/overlay/OverlayProvider.tsx` | 수정 | `openConfirm({..., size})` |
| 〃 `features/tasks/components/RelationPopover.tsx` | 수정(최소) | **단일 선택 prop 하나**(`mode?: "single" \| "multi"`) — `single` 이면 고르는 즉시 닫히고 체크박스 대신 선택 표시. **그 밖은 그대로**(업무 화면 동작 불변) |
| 〃 `hooks/useMeetingTaskLink.tsx` · `useMeetingEdit.tsx` | 수정 | `applyPendingChange` → **`applyTaskUpdate(lineId, body)`** · `savePayload(lineId, payload, taskId?)` · 칩 진입 `POST …/lines` 한 요청 |
| 〃 `features/settings/components/WorkTypePanel.tsx` · `InlineAddRow.tsx` | 수정 | 인라인 추가 행에 **설명 입력**(유동 · 최소 240) · 목록 행에 **설명 인라인 편집**(비면 「설명 없음」). 기본 유형 3종도 설명은 활성 |
| 〃 `features/settings/types.ts` · `api.ts` | 수정 | `description` |
| 〃 `MeetingTaskLink.test.tsx` · `MeetingEditMode.test.tsx` · `WorkTypePanel.test.tsx` | 수정 | 아래 검증 |

- Domain / schema note: 리비전 **1건**(`0009`). 회의 도메인 스키마 변경 없음 — **`payload` 컬럼은 WORK-012 가 만들었다**

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting_line.payload` | 액션 = 생성분 · 업무 = 변경분. **AI 가 채운 것과 사람이 「저장」한 것이 같은 컬럼 · 같은 모양** — 서버는 출처를 구분하지 않는다 |
| `meeting_line.task_id` | 채워지는 길 셋 — ① 최종 회의록(WORK-012) ② 드로어 헤더 셀렉터 「저장」/「넣기」 ③ 액션 「넣기」 |
| `meeting_line.order_index` | **구멍이 생긴다.** 새 줄은 그 안건 **최대 + 1** |
| `work_type.description` | **신설.** `list_work_types()` 가 그대로 준다 |
| `task` · `task_log` · `task_memo` · `task_todo` · `task_relation` | 「넣기」에서만 바뀐다. 판정은 `task_service` 안 |

- 상태 / invariant: **M-14**(`task_id` 가 채워지는 길 셋 · 모드별 푸터) · **M-14-a**(`payload` 두 모양 · `payload` 를 쓰는 표면 둘 · **둘 다 `task_service` 미호출**) · **M-20**(줄 삭제 넷 — 하드 · 업무 유지 · **자리 유지** · 종류 불변) · **M-5-d**(안건 삭제 없음) · **A-12**(`work_type.description`) · **A-4**(기본 유형 3종은 이름·종류 불변 · 색·설명은 가능)
- Migration 필요 여부: **있음** — `0009_work_type_description`
- SPEC 에 환류해야 하는 변경: 없음

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-014** | `AgendaLineTree.tsx` | 014 가 같은 파일에 `density` prop 을 더한다 — **013 이 먼저 머지**된다 |
| MCP `list_work_types` | `work_type.description` | WORK-009 가 응답을 **그대로 통과**시키므로 컬럼이 생기면 자동으로 실린다 |
| 업무 도메인 | `task_service.change_status()` · `create_task()` · `update_task()` · `add_memo()` | 회의록은 **무엇을 반영할지만** 넘긴다 — 판정 코드를 갖지 않는다 |

## Internal Interface Contract

외부 계약(다섯 표면 · Validation · 드로어 필드)은 **SPEC-008 §4 · U-6 ~ U-10** 이 정본이다. 여기는 Phase 사이 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`payload` 를 쓰는 백엔드 표면은 둘** | `POST …/lines`(칩 진입 — 줄 + `payload` 한 요청) · `PATCH …/lines/{id}`(있는 줄). **둘 다 `task_service` 를 import 하지 않는다**(정적 검사) |
| **업무를 바꾸는 표면도 둘** | `POST …/lines/{id}/task`(생성) · `PATCH …/lines/{id}/task`(갱신). **`task_service` 를 부르는 회의록 코드는 `meeting_task_link_service` 이 두 함수뿐**(정적 검사) |
| **`done` 뒷문 없음** | `status` enum 이 `todo`·`in_progress` **둘뿐**. `payload` 스키마와 `PATCH …/task` 본문 스키마가 **같은 Literal 을 공유**한다. `task_service.change_status()` 는 이 둘로만 불린다 |
| **같은 상태는 건너뛴다** | ① 단계에서 `status == task.status` 면 전이를 부르지 않는다 — 로그가 남지 않는다 |
| **원자성** | `PATCH …/lines/{id}/task` 의 ①~⑧ 은 한 트랜잭션. 어느 단계든 거부되면 **전부 롤백**이고 `payload` 가 남는다 |
| **드로어 prop 두 개뿐** | `prefill`(= 줄의 `payload` · 없으면 `null`) · `submitMode:"save"\|"insert"`. **AI 줄/사람 줄로 분기하는 prop·코드가 없다**(MF-65 — 있으면 반려). 드로어는 `prefill` 이 `null` 인지만 본다 |
| **푸터** | `"save"` = 「취소 · **저장**」 · `"insert"` = 「취소 · **넣기**」. **한 푸터에 버튼 셋을 두지 않는다**(MF-66 — 있으면 반려). **인라인 자동 저장 없음** — 포커스를 벗어나도 요청이 나가지 않는다 |
| **칩 진입** | 「+ 연관 업무」·「+ 액션 아이템」은 **payload 드로어가 바로** 뜬다. 「저장」이 `POST …/lines` **한 요청**으로 줄 + `payload`(+ `taskId`)를 만든다. **닫으면 줄이 없다.** 드로어를 연달아 둘 띄우면 반려 |
| **줄 본문의 출처** | 액션 = 드로어의 **제목** · 업무 = 드로어의 **내용** · 논의·결정 = U-8 의 **내용**. **서버가 업무 제목으로 덮어쓰지 않는다** |
| **`ConfirmModal` `size`** | `"light"` = 420 · 제목 + **요약 한 문장** + 취소/확인 h32. `warning` 슬롯을 받지 않는다. **`Dialog` 를 직접 import 하는 자리는 여기 하나**(FE §6-1) |
| **`RelationPopover` 단일 선택** | prop 하나(`mode`)만 더한다. **업무 화면의 다중 선택 동작이 바뀌면 안 된다**(회귀 테스트). 기본 칩은 「이 프로젝트」, **기준 프로젝트에 업무가 0건이거나 회의가 무소속이면 「전체」**(MF-14) |
| **낙관적 갱신** | 쓰는 자리 — 인라인 본문 · 안건 이름 · U-8 줄 추가 · `payload` 「저장」(칩 진입 포함). **쓰지 않는 자리** — 줄 삭제 · 「넣기」 |
| **무효화** | 줄·안건 이름·`payload` → `['meetings','detail',id]`. 「넣기」 → 거기에 `['tasks', …]` 전부(+ 기한·시작일이 바뀌었으면 `['schedules']`) |

## Execution

### Phase 1 — 스키마 층 · `payload` 두 모양 · `kind` · `newTask` 제거 (백엔드)

- **Status**: TODO
- **설명**: MF-59 · 60 · 64. **층에서 막는 것**이 이 Phase 다 — 서비스가 판정하기 전에 스키마가 거부한다.
- **작업**:
  - [ ] `ActionLinePayload` · `TaskLinePayload` · `TaskUpdateBody` 신설 · `PendingChange` 폐기
  - [ ] `LineCreate` 에서 `new_task` 삭제 · `payload`/`task_id` 를 `kind` 로 가른다
  - [ ] `LineUpdate` 에서 `kind` 삭제
  - [ ] `meeting_edit_service.add_line()` · `update_line()` 재작성
  - [ ] `tests/test_meeting_edit.py`
- **검증**:
  - [ ] `PATCH …/lines/{id}` 에 `kind` → **422**. `POST …/lines` 에 `newTask` → **422**. **논의·결정 줄에 `payload` 또는 `taskId` → 422**
  - [ ] 액션·업무 줄에 `payload` 를 실으면 받아들이고 **내 업무에 아무것도 안 생긴다**(행 수 대조)
  - [ ] **BE §12 8-c** — 업무 줄 `payload.status='done'` · `'cancelled'` 는 **스키마 층 422** 이고 `task.status` 가 안 바뀐다
  - [ ] 액션 `payload.workTypeId=null` 은 **저장된다**(넣기 때 고른다 — OQ-12 SPEC 대로)
  - [ ] `content` 는 네 종류 모두 필수이고 **서버가 업무 제목으로 덮어쓰지 않는다**
  - [ ] **정적 검사**: `meeting_edit_service` 가 `task_service` 를 import 하지 않는다 · `newTask`·`new_task`·`pendingChange` 0건(grep)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 2 — 「넣기」 두 표면 · 자리 유지 · 유형 설명 (백엔드)

- **Status**: TODO
- **설명**: MF-36 · 59 · 21. 업무를 바꾸는 코드가 **두 함수 안에만** 있게 만든다.
- **작업**:
  - [ ] `apply_task_update()` — 본문 수신 · ①~⑧ 한 트랜잭션 · `add_task_line()` · `_stored_change()` 폐기
  - [ ] `create_task_from_line()` — 줄 본문 유지
  - [ ] `meeting_line_repository.delete_line()` 당김 제거 · `next_order_index` = `max+1` 확인
  - [ ] 리비전 `0009` · `WorkType.description` · 시드 · `work_type_service` · 설정 schemas
  - [ ] `tests/test_meeting_task_link.py` · `test_work_type.py`
- **검증**:
  - [ ] **BE §12 8-b** — `order_index` 3 을 지우면 4 가 3 으로 **당겨지지 않고**, 새 줄은 **마지막 + 1** 이다
  - [ ] 줄을 지워도 `task` · `ai` 트랙 · `meeting_transcript` · `recording_path` 가 그대로다(행 수 대조). `payload` 는 줄과 함께 사라진다
  - [ ] `PATCH …/lines/{id}/task` — `status` 가 현재와 **같으면 전이를 부르지 않는다**(`task_log` 행 0). 다르면 `change_status()` 를 지난다. ⑤ 할일 · ④ 메모는 **추가**이고 기존을 덮지 않는다. ⑦ 완료 결과는 **덮어쓴다**
  - [ ] 어느 단계든 거부되면 **전부 롤백**이고 줄의 `payload` 가 남는다(전이 그래프 거부 테스트)
  - [ ] 변경분 0개로 「넣기」 → ⑧ 만 일어난다(`task_id` 확정 · `payload=NULL`)
  - [ ] `alembic upgrade head` → `downgrade -1` → `upgrade` 왕복. 시드 문구 2건이 들어가고 **미팅·회의는 `NULL`** 이다
  - [ ] `work_type.description` 0~200자 · 줄바꿈 거부 · `null` 로 지우기. **기본 유형 3종도 설명은 바뀐다**(이름·종류는 여전히 거부)
  - [ ] **정적 검사**: `task_service` 를 부르는 회의록 코드가 `create_task_from_line` · `apply_task_update` **둘뿐**(grep)
  - [ ] `make test` 전체 통과
- **완료 증거**: 미작성

### Phase 3 — payload 드로어 둘 (프론트)

- **Status**: TODO
- **설명**: MF-13 · 14 · 61 · 65 · 66 · **67**. **새 시안이 없다** — 업무 드로어의 부품 규격을 가리켜 조립한다. ⛔ 업무 탭 드로어를 고치지 않는다.
- **작업**:
  - [ ] `CreateTaskFromLineDrawer.tsx` → 액션 payload 드로어(U-10) 전면 수정
  - [ ] `LinkTaskDrawer.tsx` → 업무 payload 드로어(U-9) 전면 수정 · 헤더 업무 셀렉터
  - [ ] `RelationPopover` 단일 선택 prop
  - [ ] `openMeetingDrawers.tsx` 시그니처 · `useMeetingTaskLink` 두 함수
  - [ ] `LineTaskButton` — 세 상태 · dot · 툴팁
  - [ ] `MeetingTaskLink.test.tsx`
- **검증**:
  - [ ] **AI 액션 줄 「업무 생성」** → 액션 payload 드로어에 안건 고정 + 제목·유형·프로젝트·**계획 시작~종료**·설명·**할일**이 「회의에서 반영」 표시로 채워져 있다. **필드가 이 일곱뿐**(「시작 상태」·참고자료·연관·첨부·로그 칸 0건). 보기 모드라 푸터 「취소 · 넣기」
  - [ ] **내가 `/액션` 으로 적은 줄**을 편집 모드에서 열면 **같은 드로어**가 제목·프로젝트만 채워진 채 뜨고 푸터 「취소 · 저장」. **워커 로그에 AI 호출 0건.** 「저장」 → 줄은 액션 그대로 + dot, **내 업무에 아무것도 안 생긴다.** 보기 모드에서 다시 열면 값 그대로 + 「취소 · 넣기」 — **AI 줄과 화면이 같다**
  - [ ] `payload.workTypeId=null` 이면 유형이 비어 있고 **「저장」은 되고 「넣기」는 비활성**
  - [ ] **AI 업무 줄 「업무 갱신」** → 업무 payload 드로어 헤더 셀렉터가 그 업무를 물고 기한·메모·완료 결과가 채워져 있다. **상태 셀렉터에 「완료」가 없다.** 필드가 변경분 일곱뿐. 셀렉터로 **다른 업무를 고를 수 있다**
  - [ ] **내가 `/업무` 로 적은 줄**은 셀렉터가 **빈 채**로 열리고 본문이 비활성이며 「업무 연결」 같은 앞 단계가 없다. 회의 프로젝트에 업무 0건이면 기본 칩이 「전체」
  - [ ] 「넣기」 → 「갱신 완료」 · `payload` 비움 · 내 업무에 반영. **상태 로그에 완료 전이가 없다**
  - [ ] **어느 드로어에도 인라인 자동 저장이 없다** — 포커스를 벗어나도 네트워크 요청 0(테스트)
  - [ ] **어느 모드에서도 푸터 버튼이 둘**(취소 + 하나)
  - [ ] **업무 탭의 새 업무 드로어 · 업무 상세 드로어가 달라지지 않았다** — 업무 탭에서 열면 안건 칸도 「저장/넣기」 푸터도 없고 인라인 자동 저장 그대로(회귀 테스트)
  - [ ] **정적 검사**: `features/tasks/components/TaskCreateDrawer.tsx` · `TaskDetailDrawer.tsx` 의 diff **0줄**(`git diff --stat`) · `features/meetings` 안에 `isAiLine`·`line.track ===` 로 드로어를 가르는 코드 0건
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

### Phase 4 — 편집 모드 · 칩 둘 갈래 · 모달 420 (프론트)

- **Status**: TODO
- **설명**: MF-60 · 62 · 63 · **64(정정)**. 드로어가 연달아 둘 뜨는 갈래를 없앤다.
- **작업**:
  - [ ] `LineKindSelector.tsx` 폐기 · `LineRow` · `AgendaLineTree` 에서 `onChangeKind` 제거
  - [ ] `AddLineDrawer` 세그먼트 2값 · 캡션 정리
  - [ ] `MeetingDetailBody` 추가 칩 둘 갈래 · `submitMode` 전달
  - [ ] `ConfirmModal` `size` · `OverlayProvider.openConfirm` · `LineDeleteModal` 한 문장
  - [ ] `MeetingEditMode.test.tsx`
- **검증**:
  - [ ] 편집 모드에서 **줄 라벨 자리에 종류 셀렉터가 없다.** 본문만 입력 상자다
  - [ ] 안건을 추가·삭제하는 버튼이 **없다.** 안건 제목은 인라인으로 고쳐지고 저장된다
  - [ ] 「+ 결정」 드로어에 **종류 세그먼트가 「논의 | 결정」 둘뿐**이고 근거 구간 입력이 없으며 「추가」가 그 안건 **맨 아래**에 줄을 붙인다
  - [ ] 「+ 액션 아이템」 → **줄 추가 드로어를 거치지 않고** 액션 payload 드로어가 바로 뜬다. 푸터 「취소 · 저장」. 「저장」 → **요청 하나**(`POST …/lines`)로 줄 + `payload` 생성 · dot 켜짐 · **내 업무 변화 0**. 「+ 연관 업무」도 같다
  - [ ] **「취소」로 닫으면 줄이 생기지 않는다**
  - [ ] 「제거」 → **420 모달** 「이 줄을 삭제할까요? / **되돌릴 수 없습니다.**」 **한 문장** · 경고 슬롯 없음(업무 줄이어도 같다). 「삭제」 → 줄이 사라지고 **카운트 다섯이 따라 바뀌며 뒤 줄 번호가 당겨지지 않는다**. **AI 탭 줄 · 근거 칩 · 스크립트는 그대로**
  - [ ] 회의 삭제 모달은 **600 그대로**다(`heavy`)
  - [ ] **정적 검사**: `Dialog` 직접 import 가 `ConfirmModal` 하나 · `LineKindSelector` 0건 · `onChangeKind` 0건(grep)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

### Phase 5 — 유형 설명 UI (프론트)

- **Status**: TODO
- **설명**: MF-21. AI 가 새 업무의 유형을 고르는 근거를 사람이 적는 자리.
- **작업**:
  - [ ] `WorkTypePanel` 목록 행에 설명 인라인 편집 · `InlineAddRow` 에 설명 입력
  - [ ] `features/settings/types.ts` · `api.ts`
  - [ ] `WorkTypePanel.test.tsx`
- **검증**:
  - [ ] 인라인 추가 행이 [종류][이름][**설명**][색][취소][추가] **네 필드**이고 설명은 **선택**이다(비어도 「추가」 활성)
  - [ ] 목록 행에서 설명을 인라인으로 고치면 포커스 해제 시 저장된다. 비면 「설명 없음」
  - [ ] **기본 유형 3종도 설명은 편집된다**(이름·종류 칩은 읽기 전용 그대로 · 삭제 버튼 없음)
  - [ ] 저장 실패는 **SPEC-002 U-7 규격**(토스트 + 그 행 실패 표시 + 「다시 저장」 · 자동 재시도 없음)
  - [ ] `GET /api/work-types` 응답에 `description` 이 실린다(MCP `list_work_types` 가 그대로 통과 — WORK-009)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `alembic upgrade head` → `0009`. 시드 문구 2건이 기존 계정의 기본 유형에도 들어간다(UPDATE)
- [ ] 백·프론트 같이 배포 — `PATCH …/lines/{id}/task` 가 본문을 받게 바뀐다(옛 프론트는 빈 본문을 보낸다)
- [ ] 기존 `pending_change` 값이 `payload` 로 살아 있다(WORK-012 의 RENAME) — 배포 뒤 그 줄들의 드로어가 값을 그대로 연다
- [ ] `.env` 변경 없음

## Rollback

- **스키마**: `alembic downgrade -1` — `work_type.description` 이 사라진다(값도 사라진다 · 재입력 가능)
- **백엔드**: revert 하면 `newTask` · `kind` 전환 · 당김 삭제가 돌아온다. **WORK-012 아래로는 내려가지 않는다**
- **프론트**: 드로어 두 개와 백엔드 표면이 짝이라 **함께** 되돌린다
- 부분 revert 시: Phase 5(유형 설명)만 되돌려도 나머지가 돈다 — AI 가 이름만 보고 유형을 고를 뿐이다. Phase 3·4 는 백엔드와 짝이라 단독 revert 하지 않는다

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] **SPEC-008 §6 AC 중 이 work 의 14항목**(편집 자동 저장 · 종류 셀렉터 없음 / 안건 제목 · 추가·삭제 버튼 없음 / 420 한 문장 · 자리 유지 · AI 탭 그대로 / 업무 줄 제거 후 업무 잔존 / 「+ 결정」 세그먼트 2값 / 「+ 액션 아이템」 요청 하나 / 취소면 줄 없음 / AI 액션 줄 필드 일곱 / 사람 액션 줄 「저장」 → AI 와 같은 상태 / `workTypeId=null` / AI 업무 줄 변경분 일곱 · 완료 없음 / 완료 결과로 게이트 열림 / `status:"done"` 422 / 사람 업무 줄 빈 셀렉터 / 업무 탭 드로어 무변화 / 자동 저장 0 · 푸터 둘 / `kind`·`newTask`·논의결정 payload 422)이 **실측 캡처로** 완료 증거에 있다
- [ ] BE §12 **8-b · 8-c** 테스트가 있다
- [ ] 정적 검사 6종(`task_service` 호출 둘 · 업무 탭 드로어 diff 0 · AI/사람 분기 0 · `Dialog` 직접 import 하나 · `LineKindSelector` 0 · `newTask` 0)
- [x] `make test` · `vitest` 전체 통과 · `Errors` 줄 0
- [x] `30-work/README.md` 갱신

> 2026-09-08 — 커밋 `bfde960`(be+fe). 검수 `orchestration/work/docs-v1/work013-review-report.md` FAIL 0 · WARN 2(파일 이름 둘 → WORK-014 Phase 0 · 업무 드로어 「현재 값」 둘은 사용자 결정 대기). pytest 638 · tsc 0 · vitest 340. **미완: 앱 창 실측은 사용자(아침)**

## Open Issues

- **OQ-11 「미팅·회의」 유형의 설명 문구** → **SPEC 대로 빈 값**(SPEC-002 U-4 · A-12). 새로 묻지 않는다
- **OQ-12 AI 가 유형을 못 고를 때** → **SPEC 대로 `null` 로 두고 사람이 고른다**(U-10 · SPEC-008 §4 「페이로드 참조」). 새로 묻지 않는다
- **드로어 파일 이름** — `CreateTaskFromLineDrawer.tsx` · `LinkTaskDrawer.tsx` 를 **그대로 쓴다**(브리프 「폐기 아님 · 수정」). 이름이 새 뜻과 어긋나 보이지만 **파일 이름 변경은 이 work 의 범위가 아니다** — 바꾸려면 사용자 결정이 필요하다
- **`RelationPopover` 에 prop 을 더하는 것이 「업무 화면을 고치는 것」인가** — SPEC-008 §5 · FE §2 규칙 8 이 **「그대로 재사용한다(단일 선택 prop 하나만 더한다)」** 로 이미 허용했다. 드로어가 아니라 부품이다. 새 결정이 아니다
- **줄 본문 · 업무 제목의 동기화 없음** — 「넣기」로 만든 업무의 제목을 나중에 바꿔도 줄 본문은 안 따라간다. SPEC 에 그 규칙이 없다 — **만들지 않는다**

## Related

- SPEC: SPEC-008 U-3 · U-6 ~ U-10 · §4 · §5 · §6 · SPEC-002 §4 · U-3 · U-4 · SPEC-003 U-1 · U-3 · U-8(시각 참조) · SPEC-004 §4(전이) · DEC-001 §3 · DEC-002 §4 · §5 · DEC-003 §5
- Architecture: `frontend/README.md` §2 규칙 8 · §3-3 · §3-4 · §6 · §6-1 · §6-2 · §11 · `backend/README.md` §8-3 · §12 8-b · 8-c · `database/domains/meeting.md` M-14 · M-14-a · M-20 · `database/domains/account.md` A-4 · A-12
- Work: WORK-012(선행) · WORK-009(`list_work_types` 가 설명을 통과) · WORK-014(같은 파일 `AgendaLineTree.tsx`)
