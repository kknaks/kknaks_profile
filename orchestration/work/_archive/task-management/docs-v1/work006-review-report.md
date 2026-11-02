# WORK-006 검수 리포트 — 회의록 목록 · 생성 · 시작 전

- 대상: `a7e1bd4`(백엔드 Phase 1~3) · `2d6319e`(프론트 Phase 4~6), 브랜치 `kknaksss/docs-v1`, 기준 `b757e2a`
- 방법: **read-only.** 코드·테스트를 고치지 않았고 테스트를 돌리지 않았다. 커밋 메시지의 「pytest 389 passed · vitest 163 passed」는 **검증하지 않은 워커 보고값**이다. 앱 창 실물 확인도 하지 않았다(발주 조건).
- 판정 기준: 정책(DEC-003·001·004·005) → 아키텍처(`backend/README` · `frontend/README` · `database/README` · `domains/meeting.md`) → SPEC-006 → WORK-006. 항목마다 `파일:줄` + 어긋난 문서 절을 단다. 근거를 못 대는 것은 싣지 않았다.

## 0. 판정 요약

| 등급 | 건수 | 한 줄 |
|---|---|---|
| **FAIL** | **1** | F-1 SPEC-006 §4 Case Matrix 가 요구하는 **에러 뒤 후속 동작(목록 갱신·재조회) 3곳 누락** — 프론트, 수정 규모 작음 |
| **WARN** | **5** | W-1 영역 사이 import(meetings→settings 3건 · tasks→settings 5건) · W-2 첨부 팝오버 `role` 강제 · W-3 `validation_error` 가 항상 제목 칸으로 · W-4 임의 글꼴 크기 10건 · W-5 `v2_not_available` 토스트 문구 미매핑 |
| **문서 공백** | **9** | §5 |

코디가 지정한 다섯 축은 전부 **PASS** 다 — 공용 컴포넌트 두 번째 구현 0건 · 기획·정책에 없는 18행이 화면에 0건 · 정책에 있는데 없는 것 0건 · 배지 문구 「다음 논의로」 · E2E 대체 테스트에 통과로 위장한 항목 0건. 상세는 §1.

## 1. 코디 지정 축

### 1-1. 공용 컴포넌트 재사용 — 두 번째 구현 유무

| 부품 | 판정 | 근거 |
|---|---|---|
| `DrawerFrame` 840 | **PASS** | 생성 드로어는 `overlay.openDrawer` + `renderHeader` 로 프레임 위에 얹힌다(`features/meetings/openMeetingDrawers.tsx:32-49`). `features/meetings` 안에 폭 리터럴 `840`·`w-[840px]` 0건(grep) · `static.test.ts:102` 가 같은 것을 검사 |
| `Selector` + 「+ 새 프로젝트로 추가」 | **PASS** | `components/shared/Selector.tsx` 하나. 접힌 36px 행 → [색 28][이름][추가] · 즉시 선택 · 실패 인라인 + 입력 유지 · `Esc` 복귀를 U-3 규격대로 고쳤다(`Selector.tsx:223-240` 주석 · `:298-329` · `:357-362` · `:391-451`). 업무 드로어는 `createErrorMessage` 한 줄만 더해 같은 부품을 쓴다(`features/tasks/components/TaskCreateDrawer.tsx:492-493`). `Selector.test.tsx` 5건이 U-3 규격 그대로 |
| 첨부 팝오버 360 (SPEC-003 U-7) | **PASS** (W-2 별도) | `components/shared/AttachmentPopover.tsx` 하나를 `MeetingCreateDrawer.tsx:331-348` · `MeetingAttachmentsTab.tsx:56-70 · :91-103` 이 그대로 쓴다. 회의용 사본 0건 |
| `Calendar` | **PASS** | `CalendarGrid` 한 벌 — `PeriodStepper` · `DueDateField` · `MeetingDateTimeField.tsx:17` 이 같은 것을 import |
| `ItemRow` | **PASS** | 회의 첨부 행은 `AttachmentList` → `ItemRow` 를 지난다(`AttachmentList.tsx` diff L94-95 · `ItemRow.tsx` h44 · 테두리 없음 · `px-4` · `border-row-divider`). 단 SPEC-006 U-7 의 행 규격 문장과 어긋난다 → 문서 공백 G-6 |
| `EmptyState` · `StatusDot` · `TypeBadge` · 팔레트 | **PASS** | `EmptyState` 5곳 · `TypeBadge` 가 유형 배지(`MeetingRow.tsx:108`, `data-color-token` 경유) · 인라인 hex 0건(grep · `static.test.ts:45`) |
| `V2Gate` | **PASS** | 드롭 영역 2곳 모두 `V2Gate` 하나 아래(`MeetingCreateDrawer.tsx:321` · `MeetingAttachmentsTab.tsx:117`). `disabled` 흩뿌림 0건 |
| `MeetingTopBar` 한 파일 | **PASS** | `find -iname '*TopBar*'` → `MeetingTopBar.tsx` 하나. `waiting` · `headline` 두 변형이 한 파일(`MeetingTopBar.tsx:20-27`) · `static.test.ts:87` |
| `isEnterSubmit()` | **PASS** | `lib/keyboard.ts` 하나를 4곳이 import(`MeetingCreateDrawer.tsx:39` · `AgendaInputBar.tsx:17` · `MeetingDateTimeField.tsx:20` · `Selector.tsx:31`). `isComposing`·`keyCode === 229` 재구현 0건 |
| `schedule_service` 소비 | **PASS** | 회의 갈래 `build_meeting_placement` · `sync_from_meeting` 을 **같은 파일**에 더했다(`service/schedule_service.py:148-188`). `meeting_service` 는 `check_overlap` · `sync_from_meeting` 을 부르기만 한다(`:305-311` · `:335-341` · `:395-401` · `:410-416`). 판정식 `start_at < :end AND end_at > :start` 는 `repository/schedule_repository.py:73-74` 한 곳(grep — `meeting_repository.py:181` 은 월 범위 필터라 다른 식). `schedule` INSERT/UPDATE/DELETE 는 `schedule_repository.py` 밖 0건. `tests/test_meeting.py:562` 정적 테스트가 같은 것을 고정 |
| `build_detail()` 1개 | **PASS** | `MeetingDetailDTO(` 생성은 `service/meeting_service.py:151` 한 곳(grep · `tests/test_meeting.py:533`). 상세·생성·PATCH·`/start`·안건 3·첨부 2 표면이 전부 이 함수를 반환(`:194` · `:343` · `:418` · `:441` · `:481` · `:520` · `:565`) |
| `_assert_allowed` 한 곳 | **PASS** | `service/meeting_service.py:84-103` 표 9행. SPEC-006 §4 상태별 허용 표와 **행·열이 일치**한다(아래 부록 A). `InvalidMeetingStatusError` 는 이 함수에서만 난다 |

