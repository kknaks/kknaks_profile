---
type: work
id: WORK-008
title: "회의록 종료 — 「생성중」 · 통합본 생성 · 편집 모드 · 업무 생성/갱신"
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
  specs: [SPEC-008]
  works: [WORK-005, WORK-006, WORK-007]
  releases: []
  related: [DEC-001, DEC-002, DEC-004, DEC-005]
---

# 회의록 종료 — 「생성중」 · 통합본 생성 · 편집 모드 · 업무 생성/갱신

**회의를 끝내면 통합본이 나오고, 액션 줄에서 업무가 생긴다.** 통합본은 사람이 쓴 문장을 그대로 쓰고 AI 에서는 근거와 누락분만 가져온다 — 그 규칙을 **우리가 다시 검증**한다. 업무 상태 변경은 **WORK-005 의 완료 게이트를 우회하지 않는다.**

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-003
- Covers spec: **SPEC-008**(회의록 — 종료 · 통합 · 편집 · 업무 연동)
- Depends on work: **WORK-005**(**`PATCH /api/tasks/{id}/status` 와 완료 게이트 판정** — 이 work 는 소비만 한다) · **WORK-006**(회의 상태 축 · 트랙별 상세 · 반응형 정본) · **WORK-007**(배치 파이프라인·세션·`AgendaLineTree`·근거 칩·스크립트 스크롤 훅 · 스트림 닫기 경로) · WORK-004(`task_service` 생성·부분 수정 · 메모 추가 · 연관업무 검색 규격)
- Parallel work: 없음
- Follow-up work: 캘린더 그룹(**이 work 가 만든 회의 상세 드로어를 재사용**한다 — DEC-005 §2) · 문서함 work(첨부 실체화)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`
  - open-kknaks worker · codex(WORK-006 이 붙였다) — **통합은 회의 전체를 한 번에 읽는 작업이라 배치보다 오래 걸린다**(한 시도 300초)
  - 새 외부 시스템은 없다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-005 · WORK-007 미완 |
| Next | Phase 1 — `job` 리소스 · 종료 API · 기동 스윕 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-008 §6 Acceptance 19개 대조 | todo |
| Design |  | 종료 모달 · 「생성중」 화면 · 실패 배너 · 한 줄 요약 바 · 편집 모드 · 드로어 3종 · 회의 상세 드로어 | todo |
| FE |  | 종료·폴링·생성중 화면 · 통합본 상세 · 편집 모드 · 드로어 3종 · 업무 버튼 · 회의 상세 드로어 | todo |
| BE |  | `job` · 종료 파이프라인 · **통합본 생성과 검증 3규칙** · 줄·안건 편집 표면 · 업무 생성/갱신 중계 | todo |
| QA |  | Phase 검증(앱 창 E2E) · **게이트 우회 없음 실측** · 통합 실패·타임아웃 재현 | todo |
| Ops |  | 장시간 작업 상한·기동 스윕 로그 확인 | todo |

## Scope

포함:

- **`job` 테이블과 작업 실행** — `202 + jobId` · 폴링(2초) · 상태·`step` · **기동 스윕**
- **회의 종료** — 확인 모달 → **스트림 닫기** → `generating` → job 발행
- **통합 파이프라인** — ① 최종 배치(AI 탭 전체 재정리) ② **통합본 생성**(`track='merged'`) + **검증 3규칙**
- 통합 실패·타임아웃 → `ended` + `integration_state='failed'` · **배너 + 「다시 생성」**(그 조합에서만)
- 「생성중」 화면 — 스피너 · 단계 문구 · **사람 원본 노출** · 편집 잠금 · 취소 버튼 없음
- **종료 후 상세** — AI 한 줄 요약 바 · 통합본 트리 · **근거 타임칩**(스크립트 스크롤·강조)
- **편집 모드** — 인라인 수정 · 줄 종류 전환 4종 · 안건 CRUD · **드로어 3종**(논의·결정 / 연관 업무 / 액션 아이템)
- **업무 생성(POST) · 업무 갱신(PATCH)** — 버튼 트리거, **WORK-005 의 완료 게이트를 그대로 지난다**
- **회의 상세 드로어**(840) — 회의록이 소유하고 캘린더가 재사용한다

제외:

- 목록·생성·시작 전·삭제·프로젝트 칩 → **WORK-006**
- 회의 중 기록·STT·회의 중 배치 → **WORK-007**
- 캘린더 화면 자체 → 캘린더 그룹(이 work 는 **드로어만** 제공한다)
- **통합본 재생성** — 정상 생성분에는 없다. 「다시 생성」은 실패에서만
- 업무 상세 화면 → WORK-004·005(여기서는 열어 보내기만 한다)
- **완료 게이트 판정 로직** → **WORK-005**. 이 work 는 **소비만** 한다
- 첨부의 자료함 md 실동작 → 문서함 work

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `app/back/models/job.py` | `job` — `kind`·`target_type`·`target_id`·`status`·`attempt`·`error_code`·`error_message`·`finished_at` |
| `app/back/alembic/versions/*_job_and_merge.py` | 리비전 1건 — `job` 테이블 + **`meeting_line.source_human_line_id`** 컬럼 |
| `app/back/service/job_service.py` | job 생성·상태 전이 · **상한 마감** · **기동 스윕** |
| `app/back/main.py` | 기동 시 스윕 훅. **스윕 실패가 기동을 막지 않는다**(BE §5-3) |
| `app/back/api/job_router.py` | `GET /api/jobs/{jobId}` |
| `app/back/service/meeting_service.py` | 종료(스트림 닫기 → `generating` → job) · **통합본 생성과 검증 3규칙** · 재생성 · 편집 표면 |
| `app/back/service/meeting_batch_service.py` | **최종 배치**(`phase='final'`) — 전량 교체. WORK-007 의 제출·검증 경로 재사용 |
| `app/back/ai_schemas/meeting_merge.json` | 통합 `output_schema` — **`sourceHumanLineId` 를 포함한다** |
| `app/back/api/meeting_router.py` | `/end` · `/integration/retry` · 줄 CRUD · 안건 CRUD · `/lines/{id}/create-task` · `/lines/{id}/apply-change` |
| `app/back/core/exceptions.py` | `InvalidPendingChangeError`(422 `invalid_pending_change`) 추가 |
| `app/back/tests/test_meeting_finalize.py` · `test_meeting_task_link.py` | 통합 검증 3규칙 · 실패 2회 · 타임아웃 · **게이트 우회 없음** |
| `app/front/src/features/meetings/hooks/useMeetingJob.ts` | **2초 폴링 훅 하나.** `succeeded`/`failed` 에서 멈추고 상세를 다시 읽는다 |
| `app/front/src/features/meetings/components/EndMeetingModal.tsx` | 확인 모달 600(`ConfirmModal` 재사용) |
| `app/front/src/features/meetings/components/GeneratingScreen.tsx` | 스피너 + 단계 문구 + **사람 원본 노출** + 편집 잠금 |
| `app/front/src/features/meetings/components/IntegrationFailBanner.tsx` | 실패 배너 + 「다시 생성」(**`ended`+`failed` 조합에서만**) |
| `app/front/src/features/meetings/components/MeetingEndedScreen.tsx` · `AiHeadlineBar.tsx` | 종료 후 상세 · 한 줄 요약 바 |
| `app/front/src/features/meetings/components/EditModeHeader.tsx` · `LineKindSelector.tsx` | 「변경은 자동 저장됩니다 · 편집 완료」 · 종류 4종 전환 |
| `app/front/src/features/meetings/components/AddLineDrawer.tsx` · `LinkTaskDrawer.tsx` · `ActionItemDrawer.tsx` | **드로어 3종**(`DrawerFrame` 재사용) |
| `app/front/src/features/meetings/components/TaskLineButtons.tsx` | 「업무 생성」/「업무 갱신」/「갱신 완료」 + 변경 예정 칩 |
| `app/front/src/features/meetings/components/MeetingDetailDrawer.tsx` | **회의 상세 드로어 840 — 회의록이 소유, 캘린더가 재사용** |
| `app/front/src/lib/api/queryKeys.ts` | `['jobs', id]` 등록 · job 완료 시 `['meetings','detail',id]` 무효화 |

- Domain / schema note: **마이그레이션이 필요하다** — `job` 테이블 + **`meeting_line.source_human_line_id`**(SPEC-008 이 계약에 넣었고 DB 도메인 문서에는 없다 — S008-OQ-3)

## Domain / Schema

| Entity | 역할 |
|---|---|
| `job` | 장시간 작업 상태의 **정본**. 「회의록 생성중」이 이걸 폴링한다 |
| `meeting.integration_state` | `not_started`·`running`·`succeeded`·`failed`. 이 work 가 처음 움직인다 |
| `meeting_agenda`·`meeting_line` (`track='merged'`) | **통합본** — 이 work 가 처음 만든다 |
| `meeting_line.source_human_line_id` (신규 컬럼) | **그 통합 줄이 어느 사람 줄을 계승했는지.** 검증 3규칙의 근거 |
| `meeting_batch_run` (`phase='final'`·`'integration'`) | 최종 배치·통합 이력 |

- 상태 / invariant: `domains/meeting.md` **M-4**(`ended`+`failed` 가 배너 조건) · **M-7**(전체 재정리는 종료 후 한 번뿐) · **M-8**(통합본 본문은 사람 문장 그대로) · **M-14**(`task_id` 는 버튼으로만 채워진다) · **M-14-a**(`pending_change` 는 **기한·상태·note 셋뿐**) · `backend/README.md` **§5-3**(job 실행·기동 스윕) · **§6**(비동기 API 규약) · **§8-3**(회의록발 완료도 게이트를 탄다)
- Migration 필요 여부: **필요**. 리비전 1건(`job` + `source_human_line_id`) + `downgrade`
- SPEC 에 환류해야 하는 변경: **`invalid_pending_change` 코드**와 **`job.step` 필드**가 아키텍처 §8-2·§6 에 없고, **`source_human_line_id`** 가 `domains/meeting.md` 에 없다(S008-OQ-2·3) — 표·문서 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 캘린더 그룹 | **`MeetingDetailDrawer`(840)** | DEC-005 §2 가 「회의록이 소유하고 캘린더가 재사용」으로 못박은 표면이다. **드로어는 부모를 모른다** — 캘린더가 `openDrawer` 로 열고 콜백을 받는다 |
| 캘린더 그룹 | 회의 상태별 CTA(`scheduled` 「회의 시작」 / `recording` 「회의로 이동」 / `generating` 스피너 / `ended`+`failed` 배너 축약형) | 캘린더 블록에서 어떤 상태의 회의를 열어도 같은 드로어가 뜬다 |
| 문서함 work | 첨부 목록·파일 드로어 | 이 work 시점에는 빈 상태 스텁이다 |

## Internal Interface Contract

외부 계약(엔드포인트·요청/응답·검증·에러)은 **SPEC-008 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **완료 게이트를 우회하지 않는다** | `apply-change` 의 상태 변경은 **`task_service.change_status()`**(WORK-005) 를 부른다. **회의록 쪽에 전이 그래프도 게이트 판정도 두지 않는다**(BE §8-3). 거부 코드·문구는 **SPEC-004 와 글자 그대로 같다** — 판정이 같으므로 문구도 같다 |
| `pendingChange` | **기한 · 상태 · note 셋뿐**(M-14-a). 그 밖의 키가 오면 **`invalid_pending_change`(422)**. `note` 는 **업무 메모에 새 항목으로 추가**하고 기존 필드를 덮어쓰지 않는다 |
| 업무 생성 | **`task_service` 의 생성 규칙을 그대로** 쓴다 — 제목 필수 · 유형 필수 · 삭제되지 않은 유형(SPEC-003 §4). 회의록용 생성 경로를 따로 만들지 않는다 |
| 거부 시 상태 | 게이트·전이·겹침이 거부하면 **업무도 줄도 바뀌지 않고 `pending_change` 가 그대로 남는다.** 부분 적용이 없다 |
| **비동기 규약** | `POST /end` → **`202 { jobId }`**. 프론트는 **2초 폴링**. **통지 경로를 둘로 두지 않는다** — WS 는 종료와 함께 닫힌다(SYS-7). **job 은 결과를 담지 않는다** — 완료 후 `GET /api/meetings/{id}` 를 다시 읽는다 |
| job `step` | `final_batch`(「AI 정리 중」) → `integrating`(「통합본 만드는 중」). **화면 단계 문구의 유일한 근거**다 — 화면이 시간으로 단계를 추측하지 않는다 |
| 수치 | 통합 재시도 **2회**(총 3번) · 한 시도 상한 **300초** · job 전체 상한 **900초** · 폴링 **2초**. **무한 대기 금지** — 상한을 넘으면 `integration_timeout` 으로 마감한다 |
| 종료 순서 | **① 스트림 닫기 → ② `generating` → ③ 최종 배치 → ④ 통합본.** 스트림 닫기는 **실패 여부와 무관하게 실행**된다(BE §5-1 `finally`). **최종 배치가 실패해도 통합은 진행**하고 AI 탭은 회의 중 증분 상태로 남긴다 |
| **통합 검증 3규칙** | 임계값을 두지 않는다. 결과의 각 줄이 `sourceHumanLineId` 를 담게 하고 **우리가 검증**한다. ① 값이 있으면 **본문이 그 사람 줄과 글자 그대로 같아야 한다** — 다르면 **사람 원문으로 덮어쓴다** ② **한 사람 줄을 두 통합 줄이 계승할 수 없다** — 위반이면 그 결과를 **실패로 본다** ③ 값이 없는 줄은 AI 트랙에만 있던 내용이고 **근거는 AI 줄에서 물려받는다** |
| 통합 안건 | 사람 안건이 먼저 오고, **사람 안건에 흡수되지 않은 AI 안건이 뒤에** 붙는다. 통합본 안건·줄은 전부 `track='merged'` |
| 편집 대상 트랙 | **회의록 탭이 보여주는 트랙만** — 통합 성공이면 `merged`, **실패면 `human`**. **`ai` 트랙은 수정할 수 없다**(로그성 기록 — DEC-003 §6). 서비스가 트랙으로 거부한다 |
| 줄 종류 전환 | `task` 로 바꾸려면 **`taskId` 가 있어야 한다** — 연결 없이 업무 줄이 되지 않는다(M-14) |
| 편집 이력 | **남기지 않는다.** 편집은 덮어쓰기다(DEC-003 §6) — 그래서 **「되돌리기」를 두지 않는다** |
| 드로어 규칙 | 편집 드로어 3종과 회의 상세 드로어는 **`DrawerFrame`(WORK-004)** 을 **쓰기만 한다** — 폭·스크림·헤더/푸터 규격을 다시 정하지 않는다. **폭 리터럴이 이 work 의 코드에 나타나면 반려**다(FE §6-2, 2026-09-06 확정). **드로어 안에서 편집하지 않고**, 드로어 안에서 또 드로어를 열지 않는다. **드로어는 동시에 하나** |
| 편집 실패 표시 | **SPEC-002 U-7 규격 그대로.** 실패 상태를 **컴포넌트 내부 state 로 두지 않고** `saveFailed`·`onRetry` prop 으로 받으며 **소유자는 줄/안건 행**이다. 줄 종류 셀렉터·안건 셀렉터 같은 **팝오버형 컨트롤의 실패는 그 행 아래 인라인 자리 하나**에 모은다(2026-09-06 확정) |
| 재생성 표면 | **`status='ended'` + `integrationState='failed'` 일 때만.** 정상 생성분에는 표면 자체가 없다(DEC-003 §4) — 서비스가 조합으로 거부하고 화면은 버튼을 그리지 않는다 |
| 기동 스윕 | 앱이 뜰 때 `queued`/`running` job 을 훑어 재개하거나 실패로 마감한다. **「생성중」이 영원히 도는 상태를 만들지 않는다.** **스윕 실패는 기동을 막지 않는다**(BE §5-3 — 설계한 실패 하나) |

## Execution

### Phase 1 — `job` 리소스 · 종료 API · 기동 스윕

- **Status**: TODO
- **설명**: **비동기 규약의 뼈대**를 먼저 세운다. 종료가 `202` 를 주고 상태가 `generating` 이 되며 폴링이 도는 것까지 — 통합 내용이 비어 있어도 이 골격은 그 자체로 돌아야 한다.
- **작업**:
  - [ ] `models/job.py` + 리비전(`job` 테이블 + **`meeting_line.source_human_line_id`**) + `downgrade` + 인덱스(`(account_id, status)` · `(target_type, target_id)`)
  - [ ] `service/job_service.py` — 생성 · 상태·`step` 전이 · **상한 마감**(900초 → `integration_timeout`) · **기동 스윕**
  - [ ] `main.py` — 기동 스윕 훅. **실패해도 앱이 뜬다**
  - [ ] `api/job_router.py` — `GET /api/jobs/{jobId}`. 소유 검사
  - [ ] `POST /api/meetings/{id}/end` — 상태 가드(`recording` 만) → **스트림 닫기**(WORK-007 경로) → `status='generating'` · `integration_state='running'` → job INSERT → **`202 { jobId }`**
  - [ ] 실행은 **back 프로세스의 asyncio 태스크**(BE §5-3). **단계마다 세션을 새로 열고 그 단계 끝에 commit** 한다(BE §7)
  - [ ] `tests` — 상태 가드 · 202 · 스윕(재시작 시 `running` job 이 마감되거나 재개된다)
- **검증**:
  - [ ] `curl` 로 `/end` 를 부르면 **202 와 `jobId`** 가 오고 상태가 **`generating`** 이 된다
  - [ ] `GET /api/jobs/{jobId}` 가 `status`·`step` 을 준다
  - [ ] 이미 `ended` 인 회의에 `/end` 를 부르면 **409 `invalid_meeting_status`**
  - [ ] **종료 요청과 동시에 WS 가 닫힌다**(연결해 둔 스트림이 끊기고 서버 로그에 업스트림 종료가 남는다)
  - [ ] **작업 도중 API 를 재시작하면** 남아 있던 job 이 **재개되거나 `failed` 로 마감**되고, **`generating` 이 영원히 남지 않는다**
  - [ ] **DB 를 내린 채 기동**하면 스윕이 실패해도 **앱은 뜬다**(로그에 실패 기록)
  - [ ] 남의 job id 로 조회하면 404
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 최종 배치 · 통합본 생성 · 검증 3규칙 · 실패 처리

- **Status**: TODO
- **설명**: **이 work 의 핵심.** 「AI 가 사람 문장을 다듬지 않는다」를 **구조로 강제**한다 — 유사도 임계값이 아니라 계승 관계와 글자 일치로 판정하므로 결과만 보고 확인할 수 있다.
- **작업**:
  - [ ] `meeting_batch_service` — **최종 배치**(`phase='final'`): `resume` 세션으로 회의 전체 재정리 → **`track='ai'` 전량 교체**(DELETE + INSERT). **실패해도 증분 상태를 유지하고 통합은 계속한다**
  - [ ] `ai_schemas/meeting_merge.json` — 통합 `output_schema`. **줄마다 `sourceHumanLineId`(nullable)** 를 요구한다
  - [ ] `meeting_service` 통합 — 사람 트랙 + AI 트랙을 컨텍스트로 제출 → **검증 3규칙** → `track='merged'` 안건·줄 INSERT
    - [ ] ① 계승 줄의 **본문이 사람 줄과 글자 그대로 같지 않으면 사람 원문으로 덮어쓴다**
    - [ ] ② **한 사람 줄을 둘이 계승하면 그 결과를 실패로 본다**
    - [ ] ③ 계승 없는 줄은 **AI 줄에서 `evidence` 를 물려받는다**
  - [ ] 안건 통합 — 사람 안건 먼저, 흡수되지 않은 AI 안건이 뒤에
  - [ ] `ai_headline` · `counts{agenda,decision,action}` 산출(**`counts` 는 파생값**)
  - [ ] 실패 — **재시도 2회** → `status='ended'` + `integration_state='failed'` + job `errorCode:"integration_failed"`. 타임아웃은 `integration_timeout`
  - [ ] **`POST /api/meetings/{id}/integration/retry`** — **`ended`+`failed` 조합에서만**. `202 { jobId }`
  - [ ] **외부 호출 중 트랜잭션을 열어 두지 않는다**(BE §7)
  - [ ] `tests/test_meeting_finalize.py` — BE §12 필수 **8**(통합 실패 시 사람 줄·AI 줄·트랜스크립트 유지) + 검증 3규칙
- **검증**:
  - [ ] 종료하면 job 의 `step` 이 **`final_batch` → `integrating`** 으로 바뀐다
  - [ ] 통합 성공 후 `tracks.merged` 에 안건·줄이 생기고 **`status:"ended"` · `integrationState:"succeeded"`** 다
  - [ ] **통합 줄의 본문이 사람 줄과 글자 그대로 같다** — 대역이 문장을 다듬어 돌려주면 **사람 원문으로 덮어써진다**(테스트로 확인)
  - [ ] **한 사람 줄을 둘이 계승한 결과**를 주면 그 시도가 **실패로 처리**되고 재시도가 돈다
  - [ ] 계승 없는 줄이 **AI 줄의 `evidence` 를 그대로** 갖는다
  - [ ] **최종 배치를 실패시켜도 통합이 진행**되고 AI 탭이 **회의 중 증분 상태 그대로** 남는다
  - [ ] 통합을 3번 다 실패시키면 **`ended` + `failed`** 이고 **사람 줄·AI 줄·트랜스크립트·녹음 파일이 전부 남아 있다**
  - [ ] 한 시도를 300초 넘게 끌면 마감되고, 900초를 넘기면 **`integration_timeout`** 이다
  - [ ] `integrationState='succeeded'` 인 회의에 `retry` 를 부르면 **거부**된다(정상 생성분 재생성 없음)
  - [ ] **정적 검사**: `track='merged'` 로 INSERT 하는 코드가 **통합 함수 하나**이고, 통합 결과를 그대로 신뢰해 INSERT 하는 경로가 **없다**(검증을 지나야 한다 — grep 결과를 완료 증거에)
  - [ ] `pytest` 통과 — BE §12 필수 8
- **완료 증거**: 미작성

### Phase 3 — 종료 확인 모달 · 「생성중」 화면 · 폴링 · 실패 배너

- **Status**: TODO
- **설명**: **앱 창에서 회의를 끝내는** 단계. 생성중에도 **내가 쓴 회의록이 그대로 보이는 것**이 이 화면의 요점이다 — 빈 화면으로 덮으면 실패했을 때 사용자가 잃은 것처럼 보인다.
- **작업**:
  - [ ] `EndMeetingModal` 600 — `ConfirmModal` 재사용. 경고 슬롯 「**종료한 회의는 다시 기록할 수 없습니다.**」
  - [ ] `useMeetingJob` — **2초 폴링 훅 하나**. `succeeded`/`failed` 에서 멈추고 **`['meetings','detail',id]` 무효화**
  - [ ] `GeneratingScreen` — 스피너 + 「**회의록 생성중**」 + **단계 문구**(job `step` 이 근거) + 경과 시간. **진행률 퍼센트 없음 · 취소 버튼 없음**
  - [ ] 생성중 좌측 — **사람이 쓴 줄이 그대로 보인다**(읽기 전용, 편집 버튼 비활성, 프롬프트 바 없음). 우측 스크립트·첨부 그대로
  - [ ] 목록에서 그 회의록이 「**생성중**」으로 보이고, 열면 **같은 화면이 이어진다**
  - [ ] `IntegrationFailBanner` — **`ended`+`failed` 조합에서만**. 「**통합 정리에 실패했습니다**」 + 「사람이 쓴 회의록·AI 요약·스크립트·녹음은 그대로 있습니다」 + 「**다시 생성**」
  - [ ] 상태 바의 「회의 종료」 활성화(WORK-007 이 비활성으로 그려 둔 자리)
- **검증**:
  - [ ] 「회의 종료」를 누르면 **확인 모달**에 「종료한 회의는 다시 기록할 수 없습니다」가 보인다
  - [ ] 종료하면 「**회의록 생성중**」이 뜨고 단계 문구가 「AI 정리 중」 → 「통합본 만드는 중」으로 바뀐다
  - [ ] 생성중에도 **내가 쓴 회의록이 그대로 보이고** 편집 버튼이 비활성이며 **프롬프트 바가 없다**
  - [ ] **다른 화면으로 갔다가 목록에서 열면 생성중이 이어져** 보인다(상태가 서버에 있다)
  - [ ] **네트워크 탭 실측**: 폴링이 **2초 간격**이고 `succeeded`/`failed` 에서 **멈춘다**(무한히 계속되지 않는다)
  - [ ] 통합을 실패시키면 **배너**가 뜨고 **회의록 탭에 사람 원본이 그대로** 보인다. 스크립트·AI 탭도 남아 있다
  - [ ] 「**다시 생성**」을 누르면 생성중 화면으로 돌아가고, 성공하면 배너가 사라진다
  - [ ] **정상 생성된 회의록에는 「다시 생성」 버튼이 없다**
  - [ ] **진행률 퍼센트와 취소 버튼이 화면에 없다**
- **완료 증거**: 미작성

### Phase 4 — 종료 후 상세 · 근거 타임칩 · 회의 상세 드로어

- **Status**: TODO
- **설명**: 통합본을 **읽는** 화면. 트리는 WORK-007 의 `AgendaLineTree` 를 그대로 쓴다 — 두 탭이 같은 문법이어야 통합본과 AI 탭을 대조할 수 있다. 회의 상세 드로어도 여기서 만들어 **캘린더 그룹이 재사용**한다.
- **작업**:
  - [ ] `MeetingEndedScreen` — 헤더(제목·일시·소요·유형 배지·프로젝트 칩·회색 「**종료된 회의**」 칩·`⋯`·「편집」)
  - [ ] `AiHeadlineBar` — `#EEF1FE`/`#C9D1FB`, 한 문장 + 「안건 3 · 결정 2 · 액션 2」. **없으면 바를 그리지 않는다**
  - [ ] 좌측 회의록 탭 = **통합본**(`merged`) / AI 요약 탭 = **최종 배치 결과**(`ai`). 탭 dot 회의록 `#7181F8` · AI `#B3B3B3`
  - [ ] **근거 펼침은 hover 우측 화살표로만** — 줄 전체 클릭은 인라인 편집이라 겹치지 않는다. 칩 클릭 → **WORK-007 의 스크립트 스크롤·강조 훅** 재사용
  - [ ] **통합 실패 시 회의록 탭은 사람 원본(`human`)** 을 그린다
  - [ ] `MeetingDetailDrawer` 840 — 헤더 72(유형 배지·프로젝트 칩 / 제목 / 일시·소요 / 상태 칩 / ⤢ / ×) · 본문(한 줄 요약 → 안건>줄 트리 → 첨부) · **상태별 CTA 4종** · **편집·업무 버튼 없음**
  - [ ] ⤢ → 전체 페이지 승격(닫히고 이동). **드로어는 부모를 모른다**
  - [ ] 반응형 — 드로어가 1280~1439 에서 **전체 화면 + `←`**
- **검증**:
  - [ ] 통합이 끝나면 회의록 탭이 **통합본**으로 바뀌고 상단에 **AI 한 줄 요약 바**가 생긴다
  - [ ] 통합본에서 내가 적은 결정 줄의 **문장이 내가 쓴 그대로**다
  - [ ] 그 줄에 hover 해 화살표로 펼치면 **근거 칩**이 붙어 있고, 누르면 **우측 스크립트가 그 구간으로 스크롤·강조**된다
  - [ ] 회의 중 내가 적지 않았지만 AI 가 잡은 내용이 **추가 줄**로 들어와 있다
  - [ ] AI 요약 탭이 **최종 배치 결과**로 갈아 끼워져 있다(회의 중 증분과 다르다)
  - [ ] 목록 프리뷰에서 회의를 열면 **회의 상세 드로어(840)** 가 뜨고 **⤢ 로 전체 페이지**가 된다
  - [ ] 드로어에 **편집·업무 버튼이 없다**
  - [ ] `scheduled`·`recording`·`generating` 회의를 드로어로 열면 **상태별 CTA**가 다르게 보인다
  - [ ] 통합 실패 회의를 열면 회의록 탭에 **사람 원본**이 보인다
  - [ ] 창을 1280~1439 로 줄이면 드로어가 **전체 화면**이 되고 헤더 좌측에 `←` 가 생긴다
  - [ ] **정적 검사**: `AgendaLineTree` 를 쓰지 않고 트리를 다시 그린 컴포넌트가 **0개**다(회의록·AI·통합본 세 탭이 한 컴포넌트를 쓴다 — grep 결과를 완료 증거에)
- **완료 증거**: 미작성

### Phase 5 — 편집 모드 · 드로어 3종 · 업무 생성/갱신

- **Status**: TODO
- **설명**: 이 work 의 완성 지점 — **회의록을 고치고 액션 줄에서 업무를 만든다.** 업무 상태 변경이 **WORK-005 의 게이트를 그대로 지나는지**가 이 Phase 의 판정 기준이다.
- **작업**:
  - [ ] 줄·안건 편집 표면 — `POST/PATCH/DELETE /lines` · `POST/PATCH/DELETE /agendas`. **상태가 `ended` 일 때만**, **회의록 탭이 보여주는 트랙만**(`ai` 거부)
  - [ ] `EditModeHeader` — 「**변경은 자동 저장됩니다**」 + 「**편집 완료**」 + 회색 「편집 중」 칩. **검정을 쓰지 않는다**. **「되돌리기」 없음**
  - [ ] 편집 중 **하단 프롬프트 바를 감춘다**(줄 추가 경로를 하나로)
  - [ ] 인라인 수정(자동 저장, `InlineEditText` 재사용) · `LineKindSelector` 4종 전환. 실패는 **U-7 규격**(자동 재시도 없음)
  - [ ] `AddLineDrawer`(논의·결정 — 종류·안건·내용·상세·**근거 구간 칩**) · `LinkTaskDrawer`(**업무 검색 = SPEC-003 U-8 규격 재사용** · 단일 선택 · 기한/상태 · 진행 메모) · `ActionItemDrawer`(업무 생성 양식 + 「회의록 줄을 연관 업무로 바꾸기」 토글 **기본 켜짐**)
  - [ ] 「상세 설명」 캡션에 「(**종료된 회의에서는 채워지지 않습니다**)」를 덧붙인다
  - [ ] `POST /lines/{id}/create-task` — **`task_service` 생성 규칙 그대로**. `convertLine` 참이면 줄이 **업무 줄로 전환**되고 `taskId` 가 붙는다
  - [ ] `POST /lines/{id}/apply-change` — **기한·상태·note 셋만** 허용(`invalid_pending_change`). 상태는 **`task_service.change_status()`** 를 부른다. `note` 는 **메모 새 항목**
  - [ ] `TaskLineButtons` — 액션 줄 「업무 생성」 / 업무 줄 「업무 갱신」 + 변경 예정 칩 / 갱신 후 회색 「**갱신 완료**」
  - [ ] 게이트 거부 토스트 — **SPEC-004 와 같은 문구** + 「**업무 열기**」(그 업무 상세를 열고 회의록 화면은 남는다)
  - [ ] **낙관적 갱신 없음**
  - [ ] `tests/test_meeting_task_link.py` — 게이트 거부 · 전이 위반 · 허용 필드 밖 거부 · 메모 누적
- **검증**:
  - [ ] 「편집」을 누르면 헤더가 「변경은 자동 저장됩니다 · 편집 완료」로 바뀌고 **하단 프롬프트 바가 사라진다**
  - [ ] 줄 문장을 고치고 다른 곳을 클릭하면 **저장 버튼 없이** 저장되고, 종류 셀렉터로 「논의 → 결정」 전환이 된다
  - [ ] **AI 요약 탭의 줄은 편집되지 않는다**(입력 필드가 되지 않고 서버도 거부한다)
  - [ ] 안건 아래 「+ 액션 아이템」 드로어에서 **업무가 만들어지고**, 토글이 켜져 있으면 그 줄이 **업무 줄로 바뀌며** 업무가 연결된다
  - [ ] 만든 업무가 **내 업무 목록에 보인다**
  - [ ] 결과자료도 완료 결과도 없는 업무를 「업무 갱신」으로 **완료로 보내면 거부**되고 「**완료하려면 결과자료 1건 또는 완료 결과가 필요합니다**」 + 「업무 열기」가 뜬다. **업무도 줄도 바뀌지 않고 대기분이 남는다**
  - [ ] **네트워크 탭 실측**: 그 요청의 응답 코드가 **`task_completion_blocked`** 이고 **문구가 WORK-005 의 리스트·칸반과 글자 그대로 같다**(캡처 2장을 나란히 완료 증거에)
  - [ ] 완료 결과를 채운 뒤 다시 갱신하면 성공하고 버튼이 회색 「**갱신 완료**」가 된다
  - [ ] 갱신 메모가 **업무 메모에 새 항목으로 추가**되고 **기존 메모가 지워지지 않는다**
  - [ ] `pendingChange` 에 `title` 같은 다른 키를 넣으면 **422 `invalid_pending_change`** 이고 드로어가 닫히지 않는다
  - [ ] 완료 상태 업무를 「취소」로 갱신하려 하면 **409 `invalid_status_transition`**
  - [ ] **「되돌리기」 버튼이 화면에 없다**
  - [ ] **서버를 내린 채** 줄 종류를 바꾸면(팝오버형 컨트롤) **그 행 아래 인라인 자리**에 「종류가 저장되지 않았습니다 · 다시 저장」이 뜨고 재요청이 나가지 않는다
  - [ ] **정적 검사**: 회의록 코드에서 `task.status` 를 직접 대입하거나 완료 게이트를 판정하는 코드가 **0건**이고, `TaskCompletionBlockedError` 를 던지는 곳이 **여전히 `task_service` 1곳**이다(grep 결과를 완료 증거에 — BE §8-3)
  - [ ] **정적 검사**: **폭 리터럴(`840`·`w-[840px]`)이 `features/meetings/` 안에 0건**이고, 자동 저장 실패 상태를 `useState` 로 들고 있는 컴포넌트가 **0건**이다(FE §6-2 · SPEC-002 U-7 구현 규약)
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] job 상한이 **실제로 마감을 낸다** — 상한 없는 대기 경로가 남아 있지 않다(DEC-003 §7 「무한 대기 금지」)
- [ ] 기동 스윕이 **다른 계정의 job 을 건드리지 않는다**
- [ ] 통합 실패해도 **사람 줄·AI 줄·트랜스크립트·녹음 파일이 지워지지 않는다**
- [ ] `job` 응답에 **`errorMessage` 로 스택 트레이스가 새어 나가지 않는다**(사람이 읽는 문구만)
- [ ] 회의록발 업무 생성·갱신이 **다른 계정의 업무에 닿지 않는다**(소유 검사)

## Rollback

- **스키마**: `alembic downgrade -1` 로 `job` + `source_human_line_id` 리비전을 되돌린다. **되돌리기 전에 `generating` 상태로 남은 회의를 `ended` 로 마감**해야 한다 — job 이 사라지면 폴링할 대상이 없어져 화면이 영원히 스피너가 된다
- **백엔드**: `/end` · `/integration/retry` · 편집·업무 연동 라우트를 걷어내면 표면이 사라진다. **`track='merged'` 행은 남고 화면이 그리지 못할 뿐**이다
- **통합만 되돌리기**: 통합 단계를 건너뛰고 `status='ended'` + `integration_state='failed'` 로 마감하게 하면, 화면은 **사람 원본 + 실패 배너**로 정상 동작한다 — **설계상 통합 없이도 회의록이 비지 않는다**(부분 revert 가 가능한 지점)
- **프론트**: 브랜치 폐기. WORK-007 의 회의 중 화면이 남아 있어야 하고, **「회의 종료」 버튼은 다시 비활성으로** 되돌린다
- **되돌리지 않는 것**: WORK-005 의 상태 엔드포인트. 이 work 는 소비자일 뿐이다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-008 §6 Acceptance 19개 항목이 전부 확인**됐다.
- [ ] **게이트 우회 없음 실측** — 회의록발 완료 거부의 코드·문구가 리스트/칸반과 같다는 캡처 2장이 완료 증거에 있다.
- [ ] **통합 검증 3규칙**이 테스트로 확인됐다(다듬은 문장을 되돌린다 · 이중 계승은 실패 · 계승 없는 줄이 근거를 물려받는다).
- [ ] 정적 검사 5종(`merged` INSERT 단일 · 트리 컴포넌트 단일 · 회의록에 게이트 판정 0 · **드로어 폭 리터럴 0** · **실패 상태 내부 state 0**) 결과가 붙어 있다.
- [ ] BE §12 필수 테스트 **8(통합 실패)** 이 통과한다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **`invalid_pending_change` 코드와 `job.step` 필드가 아키텍처 §8-2·§6 에 없다**(S008-OQ-2). 표 갱신은 코디 소관
- **`source_human_line_id` 를 이 work 가 스키마에 추가한다**(S008-OQ-3). SPEC-008 이 외부 계약에 넣었으나 `domains/meeting.md` M-8 은 계승 관계를 저장한다고 적지 않았다 — **검증 3규칙이 이 컬럼 없이는 성립하지 않는다.** DB 도메인 문서 반영이 필요하다
- **통합 실패와 타임아웃을 화면에서 같은 배너로 합쳤다**(S008-OQ-4). 구분은 job 의 `errorCode` 에만 남는다
- **「되돌리기」를 뺐다**(S008-OQ-1). 회의록에 변경 이력이 없어(DEC-003 §6) 되돌릴 근거가 없다 — 필요하면 이력 정책이 먼저다
- **「상세 설명은 비우면 배치가 채운다」의 종료 후 처리**를 캡션 덧붙이기로 정했다(S008-OQ-5)
- **회의 상세 드로어의 캘린더 쪽 진입 규격은 캘린더 그룹이 정한다**(S008-OQ-6). 이 work 는 드로어 자체와 ⤢ 승격까지만 만든다
- **`GET /api/meetings/{id}` 에 `counts` 가 붙는다** — SPEC-006 §4 의 응답 예시에는 없고 SPEC-008 이 추가했다. 두 spec 의 상세 응답이 **한 계약**임을 코디가 확인해야 한다
- **회의 첨부의 자료함 갈래가 여전히 닫혀 있다**(WORK-006·007 과 같은 사유 — 문서함 work 대기)

## Related

- SPEC: SPEC-008 (frontmatter `links.specs`)
- Work: WORK-005 · WORK-006 · WORK-007 (선행) · 캘린더 그룹(회의 상세 드로어 재사용) · 문서함 work(첨부 실체화)
