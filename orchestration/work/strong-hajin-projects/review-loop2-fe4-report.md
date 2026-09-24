# 리뷰 리포트 — strong-hajin-projects / frontend 루프2 **Phase FE-4** (2026-09-22)

**역할** `@sc-ax-reviewer` · **task-id** `task_a5e20101e12c` · **워크트리**
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · **read-only**(코드 0줄 수정 ·
커밋 0건 · 개발 서버 0회 — 뮤테이션 probe 10건은 전부 파일 복원 후 `diff` 로 원상 확인).

## 판정: **FAIL** (FAIL 1 · WARN 5)

계약(L-36 · L-42~L-48)을 **깨뜨린 자리는 없다.** 틀고정 다섯도 좌표계 0줄도 **실측으로 참**이다.
FAIL 하나는 **워커가 새로 더한 단언 하나가 부하에서 흔들린다**는 것이고, Phase FE-4 의 완료 판정
첫 줄(「`make frontend-test` 통과」)이 그 한 줄 때문에 항상 서지는 않는다. 고치는 곳은 테스트 한 줄이다.

---

## 위반 (FAIL)

### [FAIL-1] 새 L-45 단언이 **부하에서 흔들린다** — 「패시브 effect 가 쓴 값」을 `waitFor` 없이 읽는다

- **무엇이**: `frontend/src/features/project/ProjectPage.test.tsx:328-336`
  「첫 진입은 «오늘» 이 보이는 자리에서 연다 (L-45)」가 `await findByText(...)` **직후**에
  `scroll.scrollLeft` 를 읽는다. 그 값을 쓰는 것은 `ProjectGantt.tsx:149-151` 의 **패시브 effect**라
  커밋과 같은 태스크에서 보장되지 않는다. **`waitFor` 로 감싸지 않은 유일한 scrollLeft 단언**이다
  (선례 `CalendarPage.test.tsx:268` 은 `waitFor` + `fireEvent` 뒤에 읽는다. 같은 판의
  L-47 단언 `ProjectPage.test.tsx:377-380` 은 `fireEvent.click`(동기 act) 뒤라 안전하다).
- **실측**: `make frontend-test` **9회**를 돌려 그중 **1회**가 여기서 빨강이 됐다 —
  `AssertionError: expected +0 to be 68 // Object.is equality` (`ProjectPage.test.tsx:334`).
  파일 단독 실행(`vitest run ProjectPage.test.tsx`)에서도 **8회 중 2회** 같은 자리에서 났다.
  `scrollLeft` 가 `0` 으로 읽혔다 = effect 가 돌기 전에 단언이 먼저 섰다.
- **어느 인수조건**: WORK-005 Phase FE-4 완료 판정 ①「`make frontend-test`(Node 20) 통과」.
  워커 리포트 §5 의 「실패 0 · 기존 실패 0」은 **1회 실행의 값**이고, 반복하면 성립하지 않는다.
- **수정안 한 줄**: `await waitFor(() => expect(scroll.scrollLeft).toBe((4 - GANTT.openLead) * GANTT.day));`
  (`not.toBe(0)` 은 그 뒤에 그대로 둔다.)

---

## 경미 (WARN)

### [WARN-1] 「오늘 앞 여백 2일」을 **어떤 단언도 붙들지 않는다** — 리포트의 「실수치 68」 주장은 과하다

- **무엇이**: `ProjectPage.test.tsx:334` · `:346` 이 기대값을 **`GANTT.openLead` 로 되계산**한다
  (`(4 - GANTT.openLead) * GANTT.day`). 즉 **구현 상수 자신을 기준으로 재는 자기참조 단언**이다.
- **뮤테이션 실측**: `projectModel.ts:35` 의 `openLead: 2 → 0` 으로 바꿔도 **23건 전건 통과**.
  `2 → 4` 에서야 `not.toBe(0)` 하나가 잡는다(계산 결과가 0 이 되기 때문). 즉 **0·1·3 은 조용히 통과**한다.
