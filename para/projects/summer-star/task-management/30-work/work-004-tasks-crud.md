---
type: work
id: WORK-004
title: "내 업무 — 생성 드로어 · 상세(드로어↔페이지) · 인라인 편집 · 자식 5종"
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
  specs: [SPEC-003]
  works: [WORK-001, WORK-002, WORK-003]
  releases: []
  related: [DEC-001, DEC-004, DEC-005]
---

# 내 업무 — 생성 드로어 · 상세(드로어↔페이지) · 인라인 편집 · 자식 5종

**업무를 만들고, 열어서 그 자리에서 고친다.** 할일·메모·참고자료/결과자료·연관업무·로그가 업무 하나에 붙는다. 상태를 바꾸는 것과 목록·칸반은 만들지 않는다 — WORK-005 다. 이 work 는 그들이 열고 그릴 **업무 하나**를 세운다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-002
- Covers spec: **SPEC-003**(내 업무 — 생성 · 상세 · 편집)
- Depends on work: **WORK-001**(마이그레이션 도구·시드·토큰 CSS·정적 골격·Tauri 셸) · **WORK-002**(세션 가드 · `client.ts` 401 재시도 · `ConfirmModal` · `AppShell`) · **WORK-003**(`work_type`·`project` API · 팔레트 8종 · `TypeBadge`/`ColorDot`/`ColorPickerPopover` · `InlineEditText` · **U-7 자동저장 실패 규격**)
- Parallel work: 없음 — WORK-005 가 이 work 의 상세·목록 항목 위에 얹힌다
- Follow-up work: **WORK-005**(상태·완료 게이트·리스트/칸반) · WORK-008(회의록이 이 업무를 만들고 갱신한다) · 캘린더 그룹(`schedule` 을 읽기만 한다) · 문서함 그룹(첨부의 「자료함 문서」 갈래를 실체화한다)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다
  - **문서함(`document`·`folder`)이 아직 없다** — 첨부의 「자료함 문서」 갈래가 이 work 에서는 **스텁**이다(§Scope 제외 · §Open Issues)
  - 그 밖의 외부 의존은 없다(Redis·codex·Soniox 는 회의록 그룹에서 합류한다)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | 없음 (WORK-001~003 완료) |
| Next | Phase 1 — 업무 도메인 마이그레이션 · `schedule` 파생·겹침 서비스 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-003 §6 Acceptance 16개 대조 | todo |
| Design |  | 드로어 840 프레임 · 첨부/연관 팝오버 · 「결과자료 · 완료 결과」 카드 · 1280~1439 전체화면 전환 | todo |
| FE |  | 드로어 프레임·셀렉터·첨부 팝오버 공용화 → 생성 드로어 → 상세(드로어·페이지 공용 본문) | todo |
| BE |  | 업무 도메인 마이그레이션 · `schedule` 파생/겹침 · 업무 본체·자식 5종 API · 로그 | todo |
| QA |  | Phase 검증(앱 창 E2E) · 계층·금지목록 정적 검사 | todo |
| Ops |  | 해당 없음(신규 env 없음) | todo |

## Scope

포함:

- **업무 도메인 마이그레이션** — `task` · `task_todo` · `task_memo` · `task_log` · `task_attachment` · `task_relation`
- **`schedule` 테이블과 파생·겹침 서비스** — 기한이 일정으로 파생되고 시간 일정끼리 겹침을 막는다(DEC-005 §3 · `database/README.md` §3-3). **캘린더 화면은 만들지 않는다**
- 업무 본체 API — 생성(자식 포함 한 트랜잭션) · 상세 · 부분 수정(기한 포함)
- 자식 컬렉션 API — 할일 · 메모 · 첨부(`doc`/`link`) · 연관업무 · 로그(응답 동봉)
- **공용 오버레이·표시 컴포넌트** — `DrawerFrame`(840) · `openDrawer` 실동작 · `Selector`(**하단 「+ 새 프로젝트」 인라인 행 포함**) · 첨부 팝오버 360 · `EmptyState` · `LogRow` · `ProgressBar` · `StatusDot`
- **생성 드로어**(840) · **상세 드로어**(840) · **전체 페이지 승격**(⤢, `/tasks/detail?id=`)
- 인라인 편집 자동 저장(제목·배경·목표·완료 결과) · **「결과자료 · 완료 결과」 카드**(칩 표시까지)
- 상세의 로딩 스켈레톤 · 「없는 업무입니다」 · 반응형 3구간

제외:

- **상태 전이·완료 게이트·취소·삭제·실행취소** → **WORK-005**. 상세 헤더의 상태 드롭다운·「완료 처리」·`⋯` 는 **자리만 두고 비활성**으로 그린다(SPEC-003 U-3 이 「자리와 표시만」으로 못박았다)
- **리스트·칸반·필터·정렬·기간 스테퍼** → WORK-005. 이 work 의 진입점은 `/tasks` 임시 진입 버튼 하나다(§Phase 5)
- 캘린더 화면·드래그 → 캘린더 그룹. 이 work 는 **`schedule` 파생만** 만든다
- 회의록이 업무를 만들고 고치는 입구 → WORK-008
- **첨부의 「자료함 문서」 실동작** → 문서함 work. 이 work 는 **URL 링크만 실동작**하고 문서 갈래는 빈 상태 스텁이다
- 업무 목록 검색 — v1 에 없다(SPEC-003 §7)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보 — 경로는 `backend/README.md` §4 · `frontend/README.md` §2 의 트리를 따른다