### 1-2. 기획·정책에 없는데 화면에 있나 — SPEC-006 §7 18행

| §7 행 | 화면 | 판정 |
|---|---|---|
| 취소된 회의 행(L120~127) | `MeetingRow.tsx` — 상태 표기는 4종 + 통합 실패뿐(`:39-64`). 「취소」 문자열 0건 | 없음 |
| 「· 회의실 A」(L153·L361) | `MeetingPreviewPanel.tsx:83-86` 일시 범위만. 「회의실」 문자열은 주석에만 | 없음 |
| 「요약」 문단 + 「AI 생성」 배지(L167~174) | `MeetingPreviewPanel.tsx:149-151` 한 줄 바 하나. 「AI 생성」 0건 | 없음 |
| PNG 첨부 행(L222~226 · L1175~1188) | 첨부 `kind` 는 `doc \| link` 뿐(`types.ts:22`) | 없음 |
| 유형 고정 칩 3종(L466~468) | 셀렉터 하나, `kind === "meeting"` 필터(`MeetingCreateDrawer.tsx:128 · :227-238`) | 없음 |
| 「만들면 바로 회의 시작」 토글(L519~525) | 드로어 본문 5블록뿐(`:189-357`) | 없음 |
| 「회의 정보 수정」 버튼(L579·L687) | 헤더 우측은 `⋯` + 「회의 시작」(`MeetingScheduledPage.tsx:112-129`) | 없음 |
| AI 안건 생성 일체 — 「초안을 만들어 줍니다」 · 추천 칩 · 「새 안건 ▾」 · 전송 버튼(L607~633) | `AgendaEmptyState`(`MeetingAgendaList.tsx:129-149`) · `AgendaInputBar.tsx:46-81`(입력 + 「추가」). 「새 안건」 문자열은 `aria-label`(`MeetingCreateDrawer.tsx:290`)뿐이고 모드 칩이 아니다 | 없음 |
| 「MacBook Pro 마이크 · 내 목소리 등록됨」(L643~645) | 우 패널 스크립트 탭은 빈 상태 두 줄뿐(`MeetingScheduledPage.tsx:193-198`) | 없음 |
| 「최대 50MB」 · 드롭 문구 | 그리되 `V2Gate` 아래(`MeetingAttachmentsTab.tsx:117-121` · `MeetingCreateDrawer.tsx:321-331`) — §7 「그리되 V2Gate」 그대로 | 규격대로 |
| 「회의 중 작성」 · 「안건 1」 메타(L1172·L1354) | `attachmentMeta()` 는 크기·수정일·경로/도메인만(`MeetingAttachmentsTab.tsx:42-49`) · 파일 드로어 헤더에 안건 메타 없음 | 없음 |
| 「반복」·「외부」·「개인」 배지 | 배지는 동적 유형 이름·색뿐(`MeetingRow.tsx:108`) | 없음 |

테스트가 같은 것을 고정한다 — `MeetingCreateDrawer.test.tsx:108-126` · `MeetingScheduledPage.test.tsx:70-87` · `MeetingListPanel.test.tsx:114`.

**반대 — 정책에 있는데 없는 것**

| 정책 | 화면 | 판정 |
|---|---|---|
| 삭제 모달 경고 「v1 에는 복원 화면이 없습니다. 녹음 원본은 지워지지 않고 서버에 남습니다」(U-5 · DEC-003 §4·§6 · M-13) | `MeetingDeleteModal.tsx:19-21` 문안 3줄 그대로. 진입점 2곳(`MeetingsScreen.tsx:75` · `MeetingScheduledPage.tsx:70`). 드로어 먼저 닫음(`:28`) | 있음 |
| AI 한 줄 요약 바(U-8 · DEC-003 §1 표) | `MeetingTopBar variant="headline"` — `headline` null 이면 안 그린다(`MeetingPreviewPanel.tsx:149-151`) · 한 개 · 본문 첫 요소 · 말줄임(`MeetingTopBar.tsx:58`) | 있음 |
| `V2Gate` 토스트 「v2에서 제공됩니다」(DEC-003 §1 표) | `V2Gate.tsx:28` · 드롭 가로채기 `:468-472` · 테스트 3곳이 요청 0건을 fetch 스파이로 확인 | 있음 |
| 「추가」 버튼 병행(U-3·U-4 · [10]) | `MeetingCreateDrawer.tsx:303-312` · `AgendaInputBar.tsx:69-78` | 있음 |
| 상태 표기 「예정」·「기록 중」+dot·「생성중」·「통합 실패」(U-2) | `MeetingRow.tsx:39-64` | 있음 |
| 헤더 `⋯` 「삭제」(U-4) | `MeetingScheduledPage.tsx:214-242` | 있음 |
| 자동 저장 실패 — 토스트 + 행 실패 표시 + 「다시 저장」 · 자동 재시도 0(SPEC-002 U-7 · DEC-001 §7) | `useAgendaAutoSave.tsx:52-69` · `MeetingScheduledPage.test.tsx:149-184`(재요청 0건 · 「다시 저장」 정확히 1건) | 있음 |

