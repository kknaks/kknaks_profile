# 바퀴 8-B 결과 보고 — 조직 · 관계 탐색 · 캘린더를 새 DS 로

## 상태: done

브랜치 `kknaksss/sc-meeting-redesign-screens-b` · base `3f9c3dc` · **커밋하지 않았다**(P-6).

---

## 0. 한 줄

시안이 없는 화면 셋을 **사다리 ③**(레이아웃 그대로, 토큰·부품만)으로 옮겼다. 새 CSS 한 벌
(`src/styles/screens-b.css`)이 구 `styles.css` 의 화면 전용 클래스를 다시 겨누고, 마크업이 인라인
`style` 로 들고 있던 구 토큰 **62곳을 0곳**으로 줄였다. `--graph-*` 14종은 **한 자도 건드리지 않았다.**

---

## 1. 만진 파일

| 파일 | 무엇을 |
|---|---|
| `src/styles/screens-b.css` | **신규.** 세 화면의 새 DS 규칙 한 벌 (611줄) |
| `src/styles/index.css` | **두 줄 append** (코디 지시 형식 그대로, 맨 끝) |
| `src/OrgPage.tsx` | 중복 h1 제거 · 읽기전용 배지를 `Badge` 부품으로 |
| `src/org/OrgTreePanel.tsx` | 인라인 style → 클래스 · 검색칸을 `.scax-textfield` 로 |
| `src/org/MemberListPanel.tsx` | 인라인 style → 클래스 |
| `src/org/MemberAxesPanel.tsx` | 인라인 style → 클래스 · `.btn link h30` → `Button` |
| `src/org/ChangeLogPanel.tsx` | 인라인 style → 클래스 · `.surface-card` → `.org-change-log` |
| `src/org/AxisHistoryPopover.tsx` | 인라인 style → 클래스 |
| `src/org/AccessDrawer.tsx` | 인라인 style → 클래스 |
| `src/RelationGraphPage.tsx` | 중복 h1 제거 · 검색칸/필터칩/줌단추/링크단추를 DS 부품으로 |
| `src/GraphCanvas.tsx` | **`.t-meta` 한 줄만.** `--graph-*` 는 손대지 않았다 |
| `src/CalendarPage.tsx` | 중복 h1 제거 · `.calendar-screen` 래퍼 |
| `src/OrgPage.test.tsx` | 깨진 질의 1건 재조준 (§6) |

`backend/` · `styles.css` · `overrides-transitional.css` · `App.tsx` · 공용 부품 — **한 줄도 안 건드렸다.**

---

## 2. 화면별 처리 결과

### ① 조직 — 가장 많이 바뀌었다

구 DS 시절 `sc-design-system` 바퀴가 그린 화면이라 **값이 CSS 가 아니라 마크업 인라인 `style` 에**
흩어져 있었다(6벌 합쳐 **47곳**). 구조를 바꾸지 않고 그 값들을 `screens-b.css` 의 클래스로 옮기면서
새 토큰으로 다시 적었다. DOM 요소·중첩·`aria-*`·순서는 **그대로**다.

| 이미 따라와 있던 것 | 이번에 간 것 |
|---|---|
| `Badge`·`Button`·`Empty`·`Skeleton`·`Popover`·`Select` (바퀴 3a·3b) | 3분할 패널 테두리·반경·배경 |
| `AccessDrawer` 의 `.scax-drawer` 골격 (바퀴 3b) | 패널 머리 3벌 · tree 행 · 구성원 행 · 여섯 축 행 |
| `Icon` 글리프 (바퀴 4) | 권한 카드 · 회수 이력 · 축 이력 팝오버 줄 |
| 변경 기록의 `Badge tone` 2종 | 검색칸 → `.scax-textfield` · 「더 보기」 → `Button` |

**조직도 트리 구조는 손대지 않았다** — 펼침/선택이 갈라진 chevron·이름 두 단추, 깊이별 들여쓰기,
리더 아바타 자리 전부 그대로다. 색·타입·간격만 바꿨다.

### ② 관계 탐색 — 캔버스 밖만

