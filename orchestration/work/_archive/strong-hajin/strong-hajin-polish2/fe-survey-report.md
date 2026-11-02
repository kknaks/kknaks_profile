# 고도화 2차 화면 전수조사

- 대상: `Strong_hajin/strong-hajin-polish2` @ `3d47a32` (origin/main, 1차 운영 반영 코드)
- 방식: 읽기 전용. 코드·테스트·빌드·서버 실행 없음. 경로는 따로 적지 않으면 `frontend/src/` 기준이다.
- 숫자는 `grep -rnoF <심볼>` 결과에서 `*.test.*` 를 뺀 값이다(§6).
- ⚠ 브리프가 시작점으로 준 `features/action/ActionTaskCard.tsx` 는 **AX 업무 초안 카드가 아니다.** 1차 3b 이후 초안 두 kind(`ax.task.create_self`·`ax.work_request.create`)는 `features/action/AxDraftCard.tsx` 가 그린다(`MessageList.tsx:308-315`). `ActionTaskCard` 는 그 밖의 `editor === "task"` 카드(예: `task.assign`)를 맡는다(`MessageList.tsx:316-322`).

---

## 0. 한 줄 요약

| 요청 | 한 줄 |
|---|---|
| E2E-1 | 카드 체크리스트 페이지는 `edit_contract.values.checklist` 를 읽어 줄마다 그린다(`AxDraftCard.tsx:197-201`). 값이 있으면 그려진다. 따라서 「없음」은 **데이터 몫**이다 — 서버가 초안 payload 를 그대로 values 로 싣는다(`backend …/platform/actions.py:1694-1697` · `modules/work/drafts.py:16-26`). 「수정」 모달은 초안 체크리스트를 미리 채우고(`AxDraftCard.tsx:437` → `WorkModals.tsx:4567`), 제출하면 그 값이 `draft.checklist` 로 confirm 에 실린다(`WorkModals.tsx:4867`). |
| E2E-2 | 모드는 `CreateWorkModal` 의 `axDraft` prop 이 있느냐로 갈린다(`WorkModals.tsx:4427`). 그 모드에서 하단 단추는 「등록」/「등록 중…」이다(`:5259`). 제출은 `confirm + draft` 로 바로 등록한다(`:4855-4890` → `AxDraftCard.tsx:424-427`). FE 에는 「확정 없이 초안만 고치는」 API 가 없다. 서버가 AX 초안에 내주는 명령도 `confirm`·`reject` 둘뿐이다(`backend …/modules/actions/policy.py:114-128`). 카드 값은 FE 가 들고 있는 스냅샷이 아니다. 대화를 다시 읽을 때마다 서버가 다시 만든 `edit_contract.values` 를 그린다. |
| E2E-3 | **원인**: 검정 덮어쓰기(`ax.css:670-673`)는 `:not(:disabled)` 에만 걸린다. 진행 중이라 비활성이 된 단추는 DS 규칙으로 돌아간다. 이때 `.scax-button:disabled`(`components.css:10`)와 `.scax-button--solid-primary:hover`(`components.css:14`)가 명시도 0,2,0 으로 같다. 그래서 **뒤에 오는 hover 가 이긴다** → 포인터가 단추 위에 있는 동안 `accent-strong` rgb(55,77,246) 파랑에 흰 글자로 보인다. `ActionProgressBatchCard`·`CommandConfirmationForm` 도 같은 구조다. 반면 `.action-task-card` 계열(`ActionTaskCard`·`ActionMeetingCard`)은 `ax.css:546`(0,4,0)이 회색으로 잡아 준다. |
| E2E-4 | 메타는 `.meta > .meta__left > (.meta__facts + p.origin-chip)` 구조다(`WorkModals.tsx:1960-2002`). `.meta__facts` 에는 아래 여백이 없고, `.origin-chip` 은 `margin:0 0 4px` 로 위 여백이 0 이다(`task-detail.css:101-104` · `screens-a.css:437`). 그래서 두 줄이 붙어 보인다. 링크는 **업무 자신이 아니라 그 업무를 만든 AX 초안(action item)** 을 가리킨다. 다만 링크 글자를 초안 payload 의 `title` 로 써서(`backend …/actions.py:1208-1214`) 업무 제목과 같아 보인다. 내 업무에서 누르면 판단 상세(`ActionItemDrawer`)가 열린다(`MyWorkPage.tsx:699-701`). 출처 배지는 이 한 자리뿐이고, 「회의에서 생성됨」 문구는 코드에 없다. |
| E2E-5 | 업무 날짜로 고칠 수 있는 필드는 `start_date`(시작 예정)·`due_date`(기한) **둘뿐**이다. 실제 시작 `started_at`·재개 `reopened_at` 은 타입에만 있고 어디에도 안 보인다. 실제 완료 `completed_at` 은 「완료 업무」 표의 「처리일」 한 칸에만 나온다. 상세의 「편집」 단추가 시작일·기한 입력칸을 열고, 실제 저장은 하단 「변경 저장」이 한다(`WorkModals.tsx:1904-1907, 2007-2031, 1818-1821`). 같은 `due_date` 가 화면마다 기한·마감일·…마감·희망 기한으로 불린다. 표시 형식도 `2026/10/06`·`2026.10.06`·`2026-10-06`·`10월 6일` 이 섞여 있다. |

---

## 1. E2E-1 AX 업무 초안 카드의 체크리스트 페이지가 「없음」

### 1-1. 카드 체크리스트 페이지가 읽는 필드
- **카드 컴포넌트**: `AxDraftCard`(`features/action/AxDraftCard.tsx:228`). 채팅에서는 `axDraftFromAction(action)` 가 null 이 아닐 때 이 카드가 그려진다(`MessageList.tsx:308-315`). 홈 판단 대기와 내 업무 「AX 제안」 칩은 같은 카드를 `AxDraftModal` 로 띄운다(`AxDraftCard.tsx:479-514`).
- **페이지 구성**: 네 장이다 — `["기본 정보","체크리스트","업무 연결","자료"]`(`labels.ts:1303`).
- **체크리스트 페이지**(`AxDraftCard.tsx:197-201`)
  - `const steps = list(values.checklist)` 로 읽는다.
    - `values` = `source.contract.values`(`:178`) = 서버 `edit_contract.values` 다.
    - `list()` 는 배열일 때만 문자열 배열을 돌려준다(`:108`).
  - `steps.length === 0` 이면 `{label:"", value:null}` 한 줄이 「없음」(`axDraftCard.none`, `labels.ts:1304`)으로 서고, 클래스는 `ax-draft-card__none` 이다(`:160`).
  - 아니면 항목마다 `{value: step, box: true}` 한 줄씩 그린다. `dd.ax-draft-card__step-line` 안에 DS `CheckboxBox checked={false}` 를 두고 항목명을 붙인다(`:155-157`).
  - 7줄을 넘으면 마지막 줄이 「외 N개」로 접힌다(`LINE_BUDGET = 7`, `:138, 145-148`).
- **카드 쪽 소스**
  - 채팅: `axDraftFromAction` 가 `action.edit_contract` 를 그대로 `contract` 로 쓴다(`:64-82`, `:75`).
  - 홈·칩: `axDraftFromEnvelope` 가 `item.edit_contract` 를 그대로 쓴다(`:85-99`, `:93`).
- **서버가 주는 값**(참고, BE 리포트가 정본)
  - `edit_contract.values` 는 서버가 action payload 를 `normalize_task_draft` 로 정규화한 값이다(`backend/src/ax_workspace/platform/actions.py:1694-1697`). 이 함수는 `TaskCreateInput.model_validate(...).model_dump()` 이다(`modules/work/drafts.py:16-26`).
  - 편집 필드 목록에는 `{"id":"checklist","type":"string_list","editable":True}` 가 갈래마다 들어 있다(`actions.py:1796-1802, 1822-1828, 2022-2028`).
  - MCP 생성 도구도 `checklist: list[str] | None` 을 받는다(`entrypoints/mcp.py:731, 748`; 요청은 `:378, 384`).
- **판정**: 화면은 `values.checklist` 에 문자열이 하나라도 있으면 그린다. 운영 초안에서 「없음」이 뜬 것은 그 값이 비어 있었다는 뜻이다(**데이터 몫**). AI 가 왜 비웠는지는 BE 리포트 몫이다.