### 1-3. 배지 문구 — DEC-003 §1 표

**PASS.** `MeetingAgendaList.tsx:35-39` — `next: "다음 논의로"`(`active` 「논의 중」 · `done` 「완료」). 이 목록은 미리보기 패널(U-8) · 시작 전(U-4)이 쓰고 「대기」 문자열은 `features/meetings` 코드에 0건(주석 제외, grep). `MeetingPreviewPanel.test.tsx:111` 이 「대기가 아니다」를 고정. 시작 전 안건은 `state=null` 이라 배지 자체가 없다(`:100-104`) — SPEC-006 §4 「시작 전 null」 그대로. 회의 중 「대기」는 WORK-007 몫.

### 1-4. `schedule_repository.py` 소프트 딜리트 회의 제외 — 업무 일정 영향

**영향 없음.** `repository/schedule_repository.py:42-53` `_inactive_meeting_source()` 는 `Schedule.source_type == 'meeting'` 을 첫 조건으로 갖는 상관 `EXISTS` 다. `source_type='task'` 인 행에서는 그 `EXISTS` 가 항상 거짓이라 `~_inactive_meeting_source()` 가 참이 되고, 업무 행의 판정은 기존 `_inactive_task_source()`(`:24-39`)만 좌우한다. 겹침 검사 밖의 `schedule` 읽기 경로(`upsert` · `delete_for_source` · `find_placement`)는 손대지 않았다. `GET /api/schedules` 는 아직 없다(`api/` 디렉토리에 `schedule_router` 없음)라 캘린더 조회 쪽 영향은 판정 대상이 아니다. 테스트 — `test_meeting_schedule.py:285 · :309 · :329 · :400`(업무↔회의 · 경계 접촉 · 고아 없음) · `:265`(지운 회의가 조회에서 빠지고 행은 남는다). `database/README.md` §3-3 「소프트 딜리트 — 행은 그대로, 조회가 원본을 조인해 거른다」 · 「겹침 검사 제외: 소프트 딜리트분」과 일치한다. WP L194 「수정하지 않는다」와의 어긋남은 코디 허용분이고 문서 공백 G-8 로만 남긴다.

### 1-5. 프론트 워커 확인 요청 2건 — 판정

**② `AttachmentPopover` 에 `role="reference"` 를 채운 것 → WARN(W-2). FAIL 아님.**

- SPEC-003 U-7(팝오버 UX 계약)에는 `role` 이 없다. `role` 은 SPEC-003 §4 **업무 첨부 API**(`POST /api/tasks/{id}/attachments { role, kind, … }` · Validation 「첨부 `role`」)의 필드다.
- SPEC-006 §4 `POST /api/meetings/{id}/attachments` 요청은 `{ kind, documentId | url, label }` 뿐이고 `role` 이 없다. 실제로 회의 쪽은 값을 받아 **버린다**(`MeetingAttachmentsTab.tsx:57-59` 주석 그대로 · `types.ts:195-199` `AddMeetingAttachmentInput` 에 `role` 없음). 서버로 `role` 이 나가지 않으니 계약 위반은 아니다.
- 「계약이 필수」는 **문서 계약이 아니라 `AttachmentPopover.tsx:28-32` 의 TS prop 계약**이다. `components/shared/` 는 「두 영역 이상이 쓰는 것」(FE §2 규칙 3)인데 한 영역(업무)만의 축을 필수 prop 으로 강제해 다른 영역이 가짜 값을 넣게 됐다.
- 정리 방향: 팝오버에서 `role` 을 뺀다. 업무 호출부(`TaskCreateDrawer` · `TaskDetailBody`)가 `onAddLink` 클로저에서 자기 `role` 을 닫아 넣으면 된다 — 팝오버는 `role` 을 읽지 않고 되돌려주기만 한다(`:59-64`).

**④ `features/meetings` → `features/settings` import 3건 → WARN(W-1). tasks 도 같다.**

- FE §2 규칙 4 「영역 사이 import 금지. 공유가 필요하면 `components/shared/` 나 `lib/` 로 올린다. **단 하나의 예외**: 업무·회의 상세/생성 드로어를 캘린더·회의록이 재사용」. 가져온 것은 `useWorkTypesQuery` · `useProjectsQuery` · `useProjectMutations`(`features/settings/hooks/useWorkSettings.ts`) · `inlineErrorMessage`(`features/settings/errors.ts`) · `useRowFailures`(`features/settings/useRowFailures.ts`) — **드로어가 아니다.** 예외에 해당하지 않는다.
- 같은 위반이 `features/tasks` 에 5건 있다: `TaskDetailHeader.tsx:38` · `TasksScreen.tsx:42` · `TaskCreateDrawer.tsx:40-41` · `hooks/useTaskFieldSave.tsx:30`. WORK-004·005 리뷰 리포트에는 지적이 없다(grep) — 그때 놓친 선례를 이번이 답습했다.
- 정리 방향(둘 다 한 번에): ① `useRowFailures` → `lib/`(자동 저장 실패의 소유자 — FE §3-5 「전 영역 공통 규격」이라 애초에 영역 것이 아니다) ② `inlineErrorMessage` → `lib/api/errors.ts`(코드→문구 매핑, 이미 `API_ERROR_CODE` 가 거기 있다) ③ 유형·프로젝트 조회/생성 훅과 `features/settings/api.ts` 의 그 두 자원 함수 → `lib/api/` 아래 한 파일(예: `lib/api/workSettings.ts` + `lib/hooks/useWorkSettings.ts`). `features/settings` 화면은 그것을 import 한다. 문서 쪽 대안(FE §2 규칙 4 에 「설정의 유형·프로젝트 조회 훅」 예외를 더하는 것)은 G-5 에 적었다 — 코디 선택.
- 덧붙여 `features/meetings/static.test.ts:132-136` ⑨ 는 `features/tasks` 만 검사한다. settings 를 못 잡는 검사라 W-1 을 통과시켰다.