| 경로 후보 | 설명 |
|---|---|
| `app/back/models/task.py` | `task` · `task_todo` · `task_memo` · `task_log` · `task_attachment` · `task_relation` |
| `app/back/models/calendar.py` | `schedule`(파생 테이블 — G-7-e 의 유일한 예외) |
| `app/back/alembic/versions/*_task_domain.py` | 리비전 1건. **`autogenerate` 초안을 사람이 읽고 고친다**(CHECK·부분 인덱스) |
| `app/back/core/enums.py`(신규) | `TaskStatus` · `AttachmentRole` · `AttachmentKind` `StrEnum` — **enum 값의 단일 출처**(G-3·G-4) |
| `app/back/repository/task_repository.py` | 본체 조회·쓰기. 기본 조회 `deleted_at IS NULL`, dto 반환 |
| `app/back/repository/task_child_repository.py` | 할일·메모·로그·첨부·연관 |
| `app/back/repository/schedule_repository.py` | 기간 조회·겹침 조회·UPSERT/DELETE |
| `app/back/service/schedule_service.py` | **겹침 검사 + `schedule` 파생 — 둘 다 여기 하나뿐**(BE §4). 다른 곳에서 `schedule` 을 쓰지 않는다 |
| `app/back/service/task_service.py` | 생성 트랜잭션 · 부분 수정 · 자식 조작 · **로그 기록** · 소유 검사 |
| `app/back/api/task_router.py` | SPEC-003 §4 의 11 표면. 라우터 단위 `require_account` |
| `app/back/schemas/task.py` · `dto/task.py` | FE 계약(camelCase alias) / 내부 dto. **PATCH 는 `T \| Unset`**(BE §3-4) |
| `app/back/tests/test_task.py` · `test_task_children.py` · `test_schedule_derive.py` | 아래 §Execution 의 검증 항목 |
| `app/front/src/lib/overlay/OverlayProvider.tsx` | **`openDrawer` 실동작**(WORK-001 은 뼈대만 만들었다) · 스택 규칙 |
| `app/front/src/components/shared/DrawerFrame.tsx` | 840 · 헤더 72 · 푸터 76 · 스크림 0.32 · ⤢/× · **1280~1439 전체화면 + `←`** |
| `app/front/src/components/shared/Selector.tsx` | 유형·프로젝트 팝오버 셀렉터. **프로젝트 갈래 하단에 「+ 새 프로젝트」 인라인 행**(SPEC-006 U-2 가 전 화면 공통으로 정한 규격) |
| `app/front/src/components/shared/AttachmentPopover.tsx` · `AttachmentList.tsx` | 팝오버 360 · 세그먼트 2(자료함 문서 / URL 링크) · 목록 행 |
| `app/front/src/components/shared/EmptyState.tsx` · `LogRow.tsx` · `ProgressBar.tsx` · `StatusDot.tsx` | 공용 표시 조각 |
| `app/front/src/features/tasks/api.ts` · `types.ts` | 호출 함수 · 응답 타입(`types/api.ts` 미러) |
| `app/front/src/features/tasks/hooks/useTaskDetail.ts` · `useTaskMutations.ts` | 쿼리·뮤테이션·무효화 |
| `app/front/src/features/tasks/components/TaskCreateDrawer.tsx` | U-1 생성 드로어 |
| `app/front/src/features/tasks/components/TaskDetailBody.tsx` | **드로어와 전체 페이지가 공유하는 본문**(§Internal Interface Contract) |
| `app/front/src/features/tasks/components/TaskDetailDrawer.tsx` · `TaskDetailPage.tsx` | 본문을 감싸는 두 표면 |
| `app/front/src/features/tasks/components/TodoList.tsx` · `MemoList.tsx` · `CompletionCard.tsx` · `RelationPopover.tsx` · `TaskLogList.tsx` · `DueDateField.tsx` | 블록 6 |
| `app/front/src/app/(app)/tasks/detail/page.tsx` | 라우트 껍데기(`'use client'`, `?id=` 파싱은 영역 훅) |
| `app/front/src/features/tasks/hooks/useTasksViewParams.ts` | **쿼리 파싱은 영역 훅 하나**(FE §1-2). WORK-005 가 `view`·필터를 여기에 덧붙인다 |
| `app/front/src/lib/api/queryKeys.ts` | `['tasks','detail',id]` 등록 · 무효화 표 연결 |
| `app/front/src/lib/datetime.ts` | 기한 표시 포맷(`08.29 14:00–15:00`). **D-day·지연은 서버 파생값을 그대로 그린다** |

