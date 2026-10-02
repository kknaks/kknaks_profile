# 고도화 1차 프론트 전수조사

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` @ `015bed2` (origin/main)
- 방식: 읽기 전용. 코드·테스트·빌드·서버 실행 없음. 경로는 별도 표기가 없으면 `frontend/src/` 기준.
- 숫자는 `grep -rnoF <심볼> src index.html` 에서 `*.test.*` 를 뺀 값이다(§9).

---

## 0. 한 줄 요약 — 요청별 한 줄

| 요청 | 한 줄 |
|---|---|
| F-01 | 담당자 변경 폼은 `TaskDetailDrawer` 안에서 펼쳐지는 `.link-draft` 블록이다(`WorkModals.tsx:2324-2366`). 제출하면 `POST /api/tasks/{id}/reassign` 를 부른다. 같은 인라인 폼 패턴은 소스 2개(담당자 변경·자료 링크 추가), 화면 3자리다. `Modal` 은 `size: "sm"(420)\|"md"(560)` 를 지원하고, 모달 위 모달은 형제 렌더 + ESC 스택(`useEscape`)으로 이미 7종이 겹쳐 뜬다. |
| F-02 | 전역 입력 기본 규칙(`components.css:737`)이 `type="search"` 를 셀렉터에서 뺐다. `.search-input-box`(`components.css:487`)·`.scax-chat__search`(`ax.css:116`)에는 테두리·반경·appearance 가 없다. 그래서 앱 전체에서 하나뿐인 `type="search"`(`ChatDrawer.tsx:258`)가 브라우저/WebKit 기본 모양으로 그려진다. |
| F-03 | 간트 범위는 `ganttAxis`(`projectModel.ts:237-248`)가 정한다. 규칙은 `span_from` 최솟값 ~ `span_to` 최댓값이고, 패딩·최소일수·오늘 포함 규칙이 없다. 34/200 은 `GANTT` 상수(`projectModel.ts:20-36`)다. 다른 화면과 공유하지 않는다. |
| D-01 | `TaskTimeline`(`WorkViews.tsx:387-482`)은 오늘-7일부터 14일 고정 창(2주 스테퍼, "오늘" 버튼 없음)을 그리는 CSS grid 다. 원본 날짜는 `start_date/due_date` 다. 간트와는 날짜 유틸 4개만 공유하는 별도 구현이다. |
| D-02 | 업무 생성 카드는 `ActionTaskCard`(`ActionTaskCard.tsx:464`)다. `data-view` 는 `editing\|pending\|approved\|rejected` 이다. 「수정」은 로컬 편집이고, 「등록」은 `POST /api/action-items/{id}/commands/confirm` 이다. `scax-actioncard` 계열은 4종이다. 「SC AX」 문자열은 화면에 2자리 남아 있다(`ActionTaskCard.tsx:467` 배지, `:934` placeholder). |
| A-01 | action item 을 목록으로 그리는 화면은 홈 하나다(`GET /api/action-items`, 필터 없음). 채팅은 대화 응답의 `actions` 로 같은 id 를 따로 그린다. 업무 상세는 `task.delivery` 만 클라이언트에서 골라 쓴다. `ax.*` 전용 분기는 0곳이다. 수신함·업무 탭에는 action item 이 없다. |
| B-01 | 라우팅은 `useState` 의 surface 전환 + 조건부 렌더(`App.tsx:75, 476-575`)라서 탭을 옮길 때마다 페이지와 레일이 언마운트된다. 데이터 캐시가 0이라 진입 때마다 재조회하고, 지연 없는 스켈레톤이 뜬다. 내 업무는 진입 때 최대 9콜을 부르고 3자리에 스켈레톤을 띄운다. |
| B-02 | 참조자 칩은 `ccCandidates.filter(c => c.id !== assigneeId)`(`WorkModals.tsx:5227-5228`)로 걸러진다. 「내 업무」 갈래에서는 `assigneeId` 가 숨겨진 채 `assigneeCandidates[0]` 로 초기화된다(`:4387`). 그래서 담당자 후보 첫 번째 사람이 참조자 목록에서 빠진다. 1인 누락을 설명하는 코드상 가장 유력한 지점이다. |

---

## 1. F-01 업무 상세 › 담당자 변경 폼

### 1-1. 컴포넌트·상태·제출·API
- **컴포넌트**: `TaskDetailDrawer`(`features/work/WorkModals.tsx:601`).
  - 껍데기 `Shell` 은 `Modal` 또는 `Drawer` 다(`:1752`). 기본값은 `presentation = "modal"`(`:620`)이고, 내 업무가 `presentation="modal"` 로 연다(`MyWorkPage.tsx:1262`).
- **노출 조건**: `canAssign && !readOnly`(`WorkModals.tsx:2324`).
  - `canAssign` 기본값은 `false`(`:603`)다. 유일한 호출부가 `detail.manage && Boolean(canAssignTasks)` 를 넘긴다(`MyWorkPage.tsx:1242`).
- **상태**
  - `handover: { assigneeId: string; reason: string } | null`(`WorkModals.tsx:748`)
  - `handoverChoices: Persona[] | null`(`:749`)
- **열기/닫기 `openHandover`**(`:1228-1241`)
  - 폼이 열려 있으면 닫는다.
  - 닫혀 있으면 `{assigneeId:"", reason:""}` 로 연다.
  - 처음 열 때만 `getTaskAssignmentCandidates()` 를 부르고, 실패하면 목록을 `[]` 로 둔다.
- **제출 `submitHandover`**(`:1243-1264`)
  - 대상이 없으면 「옮길 담당자를 골라 주세요.」를 띄운다.
  - 대상이 있으면 `reassignTask(task_id, version, assigneeId, reason.trim() || undefined)`(`:1250`)를 부른다.
  - 성공하면 폼을 닫고 「담당 변경을 제안했습니다…」 알림을 띄운 뒤(`:1254`), `onChanged` 를 부르고 `getTaskAssignments` 를 다시 읽는다.
- **마크업**(`:2324-2366`)
  - `div.handover` 안에 텍스트 버튼 「담당자 변경」(`:2328-2330`)이 있다.
  - 그 아래 `div.form-stack.link-draft`(`:2332`)가 펼쳐지고, 안에는 다음이 있다.
    - `Select#task-handover-${task_id}`(`:2338`)
    - `input#task-handover-reason-${task_id}`(`:2349`)
    - `.row-actions` 의 「변경」·「취소」(`:2355-2362`)
  - 문구는 컴포넌트에 직접 박혀 있다. `labels.ts:36` 에는 `awaiting_handover: "담당 변경 대기"` 하나뿐이다.
- **CSS**: `.handover`(`styles/screens-a.css:433`), `.link-draft`(`:434`, 패딩 12 + 테두리 + surface-alt 배경), `.link-draft .row-actions`(`:435`)
- **API**
  - 제출: `reassignTask`(`lib/api.ts:349-359`) → `POST /api/tasks/{taskId}/reassign`. body 는 `{expected_version, assignee_id, reason?}` 이고 `TaskAssignment` 를 돌려받는다.
  - 후보: `getTaskAssignmentCandidates`(`api.ts:1006`) → `GET /api/task-assignment-candidates`. 조건은 §8-3.

### 1-2. 「인라인으로 펼치는 폼」 패턴 전부
- **`.link-draft` 토글 폼은 소스 2곳, 화면 3자리**이고, 모두 업무 상세 안에 있다.
  1. `WorkModals.tsx:2332`: 담당자 변경(위 1-1)
  2. `WorkModals.tsx:1674`: 자료 「링크 추가」 폼
     - 상태는 `linkDraft`(`:704`)이고 `:1664` 에서 토글한다.
     - 이 폼을 담은 `renderMaterials`(`:1636`)가 입력·산출물 두 번 호출된다(`:2795-2796`). 그래서 화면에는 2자리지만 동시에는 하나만 열린다.
- **`form-stack` 사용**: TSX 5곳
  - `WorkModals.tsx:1674, 2332, 3893`
  - `org/AccessDrawer.tsx:96`
  - `meetings/BookingModal.tsx:297`
  - 기본 규칙은 `components.css:482` 다.
- **업무 상세 안의 다른 토글식 인라인 편집**
  - `metaEditing`(`WorkModals.tsx:744`): 버튼 `:1876`, 패널 `:1934`·`:1978`·`:2032`
  - `relDraft` 관계 편집 모드(`:1365`)
  - `RelationAddRow`(`:566-598`, `rel__addrow`)는 토글이 아니라 항상 보인다.
- **업무 상세 밖의 항상 보이는 추가 행**: `scax-create-add-row`(`WorkModals.tsx:5292, 5536`), `action-task-add-row`(`action/ActionTaskCard.tsx:213`). 이것들은 펼침 폼이 아니다.

### 1-3. 기존 모달 부품 구조와 모달-위-모달 선례
- **`ds/Modal.tsx`**
  - 공통 props `OverlayShellProps`(`:49-63`): `label, kicker?, title, headerExtra?, footer?, onClose, closeLabel, onBack?, backLabel?, children`
  - `Modal`(`:148-185`)은 `size?: "sm"|"md"`, `className?` 을 더 받는다.
  - `Drawer`(`:85-93`)는 `size?: "sm"|"lg"`(기본 `lg`)를 더 받는다.
  - `ConfirmModal`(`:223-229`)도 같은 파일에 있다.
  - DOM: `div.scax-modal-overlay` > `section.scax-modal[role=dialog][aria-modal]` > `__head` / `__body` / `__foot?`(`:159-185`). 클래스 문자열은 `:168` 에서 조립한다.
