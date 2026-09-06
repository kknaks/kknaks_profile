---
type: work
id: WORK-008
title: "회의록 — 종료 파이프라인 · 통합본 · 편집 · 업무 연동 · 상세 드로어"
status: done
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
progress: 100
created_at: 2026-09-06
updated_at: 2026-09-06
tags:
  - product/task-management
  - doc/work
  - status/done
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-008]
  works: [WORK-004, WORK-005, WORK-006, WORK-007]
  releases: []
  related: [DEC-002, DEC-005, SPEC-003, SPEC-004, SPEC-006, SPEC-007, SPEC-009]
---

# 회의록 — 종료 파이프라인 · 통합본 · 편집 · 업무 연동 · 상세 드로어

**회의를 끝내고, 통합본과 한 줄 요약을 만들고, 그 회의록을 고치고, 거기서 업무를 만들고 갱신한다.** 회의 중 화면(WORK-007)이 「회의 종료」를 누른 뒤부터가 이 work 다. 트리 컴포넌트 · 근거 칩 · 트랜스크립트 · `MeetingDetail` 은 만들지 않는다 — WORK-006 · 007 것을 쓴다. 업무 판정도 만들지 않는다 — WORK-004 · 005 의 `task_service` 를 그대로 부른다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003
- Covers spec: **SPEC-008**(회의록 — 종료 · 통합 · 편집 · 업무 연동, v0.0.3)
- Depends on work: **WORK-006**(`meeting` 도메인 마이그레이션 · `MeetingDetail` · `PATCH /api/meetings/{id}` · `PATCH …/agendas/{id}` · 삭제 모달 · 첨부 탭) · **WORK-007**(AI 배치 계약 · `meeting_batch_service` · `AgendaLineTree` · 근거 칩 스크롤 · `GET …/transcript` · `POST …/lines` · 회의 중 「회의 종료」 버튼 자리) · **WORK-005**(`PATCH /api/tasks/{id}/status` · `task_service.change_status()` · 완료 게이트 · 완료 토스트/실행취소) · **WORK-004**(`task_service` 생성 · 부분 수정 · `task_memo` 추가 · `DrawerFrame` · `Selector` · 상세 드로어 구조) · **아키텍처 반영분 2026-09-06**(ERD `meeting_line.source_human_line_id`/`source_ai_line_id` 부분 UNIQUE · `meeting_agenda.source_agenda_id` · `job` · `ai_headline` 규칙 M-19 · 줄 삭제 M-20 · BE §6 `progress` · §8-2 `invalid_meeting_status`)
- Parallel work: 캘린더 그룹 — 이 work 의 **회의 상세 드로어(SPEC-008 U-4)** 를 재사용한다. 드로어가 서기 전까지 캘린더 회의 블록 클릭은 빈 자리다
- Follow-up work: 없음 — 회의록 영역의 마지막 work 다. **WORK-006 목록 미리보기**의 `ended` 렌더가 이 work 의 통합본 · 한 줄 요약을 읽는다(SPEC-006 U-8 「SPEC-008 이 정본」)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다
  - **open-kknaks 워커(codex)** — ① 마지막 배치 · ② 통합본 생성이 여기서 돈다. 프롬프트 · `output_schema` 는 WORK-007 의 `ai_schemas/` 에 통합용 파일 하나를 더한다. Soniox 는 이 work 가 직접 부르지 않는다(스트림 종료 프레임은 WORK-007 의 `meeting_stream_service` 가 보낸다)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR | `kknaksss/docs-v1` — a48cbe2 · a5ae4c6 · 580846a · d44a3e5 |
| Blocker | WORK-006 · WORK-007 미완 |
| Next | Phase 1 — job 실행기 · 종료 파이프라인 · 통합 규칙 구조 검증 · 한 줄 요약 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-008 §6 Acceptance **25개** 대조 | todo |
| Design |  | 생성중 회색 바 · 실패 배너 · 한 줄 요약 바(페이지 56 / 드로어 72) · 「제거」 고스트 버튼 · 줄 삭제 모달 문구 · 회의 상세 드로어 | todo |
| FE |  | 폴링 훅 → 상세 페이지 상태 3종 → 편집 모드 · 드로어 3종 · 삭제 모달 → 업무 연동 버튼 → 회의 상세 드로어 · 반응형 | todo |
| BE |  | job 실행기 · 종료 파이프라인 ①② · 통합 구조 검증 · 종료 후 편집 표면 · 줄 ↔ 업무 한 트랜잭션 입구 | todo |
| QA |  | Phase 검증(앱 창 E2E) · **완료 게이트 우회 0건 실측** · 통합 검증 실패 케이스 · 정적 검사 | todo |
| Ops |  | 해당 없음 — 신규 env 없음(codex · Redis 는 WORK-007 이 잡았다). job 상한 900초 · 통합 180초 · 최종 배치 300초는 `config.py` 상수 | todo |

## Scope

포함:

- **job 실행기** — `job` 행 정본 · back 프로세스 asyncio 태스크 · **상한 900초 마감** · **기동 스윕**(BE §5-3) · `GET /api/jobs/{id}`(`progress` 파생)
- **종료 파이프라인** — `POST /api/meetings/{id}/end`(WS 닫기 · `active`→`done` · `generating` · job) → ① 마지막 배치(AI 트랙 전량 교체, 300초) → ② 통합본 + `headline`(180초 × 3회) → `ended`+`succeeded`/`failed`. `POST …/integrate`(② 만 재실행)
- **통합 규칙의 구조 검증** — 사람 줄 전수 · 이중 계승 금지 · AI 줄 중복 참조 금지 · 참조 없는 줄 금지 · 안건 축 · `headline` 1~200자. **모델은 참조 id 와 자리 · `headline` 만 낸다** — 본문은 서버가 원본에서 복사
- **종료 후 편집 표면** — `POST …/lines` 확장(`detail` · `taskId` · `pendingChange` · `newTask`) · `PATCH …/lines/{id}`(본문 · 종류) · **`DELETE …/lines/{id}`**(회의록 탭 트랙만 · 하드) · **`PATCH …/agendas/{id} {title}`** 의 `ended` 확장 · 트랙 규칙 · 상태 잠금
- **업무 연동** — `POST …/lines/{id}/task`(액션 줄 → 업무 생성) · `PATCH …/lines/{id}/task`(`pendingChange` 적용) — **`task_service` 를 한 트랜잭션에서 부르는 입구**, 판정 없음
- **화면** — 생성중(U-1) · 실패 배너(U-2) · 상세 페이지(U-3 — 한 줄 요약 바 · 통합본 탭 · AI 탭 종료 후 캡션 · 메타 인라인 편집) · 회의 상세 드로어(U-4) · 근거 펼침의 종료 후 조건(U-5) · 줄 버튼(U-6) · 편집 모드(U-7 — 「제거」 · 안건 제목 · 추가 칩) · 드로어 3종(U-8 ~ U-10) · 반응형(U-11)
- 폴링 훅(2초 · 480회 상한 · 「다시 확인」)

제외:

