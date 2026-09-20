# W1 프론트엔드 결과 보고 (WORK-001 Phase 7 + Phase 8 FE 회귀)

## 상태: done

## 1. 변경 파일 (13개, 전부 `frontend/` 안. backend·Makefile·docs 는 손대지 않았다)

| 파일 | 무엇 |
|---|---|
| `src/lib/api.ts` | `createDirectTask`(+`assignee_id`) · `createWorkRequest` · `assignTask` · `promoteMeetingTodo` 넷에 `Idempotency-Key` 헤더 필수 인자 추가 |
| `src/lib/viewModels.ts` | `WorkRequest["state"]` union 에 `assigned` 추가 |
| `src/lib/labels.ts` | `workRequestStateLabel/Tone` 에 `assigned` = 「즉시 배정됨」 · `meetingScreen.promoted(title, assignee?)` |
| `src/features/work/WorkModals.tsx` | 생성 창 담당 필드·경로 결정·멱등 키·제출 잠금·문구, 요청 상세의 `assigned` 표시, 하위 업무 생성 키, 담당자 변경 문구 |
| `src/features/work/MyWorkPage.tsx` | 생성 결과 갈래를 문구가 아니라 `onCreated` 의 `assignedToOther` 로 고름 · 「내가 지정한 업무」 부제 문구 |
| `src/features/meetings/MeetingDetailPage.tsx` | 승격에 멱등 키 전달 · 승격 토스트가 누구의 업무가 되었는지 말함 |
| `src/shell/InboxRail.tsx` | 판단함 빈 상태 문구에서 「동료의 요청, 관리자의 배정」 제거 |
| 테스트 6개 | `CreateWork.test.tsx`(W1 11건 신규) · `labels.test.ts`(3건 신규) · `MyWorkPage.test.tsx`(2건 신규 + RailHost 가 머리 액션도 받도록) · `Subtasks`·`MeetingDetail`·`MeetingAfter`(계약 변경 반영) |

## 2. 구현 요약

### 담당 필드 (Phase 7 「생성 창에 담당 필드를 연다」)
- 기본값 **나**(`me`). 후보는 **envelope 이 허용한 경로의 목록만** 합친다 —
  `assignCandidates`(부르는 쪽이 `task.assign` 일 때만 채운다) ∪ `canCreateRequest ? assigneeCandidates : []`.
  같은 사람이 둘 다에 있으면 **한 번만** 서고 **managed 우선**이다.
- 합친 목록이 비면 **담당 줄 자체를 세우지 않는다**(`directTaskContract.fields` 에서 통째로 빠진다).
- `routeFor(ownerId)` 하나가 화면과 제출에 같은 판정을 준다 — 목록에 뜬 사람은 둘 중 한 경로로 반드시 보낼 수 있다.
  목록 밖 id 면 `null` 을 내고 **임의 fallback 없이** 「이 사람에게는 업무를 보낼 수 없습니다.」로 멈춘다.
- 경로: `self` → `POST /api/tasks`(assignee_id 없음) · `horizontal` → `POST /api/tasks` + `assignee_id` ·
  `managed` → 기존 `POST /api/tasks/assign`. **API 실패 시 다른 경로로 자동 재시도하지 않는다.**

### 멱등 키 (Phase 7 「생성 의도 하나에 키 하나」)
- `submitAttempt = useRef<{fingerprint, key, route}>`. payload 지문이 그대로면 재시도·연타가 **같은 키**를 다시 보내고,
  쓴 것이 달라지면 **새 의도**라 새 키를 받는다. 경로도 attempt 에 박아 **재시도 중 endpoint 가 바뀌지 않는다**.
- 성공하면 attempt 를 비운다 — 그다음 만드는 업무는 새 키다.
- `submitting` ref 로 같은 tick 의 두 번째 제출을 막고, 단추는 「만드는 중…」으로 비활성이 된다.
- 하위 업무 생성(`createDirectTask(parent_task_id)`)도 같은 규칙으로 키를 싣는다 — 제목이 같으면 같은 키.
- 회의 승격은 **두 층**임을 코드에 적었다: 여기 싣는 키는 생성 층이고, 같은 후보가 두 번 서지 않는 것은
  서버의 후보 잠금이 따로 진다.

