# 루프 2 조사 리포트 — 구현 전에 답이 있어야 하는 다섯 (2026-09-22)

**모드**: read-only 조사 (`@sc-ax-reviewer`) · **task-id** `task_cd933fc05fda`
**코드 위치**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (워크트리, 읽기만)
**수정 0건 · 커밋 0건 · 테스트 실행 0건 · 서버 기동 0건.** 확인: 아래 §끝 `git status`.

> **설계하지 않았다.** 각 절은 「지금 이렇다 → 선택지는 이것들이다 → 비용은 이렇다」까지다.

---

## 요약 — 다섯의 결론 한 줄씩

| Q | 결론 | 위험 |
|---|---|---|
| **Q1** 틀고정 | **된다. CSS 3줄 + JSX 1요소.** 간트 재조립 아니다 | 낮음 |
| **Q2** 허용 전이 | **BE 확장 0건.** `transitions` 는 순수 FE 계산이고, 그 입력(`state`·`derived`)은 **우 레일이 이미 받고 있다** | 낮음 |
| **Q3** 설명·체크리스트 | **선택지 ⓑ 가 이미 구현돼 있다**(`getTask` 호출이 이미 산다). B-9 의 「언제나 등록된 항목이 없습니다」는 **코드와 맞지 않는다** — 재현 조건 확인 필요 | **중** (전제 어긋남) |
| **Q4** 헤더 버튼 | 프로젝트 화면은 **이미 헤더에 등록한다**(「관리」). 비어 보인 것은 `may_manage=false` 탓. 생성 폼은 지금 **`name` 한 칸만** 보낸다 | 중 (중복 결정 필요) |
| **Q5** 권한 게이트 | 게이트 참조 **4자리**, 그중 **자동 초대는 1자리**. 깨지는 테스트 **정확히 1건** | 낮음 |

---

## Q1. B-3 틀고정 — **지금 구조에서 된다** (범위 판정 포함)

### 지금 이렇다

DOM 과 CSS 전수:

| 층 | 파일:줄 | 핵심 선언 |
|---|---|---|
| `.scax-pj-gantt__scroll` | `frontend/src/styles/projects.css:65` | `overflow-x:auto` |
| `.scax-pj-gantt__canvas` | `projects.css:66` / `ProjectGantt.tsx:116` | `position:relative`, 인라인 `width = 200 + days×34` |
| `.scax-pj-gantt__plot` | `projects.css:70` / `ProjectGantt.tsx:128` | `position:relative`, 인라인 `height` |
| `.scax-pj-gantt__row` | `projects.css:80` / `ProjectGantt.tsx:187` | **`position:absolute; left:0; right:0`**, `display:flex` |
| `.scax-pj-gantt__name-cell` | `projects.css:81` / `ProjectGantt.tsx:188` | `flex:0 0 auto`, 인라인 `width:200` |
| `.scax-pj-gantt__bar` | `projects.css:93` / `ProjectGantt.tsx:222` | `position:absolute`, 인라인 `left`/`width` |

### **`position:sticky; left:0` 이 `absolute` 행 안에서 먹는가 — 먹는다**

sticky 가 죽는 조건은 셋이고, **셋 다 여기 없다**:

1. **스크롤 조상이 없다** → 있다. `.scax-pj-gantt__scroll`(`projects.css:65`)이 실제로 가로 스크롤한다(사용자가 본 증상 자체가 그 증거다).
2. **sticky 와 스크롤포트 사이에 `overflow:hidden|auto` 조상이 낀다** → **없다.** `__canvas`(66) · `__plot`(70) · `__row`(80) 어디에도 `overflow` 선언이 없고, `transform`·`filter`·`contain` 도 없다. `.scax-pj-view` 의 `overflow-y:auto`(`projects.css:41`)는 `__scroll` **바깥**이라 사이에 끼지 않는다.
3. **containing block 이 좁아 붙을 구간이 없다** → **없다.** sticky 는 **부모(=`__row`)의 content box** 안에서만 미끄러지는데, 그 행이 `left:0; right:0`(`projects.css:80`)이라 폭이 `__plot` 전체 = **스크롤 콘텐츠 전폭**이다. 즉 어느 스크롤 위치에서도 라벨 칸이 붙을 자리가 남는다.

**`position:absolute` 부모는 sticky 를 죽이지 않는다.** 행이 absolute 라도 그 행은 스크롤 콘텐츠와 **함께 움직이는** 박스지 `fixed` 가 아니다. sticky 의 스크롤포트 탐색은 containing-block 사슬이 아니라 **박스 트리 조상**을 걷는다 — 그 끝이 `.scax-pj-gantt__scroll` 이다.

### 그래서 **실제로 고쳐야 할 것은 sticky 한 줄이 아니라 넷**이다 (전부 이 화면 CSS)

| # | 무엇 | 왜 | 어디 |
|---|---|---|---|
| ① | `position:sticky; left:0` | 본체 | `projects.css:81` `.scax-pj-gantt__name-cell` |
| ② | `z-index` (양수) | **페인트 순서가 뒤집혀 있다.** 같은 행 안에서 `__name-cell` 이 `__bar`(`ProjectGantt.tsx:222`)보다 **DOM 앞**이고 둘 다 z-index:auto 인 positioned 박스라, **막대가 라벨 위에 그려진다.** sticky 로 붙여도 막대가 그 위를 덮는다 | 같은 줄 |
| ③ | `background:var(--scax-color-surface)` | 지금 `__name-cell` 에 배경이 없다. 스크롤하면 격자(`__grid` `projects.css:71`) · 오늘선(`__now` 72) · 의존선 SVG(`__links` 73)가 **라벨 글자 밑으로 비쳐 지나간다** | 같은 줄 |
| ④ | 머리줄 200px 자리를 덮을 요소 | `.scax-pj-gantt__axis` 는 `paddingLeft:200`(`ProjectGantt.tsx:117`)**만** 두고 그 자리에 요소가 없다. 스크롤하면 **날짜 숫자가 라벨 칸 위쪽 띠로 그대로 보인다** | `ProjectGantt.tsx:117-118` 사이에 sticky 스페이서 `<span>` 1개 + CSS 1줄 |