- 회의 생성 · 목록 · 시작 전 · 삭제 모달 · 첨부 탭 · `MeetingDetail` 기본 형태 → **WORK-006**
- 회의 중 화면 · 스트림 · 배치 증분 · `AgendaLineTree` · 근거 칩 스크롤 규칙 · 트랜스크립트 표면 · `POST …/lines` 의 회의 중 갈래 → **WORK-007**. 「회의 종료」 버튼의 **자리 · 활성 조건**도 WORK-007 이고 이 work 는 **눌렀을 때 부를 요청과 그 뒤**만 만든다
- 업무 생성 규칙 · 상태 전이 · 완료 게이트 · 실행취소 · 완료 토스트 → **WORK-004 · 005**. 이 work 는 **부른다**
- 캘린더 화면 → 캘린더 그룹. 이 work 는 드로어를 `openDrawer` 로 열 수 있게 만들어 둔다
- **줄 순서 이동 · 종료 후 안건 추가/삭제 · 문단 요약 · 되돌리기 · 근거 구간 수동 선택** — SPEC-008 §7 이 뺐다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보 — 경로는 `backend/README.md` §4 · `frontend/README.md` §2 의 트리를 따른다. WORK-006 · 007 이 만든 파일은 **확장**이고 새 파일은 **신규**로 표시한다

| 경로 후보 | 설명 |
|---|---|
| `app/back/models/meeting.py` | (WORK-006) `meeting_line.source_human_line_id` · `source_ai_line_id` 와 CHECK · 부분 UNIQUE 두 건이 **이미 있는지 확인**. 없으면 아래 리비전 |
| `app/back/models/job.py` **신규**(WORK-006 이 안 만들었으면) | `job` — `kind` · `target_type` · `target_id` · `status` · `attempt` · `error_code` · `error_message` · `finished_at`(`database/README.md` ERD) |
| `app/back/alembic/versions/*_meeting_close.py` **조건부** | `source_*_line_id` + 부분 UNIQUE · `job` 테이블 · 인덱스 `(account_id, status)` · `(target_type, target_id)`. WORK-006 리비전이 2026-09-06 ERD 를 이미 담았으면 **없음**(§Domain / Schema) |
| `app/back/core/enums.py` | `JobStatus` · `JobErrorCode`(`integration_failed` · `integration_timeout` · `job_timeout`) · `IntegrationState` 확인 |
| `app/back/core/exceptions.py` | `InvalidMeetingStatusError`(409 `invalid_meeting_status`) — WORK-006 이 만들었으면 재사용 |
| `app/back/config.py` | `MEETING_FINAL_BATCH_TIMEOUT_SEC=300` · `MEETING_INTEGRATION_TIMEOUT_SEC=180` · `MEETING_INTEGRATION_ATTEMPTS=3` · `JOB_TIMEOUT_SEC=900` — **SPEC-008 §4 수치의 단일 출처** |
| `app/back/ai_schemas/meeting_integration.json` **신규** | ② 통합 출력 스키마 — `agendas[]{agendaRef, lines[]{sourceHumanLineId, sourceAiLineId}}` + `headline`. **본문 필드가 없다** |
| `app/back/repository/job_repository.py` **신규** | job CRUD · 활성 job 조회(`activeJobId` 파생) · 기동 스윕 대상 조회 |
| `app/back/repository/meeting_line_repository.py` | (WORK-007 확장) `merged` 트랙 벌크 INSERT · 트랙별 DELETE · 단건 삭제 + `order_index` 당김 · `task` 요약 조인(`get_including_deleted`) · `mergedSummary` 집계 |
| `app/back/service/job_service.py` **신규** | 실행기 — 태스크 기동 · 단계마다 세션 · **상한 마감** · **기동 스윕** · `progress` 파생 |
| `app/back/service/meeting_finalize_service.py` **신규** | `/end` · `/integrate` · ① 최종 배치 호출(WORK-007 `meeting_batch_service` 의 배치 함수를 **범위 = 전체**로 재사용) · ② 통합 호출 · 재시도 · 상태 전이 |
| `app/back/service/meeting_merge_service.py` **신규** | **통합 규칙 구조 검증 + `merged` 조립** — 순수 함수에 가깝게. 모델 출력 → 검증 → `merged` 안건 · 줄 dto + `headline` |
| `app/back/service/meeting_edit_service.py` **신규** | 종료 후 편집 — 줄 추가(확장 갈래) · 수정 · 종류 전환(`task` 이탈 시 연결 해제) · **삭제(M-20)** · 안건 이름 · **트랙 규칙 · 상태 잠금 한 곳** |
| `app/back/service/meeting_task_link_service.py` **신규** | 줄 ↔ 업무 입구 — `create_task_from_line()` · `apply_pending_change()`. **`task_service` 를 부를 뿐 판정하지 않는다** |
| `app/back/service/task_service.py` | (WORK-004 · 005) **고치지 않는다.** `create()` · `update()` · `change_status()` · `add_memo()` 를 그대로 부른다. 필요하면 **같은 트랜잭션에서 부를 수 있게 세션을 인자로 받는 시그니처만** 확인 |
| `app/back/integrations/agent.py` | (WORK-007) 통합 제출 — `resume` 같은 세션 · `output_schema=meeting_integration.json` · 타임아웃 인자 |
| `app/back/api/meeting_router.py` | (WORK-006 · 007 확장) `POST /{id}/end` · `POST /{id}/integrate` · `PATCH /{id}/lines/{lineId}` · `DELETE /{id}/lines/{lineId}` · `POST /{id}/lines/{lineId}/task` · `PATCH /{id}/lines/{lineId}/task` · `POST /{id}/lines` 확장 갈래 · `PATCH /{id}/agendas/{agendaId}` 의 `ended` 갈래 |
| `app/back/api/job_router.py` **신규** | `GET /api/jobs/{id}` |
| `app/back/schemas/meeting.py` · `dto/meeting.py` | `MeetingDetail` 에 `durationMinutes` · `activeJobId` · `finalBatchState` · `mergedSummary` 추가 · `LineItem` 에 `sourceHumanLineId` · `sourceAiLineId` · `task{status,dueDate,isDeleted}` · `LineCreate` 확장 · `LineUpdate` · `LineTaskCreate` · `JobItem` |
| `app/back/tests/test_meeting_finalize.py` · `test_meeting_merge.py` · `test_meeting_edit.py` · `test_meeting_task_link.py` · `test_job.py` | §Execution 의 검증 항목 |
| `app/front/src/features/meetings/hooks/useMeetingFinalizeJob.ts` **신규** | 폴링 2초 · 480회 · 종결 시 `['meetings','detail',id]` + `['meetings','list',…]` 무효화 · 「다시 확인」 |
| `app/front/src/features/meetings/hooks/useMeetingEdit.ts` **신규** | 줄 수정 · 종류 · 추가 · 삭제 · 안건 이름 뮤테이션 + 낙관적 표 |
| `app/front/src/features/meetings/hooks/useMeetingTaskLink.ts` **신규** | 업무 생성 · 업무 갱신 **뮤테이션 하나씩** — 줄 버튼 · 연관 업무 드로어 ② · 액션 드로어가 공유 |
| `app/front/src/features/meetings/components/MeetingDetailBody.tsx` **신규** | **드로어와 전체 페이지가 공유하는 본문** — 상단 바 슬롯 · 탭 · `AgendaLineTree` 호출. `mode: 'page' \| 'drawer'` 로 버튼 · 편집 유무만 갈린다 |
| `app/front/src/features/meetings/components/MeetingDetailPage.tsx` · `MeetingDetailDrawer.tsx` **신규** | 두 표면의 껍데기. 페이지는 `app/(app)/meetings/detail/page.tsx` 가 `status` 로 WORK-006(시작 전) · WORK-007(회의 중) · 이 work(생성중 · 종료) 를 갈라 부른다 |
| `app/front/src/features/meetings/components/HeadlineBar.tsx` · `GeneratingBar.tsx` · `IntegrationFailedBanner.tsx` **신규** | 상단 바 슬롯의 세 상태 |
| `app/front/src/features/meetings/components/MeetingMetaInline.tsx` **신규** | 제목 · 일시 · 유형 · 프로젝트 인라인 컨트롤 — 페이지 · 드로어 공용 |
| `app/front/src/features/meetings/components/AgendaLineTree.tsx` | (WORK-007) **확장만** — `editable` · `showTaskButtons` · `onDeleteLine` · `onChangeKind` · `onRenameAgenda` · 「+」 칩 슬롯. **두 번째 트리를 만들지 않는다** |
| `app/front/src/features/meetings/components/LineTaskButton.tsx` · `LineKindSelector.tsx` · `LineDeleteModal.tsx` · `AgendaTitleInline.tsx` **신규** | 줄 버튼(U-6) · 종류 셀렉터 · 삭제 모달(`ConfirmModal` 프레임) · 안건 제목 입력 |
| `app/front/src/features/meetings/components/AddLineDrawer.tsx` · `LinkTaskDrawer.tsx` · `CreateTaskFromLineDrawer.tsx` **신규** | U-8 · U-9 · U-10 — `DrawerFrame`(WORK-004) 위에 |
| `app/front/src/features/meetings/api.ts` · `types.ts` | 호출 함수 · 타입 미러(`types/api.ts`) |
| `app/front/src/lib/api/queryKeys.ts` | `['jobs', id]` 등록 · 무효화 표 연결 |