### 문구 (Phase 7 「수락 문구를 전부 걷는다」)
- 담당이 남: 「{이름}에게 보냅니다. **상대의 수락 없이 바로 그 사람의 업무가 됩니다.**」
- 담당이 나: 「내가 할 업무를 만듭니다. 바로 내 업무에 들어갑니다.」
- 요청 갈래: 「상대의 수락 없이 바로 그 사람의 업무가 됩니다. 희망 기한을 함께 보낼 수 있습니다.」
- 토스트: 「'{제목}' 업무가 {이름}의 업무가 되었습니다. 수락을 기다리지 않습니다.」(세 경로 + 회의 승격 모두)
- 요청 갈래 상태 줄: 「판단 대기」 → **「즉시 배정됨」**(`state="assigned"`).
- 「수락하면 그 사람의 업무가 됩니다」류를 걷은 자리: 생성 창 머리 문구 2곳 · 참고 업무/시작 단계 안내 2곳 ·
  담당자 변경 알림 1곳 · 「내가 지정한 업무」 부제 1곳 · 판단함 빈 상태 1곳.
- **과거 행의 읽기는 그대로 둔다** — `WorkRequestDetailDrawer` 의 수락·거절 판단 UI 와 「수락하면 바뀌는 것」은
  `isOpen = pending || negotiating` 으로만 서므로 신규 `assigned` 행에는 뜨지 않는다.
  「내가 지정한 업무」 표의 `수락 상태` 칸(수락 대기/수락됨/거절됨)도 과거 배정 행을 위해 유지했다.
- `assigned` 전용 줄을 더한 곳: 「생성된 업무」 값(「수락 후 생성됨」 대신 「생성됨」) · 「결과」 문장.

### 승인자
- 생성 창에 **승인자 필드를 만들지 않았다**. `approver_id` 를 보내는 코드도 없다(테스트가 부재를 단언한다).

## 3. 검증 결과 (수치)

| 명령 | 결과 |
|---|---|
| `cd frontend && npx tsc --noEmit` | **0 에러** (exit 0) |
| `make frontend-test` (`npx vitest run`) | **Test Files 50 passed (50) · Tests 638 passed (638)** |

- 신규 테스트 **16건** (CreateWork 11 · labels 3 · MyWorkPage 2). 기존 실패 5건은 계약이 바뀐 문구·시그니처라
  기대값을 W1 계약으로 갱신했다(테스트를 지우지 않았다).
- **주의 — `make frontend-test` 는 exit 1 로 끝난다.** 테스트는 638건 전부 통과하지만 vitest 가
  `WorkViews.tsx:542` 의 drag 핸들러에서 나는 unhandled `TypeError: Cannot set properties of undefined
  (setting 'effectAllowed')` (jsdom 이 `dataTransfer` 를 주지 않는다) 때문에 비정상 종료한다.
  **HEAD 원본 파일로 되돌려 같은 파일을 돌려 확인했다 — 내 변경 이전부터 나던 것이다.**
  `WorkViews.tsx` 는 이번 범위 밖이라 손대지 않았다. 코디 `make verify` 가 여기서 막히면 이 사실을 보라.
- 사용자 지시대로 브라우저/acceptance E2E 는 돌리지 않았다. `npm run build` 도 코디 몫이라 돌리지 않았다.
- `frontend/node_modules` 가 없어서 `npm install` 을 먼저 했다(워크트리 로컬, 커밋 대상 아님).

### Phase 7 검증 항목별 증거

