---
type: work
id: WORK-006
title: "회의록 — 목록 · 생성 드로어 · 시작 전 화면 · AI 런타임 합류"
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
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-006]
  works: [WORK-003, WORK-004, WORK-005]
  releases: []
  related: [DEC-001, DEC-004, DEC-005]
---

# 회의록 — 목록 · 생성 드로어 · 시작 전 화면 · AI 런타임 합류

**회의를 만들고 안건을 적고 시작한다.** 회의록 도메인 스키마와 AI 런타임(Redis + open-kknaks worker + codex)이 여기서 선다 — 회의 중 기록·STT 는 WORK-007 이 그 위에 얹는다. 시작 전에는 **안건만** 만들어지고 줄은 하나도 생기지 않는다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003
- Covers spec: **SPEC-006**(회의록 — 목록 · 생성 · 시작 전)
- Depends on work: **WORK-003**(유형 목록 — **종류=미팅**만 거른다 · 프로젝트 · 팔레트 · `ColorPickerPopover`) · **WORK-004**(**`schedule_service` 겹침·파생** · `DrawerFrame` · `Selector` 의 「+ 새 프로젝트」 · 첨부 팝오버 · `EmptyState`) · **WORK-005**(`PeriodStepper` · `FilterChipBar` · 스켈레톤 규격)
- Parallel work: 없음
- Follow-up work: **WORK-007**(회의 중 — 이 work 가 만든 `recording` 상태와 AI 세션 위에서 시작한다) · **WORK-008**(종료·통합) · 캘린더 그룹(회의 일시가 `schedule` 로 파생된다)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`
  - **AI 런타임이 이 work 에서 처음 붙는다** — `docker-compose.local.yml` 에 **Redis + open-kknaks worker**, worker 에 **호스트 codex 바이너리와 `auth.json` 을 `ro` 바인드 마운트**, `CODEX_HOME` 은 named volume(`system/README.md` §codex 바인드 마운트). 호스트에 codex 가 설치·인증돼 있어야 한다
  - **문서함(`document`)이 아직 없다** — 회의 첨부(자료함 md)가 이 work 에서 **스텁**이다(§Open Issues)
  - Soniox 는 **WORK-007** 에서 붙는다. 이 work 는 `SONIOX_API_KEY` 를 쓰지 않는다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-004 미완 · 호스트 codex 설치·인증 미확인 |
| Next | Phase 1 — 회의 도메인 마이그레이션 · 회의록 CRUD API |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-006 §6 Acceptance 14개 대조 | todo |
| Design |  | 목록 + 프리뷰 · 생성 드로어 · 시작 전 2×2 탭 · 삭제 모달 · 회의록 영역 반응형(**이 영역 전체의 정본**) | todo |
| FE |  | 목록·프로젝트 칩·프리뷰 · 생성 드로어 · 시작 전 화면 · 프롬프트(안건만) | todo |
| BE |  | 회의 도메인 마이그레이션 · 회의록 CRUD · 안건·첨부 · `/start` + 웜스타트 | todo |
| QA |  | Phase 검증(앱 창 E2E) · 유형 필터·겹침·상태 가드 확인 | todo |
| Ops |  | **compose 에 Redis·worker 합류** · codex 마운트·`CODEX_HOME` 볼륨 · `AI_*` env | todo |

## Scope

포함:

- **회의 도메인 마이그레이션** — `meeting` · `meeting_agenda` · `meeting_line` · `meeting_transcript` · `meeting_attachment` · `meeting_batch_run`
- 회의록 CRUD API — 목록(기간·프로젝트 필터·`projectCounts`) · 생성(안건·첨부 포함 한 트랜잭션) · **트랙별 상세** · 수정(일시 포함) · 소프트 딜리트
- 안건 CRUD(시작 전·기록 중) · 첨부 추가/제거 표면
- **AI 런타임 합류** — compose(Redis + worker + codex 마운트) · `integrations/agent.py`(`AgentClient` 싱글턴 · 옵션 빌더 한 곳) · **회의 시작 웜스타트**
- **회의 시작**(`POST /start`) — 상태 `scheduled → recording`, `ai_session_id` 저장
- 회의록 **목록 화면**(월 단위 · 우측 프리뷰) · **프로젝트 필터 칩** · **프로젝트 생성 진입점**
- **새 회의록 드로어**(840) · **시작 전 화면**(안건 프롬프트) · **삭제 확인 모달**(600)
- **회의록 영역 반응형** — SPEC-006 U-6 이 이 영역 전체의 정본이다(WORK-007·008 이 참조한다)

제외:

- 회의 중 기록·STT·WS·AI 배치 → **WORK-007**
- 종료·통합·편집·업무 생성/갱신·회의 상세 드로어 → **WORK-008**
- 반복 회의·예약 알림·외부 캘린더 등록 — v1 밖(DEC-003 §1·§8)
- 회의 중 md 작성(`source=local`) — v2(§A-11 · M-17)
- 캘린더 화면 → 캘린더 그룹
- **첨부의 자료함 md 실동작** → 문서함 work. 이 work 는 **표면과 빈 상태 스텁**까지다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE) · 루트 compose
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `docker-compose.local.yml` | **Redis + open-kknaks worker 추가.** codex 번들·`auth.json` `ro` 마운트 · `CODEX_HOME` named volume · `PATH` 선두 |
| `app/back/config.py` · `.env.example` | `REDIS_URL` · `AI_NAMESPACE` · `AI_QUEUE` · `AI_MODEL` · `AI_TIMEOUT_SEC` · `STORAGE_ROOT`(WORK-007 이 쓴다) |
| `app/back/models/meeting.py` | 6 테이블. `meeting_agenda`·`meeting_line` 에 **`track` 컬럼** |
| `app/back/alembic/versions/*_meeting_domain.py` | 리비전 1건 + `downgrade` |
| `app/back/core/enums.py` | `MeetingStatus` · `IntegrationState` · `Track` · `LineKind` · `AgendaState` 추가 |
| `app/back/repository/meeting_repository.py` · `meeting_child_repository.py` | 회의 본체 / 안건·줄·첨부. **트랙별 조회는 `(meeting_id, track, agenda_id, order_index)` 인덱스** |
| `app/back/service/meeting_service.py` | 생성 트랜잭션 · 유형 종류 검증 · **겹침·파생은 `schedule_service` 를 부른다** · 상태 가드 · 시작 |
| `app/back/integrations/agent.py` | `AgentClient` 싱글턴 · **codex 실행 옵션 빌더 하나** · 웜스타트 제출 |
| `app/back/api/meeting_router.py` | SPEC-006 §4 의 11 표면 |
| `app/back/schemas/meeting.py` · `dto/meeting.py` | FE 계약 / 내부 dto |
| `app/back/tests/test_meeting.py` · `test_meeting_start.py` | 유형 종류 · 길이 상한 · 겹침 · 상태 가드 · 웜스타트 실패 허용 |
| `app/front/src/features/meetings/api.ts` · `types.ts` · `hooks/useMeetingsQuery.ts` · `useMeetingMutations.ts` | 호출·쿼리·무효화 |
| `app/front/src/features/meetings/hooks/useMeetingsViewParams.ts` | `?date=`·`?projectId=`·`?id=` 파싱 한 곳 |
| `app/front/src/features/meetings/components/MeetingListScreen.tsx` · `MeetingRow.tsx` · `MeetingPreview.tsx` | 목록 + 우측 프리뷰(1280~1439 오버레이 400) |
| `app/front/src/features/meetings/components/MeetingCreateDrawer.tsx` | U-3 드로어 840 |
| `app/front/src/features/meetings/components/MeetingSetupScreen.tsx` · `AgendaList.tsx` · `PromptBar.tsx` | 시작 전 화면 · 안건 목록 · 하단 프롬프트(**안건만**) |
| `app/front/src/features/meetings/components/MeetingSideTabs.tsx` | 우측 「실시간 스크립트 / 첨부 파일」 탭 껍데기 — **WORK-007 이 내용을 채운다** |
| `app/front/src/app/(app)/meetings/page.tsx` · `detail/page.tsx` | 라우트 껍데기. 상세는 **상태로 갈린다**(F-10) |
| `app/front/src/lib/api/queryKeys.ts` | `['meetings','list',…]` · `['meetings','detail',id]` 등록 + **유형·프로젝트 변경 시 `['meetings']` 무효화 연결**(WORK-003 이 남긴 자리) |

- Domain / schema note: **마이그레이션이 필요하다** — 회의 도메인 6 테이블을 **한 리비전에** 만든다. `meeting_transcript`·`meeting_batch_run` 은 WORK-007 이 처음 쓰지만, **같은 도메인을 세 번 마이그레이션하지 않기 위해** 여기서 함께 세운다(ERD 가 이미 닫혀 있다 — `database/README.md` §1)

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | 회의록 본체. **일시(`start_at`/`end_at`)를 소유**하고 `status`·`integration_state`·`ai_session_id`·`recording_path` 를 든다 |
| `meeting_agenda` | 안건 — **트랙별**(`human`·`ai`·`merged`) |
| `meeting_line` | 줄 — 3트랙. 이 work 는 **행을 만들지 않는다**(표면도 없다) |
| `meeting_transcript` | 확정 발화 블록 — WORK-007 이 쓴다 |
| `meeting_attachment` | 첨부(자료함 md). 이 work 는 표면까지, 실동작은 문서함 work |
| `meeting_batch_run` | 배치 이력 — WORK-007 이 쓴다 |

- 상태 / invariant: `domains/meeting.md` **M-1**(회의록이 일시 소유, 두 컬럼 NOT NULL) · **M-2**(`kind='meeting'` 유형만) · **M-3**(상태 4종, `generating` 신설) · **M-4**(`integration_state` 별도 축) · **M-5**(줄은 항상 안건에 속하고 **줄과 안건의 `track` 이 같다**) · **M-5-a**(안건도 트랙별) · **M-12**(`ai_session_id` 는 회의당 하나) · **M-13**(`recording_path` 영구 보관) · **M-18**(300분 초과 미지원)
- Migration 필요 여부: **필요**. 리비전 1건 + `downgrade`. 인덱스는 `database/README.md` §4 표 그대로
- **`meeting_attachment.document_id` 에 FK 를 걸지 않는다** — 대상 `document` 테이블이 아직 없다(WORK-004 와 같은 처리). 문서함 work 가 FK 추가 리비전을 낸다
- SPEC 에 환류해야 하는 변경: **`invalid_meeting_status` 코드**가 아키텍처 §8-2 표에 없다(SPEC-006 S006-OQ-1) — 구현은 SPEC-006 §4 를 따르고 표 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-007** | `meeting.status='recording'` · `ai_session_id` · `meeting_transcript`·`meeting_batch_run` 테이블 · `integrations/agent.py` 옵션 빌더 · 우측 사이드 탭 껍데기 | 회의 중 배치가 **웜스타트가 만든 세션을 `resume`** 한다. 세션이 없으면 배치가 매번 새 세션을 만들게 된다 |
| **WORK-008** | `meeting.status` 전이 자리(`generating`·`ended`) · `integration_state` · 트랙별 상세 응답 | 종료 파이프라인이 이 상태 축 위에서 돈다 |
| 캘린더 그룹 | `schedule`(`source_type='meeting'`) · 회의 상세 드로어(WORK-008 소유) | 회의 일시가 파생돼 캘린더에 뜬다 |
| 문서함 그룹 | `meeting_attachment.document_id` · 첨부 팝오버 | 문서함이 서면 첨부가 실동작으로 바뀐다 |

## Internal Interface Contract

외부 계약(엔드포인트·요청/응답·검증·에러)은 **SPEC-006 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| 일시 겹침·파생 | **WORK-004 의 `schedule_service` 를 그대로 부른다.** 회의용 겹침 검사·파생 함수를 새로 만들지 않는다 — 업무↔회의가 서로 막아야 하므로(DEC-005 §7 「종류 불문」) 구현이 둘이면 그 규칙이 깨진다 |
| 유형 거르기 | 회의 유형 목록은 **`kind='meeting'` 인 것만**. 화면이 걸러도 **서버 판정이 정본**이다(`invalid_work_type` 422) — 두 겹으로 막는다(M-2) |
| **트랙별 상세** | `GET /api/meetings/{id}` 의 `tracks` 는 `human`·`ai`·`merged` **세 키가 항상 있다.** 값이 없으면 `{"agendas": []}` 이고 **키를 생략하지 않는다** — 탭 하나가 트랙 하나를 그대로 그리므로(M-5-a) 화면이 키 유무를 분기하지 않게 한다 |
| 안건은 사람 트랙에 만들어진다 | 이 work 의 안건 표면은 **언제나 `track='human'`** 이다. 요청에 `track` 을 담지 않는다. AI 안건은 WORK-007 의 배치만 만든다(M-6) |
| `ai_session_id` | **회의 하나에 하나.** `POST /start` 가 웜스타트를 제출하고 받은 세션 id 를 저장한다. **이후 모든 배치가 이 세션을 `resume` 한다**(M-12 · BE §5-2) |
| 웜스타트 실패 | **회의 시작을 막지 않는다** — 결과를 쓰지 않는 호출이다. 실패는 **로그로 남기고 사용자에게 표시하지 않으며**, `ai_session_id` 가 비면 WORK-007 의 첫 배치가 새 세션을 만든다. **이 하나만 예외이고, 그 밖의 예외는 fallback 없이 전파한다**(DEC-003 §7 · BE §8-1) |
| 웜스타트 컨텍스트 | 안건 + **업무 화이트리스트**. 회의에 프로젝트가 있으면 그 프로젝트의 업무, **무소속 회의면 무소속 업무**(M-15-a · BE §5-2). 화이트리스트 산출 함수는 **한 곳**에 두고 WORK-007 의 배치 검증이 같은 함수를 쓴다 |
| codex 옵션 | **빌더 함수 하나**에서만 만든다(BE §5-2). 새 세션 호출과 `resume` 호출이 다른 옵션으로 나가는 사고를 구조로 막는다 |
| 상태 가드 | `/start` 는 `scheduled` 일 때만. 안건 수정·삭제는 `scheduled`·`recording` 일 때만. 위반은 **`invalid_meeting_status`(409)** — 상태 가드를 **service 한 곳**에서 판정한다 |
| 기록 중 삭제 | **스트림을 먼저 끊고** 소프트 딜리트한다(§5). 이 work 시점에는 스트림이 없으므로 **끊기 훅 자리만** 두고 WORK-007 이 채운다 |
| 녹음 원본 | **소프트 딜리트해도 지우지 않는다**(M-13). 삭제 경로에 파일 삭제 코드를 두지 않는다 |
| 낙관적 갱신 | 안건 추가·이름 수정은 **한다**. **일시 변경·회의 시작은 하지 않는다**(겹침·상태 거부가 정상 경로다 — FE §3-4) |
| 프로젝트 칩 집계 | `projectCounts` 는 **현재 기간 기준**이고 **프로젝트 필터 자신은 반영하지 않는다**(SPEC-004 `typeCounts` 와 같은 규칙) |

## Execution

### Phase 1 — 회의 도메인 마이그레이션 · 회의록 CRUD API

- **Status**: TODO
- **설명**: 화면 없이 **회의록 한 건이 만들어지고 읽히는 상태**를 만든다. 일시 겹침이 업무와 **같은 서비스**로 막히는지를 여기서 확인한다 — 두 번째 구현이 생기면 나중에 못 잡는다.
- **작업**:
  - [ ] `core/enums.py` — `MeetingStatus`·`IntegrationState`·`Track`·`LineKind`·`AgendaState`
  - [ ] `models/meeting.py` — 6 테이블. **`meeting_line.agenda_id` NOT NULL** · **줄과 안건의 `track` 일치 강제**(FK + 서비스 검사) · `meeting.start_at`/`end_at` NOT NULL
  - [ ] 리비전 1건 + `downgrade` + 인덱스(`(account_id, start_at)` · `(account_id, status) WHERE deleted_at IS NULL` · `(meeting_id, track, agenda_id, order_index)` · `(meeting_id, at_ms)` · `(meeting_id, seq)`)
  - [ ] `repository/meeting_repository.py` — 목록(기간·프로젝트) · 상세 · `projectCounts`
  - [ ] `service/meeting_service.py` — 생성(유형 종류 검증 → **`schedule_service` 겹침 검사** → `meeting` + 안건 + 첨부 INSERT → **파생**, 한 트랜잭션) · 상세(트랙별) · 수정 · 소프트 딜리트
  - [ ] `api/meeting_router.py` — 목록·생성·상세·수정·삭제 5표면
  - [ ] `schemas/meeting.py`·`dto/meeting.py`
  - [ ] `tests/test_meeting.py`
- **검증**:
  - [ ] `make migrate` 가 끝나고 `downgrade -1 → upgrade head` 왕복이 된다
  - [ ] `curl` 로 회의록을 만들면 `status:"scheduled"` · `integrationState:"not_started"` 이고 **`tracks` 에 세 키가 모두** 있다(`ai`·`merged` 는 빈 배열)
  - [ ] **종류가 「업무」인 유형**으로 만들려 하면 **422 `invalid_work_type`**
  - [ ] `endAt <= startAt` 또는 301분짜리는 **422 `validation_error`**, 5분 미만도 거부된다
  - [ ] **이미 14:00–15:00 업무 일정이 있는 시각**으로 회의를 만들면 **409 `schedule_overlap`** 이고 `meeting` 행이 만들어지지 않는다 — **업무↔회의가 서로 막는다**
  - [ ] 15:00–16:00 은 만들어진다(경계 접촉)
  - [ ] 일시를 PATCH 하면 **`schedule` 행이 따라 바뀐다**. 소프트 딜리트해도 **`schedule` 행은 남고 목록·캘린더 조회에서 빠진다**
  - [ ] **정적 검사**: `schedule` 을 쓰는 코드가 여전히 **`schedule_service.py` 밖에 0건**이다(WORK-004 의 격리가 깨지지 않았다 — grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 안건 · 첨부 API

- **Status**: TODO
- **설명**: 시작 전 화면이 조작할 표면을 연다. **줄을 만드는 경로가 이 work 에 없다**는 것을 표면 수준에서 못박는다 — 안건 표면만 있고 `lines` 표면은 WORK-007 이 연다.
- **작업**:
  - [ ] 안건 — 추가 · 제목/순서 수정 · 삭제. **요청에 `track` 을 담지 않고 서비스가 `human` 을 박는다**
  - [ ] 안건 개수 상한 50 · 제목 1~200자 · 상태 가드(`scheduled`·`recording` 만)
  - [ ] 첨부 — 추가 · 제거 표면. **이 시점에는 붙일 문서가 없다**(§Open Issues). 같은 문서 중복 첨부는 행을 만들지 않는다
  - [ ] `tests/test_meeting.py` 에 안건·상태 가드 케이스 추가
- **검증**:
  - [ ] 안건을 추가하면 상세의 **`tracks.human.agendas` 에만** 들어가고 `ai`·`merged` 는 빈 배열 그대로다
  - [ ] 안건 순서를 바꾸면 `orderIndex` 가 재배열되고 조회 순서가 따라온다
  - [ ] **`ended` 상태로 바꿔 둔 회의**에 안건을 추가하면 **409 `invalid_meeting_status`**
  - [ ] 51번째 안건은 **422**
  - [ ] **줄(`lines`)을 만드는 엔드포인트가 라우터에 없다**(`app/back/api/meeting_router.py` 에 `/lines` 경로 0건 — grep 결과를 완료 증거에)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 3 — AI 런타임 합류 · 웜스타트 · 회의 시작

- **Status**: TODO
- **설명**: **Redis 와 codex 워커가 compose 에 붙는 단계.** 회의 시작이 세션을 만들고 그 id 가 저장되는 것까지가 이 Phase 다 — 이 세션이 없으면 WORK-007 의 배치가 매번 새 세션을 만들어 「한 회의 = 한 세션」(M-12)이 깨진다.
- **작업**:
  - [ ] `docker-compose.local.yml` — Redis · open-kknaks worker. **codex 번들과 `auth.json` 을 `ro` 마운트**, `PATH` 선두, `CODEX_HOME` **named volume**(워커 재시작을 넘겨 세션이 산다)
  - [ ] **back 의 `open-kknaks` 핀과 worker 이미지 핀을 같은 값으로 묶는다**(system §codex)
  - [ ] `config.py`·`.env.example` — `REDIS_URL` · `AI_NAMESPACE` · `AI_QUEUE` · `AI_MODEL` · `AI_TIMEOUT_SEC`
  - [ ] `integrations/agent.py` — `AgentClient` **싱글턴** · **codex 실행 옵션 빌더 하나** · `submit_warm_start(...)` · `submit_with_resume(...)`(WORK-007 이 쓴다)
  - [ ] 업무 화이트리스트 산출 함수 — 프로젝트 회의면 그 프로젝트 업무, **무소속이면 무소속 업무**. **한 곳**에 둔다
  - [ ] `POST /api/meetings/{id}/start` — 상태 가드 → 웜스타트 제출 → `ai_session_id` 저장 → `status='recording'` · `recording_started_at` 채움
  - [ ] 웜스타트 실패 처리 — **로그만 남기고 시작을 진행**한다. `except Exception` 을 쓰지 않고 **어댑터가 던지는 구체 예외만** 잡는다(BE §8-1)
  - [ ] `tests/test_meeting_start.py` — 어댑터를 대역으로 바꿔(BE §12) 성공·실패 두 갈래
- **검증**:
  - [ ] `make up` 으로 Postgres·API·**Redis·worker** 가 함께 뜨고 로그에 오류가 없다
  - [ ] worker 컨테이너 안에서 `which codex` 가 **마운트된 호스트 바이너리 경로**를 가리킨다
  - [ ] `curl` 로 `/start` 를 부르면 **200 · `status:"recording"` · `recordingStartedAt` 이 채워지고**, DB 의 `ai_session_id` 에 **값이 들어 있다**
  - [ ] worker 를 **재시작해도** 그 세션으로 후속 제출이 붙는다(`CODEX_HOME` 볼륨 확인 — WORK-007 이 실제 배치로 다시 확인한다)
  - [ ] **Redis 를 내린 채** `/start` 를 부르면 **여전히 200 이고 상태가 `recording` 으로 바뀐다**. `ai_session_id` 만 비어 있고 **사용자에게 아무 오류도 표시되지 않는다**
  - [ ] 이미 `recording` 인 회의에 `/start` 를 다시 부르면 **409 `invalid_meeting_status`**
  - [ ] **정적 검사**: `anthropic`·`openai` 를 import 하는 코드가 **0건**이고, codex 실행 옵션을 만드는 곳이 **빌더 함수 하나**다(grep 결과를 완료 증거에 — BE §1 금지 · §5-2)
  - [ ] **정적 검사**: `except Exception` 이 **0건**이다(BE §8-1)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 4 — 회의록 목록 · 프로젝트 필터 칩 · 프리뷰

- **Status**: TODO
- **설명**: **앱 창에서 회의록이 보이는** 첫 단계. 기간·필터 규약을 WORK-005 와 같은 부품으로 세워 두 영역이 다른 문법을 갖지 않게 한다.
- **작업**:
  - [ ] `useMeetingsViewParams` — `?date=`·`?projectId=`(`none`=미정)·`?id=` 파싱 한 곳
  - [ ] `MeetingListScreen` — 타이틀 + **`PeriodStepper` 재사용**(WORK-005 산출물) + 「새 회의록」 · 좌측 캡션 「n건 · 최신순」
  - [ ] `MeetingRow` — 일시 · 유형 배지(`TypeBadge` 재사용) · 제목 · 요약 한 줄(**AI 한 줄 요약, 없으면 「안건 n」**) · 상태 표시(예정/기록 중/**생성중**/종료)
  - [ ] **프로젝트 필터 칩** — 「전체 n」·「미정 n」·프로젝트별. **선택 색(`#F1F2FE`+`#7181F8`), 검정 금지** · **줄바꿈 허용**(가로 스크롤·더보기 없음) · 같은 칩 재클릭 시 전체
  - [ ] `MeetingPreview` — 우측 프리뷰 + 「상세보기」. **1280~1439 에서 오버레이 400**
  - [ ] 스켈레톤 6줄(WORK-005 규격) · 빈 상태 · **실패 표시 + 「다시 시도」**(빈 목록으로 대체하지 않는다)