코디가 이미 넘긴 5건(① PanelTabs Ink · ③ 드롭 영역만 V2Gate · ⑤ 22:30~23:30 · ⑥ V2Gate 드롭 가로채기 · ⑦ `onRemove` optional)은 지적하지 않았다. ①은 문서 공백 G-7 로만 남긴다.

### 1-6. E2E 를 대체한 테스트 — 정직성

**통과로 위장한 항목은 찾지 못했다.** 8개 테스트 파일을 전부 읽었고, 각 `it` 이 이름대로 실제 단언을 갖는다. 특히 WP 가 「네트워크 탭」으로 적은 것들은 fetch 스파이·MSW 본문 캡처로 옮겨졌다 —

| WP 항목 | 테스트 | 단언 |
|---|---|---|
| 생성이 요청 하나(Phase 5 네트워크 캡처) | `MeetingCreateDrawer.test.tsx:130-182` | `bodies.length === 1` + 본문 전체 `toEqual` |
| 드롭 시 요청 0건(Phase 5·6) | `:239-255` · `MeetingScheduledPage.test.tsx:236-250` · `V2Gate.test.tsx:91` | `fetchSpy.mock.calls.length` 전후 동일 |
| 자동 저장 실패 → 재요청 0건 · 「다시 저장」 1건(Phase 6) | `MeetingScheduledPage.test.tsx:149-184` | `calls === 1` 유지 후 클릭 → `2` |
| `/start` 뒤 스위치 전환 캡처(Done Criteria) | `:278-297` | 플레이스홀더 문구 등장 · `push` 미호출 |
| 칩 숫자 불변(Phase 4) | `MeetingListPanel.test.tsx:58` | — |
| 상태 표기 4종 · 한 줄 요약 유무 | `:88` · `MeetingPreviewPanel.test.tsx:40-76` | — |
| 캘린더 임시 진입(Phase 6) | `MeetingCreateDrawer.test.tsx:101-106`(`initial` prop) | — |
| 정적 검사 7종 | `static.test.ts` ①~⑨ | grep 을 테스트로 고정 |

워커가 보고한 **「실물 확인 필요」 목록 자체는 코디 인박스(worker_done 본문)에만 있어 이 워크트리·`orchestration/work/docs-v1/` 어디에도 파일로 없다.** 그래서 목록의 정직성은 아래 **내가 도출한 목록과 코디가 대조**해야 한다. 테스트로 덮이지 않아 실물 확인이 남아야 하는 것 —

1. **반응형 1280~1439** — 사이드바 숨김·햄버거 · 목록 좌 400 · 시작 전 우 400 · 드로어 전체화면 + 2열→1열. 모든 테스트가 `setViewport(1600)` 이고 1280 대 케이스가 없다(`DrawerFrame.test.tsx` 는 WORK-004 것)
2. **셀렉터에서 만든 프로젝트가 설정 화면 목록에도 있다**(Phase 5 검증) — 설정 화면을 그리는 테스트 없음
3. **업무 생성 드로어 캡처**(Phase 5 · Open Issues 「업무 드로어 쪽 캡처도 함께」) — `Selector.test.tsx` 와 tasks 테스트 통과가 대신하나 캡처는 없다
4. **`alembic downgrade -1 → upgrade head` 왕복**(Phase 1 검증 첫 항목) — 테스트 없음. `downgrade()` 는 있다(`0005_meeting_domain.py:355-382`)
5. **삭제 후 캘린더에서 사라진다**(U-5 · Acceptance) — 캘린더 화면·`GET /api/schedules` 가 없어 실화면 불가. 백엔드 `test_meeting_schedule.py:265` 가 조회 제외를 대신
6. 칩 가로 스크롤(스크롤바 숨김) · 선택 행 색 · dot 광륜 같은 **시각 규격** — 픽셀 테스트를 만들지 않는 규약(FE §11)이라 실물 몫
7. 달 이동 후 **새로고침에서 그 달 유지**(Phase 4) — URL 갱신은 테스트(`MeetingsScreen.test.tsx:84`)가 보나 새로고침 자체는 실물

워커 목록에 위 1~5 가 빠져 있거나 「테스트로 덮었다」로 적혀 있으면 그때 FAIL 로 올리면 된다.

## 2. 네 층 판정 — 지적

### FAIL

**F-1. Case Matrix 의 에러 뒤 후속 동작이 3곳 빠졌다** — SPEC-006 §4 Case Matrix · 프론트

| 코드 | Case Matrix 프론트 출력 | 코드 | 빠진 것 |
|---|---|---|---|
| `invalid_work_type` | 인라인 「…다시 골라 주세요」 **+ 목록 갱신** | `features/meetings/errors.ts:37-43` 인라인만 · `MeetingCreateDrawer.tsx:173-181` 은 `setErrors` 뿐 | `['workTypes']` 무효화 없음 → 삭제된 유형이 셀렉터에 그대로 남는다 |
| `invalid_project` | 인라인 + **목록 갱신** | `errors.ts:44` · 같은 catch | `['projects']` 무효화 없음 |
| `not_found` (목록에서 삭제) | 목록: 토스트 **+ 갱신** | `MeetingsScreen.tsx:82-89` — `meetingInlineError` 가 `not_found` 에 `null` 을 돌려주므로 `inline?.toast` 가 거짓이라 `refresh()` 가 불리지 않는다 | 이미 지워진 행이 목록에 남는다 |