**`--graph-*` 14종을 건드리지 않았음을 명시한다.** `styles.css:43~57` 의 노드 8색 · `-fallback` ·
`-dim` · 선 3종 · 라벨 2종은 그대로 살아 있고, `GraphCanvas.tsx:29~36·54·105~107` 의
`getComputedStyle` 읽기 경로도 그대로다. `screens-b.css` 는 `--graph-` 라는 글자를 **재정의하지
않는다**(주석에서만 언급). 대체 팔레트를 지어내지 않았다.

캔버스 **밖**만 갔다:

| 자리 | 구 | 새 |
|---|---|---|
| 검색칸 | 맨 `<input class="graph-search">` | `.scax-textfield` + `__input` |
| 종류 고르기 | 맨 `<button class="graph-filter">` | **`Chip` 부품** (`aria-pressed` 유지) |
| 확대·축소 4단추 | 맨 `<button>` | `.scax-icon-button` |
| 상세 링크 단추 3곳 | `.btn link` | `Button variant="text"` |
| 알약·범례·힌트·상세 패널·목록 두 칸 | 구 토큰 | `--scax-*` |

> 필터 칩의 **색점만은 `--graph-node-*` 를 인라인으로 그대로 받는다.** 범례가 그림과 같은 색이어야
> 뜻이 맞기 때문이고, 새 DS 에 대신 쓸 범주형 색이 없기 때문이다.

### ③ 캘린더 — 가장 적게 바뀌었다 (그럴 수밖에 없었다)

이 화면의 본문은 **우리 `TaskCalendar`(`WorkViews.tsx`)** 이고, 그 파일은 allowed_paths 밖 ·
공용 부품(P-3)이다. 그래서 `CalendarPage.tsx` 에서 할 수 있는 일은 셋뿐이었다:

1. 중복 h1 제거 + 설명 문단을 새 머리줄로
2. `.calendar-screen` 래퍼 한 클래스 추가
3. `.calendar-*` 규칙을 **그 래퍼 안으로 가둬** 다시 겨누기

**시그니처는 건드리지 않았다** — `TaskCalendar` 의 props(`mode`·`onModeChange`·`onOpen`·`tasks`)
그대로다.

---

## 3. ⚠ 코디가 알아야 할 것 — 캘린더가 두 자리에서 다르게 보인다

`.calendar-*` 클래스는 세 곳이 함께 쓴다:

| 쓰는 곳 | 주인 | 지금 상태 |
|---|---|---|
| `CalendarPage` (내 화면) | 바퀴 8-B | **새 DS** |
| `CalendarRail` (업무 화면 우측 레일) | 바퀴 5b | 구 색 그대로 |
| `DatePicker` (`.calendar-weekdays`) | 바퀴 3b | 구 색 그대로 |

처음에는 전역으로 다시 겨눴다가, **코디 지시(「선택자를 네 화면 안으로 좁혀라 — 다른 화면이 조용히
바뀐다」)에 따라 `.calendar-screen` 안으로 되감았다.** 그 결과가 위 표다.

> **제안: 바퀴 9 에서 `.calendar-*` 를 전역 한 방으로 올려라.** 내 파일의 캘린더 절은 `.calendar-screen `
> 접두사만 떼면 그대로 전역 규칙이 된다(값은 이미 전부 `--scax-*`). 지금 나눠 둔 것은 병렬 충돌을
> 피하려는 것이지 최종형이 아니다.

---

## 4. 죽은 구 `styles.css` 구획 — **지우지 않았다. 보고만 한다** (P-1)

호출부를 `.tsx` 전수 grep 으로 세었다. 아래는 **호출부 0곳**이다.