- Domain / schema note: **마이그레이션이 필요하다** — 업무 도메인 6 테이블 + `schedule`. 스키마 전문은 코드·migration 이 SoT 이고 이 문서는 범위와 불변식만 적는다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `task` | 업무 본체. **기한(`due_date`·`due_start_time`·`due_end_time`)을 소유한다** |
| `task_todo` | 할일 — 진행률의 분모·분자 |
| `task_memo` | 메모 — 등록만(수정·삭제는 v1 에 없다) |
| `task_log` | 시스템 로그 — **서비스만 쓴다** |
| `task_attachment` | 참고자료·결과자료. `role`×`kind` 두 축 |
| `task_relation` | 연관업무 — 무방향 1행(`low < high`) |
| `schedule` | **파생 테이블** — 기한·일시의 시간축 배치. 이 work 가 만들고 캘린더 그룹이 읽는다 |

- 상태 / invariant: `domains/task.md` **T-1**(업무가 기한을 소유) · **T-1-b**(시각 두 개는 함께 · CHECK) · **T-2**(유형 필수) · **T-3**(프로젝트 0..1) · **T-8**(전이·할일 완료·첨부는 로그와 같은 트랜잭션) · **T-9·T-9-a**(첨부 2종 · `kind` 별 컬럼 CHECK) · **T-10**(무방향 1행) · **T-11**(소프트 딜리트) · `database/README.md` **§3-2 SCH-1~SCH-5** · **§겹침 검사**
- Migration 필요 여부: **필요**. 리비전 1건(업무 6 테이블 + `schedule` + 인덱스). `downgrade` 를 작성한다
- **`task_attachment.document_id` 에 FK 를 걸지 않는다** — 대상 `document` 테이블이 아직 없다. 컬럼·CHECK 은 T-9-a 최종 형태로 만들고, **문서함 work 가 FK 추가 리비전을 낸다**(§Open Issues)
- SPEC 에 환류해야 하는 변경: **`invalid_work_type` 코드**가 아키텍처 §8-2 표에 없다(SPEC-003 S003-OQ-2) — 구현은 SPEC-003 §4 Case Matrix 를 따르고 표 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-005** | `task` 스키마 · 상세/목록 항목 dto · `TaskDetailBody` · `DrawerFrame` · `StatusDot` | 상태 전이는 이 work 가 만든 업무 위에서만 의미가 있다. 상세 헤더의 상태 컨트롤 자리도 여기서 그려 둔다 |
| **WORK-006** | **`schedule_service`**(겹침 검사 + 파생) · `Selector` 의 「+ 새 프로젝트」 · `DrawerFrame` · 첨부 팝오버 | 회의 일시도 같은 서비스로 겹침을 막고 같은 테이블로 파생한다 — **두 번째 구현을 만들지 않는다** |
| **WORK-008** | `task_service` 의 생성·부분 수정 · `task_memo` 추가 | 회의록의 「업무 생성」·「업무 갱신」이 이 서비스를 그대로 부른다 |
| 캘린더 그룹 | `schedule` 테이블 · `GET /api/schedules` 가 붙을 자리 | **캘린더는 `schedule` 을 읽기만** 한다(BE-10) |
| 문서함 그룹 | `task_attachment.document_id` · 첨부 팝오버의 「자료함 문서」 세그먼트 | 문서함이 서면 이 갈래가 실동작으로 바뀐다 |

## Internal Interface Contract

