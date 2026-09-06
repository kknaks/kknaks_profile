---
type: work
id: WORK-006
title: "회의록 — 도메인 · 목록 · 생성 드로어 · 시작 전 · 첨부 · 삭제"
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
  specs: [SPEC-006]
  works: [WORK-003, WORK-004]
  releases: []
  related: [DEC-001, DEC-004, DEC-005, SPEC-007, SPEC-008, SPEC-009]
---

# 회의록 — 도메인 · 목록 · 생성 드로어 · 시작 전 · 첨부 · 삭제

**회의록을 만들고, 안건과 첨부를 미리 두고, 「회의 시작」을 누르는 데까지.** 회의 중(STT·배치)과 종료 후(통합·편집)는 만들지 않는다 — WORK-007·008 이다. 이 work 는 그 둘이 **읽고 쓸 회의록 하나**(도메인 스키마 · `MeetingDetail` · 상태 전이 진입점 · 첨부 계약)를 세운다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003
- Covers spec: **SPEC-006**(회의록 — 목록 · 생성 · 시작 전 · 첨부 · 삭제)
- Depends on work: **WORK-003**(동적 유형 — `kind='meeting'` 유형 목록 · 팔레트 · `TypeBadge` · **U-7 자동 저장 실패 규격**) · **WORK-004**(`schedule_service`(겹침 검사 + 파생 — **두 번째 구현을 만들지 않는다**, `work-004` L155 · Rollback 절이 이미 이 work 를 지목했다) · `DrawerFrame` · `Selector`(**하단 「+ 새 프로젝트」 인라인 행 포함** — 규격의 정본은 SPEC-006 U-3) · 첨부 팝오버(SPEC-003 U-7) · `AttachmentList` · `EmptyState` · `InlineEditText` · `ConfirmModal`) · **WORK-005**(`PeriodStepper` · `TaskContextMenu` 의 팝오버 220 프레임 · 삭제 모달 문안 패턴) · **아키텍처 반영분**(ERD 5건 — SPEC-006 §7 「ERD 변경 필요」 + SPEC-007 §7-C 3건. **별도 워커가 같은 시각에 `database/` 에 반영 중** — 착수 시점에 `domains/meeting.md` 가 그 판이어야 한다)
- Parallel work: 없음 — WORK-007 은 이 work 의 `/start` · `MeetingDetail` · 안건 표면 위에 얹힌다
- Follow-up work: **WORK-007**(회의 중 — WS 스트림 · 줄 표면 · AI 배치) · **WORK-008**(종료 · 통합 · `ai_headline` · 편집 · 회의 상세 드로어 · 업무 연동) · 캘린더 그룹(`POST /api/meetings` · `PATCH` · 생성 드로어를 재사용한다) · 문서함 그룹(첨부의 「자료함 문서」 갈래와 파일 드로어 본문을 실체화한다)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다
  - **문서함(`document`·`folder`)이 아직 없다**(WORK-004 와 같은 사정). 첨부의 「자료함 문서」 갈래와 파일 드로어의 md 본문은 이 work 에서 **스텁**이다(§Scope 제외 · §Open Issues). **URL 링크 갈래는 실동작**한다
  - Redis · codex · Soniox 는 **이 work 에 없다** — `/start` 는 상태 전이만이라(SPEC-006 §4) 외부 호출이 없다. WORK-007 에서 합류한다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR | `kknaksss/docs-v1` — a7e1bd4 · 2d6319e · 618d5bb |
| Blocker | WORK-004 미완 · ERD 5건 반영 대기(`domains/meeting.md`) |
| Next | Phase 1 — 회의 도메인 마이그레이션 · `schedule_service.sync_from_meeting` 연결 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-006 §6 Acceptance **22개** 대조 · 문서함 스텁 범위 승인 | todo |
| Design |  | 시안 `회의록.dc.html` L24~760 대조 · 시안 없는 조립분(삭제 모달 · 상태 표기 · 안건 목록 · 요약 바 축소판 · 반응형) 확인 | todo |
| FE |  | 목록 2패널 · 새 회의록 드로어(셀렉터 인라인 행 재사용) · 시작 전 화면 · 첨부 탭/파일 드로어 · 삭제 모달 · 상세 라우트 상태 분기 골격 | todo |
| BE |  | 회의 도메인 마이그레이션 · 본체·안건·첨부 API · `/start` · 목록 집계 · `MeetingDetail` 빌더 · `schedule_service` 소비 | todo |
| QA |  | Phase 검증(앱 창 E2E) · 겹침 검사 단일 구현 실측 · 계층·금지목록 정적 검사 | todo |
| Ops |  | 해당 없음(신규 env 없음 — `STORAGE_ROOT` 는 WORK-007 이 처음 쓴다) | todo |

## Scope

포함:

- **회의 도메인 마이그레이션** — `meeting` · `meeting_agenda` · `meeting_line` · `meeting_transcript` · `meeting_attachment`(`kind`·`url`·`label` 포함) · `meeting_batch_run`. **한 리비전**으로 6 테이블(WORK-004 가 업무 6 테이블을 한 번에 세운 것과 같다). `job` 은 WORK-008
- **회의 본체 API** — 목록(월 범위 · 프로젝트 필터 · `projectCounts`) · 생성(안건·첨부 포함 **한 트랜잭션** + `schedule` 파생) · 상세(`MeetingDetail`) · 부분 수정(제목·유형·프로젝트·**일시 둘 함께** — 겹침 검사) · 소프트 딜리트 · **`POST /start`**(상태 전이 + `recording_started_at`)
- **자식 API** — 안건(추가 · 제목 수정 · 삭제, `track='human'`) · 첨부(`doc`/`link` 추가 · 제거). 쓰기 응답은 **`MeetingDetail` 전체**
- **`MeetingDetail` 빌더 한 곳** — SPEC-006 §4 필드 소유 표의 전 필드. WORK-007·008 이 채우는 필드(`ai`·`merged` 트리 · `headline` · `mergedSummary` · `latestBatchSeq` · `finalBatchState` · `activeJobId`)는 **자리와 파생 규칙만** 두고 값은 비어 있다(`[]` · `null` · `0`)
- **회의록 목록 페이지** — 헤더 + 월 스테퍼(`PeriodStepper` 재사용) + 「새 회의록」 · 좌 목록 500(필터 칩 · 행 · 정렬 · 빈 상태 · 스켈레톤 · 컨텍스트 메뉴) · 우 미리보기 패널(`scheduled` 본문 실동작 · `recording`/`generating`/`ended` 는 **자리 + 문구**, 트리 렌더는 WORK-008)
- **새 회의록 드로어**(840) — 제목 · 프로젝트/유형 셀렉터(**종류=미팅만**) · 일시 3칸 + 기본값 · 안건 인라인 행 · 첨부 영역(팝오버 + `V2Gate` 드롭 영역). **캘린더가 그대로 열 수 있게** 부모를 모르는 드로어
- **셀렉터 하단 「+ 새 프로젝트로 추가」 인라인 행** — WORK-004 가 만든 `Selector` 를 **SPEC-006 U-3 규격(정본)에 대조**해 맞춘다. 전 영역 공통
- **회의 시작 전 화면** — `/meetings/detail?id=` 의 `scheduled` 분기. 헤더 + `⋯`(삭제) + 「회의 시작」 · 회색 상태 바 「기록 대기」 · 좌 패널(회의록 탭 안건 목록 + 인라인 편집 + 안건 입력 바 / AI 요약 탭 빈 상태) · 우 패널(스크립트 탭 빈 상태 / 첨부 탭)
- **상세 라우트의 상태 분기 골격** — `scheduled` → 이 work 화면, 나머지 셋 → **플레이스홀더**(WORK-007·008 이 교체). 상단 바 슬롯(`top 150 · 1640×56`)은 이 work 가 만들고 `waiting` 변형(회색 「기록 대기」)과 `headline` 변형(AI 한 줄 요약 바 — **U-8 미리보기 패널이 쓴다**)을 넣는다
- **첨부 파일 탭 · 파일 드로어**(840, 미리보기/원문 텍스트 탭) — 시작 전·회의 중·종료 후가 **같은 컴포넌트**를 쓴다. 이 work 시점에는 문서 갈래가 스텁이라 **링크 행만 실동작**
- **회의록 삭제** — 컨텍스트 메뉴 · 헤더 `⋯` 두 진입점 + 확인 모달 600(경고 슬롯 「녹음 원본은 지워지지 않고 서버에 남습니다」) · `recording`·`generating` 비활성
- 회의록 영역 반응형(1280~1439 · ≥1440)