- **검증**:
  - [ ] 앱 창에서 회의록 목록이 **월 단위**로 뜨고 기간 스테퍼로 지난달을 볼 수 있다
  - [ ] 프로젝트 칩에서 「**미정**」을 누르면 **프로젝트 없는 회의만** 남고, 같은 칩을 다시 누르면 전체로 돌아간다
  - [ ] 프로젝트 필터를 걸어도 **칩 숫자가 바뀌지 않는다**(기간을 바꾸면 바뀐다)
  - [ ] 칩이 한 줄을 넘으면 **줄바꿈**하고 가로 스크롤이 생기지 않는다
  - [ ] 필터·기간을 건 뒤 **새로고침해도 조건이 유지**된다
  - [ ] **서버를 내린 채** 목록을 열면 **빈 목록이 아니라** 실패 표시 + 「다시 시도」다
  - [ ] 창을 1280~1439 로 줄이면 **우측 프리뷰가 오버레이 400** 으로 바뀐다
  - [ ] **정적 검사**: 이 화면에서 `--tm-ink` 를 쓰는 컴포넌트가 **0개**다(칩은 선택 색이다 — grep 결과를 완료 증거에)
- **완료 증거**: 미작성

### Phase 5 — 새 회의록 드로어 · 시작 전 화면 · 삭제 모달