### 1-2. 「수정」 모달이 체크리스트를 미리 채우나 / confirm draft 에 실리나
- **미리 채움 — 그렇다**
  - `AxDraftCard.tsx:437` 에서 `initial.checklist = list(contract.values.checklist)` 를 넘긴다.
  - 받는 쪽은 `CreateWorkModal` 의 `const [steps, setSteps] = useState<string[]>(initial?.checklist ?? [])`(`WorkModals.tsx:4567`)다.
  - 「체크리스트」 탭 판(`WorkModals.tsx:5500-5540`)
    - `fieldset.scax-field.cc-picker` 안의 `ul.checklist > li.scax-checklist__row` 다.
    - 줄마다 「빼기」 `Button variant="text" size="sm"` 이 있다.
    - 입력 `#new-task-step` 아래 「단계 추가」 `Button size="sm"` 이 있다.
- **confirm 에 실림 — 그렇다**
  - `axDraft` 갈래의 draft 는 `{...axDraft.baseValues, …, checklist: steps, …}` 다(`WorkModals.tsx:4861-4875`, `:4867`).
  - `axDraft.onSubmit(draft, stagedIds)`(`:4880-4883`) → `AxDraftCard.tsx:424-427` `onCommand(confirm.id, confirmPayload(draft, attachmentIds))` 로 이어진다.
  - payload 는 `{base_submission_version, draft, attachment_draft_ids?}`(`:276-280`)다.
- 비교: 카드의 「등록」(모달을 거치지 않음)은 `confirmPayload()` 로 **draft 없이** confirm 을 보낸다(`AxDraftCard.tsx:403`).

---

## 2. E2E-2 「수정」으로 연 새 업무 추가 모달의 「등록」

### 2-1. AX 초안으로 여는 경로와 모드 구분
- **여는 자리**
  - 카드 「수정」 `Button size="sm"`(아이콘 `pencil`)이 `setEditing(true)` 를 부른다(`AxDraftCard.tsx:388-401`).
  - 보이는 조건은 두 가지다.
    - `editable` = `state === "pending"` 이고 `contract.fields` 중 `editable` 이 하나라도 있을 때(`:257`).
    - `confirm` 명령이 있을 때(`:388`).
  - 그러면 `createPortal(<CreateWorkModal … axDraft={…} initial={…}/>, document.body)` 를 띄운다(`:409-453`).
- **모드 구분 = `axDraft` prop 의 유무 하나다**(타입 `WorkModals.tsx:4427-4448`)
  - `{kind, baseValues, actionId, materials, onSubmit, onMaterialsChange?, approverOptions?, error?}`
  - 일반 새 업무 추가와 갈리는 자리는 다음과 같다.

| 자리 | 파일:줄 | 일반 | `axDraft` 있음 |
|---|---|---|---|
| 갈래 초깃값 | `WorkModals.tsx:4463` | 권한·재요청으로 고름 | `axDraft.kind` 로 고정 |
| 머리 갈래 토글(`SegmentedControl` 「내 업무/요청 업무」) | `:5271-5283` | `canCreateTask && canCreateRequest` 면 섬 | 안 섬 |
| 창 제목 | `:5110` | `"새 업무 추가"` / `"새 업무 요청"` | 같음(갈래로만 갈림) |
| 결재자 후보 | `:5186-5188` | 참조자 + 담당 후보 | + `axDraft.approverOptions` |
| 창 안 오류 줄 | `:5291` | 없음(부르는 쪽 `onError`) | `axDraft.error` 를 `FieldMessage` 로 |
| 상위 업무 잠금 | `:5576` · `:5594` | `initial.parentTaskId` 가 있으면 잠금 | 잠그지 않음 |
| 자료 판 | `:5736-` · 업로드 `:4512-4540` | 생성 뒤 업로드 | 판단 항목 자료 초안(`stageActionMaterialFile/Link` · `discardActionMaterialDraft`)으로 바로 올림 |
| 제출 | `:4855-4890` | 갈래·경로별 생성 API | `axDraft.onSubmit(draft, stagedIds)` → confirm |
| 하단 주 단추 | `:5256-5260` | `"업무 추가"`/`"업무 요청 보내기"`(진행 `"만드는 중…"`) | **`"등록"`(진행 `"등록 중…"`)** |
| 주 단추 비활성 | `:5256` | `isWorking` · 요청인데 담당 후보 0 | + `axUploadPending` |

- **하단 단추 모양**: `Button variant="solid" tone="primary"` → `scax-button--solid-primary`(`components.css:13`, `accent` rgb(84,103,247))다.
  - 모달이 `document.body` 로 포털돼 `.scax-drawer--chat` 밖에 있다(`AxDraftCard.tsx:411, 452`). 그래서 채팅 서랍 검정 규칙(`ax.css:670`)이 닿지 않고 **DS 파랑 그대로**다. 운영에서 본 「파란 등록」이 이것이다.
  - 왼쪽 「닫기」는 `Button variant="text"` 다(`:5253-5255`).

### 2-2. 모달 「등록」이 부르는 함수·API와 성공 뒤 갱신
- **채팅 카드에서 연 경우**
  1. `CreateWorkModal.submit()` 의 axDraft 갈래(`WorkModals.tsx:4855-4890`) → `axDraft.onSubmit`
  2. → `AxDraftCard.tsx:424-427` `await onCommand(confirm.id, confirmPayload(draft, ids)); setEditing(false)`
  3. → `MessageList.tsx:312` `onDecide(action.action_id, action.version, command, payload)`
  4. → `App.tsx:354-376` `decideConversationAction` → `chat.decide`(`useConversations.ts:338-345`)
  5. → `decideAction`(`lib/api.ts:731-745`): `decision === "confirm"` 이면 `runActionCommand(actionId, "confirm", {expected_version, ...payload})`
  6. → **`POST /api/action-items/{id}/commands/confirm`**(`api.ts:1103-1119`)
- **성공 뒤** — `refreshProjections`(`App.tsx:343-352`)가 다음 셋을 `Promise.allSettled` 로 함께 부른다.
  - 지금 화면이 등록한 갱신 함수 `surfaceRefresh.current`. 등록하는 화면: `TodayPage:161` · `MyWorkPage:418` · `CalendarPage` · `DailyReportPage` · `MeetingListPage` · `MeetingDetailPage`
  - `loadContextOptions()`
  - `chat.refreshActiveConversation()`

  끝나면 토스트를 띄운다. 모두 성공했으면 「제안을 승인해 반영했습니다.」, 하나라도 실패했으면 「제안을 승인했습니다.」다(`App.tsx:368-375`).
  - **채팅 카드**: 대화를 다시 읽어 `action.state === "approved"` 가 되면 한 줄 요약 + [업무 열기]로 접힌다(`AxDraftCard.tsx:305-324`).
  - **홈**: 홈이 현재 화면이면 `reload` 가 `getActionItems()` 를 다시 부른다(`TodayPage.tsx:114`).
  - **「AX 제안」 칩**: 내 업무가 현재 화면이면 `reload` 가 `getActionItems()` 결과에서 `isAxDraftKind && status !== "resolved"` 만 남긴다(`MyWorkPage.tsx:337-343`).
  - 현재 화면이 아닌 화면은 다음 진입 때 기억(`screenCache`)을 먼저 보이고 뒤에서 갱신한다(1차 Phase 2).
- **홈·칩에서 연 경우**(`AxDraftModal`)
  - `onCommand` 가 `runActionCommand(item.action_item_id, commandId, {expected_version: item.expected_version, ...payload})` 를 부른다(`AxDraftCard.tsx:502-507`).
  - 이어서 `onDone()` → 알림 `「'<제목>' 판단을 반영했습니다.」`(`labels.ts:1337`) → `onClose()` 순이다.
  - `onDone` 은 화면마다 다르다.
    - 홈: `onDecided` = `refreshProjections`(`TodayPage.tsx:439`)
    - 내 업무: `reload()` 다음 `onDecided()`(`MyWorkPage.tsx:1349-1352`)
- **「확정 없이 초안만 저장」 길 — 없다**
  - FE: AX 초안에 쓰는 API 는 `runActionCommand`(명령 실행)와 자료 초안 3종(`stageActionMaterialFile/Link`·`discardActionMaterialDraft`)뿐이다. 자료는 고르는 즉시 서버에 남는다(`WorkModals.tsx:4512-4540`).
  - 서버: AX 제안에 내주는 명령은 `confirm`(또는 `approve`)·`reject` 둘뿐이다(`backend …/modules/actions/policy.py:114-128`).
  - `revise` 명령은 업무 **요청** 판단 쪽에만 있다(`backend …/platform/action_center.py:225, 261`).