**①~③ 은 `projects.css:81` 한 줄에 선언 3개를 더하는 일**이고, **④ 만 JSX 에 빈 `<span>` 하나**가 는다.

### **범위 판정 — CSS 쪽이다. 간트 재조립이 아니다**

- **바꾸는 줄**: `projects.css` **1줄 수정 + 1~2줄 추가**, `ProjectGantt.tsx` **요소 1개 추가**. 합쳐 **5줄 내외.**
- **손대지 않는 것**: `anchorIndex()`(`projectModel.ts:306`) · `barGeometry()`(246) · `depPath`/`DepLines`(`ProjectGantt.tsx:239-288`) · 행 `top` 계산(`ProjectGantt.tsx:140`) · 접힘(`ganttRows` 268) — **좌표계가 하나도 안 바뀐다.** sticky 는 레이아웃 후 **페인트 오프셋**이라 `positions` 맵(`ProjectGantt.tsx:105-110`)의 값이 그대로다.
- **테스트 영향 0.** jsdom 은 sticky 를 계산하지 않고, `ProjectPage.test.tsx` 의 간트 단언은 전부 셀렉터·텍스트다(`ProjectPage.test.tsx:278·285·297·312-329·342`).

### 참고 — **「두 열로 가르는」 길은 왜 비싼가** (안 가도 되지만 비교를 적어 둔다)

고정 칸과 스크롤 캔버스를 **형제 두 열**로 가르면 깨지는 것이 넷이다:

1. **의존선 SVG 좌표계** — `positions` 의 `x1/x2` 가 `GANTT.label` 을 **더한 값**이다(`ProjectGantt.tsx:109`, `projectModel.ts:246`). 캔버스가 0 에서 시작하게 되면 **모든 x 에서 200 을 빼야** 하고, `width`(`ProjectGantt.tsx:102`)·`grid left`(129)·`nowLeft`(112)도 같이 바뀐다.
2. **행 `top`** — 두 열이 **각자** `index*40` 을 계산하게 되어 한쪽만 틀어지면 라벨과 막대가 어긋난다. 지금은 한 행이 둘을 함께 들어 어긋날 수 없다.
3. **접힘** — `rows` 배열이 두 열에 각각 매핑되면 `withFoldedLinks`(`projectModel.ts` · `ProjectGantt.tsx:58`)의 `foldedLinks` 배지(216-220)가 라벨 열에, 그 원인인 막대가 캔버스 열에 있게 된다.
4. **테스트** — `container.querySelector('.scax-pj-gantt__row[data-task-id="t-5"] .scax-pj-gantt__bar')`(`ProjectPage.test.tsx:312`)가 **행의 자손으로 막대를 찾는다.** 두 열로 가르면 이 패턴의 단언 **11건**(`312-343`)이 전부 셀렉터부터 다시 써야 한다.

→ **가지 않아도 되는 길이다.** sticky 가 먹으므로 ①~④ 로 끝난다.

### 덤 — B-3 의 나머지 절반(오늘 기준 스크롤)

지금 `.scax-pj-gantt__scroll` 에 **ref 가 없다**(`ProjectGantt.tsx:115`). **선례가 이미 있다**: `features/calendar/WeekGrid.tsx:105` 이 `scroller.current.scrollTop = WEEK_OPEN * WEEK_ROW` 로 첫 진입 스크롤을 잡고, `CalendarPage.test.tsx:268` 이 jsdom 에서 그 값을 검사한다. 가로판으로 옮기면 `scrollLeft = GANTT.label + dayDifference(axis.from, today) * GANTT.day - 여유` 이고, 두 값 모두 이미 계산돼 있다(`ProjectGantt.tsx:111-112`).

---

## Q2. B-8 허용 전이는 **어디서 오나** — 서버가 아니라 **표 하나**다

### `transitions` 의 출처 — **순수 FE 계산이다. BE 확장이 필요 없다**

`MyWorkPage.tsx:1378` 의 `const transitions = allowedTaskTransitions(task)` 를 따라가면:

- `frontend/src/features/work/WorkModals.tsx:133-138` `allowedTaskTransitions(task)`
- 읽는 것은 **정적 표** `transitionFor`(`WorkModals.tsx:108-113`) 하나: `open→in_progress(start)` · `in_progress→{blocked(block), done(complete)}` · `blocked→in_progress(resume)` · `done→in_progress(resume)`
- 더해 **한 갈래만 서버 값을 본다**: `reopenBlockedByApproval()`(`WorkModals.tsx:124-128`) — `task.state==="done"` 이고 `task.derived.approval ∈ {awaiting_review, awaiting_revision}` 이면 **전이 0건**.

**서버에 `transitions` 필드는 존재하지 않는다.** `grep -rn "transitions" backend/` 의 유일한 히트는 `modules/work/lifecycle.py:1` 의 docstring 이다.

> 그 파일의 주석(`WorkModals.tsx:100-102`)이 「`allowed_commands` 가 생기면 **몸통만** 갈아끼운다」고 못 박고 있다 — 지금 그 봉투는 없다.

### 그래서 **필요한 입력은 둘뿐**이다: `state` · `derived.approval`

- `ProjectTaskView` 에는 `state` 만 있다(`project_results.py:52`) — **`derived` 가 없다**(48-70 전체에 없음). 백로그의 서술 그대로다.
- **그러나 우 레일은 이미 `DirectTask` 를 갖고 있다.** `ProjectPage.tsx:121-143` 이 선택이 바뀔 때마다 `getTask(taskId)` 를 부르고, `ProjectTaskPanel.tsx:43` 이 `detail: DirectTask | null` 로 받는다. `DirectTask.derived`(`viewModels.ts:283`) · `state` 가 거기 실린다.