| Phase 7 검증 | 증거 |
|---|---|
| 타인 지정 생성 → 토스트가 누구의 업무가 되었는지 말한다 | `CreateWork.test.tsx` 「수신 후보에게 보내면 POST /api/tasks 에 assignee_id 를…」 |
| 화면 어디에도 「수락」 대기 문구가 없다 | 같은 파일 「화면 어디에도 「수락」 대기 문구가 남아 있지 않다」 (모달 전체 textContent 정규식) |
| 보낼 수 있는 사람이 없으면 담당 필드가 안 뜬다 | 「보낼 수 있는 사람이 하나도 없으면 담당 줄 자체가 서지 않는다」 |
| 생성 창에 승인자 필드가 없다 | 「생성 창에 승인자 필드가 없다 — W2 에서 완료 경로와 함께 연다」 |
| 제출 연타로 두 건이 만들어지지 않는다 | 「제출 단추를 연타해도 한 번만 나간다」 (3연타 → 호출 1회 + 단추 disabled) |
| 실패 재시도 = 같은 키 / 새 의도 = 새 키 | 「실패한 제출을 그대로 다시 누르면 «같은 키» 다」 · 「쓴 내용을 고쳐 다시 보내면 … «새 키»」 |
| 재시도 중 endpoint 가 안 바뀐다 | 「담당을 바꿔 다시 보내면 경로도 키도 새로 잡는다」 |
| overlap 에서 managed 우선 | 「두 목록에 다 있는 사람은 기존 관리자 배정 경로로 간다」 |
| 담당 기본값 나 · 후보 합집합 중복 제거 | 「담당 기본값은 나이고, 후보는 배정 후보와 수신 후보를 겹치지 않게 합친다」 |
| `assigned` 타입·라벨 | `labels.test.ts` 3건 (「즉시 배정됨」 · 과거 다섯 값 불변 · 톤 6값) |
| 판단함 빈 상태 문구 | `MyWorkPage.test.tsx` 「빈 상태 문구에서 「동료의 요청, 관리자의 배정」이 빠지고…」 |
| 성공 후 목록 즉시 반영 | `MyWorkPage.test.tsx` 「남의 업무가 되면 「요청·배정」으로 옮겨 서고…」 |

## 4. 계약 준수 / BE 실코드 대조

`w1-fe-api-clarification.md` 6개 항을 그대로 따랐고, **BE 가 워크트리에 올린 실제 코드와 대조했다**:

| 계약 | BE 실코드 | 일치 |
|---|---|---|
| `POST /api/tasks` + `assignee_id` | `http.py:1261-1284` `create_task(CreateTaskRequest, Header(alias="Idempotency-Key"))`, `assignee_id=request.assignee_id` | ✅ |
| 헤더 이름 `Idempotency-Key` | 네 라우트 모두 (`:1264` tasks · `:1387` tasks/assign · `:1748` work-requests · `:743` promote) | ✅ |
| `title`/`description` 유지 | `create_task` 가 `title`·`description`·`start_date`·`due_date`·`checklist`·`reference_task_ids`·`parent_task_id`·`project_id` 를 그대로 받는다 | ✅ |
| 후보 endpoint 유지 | `/api/work-request-assignee-candidates`(`:1987`) · `/api/task-assignment-candidates`(`:1394`) 둘 다 그대로 | ✅ |
| 출처 상태 `assigned` | `work_tasks.py:955` `state="assigned"` | ✅ |
| 응답 shape | `TaskMutationResult`·`TaskAssignmentResult`·`WorkRequestMutationResult` 전부 기존 타입 — FE 파싱 변화 없음 | ✅ |

**충돌 없음.** 임의 호환 fallback 을 만들지 않았다.

- 권한은 envelope 로만 판단한다 — `canCreateTask`/`canCreateRequest`/`canAssignTasks` 와 부르는 쪽이 채운 후보 목록이
  전부다. kind·status 로 command 를 추론하지 않았다.
- `api.ts` 밖에서 `fetch` 하지 않았다. 새 컴포넌트를 만들지 않았다(기존 `TaskDraftFields`·`Select`·`Empty`·`Modal` 재사용).
- 문구는 전부 기존 자리(컴포넌트 상수 · `labels.ts`)에 두었고 임의 hex 를 쓰지 않았다.

## 5. 미결 · 주의점 · W2 인수인계