- **ESC**
  - 모듈 수준 스택 `escapeLayers`(`:15`)가 있다.
  - `useEscape`(`:18-40`)는 window `keydown` 리스너를 걸고, 스택 최상단 레이어일 때만 닫는다(`:30`).
  - 레이어를 등록하는 곳: `Modal`·`Drawer`·`ConfirmModal`(`:94, :157, :223`), `Popover`(`Popover.tsx:90`).
- **오버레이 클릭**: `onMouseDown` 에서 `target === currentTarget` 일 때만 닫는다(`:161-163`).
- **없는 것**
  - 포털이 없다. `createPortal` 은 `Popover.tsx:146`·`ActionTaskCard.tsx:755`·`MeetingDetailPage.tsx:922` 에만 있다.
  - 포커스 트랩·body 스크롤 잠금이 없다(`body.style`·`focusTrap`·`inert` grep 0).
  - 초기 포커스는 `ConfirmModal` 의 × 버튼 `autoFocus`(`:229`) 하나뿐이다.
- **z-index**
  - 50: `.scax-modal-overlay`(`components.css:247`), `.scax-drawer-overlay`(`workspace.css:102`), `.modal-backdrop`(`components.css:521`)
  - 60: toast(`components.css:338, 340`)
  - 80: 자료 고르기(`ax.css:475`)
  - 90: popover(`components.css:62`). 이 줄 주석에 「모달 50 · 겹친 확인 60 · 자료 고르기 80」이 적혀 있다.
- **모달-위-모달 선례: 있다.** 업무 상세 `</Shell>`(`WorkModals.tsx:2807`) 뒤에 아래가 형제로 렌더되어 위에 겹친다.
  - `CompletionReportModal`(`:2815`)
  - `ConfirmModal`(`:2834`)
  - `ReasonPrompt` ×5(`:2858, 2878, 2904, 2926, 2944`)
  - `TermsChangePrompt`(`:2893`)
  - `CreateWorkModal`(하위 업무 요청, `:2961`)

  모두 z-index 가 50으로 같아서 DOM 순서로 위아래가 정해진다.
- **겹쳤을 때의 ESC**
  - `Modal`/`ConfirmModal`/`useEscape` 를 쓰는 것은 최상단만 닫힌다.
  - `ReasonPrompt`(`:3183`)는 맨 `.modal-backdrop`(`:3229`)을 쓰고 레이어 등록을 하지 않는다. ESC 는 input `onKeyDown`(`:3242-3244`)에서만 처리하고 `stopPropagation` 이 없다. 그래서 아래 Shell 의 window 리스너(스택 최상단)도 같은 ESC 에 반응할 수 있다. 코드로 읽은 결론이고 실행 확인은 안 했다(§10).
- **회의 쪽은 다른 패턴을 쓴다**: 확인창에 인라인 `style={{ zIndex: 60 }}` 을 주고, 부모의 `useEscape` 를 끈다.
  - `AttachModal.tsx:73/175`
  - `BookingModal.tsx:189/543`
  - `ShareModal.tsx:55/180/198`
  - `MeetingEditModal.tsx:113/255`
- **맨 `.modal-backdrop` 사용**: `className="modal-backdrop` TSX 16곳, 8파일(CSS 제외).
- **DS 문서 규칙**
  - `docs/design/design-system-v2.dc.html:573`·`:1601`: 「드로어 위에 모달을 겹치지 않습니다」
  - `:1525`: 「편집 폼은 모달로 만들지 않습니다」

### 1-4. 작은 크기 모달 변형
- **코드: 있다.** `Modal` 의 `size?: "sm"|"md"`(`Modal.tsx:150`). 주석 기준 기본 880, `md` 560, `sm` 420(`:129`).
  - `ConfirmModal` 은 `scax-modal--sm` 을 고정으로 쓴다(`:226`).
  - `--create` 는 `className` 으로 붙인다(`WorkModals.tsx:5004`).
- **CSS**
  - `.scax-modal`: 880 × `min(720px, …)`(`components.css:256`)
  - `--sm`: 420, height auto(`:271`)
  - `--md`: 560, height auto(`workspace.css:118`)
  - `--create`: 880 × `min(680px, …)`(`components.css:795`), `--create.--md` 620(`:797`)
  - 구 `.modal`: `min(600px, 100%)`(`components.css:522`)
  - Drawer: `--sm` 520 · `--lg` 840(`Modal.tsx:71-75`)
- **DS 문서**: `docs/design/README.md` 에는 "modal" 이 0건이다. `design-system-v2.dc.html` 의 "Modal" 3건(`:403, :704, :1524`)은 모두 600px 단일 규격이고, 크기 단계나 중첩 규격은 없다.

---

## 2. F-02 AX 대화 › 「대화 검색」 입력

### 2-1. CSS 정의 위치와 적용이 안 되는 이유
- **마크업**: `features/chat/ChatDrawer.tsx:253-260`. 클래스는 `className="scax-chat__search search-input-box"`, `type="search"`, `aria-label="대화 검색"`.
- **정의**
  - `.scax-chat__search{flex:none;height:42px;padding:0 var(--scax-space-300);font-size:var(--scax-text-label2-size)}`(`styles/ax.css:116`)
  - `.search-input-box { height: 34px; padding: 0 12px; font-size: 13px; }`(`styles/components.css:487`). 주석 `:485-486` 에 돋보기 자리는 비워 둔다고 적혀 있다.
  - **두 규칙 모두 `border`·`border-radius`·`background`·`appearance` 를 선언하지 않는다.**
- **원인: 전역 입력 기본값이 search 타입을 빼고 있다.**
  - 전역 규칙: `input[type="text"],input:not([type]),input[type="date"],select,textarea{…border:1px solid var(--scax-color-line-strong);border-radius:var(--scax-radius-sm);…}`(`components.css:737`)
  - 이 규칙의 셀렉터에 `type="search"` 가 없다. 그래서 테두리·반경을 주는 곳이 하나도 없고, UA 기본값(Chrome 기준 `2px inset`, radius 0)이 남는다. 운영 computed 값과 같다.
  - 같은 구획 주석(`:730-734`)에 「앱의 입력칸 67자리가 아직 맨 element 다… 이 다섯 줄이 사라지면 브라우저 기본 모양으로 벗겨진다」가 적혀 있다.
- **로드 순서는 원인이 아니다.**
  - `main.tsx:4` 가 `styles/index.css` 하나를 읽는다. 그 안에서 `components.css` 가 `ax.css` 보다 먼저 `@import` 된다(`index.css` 구획 주석 참조).
  - 두 클래스 규칙은 모두 적용되지만, 선언한 속성 자체가 높이·패딩·글자 크기뿐이다.
- **포커스**: 전역 `:focus,:focus-visible{outline:none}`(`shell.css:67`)이 외곽선을 지운다. 맨 input 용 focus 규칙(`input:focus…`)은 `components.css` 에 없다. 그래서 이 입력은 포커스 표시도 없다.

### 2-2. `type="search"` 와 검색칸 클래스를 쓰는 곳 전부
| # | 자리 | 파일:줄 | type | DS 모양이 먹나 |
|---|---|---|---|---|
| 1 | AX 대화 히스토리 검색 | `features/chat/ChatDrawer.tsx:254-258` | **search** | **안 먹는다**. 전역 `:737` 이 안 잡고 클래스는 테두리가 없다. |
| 2 | Select 내부 검색 | `ds/Select.tsx:272,282` (`.search-input-box`) | text | 테두리·반경은 전역 `:737`, 크기는 `.search-input-box` 가 준다(h34). |
| 3 | 회의 PeoplePicker | `features/meetings/PeoplePicker.tsx:41,47` (`.search-input-box`) | text | 위와 같다. |
| 4 | 조직도 이름 검색 | `features/org/OrgTreePanel.tsx:88-95` (`.scax-textfield` > `__input`) | text | DS 텍스트필드 골격(`components.css:292-295`). 테두리는 껍데기가, 입력은 `border:0` 이다. |
| 5 | 관계 그래프 검색 | `features/graph/RelationGraphPage.tsx:192-194` (`.scax-textfield.graph-search-field`) | (text) | 4와 같다. `.graph-search-field` 는 `screens-b.css:555` 에 있다. |
| 6 | 프로젝트 멤버 자동완성 | `features/project/ProjectManageModal.tsx:252-256` (`.scax-textfield.scax-textfield--search`) | (text) | 4와 같다. **`scax-textfield--search` 의 CSS 정의는 0건**이다. |

- 집계(테스트 제외)
  - `type="search"`: 1곳
  - `search-input-box`: 7건 / 6파일. 마크업 3(위 1·2·3), 나머지는 CSS 1과 주석이다.
  - `scax-chat__search`: 2건(TSX 1, CSS 1)
- 참고로 다른 비-text 타입도 셌다. `email` 1·`password` 1(`LoginPage.tsx:135,150`, 둘 다 `.scax-textfield__input`), `time` 1, `datetime-local` 2. 이 중 `datetime-local` 은 `ax.css:612` 가 따로 칠한다.