- **선례 — 「저장」 문구**: `ActionTaskCard`(초안이 아닌 task 편집 카드)와 `ActionMeetingCard` 는 카드 안에서 편집 중일 때 주 단추를 「저장」/「저장 중…」으로 바꾼다(`ActionTaskCard.tsx:568` · `ActionMeetingCard.tsx:343`). 그러나 그 「저장」도 **confirm + draft** 를 보낸다(`ActionTaskCard.tsx:559-565`). 즉 문구만 다르고 명령은 같다.

### 2-3. 카드가 초안 값을 어디서 받나 / 바뀐 초안을 보일 길
- **채팅**
  - 대화 응답 `conversation.actions[]` 중 `turn_id` 가 같은 것을 그린다(`MessageList.tsx:247`).
  - 각 action 의 `edit_contract` 는 **응답을 받을 때마다 서버가 새로 만든다**(`backend …/platform/actions.py:1238-1245, 1652-1655`).
    - payload = `action.payload`, 또는 `payload_override`(정규 payload `:521`, 최신 버전 snapshot `action_center.py:705`)
    - `base_submission_version` 은 최신 submission 이다(`actions.py:1671-1676`).
  - FE 가 메시지에 얼려 둔 스냅샷은 없다. 대화를 다시 읽는 때는 다음과 같다.
    - 폴링 중(`useConversations.ts:220-239`)
    - 대화를 열 때(`:270-272`)
    - 판단 뒤 `refreshProjections`
- **홈·칩**: `GET /api/action-items` 봉투의 `edit_contract` 다(`AxDraftCard.tsx:85-99`). 그 화면을 다시 읽을 때 바뀐다.
- **카드 안 로컬 상태**
  - `materials` 만 따로 들고 있다(`AxDraftCard.tsx:251-253`). 수정 창에서 자료를 붙이고 빼면 `onMaterialsChange` 로 따라간다. 봉투가 새로 오면 그 값이 이긴다.
  - 그 밖의 값(제목·날짜·체크리스트 등)은 로컬 상태 없이 `contract.values` 에서 바로 읽는다.
- **판정**: 서버가 같은 action 의 values(또는 최신 submission)를 바꿔 내려 주면, 카드는 다음 재조회 때 새 값을 그린다. 지금은 확정 없이 values 를 바꾸는 명령이 서버에 없어서(§2-2), 사람이 고친 값이 카드에 반영되는 길은 confirm 뒤 「등록됨」 줄뿐이다.

### 2-4. `CreateWorkModal` 을 미리 채운 값으로 여는 자리 전부 (호출 6자리)

| # | 자리 | 파일:줄 | `initial` | 갈래 | 하단 단추 문구 | 제출 함수 → API |
|---|---|---|---|---|---|---|
| 1 | AX 초안 「수정」 | `AxDraftCard.tsx:413-451` | 13필드 전부(`:432-445`) + `axDraft` | 초안 갈래 고정 | **등록 / 등록 중…** | `axDraft.onSubmit` → `POST /api/action-items/{id}/commands/confirm`(+draft) |
| 2 | 하위 업무(업무 상세 「하위 업무」) | `WorkModals.tsx:3011-3028` | `{parentTaskId}` | 두 갈래 모두(`canCreateTask`·`canCreateRequest`) | 업무 추가 / 업무 요청 보내기 (만드는 중…) | 경로별: `createDirectTask`(`POST /api/tasks`) · `assignTask`(`POST /api/tasks/assign`) · `createWorkRequest`(`POST /api/work-requests`) |
| 3 | 재요청(내 업무 「다시 요청」) | `MyWorkPage.tsx:1423-1460` | `{title, description, dueDate, checklist, assigneeId, parentTaskId, supersedesRequestId}` | 요청만(`canCreateTask && !resending`, `requestOnly` `WorkModals.tsx:4462`) | 업무 요청 보내기 | `createWorkRequest` + `supersedes_request_id`(`WorkModals.tsx:5032`) |
| 4 | 회의 할 일 승격 | `MeetingDetailPage.tsx:1289-1330` | `{title, description, dueDate: due_candidate, checklist: checklist_candidate}` | 요청만(`canCreateTask={false}`) | 업무 요청 보내기 | `onSubmitRequest` → `promoteMeetingTodo`(`POST /api/meetings/{mid}/todos/{tid}/promote`) |
| 5 | 내 업무 「새 업무」 | `MyWorkPage.tsx:1423`(`isCreating`, `initial=undefined`) | 없음 | 권한대로 | 업무 추가 / 업무 요청 보내기 | 2번과 같음 |
| 6 | 홈 「새 업무」 | `TodayPage.tsx:468-480` | 없음 | 권한대로 | 같음 | 같음 |
| 7 | 캘린더 「새 업무」 | `CalendarPage.tsx:683-698` | 없음 | 권한대로 | 같음 | 같음 |

(`<CreateWorkModal` 호출은 6줄이고, 3번과 5번이 같은 호출을 나눠 쓴다.)

---

## 3. E2E-3 AX 채팅 카드 「등록」 진행 중 단추가 파란색

### 3-1. 「등록 중」이 파래지는 원인
- **단추**: `AxDraftCard.tsx:402-406`
  - `<Button disabled={busy || locked} … size="sm" tone="primary" variant="solid">{busy ? "등록 중…" : "등록"}</Button>`
  - 클래스는 `scax-button scax-button--solid-primary scax-button--sm` 이다.
  - 진행 중에 바뀌는 것은 두 가지뿐이다. `send()` 가 `busy=true` 로 두어 `disabled` 가 되고(`:262-274`), 문구가 `"등록 중…"`(`labels.ts:1328`)이 된다. variant·class 는 바뀌지 않는다.
  - DS `Button` 에는 busy/loading prop 이 없다(`ds/Button.tsx:40-93`). `aria-busy`·스피너도 없다.
- **규칙 경합**(로드 순서 `styles/index.css:46` components → `:97` ax)

| 파일:줄 | 선택자 | 명시도 | 값 |
|---|---|---|---|
| `components.css:10` | `.scax-button:disabled` | 0,2,0 | 배경 `fill-weak` · 글자 `ink-disabled` · 테두리 투명 |
| `components.css:13` | `.scax-button--solid-primary` | 0,1,0 | 배경 `accent` rgb(84,103,247) · #fff |
| **`components.css:14`** | `.scax-button--solid-primary:hover` | **0,2,0** (`:not(:disabled)` 없음) | 배경 `accent-strong` rgb(55,77,246) · #fff |
| `ax.css:670-671` | `.scax-drawer--chat .scax-button--solid-primary:not(:disabled)` | 0,3,0 | 배경 `ink` rgb(23,23,25) · 글자 `surface` |
| `ax.css:672-673` | `… :hover:not(:disabled)` | 0,4,0 | 배경 `ink-alt` · 글자 `surface` |

- **상태별로 이기는 규칙**(AxDraftCard 「등록」)
  - 기본 → `ax.css:670` 검정
  - hover → `ax.css:672` `ink-alt`
  - 진행·비활성이고 포인터가 밖에 있을 때 → `components.css:10` 회색
  - **진행·비활성이고 포인터가 위에 있을 때 → `components.css:10` 과 `:14` 가 0,2,0 으로 같아 뒤에 있는 `:14` 가 이긴다 → `accent-strong` 파랑에 흰 글자.** 누른 직후에는 포인터가 단추 위에 있으므로 「등록 중…」이 파랗게 보인다. `.scax-button` 의 `transition: background`(`components.css:8`)로 색이 서서히 바뀐다.
- `ax.css:668` 주석은 「비활성은 DS 의 `.scax-button:disabled` 가 그대로 이긴다」고 적었다. 그러나 hover 와 겹친 경우는 이 주석과 다르게 동작한다.
- **같은 구조의 단추**: `.action-task-card` 밖에 있는 solid-primary 는 모두 같다.
  - `ActionProgressBatchCard.tsx:137, 151`(반영 중… / 저장 중…)
  - `CommandConfirmationForm.tsx:119-128`(`variant` 가 primary 면 solid)
  - `ActionPreview.tsx:58-66`(`ActionResultCard` 명령)
  - 반대로 `ActionTaskCard`·`ActionMeetingCard` 의 「등록 중…」은 `ax.css:546`(`.action-task-card > .action-task-actions .scax-button:disabled`, 0,4,0)이 회색으로 잡는다.
  - `solid-danger:hover`(`components.css:274`)에도 `:not(:disabled)` 가 없다. `outlined-neutral:hover`(`:18`)·`text-neutral:hover`(`:25`)도 같은 이유로 비활성+hover 때 활성처럼 보인다(배경 `fill-weak`, 글자 `ink-neutral`).

### 3-2. 채팅 서랍 안 사람 행동 단추 × 상태 표

**약어**