- **어긋나는 것**: SPEC 이 아니라 **워커 리포트 §5**의 「`scrollLeft` **실수치** 68 로 잰다」는 서술.
  실제로 고정되는 것은 「0 이 아니다」뿐이다.
- **수정안 한 줄**: 한 단언만 리터럴로 박는다 — `expect(scroll.scrollLeft).toBe(68)` (주석에 `(4-2)×34`).

### [WARN-2] 「오늘이 축 **왼쪽** 밖」 갈래에서 **L-45 문면이 깨진다** — 그 갈래에 테스트가 없다

- **무엇이**: `ProjectGantt.tsx:141-142`.
  `openOffset = min(max(offset,0), days-1)` · `openLeft = max(0, (openOffset-openLead)*day)`.
  **아직 시작 전 프로젝트**(오늘 < 축 시작)는 `offset < 0 → openOffset=0 → scrollLeft = 0` 이다.
- **어느 인수조건**: **L-45** 「첫 진입에 「오늘」이 보이는 위치다 — **기간의 첫날에서 시작하지 않는다**」.
  이 갈래에서는 **정확히 기간의 첫날**에서 연다. (오늘이 축 밖이니 「오늘이 보이는 위치」가 애초에
  없다 — 그래서 계약 위반이 아니라 **계약의 빈자리**다. 다만 문면과는 어긋난다.)
- **테스트 공백**: `ProjectPage.test.tsx:338-347` 은 **오른쪽 밖**(끝난 프로젝트)만 잰다.
  **왼쪽 밖** 갈래는 단언 0건이다.
- **수정안 한 줄**: SPEC L-45 에 「오늘이 축 밖이면 가장 가까운 끝」 단서를 달고(코디 몫),
  테스트에 미래 프로젝트 케이스 1건(`scrollLeft === 0`)을 더한다.

### [WARN-3] 완료 바 `opacity:.55` — **토큰 값으로 따지면 다른 바에서 더 멀어진다**

- **무엇이**: `frontend/src/styles/projects.css:110`.
- **계산**(`fig-tokens.css` 원값 → 각자의 트랙 위 합성, sRGB 상대휘도 L · HSV 채도 S):

  | 바 | fill 합성색 | L | S |
  |---|---|---|---|
  | `in_progress` | accent `.9` over accent-20 → `rgb(98,115,248)` | **0.216** | 0.61 |
  | `blocked` | danger `.9` over danger-soft → `rgb(232,54,54)` | **0.201** | 0.77 |
  | **`done` (지금 `.55`)** | positive over fill-weak → `rgb(112,217,147)` | **0.552** | **0.48** |
  | `done` (손대기 전 `.9`) | → `rgb(25,197,82)` | 0.408 | 0.87 |
  | `not-started` | line-strong `.9` over fill-weak → `rgb(221,221,222)` | 0.72 | 0.00 |

- **뜻**: 흰 트랙(`fill-weak` = 거의 흰색) 위에서 투명도를 낮추면 **채도만 내려가는 게 아니라
  밝기가 올라간다.** `.55` 는 「혼자 쨍하다」(채도 0.87 → 0.48)는 고치지만, 그 결과 **셋 중 가장
  연한 색**이 되고 휘도는 accent·danger 의 **2.5배**로 벌어져 `not-started`(0.72) 쪽에 붙는다.
  「톤이 맞는 자리」(L-36)는 **그 사이 어디**이고 `.55` 는 그 사이를 지나쳤다.
- **수치 제안**: `.70~.72` 면 `rgb(69,207,116)` · **S≈0.67**(accent 0.61 · danger 0.77 사이) ·
  L≈0.47 로 셋이 한 띠에 든다. **최종 판정은 눈이 한다** — 아래 §「눈으로만 확인되는 것」 4번.