제외:

- **회의 중** — WS 스트림 · 마이크 · 실시간 스크립트 · 줄 표면(`POST …/lines`) · 안건 상태(`PATCH { state }`) · AI 배치 · 일시정지 → **WORK-007**. `/start` 뒤의 웜스타트·`ai_session_id` 도 WORK-007
- **종료 · 생성중 · 통합본 · `ai_headline` 생성 · 편집(줄 삭제 · 안건 이름 수정 포함) · 근거 칩 · 업무 연동 · 회의 상세 드로어(SPEC-008 U-4)** → **WORK-008**. 이 work 는 미리보기 패널의 `ended` 자리에 **「통합본 트리는 WORK-008」 플레이스홀더**만 둔다
- **캘린더 화면·드래그** → 캘린더 그룹. 이 work 는 `PATCH /api/meetings/{id}` 가 겹침 검사를 지나 `schedule` 을 파생한다는 사실만 세운다
- **첨부의 「자료함 문서」 실동작 · 파일 드로어의 md 본문 렌더 · 「자료함에서 열기」 이동** → 문서함 work(WORK-004 Open Issues 와 같은 임시 계약)
- 로컬 파일 업로드 — **v2 게이트**(UI 만). 서버 표면 없음
- 반복 회의 · 예약 알림 · 회의 장소 · 회의록 검색 — v1 에 없다(DEC-003 §1 · SPEC-006 §1)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보 — 경로는 `backend/README.md` §4 · `frontend/README.md` §2 의 트리를 따른다