인라인·토스트 자체는 다 뜬다. 빠진 것은 「낡은 화면을 맞추는」 후속 한 줄씩이다(`invalidateQueries(['workTypes'])` · `(['projects'])` · `mutations.refresh()`). 상세 화면의 자식 404 는 재조회한다(`useAgendaAutoSave.tsx:42-46` · `MeetingScheduledPage.tsx:95`) — 목록 쪽만 빠졌다. 참고로 `FE §3-3` 무효화 표에 유형·프로젝트 목록 무효화 행이 「유형·프로젝트 변경」에만 있어 이 자리를 표로 뒷받침하려면 G-4 도 함께 본다.

### WARN

**W-1. 영역 사이 import** — FE §2 규칙 4. `features/meetings/components/MeetingCreateDrawer.tsx:37-38` · `features/meetings/hooks/useAgendaAutoSave.tsx:26`, 그리고 `features/tasks` 5건(§1-5 ④). 정리 방향은 §1-5.

**W-2. 첨부 팝오버가 업무 전용 `role` 을 필수 prop 으로 강제** — FE §2 규칙 3 · SPEC-006 §4. `components/shared/AttachmentPopover.tsx:28-32`; 회의 쪽 가짜 값 `MeetingCreateDrawer.tsx:333` · `MeetingAttachmentsTab.tsx:58 · :92`. 정리 방향은 §1-5.

**W-3. `validation_error` 가 무조건 제목 칸으로 간다** — SPEC-006 §4 Case Matrix 「해당 컨트롤 실패 테두리 + 인라인 문구(… 「회의는 5분 이상 300분 이하여야 합니다」 · 「종료 시각은 시작보다 뒤여야 합니다」)」. `features/meetings/errors.ts:35-36` 은 `field: "title"` 고정이고 `MeetingCreateDrawer.tsx:177` 이 그 자리에 서버 `detail`(「입력값을 확인해 주세요」)을 그린다. 화면이 일시를 먼저 거르므로(`MeetingDateTimeField.tsx:42-51`) 정상 경로에서는 안 닿지만, 서버와 화면의 판정이 어긋나면(예: 시각 경계·서버 규칙 변경) 일시 오류가 제목 칸에 뜬다. 서버 응답에 필드 식별자가 없어 화면이 고를 수 없다는 점은 G-2 문서 공백이다 — 코드 쪽은 최소한 `field` 없이(폼 전체) 보여 오답 위치를 피해야 한다.

**W-4. 임의 글꼴 크기 `text-[NNpx]` 10건** — FE §5-1 「타이포 계단은 Tailwind 유틸 프리셋으로 고정하고 컴포넌트가 임의 크기를 쓰지 않는다」. `MeetingCreateDrawer.tsx:85`(18) · `:262 · :288`(11) · `MeetingAgendaList.tsx:84 · :101`(11) · `:141`(17) · `MeetingTopBar.tsx:54`(11) · `AttachmentFileDrawer.tsx:40-41`(10) · `:75`(17). 선례가 `features/tasks` 에 6건(`TaskPageHeader.tsx:70 · :75` · `TaskDetailHeader.tsx:73 · :550` 32px · `TaskDetailBody.tsx:1043` 10px) 있어 새 위반은 아니나 규칙은 문서에 있다. 11·17·18 은 시안 계단값이라 프리셋(`fontSize`)에 이름을 붙여 올리는 것이 규약에 맞다.

**W-5. `v2_not_available` 이 토스트 문구로 매핑되지 않는다** — SPEC-006 §4 Case Matrix 「`501 v2_not_available` → 「v2에서 제공됩니다」 토스트」. `features/meetings/errors.ts:52-53` `default: null` 이라 생성 드로어에서는 「회의록을 만들지 못했습니다」, 첨부에서는 「저장하지 못했습니다 · 첨부」로 뜬다. 정상 경로가 아닌 안전망이라 낮게 둔다.

### PASS — 층별 확인(근거만)