| 줄 범위 | 무엇 | 근거 |
|---|---|---|
| **`461~468`** | `.org-grid` · `.org-chips` · `.capability-list`(+`li` · `:last-child` · `code`) | 호출부 0. 이 바퀴 **이전부터** 이미 죽어 있었다 — 조직 화면 v3 가 `.org-screen-grid` 로 갈아탔을 때 남은 v2 잔재다 |
| **`969~985`** | `.org-layout` · `.org-tree`(+`ul`) · `.org-node`(+`.selected`) · `.org-caret`(+`.placeholder`) · `.org-node-main`(+`b`) · `.member-list` · `.member-row`(+`:hover` · `.selected`) · `.member-main`(+`b`) · `.member-head` | 호출부 0. 같은 v2 잔재. ⚠ grep 주의: 내 새 클래스 `.org-tree-child` · `.org-tree-scroll` · `.org-member-row*` 가 **부분 문자열로 걸린다** — 구 `.org-tree` · `.member-row` 와는 다른 이름이다 |
| **`887~889`** | `.graph-filter` · `.graph-filter.active` · `.graph-filter.state` | 이 바퀴가 죽였다 — `Chip` 부품으로 옮겼다 |
| **`877`** | `.graph-search` | 이 바퀴가 죽였다 — `.scax-textfield` + 내 `.graph-search-field` 로 옮겼다 |
| **`890`(절반)** | `.graph-filter i` 쪽 | `.graph-overlay.legend i` 는 **살아 있다**. 앞쪽 선택자만 죽었다 |

**죽지 않은 것 — 오해 방지:**

- `.calendar-*`(385~412 · 796 · 958~961) — `TaskCalendar` 가 여전히 쓴다. **살아 있다**
- `.graph-*` 나머지(874~911 · 1233~1235) — 내 파일은 **색·타입만** 다시 겨눴고 배치(`position` ·
  `grid` · `inset` · `display`)는 구 파일이 계속 준다. **살아 있다**
- `.org-screen-grid` · `.org-panel*`(274~283) — 트랙 폭·높이·`@media` 는 구 파일이 준다. **살아 있다**
- `.page-head*`(122~128) — 내 세 화면은 뗐지만 `ProjectPage` · `DailyReportPage` ·
  `MeetingDetailPage` 가 쓴다. **살아 있다**
- `.avatar`(114~119) · `.plain-table` · `.surface-card` · `.t-item` · `.t-meta` · `.tabular` — 다른 화면들이
  쓴다. **살아 있다**

`overrides-transitional.css` 에서 이번에 죽은 규칙은 **없다**(P-2 — 읽기만 했다).

---

## 5. DS-gaps 후보 — 전수 6건

형식: 없는 것 / 어디서 몇 곳 / 구 DS 에선 무엇 / 새 DS 에서 가장 가까운 것 / 제안.
**결정은 사용자 몫이다 — 아무것도 정하지 않았다.**

### G-8B-1 · 범주형 팔레트 (= 기존 **G-06** 재확인)
- **어디서**: `GraphCanvas.tsx` 노드 8색 + `RelationGraphPage` 필터칩·범례 색점 2곳. 합 **3곳**
- **구 DS**: `--graph-node-*` 8색 + fallback/dim/선 3종/라벨, `styles.css:43~57`
- **새 DS**: **없다.** status 6색(red/green/cyan/yellow/orange/purple)은 *상태*지 *범주*가 아니고,
  8종을 구별할 수 없다. 「악센트 하나, 나머지 중립」 원칙과 정면으로 부딪힌다
- **제안**: 구 14종을 **그대로 유지**했다. 셋 중 하나를 사용자가 골라야 한다 —
  (a) 새 DS 에 범주 축을 신설, (b) 그래프만 예외 팔레트로 공인, (c) 노드 색을 버리고 모양·크기로 구별

### G-8B-2 · status 의 soft 배경이 danger 하나뿐
- **어디서**: 캘린더 업무 막대 4상태(`in_progress`·`done`·`blocked`·`cancelled`) **1곳**, 앞으로 늘어난다
- **구 DS**: `--progress-tint` · `--selected-bg` · `--danger-tint` · `--status-neutral-tint` 4벌
- **새 DS**: `--scax-color-danger-soft` **하나뿐**. positive/info/warning 에는 연한 칸이 없다
- **제안**: 없는 tint 를 지어내지 않았다. 바탕은 `fill-weak`/`accent-08`/`danger-soft` 셋으로만 말하고
  상태의 뜻은 **왼쪽 3px 선 + 글자색**이 지게 했다. status 램프에 `-soft` 4종 신설을 제안