### **선택지 ⓐ / ⓑ 판정**

| | ⓐ 프로젝트 상세 `tasks[]` 확장 | ⓑ 선택 업무만 업무 상세 |
|---|---|---|
| BE 변경 | `ProjectTaskView` 에 `derived` 추가 + `_derived_for()` 를 프로젝트 투영에서 호출 | **0** |
| FE 변경 | `ProjectTaskRow` 타입 확장 | **0 — 이미 온다** |
| 응답 크기 | 업무당 `derived` 묶음(키 7개) 만큼 증가 | 0 |
| 호출 | 0 | **0 (이미 하고 있다)** |
| **판정** | — | **ⓑ. 새로 짤 것이 없다.** `allowedTaskTransitions(detail)` 을 부르면 끝이다 |

### 「내 업무」 판정 — **서버 판정이 이미 응답에 실려 있다**

| 방법 | 근거 | 평 |
|---|---|---|
| **`detail.access === "owner"`** ← 권장 | `application.py:940-943`: `repository.task(task_id, principal.id)` 가 성공해야 `"owner"`. 그 질의는 `work_tasks.py:1090-1091` — **「활성 TaskAssignment 를 지금 들고 있는 사람」만** 통과 | **서버 판정 그대로.** FE 가 추론하지 않는다 |
| `row.assignee.member_id === personaId` | `ProjectTaskPanel` 에 `personaId` prop 이 **없다**(`ProjectTaskPanel.tsx:32-47`) — `ProjectPage.tsx:48` 에서 내려야 한다. 값 자체는 같은 「활성 배정」에서 온다(`project_results.py:27-33`) | 동작은 같지만 **판정을 화면이 다시 한다** |

**업무 화면은 무엇으로 하나** — 둘 다 아니다. **목록이 이미 「내 업무」다**: 세션 봉투의 `canManageOwnTasks`(`App.tsx:369` = `has("task.self_manage")`)를 `MyWorkPage.tsx:1113` 에서 `canManage={canManageOwnTasks && !row.awaitingAcceptance}` 로 행에 내린다. **프로젝트 화면은 남의 업무도 보여주므로 그 전제가 성립하지 않는다** — 그래서 `access` 가 대체 판정으로 필요하다.

⚠ **`!row.awaitingAcceptance` 도 함께 물려받아야 한다** — 수락 전 배정에 상태 드롭다운을 세우면 안 된다. 그 값은 `detail.derived.assignment === "awaiting_acceptance"` 다(`viewModels.ts:283` · `application.py` `_assignment_wait`).

### 완료 보고 모달 — **재사용 가능하다**

`CompletionReportModal` 은 `WorkModals.tsx:2176` 에서 **export** 돼 있고, 소비처가 이미 셋이다(`WorkModals.tsx:1979`·`2634`, `MyWorkPage.tsx:1418`).

- prop 전부가 **평범한 값**이다(`WorkModals.tsx:2187-2202`): `task: DirectTask` · `requesterName: string` · `busy?` · 콜백 넷. **MyWorkPage 문맥에 묶인 prop 이 없다.**
- `materials`·`subtasks` 를 **안 넘기면 자기가 읽는다**(`WorkModals.tsx:2210-2236` — `getTaskMaterials` · `getTask`). 프로젝트 화면이 그 둘을 모아 줄 필요가 없다.
- 프로젝트 화면이 이미 가진 것으로 prop 이 다 찬다: `task` ← `taskDetail`(`ProjectPage.tsx:64`), `requesterName` ← `detail.origin.actor.display_name`(**`ProjectTaskPanel.tsx:64` 가 이미 그 값을 꺼내 쓰고 있다**).
- 재사용해야 하는 이유도 그대로 산다: `MyWorkPage.tsx:1397-1401` 의 주석대로 **요청 업무의 `complete` 는 서버가 늘 거절한다.** `isRequestTask()`(`workRows.ts:28-30`)가 그 판정이고 `origin.kind`/`lineage` 만 본다 — 둘 다 `DirectTask` 에 있다.

---

## Q3. B-7·B-9 설명·체크리스트 — ⚠ **B-9 의 전제가 코드와 맞지 않는다**

### **확인한 사실 ① — 선택지 ⓑ 는 이미 구현돼 있다**

백로그가 「선택지」로 적은 ⓑ(선택 업무만 `getTask`)는 **1루프에서 이미 만들어졌다**:

- `ProjectPage.tsx:121-143` — `taskId` 가 바뀔 때마다 `getTask(taskId)` 를 부르고 `taskDetail`/`taskDetailState` 에 담는다. 주석(116-120)이 그 설계 의도를 그대로 적고 있다.
- `ProjectPage.tsx:250-257` — 우 레일에 `detail`·`detailState` 로 내린다.
- `ProjectTaskPanel.tsx:66` — `const checklist = detail?.checklist ?? null`.
- `ProjectTaskPanel.tsx:138-149` — `checklist` 가 있고 길이가 0 이 아니면 **항목을 실제로 그린다**.

### **확인한 사실 ② — 「언제나 등록된 항목이 없습니다」는 코드가 하는 일이 아니다**

`ProjectTaskPanel.tsx:134-154` 의 분기는 넷이다:

| 조건 | 화면 |
|---|---|
| `detailState==="loading"` && 항목 없음 | `Skeleton`(135) |
| `detailState==="error"` | `StatusNote tone=danger` = 「…」(137) |
| `checklist.length > 0` | **항목 목록**(139-149) |
| 그 밖 → `progress.total > 0` ? | **`checklistHidden`** = 「항목은 이 업무를 맡은 사람에게만 보입니다.」(`labels.ts:1010`) |
| 그 밖 → `total === 0` | `checklistNone` = 「등록된 항목이 없습니다.」(`labels.ts:1008`) |

**막대가 40% 인데 「등록된 항목이 없습니다」가 뜨는 조합은 이 표에 없다.** 40% 를 내려면 `checklist_progress.total > 0` 이어야 하고(`projectModel.ts:68`), 그러면 `checklistHidden` 문구가 뜬다.