- **DS 토큰은 참으로 0줄**: `scax.css` · `product.css` · `fig-tokens.css` 전부 `git status` 깨끗 ·
  mtime `Sep 21 19:33`. L-36 후반부(「DS 토큰 파일이 한 줄도 안 바뀌었다」)는 **PASS**.

### [WARN-4] 「기존 실패 0건」이 아니다 — 스위트 자체가 부하에서 흔들린다 (**FE-4 밖**)

- `make frontend-test` **9회** 중 이 판 **밖**에서 난 실패(전부 재현 1회씩, 매번 다른 자리):
  - `task checklist > moves a step with the keyboard and sends the whole order` (2회)
  - `task checklist` — `expected <span></span> to be null` (1회)
  - `adjustment and resubmission > claims the judgement is reflected only when every projection settled` (1회)
  - `product surfaces > decides an AX proposal through the same judgement drawer and command path…` (1회)
- **1루프에서 흔들렸다던 `MeetingMaterials`·`ActionCenter` 는 9회 모두 통과**했다. 흔들리는 자리가
  **옮겨갔다**. 이 판의 책임은 아니지만 워커 리포트 §5 의 「기존 실패는 0건이었고」는 **1회 관측**이다.
- **범위 밖**이므로 판정에 넣지 않는다. 코디의 flaky 대장(`flaky-baseline-projects.md`)에 옮길 자리다.

### [WARN-5] 틀고정·색은 **jsdom 이 한 줄도 재지 않는다** — 되돌아가도 빨강이 안 난다

- **뮤테이션 실측**: `projects.css:90` 에서 **`align-self:stretch` 를 지워도 23건 전건 통과**.
  워커가 §5 에 스스로 적은 대로이고 숨기지 않았다 — 그래서 FAIL 이 아니라 기록이다.
  ①~⑤ 와 `opacity:.55` 는 **사용자 2차 E2E 가 유일한 관측자**다.

---

## 10항목 결과

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | 틀고정 다섯 | **PASS** | 아래 §틀고정 표. ⑤의 주장도 **CSS 로 참** |
| 2 | 좌표계 0줄 | **PASS** | 아래 §좌표계. **줄번호 산술로 검증** — 믿지 않고 셌다 |
| 3 | 워커가 정한 넷 | **WARN 2 · PASS 2** | 아래 §워커가 정한 넷 |
| 4 | 양방향 · `nearest` | **PASS** | 아래 §자동 스크롤 |
| 5 | 완료 바 `.55` | **WARN-3** | 토큰 계산표 |
| 6 | 공유 자산 0줄 | **PASS** | `src/ds/*` · `components.css` · `shell.css` · `scax.css` · `product.css` · `fig-tokens.css` **전부 `git status` 깨끗 + mtime `Sep 21 19:33`**(FE-4 는 `Sep 22 13:42~13:45`). `projects.css` 안의 `.scax-inbox-card[role="button"]`(35-38) · `.scax-gutter-list__header--sub`(30)은 **1루프 줄이고 이 판이 손대지 않았다**(파일 171→182줄 · `.scax-pj-side` 116→127 = **+11**, 신설 3곳의 줄 수와 정확히 일치) |
| 7 | 단언이 뮤테이션에 반응하나 | **WARN-1 외 PASS** | 아래 §뮤테이션 10건 |
| 8 | `mockClear` 가 단언을 약화시켰나 | **PASS — 아니다** | `mockClear` 한 줄을 되돌리면 `expected 3 to be 1` 로 **그 단언이 즉시 빨강**이다(5회 연속 재현). 범위를 좁힌 것이고 약화가 아니다. `calls[0][0] === "t-9"` 는 오히려 **mockClear 가 있어야** 의미가 산다 |
| 9 | 테스트 수치 재측정 | **FAIL-1 · WARN-4** | 아래 §테스트 실측 |
| 10 | 범위 | **PASS** | 커밋 0건(`HEAD = e46ce39` = base). FE-5 몫 **전부 mtime `≤ Sep 22 01:24`** — `ProjectTaskPanel.tsx`(01:42) · `ProjectManageModal.tsx`(00:54) · `ProjectSummaryStrip.tsx`(01:06) · `App.tsx`(01:24) · `WorkModals.tsx`(**Sep 21**) 로 이 판(13:4x)이 **한 줄도 안 건드렸다**. `backend/` 3파일이 13:41~13:43 에 같이 움직였으나 **BE-3 판의 파일**(`work/assignments.py`·`application.py`·`projects.py`)이고 지시대로 지적 대상이 아니다. 개발 서버 흔적 없음 — 13:4x 에 새로 생긴 것은 `frontend/dist/`(빌드 산출물, gitignore) 하나다 |