### 2-3. DS 의 검색 입력 부품
- **DS 문서**: `docs/design/design-system-v2.dc.html:922-923` 에 「Search · h34 · w260」 규격이 있다. 1px `#D4D8E0` 테두리, radius 8, 14px 돋보기 아이콘, gap 8, 패딩 0 12, 13px.
- **코드에는 부품(컴포넌트)이 없다.**
  - `ds/FormControls.tsx:9-10` 주석: 「Search(h34)는 자리가 하나뿐이라 컴포넌트 대신 `.search-input-box` 규격만 남겼다」
  - 실제 `.search-input-box` 는 높이·패딩·글자 크기만 옮겼고, 테두리·반경·아이콘은 없다(`components.css:487`).
- **DS 텍스트필드 골격** `.scax-textfield`(`components.css:292-298`)은 TSX 6파일에서 쓴다. OrgTreePanel, LoginPage, ProjectManageModal, RelationGraphPage, ProjectCreateModal 등이고, `scax-textfield__input` 은 15건 / 7파일이다. 컴포넌트(TextField)는 없고 클래스를 직접 쓴다(`OrgTreePanel.tsx:85-87` 주석).

### 2-4. WebKit(Tauri) 차이를 만들 만한 것
- `-webkit-appearance` 는 1건이다. `.scax-textfield__input--date{appearance:none;-webkit-appearance:none}`(`components.css:296`)으로 date 전용이다.
- `::-webkit-search-*`(cancel-button, decoration 등) 처리는 **0건**이다.
- 그래서 `type="search"` 에 대해 `appearance` 리셋이 없고, WebKit 기본 `searchfield` 외형과 취소 버튼이 그대로 남는다. Chrome 기본(`2px inset`)과 모양이 달라질 수 있다.
- **Tauri 는 같은 운영 origin 을 그대로 띄운다.**
  - `src-tauri/tauri.conf.json:5-6` 은 `frontendDist: "shell-noop"` 이다.
  - `src-tauri/src/config.rs:12` 에 회사판은 `https://ax.medisolveai.xyz` 라고 적혀 있다.
  - 즉 같은 CSS를 쓰므로, 차이는 엔진(WKWebView) 기본값에서 온다.
  - 실제 WebKit 렌더 모습은 실행 확인을 안 했다(§10).

---

## 3. F-03 프로젝트 상세 › 진행 라인 간트

### 3-1. 표시 범위 계산과 현재 규칙
- **호출**: `ProjectPage.tsx:450-459` 가 `ProjectGantt` 를 렌더한다.
  - `tasks = selected?.tasks ?? []`(`:132`)
  - `today = useMemo(() => seoulToday(), [])`(`:93`)로, 마운트 때 한 번 계산한다.
- **`ganttAxis`(`features/project/projectModel.ts:237-248`)**
  - `tasks.filter(hasSpan)`: `span_from && span_to` 가 둘 다 있는 업무만 쓴다(`:211-213`, `:238`).
  - `from` 은 `span_from` 최솟값, `to` 는 `span_to` 최댓값이다(`:240-245`).
  - `days` 는 `dayDifference(from,to)+1` 일이다(`:246-247`).
- **현재 규칙은 "업무 기간의 최소~최대" 뿐이다.**
  - 앞뒤 패딩이 없다.
  - 최소 일수가 없다.
  - 오늘을 범위에 강제로 넣지 않는다.
  - 접힌 가지와 취소 업무도 범위에 들어간다. 전체 `tasks` 를 넘기기 때문이다(`ProjectGantt.tsx:58`).
- **날짜 원천**: 원본 `start_date/due_date` 가 아니라 서버가 정규화한 `span_from/span_to` 다(`projectModel.ts:10-12` 주석, `lib/viewModels.ts:126`).
  - 마감만 있는 업무는 하루 span 으로 오고, 뒤집힌 기간은 `[min,max]` 로 온다(`projectModel.test.ts:140-149`).
- **기간 있는 업무가 0개일 때**: `null` 을 돌려준다(`:239`). 그러면 `Empty`「기간이 정해진 업무가 없습니다」가 뜬다(`ProjectGantt.tsx:81-82`, `labels.ts:1118-1119`).
- **헤더 범위 라벨**: `"YYYY/MM/DD ~ YYYY/MM/DD"`(`ProjectGantt.tsx:71`, `labels.ts:1117`)
- **막대 좌표 `barGeometry`**(`projectModel.ts:251-256`): `left = GANTT.label + start*GANTT.day`, `width = (end-start+1)*GANTT.day`

### 3-2. 하루 폭·이름 열·가로 스크롤·오늘 표시
- **상수 `GANTT`**(`projectModel.ts:20-36`)
  - `day: 34`(`:22`)
  - `row: 40`(`:24`)
  - `label: 200`(`:26`)
  - `indent: 12`(`:28`)
  - `maxIndentDepth: 5`(`:30`)
  - `openLead: 2`(`:35`)
- **캔버스 크기**: 폭 `GANTT.label + days*GANTT.day`, 높이 `rows*GANTT.row`(`ProjectGantt.tsx:118-119`). 폭은 `__canvas` 에 인라인으로 준다(`:169`).
- **칸 크기**
  - `__day` 는 인라인 `width: GANTT.day`(`:178`)
  - axis pad 는 `width: GANTT.label`(`:173`)
  - grid 배경은 `backgroundSize: ${day}px ${row}px`(`:185`)
- **가로 스크롤**
  - `.scax-pj-gantt__scroll{overflow-x:auto}`(`styles/projects.css:81`)
  - axis pad 와 이름 칸은 sticky `left:0`(`projects.css:86`, `:112`)
- **처음 열 때 스크롤 위치**
  - `openOffset = clamp(오늘 offset, 0, days-1)`, `openLeft = max(0,(openOffset - openLead)*day)`(`ProjectGantt.tsx:141-142`)
  - `projectId` 가 바뀔 때만 적용된다(`:145-151`).
  - 업무를 고르면 그 행을 `nearest` 로 보여 준다(`:161-165`).
- **오늘 표시**
  - `offset = dayDifference(axis.from, today)`(`:127`)
  - 범위 안일 때만 `nowLeft` 를 계산하고, 밖이면 `null` 이다(`:128`).
  - 표시는 `span.scax-pj-gantt__now`(`:186`)이고, CSS 는 `projects.css:97`(accent-05 배경)이다.
  - 헤더 칸에는 `__day--today`(`:176`)가 붙고, CSS 는 `projects.css:88` 이다.
- `projects.css:92` 주석에 나오는 `--scax-pj-gantt-day` 커스텀 속성은 정의가 0건이다.

### 3-3. 범위 계산을 공유하는 다른 화면
- **없다.** `ganttAxis`·`barGeometry` 는 `projectModel.ts`·`ProjectGantt.tsx`·`projectModel.test.ts` 에서만 쓴다.
- 내 업무 타임라인은 `projectModel` 을 import 하지 않는다(§4-2).

---

## 4. D-01 내 업무 › 타임라인 (현재 상태)

### 4-1. 구조·범위 규칙·범례·막대 배치
- **컴포넌트**: `TaskTimeline({tasks, onOpen})`(`features/work/WorkViews.tsx:387-482`)
  - `tab === "mine" && view === "timeline"` 일 때만 렌더된다(`MyWorkPage.tsx:1108-1109`).
  - 뷰 종류는 `"list" | "timeline"`(`MyWorkPage.tsx:130,136`)이다.
- **DOM**
  - `div.timeline.work-timeline`(`:404`)
    - `div.calendar-toolbar`(`:405`)
      - `div.stepper`: 이전 / `<b>범위</b>` / 다음(`:406-416`)
      - `div.timeline-legend`(`:417-422`)
    - `div.timeline-scroll`(`:424`)
      - `div.timeline-grid[--days]`(`:425`)
        - `div.timeline-months`(`:426-429`)
        - `div.timeline-head`(`:430-437`)
        - 업무마다 `div.timeline-row`(`:446`)
          - `button.timeline-title`(`:447-457`)
          - `div.timeline-track`: `span.timeline-day` ×14, `button.timeline-bar?`(`:458-473`)
- **범위 규칙(2주 스테퍼)**
  - `today = seoulToday()`(`:388`), `offset` 초기값 0(`:389`)
  - `windowStart = addDays(today, -7 + offset*14)`(`:390`): 기본 창은 오늘-7일부터 14일이다.
  - `days` 14개(`:391`), `windowEnd` 는 마지막 날이다(`:392`).
  - 이전/다음 버튼이 `offset ∓ 1` 이다(라벨 「이전 2주」·「다음 2주」, `:407`·`:413`).
  - **타임라인에는 「오늘」 복귀 버튼이 없다**(`:405-423`). 캘린더 뷰 툴바에는 있다(`:322`).
  - 범위 라벨은 `formatDate(start) – formatDate(end)` 다(`:410-411`, `labels.ts:163-167`).
- **범례**: 하드코딩 4종(`:417-422`)
  | 범례 | 색 |
  |---|---|
  | 진행 중 `status in_progress` | `components.css:470-471` |
  | 막힘 `status blocked` | `components.css:474-475` |
  | 완료 `status done` | `components.css:472-473` |
  | 시작 전 `status open` | 전용 규칙 없음. 기본 `.status` 로 떨어진다(`:468-469`). |
  - `cancelled` 는 범례에 없다.
- **막대 날짜 `taskSpan`**(`WorkViews.tsx:175-181`)
  - `start = start_date ?? due_date`, `end = due_date ?? start_date`. 둘 다 없으면 null 이다.
  - `end < start` 이면 `end = start` 로 둔다. 서버의 `[min,max]` 정규화와 다른 방식이다.