- **Status**: TODO
- **설명**: 이 work 의 완성 지점 — **회의를 만들고 안건을 적고 시작한다.** 「회의 시작」을 누르면 상태가 `recording` 이 되고 화면이 WORK-007 자리로 넘어간다(그 화면은 아직 껍데기다).
- **작업**:
  - [ ] `MeetingCreateDrawer` — **`DrawerFrame` 을 쓰기만 한다**(폭·스크림·헤더/푸터 규격을 다시 정하지 않는다 — FE §6-2 「규격의 주인은 WORK-004」). 필드 순서(제목 / 프로젝트·유형 / 일시 / 안건 / 첨부). 열자마자 제목 포커스
  - [ ] 제출 조건 **제목 + 유형 + 시작·종료 일시**. **유형 목록은 종류=미팅만**
  - [ ] 프로젝트 셀렉터 — **WORK-004 의 `Selector` 를 그대로** 쓴다(하단 「+ 새 프로젝트」 포함)
  - [ ] 안건 인라인 추가 행 — `Enter` + **「추가」 버튼 병행**. 순서 그대로 저장
  - [ ] 첨부 — 첨부 팝오버 재사용. **문서 갈래는 빈 상태 안내**(스텁)
  - [ ] `MeetingSetupScreen` — 상태 바(회색 「기록 대기 00:00:00」 + 「회의 시작」) · 좌 「회의록 | AI 요약」 탭(**안건만, 줄 없음**) · 우 「실시간 스크립트 | 첨부 파일」 탭 껍데기
  - [ ] 하단 프롬프트 바 — 플레이스홀더 「안건을 입력하고 Enter」 + **「추가」 버튼**. **`/` 를 눌러도 줄 종류가 나오지 않고** 캡션이 뜬다
  - [ ] 안건 행 hover — 인라인 이름 수정 · 삭제 · **드래그 재정렬**(+ 행 `⋯` 의 「위로/아래로」 키보드 대체)
  - [ ] 헤더 `⋯` — 「회의록 정보 수정」(드로어를 값 채운 채로) · 「**삭제**」
  - [ ] 삭제 확인 모달 600 — `ConfirmModal` 재사용, 경고 슬롯 「**v1 에는 복원 화면이 없습니다. 녹음 원본은 서버에 그대로 남습니다.**」
  - [ ] 「회의 시작」 → `/start` → **WORK-007 화면 자리로 전환**(이 work 에서는 상태 바만 「기록 중」으로 바뀐 껍데기)
  - [ ] 반응형 — 좌 유동 + 우 사이드 탭 **400 고정**(1280~1439) / **464**(≥1440). **우측을 접지 않는다**