- Domain / schema note: 스키마는 **2026-09-06 ERD 가 이미 담고 있다.** 이 work 의 리비전은 **WORK-006 리비전이 그 ERD 를 반영했는지에 따라 조건부**다(아래)

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | `status` 전이 `recording → generating → ended` · `integration_state` · **`ai_headline`**(M-19) 을 이 work 가 처음 쓴다 |
| `meeting_agenda` | `merged` 트랙 INSERT(`source_agenda_id` = 사람 안건 또는 AI 신설 안건) · `/end` 의 `active → done` · 종료 후 `title` 수정(M-5-e ②) |
| `meeting_line` | `merged` 트랙 INSERT(`source_*_line_id`) · 종료 후 수정 · **하드 삭제**(M-20) · `task_id` · `pending_change` 쓰기 |
| `meeting_batch_run` | `phase='final'` · `'integration'` 행 — `progress.phase` · `finalBatchState` · 「MM:HH 종결」의 원천 |
| `job` | `kind='meeting_finalize'` — 정본. `attempt` · `error_code` |
| `task` · `task_memo` · `task_log` | **이 work 가 직접 쓰지 않는다.** `task_service` 가 쓴다 |

- 상태 / invariant: `domains/meeting.md` **M-3 · M-4**(상태 · 통합 상태) · **M-5-c**(`ended` 에 `active` 없음) · **M-5-d · M-5-e**(안건은 이름만) · **M-6 · M-7**(AI 트랙 전량 교체는 최종 배치 한 번) · **M-8 · M-8-a**(통합 줄 = 원본 복사 + 참조 · 부분 UNIQUE) · **M-14 · M-14-a**(`task_id` 는 버튼으로만 · `pending_change` 3필드) · **M-15 · M-16**(화이트리스트 · 스키마 위반 폐기) · **M-19**(`ai_headline`) · **M-20**(줄 삭제 경계 셋 · 하드) · `database/README.md` **§0-1**(자식 행 하드) · `task.md` **T-5 · T-6**(게이트 · 그래프 — 부르기만)
- Migration 필요 여부: **조건부.** WORK-006 의 회의 도메인 리비전이 `meeting_line.source_human_line_id`/`source_ai_line_id`(+ CHECK + 부분 UNIQUE 2) · `job` 테이블 · `meeting_agenda.source_agenda_id` 를 **이미 담았으면 없음.** 담지 않았으면 이 work 가 **리비전 1건**(`downgrade` 포함)으로 더한다. 어느 쪽인지는 **Phase 1 첫 작업에서 확인하고 이 문서에 적는다**
- SPEC 에 환류해야 하는 변경: 없음. 키 이름(`agendas.*` · `latestBatchSeq`) · 에러코드(`invalid_meeting_status` 하나) · 자식 쓰기 응답(`MeetingDetail` 전체 · 삭제만 204)은 SPEC-006 정본 그대로다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **캘린더 그룹** | `openDrawer({ key:'meeting-detail', … })` 로 여는 **회의 상세 드로어**(`MeetingDetailDrawer`) · 드로어 안의 `PATCH /api/meetings/{id}` 일시 편집 · 콜백 | SPEC-009 U-7 이 여는 드로어가 이것이다(DEC-005 §2). 드로어는 부모를 모른다 |
| **WORK-006 목록 미리보기** | `ended` 렌더 규칙 — `AgendaLineTree(track='merged', editable=false)` · `headline` | SPEC-006 U-8 「SPEC-008 이 정본, 읽기 전용으로 그대로」. 미리보기가 이 work 의 컴포넌트 규격을 **읽기 전용 모드로** 쓴다 |
| **WORK-007 회의 중 화면** | 「회의 종료」 → `useMeetingFinalizeJob.end()` → 화면 전환(같은 라우트, `status` 분기) | 버튼 자리 · 활성 조건은 WORK-007, 눌렀을 때의 요청 · 그 뒤는 이 work |
| **WORK-005** | 이 work 가 **소비**한다 — `task_service.change_status()` · 완료 토스트/실행취소 · 거부 토스트의 「결과 입력」 유도 훅 | 완료 게이트의 **네 번째 진입점**(WORK-005 L294) |
| **WORK-004** | 이 work 가 **소비**한다 — `task_service.create()` · `update()` · `add_memo()` · `DrawerFrame` · `Selector` · 첨부 팝오버 규격 | WORK-004 L156 「회의록의 업무 생성 · 갱신이 `task_service` 를 그대로 부른다」 |

## Internal Interface Contract