| 약어 | 토큰 | 값 |
|---|---|---|
| IN | `ink` | rgb(23,23,25) |
| IA | `ink-alt` | rgba(55,56,60,.61) |
| INeu | `ink-neutral` | rgba(46,47,51,.88) |
| IAs | `ink-assistive` | rgba(55,56,60,.28) |
| ID | `ink-disabled` | rgba(55,56,60,.16) |
| S | `surface` | #fff |
| FW | `fill-weak` | rgba(112,115,124,.05) |
| L | `line` | rgba(112,115,124,.16) |
| LS | `line-strong` | — |
| ACS | `accent-strong` | rgb(55,77,246) |
| FR | 포커스 링 `--scax-focus-ring` = 0 0 0 3px `accent-20` | 파랑 계열 |

DS 단추는 모두 포커스 때 FR 을 받는다(`components.css:9`). DS 가 아닌 `<button>` 은 `shell.css:67` 이 outline 을 걷는다.

| 단추 (파일:줄) | 클래스 | 기본 (배경/테두리/글자) | hover | 진행·비활성 | 비활성+hover | focus | 판정 |
|---|---|---|---|---|---|---|---|
| AX 초안 **등록** `AxDraftCard.tsx:403` | solid-primary sm | IN / 투명 / S (`ax.css:670`) | IA (`:672`) | FW / 투명 / ID, 「등록 중…」 | **ACS / 투명 / #fff** (`components.css:14`) | FR | 검정, **진행+hover 때 파랑** |
| AX 초안 거절 `:379` · 수정 `:389` | outlined-neutral sm | S / L / INeu | FW | FW / 투명 / ID | FW / – / INeu (`:18` 이 이김) | FR | 회색·검정 |
| AX 초안 업무 열기 `:318` | outlined-neutral sm | S / L / INeu | FW | 비활성 없음 | – | FR | 회색·검정 |
| AX 초안 ‹ › `:368-369` | `IconButton` (`scax-icon-button`) | 투명 / – / IAs | FW / INeu | **비활성 규칙 없음** — 겉모습이 기본과 같다 | FW / INeu | FR | 회색 |
| AX 초안 4칸 바 `:343` | `.ax-draft-card__step(--on)` | L / 켜짐 IN (`ax.css:633-634`) | – | – | – | FR (`:635`) | 회색·검정 |
| ActionTaskCard 등록/저장 `ActionTaskCard.tsx:547` | solid-primary, `.action-task-card` 안 | IN / 투명 / S (`ax.css:671`) | IA (`:673`) | surface-alt / L / ID (`:546`) | 같음 (`:546` 0,4,0) | FR | 검정 |
| ActionTaskCard 수정·취소·초기화 `:533-543` | text-neutral, 카드 안 | S / task-card-border / #171719 (`ax.css:540`) | surface-alt / LS (`:541`) | 회색 (`:546`) | 회색 | FR | 검정 |
| ActionMeetingCard 등록 `ActionMeetingCard.tsx:325` 외 | ActionTaskCard 와 같음(루트에 `action-task-card`) | 같음 | 같음 | 같음 | 같음 | FR | 검정 |
| 진행 일괄 반영/저장 `ActionProgressBatchCard.tsx:137, 151` | solid-primary, 카드 밖 규칙 | IN | IA | FW / ID, 「반영 중…」/「저장 중…」 | **ACS 파랑** | FR | **같은 문제** |
| 진행 일괄 수정·취소 `:112-157` | text-neutral sm | 투명 / – / INeu | FW | FW / ID | FW / INeu | FR | 회색 |
| 명령 확인 폼 주 단추 `CommandConfirmationForm.tsx:119-128` | solid-primary md | IN | IA | FW / ID (문구 그대로) | **ACS 파랑** | FR | **같은 문제** |
| 결과 카드 명령 `MessageList.tsx:659` → `ActionPreview.tsx:58-66` | solid-primary/solid-danger/outlined | primary 는 IN | IA | FW / ID | primary 파랑, danger 빨강 | FR | 비활성이 될 때 같은 문제 |
| 입력창 **보내기 / 대기열에 보내기** `ChatDrawer.tsx:381` | solid-primary sm | IN / S | IA | 비활성 없음 | – | FR | 검정 |
| 실행 취소 `ChatDrawer.tsx:375` | text-neutral sm | 투명 / INeu | FW | 비활성 없음 | – | FR | 회색·검정 |
| 실행 레일 다시 시도 `MessageList.tsx:615` | solid-primary sm | IN | IA | 비활성 없음 | – | FR | 검정 |
| 접수 실패 다시 보내기 `:361` · 삭제 `:364` | outlined-/text-neutral | S / L / INeu | FW | – | – | FR | 회색 |
| 근거 상세 열기 `MessageList.tsx:727` | outlined-neutral sm | S / L / INeu | FW | – | – | FR | 회색 |
| **근거 N개 더 보기** `MessageList.tsx:737` | `.scax-sources__more` (`ax.css:238`) | 투명 / 없음 / **`accent` 파랑** + 밑줄 | 규칙 없음 | – | – | 없음 | **사람 행동인데 파랑** |
| 새 메시지로 이동 `MessageList.tsx:194` | `.scax-chat__jump` (`ax.css:135`) | 검정 / L / 흰 글자 | – | – | – | 없음 | 검정 |
| **추천 대화** 칩 `MessageList.tsx:438` | `.scax-followup__item` (`ax.css:173-182`) | S / L / IN | FW / LS / IN (`:177`) | 보내는 중·선택: FW / LS / IN (`:179`). 다른 칩은 `opacity:.58` (`:178`) | – | FR (`:182`) | 검정·회색. 실패 시 빨강 (`:180`) |
| 시작 대화 추천 `ChatDrawer.tsx:327` | `.scax-chat__starters button` (`ax.css:143-145`) | S / L / IA | FW / LS / IN | – | – | 없음 | 회색·검정 |
| 대화 목록·새 대화 도구 `ChatDrawer.tsx:222, 229` | `.scax-chat__tool` (`ax.css:105-109`) | surface-alt / 투명 / IA | FW / LS / IN | – | – | FR (`:109`) | 회색·검정 |
| 서랍 닫기 `ChatDrawer.tsx:240` | `.scax-chat__tool--close` (`ax.css:108`) | 투명 / – / IAs | FW / LS / IN | – | – | FR | 회색 |
| 대화 목록 항목 `ChatDrawer.tsx:278` | `.scax-chat__history button` (`ax.css:124-129`) | S / L | 규칙 없음 | – | 눌림: FW | 없음 | 회색·검정 |
| 대화 목록 다시 시도 `ChatDrawer.tsx:266` | outlined-neutral sm | S / L / INeu | FW | – | – | FR | 회색 |
| 맥락 칩 ✕ `ChatDrawer.tsx:348` | `.scax-chat__context-chip button` (`ax.css:314`) | 칩 FW / IN, ✕ IAs | 없음 | – | – | 없음 | 회색 |

- 채팅 서랍은 `aside.scax-drawer.scax-drawer--sm.scax-drawer--chat` 이다(`ChatDrawer.tsx:212`).
- `ActionCenter` 는 채팅에 그려지지 않는다(`MessageList.tsx:3-8` import).
- 단추가 아닌 파랑: 카드 상태 글자 `.scax-actioncard>small`(`ax.css:254`, `accent`).

### 3-3. 검정 단추 변형의 정의와 DS 의 solid 단추 상태 규칙
- **검정 변형**: `ax.css:665-673` 이다(커밋 `94cacfd`, 1차 E2E). 별도 변형 클래스를 만든 것이 아니다. **채팅 서랍 범위에서 `solid-primary` 를 덮어쓴다.** 주석이 「DS 에 검정 solid 변형이 없어 여기서 세운다(DS-gaps)」라고 적고 있다(`:667`).
- **DS 구현(코드)**: `components.css:8-27`(solid/outlined/text) · `:273-274`(solid-danger) · `:408-410`(inline) · `:414-416`(ai) · `ds/Button.tsx:38-93`(variant `solid|outlined|text|inline|ai`, tone `primary|neutral|danger`). `inline`·`ai` 의 hover 만 `:not(:disabled)` 를 쓴다(`:409`, `:415`).
- **DS 문서**: `docs/design/design-system-v2.dc.html`
  - 「08 — BUTTON」(`:755-841`): 「5변형 × 3높이」(`:759`). 상태 열은 「기본 · Hover · Active · Disabled」(`:764`)이고 **진행(loading) 상태는 없다.**
  - Primary 예시(`:769-775`)
    - 기본 `#5467F7` → hover `#374DF6` → active `#1E37F4`
    - **disabled 는 배경 `#F6F7FA`, 글자 `#979FAF`**
  - **검정 solid 는 없다.**
  - 「10 — STATE」 Disabled(`:951-953`): 「배경 `#F6F7FA` · 글자 `#979FAF` · 보더 `#E8EAF0` · cursor not-allowed」 · 「opacity를 쓰지 않습니다」. 이 규칙과 달리 `.scax-followup__item:disabled{opacity:.58}`(`ax.css:178`)가 있다.
  - Loading(`:957-964`)은 스켈레톤만 다룬다.
  - 원칙 카드(`:1599`): 「#7181F8은 액션과 완료에만 — 버튼·전송·…」. 채팅만의 「사람 = 검정」 규칙은 `ax.css` 에만 있다.