**데모에서 40% 를 내는 업무는 정확히 하나다** — `redesign-survey`(「디자인 시안 조사」), 체크리스트 5개 중 2개 완료 = 40% (`bootstrap/demo_work.py:157-162`). 담당은 **jiho** 다. 데모 프로젝트 「하반기 제품 개편」의 업무 **12건 중 체크리스트가 있는 것은 이 하나뿐**이다(`demo_work.py:125-169` 전수).

→ **나머지 11건에서 「등록된 항목이 없습니다」가 뜨는 것은 정상이다**(실제로 항목이 없다). B-9 의 관찰은 **그 11건을 본 것**일 가능성이 높고, 「40% 인데 비었다」는 **jiho 가 아닌 사람으로 `redesign-survey` 를 봤다면 `checklistHidden` 문구**가 나왔어야 한다.

**못 확인한 것**: 사용자가 어느 페르소나로 어느 업무를 눌렀는지. 화면을 띄우지 못하므로(지시상 금지) **재현 조건을 사용자·코디가 한 줄로 확인해 주면 된다** — 「막대 40% 인 업무를 골랐을 때 우 레일 문구가 ⓐ『등록된 항목이 없습니다』였나 ⓑ『항목은 이 업무를 맡은 사람에게만 보입니다』였나」. ⓑ 였다면 **버그가 아니라 권한 문구**이고 B-9 는 구현 항목이 아니라 **UX 문구 결정**이 된다.

### **확인한 사실 ③ — `NotRequired` 의 실제 동작**

- `checklist: NotRequired[...]` (`task_results.py:239`)
- `application.py:940-943`: 소유자면 `_with_checklist(...)` + `access:"owner"`. 아니면 `_related_view(...)` + `access:"read_only"` — **그 분기에는 `checklist` 키가 아예 없다**(`application.py:980-988` 의 반환 딕셔너리 전수).
- `"owner"` 의 조건은 **활성 배정 보유**뿐이다(`work_tasks.py:1090-1091`).

**남의 업무를 볼 때 무엇이 오나 — 「오긴 온다」**:

| | 값 |
|---|---|
| 응답 자체 | **온다.** 프로젝트 참여자는 그 프로젝트 업무 전부를 읽는다 — `_may_read_beyond_holding()`(`application.py:1111-1118`)이 `task.project_id ∈ 내 프로젝트 범위`면 통과시킨다 |
| `access` | `"read_only"` |
| `checklist` | **없다** |
| `checklist_progress` | **없다**(`task_results.py:240` 도 `NotRequired`) — 하지만 우 레일은 **프로젝트 응답의 `row.checklist_progress`** 를 쓰므로(`ProjectTaskPanel.tsx:59`) 집계·미터는 정상이다 |
| `description` | **온다** ✅ |
| `derived` | **온다** ✅ (`_view()` 가 항상 만든다) |

읽을 수 없는 관계면 `TaskNotFound`(`application.py:978-979`) → FE 의 `.catch` 가 `detailState="error"`(`ProjectPage.tsx:135-139`) → `StatusNote tone="danger"`.

### **`description` 은 업무 상세에 오는가 — 온다**

`TaskMutationResult.description: str | None`(`task_results.py:73`), 값은 `_view()` 가 항상 싣는다(`application.py:2434`). `TaskDetailResult` 가 그것을 상속한다(229). FE 타입에도 있다(`viewModels.ts:225` `description?: string | null`).

→ **B-7 의 「업무 정보」 블록에 필요한 두 값 중 `description` 은 이미 손 안에 있다.** `ProjectTaskPanel` 이 `detail.description` 을 읽기만 하면 된다.

### **선택지별 비용 — 수치**

측정 기준: 실측 응답 1건(`be-impl-report.md §6`)을 minified UTF-8 JSON 으로 인코딩.

| 단위 | 바이트 |
|---|---|
| `ProjectTaskView` 1건 (현행) | **376 B** |
| `ChecklistItemView` 1건 (9필드, 한글 10자 text) | **236 B** |
| `"description"` 한 칸 (한글 40자) | **135 B** |

| | ⓐ `tasks[]` 확장 | ⓑ 선택 업무만 `getTask` |
|---|---|---|
| BE 변경 | `ProjectTaskView` 에 `description` + `checklist` 추가 · 프로젝트 투영에서 **N건 분 체크리스트 일괄 조회** 신설 | **0** |
| FE 변경 | `ProjectTaskRow` 타입 확장 + 블록 렌더 | **블록 렌더만** |
| **지금 데모 응답 증가** | 업무 12건 · 체크리스트 항목 5개 → `12×135 + 5×236` = **≈ 2.8 KB**. 현행 `tasks[]` 는 `12×376` ≈ **4.5 KB** → **+62%** | **0 B** |
| **업무 60건 · 업무당 항목 10개 가정** | `60×135 + 600×236` = **≈ 150 KB** (현행 `60×376` ≈ 22 KB → **약 7.8배**) | **0 B** |
| 추가 호출 | 0 | **0 — 이미 걸려 있다**(`ProjectPage.tsx:129`) |
| 지연·깜빡임 | 없음 | **이미 처리돼 있다** — `detailState` 3상태로 `Skeleton`/`StatusNote`/본문을 가른다(`ProjectTaskPanel.tsx:134-137`). 상세가 안 와도 **상자는 선다**(주석 `ProjectTaskPanel.tsx:24-26`). 우 레일은 한 번에 한 업무라 N+1 이 아니다 |
| ⚠ 권한 | **더 나쁘다.** `checklist` 를 `tasks[]` 에 실으려면 **업무 단건의 `NotRequired` 규칙을 목록에서 다시 세워야** 한다 — 12건 중 내가 든 것만 항목을 싣는 분기가 프로젝트 투영에 새로 생긴다 | 규칙이 **한 자리**(`application.py:940-943`)에 그대로 남는다 |
| **판정** | 비싸고 권한 규칙이 갈라진다 | **ⓑ. 이미 서 있는 길이다** |