### G-8B-3 · 글자 아바타(이니셜 원)
- **어디서**: `org/` 3벌 **12곳** + `LoginPage`·`TodayPage`·`WorkViews`·`ActionTaskCard`·
  `meetings/` 등 다른 화면 다수
- **구 DS**: `.avatar`(+`xs`~`xl` 5단), `styles.css:114~119`
- **새 DS**: `.scax-side-nav__avatar` · `.scax-person-chip__avatar` — 둘 다 **사진(`object-fit:cover`)**
  전제다. 글자를 받는 변형도, 크기 5단도 없다
- **제안**: 구 `.avatar` 를 남기고 내 세 패널 안에서만 새 토큰으로 다시 칠했다. DS 에 크기 램프를
  가진 이니셜 아바타 신설을 제안 — **바퀴 9 이전에 닫아야 한다**(구 파일이 통째로 사라진다)

### G-8B-4 · 28px 화면 제목이 램프 밖
- **어디서**: 세 화면 **3곳**(제거함) + `ProjectPage`·`DailyReportPage` 등 **잔여**
- **구 DS**: `.page-head h1 { font-size: 28px }`
- **새 DS**: 타입 램프가 `title 18px` 에서 끝난다. 28px 를 받을 이름이 없다
- **제안**: §6 대로 중복 h1 을 걷어내 이 바퀴에서는 필요가 사라졌다. 남은 화면들도 같은 처리가
  맞는지, 아니면 램프에 `page-title` 한 칸을 더할지 결정 필요

### G-8B-5 · 여러 줄 입력(textarea)
- **어디서**: `org/AccessDrawer` 의 사유 칸 **1곳**
- **구 DS**: `.field textarea`
- **새 DS**: `.scax-textfield` 는 한 줄짜리다. `.scax-composer` 가 있지만 채팅 입력 어휘(보내기 단추·
  글자 수)라 폼 필드가 아니다
- **제안**: 구 `.field` 를 남겼다. `.scax-textarea` 신설 제안

### G-8B-6 · 값을 읽는 표(semantic `<table>`)
- **어디서**: `org/ChangeLogPanel` 변경 기록 **1곳** (+`GutterList`·`FileList`·`MyWorkPage`·
  `meetings/ShareModal` 4곳이 같은 `.plain-table` 을 쓴다)
- **구 DS**: `.plain-table`
- **새 DS**: `.scax-task-table` 은 **업무 표 전용 div-grid** 다(`__row`·`__due`·`__resolved`…).
  5열 읽기 표를 담을 수 없고, 테스트도 `querySelector("table")` 로 `<table>` 을 요구한다
- **제안**: `<table>` 을 유지하고 `.org-change-log .plain-table th/td` 로 **내 표 안에서만** 다시
  겨눴다. 범용 데이터 표 부품 신설 제안

---

## 6. 검증

```
npx tsc --noEmit   → 0 에러
npx vitest run     → 43 files · 474 tests · 전부 통과 (기준선과 동일)
```

### 고친 테스트 — 1건뿐

`OrgPage.test.tsx:248` — **접근성·텍스트 질의라 멈추고 기능부터 확인했다.**

```js
// 전
const head = (await screen.findByRole("heading", { name: "조직" })).closest(".page-head")
expect(within(head).getByText("읽기 전용")).toBeTruthy()
```

- **기능은 살아 있나**: 살아 있다. 읽기 전용 배지는 그대로 그려지고 자리만 `.screens-b-lead` 로
  옮겼다. 깨진 것은 **h1 을 길잡이로 쓰던 부분**이다
- **왜 h1 을 없앴나**: 바퀴 2 가 셸 머리(`.scax-page-header > h1`)를 세운 뒤로 세 화면의 페이지
  h1 은 **셸 제목과 글자까지 똑같은 두 번째 줄**이었다(「조직」·「캘린더」·「관계 탐색」이
  `App.tsx:45~54` 의 `surfaceLabel` 과 정확히 일치). 바퀴 5a 가 업무 화면에서 한 처리(J-2)와 같다
- **어떻게 고쳤나**: 배지 단언은 그대로 두고 길잡이만 `.screens-b-lead` 로 재조준했다. 이 테스트가
  `.page-head` 로 범위를 좁혔던 이유(같은 파일 `:241` 이 **「조직 tree」 패널 안의 다른 「읽기 전용」**
  = `orgScreen.treeMeta` 를 따로 단언한다)를 그대로 지켰다