- `docs/design/README.md` 에는 단추 규칙이 없다(`:1-11`).

---

## 4. E2E-4 업무 상세 헤더 — 「담당 …」 줄과 「AX 제안에서 생성됨」 줄

### 4-1. 메타 영역 DOM·클래스·CSS (실제 코드 그대로)
겹(`Modal`/`Drawer`)의 머리줄(`headerExtra`, `WorkModals.tsx:1895-1928`)에는 `ChipRow` 가 선다. 그 안 순서는 다음과 같다.
- `StatusText`
- 기한 초과 `Badge tone="danger"`(`isOverdue`)
- `Badge tone="outline"` `v{version}`
- 「편집」/「편집 끝내기」 `Button variant="text" size="sm"`(`editable && relDraft === null`)
- 「AX」 `Button variant="ai" size="sm"`

본문(`WorkModals.tsx:1958-2035`):

```
div.scax-td
└ div.meta[aria-label="업무 메타"]                       ← task-detail.css:96-99  flex · gap 12 · padding 0 0 14px · border-bottom 1px line
  └ div.meta__left                                     ← :111  min-width 0 · flex 1 1 auto
    ├ (metaEditing) label.sr-only + input.meta__title-input#task-title-{id}   ← :112-116
    ├ div.meta__facts                                   ← :101-104 flex · wrap · gap 6px 14px · 12px · ink-assistive / b: ink-alt 600 (:105)
    │  ├ <span>담당 <b>{ownerName}</b></span>                         항상
    │  ├ <span>기한 <b>{formatDate(due_date)}</b></span>               !metaEditing && shown.due_date
    │  ├ <span>시작 <b>{formatDate(start_date)}</b></span>             !metaEditing && shown.start_date
    │  ├ <span>결재 <b>{이름}</b></span>                              shown.approver_id
    │  └ <span>참조 <b>{이름 · 이름}</b></span>                        cc_member_ids.length > 0
    ├ p.origin-chip[aria-label="업무 출처"]   (task.origin 이 있을 때)  ← screens-a.css:437 flex · center · wrap · gap 8 · margin 0 0 4px · 12.5px
    │  ├ Badge tone="outline" {originSentence(origin)}   (문장이 null 이 아니면)
    │  └ origin.source 가 있으면
    │       onOpenSource 있음 → Button variant="inline" {source.title ?? "출처 보기"}   ← components.css:408 accent 글자
    │       없음 → small.t-meta {source.title}
    └ (metaEditing) div.meta__edit  ← task-detail.css:119 grid · gap 8 · margin-top 8
         DateField#task-start-{id} 「시작일」 · DateField#task-due-{id} 「기한」
```

- 라벨: `담당/기한/시작/결재/참조` = `taskDetail.metaAssignee/metaDue/metaStart/metaApprover/metaCc`(`labels.ts:343-348`)
- `shown = detailTask ?? task`(`WorkModals.tsx:1313`)
- **두 줄이 붙는 이유**: `.meta__facts` 에는 margin/padding 이 없다(`task-detail.css:101-104`). 바로 아래 `p.origin-chip` 은 `margin: 0 0 4px` 로 위 여백이 0 이다(`screens-a.css:437`). 두 요소 사이 간격을 정하는 규칙이 없다. 글자 크기는 facts 12px, origin 12.5px 로 다르다.
- `.origin-chip` 은 `.scax-td` 스코프 밖의 전역 규칙이다(`screens-a.css`). 반면 `.meta*` 는 `.scax-td` 스코프다(`task-detail.css`).
- 소스 들여쓰기가 어긋나 있지만(`WorkModals.tsx:1988` 의 `{task.origin && (` 가 0열), DOM 상 `p.origin-chip` 은 `.meta__left` 안, `.meta__facts` 다음 형제다.

### 4-2. 「AX 제안에서 생성됨」 배지와 링크가 가리키는 것
- **배지 문장**: `originSentence`(`WorkModals.tsx:383-389`)
  - `actor` 가 있고 `kind === "work_request"` 면 `「{actor}가 보낸 업무」`
  - `actor` 가 있고 `kind === "direct_assignment"` 면 `「{actor}가 담당자를 지정함」`
  - 그 밖에 `actor` 가 있으면 `「{actor}가 만든 업무」`
  - **actor 가 없고 source 가 있으면 `「AX 제안에서 생성됨」`**
  - 둘 다 없으면 `null`
- **데이터**: `task.origin`(`TaskOrigin`, `lib/viewModels.ts:441-446`) = `{kind, actor_role, actor, source: {type, id, title} | null}`
  - 서버 `_origin_projection`(`backend …/modules/work/application.py:2444-2486`)에서 `task.source_action_item_id` 가 있으면 `kind="self_created"`, `actor=None`, `source=_action_item_source(...)` 다(`:2467-2471`).
  - `_action_item_source`(`:2501-2509`)는 `{"type":"action_item","id": <action item id>,"title": subject_label(action)}` 을 돌려준다. 주석은 「The label names the work that was created」.
  - `action_subject_label`(`backend …/platform/actions.py:1208-1214`)은 생성 kind 면 payload 의 `title` 을 쓴다.
  - 그래서 링크 글자가 **만들어진 업무의 제목과 같다.**
- **링크 대상**: 업무 자신이 아니라 그 업무를 만든 **AX 초안 판단 항목(action item)** 이다.
  - 내 업무에서: `onOpenSource` → `openSource`(`MyWorkPage.tsx:696-709`) → `type === "action_item"` 이면 `pushDetail({kind:"action", actionItemId})` → 같은 겹 안의 `ActionItemDrawer`(`MyWorkPage.tsx:1360-`) 판단 상세다.
  - 홈(`TodayPage.tsx:418`)·캘린더(`CalendarPage.tsx:701`)의 `TaskDetailDrawer` 는 `onOpenSource` 를 넘기지 않는다. 그래서 링크가 아닌 `small.t-meta` 글자로만 선다(`WorkModals.tsx:1999`).
  - `onOpenSource` 를 넘기는 호출은 `MyWorkPage.tsx:1314` 하나뿐이다.

### 4-3. 같은 출처 배지가 나오는 자리 전부
- `originSentence`·`.origin-chip` 이 그려지는 자리는 **`TaskDetailDrawer` 한 곳**(`WorkModals.tsx:1988-2002`)뿐이다. 이 드로어를 여는 호출은 3곳이다(내 업무·홈·캘린더).
- 「회의에서 생성됨」 문자열은 **없다**(grep 0). 회의 할 일 승격은 업무 요청으로 나가므로(`MeetingDetailPage.tsx:1289-1330`) 그 업무의 origin 은 `work_request` 갈래가 된다. 배지는 `「{actor}가 보낸 업무」` 다. 회의 승격 요청의 actor 는 시스템 id 가 올 수 있다(`MyWorkPage.tsx:714-716` 주석).
- `origin.actor` 를 다른 형태(배지가 아닌 요청자 칸)로 쓰는 자리
  - `MyWorkPage.tsx:857`·`:1186-1187`(표 상대/요청자 칸)
  - `ProjectTaskPanel.tsx:103, 153-156`(프로젝트 패널 요청자 `dd.scax-pj-facts__val`)
  - `:386` · `MyWorkPage.tsx:1548`(`requesterName`)
- `origin.source` 를 읽는 다른 자리: `MyWorkPage.tsx:724`(요청 원장 찾기, 표시 없음)

---

## 5. E2E-5 업무 날짜 (현재 상태만)

### 5-0. 타입에 있는 업무 날짜 필드 (`lib/viewModels.ts`)