외부 계약(엔드포인트 · 요청/응답 · 검증 · 에러 · 수치)은 **SPEC-008 §4** 가 정본이다. 후속 work 와 이 work 의 Phase 사이가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`job_service`** | job 행이 정본, 실행은 back 프로세스의 asyncio 태스크(BE §5-3). `start(kind, target)` 가 행을 만들고 태스크를 띄운다 · **단계마다 세션을 새로 열고 끝에 commit**(BE §7 — 외부 호출 중 트랜잭션을 열어 두지 않는다) · **상한 900초**를 넘기면 `failed(job_timeout)` 로 마감 · **기동 스윕**이 `queued/running` 잔여를 재개하거나 실패로 마감하고, 스윕 실패는 기동을 막지 않는다 · `progress` 는 **파생**(`meeting_batch_run` 최신 `phase` + `job.attempt`) |
| **`meeting_finalize_service`** | `end()` = WS 닫기 요청(WORK-007 서비스) → `active→done` → `generating`/`running` → job. `run_pipeline()` = ①(300초, 실패해도 ②로) → ②(180초 × 3회, 즉시 재시도). **`integrate()` 는 ②만** 돈다. 상태 · `integration_state` · `ai_headline` · `merged` INSERT 는 **한 트랜잭션** |
| **`meeting_merge_service.validate_and_build()`** | 입력 = 사람 트리 · AI 트리 · 모델 출력. **검증 6 + 헤드라인 1**(SPEC-008 §4 통합 규칙 표)을 전부 통과해야 `merged` dto 를 돌려주고, 하나라도 어기면 `IntegrationAttemptFailed` 를 던진다(재시도 대상). **본문은 원본에서 복사**한다 — 모델 출력의 텍스트 필드를 읽는 코드가 이 함수에 없다(`headline` 제외). 순수 함수에 가깝게 두어 **테스트가 DB 없이 돈다** |
| **AI 트랙 전량 교체** | ① 결과가 검증을 통과한 뒤에만 `DELETE + INSERT`. 검증 전에 지우지 않는다(M-7 · SPEC-008 §5) |
| **`meeting_edit_service`** | **트랙 규칙과 상태 잠금이 여기 한 곳**이다 — `ended` 만 · `succeeded` 면 `merged` · `failed` 면 `human` · `ai` 는 항상 거부(M-20 · M-5-e). 라우터 · 다른 서비스가 트랙을 다시 판정하지 않는다. `delete_line()` 은 **그 행 하나만 하드 삭제 + 뒤 줄 `order_index` 당김** — `task_service` · 트랜스크립트 · 원본 줄을 건드리는 코드가 이 경로에 없다(정적 검사 대상) |
| **`meeting_task_link_service`** | `create_task_from_line(line, task_create_dto)` 와 `apply_pending_change(line)` 둘. **`task_service` 를 같은 세션에서 부르고 줄을 갱신한다 — 한 트랜잭션.** 상태 전이는 `task_service.change_status()` **그 함수**(WORK-005 L147 「`task.status` 를 대입하는 코드는 이 함수 안에만」) · `pendingChange.status` 가 현재 상태와 같으면 **부르지 않는다**(SPEC-004 L478) · 거부(`TaskCompletionBlockedError` · `InvalidStatusTransitionError`)는 그대로 전파하고 **롤백** · `pending_change` 는 성공 시에만 `NULL` |
| **`/end` 의 사전 조건** | `status='recording'` 하나. **스트림 상태를 보지 않는다** — `paused/stream` 에서도 받는다(BE §8-2 L243 · SPEC-007 U-1 L113). WS 가 살아 있으면 WORK-007 의 스트림 레지스트리에 닫기를 요청하고, 없으면 그냥 진행한다. `scheduled`·`generating`·`ended` 는 `InvalidMeetingStatusError`(409) |
| **`MeetingDetailBody`** | 드로어와 전체 페이지가 공유하는 **유일한 본문**. `mode='page'` 에서만 「편집」 · 줄 버튼 · 「제거」 · 스크립트 패널 · 첨부 쓰기가 켜진다(SPEC-008 U-4 「드로어에서 빠진 것 넷」). 상단 바 슬롯은 `status`·`integrationState` 로 `GeneratingBar` / `IntegrationFailedBanner` / `HeadlineBar` 를 고른다. **부모를 모른다** — `onExpand` 콜백만 |
| **`AgendaLineTree` 확장** | WORK-007 컴포넌트에 `editable` · `showTaskButtons` · `renderLineAction`(「제거」) · `onChangeKind` · `onRenameAgenda` · `renderAgendaFooter`(「+」 칩 4) 를 **prop 으로** 더한다. 회의 중 화면은 전부 `false`/미지정으로 부르므로 **WORK-007 의 렌더가 바뀌지 않는다**(회귀 검사 대상). 두 번째 트리 컴포넌트를 만들지 않는다 |
| **`HeadlineBar`** | `headline` + `mergedSummary` 를 받는다. 페이지 = 56 한 줄(문장 말줄임) · 드로어 = 72 두 줄. **값 · 색은 하나**, 다른 것은 줄 나눔뿐(SPEC-008 U-4). `headline` 이 `null` 이면 그리지 않는다 |
| **`useMeetingFinalizeJob`** | `end()` · `integrate()` · 폴링(2초 · **480회 상한** · 종결에서 멈춤) · 폴링 실패 시 「다시 확인」 상태 · 종결 시 `['meetings','detail',id]` + `['meetings','list',…]` 무효화. 페이지 재진입은 `MeetingDetail.activeJobId` 로 잇는다 |
| **`useMeetingTaskLink`** | 업무 생성 · 업무 갱신 **뮤테이션 각 하나**를 줄 버튼(U-6) · 연관 업무 드로어의 ②(U-9) · 액션 드로어(U-10) 가 공유한다. 화면마다 호출을 만들지 않는다 — 요청 · 에러 분기 · 토스트가 갈리면 「같은 판정」이 화면에서만 깨진다(WORK-005 `useTaskStatus` 와 같은 결). 완료 성공 시 **WORK-005 의 완료 토스트 · 실행취소를 그대로** 띄운다 |
| 줄 삭제 모달 | `ConfirmModal`(WORK-002) 프레임. 업무 줄이면 경고 슬롯을 채운다. **드로어 모드에서는 열지 않는다**(FE §6-2 — 애초에 「제거」가 없다) |
| 낙관적 갱신 | **한다**: 인라인 본문 · 안건 이름 · 종류 전환(`task` 이탈 제외) · 논의/결정 추가. **하지 않는다**: 줄 삭제 · 업무 생성 · 업무 갱신 · 메타(일시 · 유형 · 프로젝트) · `task` 이탈 전환(SPEC-008 §5 · FE §3-4) |
| 캐시 무효화 | 줄 · 안건 이름 쓰기 · 업무 생성 · 갱신 → `['meetings','detail',id]` + `['tasks',…]` 전부(+ 기한 바뀌면 `['schedules']`). job 종결 → `['meetings','detail',id]` + `['meetings','list',…]`. 메타 → `['meetings',…]` + 일시면 `['schedules']`. **표에 없는 무효화를 하지 않는다**(FE §3-3) |
| 자동 저장 실패 | **WORK-003 U-7 규격 그대로**. `saveFailed` · `onRetry` prop, 소유자는 행/블록(WORK-004 규약) |

## Execution

### Phase 1 — job 실행기 · 종료 파이프라인 · 통합 규칙 구조 검증 · 한 줄 요약 (백엔드)

- **Status**: TODO
- **설명**: **이 work 의 핵심이 여기 있다.** 화면 없이 `curl` 로 `/end` → 폴링 → `ended` 가 돌아야 한다. 통합 규칙을 **구조 검증**으로 못박는 곳이라, 여기서 모델 출력을 믿고 넘기면 이후 어느 화면도 「사람 문장 그대로」를 보장할 수 없다.
- **작업**:
  - [ ] **스키마 확인** — WORK-006 리비전에 `source_*_line_id` + 부분 UNIQUE 2 · `job` · `source_agenda_id` 가 있는지 본다. 없으면 리비전 1건 + `downgrade`. 결과를 §Domain / Schema 에 적는다
  - [ ] `core/enums.py` — `JobStatus` · `JobErrorCode` · `config.py` 상수 4개(300 · 180 · 3 · 900)
  - [ ] `job_repository` · `job_service` — `start()` · 태스크 · 단계별 세션 · **상한 900초 마감** · **기동 스윕** · `progress` 파생 · `GET /api/jobs/{id}`
  - [ ] `ai_schemas/meeting_integration.json` — 참조 id · 자리 · `headline` 만. **본문 필드 없음**
  - [ ] `meeting_merge_service.validate_and_build()` — 검증 7종 · `merged` 조립(본문 · `kind` · `detail` · `task_id` · `pending_change` 는 원본 복사 · `evidence` 는 AI 줄에서 · `source_agenda_id` 매핑 · `order_index`)
  - [ ] `meeting_finalize_service` — `end()`(WS 닫기 · `active→done` · `generating` · job) · ① 최종 배치(WORK-007 배치 함수 재사용, 300초, 실패해도 ②) · ② 통합(180초 × 3회) · 성공 트랜잭션(`merged` INSERT + `ai_headline` + `ended`/`succeeded`) · 실패(`ended`/`failed` · `ai_headline NULL` · `error_code`) · `integrate()`
  - [ ] `POST /api/meetings/{id}/end`(`202`) · `POST …/integrate` · `MeetingDetail` 에 `durationMinutes` · `activeJobId` · `finalBatchState` · `mergedSummary` · `LineItem` 에 `sourceHumanLineId` · `sourceAiLineId`
  - [ ] `tests/test_meeting_merge.py`(DB 없이) · `test_meeting_finalize.py` · `test_job.py`