---

## 틀고정의 다섯 — **다 있고, ⑤의 주장도 사실이다**

| # | 무엇 | 어디 | 확인 |
|---|---|---|---|
| ① | `position:sticky; left:0` | `projects.css:90` | ✅ sticky 를 죽이는 조상(`overflow`·`transform`·`filter`·`contain`)이 `__canvas`(66)·`__plot`(73)·`__row`(83) 어디에도 **없다** |
| ② | `z-index:2` | `projects.css:90` | ✅ 같은 행에서 `__bar`(`ProjectGantt.tsx:278`)가 `__name-cell`(244)보다 DOM 뒤이고 둘 다 positioned 라 **양수 z-index 없이는 막대가 이름을 덮는다** |
| ③ | `background:var(--scax-color-surface)` | `projects.css:90` | ✅ 그리고 **값이 맞다** — 감싸는 `.scax-pj-gantt`(59)가 같은 `surface` 다. 다른 칸 색을 골랐으면 흰 띠가 남았다 |
| ④ | 머리줄 200px 을 **요소가** 덮는다 | `ProjectGantt.tsx:173` + `projects.css:70` | ✅ `paddingLeft` 인라인은 `__axis`(170)에서 **사라졌다**. 스페이서도 `sticky;left:0;z-index:2;background` 넷을 다 든다 |
| ⑤ | `align-self:stretch` | `projects.css:90` | ✅ **주장이 참이다.** `.scax-pj-gantt__row{…align-items:center}`(`projects.css:83`)이고 행 높이는 **인라인 40px**(`ProjectGantt.tsx:243`)인데 이름 칸 내용은 twisty 16px / 2줄 텍스트(label1+caption2)라 **40px 에 못 미친다.** stretch 가 없으면 위아래 여백으로 `__grid`(74) 격자가 그대로 샌다 |

**격자가 이름 칸을 지나간다는 근거도 참이다** — `__grid` 는 `left:GANTT.label`(`ProjectGantt.tsx:185`)
이라 캔버스 좌표 200 부터이고, 뷰포트 왼쪽 200px 가 보여 주는 캔버스 구간은 `[scrollLeft, scrollLeft+200]`
= 스크롤하면 전부 격자 영역이다.

---

## 좌표계 — **정말 0줄이다** (줄번호 산술로 검증)

조사 리포트(`loop2-survey-report.md` Q1)의 **FE-4 이전 줄번호**와 지금을 맞췄다.
**모든 이동이 「더한 줄 수」와 한 칸도 안 틀린다** = 사이에 지우거나 고친 줄이 없다.