---

## Q4. B-1 「다른 탭 페이지처럼」 — **그 방식이 이미 이 화면에도 적용돼 있다**

### ⚠ **정정 — 프로젝트 화면은 헤더에 「등록하지 않는다」가 아니다**

`ProjectPage.tsx:280-290` 이 이미 등록한다:

```tsx
useEffect(() => {
  if (!onRegisterHeaderActions) return;
  onRegisterHeaderActions(
    selected?.may_manage ? (<Button …>{projectScreen.manage}</Button>) : null,
  );
  return () => onRegisterHeaderActions(null);
}, [onRegisterHeaderActions, selected?.may_manage]);
```

`.scax-page-header__actions` 가 비어 보인 것은 **미등록이 아니라 `selected.may_manage === false`** 다. `may_manage` 는 `PROJECT_MANAGE` 를 그 프로젝트 범위에서 가졌는가로 서버가 낸다(`projects.py:516-520` `_manageable`). 데모에서 프로젝트를 만든 사람은 `lead` 로 붙지만(`projects.py:172-179`), `mina` 는 `member` 로만 붙는다(`demo_work.py:194-195`) — **`mina` 로 보면 손잡이가 없다.** SPEC-005 가 그것을 E2E 항목으로 박아 뒀다: `spec-005-projects.md:986` 「E-17 관리 권한이 없는 사람으로 연다 → 헤더에 관리 모달 손잡이가 **없다**」.

### **선례 전수 — `onRegisterHeaderActions` 를 쓰는 화면 다섯**

셸 쪽(`App.tsx`): `const [surfaceActions, setSurfaceActions] = useState<React.ReactNode>(null)`(`App.tsx:138`) → `<AppHeader actions={surfaceActions} …/>`(`App.tsx:459`) → `<div className="scax-page-header__actions">{actions}</div>`(`shell/AppShell.tsx:71`, CSS `styles/shell.css:132`).

| 화면 | 등록 자리 | 무엇을 | 게이트 |
|---|---|---|---|
| Calendar | `CalendarPage.tsx:487-496` | 「업무 만들기」 solid/primary → `setIsCreating(true)` | `canManageOwnTasks \|\| canCreateWorkRequests` |
| MyWork | `App.tsx:517` 로 넘김 (`MyWorkPage`) | 생성 손잡이 | `canManageOwnTasks` 계열 |
| Meetings | `App.tsx:500` | — | — |
| DailyReport | `App.tsx:526` / `DailyReportPage.tsx:34·59` | — | — |
| **Project** | **`ProjectPage.tsx:280-290`** | 「프로젝트 관리」 outlined | `selected?.may_manage` |

**공통 형태 넷** — 이것이 「다른 탭 페이지와 같은 방식」의 정의다:
1. `useEffect` 안에서 `onRegisterHeaderActions(node)`
2. **떠날 때 `onRegisterHeaderActions(null)`** 로 지운다 (cleanup)
3. 권한이 없으면 **`null` 을 등록한다** — 비활성 버튼을 그리지 않는다
4. deps 에 권한 값과 콜백만 둔다 (`ProjectPage.tsx:170-178` 의 ref 우회 주석이 그 이유를 적고 있다 — 인라인 화살표를 deps 에 넣으면 무한 루프)

### **`POST /api/projects` 가 실제로 받는 것**

라우트: `entrypoints/http.py:1389-1401`. 바디 모델은 `ProjectCreateInput`(`http.py:79` 에서 `CreateProjectRequest` 로 alias), 정의는 `modules/work/project_commands.py:17-23`:

| 필드 | 타입 | 필수 | 검증 |
|---|---|---|---|
| `name` | `str` | **필수** | `min_length=1, max_length=300` · 서버가 `" ".join(split())` 로 공백 정규화 후 **빈 문자열이면 `ProjectError("프로젝트 이름이 필요합니다")`**(`projects.py:157-159`) |
| `description` | `str \| None` | 선택 | 길이 제한 없음 · `strip()` 후 빈 문자열이면 `None`(`projects.py:166`) |
| `starts_on` | `date \| None` | 선택 | — |
| `ends_on` | `date \| None` | 선택 | **`ends_on < starts_on` 이면 `ProjectError("끝나는 날이 시작하는 날보다 앞설 수 없습니다")`**(`projects.py:160-161`) |
| `external_key` | `str \| None` | 선택 | `max_length=200` · **중복이면 `ProjectError("이미 있는 프로젝트 key입니다")`**(`projects.py:162-163`) |

**거절하는 것 둘 더**:
- `model_config = ConfigDict(extra="forbid")`(`project_commands.py:18`) → **모르는 필드를 보내면 422.**
- `PROJECT_MANAGE` capability 가 없으면 `ProjectAccessDenied("프로젝트를 만들 수 있는 자격이 없습니다")`(`projects.py:153-154`).

**부수 효과**: 만든 사람이 **`lead`** 로 자동 배정된다(`projects.py:172-179`).
**응답**: `ProjectView`(201) — `project_id`·`name`·`description`·`state`·`starts_on`·`ends_on`·`external_key`·`version`(`project_results.py:5-13`).

### ⚠ **중복 — 「새 프로젝트」 폼이 이미 관리 모달 안에 있다**

| 지금 | 근거 |
|---|---|
| 관리 모달 안 「새 프로젝트」 블록 — **입력 칸이 이름 하나뿐** | `ProjectManageModal.tsx:31·40` `onCreate: (name: string) => void`, 폼은 `ProjectManageModal.tsx:190-217` |
| 그 핸들러가 보내는 바디 — **`{ name }` 만** | `ProjectPage.tsx:184` `await createProject({ name })` |
| FE api 시그니처는 **네 칸까지 받게 돼 있다** (`external_key` 는 없다) | `lib/api.ts:805-812` — `name`·`description`·`starts_on`·`ends_on` |
| 그 모달을 **여는 손잡이 자체가 `may_manage` 게이트 뒤에 있다** | `ProjectPage.tsx:283` |