클래스 선택자로 깨진 것은 **0건**이다.

### 빈 검사가 된 곳 — 없다

「없음」 단언(`queryBy… === null`) **21건**을 전수로 훑고, 내 변경이 닿는 둘을 짚어 확인했다:

| 단언 | 위험 | 확인 |
|---|---|---|
| `OrgPage.test.tsx:383` `queryByRole("button", {name:/더 보기/})` | 그 단추를 `.btn link h30` → `Button` 으로 바꿨다 | **살아 있다.** 짝인 `:389` `getByRole("button", {name:"1건 더 보기"})` 가 통과한다 → 접근가능이름이 보존됐다 |
| `RelationGraph.test.tsx:155` `within(filters).queryByRole("combobox")` | 필터를 맨 button → `Chip` 으로 바꿨다 | **살아 있다.** 짝인 `:156` 이 `getAllByRole("button")` 으로 `["사람","팀","업무"]` 를 그대로 받아 통과한다 |

나머지 19건은 내 변경이 닿지 않는다(권한·자격·페이징 단언).

### ⚠ 기준선 자체의 문제 — `Checklist.test.tsx` 가 **플레이키**하다

브리프는 기준선을 「474 전부 통과」로 적었지만, **작업 시작 전 `3f9c3dc` 의 깨끗한 트리에서 돌린
첫 전체 실행에서 이미 1건이 깨졌다**(`Checklist.test.tsx:272`). 이후:

| 실행 | 결과 |
|---|---|
| 작업 전 전체 (트리 깨끗) | `Checklist.test.tsx:272` 실패 |
| 작업 중 전체 | `Checklist.test.tsx:353` 실패 (**다른 줄**) |
| 단독 3회 | 1실패 / 2통과 |
| 최종 전체 | 474 전부 통과 |

**같은 파일이 실행마다 다른 줄에서 깨진다 = 테스트 격리·타이밍 문제**이지 회귀가 아니다. 그 파일과
대상(`WorkModals.tsx` 체크리스트)은 **내가 한 줄도 건드리지 않았다.** 앞 테스트가 `release` 프라미스를
띄워 둔 채 끝나는 자리가 있어 전체 실행의 부하에 따라 다음 테스트로 샌다. **allowed_paths 밖이라
고치지 않았다 — 별도 티켓 제안.**

---

## 7. P-3 으로 넓혀야 했던 공용 부품 prop — **0건**

넓힌 것이 없다. 쓰려던 자리가 전부 이미 열려 있었다:

- **`Chip`** — 그래프 필터의 색점(`<i>`)을 넣어야 했는데 바퀴 3c 가 이미 `children`·`className`·
  `...rest` 를 열어 뒀다. 그대로 썼다
- **`Badge`** — 조직 읽기전용 배지에 `tone="neutral"` 만 쓰면 됐다
- **`Button`** — `variant="text"` · `size="sm"` · `aria-label` 전부 기존 API
- **`TaskCalendar`** — 시그니처 그대로. 래퍼 클래스는 `CalendarPage` 쪽에 붙였다

**넓히고 싶었지만 참은 것 1건 (보고만):**

> `TextField` 부품이 `src/` 에 아직 없다. `.scax-textfield` CSS 는 바퀴 3b 가 실어 뒀는데 그 자리를
> 쓰는 `.tsx` 가 0곳이라, 조직 검색칸·그래프 검색칸 2곳에서 **클래스를 직접 붙여 썼다**. 부품화는
> 다른 워커가 같은 파일을 만들고 있을 수 있어 손대지 않았다. 코디가 주인을 정해 주면 좋겠다.

---

## 8. BE 영향 · SPEC 불일치

**없다.** 이 바퀴는 서버 호출·envelope·권한 판단·`viewModels`·`api.ts` 를 한 줄도 바꾸지 않았다.
가짜 데이터도 넣지 않았다 — 사람 이름·파일·수치는 전부 기존 mock/서버 값 그대로다.