| 대상 | 조사(이전) | 지금 | 이동 |
|---|---|---|---|
| `projectModel.barGeometry` | `246` | `251` | **+5** |
| `projectModel.ganttRows` | `268` | `273` | **+5** |
| `projectModel.anchorIndex` | `306` | `311` | **+5** |
| | | | ↑ `GANTT.openLead` 블록(주석 4 + 값 1 = **5줄**)이 파일 머리에 든 것 하나뿐 |
| `ProjectGantt` `withFoldedLinks` | `58` | `63` | +5 (react import 2 + `projectId` prop 3) |
| `const width` · `positions` · `nowLeft` | `102` · `105-110` · `112` | `118` · `121-126` · `128` | +16 (`<GanttCanvas>` 호출이 prop 하나 늘며 한 줄→여러 줄로 갈림 + 시그니처 2줄) |
| `__scroll` · `__canvas` · `__axis` | `115` · `116` · `117` | `168` · `169` · `170` | +53 (scroller ref + effect 3개 + 주석 = **37줄**) |
| `__plot` · `grid left` | `128` · `129` | `184` · `185` | +56 (위 + `__axis-pad` 주석 2 + 요소 1 = **3줄**) |
| `__row` · `__name-cell` · `__bar` · 행 `top` | `187` · `188` · `222` · `140` | `243` · `244` · `278` · `196` | +56 |
| `DepLines` | `239-288` | `295-344` | +56 |

**「사라지는 선이 없다」(1루프의 핵심 · L-48)가 실제로 재어지는지도 뮤테이션으로 확인했다** —
`anchorIndex`(`projectModel.ts:319`)의 **접힌 부모로 올라가는 재귀를 끊자** 3건이 빨강이 됐다:
`projectModel.test.ts` 2건 + `ProjectPage.test.tsx:384`「가지를 접어도 선이 사라지지 않는다」.
**빈 회귀가 아니다.**

---

## 자동 스크롤 — 양방향 · `nearest` · **L-47 을 «행»에 맞춘 판단은 옳다**

- **양방향**: 간트→레일 `ProjectRail.tsx:54-58` · 레일→간트 `ProjectGantt.tsx:161-165`. ✅
- **`nearest`**: 둘 다. 「이미 보이는 것을 움직인다」는 자리 **없음**. ✅
  첫 렌더에 `taskId` 가 `null` 이라 아무것도 안 구른다(`ProjectPage.tsx:61`) —
  테스트 `ProjectPage.test.tsx:352` 의 `expect(calls.length).toBe(0)` 이 그것을 잰다.
- **L-47 의 대상이 «행»인 것은 SPEC 문면 그대로다** — L-45/L-47 은 「간트가 **그 행이** 보이는
  위치로 온다」이다. 「바가 보이게」는 SPEC 에 없다.
- **「가로가 안 튄다」는 주장도 맞다.** 행은 `left:0;right:0`(`projects.css:83`)이라 폭이 캔버스 전폭이다.
  CSSOM-View 의 `nearest` 는 **요소가 스크롤포트보다 크고 양 끝이 다 밖이면 「아무것도 안 한다」**,
  한쪽 끝이 딱 맞으면 **반대 끝이 아니라 그 끝에 맞춘다** — 두 경우 모두 `scrollLeft` 가 안 움직인다.
  캔버스가 스크롤포트보다 좁으면 애초에 스크롤이 없다. **세 갈래 다 안전**하다.
  (브라우저 규격 근거다 — jsdom 은 이것을 구현하지 않는다. §눈으로만 5번)
- **되감기 싸움 없음**: 프로젝트 전환은 `loadProject` 가 **await 뒤에** `setSelected` 하므로
  (`ProjectPage.tsx:70-77`) `projectId` 와 `tasks` 가 **같은 커밋에서** 바뀐다 → 첫 진입 effect 가
  **새 축**으로 계산한 값을 쓴다. 「낡은 축으로 되감는」 갈래는 없다.

---

## §3 「워커가 정한 넷」 — 각각의 판정