- **배치**
  - `startIndex = max(0, dayDifference(windowStart, span.start))`(`:442`)
  - `endIndex = min(13, …end)`(`:443`)
  - `visible = span && startIndex<=13 && endIndex>=0`(`:444`)
  - 위치는 `gridColumn: ${startIndex+1} / ${endIndex+2}`(`:467`)
  - 막대 글자는 `taskStateLabel[state]`(`:471`), 클래스는 `timeline-bar ${state}`(`:465`)다.
  - 레인 패킹 없이 업무당 1행이다. 날짜가 없거나 창 밖이어도 행은 남고 막대만 없다(`:440` 주석).
- **빈 상태**: `tasks.length === 0` 일 때만 「이 기간에 표시할 업무가 없습니다.」(`:438`). 창 기준이 아니다.
- **오늘**: 헤더에 `.today` + `aria-current="date"`(`:433`, `screens-a.css:479`), 트랙에 `timeline-day today`(`:460`, `components.css:512`)
- **들어가는 업무**
  - `visibleTasks = visibleRows.flatMap(row => row.task ? [row.task] : [])`(`MyWorkPage.tsx:705`)
  - `visibleRows` 는 칩 필터를 거친다(`:700-703`).
  - `mineRows = myWorkRows(liveTasks, requestsToMe)`(`:696`)
  - `liveTasks` 는 done·cancelled 를 뺀다(`:693`).
  - 그래서 **완료 업무는 타임라인에 오지 않는다. 범례에는 「완료」가 있다.**
- **CSS**
  - 기본: `screens-a.css:377-389`. 이름 열 240, 막대 24.
  - `.work-timeline` 재정의: `screens-a.css:466-486`
    - `--timeline-label:200px`, `min-width: calc(200 + days*34px)`(`:474`)
    - 열 `minmax(34px,1fr)`(`:475, :484`)
    - 행 40(`:480`), 막대 22(`:485`)
    - `:466` 주석에 「프로젝트 간트 치수를 따른다」고 적혀 있다.
  - 막대 상태색: `components.css:513-516` 에 in_progress·done·blocked·cancelled 가 있다. open 은 기본색이다.

### 4-2. F-03 간트와 공유하는 코드
- **별도 구현이다.** 모델·상수·CSS 클래스를 공유하지 않는다.
  - 34/200 이 타임라인 CSS 에 리터럴로 다시 적혀 있다. `GANTT` 를 참조하지 않는다.
- **공유하는 것**은 `lib/labels.ts` 의 날짜 유틸 4개뿐이다: `addDays`(`:216-220`), `dayDifference`(`:222-226`), `formatDate`(`:163-167`), `seoulToday`(`:158-160`).
  - import 위치: `ProjectGantt.tsx:5`, `projectModel.ts:1`, `WorkViews.tsx:7`
- **차이**
  | 항목 | 간트 | 타임라인 |
  |---|---|---|
  | 날짜 필드 | `span_from/to` | `start_date/due_date` |
  | 범위 | 데이터에서 계산 | 오늘 기준 14일 고정 |
  | 배치 | 절대 px | CSS grid |
  | 오늘 | prop 으로 받음 | 직접 호출 |
- `taskSpan` 은 캘린더 뷰 `weekSegments`(`WorkViews.tsx:209`)도 쓴다. 캘린더 페이지는 쓰지 않는다고 주석에 적혀 있다(`calendarModel.ts:11`, `CalendarPage.tsx:96`).

---

## 5. D-02 AX 대화 › 업무 생성 액션카드 (현재 상태)

### 5-1. 카드 구조·상태·「수정」「등록」·API
- **렌더 위치**: `features/chat/MessageList.tsx:307-314`
  - 조건은 `action.edit_contract?.editor === "task"` 다.
  - 핸들러는 `onCommand = (command, payload) => onDecide(action.action_id, action.version, command, payload)` 다.
- **구조**(`features/action/ActionTaskCard.tsx:456-613`)
  - 섹션 앞: `div.action-task-request-target`(아바타 + 대상 이름). `action_type === "task.assign" && state === "pending"` 일 때만 보인다(`:320`, `:458-463`).
  - `section.scax-actioncard.action-task-card[data-action-id][data-state][data-view]`(`:464`)
    - `div.action-task-content`(`:465`)
      - `div.scax-actioncard__badges`: `<Badge tone="info">SC AX</Badge>` + 상태 배지(`:466-469`)
      - 읽기 모드: `TaskSummary`(`:507`, 정의 `:50-83`) + `TaskAttachmentGroup`(`:508-526`)
        - `TaskSummary` 는 제목·설명·`dl`(담당·마감, `task.assign`·`work_request.create` 면 요청자 추가)·체크리스트를 그린다.
      - 편집 모드: (stale 이면 `StaleTaskDraft`) + `TaskDraftFields` + 편집 가능한 `TaskAttachmentGroup`(`:470-504`)
      - 오류: `p.action-task-error[role=alert]`(`:529`)
    - `div.action-task-actions`(`:531-589`)
  - 섹션 뒤
    - `p.action-task-completion-note`「업무가 등록되었습니다.」: `task.create_self && approved && taskId` 일 때(`:591-593`)
    - 요청형 완료 안내(`:594-611`)
- **상태 배지 값**(`:440-454`): 요청 · 초안 · 취소됨 · 거절됨 · 수락됨 · 내 업무 · 승인됨 · 거절됨
- **`data-state`** = `action.state`. 타입은 `"pending" | "approved" | "rejected"`(`lib/viewModels.ts:757`)다.
- **`data-view`** = `editing ? "editing" : action.state`(`:464`)로, **`editing | pending | approved | rejected` 4값**이다.
  - `editing` 초기값은 `recovered.restored`(`:299`)다. 로컬에 저장해 둔 초안을 복원하면 true 로 시작한다.
  - pending 이 아니게 되면 강제로 false 가 된다(`:342-344`).
- **「수정」**(`:532-534`)
  - 보이는 조건: `state === "pending" && contract && !editing`
  - 하는 일은 `setEditing(true)` 하나다. **API 호출이 없다.**
  - 편집 초안은 localStorage `scax.ax.action-drafts.v1` 에 둔다(`work/useActionDraft.ts:3, 29, 42`).
  - 편집 중에는 「취소」(`recovered.reset()` 후 편집 종료, `:537-542`)와 「초기화」(`:543`)가 생긴다.
  - 카드 안 첨부는 API 를 부른다.
    - `stageActionMaterialLink`: `POST /api/action-items/{id}/material-drafts/links`(`api.ts:1119-1127`, 호출 `:400`)
    - `stageActionMaterialFile`: `…/material-drafts/files`(`api.ts:1129-1133`, 호출 `:415`)
    - `discardActionMaterialDraft`(`:429`)
- **「등록」**(`:546-570`)
  - 보이는 조건: 서버가 `confirm` command 를 주고(`:323`) contract 가 있을 때
  - 라벨: 「등록」, 편집 중 「저장」, 진행 중 「등록 중…/저장 중…」(`:568`)
  - 비활성 조건: busy, stale, 업로드 중, 업로드 실패(`:547`)
  - 먼저 필수값과 시작일 ≤ 마감일을 로컬에서 검사한다(`:357-369`). 실패하면 편집 모드로 바꾸고 해당 필드에 포커스한다.
  - 검사를 통과하면 `run("confirm", {...}, clearDraft=true)`(`:558-564`)를 부른다. payload 는 다음과 같다.
    - `base_submission_version`
    - `draft?`: 편집했고 바뀐 경우만. `work_request.create` 면 contract 필드로 줄인다(`:102-105`).
    - `attachment_draft_ids?`
  - 호출 체인
    1. `onDecide`
    2. `App.decideConversationAction`(`App.tsx:329-351`)
    3. `chat.decide`(`useConversations.ts:338-345`)
    4. `decideAction`(`api.ts:731-745`)
       - `confirm`/`cancel_assignment` 는 `runActionCommand` → **`POST /api/action-items/{actionId}/commands/{command}`**, body `{expected_version, ...payload}`(`api.ts:737-739, 1103-1117`)
       - 그 밖의 결정은 `POST /api/actions/{id}/decide`(`api.ts:741-744`)
    5. 성공하면 `refreshProjections()` 를 부르고 토스트를 띄운다(`App.tsx:342-350`).
  - stale 오류면 「AX 초안이 갱신되었습니다…」를 띄운다(`ActionTaskCard.tsx:389`).
- **그 밖의 버튼**
  - 서버 command 중 **`confirm`·`reject` 를 뺀 나머지만** 그린다(`:571-583`). 그래서 업무 카드에는 거절 버튼이 없다.
  - 「요청내용 보기/업무 상세보기」: `taskId && onOpenTask` 일 때(`:584-588`)

### 5-2. `scax-actioncard` 계열 전부
- 선택 분기는 `MessageList.tsx:294-325` 에 있고, 기준은 `edit_contract?.editor` 다.
- `scax-actioncard` 는 TSX 14건 / 5파일(테스트 제외)이다.