| 필드 | 뜻 | 위치 | 화면 표시 |
|---|---|---|---|
| `start_date` | 시작(예정)일 | `:245` | 여러 곳(5-1) |
| `due_date` | 기한 | `:246` | 여러 곳 |
| `created_at` · `updated_at` | 생성·변경 시각 | `:247-248` | 상세 활동 줄 · 처리일 대체 |
| `started_at` | `open → in_progress` 시각, 「계획 시작일과 다른 값」 | `:326-327` | **표시 0곳** |
| `completed_at` | 완료 시각 | `:334` | 「완료 업무」 표 처리일 1곳 |
| `reopened_at` | 재개 시각 | `:335` | **표시 0곳** |
| `assignment.accepted_at` | 수락 시각 | `:470` | **표시 0곳** |
| `derived.overdue_days` | 지연 일수 | `:184` | 표 `+N` · 프로젝트 지연 수 |
| 프로젝트 행 `span_from/span_to` · `overdue_days` | 간트 구간 | `:114-128` | 간트·카드 |
| 캘린더 행 `start_date/due_date/span_*` · `schedules[]` | | `:1379-1382, 1350-1353` | 캘린더 |
| `TaskPatch.start_date/due_date` | 쓰기 | `:581-582` | – |

### 5-1. 날짜를 보여 주는 화면 전부

| 화면 | 파일:줄 | 필드 | 라벨 | 형식 |
|---|---|---|---|---|
| 업무 상세 머리 배지 | `WorkModals.tsx:1897` | `due_date` (클라이언트 `isOverdue`) | 기한 초과 | `Badge tone="danger"` |
| 업무 상세 메타 줄 | `WorkModals.tsx:1975-1977` | `due_date` → `start_date` 순 | 기한 · 시작 | `formatDate` `2026/10/06`, D-day 없음 |
| 업무 상세 활동 요약 | `WorkModals.tsx:238` | `created_at` · `updated_at` | … 생성 · 최근 변경 | `formatDate(isoDateInSeoul())` |
| 업무 상세 이력 줄 | `WorkModals.tsx:270` | `occurred_at` | – | `formatDateTime` `2026/10/06 14:05` |
| 업무 상세 이력 비교 | `WorkModals.tsx:153-166, 296` | `start_date`·`due_date` 전→후 | 시작일 / 기한 | `formatDate` |
| 업무 상세 조건 변경 제안 | `WorkModals.tsx:2302` | `payload.due_date` | 기한 | `formatDate` |
| 업무 상세 연관(하위·후행) | – | (`due_date` 가 타입에 있음 `:197, 218`) | – | **표시 안 함** |
| `DueText` 부품 | `WorkModals.tsx:324-332` | `due_date` | – | `2026/10/06 (D-3)` — **렌더 0곳** |
| 내 업무 표 5종(내 업무·AX 제안·보낸·참조·조직) | `WorkTables.tsx:246/274, 325/344, 399/419, 473/492, 615/630` → `DueCell` `:178-185` | `due_date` (+ `overdue_days`) | 기한 | `2026/10/06` + 빨간 `+N` |
| 내 업무 「AX 제안」 표 나이 | `WorkTables.tsx:340` | `created_at` | 만든 지 N일 / 오늘 만듦 (`labels.ts:1332`) | – |
| 내 업무 「완료 업무」 표 | `WorkTables.tsx:544, 573`, 값 `:654` | `completed_at ?? updated_at` (시각) | **처리일** | `formatDate(시각)` — 앞 10자를 잘라 **UTC 날짜**가 된다 |
| 내 업무 칩 | `workRows.ts:288-305` · `labels.ts:278` | `due_date`·`overdue_days` | 기한 지남 | 개수 |
| 내 업무 타임라인 창 | `WorkViews.tsx:449` | 5주 창 | – | `2026/10/06 – 2026/10/12` |
| 타임라인 달 띠 | `WorkViews.tsx:432-439` | – | 기간 열 | `2026년 10월`(인라인) |
| 타임라인 날 머리 | `WorkViews.tsx:475-477` | – | – | `Number(day.slice(8))`, title 은 `formatDate` |
| 타임라인 줄 | `WorkViews.tsx:492-497`, `taskSpan` `:176-182` | start ?? due ~ due ?? start | 날짜 없음 | `2026/10/06` 또는 `A → B` + ` · D-3` |
| 타임라인 막대 aria | `WorkViews.tsx:506` | 구간 | – | `제목 · A – B · 상태` |
| 홈 업무 줄(`TaskListRow`) | `WorkViews.tsx:150-160` (`TodayPage.tsx:356, 365, 373` 에서 씀) | `due_date` → 없으면 `start_date` → 없으면 `created_at` | 기한 … / … 시작 / … 등록 · 기한 초과 | `기한 2026/10/06 (D-3)` |
| 홈 머리 | `TodayPage.tsx:272` | 오늘 | – | `formatLongDate` `2026/10/02 금요일` |
| 수신함 레일 카드 | `shell/InboxRail.tsx:71` | 요청 `due_date` | 기한 | `기한 2026/10/06` |
| 요청 상세 | `WorkModals.tsx:3853-3854` | `due_date` | 희망 기한 | `2026/10/06 (D-3)` / 없음 |
| 요청 상세 참고 업무·수정 미리보기·회차 비교·제출·댓글 | `WorkModals.tsx:3922, 3976-3977, 4061, 4069-4070, 4129` | `due_date`·`submitted_at`·`created_at` | 희망 기한·기한 | `formatDate` |
| 캘린더 왼쪽 카드 | `calendarModel.ts:401-406` → `ScheduleCard.tsx:93` | `span_*`·`start_date`·`due_date` | 기한 없음 / … 마감 (`labels.ts:1070-1072`) | `2026/10/06 마감` · `A ~ B` |
| 캘린더 일정 칩 | `calendarModel.ts:424` · `labels.ts:1074` | `on_date`+`starts_at` | – | `6일 10:00` |
| 캘린더 월·주 막대 | `EventBar.tsx:47` · `WeekGrid.tsx:204` | `span_*` (위치) | 손잡이 title 「끌어서 시작일/마감일 정하기」 (`labels.ts:1081-1082`) | 글자 없음 |
| 셸 캘린더 레일 | `shell/CalendarRail.tsx:71-73` | **`due_date` 날에만** 놓음 | – | – |
| 셸 캘린더 레일 머리·주·지연 | `CalendarRail.tsx:58-68, 254-258` | – | – | `10월 6일 월요일` · `2026년 10월 2주 차` · `+N` |
| 프로젝트 왼쪽 카드 | `projectModel.ts:184-193, 200` → `ProjectRail.tsx:153` | `start_date`·`due_date` | 기한 없음 / … 마감 / … 시작 (`labels.ts:1106-1108`) | `A ~ B` 또는 한 날 |
| 프로젝트 업무 패널 | `ProjectTaskPanel.tsx:143-144, 246` | 같은 `taskWhen` | 기간 (`labels.ts:1136`) | 같음 |
| 프로젝트 간트 | `ProjectGantt.tsx:71, 182, 280` | 축 범위 · 날 · `span_*` | – | `A ~ B` (`labels.ts:1119`) · 날 숫자 · 막대 글자 없음 |
| 프로젝트 요약 | `ProjectSummaryStrip.tsx:20` · `projectModel.ts:165` | `overdue_days` 개수 | 지연 | 숫자 |
| AX 초안 카드 | `AxDraftCard.tsx:168-174, 188` | `start_date`·`due_date` | 기간 (`labels.ts:1312`) | `A → B` · `A ~` · `~ B` |
| AX 초안 카드(등록 뒤) | `AxDraftCard.tsx:314` | `due_date` | – | `formatDate` / — |
| AX task 카드(초안 외) | `ActionTaskCard.tsx:31-33, 66` | `preview[]` kind date/datetime | 서버 라벨 | **`2026.10.06`** (`/`→`.`) |
| AX 미리보기 상세 | `ActionPreview.tsx:37` | `preview[]` | 서버 라벨 | `2026/10/06` (ActionTaskCard 와 다름) |
| 판단 상세(ActionCenter) | `ActionCenter.tsx:54, 69-73, 150, 160, 209, 310` | `due_date` | 희망 기한 | `formatDate` / 없음 |
| 판단 상세 시각 | `ActionCenter.tsx:143, 171, 231` · `:583` | `submitted_at`·`decided_at`·`created_at` | 첫 제출(`:583`) | `formatDateTime` · `:583` 은 `slice(0,10)` 이라 **UTC 날짜** |
| 회의 할 일 후보 | `MeetingDetailPage.tsx:1189, 1196` → `AgendaBlock.tsx:223` | `due_candidate` | – | **ISO 그대로 `2026-09-12`** |
| 일일보고 | `DailyReportPage.tsx:361, 499` | 보고 날짜·제출 시각 | – | 업무 날짜 없음 |
| 조직·관계 그래프·채팅 본문 | – | 업무 날짜 없음(그래프 `node.date` `viewModels.ts:12` 표시 0곳) | – | – |
| 렌더 0곳 부품 | `WorkViews.tsx:29` `TaskCard` · `:258` `TaskCalendar`(테스트만) · `:537` `TaskKanban`(`:606` 이 `created_at` 을 「… 시작」으로 씀) | | | |