| 자리 | 판정 | 근거 |
|---|---|---|
| **첫 진입 + 프로젝트 전환** | **WARN — 빈자리를 메웠다. 어긋나지 않는다** | SPEC §2.4 · L-45 는 「첫 진입」만 말한다. **별도 프로젝트 목록 화면이 없으므로**(D-05) 셀렉터 전환이 곧 그 프로젝트의 첫 진입이다. 의존이 `[projectId]` 하나라 자료 갱신으로는 안 되감는다 — **SPEC 과 충돌 0**. 코디가 §2.4 에 한 줄 얹으면 된다 |
| **오늘 앞 여백 2일** | **WARN — 빈자리 + 단언이 안 붙든다** | SPEC 에 값이 없다. 2일이면 오늘이 고정 칸 바로 오른쪽 세 번째 칸에 선다(`scrollLeft+200` 이 곧 `offset-2` 일) — **L-45 의 「오늘이 보인다」를 만족한다.** 다만 **WARN-1**: 어떤 단언도 이 2 를 붙들지 않는다 |
| **오늘이 축 밖 → 가장 가까운 끝** | **WARN — 빈자리이나 왼쪽 갈래에서 L-45 문면과 어긋난다** | **WARN-2.** 오른쪽 밖(끝난 프로젝트)은 옳고 테스트도 있다. **왼쪽 밖(시작 전)은 `scrollLeft=0` = 기간의 첫날**이고 테스트도 없다 |
| **`block:"nearest"`(양방향)** | **PASS** | L-46「카드가 뷰포트 밖에 남지 않는다」를 **최소 이동으로** 만족하고, 「이미 보이는 것을 움직이지 않는다」는 SPEC 이 요구하지 않은 **더 엄격한** 조건이다. 어긋남 0 |
| (다섯째) **L-47 의 대상 = 행** | **PASS** | SPEC 문면 그대로. 위 §자동 스크롤 |

---

## 뮤테이션 실측 10건 — **단언이 정말 무는가**

| # | 무력화한 구현 한 줄 | 결과 |
|---|---|---|
| M1 | `projectModel.ts:35` `openLead: 2 → 0` | ⚠ **23건 전건 통과 — 안 문다**(WARN-1) |
| M1b | `openLead: 2 → 4` | ✅ L-45 빨강(`not.toBe(0)` 이 잡음) |
| M2 | `ProjectGantt.tsx:164` `inline:"nearest"` 삭제 | ✅ L-47 빨강 |
| M3 | `ProjectRail.tsx:57` `block:"nearest" → "center"` | ✅ L-46 빨강 |
| M4 | `ProjectGantt.tsx:173` 스페이서 폭 `GANTT.label → 100` | ✅ L-44 빨강 |
| M5 | `ProjectRail.tsx:56` 선택자를 `.scax-inbox-card`(첫 카드)로 | ✅ L-46 빨강 — **「어느 요소가 굴렀나」를 진짜로 본다** |
| M7 | `ProjectGantt.tsx:141` 축 밖 clamp 제거 | ✅ 「오늘이 기간 밖이면…」 빨강 |
| M6 | `ProjectPage.test.tsx:219` `getTask.mockClear()` 되돌림 | ✅ `expected 3 to be 1` — **그 단언이 살아 있다**(§8) |
| M9 | `projects.css:90` `align-self:stretch` 삭제 | ⚠ **전건 통과 — CSS 는 아무도 안 잰다**(WARN-5) |
| M10 | `projectModel.ts:319` 접힌 부모로의 재귀 차단 | ✅ **3건 빨강** — L-48 의 핵심이 빈 회귀가 아니다 |

*모든 probe 는 뒤에 백업본으로 되돌리고 `diff` 로 원상을 확인했다. `git status` 는 검수 시작 시점과 같다.*

---

## 테스트 실측 (내가 다시 쟀다)