- **검증**:
  - [ ] 드로어의 **유형 목록에 종류가 「미팅」인 유형만** 보이고 「반복」·「개인」 항목이 없다
  - [ ] 제목·유형·일시를 넣기 전에는 「회의록 만들기」가 **비활성**이다
  - [ ] 프로젝트 셀렉터 하단 「**+ 새 프로젝트**」로 만든 프로젝트가 **바로 선택**되고 **설정 화면 목록에도 나타난다**
  - [ ] 드로어에서 넣은 **안건이 생성 직후 시작 전 화면에 그대로** 있다
  - [ ] 이미 일정이 있는 시각으로 만들면 「**그 시간에 다른 일정이 있습니다**」 토스트가 뜨고 **드로어가 닫히지 않으며 값이 남는다**
  - [ ] 301분짜리 회의를 만들려 하면 「회의는 300분을 넘을 수 없습니다」가 뜬다
  - [ ] 하단 프롬프트로 **안건이 추가**되고, **`/` 를 눌러도 줄 종류가 나오지 않는다**
  - [ ] 우측 스크립트 탭에 「**아직 회의 전입니다**」, 첨부 탭에 「첨부한 자료가 없습니다」가 보인다
  - [ ] 「자료 첨부」를 눌러도 붙일 문서가 없고 **「자료함이 아직 없습니다」 안내**가 보인다
  - [ ] 「회의 시작」을 누르면 상태 바가 「**기록 중**」이 되고 **목록에서도 「기록 중」**으로 보인다
  - [ ] 삭제 모달에 「**v1 에는 복원 화면이 없습니다. 녹음 원본은 서버에 그대로 남습니다**」가 보이고, 삭제하면 목록에서 사라진다
  - [ ] 창을 1280~1439 로 줄여도 **우측 사이드 탭이 400 을 유지하고 접히지 않는다**
  - [ ] **실측**: 서버를 내린 채 안건 이름을 고치면 토스트 + 그 필드 「저장되지 않았습니다 · 다시 저장」이 뜨고 **네트워크 탭에 재요청이 0건**이다. 유형·프로젝트 셀렉터(팝오버형)의 실패는 **그 행 아래 인라인 자리**에 나온다(SPEC-002 U-7)
  - [ ] **정적 검사**: **폭 리터럴(`840`·`w-[840px]`)이 `features/meetings/` 안에 0건**이다 — 이 work 의 드로어는 `DrawerFrame` 을 쓰기만 한다(FE §6-2. grep 결과를 완료 증거에)
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] **`auth.json` 은 파일 하나만 `ro` 로** 마운트한다 — codex 세션 디렉토리를 통째로 내주지 않는다
- [ ] `AI_NAMESPACE`·`AI_QUEUE` 가 **back 과 worker 에서 같은 값**이다(다르면 제출이 조용히 사라진다)
- [ ] `.env` 실제 값과 codex 인증 파일이 **레포에 커밋되지 않았다**
- [ ] 회의 응답에 **`recording_path`·`ai_session_id` 같은 내부 값이 실리지 않는다**
- [ ] 회의록 삭제 경로에 **녹음 파일을 지우는 코드가 없다**(M-13)