- **정책** — 소프트 딜리트·자식 하드 삭제(`meeting_repository.py:167-173` · `meeting_child_repository.py:118-125 · :270-280` · DB §0-1) · 녹음 원본 보존(`meeting_service.py:444-455` — `integrations/` import 0건 · `test_meeting.py:383-414` 가 `recording_path` 유지 확인 · M-13) · 첨부 두 갈래 + `doc` CHECK(`models/meeting.py:323-329` · M-17) · v2 게이트(§1-2) · 장소 없음(`schemas/meeting.py:63-70` `extra="forbid"` — `location`·`attendees` 를 거부, ERD 컬럼 없음) · 화자 이름 없음(`meeting_transcript.speaker_label` 만) · 자동 재시도 없음(`retry:false` 전역 · `useAgendaAutoSave` 는 「다시 저장」에만 재요청) · 상태 한 방향(`_ALLOWED["start"] = {scheduled}`) · `PATCH` 에 `status` 없음(`MeetingUpdateDTO` · `test_meeting.py:260`).
- **아키텍처(BE)** — service 에 `fastapi`·`schemas` import 0건(grep · `test_meeting.py:525`) · repository 가 dto 만 반환 · `commit()` 0건 · `except Exception` 0건 · `Query(alias=…)` 손으로 명시(`meeting_router.py:49-54`) · `T | Unset` + `model_fields_set`(`schemas/meeting.py:168-181`) · 트랜잭션은 요청 하나(원본 쓰기 → `sync_from_meeting` 같은 세션) · `require_account` 라우터 단위(`:32-36`) · 남의 것 404(`_require_meeting` · `test_meeting.py:496`) · 상세에 `recording_path`·`ai_session_id` 미노출(`MeetingDTO` 에 필드 없음) · enum 은 `dto/enums.py` `StrEnum` + varchar CHECK(G-3) · 인덱스·부분 UNIQUE 가 `database/README.md` §4 표와 일치(`(account_id,start_at) WHERE deleted_at IS NULL` · `(account_id,status)` · `uq_meeting_agenda_human_active` · `uq_meeting_attachment_meeting_id_document_id` · `uq_meeting_line_source_{human,ai}_line_id`) · `document_id` FK 없음(WP 임시 계약).
- **아키텍처(FE)** — 동적 세그먼트 0 · 두 `page.tsx` 모두 `"use client"` · 쿼리 파싱은 `useMeetingsViewParams` 하나 · `fetch` 직접 호출 0(`api.ts` 는 `apiFetch`) · 캐시 키는 `queryKeys` 경유 · 무효화는 §3-3 표대로(생성·삭제 → `['schedules']` 포함, `useMeetingMutations.ts:42-47 · :85 · :97`) · 낙관적 갱신은 안건 제목만(`:110-136`) · `Sheet`/`Dialog` 직접 import 0 · hex 0 · `new Date()` 컴포넌트 0(변환은 `lib/datetime.ts:283-417`) · `localStorage` 0 · `retry:false` · 오버레이는 `openDrawer`/`openConfirm`(드로어 위 모달 금지 — 삭제 모달이 먼저 닫는다).
- **SPEC-006 §4** — API 11 표면(`meeting_router.py`) · 목록 `{ items, total, projectCounts }` 와 `total` 필터 후/`projectCounts` 필터 전(`meeting_service.py:254-281` · `test_meeting.py:415`) · `projectId=none`(`:38-40 · :69-74`) · `MeetingDetail` 필드 소유 표 전 필드 + `ai`·`merged` 항상 `[]`(`_build_tracks`) · 파생값 5종 서버 계산 · `recordingStartedAt` 한 UPDATE(`meeting_repository.py:145-164`) · 자식 쓰기 → `MeetingDetail` 전체 · 삭제 204 · 없는 자식 404(`test_meeting_children.py:164`) · 안건 `track='human'` · `orderIndex` 마지막+1 · `state=null` · 첨부 `link` 검증(`http/https` · `label` ≤100 · 비우면 URL 이 이름) · 같은 `documentId` 재첨부 행 유지(`_create_attachment`) · 일시 둘 함께(`update_meeting:364-366`) · 길이 5~300 · 겹침은 원본 쓰기 앞(`:305-311`) · 상태별 허용 표 9행 일치(부록 A) · Case Matrix 11행 대조(부록 B — F-1·W-3·W-5 제외 일치).
- **SPEC-006 §2 U-1~U-8** — 월 스테퍼 `?month=` · 첫 진입 최신 행 선택(`MeetingsScreen.tsx:37-43`) · 생성 직후 새 행 선택(`:66-73`) · 삭제 후 다음 행(`:75-91`) · 칩 단일 선택 · 정렬 즉시 반영 · 빈 상태 2종 문구 그대로 · 조회 실패는 빈 목록 아님(`MeetingListPanel.tsx:95-104`) · 첫 로딩만 스켈레톤(`:86-90 · :93`) · 행 클릭=선택 / 더블클릭=상세 · 컨텍스트 메뉴 「열기」/「삭제」 비활성(`MeetingContextMenu.tsx:25-27`) · 드로어 제목 포커스·제출 조건·기본값·유형 기본 「미팅·회의」·안건 행·첨부 목록 행·「자료함에서 선택」 30px · 시작 전 헤더 서브 문구·상태 바·좌우 탭 dot 색·AI 탭 빈 상태·입력 바 캡션·「첨부 파일 n」 0이면 숫자 생략 · 파일 드로어 헤더/탭(본문 스텁은 WP 허용) · 미리보기 헤더 일시 범위·「상세보기」·상태별 본문 5행 · 반응형 클래스(`w-[400px] wide:w-[500px]` · `wide:w-[464px]` · `grid-cols-1 wide:grid-cols-2`).
- **WP 범위** — `app/back` · `app/front` 밖 변경 0. `schedule_repository.py` 1건은 코디 허용. Phase 4~6 이 만든 파일이 WP Code Surface 표와 일치하고 `layout.tsx` 는 만들지 않았다(목록 헤더를 `MeetingsScreen` 이 그린다 — 라우트 껍데기 규칙과 충돌 없음). 범위 밖 기능(검색·반복·장소·회의 중/종료 후 화면) 0건 — `recording`/`generating`/`ended` 는 플레이스홀더(`MeetingStatusPlaceholder.tsx`).

## 3. 가장 심각한 3건

1. **F-1** — 에러 뒤 목록 갱신·재조회 3곳 누락. 계약(Case Matrix) 미충족이라 재발주 대상이나 수정은 세 줄이다.
2. **W-1** — 영역 사이 import 8건(meetings 3 · tasks 5). 규약 위반이 두 영역에 굳어지기 전에 `lib/` 로 올려야 한다. 회의 중·종료 후 화면(WORK-007·008)이 같은 훅을 또 가져오면 세 영역이 된다.
3. **W-2** — 공용 팝오버의 `role` 강제. 작은 문제지만 「공용은 두 영역 이상의 공통 부분만」이라는 원칙이 첫 회의 화면에서 이미 흔들린 자리다. W-1 과 함께 한 번에 정리하면 된다.

## 4. 부록

### A. 상태별 허용 표 대조 — SPEC-006 §4 vs `meeting_service.py:84-94`