1. **생성 창에 「업무 | 요청」 세그먼트가 그대로 남아 있다.** W1 이후 두 갈래가 같은 결과(즉시 배정)를 내므로
   사람에게는 중복으로 보인다. SPEC-001 U-6 의 **「한 창, 한 번의 생성 명령」** 은 업무 페이지 축 개편 work 의
   범위라 이번에 걷지 않았다. 회의록 승격이 `canCreateTask={false}` + 요청 모드로 이 자리를 쓰고 있어,
   세그먼트를 지우면 승격 경로를 함께 옮겨야 한다.
2. **`WorkRequestDetailDrawer` 의 판단 UI 는 과거 행 전용으로 남겼다.** `assigned` 행에는 뜨지 않지만 코드는 살아 있다
   (WORK-001 「과거 수락 항목의 읽기 경로 코드를 지우지 않는다」). W2 상태 모델 전환 때 다시 볼 자리다.
3. **`onCreated(notice, outcome)` 2번째 인자가 새로 생겼다** — `{ assignedToOther: boolean }`.
   목록 갈래를 알림 문구 문자열 매칭으로 고르던 것을 걷어냈다. W2 에서 완료·승인 갈래가 늘면 여기에 얹으면 된다.
4. **W2 가 소비할 FE 경계**: `WorkRequest.state === "assigned"` 가 「판단 없이 선 출처」이고,
   `request.task_id` + `source_work_request_id` 기반 완료 승인은 현행 그대로 돈다.
   **승인자는 FE 어디에도 입력·표시가 없다** — 생성 창에 필드가 없고 `api.ts` 어느 함수도 `approver_id` 를 보내지 않는다.
   W2 가 완료 경로와 **같은 단위로** 열면 된다.
5. `frontend/src/lib/labels.ts` 의 `meetingScreen.promoted` 가 `(title, assignee?)` 2인자가 되었다 — 호출부는 한 곳.
6. **사용자가 볼 E2E 항목** (브라우저에서 직접 확인할 것):
   - 일반 구성원 계정으로 `[업무 만들기]` → 담당에서 동료 고르기 → 생성 → **상대 계정의 `내 업무` 에 `시작 전` 으로 즉시 뜨는지**,
     그리고 **상대의 판단함에 수락 카드가 생기지 않는지**.
   - 같은 생성 뒤 내 `요청·배정` 탭으로 자동으로 옮겨 서는지, 거기 상태가 「즉시 배정됨」인지.
   - 관리자 계정에서 조직 범위 안 사람 고르기 → 기존 배정 경로로 가고 역시 즉시 서는지.
   - 보낼 수 있는 사람이 없는 계정(수신 후보 0 · 배정 권한 없음)에서 **담당 줄이 아예 없는지**.
   - 네트워크를 끊고 `[생성]` → 실패 → 그대로 다시 `[생성]` → **업무가 한 건만 생기는지**.
   - 회의록 후속 후보 `[업무 생성]` → 승격 → 토스트가 누구의 업무가 되었는지 말하는지, 두 번 승격해도 한 건인지.


## 후속 검증 — 2026-09-16

태스크 task_c15ab5b79290 / ctx_7a4f200b1970 완료. MyWorkPage.test.tsx 드래그 fixture에 동일 DataTransfer 객체를 dragStart/dragOver/drop에 전달하고 effectAllowed=move 단언 추가. 제품 코드 변경·오류 무시·skip 없음. 코디가 실제 diff에서 기존 drop 단언 유지 확인.
워커 실행 보고: make frontend-test 연속 3회 exit 0, 638 passed, unhandled 0; tsc 오류 0. 앞선 부하 중 Checklist/MeetingList 타임아웃 관측도 있음. 최종 코디 make verify는 BE 테스트와 겹치지 않게 직렬 실행한다. E2E는 사용자 담당.


## F-1 수정 수령 — 2026-09-16

수평 대상은 시작일 필드 미노출·payload 미포함, effectiveStartDate로 지문·검증·전송 정렬. self/managed 날짜 지원 및 self 복귀 시 값 보존. 코디 소스 검색에서 적용 지점 확인, 최종 판정은 BE 수정과 묶어 reviewer 재검수 예정.
워커 실행 보고: 신규 회귀 7건, CreateWork 33/33, 전체 FE 645 passed·exit0·unhandled0, tsc0. diff는 frontend-f1-fix.diff. E2E 미실행.