외부 계약(엔드포인트·요청/응답·검증·에러)은 **SPEC-003 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`schedule_service`** | `check_overlap(...)` 과 `sync_from_task(...)` / `sync_from_meeting(...)` 두 갈래. **`schedule` 을 INSERT/UPDATE/DELETE 하는 코드는 이 파일 하나뿐**이다(SCH-1 · BE §4). 겹침 검사는 **원본을 쓰기 전에** 돌고, 걸리면 원본도 안 바뀐다 |
| 겹침 판정 | `start_at < :end AND end_at > :start` — **경계 접촉은 겹침이 아니다.** 대상은 `is_all_day=false` 끼리, **종류 불문**(업무↔회의). 소프트 딜리트·취소 상태는 제외(`database/README.md` §겹침 검사) |
| 기한 → 일정 | 기한만 있으면 **종일**, 시각까지 있으면 **시간 일정**. 기한을 지우면 행이 **사라진다**. `date`/`time` → `timestamptz` 변환은 **`APP_TIMEZONE`(KST)** 기준 한 곳에서 |
| 로그 기록 | `task_log` 를 쓰는 곳은 `task_service` 하나. 대상은 **생성·상태 전이·할일 완료·첨부·연관 연결**뿐이고 **제목·배경·목표·완료 결과 인라인 편집은 대상이 아니다**(04-task-detail). 사용자는 로그를 쓰거나 지울 수 없다 |
| 파생값 | `dDay` · `isOverdue` · `overdueDays` · `todoProgress` 는 **서버가 계산해 내려준다**. 컬럼으로 두지 않고(G-7) **화면이 다시 계산하지 않는다** |
| `TaskDetailBody` | **드로어와 전체 페이지가 공유하는 유일한 본문 컴포넌트**다. 두 표면의 차이는 **감싸는 껍데기(스크림·헤더·2단 배치)뿐**이고 블록 규격·편집 규칙은 한 벌만 존재한다(SPEC-003 U-4 「드로어와 페이지가 다른 규격을 갖지 않는다」). 본문은 **부모를 모른다** — `onExpand` 콜백만 받는다(FE §6-2) |
| `DrawerFrame` | **이 work 가 규격의 주인이다**(FE §6-2 — 첫 드로어를 만드는 work). 폭 **840 고정** · 스크림 `rgba(30,30,30,0.32)` · 헤더 72 / 푸터 76 · `Esc`·×·스크림 클릭 셋 다 닫는다 · `expandTo` 로 ⤢ 승격. **폭을 `prop` 으로 받지 않는다** — `width`·`size`·`className` 으로 폭을 넘기는 길을 두지 않는다. **유일한 예외는 좁은 화면 전체화면 전환이고 그 판정도 `DrawerFrame` 안에 있다.** **컴포넌트가 `Sheet`/`Dialog` 를 직접 import 하지 않는다**(FE §6-1). 드로어는 **동시에 하나**, 드로어 위에 모달을 겹치면 개발 모드에서 throw. 이후 회의·캘린더는 **쓰기만 한다** |
| 자동 저장 실패 상태 | **컴포넌트 내부 state 로 두지 않는다.** `saveFailed`·`onRetry` 를 **prop** 으로 받고 **소유자는 행/블록**이다(SPEC-002 U-7 구현 규약, 2026-09-06 확정). 내부 state 로 두면 두 번째 자동 저장 컨트롤이 생기는 순간 규격이 샌다 — WORK-003 검수 F-1 이 그 사례다. **팝오버형 컨트롤**(기한 트리거·유형/프로젝트 셀렉터)의 실패도 **그 행 아래 인라인 자리 하나**에 모은다 |
| `Selector` | 유형·프로젝트 공통 팝오버. **프로젝트 갈래 하단에 구분선 + 「+ 새 프로젝트」 인라인 행**(이름 + 색 트리거)을 둔다 — 만든 프로젝트가 **즉시 선택**되고 `['projects']` 를 무효화한다. 팔레트·검증은 **WORK-003 의 것을 그대로** 쓴다 |
| 첨부 팝오버 | 세그먼트 2 — 「자료함 문서」 / 「URL 링크」. **여러 건을 연달아 붙일 수 있게 팝오버가 열린 채 유지**된다. 이 work 시점의 문서 갈래는 **빈 결과 + 안내 캡션**이다(§Open Issues) |
| 캐시 키·무효화 | `['tasks','detail',id]`. 업무 생성·수정은 `['tasks', …]` 전부 + **기한이 바뀌었으면 `['schedules']`** 를 무효화한다(FE §3-3 표). **표에 없는 무효화를 하지 않는다** |
| 낙관적 갱신 | **할일 체크·메모 추가·인라인 텍스트만** 낙관적이다. **기한·유형·프로젝트·첨부는 하지 않는다** — 겹침·삭제된 항목·사라진 문서가 거부할 수 있다(SPEC-003 §5 표 · FE §3-4) |

## Execution

### Phase 1 — 업무 도메인 마이그레이션 · `schedule` 파생·겹침 서비스

- **Status**: TODO
- **설명**: 화면도 API 도 없이 **스키마와 시간 규칙이 도는 상태**를 만든다. 기한이 일정으로 내려오고 겹침이 막히는 것이 이후 업무·회의 두 영역의 공통 바닥이다 — 여기서 한 번만 만든다.
- **작업**:
  - [ ] `core/enums.py` — `TaskStatus`(`todo`·`in_progress`·`done`·`cancelled`) · `AttachmentRole` · `AttachmentKind`. **한국어 라벨을 저장하지 않는다**(G-4)
  - [ ] `models/task.py` — 6 테이블. `task_relation` 은 `low_task_id < high_task_id` CHECK + `UNIQUE`, `task_attachment` 는 **T-9-a CHECK**(`doc` 이면 `document_id` 만 / `link` 면 `url`·`label` 만)
  - [ ] `models/calendar.py` — `schedule`(`UNIQUE (source_type, source_id)`, **FK 없음** — §3-4)
  - [ ] 리비전 1건 + `downgrade`. 인덱스는 `database/README.md` §4 표 그대로 — 특히 **`task (account_id, due_date NULLS LAST) WHERE deleted_at IS NULL`** 와 **`schedule (account_id, start_at, end_at)`**
  - [ ] `repository/schedule_repository.py` · `service/schedule_service.py` — 겹침 검사 · 파생(UPSERT/DELETE) · KST 변환 한 곳
  - [ ] `tests/test_schedule_derive.py` — BE §12 필수 테스트 **3·5·5-a·9**
- **검증**:
  - [ ] `make migrate` 가 빈 DB 에서 끝나고 `alembic downgrade -1 → upgrade head` 왕복이 된다
  - [ ] 시각을 하나만 넣은 행(`due_start_time` 만)이 **DB CHECK 로 거부**된다(T-1-b)
  - [ ] `kind='doc'` 인데 `url` 이 있는 행이 **DB CHECK 로 거부**된다(T-9-a)
  - [ ] 같은 쌍을 `(low, high)` 순서를 바꿔 두 번 넣으면 **UNIQUE 로 거부**된다(T-10)
  - [ ] **정적 검사**: `schedule` 을 INSERT/UPDATE/DELETE 하는 코드가 **`schedule_service.py` 밖에 0건**이다(grep 결과를 완료 증거에 붙인다 — SCH-1)
  - [ ] `pytest` 통과 — 겹침(시간 일정끼리 막힘 / 종일은 안 막힘 / **경계 접촉 10–11 · 11–12 는 통과**) · 파생(기한 넣으면 종일 행, 시각 넣으면 시간 행, 기한 지우면 행 삭제) · 고아 `schedule` 없음