| editor | 컴포넌트 | 클래스·속성 | 배지 |
|---|---|---|---|
| `"task"` | `ActionTaskCard` | `scax-actioncard action-task-card`, data-state·data-view (`ActionTaskCard.tsx:464`) | **SC AX** + 상태 |
| `"meeting"` | `ActionMeetingCard` | `scax-actioncard action-task-card action-meeting-card`, 같은 data-state/view (`ActionMeetingCard.tsx:239`) | 「회의」(`:242`). SC AX 배지 없음. 수정/등록/저장 동작은 task 카드와 같고(`:311-344`), confirm·reject 를 뺀다(`:346`). |
| `"task_progress_batch"` | `ActionProgressBatchCard` | `scax-actioncard action-progress-batch-card`, data-state 만 (`ActionProgressBatchCard.tsx:79`) | 「AX 제안 · {operation_label} · 승인 필요」(`:80`). 수정은 로컬(`:149`), 저장은 `confirm` + `{draft:{operations}}`(`:138-141`), 서버 라벨 확인 버튼(`:150-156`)과 거절 버튼(`:157`)이 있다. |
| 그 외(계약 없음 포함) | `ActionResultCard` | `scax-actioncard`, data-state 만 (`MessageList.tsx:632-655`) | 「{kicker} · 승인 필요」(`:635-638`). 서버 command 를 전부 그린다(`:648-652`). |
| `"command"` | **계열 밖**: `section.ax-action-card` + `CommandConfirmationForm` | `MessageList.tsx:294-300` | — |

- `ActionCenter.tsx`·`ActionPreview.tsx` 는 `scax-actioncard` 를 그리지 않는다.
  - `ActionPreview` 는 kicker 「AX 제안」/「AX 제안 · {label}」(`ActionPreview.tsx:13-15`)과 `details.scax-preview`(`:29`)만 준다.

### 5-3. 「SC AX」 문자열이 화면에 나가는 곳
- **화면 노출 2자리(소스)**
  1. `features/action/ActionTaskCard.tsx:467`: `<Badge tone="info">SC AX</Badge>`. **배지는 이것 하나다.**
  2. `features/action/ActionTaskCard.tsx:934`: 링크 첨부 입력 placeholder 「예: SC AX 디자인 가이드」
- **개발용 화면**: `dev/ProbePage.tsx:61` `<h1>SCAX 탐침 계측 — WORK-006 Phase 1</h1>`. probe 진입점(`probe.html`)으로만 뜬다.
- **파비콘**: `index.html:9` 의 SVG 가 「SC」 두 글자를 그린다.
- **비노출**
  - CSS 주석 `styles/index.css:1` 「TheSC AX Design System」
  - 저장 키 `scax.ax.drafts`(`useConversations.ts:36`), `scax.ax.action-drafts.v1`(`useActionDraft.ts:3`)
  - 기준 URL `http://scax.local`(`AssistantMarkdown.tsx:42`)
  - 코드 주석 여러 곳(`WorkModals.tsx:1673,1730`, `viewModels.ts:508,512,514`, `api.ts:336`)
  - `src-tauri` 스레드명·env 접두사(`power.rs:67`, `lib.rs:22,746`)
  - `labels.ts` 에는 SC AX 문자열이 0건이다.
- **MEDISOLVE 워드마크가 들어간 자리**
  - `index.html:6`(meta description), `:11`(title)
  - `App.tsx:415`: `logo="MEDISOLVE"` → `SideNav.tsx:189`(접히면 첫 글자, 기본값 "LOGO" `:82`)
  - `features/auth/LoginPage.tsx:63-66`(wordmark), `:74`(문장)
  - Tauri `productName` 은 「Strong Hajin」이다(`src-tauri/tauri.conf.json:3`).

---

## 6. A-01 AX 제안(초안 action)이 어디에 보이나

같은 id 가 두 경로로 그려진다.
- 홈: `ActionItemEnvelope.action_item_id` → `data-action-item-id`(`features/action/ActionCenter.tsx:85`)
- 채팅: 대화 응답의 `ActionItem.action_id` → `data-action-id`(`ActionTaskCard.tsx:464`)
- 두 쪽의 command 는 같은 엔드포인트 `/api/action-items/{id}/commands/{command}`(`api.ts:1113`)로 간다.

### 6-1. action item 을 받아 그리는 화면 전부
| 화면 | API | 서버 필터 | 클라이언트 필터 | 근거 |
|---|---|---|---|---|
| **홈(Today) 「오늘 나에게 요청된 업무」 열** | `getActionItems()` → `GET /api/action-items` | **쿼리 없음** | **없음**. `setActionItems(judgements)` 그대로 `ActionItemCard` 로 그린다. | `api.ts:1095-1097`, `TodayPage.tsx:100-107, 312-314` |
| 홈 카드 → 드로어 | `getActionItem` → `GET /api/action-items/{id}`, `runActionCommand` | — | — | `ActionCenter.tsx:360, 379-383`, `TodayPage.tsx:417-428` |
| **AX 채팅** | `getConversation` → `GET /api/conversations/{id}[?before_sequence]` 응답의 `conversation.actions` | — | `action.turn_id === turn.turn_id` 만. 카드 종류는 kind 가 아니라 `edit_contract.editor` 로 고른다. | `useConversations.ts:166,190`, `api.ts:708-710`, `MessageList.tsx:246, 294-325` |
| **업무 상세(완료 확인)** | `getActionItems()` | 쿼리 없음 | `kind === "task.delivery" && resource.id === task_id && status === "awaiting_review" && allowed_commands ∋ "accept"`. 조건 `awaitingReview && viewerIsRecordRequester` 일 때만 부른다. | `WorkModals.tsx:1104-1125`, command `:1138, :1151` |
| 내 업무 | **목록 없음**. `actionItems`/`setActionItems`/`selectedActionItem`(`MyWorkPage.tsx:206-207`)는 선언만 있고 쓰지 않는다. 업무의 출처가 `action_item` 일 때만 `ActionItemDrawer` 모달을 연다. | — | — | `MyWorkPage.tsx:656-660, 1260-1274` |
| 수신함(InboxRail) | **action item 을 담지 않는다** | — | — | `shell/InboxRail.tsx:15` 주석 「TaskReference와 AX 판단 항목은 이 목록의 원천이 아니다」 |

- 홈 카드(`ActionItemCard`, `ActionCenter.tsx:75-108`)
  - 마크업: `article.task-card.openable[data-action-item-id][data-kind=item.kind]`
  - 내용: kicker(`operation_label`), 상태, 제목, `current_question`, 회차, 「{waiting_on} 차례」, 「판단하기」
  - 상태 라벨(`:27-31`): awaiting_review「판단 대기」 / awaiting_revision「조정 필요」 / resolved「판단 완료」
- 홈 수치
  - `decisionCount = actionItems.length`(`TodayPage.tsx:248`)가 지표 「오늘 나에게 요청된 업무」(`:285`)와 같은 제목의 열(`:296-316`)에 들어간다.
  - 빈 문구는 「동료의 요청과 AX 제안이 오면 여기에 쌓입니다.」(`:308`)다.
  - `canReadActions` prop(`:43, :65`)은 요청을 막는 데 쓰이지 않는다.