| 동작 | SPEC | 코드 `_ALLOWED` | 일치 |
|---|---|---|---|
| `/start` | S | `{S}` | ✔ |
| PATCH 제목·유형·프로젝트 | S · E | `{S,E}` | ✔ |
| PATCH 일시 | S · E | `{S,E}` | ✔ |
| 안건 추가 | S · R | `{S,R}` | ✔ |
| 안건 제목 수정 | S · E | `{S,E}` | ✔ |
| 안건 상태 변경 | R | `{R}` (schema 는 WORK-007 이 연다) | ✔ |
| 안건 삭제 | S | `{S}` + 사람 트랙 + 줄 0건 | ✔ |
| 첨부 추가·제거 | S · R · E | `{S,R,E}` | ✔ |
| DELETE | S · E | `{S,E}` | ✔ |

테스트 — `test_meeting.py:324-382` · `test_meeting_children.py:115-162 · :298`.

### B. Case Matrix 11행 대조

| 코드 | 백엔드 | 프론트 | 판정 |
|---|---|---|---|
| `validation_error` | 422 `_INVALID_INPUT` + schema `extra="forbid"` · 줄바꿈 거부 | 인라인 — 항상 제목 칸 | W-3 · G-2 |
| `invalid_work_type` | 422, `kind≠meeting`·삭제·남의 것 | 인라인 ✔ · 목록 갱신 ✗ | F-1 |
| `invalid_project` | 422 | 인라인 ✔ · 목록 갱신 ✗ | F-1 |
| `schedule_overlap` | 409, 원본 미변경(`test_meeting.py:274`) | 토스트 + 일시 테두리 + 드로어 유지 ✔ | ✔ |
| `invalid_meeting_status` | 409 `_assert_allowed` | 토스트 + 상세 재조회 ✔(시작·안건·첨부·삭제) | ✔ |
| `unsupported_file_type` | **닿지 않는다** — `doc` 은 `validation_error`(WP 임시 계약) | 문구만(`errors.ts:50`) | G-3 |
| `not_found` | 404, 남의 것 동일 | 상세 ✔ · 자식 ✔ · **목록 갱신 ✗** | F-1 |
| `duplicate_name` · `invalid_color_token` | SPEC-002 | 셀렉터 행 아래 인라인 + 입력 유지 ✔(`Selector.tsx:325-328`) | ✔ |
| `v2_not_available` | 서버에 없음(정상) | 문구 미매핑 | W-5 |
| 자동 저장 실패 | 서버 재시도 없음 | U-7 규격 ✔ | ✔ |
| 5xx · 네트워크 | 전파 | 목록·상세 「다시 시도」 · 빈 목록 대체 없음 ✔ | ✔ |

### C. Acceptance 22개 — 확인 경로

| # | 항목 | 경로 |
|---|---|---|
| 1 | 스테퍼 + 이번 달 + 최신 행 선택 | `MeetingsScreen.test.tsx:62` |
| 2 | 「미정」 칩 · 숫자 불변 | `MeetingListPanel.test.tsx:58` |
| 3 | 드로어 포커스·기본 유형·기본 일시 | `MeetingCreateDrawer.test.tsx:88` |
| 4 | 종류=미팅만 · 칩 없음 | `:108` |
| 5 | 새 프로젝트 즉시 선택 | `Selector.test.tsx:54` (설정 화면 반영은 실물) |
| 6 | 제목+유형+일시 생성 · 새 행 선택 · 안건·첨부 미리보기 | `MeetingCreateDrawer.test.tsx:130` + `MeetingsScreen.tsx:66-73`(코드) — 생성 후 선택은 화면 테스트 없음, 실물 권장 |
| 7 | 겹침 토스트 · 드로어 유지 · 경계 접촉 통과 | `:184` · BE `test_meeting_schedule.py:329` |
| 8 | 301분 거부 | `:202` · BE `test_meeting.py:123` |
| 9 | 토글 없음 | `:119` |
| 10 | 시작 전 상태 바 · 없는 것 | `MeetingScheduledPage.test.tsx:70` |
| 11 | 입력 바 · Enter · 「추가」 | `:98` |
| 12 | 인라인 편집 · 실패 규격 | `:126 · :149` |
| 13 | 첨부 md·링크 · 파일 드로어 · 자료함에서 열기 | 링크 갈래만 `:209` — md·드로어 본문·「자료함에서 열기」는 문서함 work(WP Done Criteria 대체 확인) |
| 14 | PDF 드롭 요청 0 | `:236` |
| 15 | 회의 시작 → 스위치 · 「기록 중」 dot · 삭제 비활성 | `:278` · `MeetingsScreen.test.tsx:125` |
| 16 | 삭제 모달 문안 · 목록·캘린더 제거 · 녹음 유지 | `:254` · `MeetingsScreen.test.tsx:96` · BE `test_meeting.py:383` — 캘린더는 실물 |
| 17 | 캘린더 「+ 새 일정」 같은 드로어 | `MeetingCreateDrawer.test.tsx:101`(대체) |
| 18 | 캘린더 드래그 → 목록 일시 변경 | BE `test_meeting.py:229`(PATCH 대체) |
| 19 | 종료 회의 요약 바 한 개 · 셋째 줄 동일 · 통합 전 없음 | `MeetingPreviewPanel.test.tsx:40 · :60` |
| 20 | 회의실·AI 생성·취소 행 없음 | `MeetingListPanel.test.tsx:114` |
| 21 | 없는 회의록 · 리다이렉트 없음 | `MeetingScheduledPage.test.tsx:317` |
| 22 | 1280~1439 반응형 | **실물 확인 필요** |

## 5. 문서 공백 — 지적이 아니라 문서가 비어 있거나 서로 어긋난 자리