- **검증**:
  - [ ] `recording` 회의에 `POST /end` → **202 + jobId**, DB `status='generating'` · `integration_state='running'` · `active` 안건이 `done`
  - [ ] **`paused/stream`(WS 없음)에서도 `POST /end` → 202** 이고 파이프라인이 돈다(WS 닫기 요청이 실패로 터지지 않는다). `scheduled`/`ended` 에서 → **409 `invalid_meeting_status`**
  - [ ] 워커 목(mock)이 정상 출력을 주면 폴링이 `succeeded` 로 끝나고 `GET /api/meetings/{id}` 에 `agendas.merged` · `headline` · `mergedSummary` 가 있다. **`merged` 줄의 `content` 가 사람 줄과 바이트 단위로 같다**
  - [ ] 목이 **사람 줄 하나를 빠뜨린 출력** · **같은 사람 줄을 두 번 참조한 출력** · **같은 AI 줄을 두 줄에 붙인 출력** · **참조 없는 줄** · **`headline` 없음/201자** 을 주면 각각 그 시도가 실패로 세어지고, 3회 뒤 `ended`+`failed` · `error_code='integration_failed'` · **`merged` 행 0건 · `ai_headline NULL`**
  - [ ] 목이 통합 출력에 **본문 텍스트를 실어 보내도** `merged.content` 는 원본과 같다(모델 본문을 읽는 코드가 없다)
  - [ ] ① 이 실패(예외 · 300초 초과)해도 **AI 줄이 회의 중 상태 그대로**이고 ②로 넘어가 `succeeded` 가 될 수 있다. `finalBatchState='failed'`
  - [ ] 통합 시도가 180초를 넘기면 그 시도만 실패로 세고, 3회 다 넘기면 `error_code='integration_timeout'`
  - [ ] job 이 900초를 넘기면 `failed(job_timeout)` 로 마감된다. 앱을 재시작하면 **기동 스윕**이 `running` 잔여를 마감하고, 스윕이 예외를 내도 앱은 뜬다
  - [ ] `ended`+`failed` 에서 `POST /integrate` → ②만 다시 돌고(①의 배치 행이 늘지 않는다) 성공하면 `headline` 이 처음 채워진다. `succeeded` 회의에 `/integrate` → **409**
  - [ ] **정적 검사**: `meeting_merge_service` 가 모델 출력에서 읽는 필드가 `agendaRef` · `sourceHumanLineId` · `sourceAiLineId` · `headline` **넷뿐**이다(grep 결과를 완료 증거에) · `ai_headline` 을 쓰는 코드가 `meeting_finalize_service` **한 곳**이다
  - [ ] `pytest` 통과 · `EXPLAIN` 으로 `merged` 트랙 조회가 `(meeting_id, track, agenda_id, order_index)` 인덱스를 탄다
- **완료 증거**: 미작성

### Phase 2 — 종료 후 편집 표면 (백엔드)

- **Status**: TODO
- **설명**: 회의록을 **고치고 지우는** 서버 표면. 트랙 규칙과 상태 잠금이 **서비스 한 곳**에 있어야 이후 화면 · 업무 연동이 같은 규칙을 탄다. 삭제의 경계 셋(M-20)이 여기서 코드가 된다.
- **작업**:
  - [ ] `meeting_edit_service` — 트랙 판정 함수 하나(`ended` · `succeeded→merged` · `failed→human` · `ai` 거부 · `generating` 잠금)
  - [ ] `POST …/lines` 확장 갈래 — `detail` · `taskId`(+ 서버가 `content` = 업무 제목) · `pendingChange` · `newTask`(Phase 5 의 `meeting_task_link_service` 를 부른다 — 이 Phase 에서는 `newTask` 갈래를 `501` 스텁으로 두고 Phase 5 가 채운다) · `recording` 에서는 확장 필드를 **거부**(SPEC-007 규칙 유지)
  - [ ] `PATCH …/lines/{id}` — `content` · `kind`(`task` 이탈 시 `task_id` · `pending_change` NULL · `task` 진입은 `task_id` 있을 때만)
  - [ ] **`DELETE …/lines/{id}`** — 하드 삭제 + 뒤 줄 `order_index` 당김. **원본 줄 · `ai` · 트랜스크립트 · 업무를 건드리지 않는다**
  - [ ] `PATCH …/agendas/{id} {title}` 의 `ended` 갈래(WORK-006 표면 확장) — `merged`/`human` 안건 · `state` 동봉 거부 · 종료 후 `POST`/`DELETE …/agendas` 는 **409**
  - [ ] `tests/test_meeting_edit.py`