**→ 오늘 상태를 한 줄로**: 생성 손잡이는 **관리 권한이 있는 사람에게만, 관리 모달 안에서만** 있고, **DB 가 받는 5칸 중 1칸(`name`)만** 보낸다.

**선택지 셋 — 결정은 코디·사용자** (설계하지 않는다)

| | 무엇 | 비용 | 걸리는 것 |
|---|---|---|---|
| **ⓐ** 헤더 버튼이 **같은 관리 모달**을 연다 | 가장 싸다 — `ProjectPage.tsx:284` 의 `setManaging(true)` 를 버튼 하나 더에 물린다 | 모달 제목이 「프로젝트 관리」라 **생성하러 온 사람에게 참여자 관리가 먼저 보인다.** 그리고 **`may_manage` 게이트를 그대로 물려받아** 관리 권한 없는 사람은 여전히 못 만든다 |
| **ⓑ** 헤더 버튼이 **새 생성 전용 모달**을 연다 + 관리 모달의 생성 블록을 **뗀다** | 모달 1개 신설(5칸) + 관리 모달에서 블록 1개 제거 + `create()` 를 5칸으로 확장 | 「옮기기」라 **두 자리에 같은 것이 남지 않는다**(1루프 D-05 가 관리 기능을 모달로 옮길 때 쓴 논리와 같다) |
| **ⓒ** 둘 다 둔다 | 최소 변경 | **같은 일을 하는 손잡이가 둘** — 저장소 주석의 반복되는 규율(「두 자리에 같은 것을 두지 않는다」, `App.tsx:449-450`)과 정면으로 어긋난다 |

⚠ **어느 쪽이든 함께 정해야 할 것**: 헤더 「프로젝트 추가」 버튼의 **게이트**. 「관리」가 `may_manage`(그 프로젝트의 관리 권한)인 데 반해, **생성은 `PROJECT_MANAGE` capability 보유 여부**라 판정 대상이 다르다(`projects.py:153`). 프로젝트가 **0개인 사람**도 만들 수 있어야 한다면 `selected?.may_manage` 로는 절대 열리지 않는다 — `noProjects` 갈래(`ProjectPage.tsx:292-298`)에서는 화면이 `Empty` 만 그리고 레일도 안 세운다(`ProjectPage.tsx:230-235`).

---

## Q5. A-1 권한 게이트를 빼면 **무엇이 함께 움직이나**

### **게이트를 읽는 자리 — 전수 4건** (`grep -rn "may_assign_in" backend frontend`)

| # | 파일:줄 | 무엇 | **이번 변경 대상인가** |
|---|---|---|---|
| 1 | `modules/work/projects.py:494` | **정의** `may_assign_in(principal, project_id) → principal.allows(TASK_ASSIGN, project=...)` | 정의는 남는다 (2·4 가 쓴다) |
| 2 | `modules/work/assignments.py:59` | Protocol 선언 | 남는다 |
| 3 | **`modules/work/projects.py:230`** | **자동 초대** `join_for_assignment()` 의 첫 줄 `if not self.may_assign_in(...): return False` | **★ 이 한 줄이 A-1 이다** |
| 4 | `modules/work/assignments.py:171` | **`plan_project_work()`** — 프로젝트에 계획 줄을 올릴 때. 실패하면 `TaskError("이 프로젝트에 업무를 올릴 수 있는 자격이 없습니다")` | **다른 용도다 — 건드리지 않는다** |

**프론트엔드 히트 0건.** 화면은 이 게이트를 모른다.

**자동 초대를 부르는 자리 둘**(참고):
- `modules/work/assignments.py:237` — 담당 교체 제안
- `modules/work/requests.py:476` — 업무 요청 발송

⚠ **4번이 함께 움직이지 않는다는 점이 중요하다.** 「배정 권한 없는 사람은 그 프로젝트에 업무를 올릴 수 없다」는 규칙은 그대로 산다. A-1 이 뒤집는 것은 **오직 「붙이기」 한 줄**이다.

### **깨지는 테스트 — 정확히 1건**

게이트를 만지는 테스트 파일 셋(`grep -rln "join_for_assignment|may_assign_in|자동 초대|auto_joined" backend/tests`):

| 파일 | 건수 | 영향 |
|---|---|---|
| `tests/contract/test_project_membership_follows_work.py` | 18 | **1건 깨진다** (아래) |
| `tests/unit/test_project_auto_join_flag.py` | 3 | **0건** — `auto_project_join` **칸을 읽는 법**만 본다(`:26·34·42`). 게이트와 무관 |
| `tests/integration/postgres/test_project_participation.py` | 3 | **0건** — 동시성·유니크 인덱스. `POSTGRES_TEST_URL` 필요라 기본 스위트에 안 든다 |

**깨지는 그 1건** — `test_project_membership_follows_work.py:121-159`
`test_the_key_is_assigning_in_that_project_not_managing_it`

무엇을 주장하나 (docstring `:122-130`):
> 「열쇠는 그 프로젝트에서의 **업무 배정 권한**이다. 관리 권한이 아니고, 『배정이 성공했다』도 아니다.」

실행 흐름과 **깨지는 줄**:

| 줄 | 무엇 | 게이트 제거 후 |
|---|---|---|
| `:132-134` | jiho 를 `member` 로 붙이고 `may_manage is False` 확인 | 그대로 통과 |
| `:136-137` | jiho 의 `POST /projects/{id}/tasks` 가 **422** — `plan_project_work` 게이트(=위 4번) | **그대로 통과** (그 게이트는 안 건드린다) |
| `:139-144` | jiho 가 조직 축 권한으로 mina 에게 **reassign → 200** | 그대로 통과 |
| **`:148`** | **`assert _selector(client, MINA) == set()`** — 「배정은 됐지만 **초대는 안 된다**」 | ❌ **실패한다.** mina 가 붙으므로 `{"한빛 통합 마케팅"}` 이 된다 |
| `:151-158` | yuna(배정 가능자)가 같은 일을 하면 붙는다 | 통과하지만 **대비 자체가 무의미해진다** |