### 6-2. `ax.*` kind 전용 분기
- **0곳.** 소스(테스트 제외)에서 `"ax.`·`'ax.`·`` `ax. ``·`startsWith("ax")` 는 0건이다(테스트 7줄).
- kind/type 분기가 있는 곳
  - `WorkModals.tsx:1117`: `item.kind === "task.delivery"`
  - `ActionTaskCard.tsx:52, 288, 318, 320, 591`: `action_type` 이 `task.assign`/`work_request.create`/`task.create_self` 인지 본다.
  - `ActionCenter.tsx:58`: `id === "ax"` 면 「AX」로 표시한다(참여자 이름).
- `data-kind` 출력은 `ActionCenter.tsx:85` 한 곳이고, 다시 읽는 곳은 없다.

### 6-3. 수신함과 업무 탭의 분류
- **수신함(InboxRail) `SegmentedControl`**: 전체 / 업무 / 참고
  - 라벨은 `labels.ts` 가 아니라 `InboxRail.tsx:110-112` 에 하드코딩되어 있다.
  - 업무·참고는 `item.category === filter`(`:37-38`)로 거른다. 카드 배지는 「업무 요청」/「참고」(`:62`)다.
  - 데이터: `requestInboxItems(inboxRequests, allRequests, personaId)` 에서 이번 세션에 읽은 항목을 뺀다(`MyWorkPage.tsx:898-900`).
    - `inboxRequests`: `getWorkRequestInbox()` → `GET /api/work-requests/inbox`. `canDecideWorkRequests` 일 때만 부르고, 아니면 `[]` 다(`MyWorkPage.tsx:264-279`, `api.ts:514-515`).
    - `allRequests`: `getWorkRequests(true)` → `GET /api/work-requests?include_removed=true`. 실패하면 `/api/work-requests` 로 다시 부른다(`MyWorkPage.tsx:293-305`, `api.ts:509-510`).
  - 분류 규칙(`work/requestInbox.ts:21-33`)
    - 요청 목록에서: `category==="reference"` 이거나, category 가 없고 본인이 `cc_member_ids` 에 있으면 참고
    - inbox 에서: 서버 category 가 우선이고, 없으면 `assignee_id===본인` 이면 업무, CC 면 참고
- **업무 탭**(`labels.ts:297-302` → `MyWorkPage.tsx:1056-1072`)

  | 탭 | 칩 | 데이터 출처 |
  |---|---|---|
  | 내 업무(mine) | 전체 · 받은 요청(`derived.assignment==="awaiting_acceptance"`) · 시작 전 · 진행 중 · 기한 지남 | `myWorkRows(liveTasks, requestsToMe)`(`:696`, `workRows.ts:257-271`). `getMyWork()`(`GET /api/my-work`) + `getTasks(true)`(`GET /api/tasks?include_closed=true`)를 합치고, 열린 요청에 묶인 업무는 뺀다(`:282-319`, `api.ts:151-156`). `requestsToMe` 는 `assignee_id===본인`(`:562`). done·cancelled 는 뺀다(`:694`). |
  | 보낸 업무(sent) | 전체 · 시작 안함 · 기한 지남 | `sentRequests`(`requester_id===본인`, `:563`) + `getSentTaskAssignments()`(`GET /api/task-assignments/sent`, `canAssignTasks` 일 때, `:306`, `api.ts:1024-1025`). 숨김 행은 뺀다(`:708-748`). |
  | 완료 업무(done) | 전체 · 확인 대기(`derived.approval==="awaiting_review"`) | done·cancelled 업무(`:695, :771-805`) |
  | 참조 업무(cc) | 전체 · 기한 지남 | `ccRequests`(본인 ∈ `cc_member_ids`, `:564, :808-845`) |

  - 칩 라벨은 `workChipLabel`(`labels.ts:272-280`)이다.
  - 탭별 칩 집합은 `labels.ts:282-289` 에 있고, `MyWorkPage.tsx:139-144` 에서 매핑한다.
  - 매칭 규칙은 `workRows.ts:278-299`, 개수는 `chipCounts`(`workRows.ts:304-308`)가 센다. 표시는 「{label} {count}」(`MyWorkPage.tsx:1082`)다.
  - **어느 탭·칩에도 action item 은 없다.**

---

## 7. B-01 탭 이동 때 화면 깜박임

### 7-1. 주요 화면의 데이터 로딩 — 캐시·전역 상태
- **캐시가 없다.**
  - `request<T>`(`lib/api.ts:127-144`)는 맨 `fetch` 래퍼이고, 캐시·메모·중복 제거가 없다.
  - SWR/react-query/스토어 같은 라이브러리가 없다(`package.json`).
  - React context 는 `BrowserOperationScope`(`lib/browserOperationGuard.ts:3`) 하나뿐이다.
- **App 이 들고 있는 탭 간 공유 데이터**
  - `getSession` 1회(`App.tsx:169-184`)
  - `getMemberDirectory` 세션당 1회 → `personas`(`App.tsx:186-199, 368`)
  - 대화 데이터: `useConversations`(`App.tsx:154`)
- 나머지는 **모든 페이지가 마운트마다 `useEffect` 로 다시 부른다.**

| 화면 | 진입 effect | 비고 |
|---|---|---|
| 홈 | `reload()` `TodayPage.tsx:113-125`(정의 `:99-111`), cc 후보 `:152-168`, 담당 후보 `:170-186` | 보고 생성 중에는 1초 폴링(`:127-143`) |
| 내 업무 | `reload()` `MyWorkPage.tsx:352-369`(정의 `:282-339`, `reloadInbox` `:264-280`), 후보 3종 `:401-453`, CalendarRail `onRange` → `getCalendar`(`CalendarRail.tsx:178-180` → `MyWorkPage.tsx:943-957`) | `railRange` ref 로 중복을 막지만(`:205, :945`) 리마운트되면 초기화된다. |
| 캘린더 | `reload()` → `getCalendar(range)` `CalendarPage.tsx:151-173` | 후보는 생성 모달을 열 때만 부른다(`:499-518`). |
| 프로젝트 | `reload()` + `getMemberDirectory()` `ProjectPage.tsx:126-130`, 업무 선택 시 `getTask` `:146-168` | App 이 이미 가진 멤버 목록을 다시 부른다. |
| 조직 | `Promise.all([getMyOrganizationProfile, getOrganizationTree])` `OrgPage.tsx:88-120`, 유닛 멤버 `:124-158`, 관리자일 때 `getInstalledAccessRoles` `:160-173`·`getOrganizationActivity` `:211-235` | |
| 보고 | `getTasks()`(실패하면 `getMyWork`) `DailyReportPage.tsx:103-120`, `loadReport({reset:true})` `:168-177`, 출처 제목용 N× `getTask` `:81-97` | 생성 중 1초 폴링(`:192-215`) |
| 회의 목록 | `listMeetings()` `MeetingListPage.tsx:62-76` | 선택 상태는 `MeetingWorkspace.tsx:52` 에 있고 리마운트하면 null 이 된다. |
| 회의 상세 | `readMeeting` `MeetingDetailPage.tsx:226-241` → `readMeetingTranscript`(`:268-280`)·`readMeetingMaterials`(`:283-295`) | 정착 폴링(`:445-453`), 1초 시계(`:437-441`), 스트림(`:414`) |
| 관계 그래프 | `graphOverview` `RelationGraphPage.tsx:56-74` | 사이드 메뉴에서 비활성(`App.tsx:47`) |
| AX 대화(드로어) | `isOpen` 이 될 때 `refreshConversations`(`useConversations.ts:205-208`) + `loadContextOptions`(`App.tsx:245-274`: `getMyWork`·`getWorkRequests`) | `loadContextOptions` 의존성에 `surface` 가 있어서(`:262`) 드로어가 열린 채 탭을 옮기면 다시 부른다. |

### 7-2. 스켈레톤을 띄우는 조건
- **스켈레톤에는 지연이 없다.** `ds/Skeleton.tsx:12-14` 주석에 따르면 구 0.4초 지연을 일부러 되살리지 않았다. 그래서 빠른 응답에도 한 번 번쩍인다.

| 화면 | 조건 | 이전 데이터가 있어도 띄우나 |
|---|---|---|
| 홈 | 스켈레톤 없음. 초기 `[]` 로 0 카운트와 `Empty` 를 그린 뒤 데이터로 바뀐다(`TodayPage.tsx:80-81, 306-308, 329-335`). | 진입마다 「빈 화면 → 데이터」가 된다. |
| 내 업무 | `loadState` 초기값 `"loading"`(`MyWorkPage.tsx:262`), 마운트 때 다시 `"loading"`(`:354`). 표 5곳(`:1129,1181,1196,1211,1221`) → `WorkTables.tsx:145`, InboxRail(`:977`, `InboxRail.tsx:46-47`), CalendarRail(`:987`, `CalendarRail.tsx:183-184`) | **띄운다.** `reloadInbox` 가 `reload()` 마다 `inboxState("loading")`(`:270`)를 넣는다. 그래서 변경 작업(`:464,482,500,520,541`)마다 InboxRail 이 기존 항목 위로 스켈레톤을 띄운다. |
| 캘린더 | `state` 초기값 `"loading"`(`CalendarPage.tsx:121`), 범위가 바뀔 때마다 `"loading"`(`:158`). ScheduleRail 은 `state==="loading"` 이면 스켈레톤(`ScheduleRail.tsx:50-51`) | **띄운다.** `entries` 는 비우지 않지만 레일은 스켈레톤이 된다. 본 그리드는 스켈레톤이 없다(`:606-627`). |
| 프로젝트 | `projects === null` 동안 레일을 등록하지 않는다(`ProjectPage.tsx:332, 341-343`). 목록을 넣은 뒤(`:108`) `loadProject` 를 await(`:111`)하고 `"ready"`(`:116`)로 바꾸는데, 그 사이 ProjectRail 이 스켈레톤이다(`ProjectRail.tsx:61-62`). 업무 패널은 `detailState==="loading" && checklist===null`(`ProjectTaskPanel.tsx:193-194`) | 진입 때는 「레일 없음 → 레일 스켈레톤 → 데이터」이고, 이후 reload 에서는 다시 띄우지 않는다. |
| 조직 | 트리 `units===null`(`OrgPage.tsx:363`, `OrgTreePanel.tsx:100-101`). 멤버 `members===null`, 유닛을 바꿀 때마다 null 로 되돌린다(`OrgPage.tsx:143`, `MemberListPanel.tsx:47-50`). 상세는 empty/error 가 아니면(`OrgPage.tsx:189`, `MemberAxesPanel.tsx:78-84`). 변경 로그 `events===null`, 로드마다 null(`OrgPage.tsx:215`, `ChangeLogPanel.tsx:36-39`) | 유닛을 바꾸거나 로그를 다시 부르면 기존 데이터를 지우고 띄운다. |
| 보고 | 스켈레톤 없음. 빈 문구 → 데이터(`DailyReportPage.tsx:335-336, 413-414`). `reset:true` 가 마운트·날짜 변경마다 초안·본문·이력을 비운다(`:132-137`). | 비우고 다시 그린다. |
| 회의 | 목록 `payload===null`(`MeetingListPage.tsx:214-216`). 상세 `!record || !meeting`(`MeetingDetailPage.tsx:515-519`)이고 reload effect 가 `setRecord(null)`(`:233`)을 한다. 자료 `materials===null`(`:883-884`) | 목록은 리마운트 때만, 상세는 다시 읽을 때마다 띄운다. |
| 관계 그래프 | `around===null && overview===null` 이면 텍스트 「관계를 불러오는 중…」(`RelationGraphPage.tsx:219-220`) | — |
| AX 대화 | `listStatus==="loading" && conversations.length===0`(`ChatDrawer.tsx:261-262`). 새로고침 중에는 `listStatus` 가 `"ready"` 로 남는다(`useConversations.ts:135`). | **띄우지 않는다.** 기존 데이터를 유지하는 유일한 화면이다. |

### 7-3. 라우팅과 언마운트
- **라우팅은 상태 하나다.** `const [surface, changeSurface] = useState<ProductSurface>("today")`(`App.tsx:75`)
  - `canNavigate` 가드를 거친다(`:110-115`).
  - `SideNav` 가 `onSelect(id)` 를 부른다(`App.tsx:417`, `SideNav.tsx:110,119`).
  - hash/history/router 가 없다. `pushState`·`popstate` 는 `dev/ProbePage.tsx:390,398` 에만 있다.
  - URL 은 `?interaction=` 만 읽는다(`App.tsx:62, 400-405`).
  - `surface ===` 분기는 18건, 모두 `App.tsx` 에 있다.
- **조건부 렌더**: `{surface === "today" && <TodayPage/>}` 형식이다(`App.tsx:476-575`). keep-alive 가 없다.
  - 그래서 **탭을 옮기면 이전 페이지가 언마운트**되고, 데이터·필터·탭·뷰·선택 상태를 모두 잃는다.
  - 같은 탭을 다시 누르면 React 가 같은 값 갱신을 생략하므로 리마운트하지 않는다.
- **레일도 함께 사라진다.**
  - App 의 `surfaceRails` 상태(`App.tsx:143-144`)에 페이지가 `useEffect` 로 레일을 등록하고, cleanup 에서 `onRegisterRails({})` 로 지운다.
    - `MyWorkPage.tsx:961-993`
    - `CalendarPage.tsx:459-477`
    - `ProjectPage.tsx:339-400`
    - `MeetingWorkspace.tsx:111-117`
  - `AppBody` 는 노드가 있을 때만 `<aside>` 를 그린다(`AppShell.tsx:77,79`).
  - 그래서 CalendarRail 자체 범위 상태, MeetingListPage 의 `payload` 같은 레일 상태도 탭 이동 때 사라진다.
  - 헤더 액션도 같은 방식이다(`surfaceActions`, `App.tsx:140,147`).
- **AX 대화 드로어**는 `{isAxOpen && <ChatDrawer/>}`(`App.tsx:632`)라서 조건부 렌더지만, 데이터는 App 의 훅에 남는다.
- **재조회 훅**: 각 페이지가 `surfaceRefresh` ref(`App.tsx:148-151`)에 자기 `reload` 를 등록한다.
  - `refreshProjections`(`:318-327`)만 부른다. AX 결정 후(`:342`)와 stale 토스트의 「다시 불러오기」(`:607`)에서다.
  - 리마운트 없이 다시 부르는 용도다(`:135-136` 주석).
  - 회의 목록과 상세가 같은 슬롯에 둘 다 등록한다(`MeetingListPage.tsx:78-81`, `MeetingDetailPage.tsx:243-246`).
- **dev 모드**: `<StrictMode>`(`main.tsx:7`) 때문에 진입 effect 가 2번씩 돈다. 운영 빌드에는 해당하지 않는다.

### 7-4. 화면 하나가 진입 때 부르는 API 개수 (운영 기준)
| 화면 | 개수 | 직렬/병렬 |
|---|---|---|
| 홈 | 최대 6 | 1단계 병렬 `getMyWork`·`getActionItems`·`getWorkRequests`(`TodayPage.tsx:100-104`). 별도 effect 로 cc 후보(`:158`)·담당 후보(`:176`). 2단계 직렬 `getDailyReportStatus`(`:110`, 권한이 있을 때) |
| 내 업무 | 최대 9(+실패 시 1) | `Promise.all`: `getMyWork`·`getTasks(true)`·`getWorkRequestInbox`(권한)·`getWorkRequests(true)`(실패하면 직렬로 `getWorkRequests()`, `:298-299`)·`getSentTaskAssignments`(권한)(`:283-307`). 별도 effect 후보 3종(`:407,:425,:443`). 레일이 마운트된 뒤 `getCalendar`(`:949`) |
| 캘린더 | 1 | `getCalendar`(`CalendarPage.tsx:152`) |
| 프로젝트 | 4, 2단계 | `listProjects` → `Promise.all([getProject, getProjectParticipationHistory])`(`ProjectPage.tsx:107, 96-99`) 직렬. `getMemberDirectory` 는 병렬(`:128`) |
| 조직 | 2 + 최대 4, 2단계 | 1단계 `Promise.all` profile·tree(`:90`). 2단계 유닛 멤버 ×2(`:127, :146`), 관리자는 역할·활동(`:163, :219`) |
| 보고 | 3 + N, 최대 3단계 | `getTasks`(병렬, 실패하면 `getMyWork`)와 `getDailyReportStatus` → `getDailyReportHistory` 직렬(`:139, :149`) → N× `getTask` 병렬(`:87-88`) |
| 회의 | 1 | `listMeetings`(`:64`). 회의를 열면 `readMeeting` → transcript·materials 병렬(2단계) |
| 관계 그래프 | 1 | `graphOverview`(`:61`) |
| AX 대화 열기 | 1–3 | `getConversations`(`useConversations.ts:138`) + 문맥용 `getMyWork`·`getWorkRequests` 병렬(`App.tsx:249-252`) |

---

## 8. B-02 새 업무 추가 › 참조자 후보

### 8-1. 참조자 후보의 출처와 거르는 조건 전부
- **API**: `getWorkRequestCcCandidates`(`lib/api.ts:1050`) → `GET /api/work-request-cc-candidates`
- **백엔드 경로**(읽기만 함)
  - `backend/src/ax_workspace/entrypoints/http.py:2287`
  - → `application.py:3308`
  - → `modules/work/requests.py:1361`: 권한 `WORK_REQUEST_CREATE` 또는 `TASK_SELF_MANAGE` 필요(`:1372`)
  - → `platform/organization_access.py:876 member_candidates`
- **서버 조건**(`organization_access.py:883-889`)
  1. `MemberRecord.employment_state == "active"`
  2. `EmploymentPeriodRecord` inner join: `state == "active"` 이고 `ended_at IS NULL`
  3. `id != principal.id`(본인 제외)
  4. `MemberRecord.id` 순 정렬
  - 역할·팀·계정·조직 범위 조건은 **없다.**
- **프론트에서 부르는 곳**
  - `MyWorkPage.tsx:400-417`: `canManageOwnTasks || canCreateWorkRequests` 일 때만. 실패하면 `[]`
  - `TodayPage.tsx:158`
  - `CalendarPage.tsx:502`
  - `MeetingDetailPage.tsx:212`
- **모달 안 렌더**(`features/work/WorkModals.tsx`, `CreateWorkModal`)
  - 목록이 비면 fieldset 자체를 숨긴다(`:5223`).
  - 칩은 **`ccCandidates.filter((candidate) => candidate.id !== assigneeId)`**(`:5227-5228`)로 걸러 그린다. 이 필터는 「내 업무」·「요청」 **두 갈래 모두에 걸린다.**
- **`assigneeId` 초기값**
  - `useState(initial ? initial.assigneeId ?? "" : assigneeCandidates[0]?.id ?? "")`(`:4387`)
  - 바로 위 주석(`:4386`)은 「미리 채운 값으로 열 때는 담당을 비워 둔다」다. 반대로 말하면, 미리 채운 값 없이 열면 첫 후보를 자동으로 고른다.
  - `kind` 기본값은 `canCreateTask && !requestOnly ? "task" : "request"`(`:4381`)다. 「새 업무 추가」는 보통 「내 업무」 갈래로 열린다.
  - 담당자 선택 UI 는 `kind === "request"` 일 때만 보인다(`:5172-5191`). **「내 업무」 갈래에서는 `assigneeId` 가 화면에 보이지 않는 채 첫 담당 후보 id 를 들고 있다.**
- **payload**
  - 내 업무 갈래는 `cc_member_ids: ccIds`(`:4744`)로 필터 없이 보낸다.
  - 요청 갈래는 `ccIds.filter(id => id !== assigneeId)`(`:4813`)로 보낸다.
- **담당 후보 `assigneeCandidates`**
  - `GET /api/work-request-assignee-candidates`(`api.ts:526`)
  - 서버 `organization_access.py:851-874` 조건
    - 본인 제외
    - `account_ref` 없는 사람 제외(`_can_answer`, `:838-849`)
    - 본인의 `organization_scope` 와 겹치지 않는 사람 제외
    - `MemberRecord.id` 순 정렬
  - 내 업무 화면은 `canCreateWorkRequests` 일 때만 부른다(`MyWorkPage.tsx:419-434`).
- **3명 중 1명이 빠지는 것을 설명하는 코드상 지점**(추정이 아니라 위 코드가 만드는 결과다)
  1. **숨은 `assigneeId` 필터**(`:4387` + `:5228`)
     - 미리 채운 값 없이 열고, 담당 후보가 이미 로드되어 있으면, 담당 후보 1번(id 가 가장 작은, 계정과 범위가 있는 동료)이 참조자 칩에서 빠진다.
     - 로그인한 사람에게 `work_request.create` 권한이 없으면 담당 후보가 `[]` 라서 아무도 안 빠진다.
     - `initial` 을 넘겨 여는 자리(하위 업무 `:2967`, 회의 승격, 재요청)에서는 생기지 않는다.
  2. **서버 데이터 조건**: 재직 기간(EmploymentPeriod) 레코드가 active·미종료가 아니거나 `employment_state != "active"` 인 사람은 서버가 아예 돌려주지 않는다(`organization_access.py:883-888`). 시드 데이터가 실제로 어떤지는 확인하지 않았다(§10).
  - 결재자·역할·팀·계정은 참조자 목록에 영향을 주지 않는다.

### 8-2. 결재자 후보의 출처·조건과 참조자와의 관계
- `approverCandidates = [...ccCandidates, ...assigneeCandidates 중 cc 에 없는 사람]`(`WorkModals.tsx:4966-4969`)
  - **assigneeId 필터가 없어서**, 참조자 칩에서 빠진 사람도 결재자 목록에는 나온다.
- 기본 결재자가 없다: `useState("")`(`:4449`), placeholder 「결재자 고르기」(`:5259`).
- 결재자를 골라도 참조자에서 빠지지 않는다. `approverId` 로 cc 를 거르는 코드는 0곳이다.
- 도움말은 「담당자는 결재자가 될 수 없다」고 말하지만(`:5265`), 결재자 목록을 `assigneeId` 로 거르지 않는다.
- 집계: `approverCandidates` 3건 / 1파일, `ccCandidates` 21건 / 5파일

### 8-3. 다른 「사람 고르기」 자리와 조건 비교
| 자리 | 출처 | 조건 | 본인 |
|---|---|---|---|
| **참조자**(새 업무) | `/api/work-request-cc-candidates` | 재직 active + 활성 재직 기간 | 제외 |
| 요청 담당자 | `/api/work-request-assignee-candidates` | 계정 있음 + 조직 범위 교집합 | 제외 |
| **담당자 변경 대상**(F-01) | `GET /api/task-assignment-candidates`(`api.ts:1006`) → `assignments.py:88`, `_assignable`(`:92`) | `organization_access.py:931-947`: 본인의 `TASK_ASSIGN` 범위 유닛 안 + 계정 있음 + 후보가 `task.self_manage` 능력을 가짐. 프로젝트 `assignable_members` 와 합친다. `TASK_ASSIGN` 권한이 필요하다. | 제외 |
| 회의 승격 | `/api/meetings/{id}/promotion-candidates`(`api.ts:1046`) | `organization_access.py:893-929`: active + 계정. 참석자를 앞에 둔다. `api.ts:1037-1045` 주석에 과거 assign 필터로 6명이 2명이 된 버그 기록이 있다. | **포함** |
| 회의 PeoplePicker / PersonSearch | `meetings/roster.ts:22-40`: `/api/organization/tree` + `/units/{id}/members` | 이름 일치 + `excluded` 집합만(`roster.ts:69-78`) | 조건 없음 |
| 프로젝트 멤버 | `getMemberDirectory`(`/api/organization/members`, `api.ts:147`; `ProjectPage.tsx:128`) | 서버 `_active_member_names`(`organization_access.py:804-836`): active 만. 프론트는 기존 멤버를 뺀다(`ProjectManageModal.tsx:50`). | 포함 |

- **조건은 자리마다 다르다.** 참조자는 재직만 보고, 담당 변경은 범위 + 계정 + `task.self_manage` 까지 본다.
  - 그래서 `task.self_manage` 능력이 없는 역할(예: executive)은 담당 변경 후보에서 빠질 수 있다. 역할-능력 매핑은 백엔드 설치 데이터에 달려 있고 이번에 확인하지 않았다(§10).

---

## 9. grep 개수표

`grep -rnoF <심볼> frontend/src frontend/index.html`, `*.test.*` 제외. "건/파일".

| 요청 | 심볼 | 건 | 파일 |
|---|---|---|---|
| F-01 | `handover` | 20 | 4 |
| F-01 | `link-draft` | 4 | 2 (TSX 2자리 + CSS 2줄) |
| F-01 | `task-handover-` | 3 | 1 |
| F-01 | `form-stack` (TSX 사용) | 5 | 3 |
| F-01 | `scax-modal` | 59 | 7 |
| F-01 | `scax-modal--sm` | 4 | 3 |
| F-01 | `scax-modal--md` | 3 | 3 |
| F-01 | `scax-modal--create` | 7 | 2 |
| F-01 | `useEscape` | 19 | 8 |
| F-01 | `modal-backdrop` | 19 | 9 (TSX `className="modal-backdrop` 16) |
| F-01 | 업무 상세 뒤 형제 모달 | 10 | 1 (`WorkModals.tsx:2815-2961`) |
| F-02 | `type="search"` | 1 | 1 |
| F-02 | `search-input-box` | 7 | 6 (마크업 3) |
| F-02 | `scax-chat__search` | 2 | 2 |
| F-02 | `scax-textfield__input` | 15 | 7 |
| F-02 | `scax-textfield--search` (CSS 정의) | 0 | 0 |
| F-02 | `webkit-appearance` | 1 | 1 (date 전용) |
| F-02 | `::-webkit-search` | 0 | 0 |
| F-03 | `scax-pj-gantt` | 161 | 3 (테스트 포함) |
| F-03 | `ganttAxis` | 6 | 3 (테스트 포함) |
| F-03 | `barGeometry` | 7 | 3 (테스트 포함) |
| F-03 | `GANTT` | 43 | 5 (테스트 포함) |
| D-01 | `work-timeline` | 23 | 2 |
| D-01 | `calendar-toolbar` | 4 | 3 |
| D-01 | `timeline-grid` | 3 | 2 |
| D-01 | `timeline-bar` | 10 | 4 |
| D-01 | `TaskTimeline` | 7 | 5 (테스트 포함) |
| D-01 | `taskSpan` | 10 | 4 |
| D-01/F-03 공유 | `addDays` / `dayDifference` | 42 / 19 | 10 / 8 |
| D-02 | `scax-actioncard` | 14 | 5 |
| D-02 | `data-view` | 3 | 3 |
| D-02 | `SC AX` | 3 | 2 (화면 노출 2 + CSS 주석 1) |
| D-02 | `MEDISOLVE` | 5 | 3 |
| A-01 | `getActionItems` | 5 | 3 |
| A-01 | `data-action-item-id` | 1 | 1 |
| A-01 | `data-action-id` | 5 | 4 |
| A-01 | `"ax.` 류 kind 리터럴 | 0 | 0 |
| B-01 | `surface ===` | 18 | 1 (`App.tsx`) |
| B-01 | `Skeleton ` (태그·임포트) | 40 | 20 |
| B-02 | `cc-picker` | 9 | 3 |
| B-02 | `getWorkRequestCcCandidates` | 9 | 5 |
| B-02 | `getWorkRequestAssigneeCandidates` | 10 | 5 |
| B-02 | `getTaskAssignmentCandidates` | 8 | 4 |
| B-02 | `ccCandidates` | 21 | 5 |
| B-02 | `approverCandidates` | 3 | 1 |