- **완료 증거**: 미작성

### Phase 2 — 업무 본체 API (생성 · 상세 · 부분 수정)

- **Status**: TODO
- **설명**: `curl` 로 **업무를 만들고 읽고 고치는** 왕복을 닫는다. 생성이 자식까지 **한 트랜잭션**인 것과, 기한이 겹치면 **원본도 안 바뀌는** 것이 이 Phase 의 핵심이다.
- **작업**:
  - [ ] `repository/task_repository.py` — 기본 조회 `deleted_at IS NULL` · **dto 만 반환**
  - [ ] `service/task_service.py` — 생성(유형 검증 → 겹침 검사 → `task` INSERT + 자식 INSERT + `task_log`「업무 생성」, **같은 트랜잭션**) · 상세(자식·로그·파생값 포함) · 부분 수정
  - [ ] 부분 수정 — `TaskUpdateDTO` 의 필드를 **`T | Unset`** 으로 두고 「보내지 않음」과 「`null` 로 지움」을 구분(BE §3-4). `dueDate: null` 은 기한 삭제이고 **파생 일정도 사라진다**
  - [ ] `api/task_router.py` — `POST /api/tasks` · `GET /api/tasks/{id}` · `PATCH /api/tasks/{id}`. 라우터 단위 `require_account`
  - [ ] `schemas/task.py`·`dto/task.py` — camelCase alias · `response_model_by_alias=True`
  - [ ] 파생값 계산 — `dDay` · `isOverdue` · `todoProgress`(G-7)
  - [ ] `tests/test_task.py`