→ **이 테스트는 한 줄 고치는 것이 아니라 주장이 뒤집힌다.** 이름·docstring·`:148` 단언을 함께 다시 쓰는 일이다.

**깨지지 않는 이웃 둘** (헷갈리기 쉬워 명시):
- `:460-476` `test_no_new_rejection_branch_appears_on_the_invite_path` — jiho 의 reassign 이 **422 「assignment scope」로 먼저 막힌다**(`:472-473`). **배정 자체가 안 되므로** 초대 게이트에 닿지 않는다. 통과 유지.
- `:170-188` `test_direct_assignment_is_not_one_of_the_two_places` — 직접 배정 업무에는 `project_id` 가 없다. 통과 유지.

**나머지 `== set()` 단언 12곳**(`:81·96·167·186·205·220·240·265·346·383·475`)은 **전부** ⓐ 「붙기 전」 사전 확인이거나 ⓑ 자동 **해제**(D-13~D-15) 후 확인이다 — 영향 없음.

**아키텍처 테스트 0건** — 시그니처·라우트가 안 바뀌므로 `tests/architecture/test_operation_inventory.py` 는 움직이지 않는다.

### **SPEC-005 에서 고쳐야 할 줄 — 목록** (`20-spec/spec-005-projects.md`)

전수 근거: `grep -n "may_assign_in\|D-12\|배정 권한\|관리 권한 없는" spec-005-projects.md` → **히트 19줄.**

| 줄 | 지금 문장 | 성격 |
|---|---|---|
| `:152` | §1 범위 목록 「자동 초대 … **(확정 — D-11·D-12)**」 | 표기 |
| `:526` | 시나리오 **S-5** 「프로젝트 밖 사람에게 일을 보내면 그 사람이 프로젝트를 읽는다 (D-11·D-12)」 | 표기 (본문 서사는 그대로 참) |
| `:591` | 붙는 자리 표 「요청 발송 · 담당 교체 제안 \| 자동 초대 한 겹이 붙는다 **(확정 — D-11·D-12)**」 | 표기 |
| `:641` | 인용 블록 「**그 프로젝트에서 업무를 배정할 수 있는 사람은**, 배정받는 사람을 그 프로젝트에 참여시킬 수 있다. **(확정 — D-12)**」 | **★ 본문 — 핵심 문장** |
| `:647` | 계약 표 「열쇠 \| **업무 배정 권한**이다. **프로젝트 관리 권한이 아니다**」 | **★ 표 행** |
| `:648` | 계약 표 「판정 \| **「이 사람이 그 프로젝트에서 배정할 수 있는가」**」 | **★ 표 행** |
| `:649` | 계약 표 「이미 붙어 있으면 \| 아무 일도 안 일어난다(멱등)」 | 유지 |
| `:651` | 계약 표 「새 거절 갈래 \| **0건**」 | 유지 (더 참이 된다) |
| `:653-657` | 「**왜 관리 권한이 아닌가** (확정 — D-12)」 문단 전체 | **★ 문단 — 다시 쓸 자리** |
| `:790` | §5 요약 표 「자동 초대의 열쇠 \| **그 프로젝트에서의 업무 배정 권한**」 | **★ 표 행** |
| `:791` | §5 요약 표 「자동 초대의 멱등 \| 이미 붙어 있으면 아무 일도 안 일어난다」 | 유지 |
| `:823-824` | 「자동 초대는 새 거절 갈래를 만들지 않는다 (도출 — D-12). **붙이는 권한을 배정 권한이 함의하므로**…」 | **★ 근거 문장이 바뀐다** (이제 「게이트가 없으므로」) |
| `:854` | 표 「자동 초대의 판정 \| **그 프로젝트에서의 업무 배정 권한**」 | **★ 표 행** |
| `:858` | 표 「새 오류 코드 \| **0건** (도출 — D-12·D-14·D-19)」 | 유지 |
| `:902` | 「**프로젝트 관리 권한을 넓히지 않는다** (확정 — D-12)」 | **유지해도 된다** — 넓히지 않는 것은 계속 참이다 |
| `:971` | 인수조건 「프로젝트 밖 사람에게 업무를 보내면 그 사람이 그 프로젝트를 읽게 된다 (D-11·D-12)」 | 표기 (조건 자체는 유지) |
| `:1061` | 인수조건 묶음 제목 「**자동 초대 (D-11·D-12)**」 | 표기 |
| **`:1068`** | **인수조건** 「**프로젝트 관리 권한이 없는 참여자**가 배정해도 붙는다 — 열쇠가 **배정 권한**이다.」 | **★ 인수조건 — 백로그가 지목한 그 줄** |
| `:1125` | 결정 대조표 「**D-12** \| 열쇠는 배정 권한이다 \| §4 자동 초대 · §4 에러 · §6 자동 초대」 | **★ 대조표 행** |

> ⚠ **인수조건은 `:1068` 한 줄이다.** 그 줄이 속한 체크리스트 「자동 초대 (D-11·D-12)」(`:1061-1073`)의
> **나머지 6줄은 전부 그대로 참이다** — 붙는 자리 둘, `member` 로 붙음, 멱등, 새 오류 코드 0,
> 프로젝트 없으면 무동작, 새 라우트 0.

### **WORK-005 에서 고쳐야 할 줄** (`30-work/work-005-projects.md`)

전수 근거: 같은 grep → **히트 7줄.**