| 무엇 | 워커 주장 | **내 실측** |
|---|---|---|
| `make frontend-test` | 70파일 · 983 · 실패 0 (1회) | **70파일 · 983건.** **9회 중 7회 전건 통과 · 2회 실패** |
| — 이 판의 실패 | 0 | **1회** — L-45 (`expected +0 to be 68`, `ProjectPage.test.tsx:334`) → **FAIL-1** |
| — 기존 실패 | 0 | **4회** — `task checklist`(2) · `task checklist`(span/null) · `adjustment and resubmission` · `product surfaces`. **전부 FE-4 밖** → WARN-4 |
| — 1루프의 `MeetingMaterials`·`ActionCenter` | 통과 | **9회 모두 통과** ✅ |
| `npx tsc --noEmit` | 에러 0 | **에러 0 (exit 0)** ✅ |
| `ProjectPage.test.tsx` 단독 | 23건 | **23건 통과**(정상 코드 5회 연속). 단, 부하 없는 단독 실행에서도 §FAIL-1 의 자리가 흔들린 적 있음 |
| `projectModel.test.ts` | 13건 | **13건 통과** ✅ |

---

## 기존 부채 (이번 판정 제외)

- 프론트 스위트가 **부하에서 여러 자리가 흔들린다**(WARN-4). 흔들리는 자리가 1루프의
  `MeetingMaterials`·`ActionCenter` 에서 `task checklist`·`adjustment`·`product surfaces` 로 **옮겨갔다.**
- `frontend/dist/` 에 13:4x 빌드 산출물이 남아 있다(gitignore 대상이라 diff 0 — 위반 아님).

---

## 눈으로만 확인되는 것 — **사용자 2차 E2E 가 볼 자리**

1. **L-42** 가로로 밀 때 이름 칸이 실제로 서는가 (sticky 는 브라우저만 안다).
2. **L-43** 고정된 칸 위로 막대·격자·오늘선·의존선이 비치지 않는가.
   ⚠ **행 위아래 모서리**를 특히 보라 — `align-self:stretch` 가 맡은 자리이고 **테스트가 못 잡는다**(M9).
3. **L-44** 머리줄 날짜 숫자가 이름 칸 위로 안 올라오는가(요소가 있다는 것까지가 테스트다).
4. **L-36 완료 바 톤** — **여기가 이번 판 유일한 «수치 미정» 자리**다.
   WARN-3 의 계산으로는 `.55` 가 **너무 연하다**(셋 중 가장 낮은 채도 · 휘도는 2.5배).
   **`.70~.72` 를 나란히 놓고 골라 달라.** 고치는 곳은 `projects.css:110` 한 곳이다.
5. **L-45·L-46·L-47 의 «느낌»** — 2일 여백이 충분한지 · `nearest` 점프가 거슬리지 않는지 ·
   **좌 레일 카드를 고를 때 간트 가로가 안 튀는지**(규격상 안 튀지만 jsdom 이 못 재는 자리다).
6. **아직 시작 안 한 프로젝트**를 열어 보라 — WARN-2 의 갈래다. 지금은 **기간 첫날**에서 열린다.

---

## 확인한 것 (PASS 근거 — 리뷰어 체크리스트)

- **envelope**: FE-4 가 만진 6파일에 kind·status 로 권한을 추론하는 코드 **0건**(권한 판단 자체가 없다).
- **호출 자리**: `src/api.ts` 밖 `fetch` **0건** — 이 판은 API 호출을 하나도 더하지 않았다.
- **재사용**: 새 컴포넌트 0개. `ds/GutterList.tsx:36` · `ds/Select.tsx:159-160` 의 `scrollIntoView` 선례와
  `WeekGrid.tsx:105` 의 첫 진입 스크롤 선례를 **그대로 따랐다**(둘 다 실재를 확인).
- **카피·스타일**: 새 한국어 문자열 0건(`labels.ts` mtime `01:06`, 이 판이 안 건드림). 임의 hex 리터럴 **0건** —
  `opacity` 수치 하나뿐이고 색은 전부 토큰이다.
- **테스트 자리**: 옆자리 `ProjectPage.test.tsx` · `projectModel.test.ts` 에 붙었다.