- **검증**:
  - [ ] `curl` 로 **제목 + 유형만** 넣어 업무가 만들어지고, 상세에 `status: "todo"` 와 로그 「업무 생성」이 있다
  - [ ] 유형을 빼면 **422 `validation_error`**, 삭제된 유형을 주면 **422 `invalid_work_type`**
  - [ ] 할일·첨부(`kind:"link"`)·연관업무를 함께 보낸 생성이 **전부 저장**되고, 그중 하나를 잘못 주면(예: 자기 자신 연관) **업무 본체도 만들어지지 않는다**(부분 저장 없음)
  - [ ] 이미 14:00–15:00 일정이 있는 시각으로 기한을 PATCH 하면 **409 `schedule_overlap`** 이고 **`task` 행의 기한이 그대로**다(DB 로 확인)
  - [ ] 15:00–16:00 으로 PATCH 하면 **저장된다**(경계 접촉)
  - [ ] `{"dueDate": null}` 을 보내면 기한이 지워지고 **`schedule` 행이 사라진다**
  - [ ] `{"background": "..."}` 만 보내면 **다른 필드가 그대로**이고 **`task_log` 가 늘지 않는다**
  - [ ] 남의 업무 id 로 조회하면 **404 `not_found`**
  - [ ] **정적 검사**: `service/` 에서 `fastapi`·`schemas` 를 import 하는 코드 **0건**, `repository/` 가 ORM 모델을 반환하는 함수 **0건**(BE §2·§3 — grep/AST 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — 자식 컬렉션 API (할일 · 메모 · 첨부 · 연관 · 로그)

- **Status**: TODO
- **설명**: 상세 화면이 조작할 표면을 마저 연다. **로그가 남는 자리와 안 남는 자리**를 여기서 못박는다 — 나중에 화면을 보고 고치면 이미 로그가 오염돼 있다.
- **작업**:
  - [ ] 할일 — 추가 · 내용/완료 수정 · 삭제. **완료로 바뀌면 `task_log`「할일 n건 완료」**(같은 트랜잭션 — T-8)
  - [ ] 메모 — 등록만. **수정·삭제 표면을 만들지 않는다**(SPEC-003 S003-OQ-4)
  - [ ] 첨부 — 추가(`doc`/`link`) · 제거. 로그 「참고자료 n건 첨부」/「결과자료 n건 첨부」. **`kind='link'` 는 `http`/`https` 만**
  - [ ] 연관업무 — 여러 건 연결(무방향 1행, **중복 재전송이 행을 늘리지 않는다**) · 해제. 로그 「연관업무 n건 연결」. 상세 응답은 **최근 5건 + `relationTotal`**
  - [ ] 연관업무 후보 조회 — 검색어가 없으면 **같은 프로젝트 → 기한 ±7일 → 최근 수정** 순 최대 20건(SPEC-003 U-8)
  - [ ] `tests/test_task_children.py`
- **검증**:
  - [ ] 할일을 완료로 바꾸면 상세의 `todoProgress` 가 오르고 **로그가 한 줄 늘어난다**. 되돌리면 진행률만 내려가고 **로그는 지워지지 않는다**
  - [ ] 메모를 등록해도 **로그가 늘지 않는다**(DEC-002 §6)
  - [ ] `kind:"link"` 로 `ftp://…` 를 주면 **422 `validation_error`**
  - [ ] **`kind:"doc"` 요청은 이 시점에 거부된다** — 대상 문서 테이블이 없다(§Open Issues 의 임시 계약)
  - [ ] A 에 B 를 연결한 뒤 **B 의 상세에도 A 가 보인다**. 같은 쌍을 다시 연결해도 `relationTotal` 이 늘지 않는다
  - [ ] 자기 자신을 연관에 넣으면 **422**
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 4 — 공용 오버레이·표시 컴포넌트

- **Status**: TODO
- **설명**: **화면보다 먼저** 만든다. 드로어 프레임·셀렉터·첨부 팝오버는 이 work 의 두 화면과 WORK-005·006·008 이 전부 쓴다 — 화면부터 만들면 다음 work 가 복제한다.
- **작업**:
  - [ ] `lib/overlay/OverlayProvider.tsx` — `openDrawer` 실동작 · 스택 · **드로어 위 모달 금지**(개발 모드 throw)
  - [ ] `components/shared/DrawerFrame.tsx` — 840 · 스크림 0.32 · 헤더 72 / 푸터 76 · `Esc`/×/스크림 · `expandTo` · **1280~1439 전체화면 전환**(스크림 없음 + 헤더 74 한 줄 + `←`). **폭 prop 을 두지 않는다**(FE §6-2, 2026-09-06 확정)
  - [ ] `components/shared/Selector.tsx` — 유형·프로젝트 팝오버. **프로젝트 갈래 하단 「+ 새 프로젝트」 인라인 행**(이름 + 색 트리거, WORK-003 의 `ColorPickerPopover` 재사용)
  - [ ] `components/shared/AttachmentPopover.tsx` — 360 · 세그먼트 2 · 문서 갈래는 **빈 결과 + 「자료함이 아직 없습니다」 캡션**(스텁) · 링크 갈래는 URL + 표시 이름 + 「추가」
  - [ ] `components/shared/AttachmentList.tsx` · `EmptyState.tsx` · `LogRow.tsx` · `ProgressBar.tsx` · `StatusDot.tsx`
  - [ ] `lib/datetime.ts` — 기한 표시 포맷 한 곳
- **검증**:
  - [ ] 임시 화면에서 드로어를 열고 **`Esc`·×·스크림 클릭 셋 다** 닫힌다
  - [ ] 드로어가 열린 상태에서 `openConfirm` 을 부르면 **개발 모드에서 throw** 한다(FE §6-2)
  - [ ] 창을 1439 이하로 줄이면 드로어가 **전체 화면**이 되고 스크림이 사라지며 헤더 좌측에 `←` 가 생긴다
  - [ ] 셀렉터 하단 「+ 새 프로젝트」로 프로젝트를 만들면 **즉시 선택**되고 **설정 화면 목록에도 나타난다**
  - [ ] **정적 검사**: `Sheet`/`Dialog` 를 `components/shared/` 밖에서 import 하는 코드 **0건**, 인라인 `style` 로 색 hex 를 지정하는 코드 **0건**, 컴포넌트에서 `new Date()` 로 포맷하는 코드 **0건**(FE §금지 목록 3·4·8 — grep 결과를 완료 증거에)
  - [ ] **정적 검사**: **폭 리터럴(`840` · `w-[840px]`)이 `DrawerFrame.tsx` 밖에 0건**이고 `DrawerFrame` 이 폭 관련 prop(`width`·`size`)을 받지 않는다(FE §6-2, 2026-09-06 확정 — grep 결과를 완료 증거에)
- **완료 증거**: 미작성

### Phase 5 — 생성 드로어

- **Status**: TODO
- **설명**: **앱 창에서 실제로 업무를 만드는** 단계. 목록이 아직 없으므로 `/tasks` 에 임시 진입(「새 업무」 버튼 + 방금 만든 업무 id 표시)만 두고, WORK-005 가 그 자리를 리스트로 대체한다.
- **작업**:
  - [ ] `features/tasks/api.ts` · `types.ts` · `hooks/useTaskMutations.ts` — 생성 호출·무효화
  - [ ] `TaskCreateDrawer.tsx` — 블록 6 순서(제목 / 유형·프로젝트·기한 / 배경·목표 / 할일 / 참고자료·연관업무 / 결과자료·완료 결과 안내 + 로그 안내)
  - [ ] 열자마자 **제목 포커스** · 제출 조건 **제목 1자 + 유형 선택** · 제출 중 버튼 비활성(중복 제출 금지)
  - [ ] 기한 — 날짜 + 「시간 지정」 토글(켜면 시작–종료). **낙관적 갱신 없음**
  - [ ] 할일 인라인 추가 행 — `Enter` 와 **「추가」 버튼 병행**
  - [ ] 연관업무 팝오버 382 — 검색·필터 칩 3·하이라이트·「n건 선택됨」
  - [ ] 실패 처리 — 드로어를 닫지 않고 해당 필드 인라인 안내(SPEC-003 §4 Case Matrix)
  - [ ] `app/(app)/tasks/page.tsx` 에 **임시 진입 버튼**(WORK-005 가 대체)
- **검증**:
  - [ ] 「새 업무」로 드로어가 열리고 **제목에 커서**가 있다
  - [ ] 유형을 고르기 전에는 「업무 만들기」가 **비활성**이다
  - [ ] 제목 + 유형만으로 업무가 만들어지고 드로어가 닫힌다
  - [ ] 드로어에서 넣은 **할일 2건·URL 링크 1건·연관업무 1건이 생성 직후 상세에 그대로** 있다(Phase 6 후 확인 / 이 Phase 에서는 `GET` 응답으로)
  - [ ] **드로어에 상태 필드가 없고**, 만들어진 업무의 상태가 항상 「시작전」이다
  - [ ] 「임시저장」 배지가 **없다**(SPEC-003 S003-OQ-1)
  - [ ] 이미 일정이 있는 시각을 기한에 넣으면 「**그 시간에 다른 일정이 있습니다**」 토스트가 뜨고 **드로어가 닫히지 않으며 입력이 남는다**
  - [ ] 첨부 팝오버에서 「URL 링크」로 두 건을 **연달아** 붙일 수 있다(팝오버가 닫히지 않는다)
  - [ ] 「자료함 문서」 세그먼트에는 **「자료함이 아직 없습니다」 안내**가 보이고 붙일 수 있는 것이 없다
- **완료 증거**: 미작성

### Phase 6 — 상세 드로어 · 전체 페이지 승격 · 인라인 편집 · 자식 블록

- **Status**: TODO
- **설명**: 이 work 의 완성 지점 — **업무를 열어서 그 자리에서 고친다.** 드로어와 페이지가 **같은 본문 컴포넌트**를 쓰는 것이 구조의 핵심이라, 두 표면을 같은 Phase 에서 붙여 규격이 갈리지 않게 한다.
- **작업**:
  - [ ] `TaskDetailBody.tsx` — 블록 6(배경·목표 / 할일 / 참고자료·연관업무 / 결과자료·완료 결과 / 메모 / 로그). **부모를 모른다**
  - [ ] `TaskDetailDrawer.tsx` — 헤더(유형 배지·프로젝트 칩 / 제목 26·700 / **상태 드롭다운·「완료 처리」·`⋯` 는 자리만 비활성** · 기한 · ⤢ · ×)
  - [ ] `app/(app)/tasks/detail/page.tsx` + `TaskDetailPage.tsx` — breadcrumb · 좌(유동) + 우 528(메모·로그) 2단. **드로어로 되돌리는 버튼 없음**
  - [ ] 인라인 편집(`InlineEditText` 재사용) — 제목·배경·목표·완료 결과. blur 저장 · `Esc` 는 편집 전 값으로 · **저장 버튼 없음**
  - [ ] 자동 저장 실패 — **WORK-003 의 U-7 규격 그대로**(토스트 + 필드 실패 테두리 + 「다시 저장」, 자동 재시도 없음). **새로 만들지 않는다.** **실패 상태는 `saveFailed`·`onRetry` prop 으로 받고 소유자는 블록**이며, 기한 트리거·셀렉터 같은 **팝오버형 컨트롤의 실패는 그 행 아래 인라인 자리 하나**에 모은다(SPEC-002 U-7, 2026-09-06 확정)
  - [ ] 할일(진행률 바·체크·삭제·인라인 추가) · 메모(시간 78 + 내용 2단, 등록만) · 첨부 2열 · 연관업무(최근 5 + 「전체 n 보기」) · 로그(dot 규칙)
  - [ ] 「결과자료 · 완료 결과」 카드 — 미충족 시 「**완료 시 필요**」 칩 · 게이트 유도 진입 훅(스크롤 + 포커스 + 1.5초 강조)을 **WORK-005 가 부를 수 있게 노출**
  - [ ] 로딩 스켈레톤(`#F1F2F5`, 애니메이션 없음) · 「없는 업무입니다」 + 「목록으로」(**리다이렉트 금지**)
  - [ ] 반응형 — 1280~1439 에서 드로어 전체화면 + 2열 블록 1열로 쌓기, 전체 페이지는 좌 유동 + 우 400
- **검증**:
  - [ ] 리스트가 없는 상태에서도 `?id=` 로 상세를 열 수 있고, **드로어와 전체 페이지가 같은 블록·같은 규격**으로 보인다
  - [ ] 제목을 고치고 바깥을 클릭하면 **저장 버튼 없이** 저장되고 **로그에는 남지 않는다**
  - [ ] 할일을 체크하면 진행률 「n / m」이 즉시 바뀌고 **로그에 「할일 n건 완료」**가 생긴다
  - [ ] 완료 결과를 적으면 「**완료 시 필요**」 칩이 사라진다
  - [ ] 연결한 업무를 열면 **반대편에도 이 업무가** 보인다
  - [ ] ⤢ 를 누르면 **전체 페이지**로 바뀌고 메모·로그가 우측에 붙는다. breadcrumb 로 돌아온다
  - [ ] 없는 업무 주소로 들어가면 「**없는 업무입니다**」가 뜨고 **자동으로 튕기지 않는다**
  - [ ] **서버를 내린 채** 배경을 고치면 토스트 + 그 필드 「저장되지 않았습니다 · 다시 저장」이 뜨고, **가만히 두어도 네트워크 탭에 재요청이 0건**이다. 서버를 올리고 「다시 저장」을 누르면 저장된다
  - [ ] **기한을 바꿀 때는 응답이 오기 전까지 값이 바뀌지 않는다**(낙관적 갱신을 하지 않는 것의 실측 — 네트워크를 느리게 해 확인)
  - [ ] **서버를 내린 채 유형을 바꾸면**(팝오버형 컨트롤) 트리거 테두리가 실패색이 되고 **그 행 아래 인라인 자리**에 「유형이 저장되지 않았습니다 · 다시 저장」이 뜬다 — 캡션이 컨트롤 안에 끼거나 레이아웃이 밀리지 않는다
  - [ ] **정적 검사**: 자동 저장 실패 상태를 `useState` 로 들고 있는 컴포넌트가 **0건**이다(prop 으로 받는다 — grep 결과를 완료 증거에)
  - [ ] 상태 드롭다운·「완료 처리」·`⋯` 는 **보이지만 눌러도 아무 요청이 나가지 않는다**(WORK-005 가 연결한다)
  - [ ] 창을 1280~1439 로 줄이면 드로어가 전체 화면이 되고 2열 블록이 1열로 쌓인다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 신규 env 가 없다(`APP_TIMEZONE` 은 WORK-001 이 이미 잡았다)
- [ ] 목록·상세 응답에 **다른 계정의 업무가 섞이지 않는다**(소유 검사가 service 에 있다)
- [ ] 응답에 **`storage_path`·내부 경로·스택 트레이스가 실리지 않는다**
- [ ] 삭제가 **소프트**이고 하드 삭제 경로가 없다(이 work 는 삭제 표면을 만들지 않지만 스키마가 그 전제다)

## Rollback

- **스키마**: `alembic downgrade -1` 로 업무 도메인 + `schedule` 리비전을 되돌린다. **WORK-003 까지의 데이터(계정·유형·프로젝트)는 영향이 없다** — 업무 테이블이 그들을 참조하는 방향이라 자식이 먼저 사라진다
- **백엔드**: `task_router` 미등록으로 표면을 걷어낼 수 있다. `schedule_service` 는 아직 다른 소비자가 없으므로 함께 되돌려도 영향이 없다 — **단 WORK-006 이 시작된 뒤에는 되돌리지 않는다**(회의 겹침 검사가 이 서비스를 부른다)
- **프론트**: 브랜치 폐기. `OverlayProvider` 의 `openDrawer` 를 되돌리면 이후 work 의 드로어가 전부 열리지 않으므로 **Phase 4 는 단독으로 되돌리지 않는다**
- 부분 revert 시: Phase 5·6 만 되돌리면 API 는 살아 있고 화면만 없어진다 — `/tasks` 는 WORK-002 의 빈 셸로 돌아간다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-003 §6 Acceptance 16개 항목이 확인**됐다. **단 「첨부한 문서를 누르면 문서함 상세로 이동한다」 1건은 문서함 work 이후로 미룬다**(§Open Issues)
- [ ] 정적 검사 6종(`schedule` 쓰기 격리 · 계층 위반 · `Sheet`/`Dialog` 직접 import · 색 hex/`new Date()` · **드로어 폭 리터럴 격리** · **실패 상태 내부 state 0**) 결과가 완료 증거에 붙어 있다.
- [ ] BE §12 필수 테스트 중 **3(겹침)·5(파생)·5-a(조인 없음)·9(고아 없음)** 가 통과한다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **첨부의 「자료함 문서」 갈래가 이 work 에서 닫혀 있다.** 문서함(SPEC-005)이 다음 그룹으로 미뤄져 `document` 테이블이 없다. 임시 계약은 ① `task_attachment.document_id` 는 **컬럼·CHECK 만 최종 형태로** 두고 **FK 를 걸지 않는다** ② `kind='doc'` 요청을 서비스가 거부한다 ③ 팝오버 문서 세그먼트는 **빈 상태 안내**다. **문서함 work 가 FK 추가 리비전과 함께 이 갈래를 실체화한다** — SPEC-003 §4 계약과 일시적으로 어긋나는 지점이라 코디 확인이 필요하다
- **`invalid_work_type` 코드가 아키텍처 §8-2 표에 없다**(SPEC-003 S003-OQ-2). 구현은 SPEC-003 §4 를 따르고 표 갱신은 코디 소관
- **`schedule` 을 이 work 가 만든다.** 캘린더 그룹의 자산이지만 업무 기한이 그 원본이라 여기서 서지 않으면 겹침 검사(SPEC-003 S-3)가 성립하지 않는다. **캘린더 work 는 `GET /api/schedules` 와 화면만** 만든다
- **본문 길이 상한(제목 200 · 배경/목표/완료 결과 4000)은 spec 판단이다**(SPEC-003 S003-OQ-5). 정책서에 근거가 없다
- **메모 수정·삭제 · 연관업무 팝오버의 「새 업무로 만들기」 · 「임시저장」 배지를 만들지 않았다**(S003-OQ-1·3·4). 필요하면 DEC-002 갱신이 먼저다
- **상세 헤더의 상태 컨트롤이 이 work 에서 비활성이다.** WORK-005 착수 전까지 사용자가 업무를 완료로 보낼 수 없다 — 두 work 를 연달아 진행하는 것을 전제한다

## Related

- SPEC: SPEC-003 (frontmatter `links.specs`)
- Work: WORK-001 · WORK-002 · WORK-003 (선행) · WORK-005 (후속)