- **검증**:
  - [ ] `ended`+`succeeded` 에서 `merged` 줄 본문 PATCH → 200, `human` 줄 PATCH → **422**, `ai` 줄 → **422**. `ended`+`failed` 에서는 반대로 `human` 만 200
  - [ ] `generating` 중 어느 줄 쓰기든 **409 `invalid_meeting_status`**
  - [ ] `merged` 업무 줄을 `kind:"decision"` 으로 바꾸면 `task_id` · `pending_change` 가 NULL 이 되고 **`task` 행은 그대로**다. `task_id` 없는 줄을 `kind:"task"` 로 바꾸면 **422**
  - [ ] `DELETE` 한 `merged` 줄이 `source_human_line_id`/`source_ai_line_id` 로 가리키던 **`human`·`ai` 줄이 DB 에 그대로** 있고, `meeting_transcript` 행 수 · `recording_path` 가 변하지 않는다. 뒤 줄 `order_index` 가 하나씩 당겨진다
  - [ ] `task_id` 가 있던 줄을 `DELETE` 해도 **`task` 행 · `task_log` · `task_memo` 가 그대로**다(업무 쪽 카운트를 삭제 전후로 비교)
  - [ ] 같은 줄을 두 번 `DELETE` → 두 번째는 **404**. `ai` 줄 `DELETE` → **422**
  - [ ] `ended` 에서 `merged` 안건 `{title}` → 200 · `{title, state}` → 422 · `POST …/agendas` · `DELETE …/agendas/{id}` → **409**. `recording` 에서 `{title}` → SPEC-007 규칙대로 거부
  - [ ] **정적 검사**: 트랙을 판정하는 코드가 `meeting_edit_service` **한 함수**뿐이다 · `delete_line` 경로에서 `task_service` · `meeting_transcript` · `storage` 를 import/호출하는 코드 **0건**(grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — 생성중 · 실패 배너 · 상세 페이지 · 한 줄 요약 바 · 폴링 (프론트)

- **Status**: TODO
- **설명**: 앱 창에서 **회의를 끝내고 통합본을 보는** 단계. 상단 바 슬롯 하나를 세 상태가 나눠 쓰고, 트리는 WORK-007 컴포넌트를 `track='merged'` 로 부를 뿐이다.
- **작업**:
  - [ ] `useMeetingFinalizeJob` — `end()` · `integrate()` · 폴링 2초 · 480회 · 「다시 확인」 · 무효화 · `activeJobId` 로 재진입
  - [ ] `app/(app)/meetings/detail/page.tsx` 분기 — `generating` · `ended` 를 이 work 의 `MeetingDetailPage` 로
  - [ ] `MeetingDetailBody`(`mode='page'`) — 상단 바 슬롯(`GeneratingBar` · `IntegrationFailedBanner` · `HeadlineBar`) · 탭 회의록 | AI 요약 · `AgendaLineTree(track='merged' | 'human')` · AI 탭 안내 바 종료 후 문구(「종결 · HH:MM」 / 「배치 n회 반영 · 종결 정리 실패」 / 「… · 종결 정리 중」) · 우 패널(WORK-007 스크립트 패널을 종료 후 옵션으로 · 첨부 탭은 WORK-006)
  - [ ] `HeadlineBar`(페이지 56) · `MeetingMetaInline`(제목 · 일시 · 유형 · 프로젝트 인라인 — WORK-006 `PATCH` 호출, 겹침 토스트 + 원복)
  - [ ] 상태 칩 「회의록 생성중」(스피너) / 「종료된 회의」 · 「삭제」 버튼(WORK-006 모달) — `generating` 잠금
  - [ ] 근거 펼침의 종료 후 조건 — 회의록 탭은 `detail`/`evidence` 있는 줄만 화살표(AI 탭은 WORK-007 그대로) · 스크립트 푸터 「전체 스크립트 n분 · 화자 n명」
  - [ ] 로딩 스켈레톤 · 「없는 회의록입니다」 · 상세/트랜스크립트 조회 실패 표시 + 「다시 시도」
- **검증**:
  - [ ] 회의 중 화면에서 「회의 종료」 → **그 자리에서** 상태 칩 스피너 + 「회의록 생성중」, 상단 바 「AI 요약을 정리하고 있습니다」 → 「회의록을 통합하고 있습니다」 (워커 목의 지연으로 순서를 실측)
  - [ ] 생성중에 「편집」 없음 · 줄 버튼 · 「삭제」 비활성 · 회의록 탭에 **원본 그대로**. **새로고침해도 스피너가 이어진다**
  - [ ] 통합이 끝나면 회의록 탭 문장이 **글자 그대로**, 근거 칩 붙음, AI 탭 「종결 · HH:MM」, **상단에 「AI 한 줄 요약」 배지 + 문장 + 「안건 n · 결정 n · 액션 n」**. 목록 셋째 줄에도 같은 문장(WORK-006 화면에서 확인)
  - [ ] 통합본에 AI 에만 있던 줄이 추가돼 있고 「논의 중」이던 안건이 「완료」
  - [ ] 워커를 내린 채 끝내면 AI 탭 내용이 남고 「종결 정리 실패」. 통합이 3회 실패하면 **배너 + 「다시 생성」**, 한 줄 요약 없음, 원본 노출 + 「편집」 활성. 「다시 생성」은 성공한 회의록에 **없다**
  - [ ] 서버의 job 상한을 짧게 낮춘 채 워커를 멈추면 상한 뒤 **실패 배너**가 뜬다(무한 스피너 없음). 폴링 중 서버를 내리면 스피너 유지 + 「상태를 확인하지 못했습니다 · 다시 확인」
  - [ ] 칩 → 스크립트 스크롤 · 「근거 구간」(WORK-007 규칙) · 회의록 탭에서 `detail`·근거 없는 줄에 화살표 없음
  - [ ] 제목 · 일시를 인라인으로 고치면 저장되고, 겹치는 일시는 토스트 + 원복
  - [ ] **네트워크 탭 실측**: 폴링 간격 2초 · 종결 뒤 상세 GET 한 번 · 재요청이 없다(`retry:false`)
  - [ ] **정적 검사**: 상단 바 슬롯을 그리는 곳이 `MeetingDetailBody` **하나** · 트리 컴포넌트가 `features/meetings/components/AgendaLineTree.tsx` **하나**(두 번째 트리 0건 — grep 결과를 완료 증거에)
- **완료 증거**: 미작성

### Phase 4 — 편집 모드 · 논의/결정 드로어 · 줄 삭제 모달 · 안건 이름 (프론트)

- **Status**: TODO
- **설명**: **회의록을 고치는** 단계. 자동 저장(인라인 · 종류 · 안건 이름)과 확인 모달(삭제)의 경계가 화면에서 갈린다. 업무 연동 드로어 두 개(U-9 · U-10)는 Phase 5 다.
- **작업**:
  - [ ] `useMeetingEdit` — 본문 · 종류 · 추가 · 삭제 · 안건 이름 뮤테이션 + 낙관적 표(SPEC-008 §5)
  - [ ] `AgendaLineTree` 확장 prop — `editable` · `renderLineAction`(「제거」 고스트) · `onChangeKind` · `onRenameAgenda` · `renderAgendaFooter`(「+」 칩 4). **WORK-007 회의 중 렌더가 변하지 않는다**
  - [ ] 편집 모드 헤더 「변경은 자동 저장됩니다 · 편집 완료」(되돌리기 없음) · `LineKindSelector`(「업무」는 `taskId` 있을 때만) · `AgendaTitleInline` · 빈 값 되돌림 캡션
  - [ ] `LineDeleteModal` — `ConfirmModal` 프레임 · 업무 줄 경고 슬롯 · 실패 시 줄 유지 + 토스트
  - [ ] `AddLineDrawer`(U-8) — 세그먼트 논의|결정 · 안건 셀렉터 · 내용 · 상세 설명(근거 구간 입력 **없음** · 「AI 가 채웁니다」 캡션 **없음**)
  - [ ] 자동 저장 실패 — WORK-003 U-7 규격 · `saveFailed` prop
  - [ ] `mergedSummary` 가 응답으로 갱신되어 `HeadlineBar` 카운트가 따라 바뀐다(화면이 세지 않는다)
- **검증**:
  - [ ] 「편집」 → 줄 · 안건 제목이 입력 상자가 되고 헤더에 「되돌리기」가 **없다**. 본문을 고치고 바깥 클릭 → 저장, 로그 없음
  - [ ] 종류를 「결정」으로 → 라벨 색 · 저장. 「업무」는 업무 없는 줄에서 **비활성 + 캡션**. 업무 줄을 「논의」로 → 배지 · 버튼 사라짐(응답 후 반영 — 낙관적 아님)
  - [ ] 안건 제목을 고치고 바깥 클릭 → 저장되고 보기 모드 · 드로어 · 목록 미리보기에 같은 이름. 안건 추가/삭제 버튼 **없음**
  - [ ] 「제거」 → 모달 「이 줄을 삭제할까요?」 → 「삭제」 → 줄 사라짐 · 뒤 줄 당겨짐 · 상단 카운트 갱신. **AI 탭 원본 줄 · 근거 칩 · 스크립트 그대로**. 실패 상태(원본 편집)에서 지워도 AI 탭 그대로
  - [ ] 업무 줄 「제거」 → 경고 슬롯 「연결된 업무는 삭제되지 않습니다」 → 지운 뒤 내 업무에 **그 업무 그대로**
  - [ ] 「+ 결정」 → 드로어에 근거 구간 입력 없음 → 「추가」 → 안건 맨 아래에 줄
  - [ ] **서버를 내린 채** 본문 수정 → 토스트 + 필드 실패 표시 + 「다시 저장」, 재요청 0건. 「제거」 확인 → 줄 **그대로** + 「삭제하지 못했습니다」
  - [ ] **회귀**: WORK-007 회의 중 화면의 트리가 편집 prop 없이 이전과 같이 그려진다(스냅숏 또는 화면 비교)
  - [ ] **정적 검사**: 삭제를 낙관적으로 반영하는 코드 0건(`onMutate` 에 삭제 없음) · 자동 저장 실패 상태를 `useState` 로 드는 컴포넌트 0건
- **완료 증거**: 미작성

### Phase 5 — 업무 연동 (백엔드 + 프론트 · 독립 Phase)

- **Status**: TODO
- **설명**: **완료 게이트의 네 번째 진입점**이 붙는 곳이다(WORK-005 L294). 회의록 쪽에 판정 코드가 **하나도 없어야** 하고, 그걸 이 Phase 의 검증 항목으로 실측한다. 줄과 업무를 한 트랜잭션으로 묶는 입구 둘, 화면은 줄 버튼 하나와 드로어 둘이다.
- **작업**:
  - [ ] `meeting_task_link_service.create_task_from_line()` — `task_service.create()`(SPEC-003 규칙) + 줄 `kind='task'` · `task_id`, **한 트랜잭션**
  - [ ] `meeting_task_link_service.apply_pending_change()` — ① `status`(현재와 다를 때만 `task_service.change_status()`) → ② `dueDate`(`task_service.update()`) → ③ `note`(`add_memo()`) → ④ `pending_change=NULL`. 거부 시 **전부 롤백**
  - [ ] `POST …/lines/{id}/task` · `PATCH …/lines/{id}/task` · `POST …/lines` 의 `taskId`/`newTask` 갈래(Phase 2 스텁 교체) · `pendingChange` 3키 검증(`cancelled` 거부)
  - [ ] `useMeetingTaskLink` — 생성 · 갱신 뮤테이션 각 하나 · 게이트 거부 토스트(WORK-005 규격 + 「결과 입력」 유도) · 완료 성공 시 WORK-005 완료 토스트/실행취소
  - [ ] `LineTaskButton`(U-6) — 「업무 생성」 / 「업무 갱신」(툴팁 = `pendingChange` 키, 같은 상태 제외) / 「갱신 완료」 / 「삭제된 업무」 · `generating` 잠금 · 드로어 모드 숨김
  - [ ] `LinkTaskDrawer`(U-9) — 프로젝트 셀렉터 + 검색 + 후보 목록(`GET /api/tasks/relations/candidates`) · 기한/상태/메모 · 「연결하고 갱신」 = 줄 추가 → 변경 있으면 갱신 뮤테이션
  - [ ] `CreateTaskFromLineDrawer`(U-10) — 제목 프리필 · 유형/프로젝트 · 기한 · 메모(→ `description`) · 「시작 상태」 **없음** · 토글 **없음**
  - [ ] `tests/test_meeting_task_link.py`
- **검증**:
  - [ ] 결과자료도 완료 결과도 없는 업무 줄(`pendingChange.status='done'`)에 `PATCH …/task` → **422 `task_completion_blocked`** 이고 **`task.status` · `due_date` · 메모 수 · `pending_change` 전부 그대로**(기한 · 메모가 먼저 반영되지 않았음을 DB 로 확인 — 롤백 실측)
  - [ ] 결과자료를 붙인 뒤 같은 요청 → 200, 업무가 `done`, `task_log` 에 전이 한 줄, 기한 · 메모 반영, `pending_change NULL`. **완료 토스트 「완료 처리했습니다 · 실행취소」**가 뜨고 실행취소가 WORK-005 와 같이 동작한다
  - [ ] 이미 `done` 인 업무에 `status:'done'` 이 남은 줄 → **409 없이 200**, 기한 · 메모만 반영(전이 로그 없음)
  - [ ] `pendingChange` 에 `cancelled` · 네 번째 키 → **422**. 삭제된 업무 줄 → **404** + 화면 「삭제된 업무」 비활성
  - [ ] 액션 줄 `POST …/task` → 201, 내 업무에 「시작전」 업무 + 로그 「업무 생성」, 줄이 `kind='task'`. 유형을 빼면 422 · 삭제된 유형이면 `invalid_work_type` 이고 **줄이 바뀌지 않는다**
  - [ ] 「+ 연관 업무」 → 후보 목록 · 검색 · 기한만 바꿔 「연결하고 갱신」 → 줄 「갱신 완료」 + 내 업무 기한 변경 + **전이 로그 없음**
  - [ ] 액션 줄 「업무 생성」 드로어에 제목 프리필 · 「시작 상태」 칸 없음 · 만들면 줄이 업무 줄
  - [ ] 「업무 갱신」 거부 시 토스트 「완료하려면 결과자료 1건 또는 완료 결과가 필요합니다」 + 「결과 입력」 → 업무 상세 드로어의 카드로 포커스(WORK-005 유도 훅)
  - [ ] **완료 게이트 우회 0건 — 정적 검사 3종**(grep 결과를 완료 증거에): ① `task.status` 에 값을 대입하는 코드가 `task_service.change_status()` **안에만**(WORK-005 검사의 재실행) ② `meeting_*` 서비스에서 `TaskCompletionBlockedError` · 전이 그래프 · 결과자료를 **참조하는 코드 0건** ③ 프론트에서 업무 API(`/api/tasks/...`)를 직접 부르는 곳이 **후보 검색 `candidates` 하나**뿐(생성 · 갱신은 전부 `/api/meetings/.../task`)
  - [ ] **네트워크 탭 실측**: 「업무 갱신」 한 번에 요청이 **하나**(`PATCH …/lines/{id}/task`)다 — 업무 API 를 나눠 부르지 않는다
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 6 — 회의 상세 드로어 · 반응형 (프론트)

- **Status**: TODO
- **설명**: 캘린더가 재사용할 **두 번째 표면**. 같은 `MeetingDetailBody` 를 `mode='drawer'` 로 감싼다 — 규격이 갈리지 않는 것이 이 Phase 의 목적이다.
- **작업**:
  - [ ] `MeetingDetailDrawer` — `DrawerFrame` 위에 헤더(유형 배지 · 프로젝트 칩 · 제목 · 일시 인라인 · 상태 칩 · `⋯` 삭제 · ⤢ · ×) + `MeetingDetailBody(mode='drawer')` · `HeadlineBar`(72 두 줄 · 툴팁) · 캡션 「편집과 업무 연동은 전체 페이지에서 합니다」 · 칩 표시만
  - [ ] 상태별 본문 — `scheduled`(안건 목록 + 캡션) · `recording`(스냅숏 + 캡션, WS 없음) · `generating`(폴링) · `ended`(배너 또는 한 줄 요약 + 트리)
  - [ ] `openDrawer({ key:'meeting-detail' })` 등록 — 목록(WORK-006) · 캘린더 그룹이 부른다. `⋯` 「삭제」는 드로어를 닫고 모달
  - [ ] 반응형 — 페이지 1280~1439 좌 유동 + 우 400 · 드로어 전체 화면(`DrawerFrame` 규칙) · 한 줄 요약 말줄임
- **검증**:
  - [ ] 목록에서 연 드로어와 캘린더(있으면) 에서 연 드로어가 **같다**. 상단 한 줄 요약(두 줄) · 트리 · 첨부 n 이 보이고 **줄 버튼 · 「편집」 · 「제거」 · 스크립트 패널이 없다** + 캡션
  - [ ] 드로어에서 제목 · 일시를 고치면 저장되고 겹침은 토스트 + 원복. `⋯` → 「삭제」 → 드로어가 닫힌 뒤 모달
  - [ ] ⤢ → 전체 페이지, 같은 회의 · 같은 트리
  - [ ] `generating` 회의를 드로어로 열면 스피너 + 폴링이 돌고 끝나면 통합본으로 바뀐다. `recording` 회의는 스냅숏 + 캡션이고 **WS 연결이 생기지 않는다**(네트워크 탭)
  - [ ] 창을 1280~1439 로 → 우 패널 400 · 한 줄 요약 말줄임 · 드로어 전체 화면 + `←`
  - [ ] **정적 검사**: `Sheet` 직접 import 0건 · 폭 리터럴 `840` 이 `DrawerFrame` 밖 0건(WORK-004 규약) · `MeetingDetailBody` 를 감싸는 껍데기가 **둘**(페이지 · 드로어)이고 본문이 셋이 아니다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 신규 env 없음. `config.py` 상수 4개(300 · 180 · 3 · 900)가 코드에 흩어져 있지 않다
- [ ] job 태스크가 **앱 재시작에서 되살아나거나 마감**된다(기동 스윕) — `running` 으로 영원히 남는 행이 없다
- [ ] 통합 실패 3회 뒤 `merged` 행 0건 · `ai_headline NULL` — **부분 저장이 없다**
- [ ] 줄 삭제가 `human` · `ai` · `meeting_transcript` · 녹음 파일 · `task` 를 건드리지 않는다(Phase 2 검증 재확인)
- [ ] 회의록 경로에서 만든 업무 · 전이가 **내 업무 화면에서 여는 것과 같은 로그**를 남긴다(같은 서비스)
- [ ] 응답에 `ai_session_id` · `recording_path` · 스택이 실리지 않는다
- [ ] 남의 회의 · 줄 · 업무는 404

## Rollback

- **스키마**: 이 work 의 리비전이 있었으면 `alembic downgrade -1`. `source_*_line_id` 를 지우면 **`merged` 행의 참조가 사라지므로 `merged` 트랙 행을 먼저 지운다**(통합본은 파생물이라 원본 손실이 없다). `job` 은 이 work 의 소비자뿐이다
- **백엔드**: `job_router` · 회의 라우터의 이 work 갈래(`/end` · `/integrate` · `lines/{id}` · `.../task` · `agendas` `ended` 갈래)를 걷어내면 표면이 사라진다. **그 순간 회의를 끝낼 수 없다** — WORK-007 의 「회의 종료」가 실패 토스트가 된다(부분적으로 도는 상태가 없다). `task_service` 는 고치지 않았으므로 내 업무는 영향이 없다
- **프론트**: 브랜치 폐기. `detail/page.tsx` 분기에서 `generating` · `ended` 갈래를 빼면 그 상태의 회의는 「지원하지 않는 상태」 안내로 떨어진다(빈 화면 아님). `AgendaLineTree` 확장 prop 은 기본값이 `false` 라 되돌려도 WORK-007 렌더가 그대로다
- 부분 revert 시: **Phase 5(업무 연동)만** 되돌려도 통합본 · 편집은 돈다(줄 버튼이 비활성으로 남는다). **Phase 1 은 단독으로 되돌리지 않는다** — Phase 2~6 전부가 `ended` 를 전제한다. Phase 6 만 되돌리면 캘린더의 회의 블록 클릭이 빈 자리로 돌아간다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-008 §6 Acceptance 25개 항목이 전부 확인**됐다.
- [ ] **완료 게이트 우회 0건** — Phase 5 의 정적 검사 3종 + 「업무 갱신」 요청 하나 실측 캡처가 완료 증거에 있다(WORK-005 L294).
- [ ] **통합 규칙 구조 검증의 실패 케이스 5종**(사람 줄 누락 · 이중 계승 · AI 중복 참조 · 참조 없음 · `headline` 누락/초과)이 테스트로 고정돼 있고, 모델 본문을 읽는 코드가 0건이라는 grep 결과가 있다.
- [ ] 줄 삭제가 원본 · AI · 트랜스크립트 · 녹음 · 업무를 건드리지 않는다는 DB 전후 비교가 완료 증거에 있다.
- [ ] 정적 검사(트랙 판정 단일 · 상단 바 슬롯 단일 · 트리 컴포넌트 단일 · 본문 껍데기 둘 · 드로어 폭 리터럴 격리 · 실패 상태 내부 state 0) 결과가 붙어 있다.
- [ ] WORK-007 회의 중 화면의 트리 렌더 **회귀 없음**이 확인됐다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- ~~재개가 되지 않는 회의를 닫을 길이 없다(S008-OQ-3)~~ → **닫힘(2026-09-06 코디 정정)**. `/end` 는 `paused/stream` 에서도 받는다(BE §8-2 L243 · SPEC-007 U-1 L113). Phase 1 의 사전 조건이 그 규칙이다
- **`MeetingDetail` 키 이름은 `agendas.{human,ai,merged}` · `latestBatchSeq` 다**(SPEC-006 정본 · 2026-09-06 정정 완료). **자식 쓰기 응답은 `MeetingDetail` 전체, 삭제만 204** — `LineItem` 부분 응답을 만들지 않는다
- **안건 `next` 배지 문구는 상태별로 갈린다** — 회의 중 「대기」 · 종료 후 「**다음 논의로**」(DEC-003 §1 표 L45). `AgendaLineTree` 는 WORK-007 것이라 라벨 매핑도 거기 있다 — 이 work 가 **종료 후 매핑 값 「다음 논의로」를 그 한 곳에 더한다**(회의 상태로 갈린다)
- **`job` 테이블 · `source_*_line_id` 의 리비전 소유가 WORK-006 인지 이 work 인지** Phase 1 첫 작업에서 확인한다. 두 work 가 같은 컬럼을 두 번 만들지 않게 코디가 WORK-006 문서에 적어 두면 좋다
- **통합 규칙의 모델 프롬프트 품질**은 이 work 의 계약이 아니다 — 구조 검증이 잘못된 짝짓기를 막지는 않는다(사람 줄과 무관한 AI 줄을 짝지어도 「근거」만 틀리게 붙는다). 실측 후 프롬프트를 다듬는 것은 계약 밖이고, 검증 규칙(구조)은 불변이다
- **한 줄 요약의 언어 · 어조**는 정하지 않았다(`headline` 1~200자 한 문장만). 실측에서 어색하면 프롬프트 몫이다
- **수치 4개(300 · 180 · 3 · 900)는 실측 전 값**이다(SPEC-008 §4). 계약(단계 · 재시도 2회 · 상한 존재)은 불변이고 값만 `config.py` 에서 조정한다

## Related

- SPEC: SPEC-008 (frontmatter `links.specs`) · 물려받는 계약 SPEC-003 · SPEC-004 · SPEC-006 · SPEC-007 · 소비자 SPEC-009
- Work: WORK-004 · WORK-005 · WORK-006 · WORK-007 (선행) · 캘린더 그룹 (드로어 소비)