### 5-2. 날짜를 고치는 입구 전부
모든 업무 날짜 쓰기는 `updateTask`(`lib/api.ts:247-277`) → **`PATCH /api/tasks/{id}`** 로 간다.
- body: `{expected_version, title?, description?, start_date? | clear_start_date, due_date? | clear_due_date, project_id? | clear_project, parent_task_id? | clear_parent, preceding_task_ids?}`

| 입구 | 파일:줄 | 무엇을 고치나 | API |
|---|---|---|---|
| 업무 상세 **「편집」** | 단추 `WorkModals.tsx:1904-1907`(`variant="text" size="sm"`, 조건 `editable = canManage && !closed && !readOnly` `:797` + `relDraft === null`) | 켜면 제목 입력(`:1963-1972`)·**시작일·기한 `DateField`**(`:2007-2031`)·업무 내용 textarea(`:2061-2073`)가 선다. 메타 줄의 기한·시작 글자는 숨는다(`:1976-1977`). | (저장은 아래 줄) |
| 업무 상세 **「변경 저장」** | `WorkModals.tsx:1818-1821`(하단 줄, `editable && dirty` 일 때) → `save()` `:1072-1087`(시작 ≤ 기한 검사 `:1077-1079`) → `onUpdate` | 제목·내용·`start_date`·`due_date` 중 바뀐 것만 | `MyWorkPage.tsx:519-522` · `TodayPage.tsx:225-228` · `CalendarPage.tsx:594-597` → `updateTask` → `PATCH /api/tasks/{id}` |
| 조건 변경 제안(요청자, 수락 뒤) | 단추 `WorkModals.tsx:1812-1814`, 모달 `TermsChangePrompt` `:3327-3400`(`DateField` 「기한」 `:3364`) | `due_date`(시작일 없음)·제목·내용 | `createTaskProposal`(`api.ts:399`) → `POST /api/tasks/{id}/proposals` `{kind:"terms_change", payload:{due_date…}}` · 응답 `respondTaskProposal`(`api.ts:411`) |
| 새 업무 추가 모달 | `WorkModals.tsx:5360-5388`: 시작일(`:5362, 5370`) · 기한 라벨 **「마감일」(업무) / 「희망 기한」(요청)** (`:5377, 5385`) | `start_date`·`due_date` | 경로별: `createDirectTask`(`POST /api/tasks`, `:4942-4945`) · `assignTask`(`POST /api/tasks/assign`, `:4922-4927`) · `createWorkRequest`(`POST /api/work-requests`, `:5017-5022`) · `promoteMeetingTodo`(`:5011`, 기한만) |
| ↳ 동료에게 바로 보내기(horizontal 경로) | `WorkModals.tsx:4650-4651, 4930-4937` | 시작일 칸은 **늘 보인다**(`:5360` 무조건). 그러나 `effectiveStartDate = ""` 라 실리지 않는다. | `POST /api/tasks` (기한만) |
| 요청 수정·재상신 | `WorkModals.tsx:3714-3755, 3949-3953` | `due_date`(희망 기한) | `amendWorkRequest`(`api.ts:1070`) · `resubmitWorkRequest`(`api.ts:991`) |
| 캘린더 날짜 칸에 끌어 놓기 | `CalendarPage.tsx:288-308` → `calendarWrites.ts:46-55, 270-286` | 두 날 모두 있으면 길이를 유지해 옮김 · 하나면 그 날만 · 없으면 시작=기한=놓은 날 | `PATCH /api/tasks/{id}` |
| 캘린더 막대 손잡이 | `CalendarPage.tsx:315-331` → `calendarWrites.ts:71-78` | 앞 손잡이 `start_date`, 뒤 손잡이 `due_date` | 같음 |
| 캘린더 시간 칸(업무 날짜 아님) | `CalendarPage.tsx:397, 399, 446` | 일정 `on_date/starts_at/ends_at` | `POST /api/tasks/{id}/schedules` · `PATCH /api/task-schedules/{sid}` |
| AX 초안 「수정」 | `AxDraftCard.tsx:435-436` → 새 업무 추가 모달 | 초안 `start_date`·`due_date` | confirm + draft (§2-2) |
| AX task 카드(초안 외) | `ActionTaskCard.tsx:132-145` (`DateField displaySeparator="."`) | draft `start_date`·`due_date` | confirm + draft |
| 판단 상세 수정·조정 제안 | `ActionCenter.tsx:282, 545` | 희망 기한 | `runActionCommand` |
| 프로젝트 간트·패널 | – | **고치는 입구 없음**(features/project 에 `updateTask`·드래그 0곳) | – |

- 날짜 입력 부품은 `ds/DateField.tsx:17-71` → `ds/DatePicker.tsx:165` 이다.
  - 기본 표시는 ISO `2026-10-06` 이다. `displaySeparator` 를 주면 `/` 또는 `.` 로 바뀐다(`:49`).
  - `<DateField` 는 15곳이고, 그중 `displaySeparator="."` 를 주는 곳이 5곳이다(ProjectCreateModal 2 · ActionTaskCard · ActionMeetingCard).
  - 네이티브 `type="date"` 는 0곳이다.
- **실제 시작일·실제 종료일을 고치는 입구는 없다**(`started_at`·`completed_at` 쓰기 0곳).

### 5-3. 날짜 표시 형식 함수

| 함수 | 정의 | 출력 | 호출 수 |
|---|---|---|---|
| `formatDate` | `lib/labels.ts:163-167` | `YYYY/MM/DD`, 비면 `—`. 앞 10자 정규식이라 **시간대 변환 없음** | 68 |
| `formatDateTime` | `labels.ts:200` | `YYYY/MM/DD HH:MM`(서울) | 9 |
| `formatLongDate` | `labels.ts:209` | `YYYY/MM/DD 금요일` | 2 |
| `formatMonth` | `labels.ts:180` | `YYYY/MM` | 1 |
| `formatMonthLong` | `labels.ts:188` | `2026년 9월` | 15 (DateField prop) |
| `isoDateInSeoul` | `labels.ts:192` | 시각 → 서울 `YYYY-MM-DD` | 15 |
| `dueDayText` | `labels.ts:228` | `D-Day`/`D-3`/`D+2` | 4 |
| `isOverdue` | `labels.ts:235` | boolean | 5 |
| `dayDifference` / `addDays` | `labels.ts:222` / `:216` | 일수 / ISO | 11 / 다수 |
| `formatPeriod` · `formatActivityTime` | `labels.ts:610` · `:620` | 조직 이력용 | 2 · 1 |
| `meetingWhen/Clock/Range/DateInput` | `labels.ts:969, 990, 997, 1029` | 회의용 | 3/12/1/3 |
| `calendarScreen.dueOnly/range/scheduleChip` | `labels.ts:1071-1075` | `… 마감` / `A ~ B` / `6일 10:00` | – |
| `projectScreen.dueOnly/startOnly/ganttRange` | `labels.ts:1107-1108, 1119` | `… 마감` / `… 시작` / `A ~ B` | – |
| `taskWhen`(프로젝트) | `features/project/projectModel.ts:184` | 위 표 | 3 |
| `taskWhen`(캘린더, 비공개) | `features/calendar/calendarModel.ts:401` | 위 표 | 1 |
| `seoulDate` / `seoulClock` | `calendarModel.ts:73 / 77` | ISO / `HH:MM` | 6 / 8 |
| `taskSpan` | `features/work/WorkViews.tsx:176` | `{start,end}` | 3 |
| `DueCell` | `features/work/WorkTables.tsx:178` | `YYYY/MM/DD` + `+N` | 5 |
| `DueText` | `WorkModals.tsx:324` | `YYYY/MM/DD (D-n)` | **0** |
| `diffValue` | `WorkModals.tsx:153` | 날짜 칸은 `formatDate` | 4 |
| `displayValue` | `ActionCenter.tsx:69` | `formatDate` / 없음 | 6 |
| `taskPreviewValue` | `ActionTaskCard.tsx:31` | `YYYY.MM.DD` | 1 |
| `periodText` | `AxDraftCard.tsx:169` | `A → B` / `A ~` / `~ B` | 1 |
| `railDate` / `weekLabel` | `shell/CalendarRail.tsx:58 / 64` | `10월 6일 월요일` / `2026년 10월 2주 차` | 3 / 1 |
| `overdueDaysOf` | `features/work/workRows.ts:186` | 서버 `overdue_days`, 없으면 클라이언트 계산 | 5 |