## Rollback

- **스키마**: `alembic downgrade -1` 로 회의 도메인 리비전을 되돌린다. 업무·계정 데이터는 영향이 없다
- **compose**: Redis·worker 서비스를 주석 처리하면 나머지는 그대로 뜬다. **웜스타트가 실패해도 회의 시작은 막히지 않으므로**(설계) 회의록 기능은 AI 없이도 Phase 5 까지 돈다 — 되돌림이 부분적으로 가능한 유일한 지점이다
- **백엔드**: `meeting_router` 미등록으로 표면을 걷어낼 수 있다. `schedule_service` 는 **되돌리지 않는다**(업무가 쓰고 있다)
- **프론트**: 브랜치 폐기. 사이드바의 「회의록」 메뉴는 WORK-002 의 셸에 이미 있으므로 **빈 화면이 되지 않게 라우트 껍데기는 남긴다**
- 부분 revert 시: Phase 3(AI 런타임)만 되돌리면 `/start` 가 세션 없이 상태만 바꾼다 — **WORK-007 착수 전이면 허용**, 이후에는 배치가 매번 새 세션을 만들게 되므로 되돌리지 않는다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-006 §6 Acceptance 14개 항목이 확인**됐다. **단 「첨부 팝오버에 자료함 md 문서만 나온다」 1건은 문서함 work 이후로 미룬다**(§Open Issues)
- [ ] 정적 검사 7종(`schedule` 쓰기 격리 유지 · `/lines` 표면 없음 · LLM SDK import 0 · codex 옵션 빌더 단일 · `except Exception` 0 · Ink 0 · **드로어 폭 리터럴 0**) 결과가 완료 증거에 붙어 있다.
- [ ] **업무↔회의 겹침이 서로 막힌다**는 실측이 완료 증거에 있다(DEC-005 §7 「종류 불문」).
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **회의 첨부가 이 work 에서 닫혀 있다.** 문서함(SPEC-005)이 다음 그룹이라 `document` 테이블이 없다. 임시 계약은 ① `meeting_attachment.document_id` 에 **FK 를 걸지 않는다** ② 팝오버 문서 세그먼트는 **빈 상태 안내** ③ 첨부 추가 요청은 대상이 없어 거부된다. **문서함 work 가 FK 추가 리비전과 함께 실체화한다** — SPEC-006 §4 계약과 일시적으로 어긋나는 지점이라 코디 확인이 필요하다
- **회의 도메인 6 테이블을 한 리비전에 만들었다.** `meeting_transcript`·`meeting_batch_run` 은 WORK-007 이 처음 쓴다 — 같은 도메인을 세 번 마이그레이션하지 않으려는 판단이고, ERD 가 이미 닫혀 있어(§1) 나중에 바뀔 여지가 작다
- **`invalid_meeting_status` 코드가 아키텍처 §8-2 표에 없다**(SPEC-006 S006-OQ-1). 표 갱신은 코디 소관
- **회의 길이 상한 300분·최소 5분을 생성 단계에서 막는 것은 spec 판단이다**(S006-OQ-2). DEC-003 §4 는 「다루지 않는다」이지 「입력을 막는다」가 아니다
- **프리뷰의 「원문」 탭이 시작 전·기록 중 회의에서 무엇을 보일지 정책에 없다**(S006-OQ-3). 지금 계약은 **상태 안내 문구만**이다
- **안건 재정렬을 드래그로 정했다**(S006-OQ-4). 디자인에 규격이 없어 키보드 대체 경로(`⋯` 의 위로/아래로)를 함께 뒀다
- **호스트 codex 설치·인증이 선행돼야 한다.** WORK-001 이 「codex·Redis·Soniox 는 범위 밖」으로 미룬 준비물이 이 work 에서 처음 필요하다 — 착수 전에 호스트에서 `codex` 실행과 `auth.json` 존재를 확인해야 한다(코디)
- **Windows 에서 codex 바인드 마운트가 확인되지 않았다.** 이 work 의 검증은 macOS 기준이다 — WORK-001 Open Issues 의 Windows 확인 시점과 함께 잡는다

## Related

- SPEC: SPEC-006 (frontmatter `links.specs`)
- Work: WORK-003 · WORK-004 · WORK-005 (선행) · WORK-007 · WORK-008 (후속)