---

## 10. 조사 한계

- **실행 확인 없음**: 브리프대로 서버·브라우저·테스트를 띄우지 않았다. 아래는 코드를 읽어서 낸 결론이고 화면으로 확인하지 않았다.
  - F-02 의 WebKit 실제 렌더 모양
  - F-01 의 `ReasonPrompt` ESC 이중 반응
  - B-01 의 깜박임 체감 시간
- **B-02 원인 확정 불가**
  - 프론트의 숨은 `assigneeId` 필터는 코드로 확인했다. 하지만 운영 시드의 실제 값은 보지 않았다.
    - 로그인한 사람의 `work_request.create` 권한 여부
    - 담당 후보 1번이 누구인지
    - 4명 각자의 `EmploymentPeriodRecord`
  - 그래서 두 원인(프론트 필터 / 서버 재직 조건) 중 어느 쪽인지 확정하지 않았다.
  - 서버 쪽 경로·조건은 `backend/` 를 읽기만 해서 적었다. 백엔드 워커 리포트와 대조가 필요하다.
- **역할-능력 매핑**: executive/team-lead/member 가 각각 어떤 capability(`task.self_manage`·`task.assign`·`work_request.create`)를 갖는지는 백엔드 설치 데이터 영역이라 보지 않았다.
- **A-01 서버 필터**: `GET /api/action-items` 가 서버에서 어떤 kind·state 를 돌려주는지(예: `ax.task.create_self` 를 포함하는 기준)는 프론트 범위 밖이라 확인하지 않았다. 프론트는 쿼리 없이 받은 것을 전부 그린다.
- **SPEC 문서 대조**: 문서 리포(`20-spec`·`21-screen`) 와의 대조는 이번 브리프 범위가 아니라서 하지 않았다. DS 문서(`docs/design/`)는 grep 으로만 봤다.
- **조사 방식**: 일부 절(F-01·B-02·D-02·A-01·B-01·F-03·D-01)은 읽기 전용 탐색 보조 에이전트가 1차로 모았다. 핵심 근거 줄은 직접 다시 열어 확인했다.
  - 확인한 줄: `WorkModals.tsx:4381,4387,4966-4969,5227-5228,4744,4813,2324-2334` · `projectModel.ts:237-248` · `WorkViews.tsx:388-392` · `api.ts:1095-1097` · `TodayPage.tsx:100-110` · `ActionTaskCard.tsx:464,467,934` · `App.tsx:75,476-480` · `Skeleton.tsx:10-16` · `MyWorkPage.tsx:352-356` · `components.css:487,737` · `ax.css:116` · `ChatDrawer.tsx:240-270`
  - 그 밖의 줄 번호는 보조 에이전트가 낸 값이다.
