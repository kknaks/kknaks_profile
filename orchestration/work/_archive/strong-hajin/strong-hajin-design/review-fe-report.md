# 검수 리포트 — WORK-007 Phase F-1 · F-2 · F-3 프론트 (2026-09-28)

검수자: `@sc-ax-reviewer` (read-only). **코드를 한 줄도 고치지 않았다** — 산출물은 이 파일 하나다.

- 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`)
- base: `origin/main` = `b145745`. **`HEAD == origin/main`** — 커밋·push 0건
- 검수 범위: **`frontend/` 만.** `backend/` diff 는 이 검수의 대상이 아니다(§7 에 사실만 적는다)
- 기준: 확정 시안 `TaskDetail.html` · SPEC-007 v0.2.0 · WORK-007 F-1(`:342`)·F-2(`:379`)·F-3(`:416`)
- 대조 대상: `fe-report.md` — **믿지 않고 diff·소스로 확인했다**

> ⚠ **검수 도구 주의.** `WorkModals.tsx` 에 **원시 NUL 바이트 둘**이 들어 있어(W-1) `grep` 이 이 파일을
> **binary 로 보고 건너뛴다.** 이 리포트의 모든 grep 은 `grep -a` 로 다시 돌린 것이다. `-a` 없이 돌리면
> 「WorkModals 에 그 문자열이 0건」이라는 **거짓 음성**이 나온다 — 나도 처음 한 번 그렇게 속았다.

---

## 0. 판정 (FAIL 2 · WARN 12)

**FAIL.**

**FAIL-1 이 이 판정의 전부다** — 시안 CSS 를 옮긴 `styles/task-detail.css` 129줄이 **전부 `.scax-td` 스코프
아래**인데 **그 클래스를 붙이는 요소가 저장소 어디에도 없다.** 마크업은 시안대로 섰는데 **그 마크업을
시안으로 만드는 규칙이 하나도 닿지 않는다** — 2열도, 3행 스크롤도, 파란 「추가」도, 값 한 줄 상자도
화면에 없다. jsdom 은 CSS 를 적용하지 않으므로 **테스트 1082건이 전부 초록인 채로 시안 계약이 깨진다.**
브리프 §4 가 「조용히 통과하는 자리」로 지목한 바로 그 모양이다.

**FAIL-2** 는 프로젝트 칸의 이름이 **단추가 아니다**(§2.4.4 · 시안 `:182`).

**구조·동작 계약은 거의 전부 충족이다** — 구획 열여섯이 하나도 사라지지 않았고(§3), 선행 배선이
실제로 복구됐으며, 못 읽는 후행의 제목·식별자가 DOM 어디에도 없고, 저장이 칸마다 따로 나가며
거절 문장이 서버 것 그대로 선다. **FAIL-1 은 CSS 한 겹의 문제이고 되돌리기가 «한 줄»이다** —
드로어 본문에 `scax-td` 를 붙이거나 스코프를 걷으면 나머지가 그대로 산다.

---

## 1. 시안 대조표 — 브리프 §3 여덟 항목

| # | 항목 | 마크업 | **화면(CSS 적용 후)** | 근거 |
|---|---|---|---|---|
| 1 | **덩어리 여섯** — 업무 메타·업무 정보·연관 업무·자료·진행과 판단·이력 | **충족** | **충족** | `WorkModals.tsx:1854`(메타) · `:1949`(업무 정보) · `:2104`(연관 업무) · `:2428`(자료) · `:2448`(진행과 판단) · `:2662`(이력). 배너는 `:1940` 으로 메타 **아래**·업무 정보 **위**다(§2.1) |
| 2 | 세 덩어리 제목이 **같은 레벨** | 충족 — 다섯 다 `.block__row > h3` | **불충족** | `.scax-td .block__row > h3 { font-size:15px; font-weight:700; border-bottom… }`(`task-detail.css:26`)가 **안 걸린다** → h3 브라우저 기본값으로 선다. **FAIL-1** |
| 3 | **업무 정보는 1열**(내용 → 체크리스트) | 충족 — `.stack` 안에 `.cell` 둘, 내용이 먼저 | **미적용** | `:1951` `<div className="stack">` · `:1952`(내용) → `:1978`(체크리스트). `.scax-td .stack { display:grid; gap:14px }`(`:36`) 미적용 — 블록 요소라 시각 결과는 비슷하나 `gap` 이 없다. **FAIL-1** |
| 4 | **연관 업무 2열 짝** — 상위\|프로젝트 · 하위\|선행 · 참고\|후행 | 충족 — DOM 차례가 정확히 그 여섯 | **불충족 — 1열로 쌓인다** | `:2126`~`:2418` 여섯 `RelationCellFrame` 이 `<div className="cols">`(`:2125`) 안에 있고 test 가 차례를 센다(`TaskDetailRelations.test.tsx:254`). 그런데 `.scax-td .cols { display:grid; grid-template-columns: 1fr 1fr }`(`:32`)가 **안 걸려** 여섯 칸이 **세로로 여섯 줄**이 된다. **짝이 화면에서 사라진다.** **FAIL-1** |
| 5 | **자료 2열** — 참고 자료 \| **결과 자료** | 충족 | 라벨 충족 · **2열 불충족** | 라벨: `labels.ts:417`·`:419` · `renderMaterials:1577`. 「산출물」이 드로어에 **0건**임을 `TaskDetailRelations.test.tsx:226` 이 `dialog.textContent` 로 센다(다른 표면의 「산출물」은 범위 밖 — OQ-705). 2열은 `.cols` 라 **FAIL-1** |
| 6 | 목록 **3행 기본 + 칸 안 스크롤**, 머리는 스크롤 밖 | 충족 — 머리가 `.scroll` **밖** | **불충족 — 상한도 스크롤도 없다** | `RelationCellFrame:414-439` 가 `.cell__head`(`:431`) 를 `children` **밖**에 두고 `RelationList:448-488` 이 `<div className="scroll">`(`:485`) 로 목록만 감싼다. 그런데 `.scax-td .scroll { max-height:105px; overflow-y:auto }`(`:41`)·`.scroll--tall{280px}`(`:48`)가 **안 걸린다** → 하위 30개가 연관 업무를 화면 밖으로 민다(시안 주석 `:47-48` 이 막으려던 바로 그것). **FAIL-1** |
| 7 | 「편집」은 **A 에만** | 충족(조건 하나) | 충족 | `:1811` `editable && relDraft === null`. C(연결 편집)에서 사라지고 읽기 전용에는 **안 그린다**. B 무대 조건은 **W-8** |
| 8 | 「추가」는 **글자 + 파란색** | 글자 충족 | **파란색 불충족** | `RelationAddRow:512-540` 의 `<span className="rel__addlabel">{taskDetail.add}</span>` — 글자는 「추가」다. 색은 `.scax-td .rel__addlabel { color: var(--scax-color-accent); font-weight:600 }`(`task-detail.css:123`)뿐이라 **안 걸린다** → 검은 보통 글자. **FAIL-1** |

---

## 2. 동작 계약 대조표 — 브리프 §3 아홉~열아홉

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 9 | **선행 배선 복구** — 상세 조회가 `predecessors` 를 채우나 · **`successors` 도 같은 함정에 안 빠졌나** | **충족** | `readDetail()`(`:772-791`)이 `checklist·references·delivery·children·parent·predecessors·successors·hidden_successor_count·project_id` **아홉**을 담는다(전에는 다섯). 그리는 쪽은 `related`(`:1231-1239`)와 `shown`(`:1230`)을 읽는다 — `task.predecessors` 등 여섯 건은 전부 `useState` **초기값**이고(`:651`·`:655`·`:676-679`) 렌더에 prop 을 읽는 자리가 없다(`grep -a` 로 재확인). `MyWorkPage.tsx:578-599` 가 목록에서 여는 길도 `getTask` 를 태운다. test `TaskDetailRelations.test.tsx:134` |
| 10 | **못 읽는 후행은 건수만** — 제목·담당자가 화면 어디에도 안 나오나 | **충족** | 서버가 `task_id` 조차 안 주므로 화면이 그릴 재료가 없다. 읽기 상태는 `:2400` `taskDetail.hiddenSuccessors(n)` 한 줄, 편집 상태는 `:2388` `hiddenSuccessorsLocked(n)`. **DOM 에 `data-*`·`key` 로도 남지 않는다** — 후행 줄의 `key` 는 `row.task_id`(`:2405`)이고 비공개는 `rows` 에 아예 없다. test `:261`(줄 2개 · 셈 3) |
| 11 | **못 읽는 선행도 건수만이고 미완으로 센다** | **충족** | 건수 한 줄 `:2298` `hiddenPreceding(n)` — **빈 줄을 늘어놓지 않는다**(`visiblePredecessorsOf` 가 `title===null` 을 뺀다). 셈은 `precedingCountOf`(배열 길이 = 읽는 수 + 못 읽는 수) · `unfinishedPrecedingCountOf`(`workRows.ts:164-166`)가 `state !== "done" && state !== "cancelled"` 로 걸러 **`state === null` 을 미완에 넣는다**. test `:337`(`1 · 미완 1`) · `:351`(`2 · 모두 완료`) |
| 12 | **선행=시작 / 하위=완료** — 문구가 갈려 있나 | **충족** | 배너 「시작할 수 없습니다」(`:1940`·`labels.ts:414`) vs 하위 「아직 끝나지 않은 하위가 있습니다」(`:2553`). 두 구획이 자리도 문구도 다르고 한 낱말로 뭉갠 자리가 없다. test `:294`. ⚠ 라벨 상수 쪽은 **W-4** |
| 13 | **화면이 유효성을 선제로 막지 않는다** | **충족** | `loadRelationChoices()`(`:1555-1563`)가 `getTasks(true)` 에서 **자기 자신만** 뺀다. `relationOptions(taken)`(`:1341-1344`)가 그 칸에 **이미 걸린 것**을 뺀다. 순환·읽기 권한·프로젝트 일치·V-8 은 **한 줄도 안 거른다**. test `:443` 이 **조상이 후보에 «있다»**를 센다 |
| 14 | **거절 문장을 그대로 보여주나** | **충족** | `request()`(`api.ts:137-141`)가 `detail` 문자열로 `ApiError` 를 던지고 → `saveCell`(`:1367-1376`)이 `error.message` 를 그 칸에 담고 → `RelationCellFrame:437` `<p className="rel__error" role="alert">{error}</p>`. **화면이 코드로 갈라 문장을 고르는 자리가 0건.** test `:513` 이 `textContent` 가 서버 문장과 같음을 센다 |
| 15 | **저장은 칸마다 따로** — 한 칸 거절이 나머지를 되돌리나 | **충족** | `saveRelations()`(`:1385-1449`)가 여섯 칸을 **따로** 호출하고 `saveCell` 이 각각 잡는다. 실패해도 `allOk=false` 만 서고 성공한 칸은 그대로다. 끝에 `readDetail()` 한 번으로 **거절된 칸은 서버의 옛 값으로 되돌아온다**(되돌릴 값을 따로 안 든다). test `:513` |
| 16 | **비공개 후행에 해제 단추가 없나** | **충족** | 편집 목록 `rows` 는 `relDraft.successors`(= 읽을 수 있는 것만)로만 만들고, 비공개는 `after` 의 건수 한 줄이다(`:2386-2396`). test `:548` 이 해제 단추가 **읽을 수 있는 하나에만** 있음을 센다 |
| 17 | **OQ-709** — 못 읽는 선행만 남았을 때 `[시작]` 을 **막지 않나** | **충족** | `startBlockedByPredecessors`(`workRows.ts:145-147`)가 `blockingPredecessorsOf` 를 쓰고 그 함수는 `title !== null` 로 **못 읽는 선행을 뺀다**(`:113-117`). test `:337` 이 「셈은 `1 · 미완 1` 인데 `[시작]` 이 `disabled === false`」를 센다. ⚠ 배너까지 연 것은 **W-12** |
| 18 | `parent_task_id` + `project_id` 를 **한 PATCH 에 안 보내나** | **충족** | `saveRelations` 가 상위(`:1399-1403`)와 프로젝트(`:1406-1410`)를 **다른 `updateTask` 두 번**으로 보내고, 프로젝트 쪽은 회차를 `getTask` 로 다시 읽는다(상위 이동이 회차를 올렸으므로). `api.ts:263-274` 도 두 칸을 각각 `!== undefined` 로만 싣는다. test `:489` 가 **모든 호출에 둘이 함께 있지 않음**을 전수로 센다 |
| 19 | 후행 해제가 **멱등이 아님**(두 번째 404)을 견디나 | **충족** | 해제는 `saveCell("successors", …)` 안이라 404 의 서버 문장이 후행 칸 아래에 서고, 뒤이은 `readDetail()` 이 **지금 사실**로 목록을 다시 맞춘다. 화면이 낙관적으로 줄을 지우지 않는다(`:1440-1447`) |

---

## 3. 구획 이사 대조 — 착수 전 목록(`fe-survey-report.md` §4)과 대조

**사라진 구획 0건.** 열여섯을 전수로 짚었다.

| 착수 전 구획 (survey §4) | 지금 자리 | 확인 |
|---|---|---|
| 머리 `headerExtra` — 상태 배지·기한 초과·`v{version}` | `업무 메타` 오른쪽 | `:1806-1808` |
| 아래 `footer` — 취소/제안/시작/완료 처리/… | 그대로 `Shell footer` | `:1700`~ |
| 1 `완료 확인 대기` | `진행과 판단` | `:2456` |
| 2 `보완 필요` | `진행과 판단` | `:2477` |
| 3 `담당 변경 대기` | `진행과 판단` | `:2489` |
| 4 `응답 대기 제안` | `진행과 판단` | `:2506` |
| 5 `완료를 막는 하위` | `진행과 판단` | `:2552` — 하위 **관계**는 `연관 업무` 에 따로(`:2192`). 같은 값을 두 자리에서 다르게 쓰는 것이 §2.1 계약이다 |
| 6-a `handover` 담당자 변경 폼 | `진행과 판단` | `:2569` (`canAssign && !readOnly` 조건 그대로) |
| 6-b `업무 출처` origin-chip | `업무 메타` 왼쪽 | `:1884` |
| 6-c 제목 `input.title-input` | `업무 메타` — **「편집」 안에서만** | `:1858-1866` |
| 6-d `meta-grid` 담당자·시작일·기한 | `업무 메타` 사실 한 줄 + 「편집」 안의 `DateField` 둘 | `:1870-1874` · `:1902-1928` |
| 6-e `체크리스트` | `업무 정보` 둘째 칸 (`!readOnly` 조건 **그대로**) | `:1979-1990` |
| 6-f 업무 내용 `textarea` | `업무 정보` **첫째** 칸 (읽을 땐 `.desc`) | `:1952-1972` |
| 7 막힘 사유(읽기) | `진행과 판단` | `:2609-2613` |
| 8 `막힘 사유 입력` | `진행과 판단` | `:2624` |
| 9 `선행업무` | `연관 업무` 2행 오른쪽 | `:2267` |
| 10 `상위 업무` | `연관 업무` 1행 왼쪽 | `:2126` |
| 11 `하위 업무` | `연관 업무` 2행 왼쪽 — **읽기 전용에서도 «선다»**(§2.7 W-3 대로 바뀌었다) | `:2192` |
| 12 `참고 업무` | `연관 업무` 3행 왼쪽 (`!readOnly` — 서버가 값을 안 주므로 §2.7 대로) | `:2311` |
| 13 참고 자료 | `자료` 왼쪽 | `renderMaterials("input")` `:1577` |
| 14 산출물 | `자료` 오른쪽 — **「결과 자료」** | 같은 함수 · `labels.ts:413` |
| 15 `활동·이력` | `이력` (덩어리 하나를 혼자) | `:2662` |
| 16 AX | **덩어리가 아니다** — `업무 메타` 오른쪽 단추 | `:1819-1836` |

- **덩어리가 비면 서지 않는다** — `hasProgressBlock`(`:1480-1489`)이 여덟 조건의 `or` 이고 `:2447` 이 그것으로 가린다.
- `TaskDetailRelations.test.tsx:185` 「상태·판단 구획 여덟이 「진행과 판단」 안에 그대로 있다」가 이 표를 못질한다.
- **새로 선 것 셋**: 프로젝트 칸(`:2157`) · 후행 칸(`:2383`) · 시작 막힘 배너(`:1940`).

---

## 4. FAIL

### FAIL-1 — `task-detail.css` 129줄이 **한 요소에도 안 걸린다** (`.scax-td` 가 DOM 에 없다)

**무엇이 계약과 다른가.**
`frontend/src/styles/task-detail.css` 는 확정 시안의 `<style>` 을 옮긴 파일이고 **규칙 전부가
`.scax-td` 로 시작한다**(`:17`~`:136`, 예외 0건). 그 스코프를 붙이는 요소가 **저장소 전체에 없다.**

```
$ grep -ran "scax-td" frontend/src
frontend/src/styles/index.css:100:      … `.scax-td` 아래 …            ← 주석
frontend/src/styles/task-detail.css:7:  … `.scax-td` 아래에 넣었다 …    ← 주석
frontend/src/styles/task-detail.css:17-136                              ← 선택자 49건
(.tsx · .ts 0건)
```

- `Drawer`(`ds/Modal.tsx:93-120`)는 `className` prop 을 **받지 않는다**(`OverlayShellProps:49-63`에 없다).
  `Modal` 은 받지만 `Shell` 이 `(props: OverlayShellProps) => ReactElement` 로 좁혀져 있어(`:1691`)
  넘길 자리가 없고, 실제로 넘기지도 않는다(`:1695-1843` 에 `className` 0건).
- 다른 CSS 파일이 대신 받쳐 주지도 않는다 — `styles/*.css` 전수에서 `.block`·`.cols`·`.stack`·
  `.scroll`·`.one`·`.private`·`.desc`·`.rel__*` 를 **스코프 없이** 정의하는 자리가 **0건**이다
  (`.material-list` 만 `components.css:560-561` 에 살아 있다).

**무엇이 화면에서 사라지나.** 시안 대조표 §1 의 ②③④⑤⑥⑧ 전부 — 특히

| 잃는 것 | 죽은 규칙 |
|---|---|
| **연관 업무·자료의 2열** → 칸 여섯이 **세로로 쌓인다** | `task-detail.css:32` `.cols{grid-template-columns:1fr 1fr}` |
| **목록 3행 상한과 칸 안 스크롤** → 하위 30개가 화면을 민다 | `:41` `.scroll{max-height:105px;overflow-y:auto}` · `:48` `--tall{280px}` |
| **값 한 줄 상자**(상위·프로젝트) → 테두리·배경·34px 없음 | `:58` `.one` |
| **빈 상태 점선 상자** | `:79` `.empty` |
| **🔒 비공개 줄의 점선 상자** | `:83` `.private` |
| **「추가」의 파란색** | `:123` `.rel__addlabel` |
| **거절 문장의 danger 색** | `:131` `.rel__error` |
| **덩어리 머리 15px/700 + 밑줄** | `:22`·`:26` `.block__row` |
| **칸 머리 13px/600 + 셈 11px + 단추 오른쪽 정렬** | `:52-55` `.cell__head` |
| **메타 한 줄 배치**(19px 제목·12px 사실·오른쪽 정렬) | `:90-110` `.meta*` |
| **목록 줄 2열 34px** → `components.css:561` 의 **3열** 격자가 대신 걸려 빈 칸이 하나 남는다 | `:67` `.material-list li` |

**왜 테스트가 못 잡았나.** jsdom 은 스타일시트를 적용하지 않는다. `TaskDetailRelations.test.tsx:251`
의 「여섯 칸이 정해진 짝과 차례로 선다」는 `querySelectorAll(".cell")` 의 **DOM 차례**를 세므로
1열이든 2열이든 통과한다. **브리프 §4 「조용히 통과하는 자리」가 정확히 이것이다.**

**어떻게 재현하나.** 빌드 산출물에서도 같다 —
`cd frontend && npm run build` 뒤 `dist/assets/*.css` 에 `.scax-td .cols{…}` 가 들어 있고,
`dist/assets/*.js` 에 `scax-td` 문자열이 **없다**. 브라우저에서는 드로어를 열고 개발자 도구로
`연관 업무` 구획의 `.cols` 에 계산된 `display` 를 보면 `block` 이다(`grid` 가 아니다).

**되돌리기 — 한 줄이다.** 드로어 본문의 최상위(예: `업무 메타` 를 감싸는 자리)나 `Shell` 이 그리는
겹에 `scax-td` 를 붙이면 된다. **워커의 스코프 판단 자체는 옳다**(`.block`·`.cell`·`.meta` 는 너무
일반적인 이름이다) — 스코프를 **씌우기만 하고 붙이지 않은 것**이 이 FAIL 이다.

### FAIL-2 — 프로젝트 칸의 이름이 **단추가 아니다**

**계약.** SPEC-007 §2.4.4 「`project_id` 가 있고 이름을 알 수 있다 → 이름을 **단추로**
(시안 `TaskDetail.html:182`)」 · §2.4.1 표 「프로젝트 \| — \| **이름**(단추) — 상태 없음」.
시안 `:182` 는 `<button class="scax-button scax-button--inline">하반기 제품 개편</button>` 이다.

**구현.** `WorkModals.tsx:2182-2185`

```tsx
) : projectName ? (
  <div className="one">
    <span>{projectName}</span>
  </div>
```

— **`<span>` 이다.** 같은 칸의 나머지 다섯(상위 `:2146` · 하위 `:2246` · 선행 `:2306` ·
참고 `:2360` · 후행 `:2407`)은 전부 `variant="inline"` 단추라 **여섯 중 하나만 못 누른다.**

**왜 FAIL 인가.** §2.4 「줄을 누르면 그 업무가 열린다 — **여섯 칸 전부**」가 계약이고,
`fe-report.md` §2 Phase F-2 표가 그 항목의 근거로 **다섯 줄만**(`:2134·:2234·:2294·:2349·:2395`)
댔다 — **프로젝트가 빠진 것을 §5 DS-gaps 에도 안 적었다.** 「시안과 다르게 만든 자리는 전수로
적었다」(`fe-report.md` §3 끝줄)가 이 한 건에서 어긋난다.

**참작.** 드로어에 프로젝트를 여는 통로(`onOpenProject` 류 prop)가 **없다** — 단추로 만들려면
`MyWorkPage`·`App` 쪽 배선이 한 줄 더 필요하다. **계약 불충족은 맞고 범위는 작다.**

---

## 5. WARN

### W-1 — `WorkModals.tsx:1419` 에 **원시 NUL 바이트 둘**이 들어갔다

`if (relDraft.preceding.join("␀") !== before.preceding.join("␀"))` — 구분자를 `"\0"` **이스케이프가
아니라 실제 0x00 바이트**로 적었다. 바이트 오프셋 65580·65611, 둘 다 1419줄. `origin/main` 판에는
**0건**이다(둘 다 python 으로 바이트 단위 확인).

- **동작은 맞다** — `task_id` 에 NUL 이 못 들어가므로 구분자로 안전하다.
- **도구가 조용히 멀어진다** — `grep`/`rg` 가 이 파일을 **binary 로 보고 건너뛴다.**
  `grep -rn "cell__head" frontend/src` 가 **0건**을 내놓는다(실제로는 4건). `fe-report.md` §1-3 의
  grep 근거도 같은 위험 위에 서 있다.
- 고치기: `join("\0")` 로 쓰면 끝이다.

### W-2 — 체크리스트 0건 문구가 시안과 다르다 (`taskDetail.checklistNone` 이 **미사용**)

SPEC-007 §2.3 「체크리스트가 0건이면 **「단계가 없습니다.」**(시안 `:283`)」.
`labels.ts:355` 에 `checklistNone: "단계가 없습니다."` 를 **만들어 두고 한 번도 안 쓴다**
(`taskDetail.checklistNone` 참조 0건 — `frontend/src` 전수). 실제로 서는 것은 예전 문장
`WorkModals.tsx:2065` 「아직 단계가 없습니다. 이 업무를 쪼개서 적어 두세요.」다.

### W-3 — 체크리스트 칸에 **머리가 두 번** 선다

`:1980-1985` 가 `.cell__head` 에 `<h5>체크리스트</h5>` + `.cell__n`(`1 / 3`)을 세우는데,
그 **안쪽**의 옛 구획이 `:1988-1998` 에서 `<h4>체크리스트 <span>1/3</span></h4>` + `ProgressBar` 를
다시 그린다. 시안 §2.3 의 머리는 **하나**(제목 + 셈 + 「추가」)다. 그리고 그 「추가」 입력줄이
`.cell__head` 가 아니라 **`.scroll` 안**(`:2066-2087`)에 있어 「머리는 스크롤 밖」과도 어긋난다
(FAIL-1 때문에 지금은 스크롤 자체가 없다).

### W-4 — `taskDetail.childrenBlockHeading` 이 **미사용**이고 리포트 근거가 실제 렌더와 다르다

`labels.ts:414` 에 「아직 끝나지 않은 하위가 있습니다」를 두었으나 참조 0건이다. 실제로는 같은
문장이 `WorkModals.tsx:2553` 에 **하드코딩**돼 있다(그 줄은 이 판이 만든 것이 아니다).
**계약(§3 항목 12)은 충족**이지만 — 문구가 배너와 갈려 있다 — `fe-report.md` 가 근거로 댄
`labels.ts:408` 은 **화면에 안 나가는 상수**다. 역할 `rules.md` 의 「한국어 문자열이 `labels.ts`
밖에 흩어지지 않았나」 관점에서도 **상수와 리터럴이 둘 다 남았다.**

### W-5 — `hiddenPredecessorsText` 를 import 만 하고 안 쓴다

`WorkModals.tsx:58` 이 그것을 들여오지만 호출이 **0건**이다(`hiddenPredecessorsText(` 0건).
문구가 `taskDetail.hiddenPreceding` 으로 옮겨 갔는데 옛 import 와 옛 export(`labels.ts:318`)가
함께 남았다. `tsc --noEmit` 은 통과한다(미사용 import 를 에러로 보지 않는 설정).

### W-6 — 시작 막힘 배너가 막는 제목을 **강조하지 않는다**

시안 `:270` 은 `<p><b>연동 규격 확인</b>이 끝나지 않았습니다.</p>` 이고 SPEC-007 §2.6 표도
「제목을 **강조한다**」다. 구현은 `:1942` `<p>{blockedBanner}</p>` — 문자열 하나라 `<b>` 가 없다
(`labels.ts:410` 이 제목과 조사를 한 문자열로 잇는다).

### W-7 — 선행 줄에 **담당**이 없다 (서버가 값을 안 준다)

SPEC-007 §2.4.1 표는 선행 줄을 「제목(단추) + `상태 · 담당`」으로 적는다. 구현은 상태만 낸다
(`:2305-2311`). **화면 탓이 아니다** — 응답의 `predecessors` 는
`{task_id, title, state}` 셋뿐이고(`viewModels.ts:282`) SPEC-007 §4 가 「선행의 값 자체는
손대지 않는다」로 그 모양을 고정했다. 하위·참고·후행 줄은 담당을 낸다(`:2253`·`:2373`·`:2410`).
**계약 안에서 모순이다 — 코디 판단 자리.**

### W-8 — 「편집」이 **무대 B 에서도** 담당자에게는 선다

SPEC-007 §2.2 표는 A 만 「선다」, **B 는 「서지 않는다」**(시안 `:265`)로 적는다. 구현 조건은
`editable && relDraft === null`(`:1811`) 하나라 **C 만 닫히고 B 는 안 닫힌다** — 선행이 안 끝난
업무라도 담당자가 열면 「편집」이 선다. 워커가 코드 주석(`:1807-1810`)에 「시안 B 에 없는 것은
막혔다가 아니라 **그 무대의 사람이 담당이 아니어서**다」라는 근거를 남겼다. **시안이 그 둘을
가르지 않으므로 모호하다 — 코디 판단 자리.**

### W-9 — `related` 가 **prop 과 상세 값을 한 객체에 섞는다**

`:1231` `const related: DirectTask = { ...task, children, references, predecessors, successors,
hidden_successor_count, project_id }` — 관계 배열은 **상세가 채운 state** 인데 나머지 스칼라
(`state`·`version`·`child_progress`·`derived`·`block_reason`)는 **`task` prop**(목록 투영일 수
있다)에서 온다. `shown`(`:1230`)은 `detailTask ?? task` 로 올바르게 고르므로 **두 합본이 서로 다른
규칙**을 쓴다. 브리프 §4 가 지목한 자리다.

- 실제로 틀리게 그려지는 갈래는 **찾지 못했다** — `childProgressOf`(`workRows.ts:74-90`)가
  `child_progress` 가 없으면 `children` 으로 다시 세고, `block_reason` 은 `shown` 쪽을 읽는다(`:2609`).
- 그래도 `startBlockedByPredecessors(related)` 는 `related.state` 를 본다 — 목록 투영의 상태가
  낡으면 배너가 어긋난다. `related` 를 `{...shown, …}` 로 바꾸면 규칙이 하나가 된다.

### W-10 — `readOnly` 가 **상세가 아니라 prop** 을 읽는다 (기존 부채 · 이 판이 그 위에 §2.7 을 세웠다)

`:732` `const readOnly = task.access === "read_only"` — `origin/main:539` 와 **글자까지 같다**(기존 부채).
그런데 `access` 는 **상세 응답에만 있다**(`application.py:1123`·`:1125`) — 목록 투영에는 없다.
`MyWorkPage` 는 이번 판이 prop 을 상세로 갈아 끼우게 고쳤지만(`:578-599`) **나머지 세 입구
(Today·Calendar·회의)는 여전히 목록 투영을 넘긴다**(`fe-report.md` §7②가 그 사실을 적는다).
그 길로 **읽기 전용 업무**를 열면 `readOnly === false` 가 되어 §2.7 이 「그리지 않는다」로 정한
「편집」·「연결 편집」·참고 칸·자료 칸이 그려진다(명령은 서버가 거절한다).
`(detailTask ?? task).access` 한 줄이면 `shown` 과 같은 규칙이 된다.

### W-11 — OQ-709 를 **단추뿐 아니라 배너까지** 폈다 (워커 자진 신고 ①)

SPEC-007 §2.4.3·§2.6 은 **막는 쪽**으로 적혀 있고(「화면을 막는 쪽으로 정했다」), 브리프 §4-7 의
사용자 확정이 **단추**를 열었다. 워커는 배너도 같은 조건(`startBlocked`, `:1267`)에 묶어 **둘 다**
열었다 — 「게이트가 열렸는데 『시작할 수 없습니다』가 서면 무엇을 믿을지 모른다」가 근거다.
**셈은 SPEC 대로 미완으로 센다.** 배너만 명문이 없으니 **코디 확인 자리**다(되돌리기: `:1267` 조건 하나).

### W-12 — 그 밖 자진 신고 셋 · 간헐 실패 하나

| 무엇 | 근거 |
|---|---|
| 목록에서 열면 `getTask` 가 **두 번** 나간다(`MyWorkPage:580` + 드로어 자기 effect) | `fe-report.md` §7②. 네 화면을 함께 손대야 해 이 판 밖 |
| `openMyTask` 의 `.catch(() => undefined)`(`MyWorkPage:597`)가 조회 실패를 **삼킨다** | 의도된 폴백이다 — 서랍이 자기 읽기에서 칸마다 「이 칸을 불러오지 못했습니다.」 + 「다시 시도」를 낸다(`RelationList:465-478`). 「없음」으로 그리지 않는다 |
| `design-items.md` #2 의 「내 업무」 탭 **비활성 + 사유** 미이행 | `fe-report.md` §5-1. 판정에 필요한 「부모를 든 사람」 칸이 응답에 없다 — 서버 몫 |
| 전체 스위트 간헐 실패 1건 | §8 |

---

## 6. 조용히 통과하는 자리 (브리프 §4) — 봤고 문제 없는 것도 적는다

| 자리 | 봤나 | 결과 |
|---|---|---|
| **구획이 이사 가다 사라진 것** — 이번 판 최대 위험 | 봤다 | **사라진 것 0건.** §3 표가 열여섯을 전수로 짚었다. 조건(`!readOnly`·`canAssign`)도 옛 것 그대로 옮겨졌다 |
| **`task` prop 과 상세 값이 섞인 곳** | 봤다 | **둘 찾았다** → **W-9**(`related`) · **W-10**(`readOnly`). 그리는 쪽이 prop 의 관계 배열을 읽는 자리는 **0건**(`grep -a` 로 재확인: `task.predecessors` 등 여섯 건이 전부 `useState` 초기값) |
| **빈 단언·항상 참인 단언** | 봤다 | **0건.** 새 파일 585줄 / 24 `it` / 72 `expect`. `assert`-없는 `it` 도, `toBeTruthy()` 만 있는 판도 아니다 — `:254`(배열 전체 비교) · `:274`(`.cell__n` textContent) · `:226`(`dialog.textContent` 전수) · `:348`(`disabled === false`) 처럼 값을 본다. 고친 12파일에도 단언을 약하게 만든 자리를 못 찾았다 |
| **폴백이 거절을 삼키는 곳** | 봤다 | `catch` 로 **빈 배열을 돌려 「없음」이 되는** 자리는 **0건**이다. `readDetail` 의 `catch` 는 `detailState="error"` 로 가고(`:786-790`) 칸마다 「이 칸을 불러오지 못했습니다.」 + 「다시 시도」가 선다. `loadRelationChoices`·`listProjects` 의 `catch`→`[]` 는 **후보 목록**이라 「없음」이 아니라 「고를 것이 없다」이고, 프로젝트는 그때 「비공개 프로젝트」로 읽힌다(코드 주석이 그 사실을 적는다). `openMyTask` 의 `catch` 는 **W-12** |
| **`api.ts` 밖 fetch** | 봤다 | **0건** (`frontend/src` 전수, 테스트 제외) |
| **새 DS 부품을 만든 곳** | 봤다 | **0건.** `Select`·`Button`·`Badge`·`DateField`·`ProgressBar`·`FieldMessage`·`Modal`/`Drawer` 를 그대로 쓴다. 새로 만든 셋(`RelationCellFrame`·`RelationList`·`ReleaseRow`·`RelationAddRow`)은 **이 화면 안의 조립 부품**이고 `ds/` 밖이다. 네이티브 `<select>` 를 쓰지 않고 DS `Select` 로 간 판단은 `fe-report.md` §5-3 에 적혀 있다 |
| **`.section-row` 고침이 다른 화면을 깨뜨렸나** | 봤다 — **소비처 전수** | **안 깨진다.** `origin/main` 의 6곳 중 `WorkModals` 4곳(`:224`·`:1155`·`:1807`·`:1882`)은 `.cell__head` 로 옮겨 갔고, **남은 3곳**은 `WorkModals:227`(활동·이력) · `WorkModals:3899`(근거 자료) · `RelationGraphPage:405`(연결). **셋 다 직속 자식이 `<h4>` + 단추 하나**라 `justify-content:flex-start` + `h4{margin-right:auto}` 가 `space-between` 과 **같은 자리**에 단추를 둔다. 단추가 조건부로 빠지는 두 곳(`:3903`·`RelationGraphPage:407`)도 결과가 같다(자식 하나면 양쪽 다 왼쪽) |
| **`.material-list` 고침이 다른 화면을 깨뜨렸나** | 봤다 — **소비처 전수 8곳** | **안 깨진다.** 새 규칙은 `li > .scax-button--inline { justify-content:flex-start }` 하나다. `li` 의 격자가 `minmax(0,1fr) auto auto`(`components.css:561`)라 **늘어나는 칸은 첫째뿐**이고, 그 칸의 인라인 단추는 어느 화면에서나 **제목**이다. 그래프 화면은 격자가 아예 다르지만(`components.css:582` `.graph-layout .material-list li`) 거기 단추는 `variant="text"`(→ `scax-button--text-neutral`)라 **이 선택자에 애초에 안 걸린다**(`ds/Button.tsx:74-76`, `RelationGraphPage:385`·`:425`). 나머지 6곳(`WorkModals:486·1651·2554·2995·3714·3913`)은 전부 첫 칸 제목이다 |
| **못 읽는 후행의 `task_id` 가 DOM 에 남아 있나** (`data-*`·`key` 포함) | 봤다 | **0건.** 서버가 비공개 후행의 `task_id` 를 아예 안 주므로(`successors` 배열에 자리가 없다) 화면에 값이 도착하지 않는다. 후행 줄의 `key`·`aria-label` 은 `successors` 배열에서만 나온다(`:2404-2412`). 편집 상태도 같다(`relDraft.successors` 는 읽을 수 있는 것만 — `:1309`). 하위 줄에만 `data-child-task` 가 있는데(`:2243`) 그것은 기존 속성이고 **하위는 가리는 계약이 아니다** |

---

## 7. 범위 이탈 (브리프 §5)

| 물음 | 답 |
|---|---|
| `backend/` 를 건드렸나 | **FE 워커는 아니다.** backend 파일의 마지막 수정 시각은 **15:51**(`test_task_parent_change.py`)이고 나머지는 13:2x~15:45다. FE 파일은 **16:25**(`WorkModals.tsx`), `fe-report.md` 는 **16:29** — FE 작업 창(16:0x~16:29) 안에 바뀐 backend 파일이 **0건**이다 |
| ⚠ **다만 backend diff 가 내 BE 검수 때와 다르다** | `modules/work/application.py` 가 **+293 → +357**, backend 전체가 **+650/-14 → +703/-25** 로 늘었다. `strong-hajin-design-be-fix-brief.md`(15:40)와 `application.py`(15:45) · `be-report.md`(16:05)가 그 사이에 있다 — **코디가 내 `review-be-report.md`(15:39) 뒤에 발주한 BE 수정**으로 보인다. **이 검수의 대상이 아니라 지적하지 않았다.** 다만 **`review-be-report.md` 의 PASS 는 «수정 전» 내용에 대한 것**이니 코디가 재검수 여부를 판단할 자리다 |
| WORK-007 에 없는 단계를 했나 | **아니다.** diff 19+2 파일이 전부 F-1(`WorkModals`·`MyWorkPage`·`viewModels`·`labels`·`styles`·테스트) · F-2(+`workRows`) · F-3(+`api.ts`) 의 allowed paths 안이다 |
| 커밋·push 했나 | **아니다.** `HEAD = origin/main = b1457455…` |
| 서버·프론트를 띄웠나 / 사용자 포트를 건드렸나 | **흔적 없다.** `8001`·`5176`·`54329` 를 죽이거나 재시작한 자취가 없고, 나도 건드리지 않았다. `fe-report.md` §7⑦ 이 「브라우저로 확인하지 않았다」로 같은 말을 한다 |
| 리포트 밖 문서를 고쳤나 | **아니다.** 문서 리포에서 바뀐 것은 `fe-report.md` 하나다 |

---

## 8. 검증 재현 결과 — 워커 수치와 대조

| 명령 | 워커 보고 | **내 실측** | 일치 |
|---|---|---|---|
| `npx tsc --noEmit` (frontend) | 0 에러 | **exit 0, 출력 0줄** | ✓ |
| `make frontend-test` **1회차** | — | **75 files (1 failed) · 1082 tests (1 failed)**, exit 2 | 간헐 |
| `make frontend-test` **2회차** | 75 files / 1082 tests / 0 failed | **75 passed (75) · 1082 passed (1082)**, exit 0 | ✓ |
| 떨어진 판 단독 재현 | — | `npx vitest run src/features/project/ProjectPage.test.tsx` → **57 passed**, exit 0 (0/1 재현) | — |

**1회차의 1건은 이 판과 무관한 간헐 실패다 — 근거 셋.**

1. 떨어진 판이 `ProjectPage.test.tsx > 프로젝트 > 머리의 두 손잡이 …` 이고 **이 판은 그 파일도
   `ProjectPage.tsx` 도 한 줄도 건드리지 않았다**(`git diff --stat origin/main -- frontend/` 에 없다).
2. 증상이 `Unable to find an element by: [data-testid="rail-left"]` 이고 그 판의 소요가 **2108ms** 였다 —
   `waitFor` 창이 병렬 부하에 먹힌 모양이다. 덤프에는 `header-actions` 와 요약 카드가 이미 그려져 있다.
3. **단독으로 돌리면 통과하고**(57/57) **2회차 전체도 통과한다**(1082/1082).
   2026-09-24 회고가 적은 시간 의존 불안정과 같은 모양이고, `fe-report.md` §6 이 회차마다 **다른 판**이
   떨어졌다고 적은 것과도 맞는다.

**내가 돌리지 «않은» 것 — 코디 몫**: `make frontend-assets` · `npm run build`(=`make frontend-build`) ·
`make verify`. 브리프 §6 이 지시한 둘만 돌렸다. ⚠ **FAIL-1 은 빌드로는 안 잡힌다** — CSS 도 JS 도
정상으로 빌드되고 **선택자만 아무것에도 안 걸린다.**

---

## 9. 검수 한계

1. **브라우저로 보지 않았다.** 지시대로 서버·프론트를 띄우지 않았다. **FAIL-1 은 소스 전수 grep 과
   CSS 선택자 대조로 «연역»한 것**이다 — `.scax-td` 를 내는 요소가 없고, 같은 선택자를 받쳐 주는
   다른 CSS 도 없다는 두 사실에서 나온다. **눈으로 본 것은 아니다.** 코디가 화면을 열어 `연관 업무`
   구획의 계산된 `display` 가 `grid` 인지 한 번만 보면 즉시 확정된다.
2. **반응형을 판정하지 않았다.** 시안에 반응형 규칙이 없고 이 판도 두지 않았다(`fe-report.md` §7⑦).
   좁은 폭에서 2열이 어떻게 접히는지는 계약에 없다.
3. **접근성을 전수로 보지 않았다.** `aria-label`·`role="group"`·`role="alert"` 이 새 칸마다 붙은 것은
   확인했으나 키보드 순서·포커스 트랩·스크린리더 낭독은 확인하지 않았다.
4. **고친 기존 테스트 12파일을 «전수»로 읽지 않았다.** 각 파일에서 단언을 약하게 만든 자리
   (`toBeTruthy` 로의 후퇴·`expect` 삭제)를 표본으로 훑었고 못 찾았다. 「계약이 바뀌어서 고쳤다」는
   `fe-report.md` §4-1 의 설명 자체는 SPEC-007 §2.2·§2.3·§2.7·§2.8 과 대조해 타당하다고 봤다.
5. **backend 를 판정하지 않았다.** 브리프가 범위 밖으로 두었고, 다만 §7 에 「내 BE 검수 뒤에 backend 가
   더 바뀌었다」는 사실만 적었다. 그 변경의 내용은 읽지 않았다.
6. **W-9 · W-10 의 「실제로 틀리게 그려지는 갈래」를 재현하지 못했다.** 코드 경로로는 성립하지만
   (`Today`·`Calendar`·회의가 목록 투영을 넘긴다), 그 세 입구에 읽기 전용 업무가 실제로 서는지는
   확인하지 않았다. **가능성으로만 적었다.**
7. **성능을 재지 않았다.** `getTask` 이중 호출(W-12)과 `listProjects` 의 조건부 호출이 실제 왕복 수를
   어떻게 바꾸는지는 측정하지 않았다.