| 줄 | 지금 문장 | 성격 |
|---|---|---|
| `:133` | 「…(D-11·D-12 · 어긋남 ④)」 | 표기 |
| `:563` | 근거 결정 목록 「**D-11**(자동 초대, 사용자 결정) · **D-12**(열쇠는 배정 권한)」 | **★ 뒤집힌 결정을 가리킴** |
| `:583` | 「열쇠는 **`may_assign_in`**(`projects.py:299-300`)이다. **`project.manage` 를 요구하지 않고…**」 | **★ 본문 — 구현 지시 문장** |
| `:616` | 「**`project.manage` 를 넓히지 마라** (D-12). 넓히면 참여자 붙이기/떼기 전체가 열린다」 | **유지 가능** |
| **`:646`** | **인수조건** 「**관리 권한이 없는 참여자**가 배정해도 붙는다 — 열쇠가 **배정 권한**이다.」 | **★ WORK 쪽 인수조건** |
| `:986` | E2E 「E-17 \| **관리 권한이 없는 사람**으로 연다 \| 헤더에 관리 모달 손잡이가 없다」 | **A-1 과 무관 — 그대로 둔다** (Q4 가 쓰는 줄이다) |
| `:1103` | 검증표 「H \| 자동 초대 (D-11·D-12) \| **7** \| BE-2 \| `make test-contract` · E2E E-9」 | **★ 건수 7 이 바뀔 수 있다** — Q5 의 「깨지는 1건」이 이 묶음 안이다 |

⚠ `:583` 이 인용한 줄 번호 `projects.py:299-300` 은 **지금 소스와 어긋나 있다** — 실제 `may_assign_in`
정의는 `modules/work/projects.py:494` 이고 자동 초대의 게이트 호출은 `:230` 이다. 이 줄을 손볼 때
**줄 번호도 함께 맞추는 것이 옳다**(기존 부채이지 이번 변경이 만든 것은 아니다).

### **DEC-004 — 함께 손봐야 할 관련 결정**

`10-decision/decision-004-projects.md`:

| 결정 | 줄 | A-1 이 닿나 |
|---|---|---|
| **D-12** 「자동 초대의 열쇠는 `task.assign` 이다」 | **`:321`** (본문), `:692`(대조표 「판정은 `may_assign_in`」), `:710`, `:627` | **★ 뒤집는 대상.** 취소선 + 사유 |
| **D-11** 「배정·발송 시 `member` 로 자동 초대」 | `:296`, `:763` | **그대로 산다.** 붙는 관계(`member`)도 붙는 자리(둘)도 안 바뀐다 |
| **D-13** 「거절·철회되면 뗀다」 | `:343-356` | **그대로.** 떼는 쪽은 게이트를 안 본다 — `release_for_assignment()`(`projects.py:247`)에 `principal` 인자조차 없다 |
| **D-14** 「떼는 조건은 둘 다 맞을 때만」 | `:358` | **그대로.** 조건 ①은 `auto_joined_by()`(`projects.py:90`)가 배정 행의 칸을 읽는다 |
| **D-15** 「수락 뒤 취소·완료돼도 안 뗀다」 | `:382-392` | **그대로** |

⚠ **한 갈래만 함께 확인할 것**: D-12 를 뒤집으면 **붙는 사람이 늘어난다** → 그만큼 **떼는 자리(D-13·D-14)를 지나는 사람도 는다**. 조건 ①(`auto_project_join` 칸)이 그 판정을 들고 있으므로 **논리는 그대로 성립하지만**, 「배정은 됐는데 초대 게이트에 걸려 안 붙던」 사람이 이제 붙었다가 거절 시 떼어지는 경로가 **처음으로 실행된다.** `test_project_membership_follows_work.py:192-267`(떼는 자리 넷)이 그 경로를 이미 덮고 있다.

⚠ **파생 문서 각주**: `:49`·`:82`·`:90`·`:92`(결정 분류 표에 D-12 가 「코디 기본값·제안」으로 실려 있다) · `:811`·`:827` — 뒤집으면 **분류표의 성격이 바뀔 수 있다**(제안 → 사용자 결정으로 대체). 정본 판단은 코디·사용자.

---

## 못 찾은 것 · 확인하지 못한 것 (숨기지 않는다)

1. **B-9 의 실제 재현 조건** — §Q3 참조. 화면을 띄우지 못해(지시상 금지) 「사용자가 어느 페르소나로 어느 업무를 눌렀는가」를 확인할 수 없었다. 대신 **코드 분기 전수 + 데모 시드 전수**로 「그 조합이 코드상 나오지 않는다」까지 확인했다. 찾아본 방법: `ProjectTaskPanel.tsx:134-154` 분기 전수 · `labels.ts:1007-1010` 문구 대조 · `demo_work.py:125-169` 시드 12건 전수 · `application.py:938-988` 권한 분기 추적.
2. **sticky 의 브라우저 실측** — 렌더링을 돌리지 않았다. 결론은 **CSS 명세상의 3가지 실패 조건을 전수 배제**하는 방식으로 냈다(§Q1). 실측이 필요하면 구현 워커가 첫 5줄을 넣고 **한 번 열어 보는 것**으로 5분 안에 닫힌다 — 되돌리는 비용도 그 5줄이다.
3. **`may_manage` 가 데모에서 실제로 어느 페르소나에게 참인지** — 코드(`projects.py:172-179`·`demo_work.py:194-195`)로 「만든 사람=lead, mina=member」까지 읽었고 런타임 확인은 하지 않았다.

---

## 검증 — read-only 확인

```
$ git status --porcelain --untracked-files=no | wc -l   # 조사 전후 동일
$ git stash list                                        # 건드리지 않음
```

- **이 워크트리에 수정·생성·삭제 0건.** 유일한 산출물은 이 리포트 1개(문서 리포 쪽 경로).
- **테스트·서버·`reset-demo` 실행 0건.** 쓴 명령은 `cat`/`sed -n`/`grep`/`wc`/`ls`, 그리고 바이트 계산용 `python3` 1회(`/tmp` 에서, 저장소 파일 미접근)뿐이다.
- canonical(`/Users/kknaks/git/toy_pr2/*`) 접근 0건.