| ID | 어디 | 무엇 | 필요한 것 |
|---|---|---|---|
| **G-1** | SPEC-006 §4 Case Matrix | 안건 삭제에 **딸린 줄이 있을 때**의 에러가 없다. 코드는 `validation_error` 422 로 낸다(`meeting_service.py:541-542`). 시작 전에는 안 닿지만 WORK-008 편집 모드에서 같은 표면을 쓴다 | Case Matrix 에 행 추가(코드 확정 — `validation_error` 로 둘지 `invalid_meeting_status` 로 합칠지) |
| **G-2** | SPEC-006 §4 Case Matrix `validation_error` · `backend/README.md` §8-2 | 프론트 출력이 「해당 컨트롤」인데 응답 `{detail, code}` 에 **어느 필드인지가 없다.** 화면은 고를 수 없어 제목 칸으로 보낸다(W-3). SPEC-003 도 같은 구조다 | 응답에 `field`(또는 필드별 `detail`)를 싣든지, 「폼 전체 인라인」으로 계약을 낮추든지 — §8-2 응답 형태 결정 |
| **G-3** | SPEC-006 §4 · U-7 | 문서함 전 임시 계약(`doc` → `validation_error` · 팝오버 문서 세그먼트 스텁 · 파일 드로어 본문 스텁)이 **SPEC-003 L462 에는 각주로 있는데 SPEC-006 에는 없다.** 그래서 `unsupported_file_type` 행이 닿지 않는 상태가 문서상 보이지 않는다 | SPEC-003 L462 와 같은 각주를 SPEC-006 §4 Case Matrix 아래에 |
| **G-4** | `frontend/README.md` §3-3 무효화 표 | 「유형·프로젝트 변경 → `['workTypes']`/`['projects']`」만 있고, **`invalid_work_type`/`invalid_project` 응답을 받았을 때** 목록을 무효화하는 행이 없다. Case Matrix 는 「+ 목록 갱신」을 요구한다(F-1 의 문서 짝) | §3-3 표에 「422 `invalid_work_type`/`invalid_project` 수신 → 그 목록 무효화」 행 추가 |
| **G-5** | `frontend/README.md` §2 규칙 4 | 유형·프로젝트 조회/생성 훅과 자동 저장 실패 소유자(`useRowFailures`)가 **어느 층에 살아야 하는지**가 없다. 두 영역이 `features/settings` 에서 가져다 쓰고 있다(W-1). `lib/` 로 올리는 것이 규칙 4 문면이나, 「설정은 다른 영역에 유형·프로젝트를 제공하는 쪽」(DEC-001 §8)이라 예외를 둘 여지도 있다 | 규칙 4 에 자리 명시 — `lib/` 승격(권장) 또는 예외 추가 |
| **G-6** | SPEC-006 U-7 목록 행 · SPEC-003 U-7 · 코디 브리프 「ItemRow h44」 | U-7 이 「행 padding 11/12 · r10 · 1px `#EBEBEB` · **MD 타일 32**」로 자기 규격을 적었는데, 재사용을 강제한 `AttachmentList`/`ItemRow` 는 「h44 · 테두리 없음 · 22px 타일」이다. 코드는 후자를 따랐고(`AttachmentList.tsx` diff) `MdTile size=32`(`AttachmentFileDrawer.tsx:34`)는 목록에서 쓰이지 않는다 | SPEC-006 U-7 목록 행을 「SPEC-003 U-7 · `ItemRow` 규격 그대로」로 정정하거나, 32 타일이 정말 필요하면 `ItemRow` leading 슬롯 규격을 두 값으로 |
| **G-7** | `frontend/README.md` §5-2 | 「`--tm-ink` 를 쓰는 컴포넌트는 셋뿐 … 화면당 Ink 는 하나」인데 `PanelTabs`(코디 허용 ①)가 넷째이고, 시작 전 화면은 좌·우 패널 탭 둘 + 사이드바 = Ink 셋이다 | §5-2 목록에 `PanelTabs` 추가 + 「화면당 하나」를 「본문 탭 하나 + 패널 탭은 패널당 하나」로 정정 |
| **G-8** | DEC-003 §1 표 「안건 `next` 배지 문구」 · SPEC-006 §7 정합 #4 | DEC-003 은 「**회의 중·시작 전** = 대기」로 적었으나 SPEC-006 §4 는 시작 전 `state=null`(배지 없음)이라 「시작 전」 어휘가 공허하다. 또 SPEC-006 §7 「SPEC 간 정합 #4」는 여전히 「SPEC-008 「다음으로」 → **「대기」로 통일**」이라 §7 「닫은 것」의 확정(「다음 논의로」)과 **같은 문서 안에서 모순**된다 | DEC-003 §1 표에서 「시작 전」 삭제 · SPEC-006 §7 정합 #4 를 「「다음 논의로」로 통일」로 갱신 |
| **G-9** | WORK-006 Code Surface(`core/enums.py` · `MeetingAttachmentKind`) · Phase 1 L194 | 코드 관습은 `dto/enums.py`(`ScheduleSourceType`·`TaskStatus` 가 이미 거기) 이고 `AttachmentKind` 를 업무와 공유한다 — 워커가 맞게 골랐다. WP 가 적은 경로·이름이 관습과 다르다. L194 「`schedule_repository.py` 를 수정하지 않는다」도 SPEC-006 §4 「소프트 딜리트분 검사 제외」와 충돌한다(코디 허용분) | WP 표 경로를 `dto/enums.py` 로, `MeetingAttachmentKind` 를 「`AttachmentKind` 공유」로, L194 를 「`_inactive_meeting_source` 1건은 예외」로 정정. `backend/README.md` §4 트리에도 `dto/enums.py` 반영 |

부수 관찰(지적 아님): `schemas/meeting.py:42` URL 상한 2000 자는 SPEC-006 §4 Validation 에 없는 값이다(SPEC-003 도 같다). 필요하면 G-2 와 함께 §4 표에 적는다.