- **헬퍼 밖 인라인 형식**
  - `toLocale*`/`Intl.DateTimeFormat` 8곳 중 6곳은 labels.ts 헬퍼 안이다. 나머지 둘은 `calendarModel.ts:80` · `BookingModal.tsx:71-72` 다.
  - 날 숫자: `WorkViews:346, 476` · `ProjectGantt:182` · `MonthGrid:86` · `WeekGrid:178` · `CalendarRail:246` · `DatePicker:135`
  - 구분자 바꿈: `DateField:49` · `ActionTaskCard:32` · `ActionMeetingCard:83`
  - 달 라벨 `${year}년 ${month}월`: `WorkViews.tsx:434`
- **시각 → 날짜를 UTC 로 자르는 자리 3곳**: `WorkTables.tsx:573`(처리일) · `ActionCenter.tsx:583`(첫 제출) · `ProjectManageModal.tsx:78`(`valid_until.slice(0,10)`)
- **같은 `due_date` 의 이름**
  - 기한: 상세 메타·편집, 표 머리 5종, 이력, 제안, 수신함
  - 마감일: 새 업무 모달 업무 갈래 `WorkModals.tsx:5377`, 캘린더 손잡이 `labels.ts:1082`, 거절 문구 `:1247`, 간트 빈 상태 `:1121`
  - 「… 마감」: 캘린더·프로젝트 카드
  - 희망 기한: 요청 쪽
- **`start_date` 의 이름**
  - 시작: 상세 메타 `labels.ts:345`
  - 시작일: 편집·새 업무·이력
  - 「… 시작」: 프로젝트 카드·홈 줄
- **구간 구분자**: `~`(프로젝트·캘린더) · `→`(타임라인 줄·AX 초안) · `–`(타임라인 창·aria·`formatPeriod`)

---

## 6. grep 개수표

명령은 `grep -rnoF '<심볼>' frontend/src` 에서 `*.test.*` 를 뺀 것이다(파일 수는 `-l`). E2E-5 의 함수 호출 수는 정의를 뺀 `\bfn\(` 개수다.

| 요청 | 심볼 | 개수 | 파일 |
|---|---|---|---|
| E2E-1/2 | `<CreateWorkModal` | 6 | CalendarPage · TodayPage · AxDraftCard · WorkModals · MyWorkPage · MeetingDetailPage |
| E2E-1/2 | `axDraft` | 99 | MessageList · TodayPage · AxDraftCard · ActionTaskCard(라벨 import) · WorkTables · WorkModals · MyWorkPage · labels |
| E2E-1/2 | `AxDraftCard` | 7 | MessageList · TodayPage · AxDraftCard · MyWorkPage |
| E2E-1/2 | `AxDraftModal` | 5 | TodayPage · AxDraftCard · MyWorkPage |
| E2E-1/2 | `axDraftFromAction` / `axDraftFromEnvelope` / `isAxDraftKind` | 4 / 7 / 5 | |
| E2E-1 | `values.checklist` | 5 | ActionTaskCard · AxDraftCard |
| E2E-2 | `runActionCommand(` | 6 | AxDraftCard · WorkModals · api · ActionCenter |
| E2E-2 | `decideAction(` | 2 | useConversations · api |
| E2E-2 | `getActionItems(` | 4 | TodayPage · WorkModals · MyWorkPage · api |
| E2E-2/3 | `"등록 중…"` | 4 | ActionTaskCard · ActionMeetingCard · WorkModals · labels |
| E2E-2 | `onRegisterRefresh?.(` 등록 화면 | 6 파일 | Calendar · Today · DailyReport · MyWork · MeetingList · MeetingDetail |
| E2E-3 | `solid-primary` (CSS 규칙) | components.css 2 · ax.css 6 | |
| E2E-3 | `:not(:disabled)` 없는 hover (`solid-primary`·`solid-danger`·`outlined-*`·`text-neutral`) | 5 (`components.css:14, 16, 18, 25, 274`) | |
| E2E-3 | `.scax-drawer--chat` 단추 규칙 | 4 선택자 (`ax.css:670-673`) | |
| E2E-3 | `.action-task-card … :disabled` | 1 (`ax.css:546`) | |
| E2E-4 | `originSentence` | 3 (정의 1 + 사용 2, 같은 줄) | WorkModals |
| E2E-4 | `origin-chip` | 2 | WorkModals · screens-a.css |
| E2E-4 | `AX 제안에서 생성됨` | 1 | WorkModals |
| E2E-4 | `회의에서 생성됨` | 0 | |
| E2E-4 | `onOpenSource` | 8 (넘기는 호출 1: `MyWorkPage.tsx:1314`) | WorkModals · MyWorkPage |
| E2E-4/5 | `<TaskDetailDrawer` | 3 | CalendarPage · TodayPage · MyWorkPage |
| E2E-4 | `meta__facts` | 4 | WorkModals · task-detail.css |
| E2E-5 | `formatDate(` 호출 | 68 | 5-3 |
| E2E-5 | `formatDateTime(` / `isoDateInSeoul(` / `dueDayText(` / `isOverdue(` | 9 / 15 / 4 / 5 | |
| E2E-5 | `<DateField` | 15 (`displaySeparator="."` 5) | |
| E2E-5 | `<DueText` | 0 | |
| E2E-5 | `started_at` · `reopened_at` 표시 | 0 · 0 | |
| E2E-5 | 「기한」 / 「마감」 / 「시작일」 / 「마감일」 / 「희망 기한」 / 「처리일」 / 「완료일」 (`grep -o`, 주석 포함) | 57 / 15 / 25 / 5 / 7 / 2 / 0 | |
| E2E-5 | 날짜 쓰기 API `updateTask` 호출 화면 | 3 (MyWork · Today · Calendar) + 캘린더 끌기 `calendarWrites.ts` | |

---

## 7. 조사 한계

- **실행·화면 확인을 하지 않았다.** E2E-3 의 「진행+hover = 파랑」은 CSS 명시도와 순서를 읽고 내린 판정이다. 실제 브라우저 계산 스타일(특히 Tauri WebKit)로는 확인하지 않았다. 포인터를 단추 밖으로 옮기면 회색이 된다는 것도 같은 추론이다.
- **E2E-1 의 데이터 쪽 원인**(AI 가 체크리스트를 비운 이유 · 운영 초안 payload 실값)은 FE 코드로 답할 수 없다. 서버 프롬프트·도구 설명·운영 DB 는 BE 리포트 몫이다. 운영 서버에는 접속하지 않았다.
- **E2E-2 의 「초안 저장」 서버 동작**: 확정 없이 values 를 바꾸는 명령이 없다는 것은 `policy.py:114-128` 과 FE `api.ts` 를 읽어 확인했다. 다른 서버 경로(예: submission 회차를 올리는 내부 함수)가 쓸 수 있는 형태로 있는지는 BE 리포트에 맡긴다. 카드가 「최신 submission snapshot」을 그리는 조건(`action_center.py:705` 의 `version`/`recovery_payload`)도 자세히 따지지 않았다.
- **E2E-4 「자기 자신 업무로 보인다」**: 링크 글자가 업무 제목과 같은 이유는 서버 `subject_label` 이 payload `title` 을 쓰기 때문이다(코드로 확인). 운영 화면에서 실제로 무엇이 열렸는지는 직접 보지 않았다. 홈·캘린더에서 연 상세는 링크가 아니라 글자다(§4-2).
- **E2E-5 표**의 일부 줄 번호(캘린더·프로젝트·요청 상세·ActionCenter 세부)는 조사 보조 에이전트가 찾았다. 그중 `InboxRail:71` · `WorkTables:544/573/654` · `WorkModals:5360-5388, 4650-4651` · `WorkViews:150-160` · `DueCell` · `taskWhen` 두 벌 · `CalendarRail:71-73` · `DueText` 렌더 0곳은 직접 다시 확인했다. 나머지는 이 수준으로 재확인하지 않았다.
- 「시작」「기간」「종료」 낱말 개수에는 상태 낱말(시작 전·회의 시작 등)과 주석이 섞여 있어, 날짜 라벨 개수로 그대로 읽으면 안 된다.
- 테스트 파일(79개)은 개수에서 뺐다. 테스트가 단언하는 문구(예: 「등록」)가 몇 곳인지는 세지 않았다.