| 경로 후보 | 설명 |
|---|---|
| `app/back/models/meeting.py` | `meeting` · `meeting_agenda` · `meeting_line` · `meeting_transcript` · `meeting_attachment` · `meeting_batch_run` — ERD `domains/meeting.md`(반영분 포함) 그대로 |
| `app/back/alembic/versions/*_meeting_domain.py` | 리비전 1건. `autogenerate` 초안을 읽고 CHECK(`status` 4종 · `track` 3종 · `kind` 4종 · **첨부 `kind` CHECK — `doc` 이면 `document_id` 만 / `link` 면 `url`·`label` 만**) · 부분 인덱스(`(account_id, start_at) WHERE deleted_at IS NULL` · `(account_id, status) WHERE deleted_at IS NULL`) · `UNIQUE (meeting_id, document_id) WHERE document_id IS NOT NULL` 을 손으로 넣는다 |
| `app/back/core/enums.py` | `MeetingStatus` · `IntegrationState` · `MeetingTrack` · `LineKind` · `AgendaState` · `MeetingAttachmentKind` `StrEnum` — 값의 단일 출처(G-3·G-4) |
| `app/back/core/exceptions.py` | `InvalidMeetingStatusError`(409 `invalid_meeting_status`) 추가. **`meeting_not_recording` 은 만들지 않는다**(SPEC-006 §7 정합 #3) |
| `app/back/repository/meeting_repository.py` | 본체 조회(기본 `deleted_at IS NULL`) · 월 범위 목록 + `projectCounts` 집계 · dto 반환 |
| `app/back/repository/meeting_child_repository.py` | 안건 · 첨부 · (읽기만) 줄 · 배치 run 최대 `seq` |
| `app/back/service/meeting_service.py` | 생성 트랜잭션(유형 `kind=meeting` 검증 → `schedule_service.check_overlap` → INSERT + 안건·첨부 + `schedule_service.sync_from_meeting`) · 상세 · 부분 수정 · **`start()`** · `soft_delete()` · 안건·첨부 조작 · **상태별 허용 표 판정** · 소유 검사 |
| `app/back/service/meeting_detail_builder.py`(또는 `meeting_service` 내부 함수 하나) | **`MeetingDetail` 을 만드는 유일한 곳** — 트랙별 트리 조립 · 파생값(`durationMinutes` · `latestBatchSeq` · `mergedSummary` · `finalBatchState` · `activeJobId`) |
| `app/back/api/meeting_router.py` | SPEC-006 §4 의 11 표면. 라우터 단위 `require_account`. `/end` · `/lines` · `/stream` · `/transcript` 는 **여기 자리만 비워 둔다**(WORK-007·008 이 같은 라우터에 더한다) |
| `app/back/schemas/meeting.py` · `dto/meeting.py` | FE 계약(camelCase alias) / 내부 dto. **`MeetingUpdateDTO` 에 `status` 없음**, `PATCH` 필드는 `T \| Unset`, 일시는 `startAt`·`endAt` 둘 함께 |
| `app/back/tests/test_meeting.py` · `test_meeting_children.py` · `test_meeting_schedule.py` | §Execution 의 검증 항목 |
| `app/front/src/app/(app)/meetings/page.tsx` · `layout.tsx` | 목록 페이지 — breadcrumb · 타이틀 + `PeriodStepper` + 「새 회의록」 · 2패널 |
| `app/front/src/app/(app)/meetings/detail/page.tsx` | `?id=` 상세 라우트 — **`status` 로 화면을 고르는 스위치**(FE §1 L47) |
| `app/front/src/features/meetings/api.ts` · `types.ts` · `hooks/useMeetingsQuery.ts` · `useMeetingDetail.ts` · `useMeetingMutations.ts` | 목록·상세 쿼리 · 생성/수정/삭제/시작/안건/첨부 뮤테이션 · 무효화(FE §3-3 표 — 일시가 바뀌면 `['schedules']`) |
| `app/front/src/features/meetings/components/MeetingListPanel.tsx` · `MeetingRow.tsx` · `MeetingProjectChips.tsx` · `MeetingSortPopover.tsx` · `MeetingSkeleton.tsx` | 좌 패널 500 — SPEC-006 U-2 |
| `app/front/src/features/meetings/components/MeetingPreviewPanel.tsx` | 우 패널 — 헤더 · 탭 · 상태별 본문(U-8). `ended` 트리 자리는 WORK-008 이 채운다 |
| `app/front/src/features/meetings/components/MeetingCreateDrawer.tsx` | 새 회의록 드로어 — `DrawerFrame` 위. **부모를 모른다**(캘린더 재사용 · FE §6-2) |
| `app/front/src/features/meetings/components/MeetingScheduledPage.tsx` | 시작 전 화면(U-4) — 헤더 · 상단 바 · 좌/우 패널 |
| `app/front/src/features/meetings/components/MeetingTopBar.tsx` | **상단 바 슬롯 하나**(top 150 · 1640×56). 변형 `waiting`(회색) · `headline`(AI 한 줄 요약). `recording`·`paused`·`generating`·`failed` 변형은 WORK-007·008 이 **같은 컴포넌트에** 더한다 |
| `app/front/src/features/meetings/components/MeetingAgendaList.tsx` · `AgendaInputBar.tsx` | 시작 전 안건 목록(인라인 편집 · 제거) · 하단 입력 바(입력 + 「추가」). 안건 목록은 미리보기 패널 · SPEC-008 U-4 드로어(`scheduled`)도 재사용 |
| `app/front/src/features/meetings/components/MeetingAttachmentsTab.tsx` · `AttachmentFileDrawer.tsx` | 첨부 탭(라벨 n · 「추가」 · 빈 상태 · 목록 행 · `V2Gate` 푸터) · 파일 드로어 840(미리보기/원문 탭). **세 화면 공용** |
| `app/front/src/features/meetings/components/MeetingContextMenu.tsx` · `MeetingDeleteModal.tsx` | 우클릭 팝오버 220(WORK-005 `TaskContextMenu` 와 같은 프레임 — 항목만 다르다) · 삭제 모달 600(`ConfirmModal` 위) |
| `app/front/src/components/shared/Selector.tsx` | **수정** — 프로젝트 갈래 하단 인라인 행을 SPEC-006 U-3 규격(36px 행 → [색 트리거 28][이름][추가] · 즉시 선택 · 실패 인라인 · `Esc` 복귀)에 대조해 맞춘다 |
| `app/front/src/lib/api/queryKeys.ts` | `['meetings','list',{period,projectId,sort}]` · `['meetings','detail',id]` 등록(FE §3-3) |

- Domain / schema note: 이 work 가 **회의 도메인 6 테이블을 만든다.** `schedule` 은 WORK-004 가 만들었고 이 work 는 `source_type='meeting'` 행을 **`schedule_service` 를 통해서만** 만든다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | 본체. **일시(`start_at`/`end_at`)를 소유**(M-1). `status` 4종 · `integration_state` · `ai_headline`(WORK-008 이 채운다) · **`recording_started_at`**(이 work 의 `/start` 가 채운다) · `recording_path` · `ai_session_id`(WORK-007) · `deleted_at` |
| `meeting_agenda` | 안건 — `track` 3종 · `state`(NULL 허용, `active\|done\|next`) · `source_agenda_id`. 이 work 는 **`track='human'` 만** 만든다 |
| `meeting_line` | 줄 — 이 work 는 **읽기만**(상세 응답 조립). 쓰기는 WORK-007·008 |
| `meeting_transcript` · `meeting_batch_run` | 이 work 는 테이블만 세우고 **행을 만들지 않는다**. `latestBatchSeq` 파생이 `meeting_batch_run` 을 읽는다(비어 있으면 0) |
| `meeting_attachment` | 첨부 — **`kind`(`doc`\|`link`) · `document_id`(NULL 허용) · `url` · `label`**(ERD 반영분). 문서함 전까지 `document_id` 에 **FK 를 걸지 않는다**(WORK-004 와 같은 임시 계약) |
| `schedule` | **쓰지 않는다** — `schedule_service.sync_from_meeting()` 이 같은 트랜잭션에서 만든다(SCH-1) |

- 상태 / invariant: `domains/meeting.md` **M-1**(일시 소유 · NOT NULL) · **M-2**(`kind='meeting'` 유형만) · **M-3**(상태 4종) · **M-5**(줄은 안건에 속한다 — 시작 전 안건 삭제는 줄이 없을 때만 성립) · **M-5-a**(안건도 트랙별) · **M-13**(녹음 원본 영구 보관 — 소프트 딜리트가 파일을 건드리지 않는다) · **M-17**(첨부 갈래 — ERD 반영분으로 「md 문서 · URL 링크」) · **M-18**(300분 상한) · `database/README.md` §0-1(소프트 딜리트 · 자식은 하드) · §3(`schedule` 파생)
- Migration 필요 여부: **있음** — 회의 도메인 리비전 1건. **ERD 5건(SPEC-006 §7) + SPEC-007 §7-C 3건이 `domains/meeting.md` 에 반영된 판을 기준으로** 만든다. 반영 전이면 착수하지 않는다(§Open Issues)
- SPEC 에 환류해야 하는 변경: **`invalid_meeting_status` 가 `backend/README.md` §8-2 표에 없다**(SPEC-006 §7). 구현은 SPEC-006 §4 를 따르고 표 갱신은 코디 소관. **`meeting_not_recording` 을 만들지 않는 것**도 그 표에 적혀야 한다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-007** | `POST /api/meetings/{id}/start` 뒤의 `status='recording'` + `recording_started_at` · `MeetingDetail` 빌더 · `POST …/agendas { title }`(회의 중 「새 안건」이 같은 표면) · `PATCH …/agendas/{id}`(`state` 필드를 **더한다** — 이 work 는 `title` 만) · 상세 라우트의 `recording` 분기 슬롯 · `MeetingTopBar` 의 변형 슬롯 · 첨부 탭/파일 드로어 컴포넌트 | WORK-007 은 라우터·빌더·스위치에 **더하기만** 한다. 새 라우터·새 빌더를 만들지 않는다 |
| **WORK-008** | `MeetingDetail` 빌더의 `merged` 트리 · `headline` · `mergedSummary` · `finalBatchState` · `activeJobId` 자리 · `PATCH /api/meetings/{id}`(상세 드로어 U-4 가 쓴다) · `DELETE`(전체 페이지 「삭제」 → 같은 모달) · `PATCH …/agendas/{id} { title }` 의 **`ended` 허용**(상태별 허용 표) · `MeetingTopBar` `headline` 변형 · `MeetingAgendaList`(드로어의 `scheduled` 본문) · 상세 라우트의 `generating`/`ended` 분기 슬롯 | `ai_headline` 을 **쓰는** 곳은 WORK-008 의 통합 트랜잭션 하나다. 이 work 는 읽어서 그릴 뿐이다 |
| 캘린더 그룹 | `POST /api/meetings`(드로어 재사용) · `PATCH /api/meetings/{id} { startAt, endAt }`(드래그) · `invalid_meeting_status` · `schedule` 의 `source_type='meeting'` 행 | 캘린더는 **화면과 `GET /api/schedules` 만** 만든다(WORK-004 Open Issues 와 같은 경계) |
| 문서함 그룹 | `meeting_attachment.document_id` FK 리비전 · `kind='doc'` 실동작 · 파일 드로어 본문(`GET /api/documents/{id}/content`) · 「자료함에서 열기」 | 이 work 의 스텁 셋을 실체화한다(§Open Issues) |
| WORK-004 | `schedule_service.check_overlap()` · `sync_from_meeting()` · `DrawerFrame` · `Selector` · 첨부 팝오버 | 이 work 가 소비한다. **`Selector` 인라인 행은 SPEC-006 U-3 규격에 맞춰 이 work 가 손본다**(소유는 `components/shared/`) |

## Internal Interface Contract

외부 계약(엔드포인트·요청/응답·검증·에러)은 **SPEC-006 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`MeetingDetail` 빌더는 하나다** | `meeting_service` 의 **함수 하나**(`build_detail(meeting_id)`)가 상세·생성·`PATCH`·`/start`·안건·첨부 응답을 **전부** 만든다. WORK-007·008 은 **이 함수에 필드를 더한다** — 표면마다 다른 조립을 두지 않는다(SPEC-006 §5 · WORK-004 F-4 교훈). 삭제만 `204` |
| **상태별 허용 판정은 한 곳** | `meeting_service._assert_allowed(meeting, action)` 이 SPEC-006 §4 상태별 허용 표를 **표 그대로** 갖는다(`action` ∈ `start` · `patch_meta` · `patch_time` · `agenda_add` · `agenda_title` · `agenda_state` · `agenda_delete` · `attachment` · `delete`). 어기면 `InvalidMeetingStatusError`(409). WORK-007·008 은 자기 `action`(`line_write` · `end` · `integrate` …)을 **같은 표에 행으로 더한다** — 판정 코드를 둘로 두지 않는다 |
| **겹침 검사 · `schedule` 파생** | `schedule_service.check_overlap()` → 원본 쓰기 → `schedule_service.sync_from_meeting()` 순서, **같은 트랜잭션**(BE §7). **`schedule` 을 INSERT/UPDATE/DELETE 하는 코드는 이 work 에 0건**이다(SCH-1 · WORK-004 L155 「두 번째 구현을 만들지 않는다」). 회의는 항상 시간 일정(`is_all_day=false`)이라 생성·일시 변경 **모두** 검사를 지난다 |
| `/start` | `status` 를 `recording` 으로, `recording_started_at` 을 `now()` 로 — **한 UPDATE**. 외부 호출 없음. `start_at` 을 덮어쓰지 않는다. 응답은 `build_detail` |
| 상태 대입 격리 | `meeting.status` 에 값을 대입하는 코드는 `meeting_service` 의 **전이 함수 안에만** 있다(이 work 는 `start()` 하나). `MeetingUpdateDTO` 에 `status` 가 **없어** 일반 `PATCH` 로 상태를 보내면 스키마 층에서 422 |
| 목록 집계 | `projectCounts` 는 **프로젝트 필터를 적용하기 전** 그 달 전체 · `total` 은 **적용 후**(SPEC-006 §4). `projectId=none` 이 무소속. 삭제된 프로젝트의 회의도 그 프로젝트 이름·색으로 집계에 남는다 |
| 파생값 | `durationMinutes` · `latestBatchSeq` · `mergedSummary` · `finalBatchState` · `activeJobId` · `agendaTitles` · `attachmentCount` 는 **서버가 계산**한다(G-7). 이 work 시점의 값은 `durationMinutes`·`agendaTitles`·`attachmentCount` 만 의미가 있고 나머지는 `0`·`null` — **컬럼으로 두지 않는다** |
| 안건 표면 공유 | `POST …/agendas { title }` 는 `track='human'` · `orderIndex` = 사람 트랙 마지막 + 1 · `state=null`. `PATCH …/agendas/{id}` 는 **보낸 필드만**(이 work `title`, WORK-007 이 `state` 를 더한다). `DELETE …/agendas/{id}` 는 사람 트랙 + 딸린 줄 0건일 때만(시작 전엔 항상 참) |
| 첨부 | `kind` 별 CHECK(DB) + 서비스 검증(`doc` 는 본인 md 문서 · `link` 는 `http/https`). **같은 `document_id` 재첨부는 행을 늘리지 않고 201**. **문서함 전까지 `kind='doc'` 은 서비스가 거부**(임시 계약 — §Open Issues). 첨부 계약은 SPEC-007·008 이 **그대로 승계**한다 |
| 상세 라우트 스위치 | `meetings/detail/page.tsx` 가 `useMeetingDetail(id)` 의 `status` 로 **화면 컴포넌트 하나를 고른다**. `scheduled` → `MeetingScheduledPage`. `recording`/`generating`/`ended` 는 **플레이스홀더 컴포넌트**(문구 「이 화면은 WORK-007/008 에서 만든다」)이고 WORK-007·008 이 **같은 스위치의 그 분기만** 교체한다. `/start` 성공 후 페이지 이동 없이 스위치가 바뀐다 |
| `MeetingTopBar` | 상단 바 슬롯 하나(top 150 · 본문 폭 · 56). `variant` 로 갈린다 — 이 work: `waiting`(회색 `#F4F5F7` · dot `#B3B3B3` · 「기록 대기 00:00:00」 · 캡션) · `headline`([09] L727~733 — 배지 + 문장 말줄임 + 「안건 n · 결정 n · 액션 n」). WORK-007·008 이 `recording` · `paused` · `generating` · `failed` 를 **같은 파일에** 더한다. **바를 두 개 그리지 않는다** |
| `MeetingAgendaList` · `AgendaInputBar` | 시작 전 안건 목록 — `InlineEditText`(WORK-003) 로 제목 인라인 편집, 실패 상태는 **`saveFailed`·`onRetry` prop**(SPEC-002 U-7 구현 규약 · 소유자는 목록). 입력 바는 `Enter` + 「추가」 병행. **부모를 모른다** — 미리보기 패널(읽기 전용 모드) · SPEC-008 U-4 드로어가 재사용 |
| 첨부 탭 · 파일 드로어 | `MeetingAttachmentsTab`(라벨 n · 「추가」 → WORK-004 첨부 팝오버 · 목록 행 → `AttachmentList` 재사용 · `V2Gate` 푸터) · `AttachmentFileDrawer`(`DrawerFrame` 위, 미리보기/원문 탭). **세 화면(시작 전 · 회의 중 · 종료 후)이 이 두 컴포넌트를 그대로 쓴다** — 화면별 조건은 prop 으로 |
| 삭제 모달 | `MeetingDeleteModal` = `ConfirmModal` + 문안 3줄(SPEC-006 U-5). 진입점은 컨텍스트 메뉴 · 헤더 `⋯`. WORK-007·008 의 헤더 삭제 버튼도 **이 모달을 연다**. 드로어가 열려 있으면 **먼저 닫는다**(FE §6-2) |
| 캐시 키·무효화 | `['meetings','list',{period,projectId,sort}]` · `['meetings','detail',id]`. 생성·수정·삭제·시작 → `['meetings']` 전부 + **일시가 바뀌었으면 `['schedules']`**(FE §3-3). 미리보기 패널과 상세 페이지가 **같은 detail 키**를 본다 |
| 낙관적 갱신 | **안건 제목 인라인 편집만.** 안건 추가·삭제 · 일시·유형·프로젝트 · 첨부 · 「회의 시작」은 하지 않는다(SPEC-006 §5 표 · FE §3-4) |
| 드로어 | `MeetingCreateDrawer` 는 **부모를 모른다** — `openDrawer` 로 열리고 `onCreated(detail)` 콜백만 낸다. 캘린더가 같은 방식으로 연다. 폭·스크림은 `DrawerFrame` 이 정한다(폭 prop 없음) |

## Execution

### Phase 1 — 회의 도메인 마이그레이션 · `schedule_service` 연결

- **Status**: TODO
- **설명**: 화면도 API 도 없이 **스키마와 시간 규칙이 회의에도 도는 상태**를 만든다. `schedule_service` 는 WORK-004 것 하나뿐이고 여기서는 `sync_from_meeting` 갈래를 **호출**만 한다 — 두 번째 겹침 검사·파생 구현이 생기면 이 Phase 에서 잡는다.
- **작업**:
  - [ ] **선행 확인** — `40-architecture/database/domains/meeting.md` 에 ERD 반영분(첨부 `kind`·`url`·`label` · `document_id` NULL · 첨부 UNIQUE · `agenda.state` NULL · `(account_id,start_at)` 인덱스 · `recording_started_at` · `agenda.state` `active` · `source_agenda_id`)이 들어 있는지 대조. 없으면 **착수하지 않고 코디에 알린다**
  - [ ] `core/enums.py` — `MeetingStatus`(`scheduled`·`recording`·`generating`·`ended`) · `IntegrationState` · `MeetingTrack` · `LineKind` · `AgendaState` · `MeetingAttachmentKind`. **한국어 라벨을 저장하지 않는다**(G-4)
  - [ ] `models/meeting.py` — 6 테이블. `meeting` 은 `start_at`·`end_at` NOT NULL, `meeting_line.agenda_id` NOT NULL, `meeting_attachment` **kind CHECK**(`doc` 이면 `document_id` 만 / `link` 면 `url`·`label` 만) + 부분 UNIQUE. `document_id` 에 **FK 없음**(임시 계약)
  - [ ] 리비전 1건 + `downgrade`. 인덱스는 `database/README.md` §4 + 반영분
  - [ ] `repository/schedule_repository.py`·`service/schedule_service.py` — **수정하지 않는다.** `sync_from_meeting(meeting_dto)` 가 이미 있으면 그대로, 없으면 **그 파일 안에** `sync_from_task` 와 같은 모양으로 더한다(다른 파일에 만들지 않는다)
  - [ ] `tests/test_meeting_schedule.py` — 회의 생성·일시 변경·삭제 시 `schedule` 파생 · 업무↔회의 겹침 · 경계 접촉 통과 · 고아 없음(BE §12 필수 **3·5·9** 의 회의 쪽)
- **검증**:
  - [ ] `make migrate` 가 빈 DB 에서 끝나고 `alembic downgrade -1 → upgrade head` 왕복이 된다. **WORK-004 까지의 데이터에 영향이 없다**
  - [ ] `kind='doc'` 인데 `url` 이 있는 첨부 행 · `kind='link'` 인데 `document_id` 가 있는 행이 **DB CHECK 로 거부**된다
  - [ ] 같은 회의에 같은 `document_id` 를 두 번 넣으면 **UNIQUE 로 거부**된다
  - [ ] `agenda_id` 없는 `meeting_line` 이 **NOT NULL 로 거부**된다(M-5)
  - [ ] **정적 검사**: `schedule` 을 INSERT/UPDATE/DELETE 하는 코드가 **`schedule_service.py` 밖에 0건**이고, 겹침 판정식(`start_at < :end AND end_at > :start`)이 **그 파일에만** 있다(grep 결과를 완료 증거에 — WORK-004 L155)
  - [ ] `pytest` 통과 — 14:00–15:00 업무가 있을 때 같은 시각 회의가 막히고, 15:00–16:00 은 통과하고, 회의를 지우면 `schedule` 조회에서 빠진다(행은 남는다 — §3-3)
- **완료 증거**: 미작성

### Phase 2 — 회의 본체 API · `/start` · `MeetingDetail` 빌더

- **Status**: TODO
- **설명**: `curl` 로 **회의록을 만들고 읽고 고치고 시작하는** 왕복을 닫는다. `MeetingDetail` 을 **한 함수**가 만드는 것과 상태별 허용 판정이 **한 곳**에 있는 것이 이 Phase 의 핵심이다 — WORK-007·008 이 여기에 더하기만 하게 된다.
- **작업**:
  - [ ] `repository/meeting_repository.py` — 기본 조회 `deleted_at IS NULL` · 월 범위(`from`·`to` UTC, `start_at` 기준) · `projectId`(숫자/`none`) · 정렬 2종 · `projectCounts`(필터 전) · `total`(필터 후) · **dto 만 반환**
  - [ ] `service/meeting_service.py` — 생성(유형 `kind='meeting'`·미삭제 검증 → 프로젝트 검증 → 길이 5~300분 → `check_overlap` → INSERT + 안건·첨부 + `sync_from_meeting`, **같은 트랜잭션**) · 부분 수정(`T | Unset`, 일시는 둘 함께) · `soft_delete()`(파일 안 건드림) · **`start()`**(`status` + `recording_started_at` 한 UPDATE)
  - [ ] **`_assert_allowed(meeting, action)`** — SPEC-006 §4 상태별 허용 표 그대로. `InvalidMeetingStatusError`(409)
  - [ ] **`build_detail()` 하나** — 트랙별 트리(`human`·`ai`·`merged`, 줄은 안건 안) · 첨부 · 파생값 전부. `ai`·`merged` 는 항상 `[]` 키
  - [ ] `api/meeting_router.py` — `GET /api/meetings` · `POST` · `GET /{id}` · `PATCH /{id}` · `DELETE /{id}` · `POST /{id}/start`. 라우터 단위 `require_account`
  - [ ] `schemas/meeting.py`·`dto/meeting.py` — camelCase alias · `response_model_by_alias=True` · **`MeetingUpdateDTO` 에 `status` 없음**
  - [ ] `core/exceptions.py` — `InvalidMeetingStatusError`(409 `invalid_meeting_status`). `persist_changes` 는 켜지 않는다
  - [ ] `tests/test_meeting.py`
- **검증**:
  - [ ] `curl` 로 **제목 + 유형 + 일시**만 넣어 회의록이 만들어지고 상세에 `status: "scheduled"` · `recordingStartedAt: null` · `agendas.ai: []` · `agendas.merged: []` · `latestBatchSeq: 0` · `headline: null` 이 있다
  - [ ] 종류가 `task` 인 유형을 주면 **422 `invalid_work_type`**, 삭제된 프로젝트를 주면 **422 `invalid_project`**
  - [ ] 301분짜리 · 4분짜리 · `endAt ≤ startAt` · `startAt` 만 보낸 요청이 **422 `validation_error`**
  - [ ] 14:00–15:00 업무가 있는 시각으로 만들면 **409 `schedule_overlap`** 이고 **`meeting` 행이 생기지 않는다**(DB 로 확인). 15:00–16:00 은 만들어진다
  - [ ] 안건 2건 + 첨부(`link`) 1건을 함께 보낸 생성이 **전부 저장**되고, 그중 하나를 잘못 주면(`ftp://`) **본체도 만들어지지 않는다**
  - [ ] `PATCH { startAt, endAt }` 뒤 `schedule` 행이 **새 시각으로 바뀌어 있다**. `PATCH { title }` 은 `schedule` 을 건드리지 않는다
  - [ ] `PATCH { status: "recording" }` 은 **422 `validation_error`**(스키마 층)
  - [ ] `POST /start` → **200, `status: "recording"`, `recordingStartedAt` 이 채워진다.** 다시 부르면 **409 `invalid_meeting_status`**. `recording` 에서 `PATCH { title }` · `DELETE` 도 **409**
  - [ ] `DELETE` 후 목록·상세에서 빠지고 **DB 에 행·자식이 남는다**. `recording_path` 가 있는 행을 지워도 파일 삭제 호출이 **없다**(스토리지 어댑터 호출 0건)
  - [ ] 목록: `projectId=none` 이 무소속만 주고, `projectCounts` 는 **필터를 걸어도 같은 값**이며 `total` 은 바뀐다
  - [ ] 남의 회의 id 로 조회하면 **404 `not_found`**
  - [ ] **정적 검사**: `meeting.status` 에 값을 대입하는 코드가 **`meeting_service.start()` 안에만** 있고, `MeetingDetail` 을 조립하는 함수가 **1개**이며, `service/` 에서 `fastapi`·`schemas` import **0건**(grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — 안건 · 첨부 API

- **Status**: TODO
- **설명**: 시작 전 화면이 조작할 자식 표면을 연다. **안건 표면을 WORK-007(회의 중 「새 안건」·`state`)과 WORK-008(종료 후 제목 수정)이 그대로 쓴다** — 여기서 상태별 허용을 표대로 못박지 않으면 두 work 가 각자 조건을 단다.
- **작업**:
  - [ ] 안건 — `POST …/agendas { title }`(사람 트랙 · `orderIndex` · `state=null`) · `PATCH …/agendas/{id} { title }`(보낸 필드만 — `state` 필드는 **받지 않되 dto 에 자리를 비워 둔다**, WORK-007 이 채운다) · `DELETE …/agendas/{id}`(사람 트랙 · 딸린 줄 0건)
  - [ ] 첨부 — `POST …/attachments { kind, documentId | url, label }` · `DELETE …/attachments/{id}`. **`kind='doc'` 은 문서함 전까지 거부**(`validation_error` — WORK-004 와 같은 임시 계약). 같은 `documentId` 재첨부는 201 + 행 유지
  - [ ] 상태별 허용 — `agenda_add`(`scheduled`·`recording`) · `agenda_title`(`scheduled`·`ended`) · `agenda_delete`(`scheduled`) · `attachment`(`generating` 외 전부)
  - [ ] 응답 — **전부 `build_detail()`**, 삭제만 204, 없는 자식 404
  - [ ] `tests/test_meeting_children.py`
- **검증**:
  - [ ] 안건을 넣으면 응답이 **`MeetingDetail` 전체**이고 `agendas.human` 에 `orderIndex` 순으로 붙는다
  - [ ] 공백만인 제목 · 201자 제목이 **422**
  - [ ] `PATCH { title }` 뒤 상세에 반영되고 **`orderIndex` 는 그대로**다
  - [ ] `recording` 에서 `PATCH { title }` 은 **409**, `POST { title }` 은 **201**(회의 중 안건 추가는 허용) — 상태별 허용 표 그대로임을 표와 나란히 완료 증거에
  - [ ] 없는 안건을 지우면 **404**(멱등 아님)
  - [ ] `kind:"link"` 에 `ftp://` → **422**, `label` 101자 → **422**, `label` 비우면 응답 `name` 이 URL 이다
  - [ ] `kind:"doc"` 요청은 **이 시점에 422** 로 거부된다(§Open Issues 임시 계약)
  - [ ] 첨부를 지워도 **문서·링크 원본은 지워지지 않는다**(첨부 행만)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 4 — 목록 페이지 · 미리보기 패널 · 삭제 모달

- **Status**: TODO
- **설명**: **앱 창에서 회의록을 훑는** 단계. 「새 회의록」은 Phase 5 가 붙이므로 여기서는 시드 데이터로 목록·미리보기·삭제까지 돌린다.
- **작업**:
  - [ ] `features/meetings/api.ts`·`types.ts`·`hooks/*` — 목록·상세 쿼리 · 삭제 뮤테이션 · 캐시 키 등록
  - [ ] `meetings/page.tsx`·`layout.tsx` — breadcrumb · 타이틀 28/700 + **`PeriodStepper`(월 단위 · `?month=`)** + 「새 회의록」 34px · 2패널(좌 500 고정 / 우 유동)
  - [ ] `MeetingListPanel` — 헤더 48(「8월 회의록」 · 「n건」 · 정렬 트리거) · **프로젝트 필터 칩 행**(전체 · 미정 · 프로젝트별, 단일 선택, 가로 스크롤, 숫자는 `projectCounts`) · 행(일시 + **상태 표기** + 유형 배지 / 제목 / 셋째 줄 `headline` ?? 안건 제목 ?? 「안건 없음」) · 선택 행 `#F8FAFF`
  - [ ] `MeetingSortPopover`(최신순/오래된순, 즉시 반영) · `MeetingSkeleton`(6줄 · 애니메이션 없음) · 빈 상태 2종(`EmptyState` 재사용) · 조회 실패 표시 + 「다시 시도」
  - [ ] `MeetingContextMenu` 220 — 「열기」 / 구분선 / 「삭제」(`recording`·`generating` 비활성)
  - [ ] `MeetingDeleteModal` 600 — 문안 3줄(SPEC-006 U-5) · 삭제 후 다음 행 선택 · `['meetings']`+`['schedules']` 무효화
  - [ ] `MeetingPreviewPanel` — 헤더(제목 · 일시 범위 · 「상세보기」) · 탭 회의록/원문 · `scheduled` 본문(`MeetingAgendaList` 읽기 전용 + 첨부 행) · `recording`/`generating` 문구 · **`ended` 는 `MeetingTopBar variant="headline"` + 「통합본 트리 — WORK-008」 플레이스홀더**
  - [ ] `MeetingTopBar` — `waiting` · `headline` 두 변형(Phase 6 의 시작 전 화면과 공유)
- **검증**:
  - [ ] 회의록 메뉴로 들어가면 「‹ 2026년 9월 ›」와 **이번 달 목록**이 보이고 **가장 최근 행이 선택**된 채 우측에 그 회의가 보인다
  - [ ] `‹` 로 지난달에 가면 그 달만 보이고 **새로고침해도 그 달**이다(`?month=`)
  - [ ] 「미정 n」을 누르면 무소속만 남고 **칩 숫자는 바뀌지 않으며** 헤더 「n건」은 바뀐다
  - [ ] 시드로 `recording` · `generating` · `ended+failed` 행을 두면 각각 「기록 중」 dot · 「생성중」 · 「통합 실패」 가 붉게 보이고, `ended` 정상 행은 아무 표기가 없다
  - [ ] **시드로 `ai_headline` 을 채운 종료 회의를 고르면** 우측 본문 맨 위에 **「AI 한 줄 요약」 바 한 개**가 뜨고 그 문장이 **행 셋째 줄과 같다**. `ai_headline` 이 비어 있으면 바가 **없다**. 문단 요약 · 「· 회의실 A」 · 취소 행이 **없다**
  - [ ] 행 우클릭 → 「삭제」 → 모달에 「**v1 에는 복원 화면이 없습니다. 녹음 원본은 지워지지 않고 서버에 남습니다**」 → 삭제하면 행이 빠지고 **다음 행이 선택**된다. `recording` 행에서는 「삭제」가 **비활성**이다
  - [ ] 「상세보기」를 누르면 `/meetings/detail?id=` 로 가고, `scheduled` 가 아닌 회의는 **플레이스홀더 문구**가 보인다(WORK-007·008 전)
  - [ ] 첫 로딩에 **스켈레톤**, 달·필터 변경 시 **이전 결과 유지 + 진행 표시**. 서버를 내리면 **빈 목록이 아니라** 실패 표시 + 「다시 시도」(요청 1회 — 네트워크 탭)
  - [ ] 없는 회의록 주소로 들어가면 「**없는 회의록입니다**」 + 「목록으로」, 자동으로 튕기지 않는다
  - [ ] **정적 검사**: `Sheet`/`Dialog` 직접 import 0건 · 인라인 색 hex 0건 · `new Date()` 포맷 0건(FE 금지 목록 — grep 결과를 완료 증거에) · **상단 바 컴포넌트가 1개 파일**이다
- **완료 증거**: 미작성

### Phase 5 — 새 회의록 드로어 · 셀렉터 인라인 행

- **Status**: TODO
- **설명**: **앱 창에서 실제로 회의록을 만드는** 단계. 드로어가 부모를 모르게 만들어야 캘린더가 그대로 연다. 셀렉터 하단 「+ 새 프로젝트로 추가」는 WORK-004 가 먼저 만들었지만 **규격의 정본은 SPEC-006 U-3** 이므로 여기서 대조해 맞춘다.
- **작업**:
  - [ ] `hooks/useMeetingMutations.ts` — 생성 호출 · `['meetings']` + `['schedules']` 무효화
  - [ ] `MeetingCreateDrawer` — `DrawerFrame` 위. 헤더 72(제목 · 캡션 · ×) · 본문 5블록(제목 / 프로젝트·유형 2열 / 일시 3칸 / 안건 인라인 행 / 첨부 영역) · 푸터 80(취소 · 만들기)
  - [ ] 열자마자 **제목 포커스** · 제출 조건 **제목 + 유형 + 일시 셋 모두** · 제출 중 비활성 · 실패 시 인라인(SPEC-006 §4 Case Matrix), `schedule_overlap` 은 토스트 + 일시 실패 테두리
  - [ ] 유형 셀렉터 — **`kind='meeting'` 만** · 기본값 시드 「미팅·회의」 / 프로젝트 셀렉터 — 캡션 「목록에 없으면 셀렉터 맨 아래 '새 프로젝트로 추가'」
  - [ ] **`components/shared/Selector.tsx` 인라인 행 대조** — 36px 행 「+ 새 프로젝트로 추가」 → [색 트리거 28][이름][추가] · `Enter`/「추가」 → `POST /api/projects` → 즉시 선택 + 팝오버 닫힘 · 실패 인라인 + 입력 유지 · `Esc` 복귀. 어긋난 곳만 고친다(전 영역 공통 — 업무 드로어도 같이 바뀐다)
  - [ ] 일시 — 날짜 200 + 시작 130 – 종료 130 · **기본값**(오늘 · 현재 시각 30분 올림 · +1시간) · 30분 간격 목록 + 「직접 입력」 · 종료 ≤ 시작 인라인 문구
  - [ ] 안건 — 행 44(「안건 n」 · 입력 · 「제거」) · 마지막 빈 행 + **「추가」 버튼 병행** · 공백 행 미저장
  - [ ] 첨부 — 점선 영역(`V2Gate` — 드롭 시 「v2에서 제공됩니다」 토스트, 요청 없음) + 「자료함에서 선택」 → WORK-004 첨부 팝오버(문서 갈래 스텁 · 링크 갈래 실동작) · 목록 행(`AttachmentList`) · **드로어 안에서 파일 드로어를 열지 않는다**
  - [ ] **없는 것 확인** — 상태 필드 · 연관 업무 칸 · 「만들면 바로 회의 시작」 토글 · 유형 고정 칩
  - [ ] `onCreated(detail)` 콜백 → 목록에서 새 행 선택·하이라이트 + 미리보기 갱신
- **검증**:
  - [ ] 「새 회의록」로 드로어가 열리고 **제목에 커서**, 유형에 「미팅·회의」, 일시에 **오늘 다음 30분 경계부터 1시간**이 미리 들어 있다
  - [ ] 유형 셀렉터에 **종류=미팅인 유형만** 나온다(설정에서 업무 유형을 만들어 두고 확인). 「반복·개인」 칩이 없다
  - [ ] 프로젝트 셀렉터 맨 아래 「+ 새 프로젝트로 추가」로 그 자리에서 만들면 **즉시 선택**되고 **설정 화면 목록에도** 있다. 같은 이름을 다시 넣으면 행 아래 인라인 문구가 뜨고 입력이 남는다
  - [ ] 제목 + 유형 + 일시만으로 만들어지고 **목록에서 새 행이 선택·하이라이트**되며 드로어에 넣은 **안건·링크 첨부가 우측 미리보기에 그대로** 있다
  - [ ] 이미 시간 일정이 있는 시각으로 만들면 「그 시간에 다른 일정이 있습니다」 토스트 + 일시 칸 실패 테두리, **드로어가 닫히지 않고 입력이 남는다.** 끝시각 = 다른 일정 시작시각이면 만들어진다
  - [ ] 301분으로 맞추면 만들어지지 않고 일시 칸에 안내가 뜬다
  - [ ] 첨부 영역에 파일을 드롭하면 「**v2에서 제공됩니다**」 토스트만 뜨고 네트워크 탭에 요청이 **없다**
  - [ ] 「URL 링크」 두 건을 **연달아** 붙일 수 있다(팝오버 유지). 「자료함 문서」 세그먼트는 「자료함이 아직 없습니다」 안내
  - [ ] 드로어에 「만들면 바로 회의 시작」 토글·상태 필드·연관 업무 칸이 **없다**
  - [ ] **네트워크 탭 실측**: 생성이 **요청 하나**(`POST /api/meetings`)로 나가고 안건·첨부가 본문에 실려 있다(캡처를 완료 증거에)
  - [ ] **정적 검사**: `MeetingCreateDrawer` 가 라우터·부모 상태를 import 하지 않는다(콜백만 — grep) · 폭 리터럴 `840` 이 `DrawerFrame` 밖에 0건
- **완료 증거**: 미작성

### Phase 6 — 회의 시작 전 화면 · 첨부 탭 · 파일 드로어 · 반응형

- **Status**: TODO
- **설명**: 이 work 의 완성 지점 — **안건을 미리 두고 「회의 시작」을 누른다.** 상단 바 슬롯 · 안건 목록 · 첨부 탭 · 파일 드로어를 **WORK-007·008 이 그대로 쓰는 모양**으로 만든다. 여기서 화면 전용으로 만들면 다음 work 가 복제한다.
- **작업**:
  - [ ] `meetings/detail/page.tsx` — `status` 스위치(`scheduled` → `MeetingScheduledPage`, 나머지 플레이스홀더) · 로딩 스켈레톤 · 「없는 회의록입니다」(리다이렉트 금지)
  - [ ] `MeetingScheduledPage` — breadcrumb 「홈 › 회의록 › 시작 전」 · 헤더(제목 28/700 · 서브 「… 예정 · <유형> · <프로젝트>」 · `⋯`(「삭제」 → 모달) · 「회의 시작」) · **`MeetingTopBar variant="waiting"`** · 좌 1160 / 우 464 패널
  - [ ] 좌 패널 — 탭 「회의록」/「AI 요약」(dot `#B3B3B3`, AI 탭은 빈 상태 문구) · `MeetingAgendaList`(안건 없음 빈 상태 / 안건 있음 행 + `InlineEditText` + 「제거」) · `AgendaInputBar`(입력 + 「추가」 · 캡션 「시작 전에는 새 안건만 만들 수 있습니다」). **없는 것**: 「새 안건 ▾」 칩 · 추천 칩 · 전송 버튼 · 「회의 정보 수정」 · 「내 목소리 등록됨」 푸터
  - [ ] 우 패널 — 탭 「실시간 스크립트」(빈 상태) / 「첨부 파일 n」(0이면 숫자 생략)
  - [ ] `MeetingAttachmentsTab` — 「추가」 · 빈 상태 + 「파일 첨부하기」 · 목록 행(MD 타일/링크 글리프 · 이름 · 메타 · 「제거」) · 삭제된 문서 흐림 · `V2Gate` 푸터 「끌어다 놓아도 첨부됩니다 · 최대 50MB」
  - [ ] `AttachmentFileDrawer` — `DrawerFrame` 위. 헤더(타일 · 이름 · 메타 · 「다운로드」 · 「자료함에서 열기」 · ×) · 탭 미리보기/원문 텍스트 · **본문은 문서함 전까지 「자료함이 아직 없습니다」 스텁**. 링크 행은 드로어 대신 **기본 브라우저**
  - [ ] 「회의 시작」 → `POST /start` → 성공 시 **스위치가 `recording` 분기로 바뀐다**(페이지 이동 없음). 실패(409) 토스트 + 상세 재조회
  - [ ] 자동 저장 실패 — **WORK-003 U-7 규격 그대로**(`saveFailed`·`onRetry` prop, 소유자는 목록). 새로 만들지 않는다
  - [ ] 반응형 — 1280~1439: 사이드바 숨김 · 목록 좌 400 고정 · 시작 전 우 패널 400 고정 · 드로어 전체 화면 + 2열 → 1열 / ≥1440: 좌 500 · 우 464
- **검증**:
  - [ ] 「상세보기」로 들어간 시작 전 화면에 「기록 대기 00:00:00」 상태 바와 「회의 시작」이 있고, **「회의 정보 수정」 버튼과 「내 목소리 등록됨」 푸터가 없다**
  - [ ] 하단 입력 바에 **「새 안건 ▾」 칩 · 추천 칩 · 전송 버튼이 없고** 안건을 적어 `Enter` 하면 「안건 n」 행이 생기며 입력이 비워진다. 「추가」 버튼이 항상 있다
  - [ ] 안건 제목을 클릭해 고치고 바깥을 클릭하면 **저장 버튼 없이** 저장된다. **서버를 내린 채** 고치면 토스트 + 그 행 실패 표시 + 「다시 저장」이 뜨고 **가만히 두어도 재요청 0건**(네트워크 탭)
  - [ ] 「제거」로 안건을 지우면 확인 없이 사라지고 번호가 당겨진다
  - [ ] 「첨부 파일」 탭에서 URL 링크를 붙이면 라벨이 「첨부 파일 1」이 되고, 링크 행을 누르면 **브라우저가 열린다**. 「자료함 문서」는 스텁 안내
  - [ ] 첨부 탭에 PDF 를 드롭하면 「**v2에서 제공됩니다**」 토스트만 뜨고 요청이 없다
  - [ ] 헤더 `⋯` → 「삭제」 → **같은 모달**이 뜨고 삭제하면 **목록으로 이동**한다
  - [ ] 「회의 시작」을 누르면 **같은 화면이 `recording` 분기(플레이스홀더)로 바뀌고** 목록의 그 행에 「기록 중」 dot 이 붙는다. 그 행 우클릭 「삭제」는 비활성. 다른 창에서 다시 「회의 시작」을 누르면 「지금 상태에서는 할 수 없습니다」 토스트
  - [ ] 캘린더가 아직 없으므로 **임시 진입 버튼**(개발 화면)에서 `openDrawer(MeetingCreateDrawer, { startAt, endAt })` 로 열어 일시가 미리 채워지는지 확인한다(캘린더 그룹이 이 호출을 그대로 쓴다)
  - [ ] 창을 1280~1439 로 줄이면 목록 패널이 400, 시작 전 우 패널이 400 이 되고 드로어가 **전체 화면** + 프로젝트·유형 2열이 1열로 쌓인다
  - [ ] **정적 검사**: 자동 저장 실패 상태를 `useState` 로 드는 컴포넌트 0건 · `MeetingAttachmentsTab`/`AttachmentFileDrawer`/`MeetingAgendaList`/`MeetingTopBar` 가 **회의 상태·라우트를 import 하지 않는다**(prop 만 — WORK-007·008 재사용의 증명, grep 결과를 완료 증거에)
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 신규 env 가 없다(`STORAGE_ROOT` · `SONIOX_API_KEY` 는 WORK-007 이 처음 쓴다)
- [ ] 목록·상세 응답에 **다른 계정의 회의가 섞이지 않는다**(소유 검사가 service 에 있다 · 남의 것은 404)
- [ ] 응답에 `recording_path` · `ai_session_id` · 내부 경로 · 스택 트레이스가 **실리지 않는다**(SPEC-006 §4 「상세에 싣지 않는다」)
- [ ] 삭제가 **소프트**이고 녹음 파일을 지우는 코드가 **없다**(M-13). 복원 엔드포인트도 없다
- [ ] `schedule` 을 직접 쓰는 코드가 이 work 에 **0건**이다(SCH-1)
- [ ] `PATCH /api/meetings/{id}` 로 `status` 를 보내면 422 다(전이 우회 없음)

## Rollback

- **스키마**: `alembic downgrade -1` 로 회의 도메인 리비전을 되돌린다. **WORK-004 까지의 데이터(업무·`schedule`)는 영향이 없다** — `schedule` 의 `source_type='meeting'` 행은 남지만 조회가 원본 조인으로 거른다(§3-4 · FK 없음). 되돌린 뒤 고아 행은 캘린더 조회에 나오지 않는다
- **백엔드**: `meeting_router` 미등록으로 표면을 걷어낼 수 있다. `schedule_service.sync_from_meeting` 갈래는 남겨도 호출자가 없어 무해하다. **단 WORK-007 이 시작된 뒤에는 되돌리지 않는다** — `/start` · `build_detail` · 안건 표면에 WORK-007 이 얹힌다
- **프론트**: 브랜치 폐기. `/meetings` 는 WORK-002 의 빈 셸로 돌아간다. **`Selector` 인라인 행 수정은 단독으로 되돌리지 않는다** — 업무 드로어(WORK-004)도 같은 컴포넌트를 쓴다
- 부분 revert 시: Phase 5·6 만 되돌리면 API 와 목록은 살아 있다. Phase 4 만 되돌리면 상세 라우트가 없어 「상세보기」가 죽는다 — Phase 4·6 은 함께 되돌린다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-006 §6 Acceptance 22개 항목이 전부 확인**됐다. 단 **문서함 의존 3건**(자료함 md 첨부 · 파일 드로어 미리보기 렌더 · 「자료함에서 열기」 이동)은 **링크 갈래로 대체 확인**하고 문서 갈래는 문서함 work 이후로 미룬다(§Open Issues). **캘린더 의존 2건**(「+ 새 일정」에서 같은 드로어 · 드래그로 일시 변경)은 **임시 진입 호출 + `PATCH` curl** 로 대체 확인하고 캘린더 그룹이 실화면으로 다시 확인한다.
- [ ] 정적 검사 6종(`schedule` 쓰기 격리 · 상태 대입 격리 · `MeetingDetail` 빌더 단일 · 계층 위반 · 공용 컴포넌트의 상태/라우트 무의존 · 실패 상태 내부 state 0) 결과가 완료 증거에 붙어 있다.
- [ ] **생성이 요청 하나로 나가는 네트워크 캡처**와 **`/start` 뒤 스위치 전환 캡처**가 완료 증거에 있다.
- [ ] BE §12 필수 테스트 중 **3(겹침 — 업무↔회의 · 경계 접촉) · 5(파생) · 9(고아 없음)** 의 회의 쪽이 통과한다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **첨부의 「자료함 문서」 갈래와 파일 드로어 본문이 이 work 에서 스텁이다.** 문서함(SPEC-005)이 아직 없다. 임시 계약은 WORK-004 와 같다 — ① `meeting_attachment.document_id` 는 컬럼·CHECK·부분 UNIQUE 만 최종 형태로 두고 **FK 를 걸지 않는다** ② `kind='doc'` 요청을 서비스가 `validation_error` 로 거부한다 ③ 팝오버 문서 세그먼트와 파일 드로어 본문은 「자료함이 아직 없습니다」 안내다. **문서함 work 가 FK 리비전과 함께 셋을 실체화한다.** SPEC-006 §4·U-7 과 일시적으로 어긋나는 지점이라 코디 확인이 필요하다
- **ERD 반영분이 착수 전제다.** SPEC-006 §7 「ERD 변경 필요」 5건 + SPEC-007 §7-C 3건이 별도 워커에서 `database/` 에 반영 중이다. Phase 1 첫 항목이 그 대조이고, **반영 전 초안으로 마이그레이션을 만들지 않는다**(두 번 리비전을 파게 된다)
- **`invalid_meeting_status` 가 아키텍처 §8-2 표에 없고, SPEC-007 의 `meeting_not_recording` 과 합쳐야 한다**(SPEC-006 §7 정합 #3). 이 work 는 `invalid_meeting_status` 하나만 만든다. 표 갱신과 SPEC-007 정정은 코디 소관 — **WORK-007 착수 전에 닫혀야 한다**
- **SPEC-007 `PATCH …/agendas/{id} { state }` 의 응답 형태**(「사람 안건 전량」)가 이 work 의 「자식 쓰기는 `MeetingDetail` 전체」 규칙과 다르다(SPEC-006 §7 정합 #2). 이 work 는 `MeetingDetail` 전체로 만든다 — WORK-007 이 `state` 를 더할 때 코디 판정을 따른다
- **미리보기 패널의 `ended` 본문과 상세 라우트의 `recording`·`generating`·`ended` 분기가 플레이스홀더다.** WORK-007·008 착수 전까지 사용자는 시작한 회의를 **열 수 없다**(목록에 「기록 중」 표기만 보인다) — 세 work 를 연달아 진행하는 것을 전제한다
- **캘린더가 없어 생성 드로어 재사용과 드래그 `PATCH` 를 실화면으로 검증하지 못한다.** 임시 진입 호출과 curl 로 대체하고 캘린더 그룹이 다시 확인한다
- **`Selector` 인라인 행을 이 work 가 손보면 업무 생성 드로어도 바뀐다**(공용 컴포넌트). WORK-004 검수를 통과한 화면이 바뀌므로 그 Phase 의 완료 증거에 **업무 드로어 쪽 캡처도 함께** 붙인다
- **회의 길이 하한 5분 · 제목/안건 200자는 spec 판단이다**(SPEC-006 §4). 정책서에 근거가 없다 — 다른 값이 필요하면 DEC-003 갱신이 먼저다

## Related

- SPEC: SPEC-006 (frontmatter `links.specs`) · 인접 SPEC-007 · SPEC-008 · SPEC-009 (계약을 물려받는 쪽)
- Work: WORK-003 · WORK-004 · WORK-005 (선행) · WORK-007 · WORK-008 (후속 — `/start` · `MeetingDetail` · 안건·첨부 표면을 소비한다) · 캘린더 그룹 · 문서함 그룹
