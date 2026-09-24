# 프론트 현재 구조 조사 — 「프로젝트」 시안 대비

**성격**: read-only 조사. 코드·설정·테스트 **한 줄도 고치지 않았다.** 빌드·테스트·서버 **안 돌렸다.**
**워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (브랜치 `kknaksss/strong-hajin-projects`, 작업 시작 시 clean)
**경로 표기**: 코드 레포는 `frontend/` 기준 상대 경로. 시안은 `package 2/` 기준.
**근거 규율**: 아래 모든 판정에 `파일:줄` 을 달았다. API 경로·토큰 이름은 전부 코드에서 복사한 실값이다.

---

## 0. 한 줄 결론

지금 「프로젝트 화면」은 **시안과 같은 화면이 아니다.** 시안은 3레일 + 간트 + 의존선인데,
지금 것은 **본문 한 칸 안의 2컬럼 관리 화면**(프로젝트 목록 ↔ 담당자 붙이기/떼기 + 참여 이력)이다
(`src/features/project/ProjectPage.tsx:146-330` · `src/styles/screens-a.css:232`).
겹치는 것은 「프로젝트를 고른다」 하나뿐이고, 시안이 본문에 그리는 것(요약 스트립·간트·의존선)과
우 레일(업무 상자)은 **지금 화면에 대응물이 없다.**

반대로 **틀과 부품은 대부분 이미 있다.** DS 토큰은 이름까지 같고, `scax-inbox-card` 와
`.scax-gutter-list` 마크업은 업무·캘린더 레일에 이미 살아 있다. **새로 만들 것은 사실상 간트와 의존선 둘**이다.

---

## 1. 지금 있는 프로젝트 화면 (4-1)

### 1-1. 파일 전수

`frontend/src/features/project/` 에는 **파일이 둘뿐**이다.

| 파일 | 줄 수 | 무엇 |
|---|---|---|
| `src/features/project/ProjectPage.tsx` | 333 | 화면 전부 (하위 컴포넌트 분리 없음) |
| `src/features/project/ProjectPage.test.tsx` | 179 | 테스트 7개 |

viewModel 도, 전용 hook 도, 전용 CSS 파일도 없다. 스타일은 `src/styles/screens-a.css:231-260` 이 갖는다.

### 1-2. 화면 구조 — 시안 3레일과 나란히

```
[지금]                                       [시안]
AppShell(App.tsx:396-453)                    AppShell
└ SideNav (App.tsx:397-404)                  └ SideNav (activeId='project')
└ AppHeader title="프로젝트" (App.tsx:447-452) └ AppHeader title="프로젝트"   ← 같다
└ AppBody railLeft=undefined railRight=undefined  └ AppBody railLeft=380 railRight=342
   └ .scax-page-scroll (App.tsx:460)             │
      └ .project-page (ProjectPage.tsx:136)      │
         ├ .screens-b-lead 설명 한 줄 (:140-144) │  ← 시안에 없다
         └ .project-layout (:146)                │
            ├ aside.project-list (:147-189)      ├ 좌 레일: 업무 헤더 + Select + 업무 카드
            │   ・프로젝트 «목록» + [새 프로젝트]  │     (시안은 프로젝트를 «셀렉터» 로 고른다)
            └ div.project-detail (:196-328)      ├ 본문: 요약 스트립 + 간트 + 의존선
                ├ h3 프로젝트명 (:197)            └ 우 레일: 선택 «업무» 상자
                ├ 기간·설명 (:198-204)
                ├ section 현재 참여자 (:206-290)
                ├ section 참여 이력 (:292-306)
                └ section 이 프로젝트의 업무 (:308-327)
```

**결정적 차이 넷**

1. **레일이 없다.** `App.tsx:515` 는 `<ProjectPage {...pageProps} />` 만 넘기고 `pageProps`
   (`App.tsx:352`)에는 `onRegisterRails` 가 없다. 레일을 쓰는 화면은 셋뿐이다 —
   캘린더(`App.tsx:477`) · 업무(`App.tsx:488`) · 회의(`App.tsx:505`).
   레일을 안 넘기면 그 칸이 **아예 렌더되지 않는 것이 셸 규약**이다(`src/shell/AppShell.tsx:77,79`).
2. **좌 칸이 「프로젝트 목록」이다.** 시안은 좌 레일이 **업무 목록**이고 프로젝트는 헤더의 `Select` 다
   (`handoff/projects/js/projects.v1.jsx:39`). 지금은 `<ul>` 프로젝트 행 목록이다
   (`ProjectPage.tsx:175-188`), 폭은 `minmax(240px,320px)`(`screens-a.css:232`) — 시안 380px 와 다르다.
3. **선택 축이 프로젝트 하나뿐이다.** 「업무를 고른다」는 축이 없다 — 업무는 클릭도 안 되는 `<li>` 다
   (`ProjectPage.tsx:318-324`).
4. **본문이 「담당자 관리 화면」이다.** 시안 본문(요약 스트립·간트)은 **관리 기능을 하나도 안 그린다.**
   반대로 지금 화면의 핵심인 참여자 붙이기/떼기·참여 이력·새 프로젝트 만들기는 **시안 어디에도 없다.**

### 1-3. 라우팅 · 내비

- **라우터가 없다.** 화면 전환은 `App.tsx:73` 의 `useState<ProductSurface>` 다.
  프로젝트는 `surface === "project"` 한 줄(`App.tsx:515`). URL 도 딥링크도 없다 —
  **시안의 `project`·`taskId` 를 URL 에 실을 자리가 지금 없다.**
- 셸 머리 제목은 `surfaceLabel.project = "프로젝트"` (`App.tsx:53`) → `AppHeader title` (`App.tsx:451`).
  **breadcrumb 은 바퀴 6a 에서 지워졌고**(`App.tsx:449-450`) actions 는 이 화면이 등록하지 않는다.
  → **머리 한 줄만 있고 actions 없음. 시안(§1 AppHeader) 과 이미 같다.**

**내비 비교** — 시안 `nav.js` 9항목 vs 우리 `App.tsx:35-46` 9항목

| # | 시안 (`handoff/shell/js/nav.js:11-21`) | 우리 (`App.tsx:36-45`) |
|---|---|---|
| 1 | 홈 `home` | 오늘 `home` (id `today`, 라벨 「홈」) |
| 2 | 업무 `square-check` | 업무 `square-check` |
| 3 | **프로젝트 `folder`** | 캘린더 `calendar` |
| 4 | 캘린더 `calendar` | **프로젝트 `folder`** |
| 5 | 회의 `persons` | 자료함 `document` (`disabled: true`) |
| 6 | 채팅 `chat` | 회의 `persons` |
| 7 | 수신함 `inbox` | 조직 `company` |
| 8 | 진행 현황 `arrow-right` | 보고 `document` |
| 9 | 자료 `document` | 관계 탐색 `link` |

- **아이콘은 시안과 같다** (`folder` — `App.tsx:39`). **자리만 다르다**: 시안은 업무 다음·캘린더 앞,
  우리는 캘린더 다음. (`App.tsx:34` 주석이 「표시 순서는 시안에 맞추고」라 적지만 3·4번이 뒤바뀌어 있다 — 실측이 정본.)
- 시안에 없고 우리에만: 조직 · 보고 · 관계 탐색. 우리에 없고 시안에만: 채팅 · 수신함 · 진행 현황.
- 상단 `NAV_PRIMARY` 알림·설정은 양쪽 다 있다 (`nav.js:5-8` ↔ `App.tsx:420-425`, `utilityItems`).
- `visibleNavigation`(`App.tsx:345-351`) 이 보고/관계탐색을 권한으로 거른다. **프로젝트는 안 거른다 — 항상 보인다.**

### 1-4. 테스트 — 무엇을 보장하고, 다시 그리면 무엇이 깨지나

`ProjectPage.test.tsx` 의 검사 7개. **다시 그리면 7개 중 6개가 깨진다.**

| # | 줄 | 보장하는 것 | 다시 그리면 |
|---|---|---|---|
| 1 | `:80-87` | 화면이 「프로젝트」 제목을 또 그리지 않는다 (`.page-head` 없음, `h3` 로 프로젝트명) | **부분 생존** — 「제목 중복 금지」 의도는 시안과 같다. 단 `h3` selector(`:82`)와 `.screens-b-lead` 설명문(`:86`)은 깨진다 (시안에 설명 줄이 없다) |
| 2 | `:89-105` | `aria-label="현재 참여자"` · `aria-label="이 프로젝트의 업무"` 영역, 「업무 2건 / 완료 1건」 문자열, `li[data-task-id].child` 들여쓰기 | **전부 깨진다** — 두 영역 다 시안에 없다 |
| 3 | `:107-121` | `may_manage` 로 「참여 종료」·「붙일 구성원」을 감춘다 | **전부 깨진다** — 관리 UI 자체가 시안에 없다 |
| 4 | `:123-127` | 안 붙은 사람에게 「담당자에게만 보입니다」를 말한다 | **깨진다** (문구 자리가 사라진다) |
| 5 | `:129-137` | 담당자 붙이면 `assignToProject("p-1",{member_id,kind})` 호출 | **전부 깨진다** |
| 6 | `:139-157` | 현재 참여자/참여 이력 분리 + 사유로 참여 종료 | **전부 깨진다** |
| 7 | `:159-178` | 프로젝트 전환 시 열린 「참여 종료 사유」 입력을 닫는다 (`.project-row-name` 클릭) | **깨진다** — `.project-row-name` 이 `Select` 로 바뀐다 |

- mock 하는 api 함수는 8개뿐(`:4-13`): `assignToProject` `createProject` `getMemberDirectory`
  `getOrganizationTree` `getProject` `getProjectParticipationHistory` `listProjects` `releaseFromProject`.
  **시안이 요구하는 업무 상세 조회(`getTask`)·체크리스트·선행업무는 이 테스트가 한 번도 부르지 않는다.**
- `ProjectPage` 를 겨누는 테스트는 이 파일 **하나뿐**이다 — `src/App.test.tsx` 에 「프로젝트」 문자열 **0건**.
- `screens-a.css:5-8` 이 이 테스트가 겨누는 `.project-row-name`·`li.child` 를 **일부러 살려 둔다**고 적어 둔다.

---

## 2. 부품 재고 — 시안 부품 ↔ 우리 `src/ds` (4-2)

판정: **있다** = 같은 이름·같은 역할로 쓸 수 있다 / **다르다** = 있지만 API·마크업·값이 어긋난다 / **없다** = 대응물 0.

| 시안 부품 | 판정 | 근거 (`파일:줄`) |
|---|---|---|
| `AppShell` | **있다** | `src/shell/AppShell.tsx:37-44` — `.scax-app-shell` + `.scax-app-main`, 시안 `scax-ui.jsx:207-213` 과 마크업 동일 |
| `SideNav` | **있다** | `src/shell/SideNav.tsx:70-195`. 시안(`scax-ui.jsx:217-262`)과 다른 점 넷은 `SideNav.tsx:12-21` 이 스스로 적는다 (`onSelect` 추가 · `label` prop · `onUserClick` · 아바타 조건부). 항목 목록은 `nav.js` 대신 `App.tsx:35-46` 이 prop 으로 준다 |
| `AppHeader` | **있다** | `src/shell/AppShell.tsx:46-72`. `title`·`actions` 그대로. `breadcrumb` 은 우리가 더 갖고 있으나 프로젝트는 안 쓴다(`App.tsx:449-450`) |
| `AppBody`(3레일) | **있다** | `src/shell/AppShell.tsx:74-82` — `railLeft`/`railRight` 슬롯. 폭은 `src/styles/shell.css:137-138` |
| `GutterList`(헤더+스크롤 바디) | **다르다** ⚠ | **이름이 같은 다른 부품이다.** 우리 `src/ds/GutterList.tsx:20-58` 은 「왼쪽 고정폭 메타 칸 + 본문」 표(`.gutter-list`/`.gutter-row`)이고 **소비처 0건**(`grep <GutterList` → 0). 시안의 것(`scax-ui.jsx:160-174`, `.scax-gutter-list`)은 **React 부품 없이 마크업으로만** 두 곳에 손으로 쓰여 있다 — `src/shell/InboxRail.tsx:103-114` · `src/features/calendar/ScheduleRail.tsx:81-108`. CSS 는 있다: `src/styles/components.css:105-108` |
| `scax-inbox-card` | **있다** (선택 상태만 **없다**) | CSS `src/styles/components.css:111-121`. 쓰는 곳 둘: `src/shell/InboxRail.tsx:59-71` · `src/features/calendar/ScheduleCard.tsx:42-99`. **`ScheduleCard` 가 시안 `ProjectTaskCard`(`projects.v1.jsx:8-28`)와 거의 같다** — 배지 → 제목 → `meta-who` + `meta-sep` 반복. ⚠ `.scax-inbox-card--selected` 는 우리 코드에 **0건**(`grep` 결과), 시안은 `handoff/projects/css/projects.css:6-9` 에서 hover/focus/selected 넷을 더한다 |
| `Select` | **다르다** | `src/ds/Select.tsx:338-430` 존재. 기본 트리거는 폼 필드꼴 `.select-trigger`(`Select.tsx:407` · `components.css:578`)이고, 시안 레일 헤더의 **알약꼴** `.scax-select__trigger` 는 **CSS 만 있다**(`components.css:44-49`). 다만 `trigger` prop 으로 갈아끼우는 길이 열려 있고 **선례가 이미 있다** — `src/features/work/MyWorkPage.tsx:1410`. 또 시안 `Select`(`scax-ui.jsx:74-108`)는 `ariaLabel`·`options`·`value`·`onChange` 넷뿐인데 우리 것은 `label`·`labels`(SelectLabels 6종)·`emptyActionLabel` 을 **필수**로 받는다(`Select.tsx:353,382,384`) |
| `Badge`(tone) | **있다** | `src/ds/Badge.tsx:26-44`. 톤 6종 `Badge.tsx:24` = accent·neutral·danger·positive·info·outline. CSS `components.css:37-40,216,421`. **시안 5종 tone 을 전부 덮는다** (§4 참조) |
| `Badge variant="count"` | **있다** | `src/ds/Badge.tsx:34,38` + CSS `components.css:41`. 쓰는 곳 둘: `InboxRail.tsx:108` · `ScheduleRail.tsx:86` — **시안 좌 레일 헤더와 같은 쓰임** |
| `Empty` | **있다** (크기만 다르다) | `src/ds/Empty.tsx:39-82`. `icon` prop 있음(`Empty.tsx:53`), `square-check` 글리프 있음(`src/ds/icons/glyphs.tsx:289`). ⚠ 글리프를 **20px 로 못박았다**(`Empty.tsx:70`) — 시안은 24 (`scax-ui.jsx:179`). props 이름도 다르다: 우리 `description`, 시안 `desc` |
| `Icon` `square-check` | **있다** | `src/ds/icons/glyphs.tsx:289` |
| `Icon` `chevron-down` | **있다** | `glyphs.tsx:163` |
| `Icon` `chevron-right` | **있다** | `glyphs.tsx:164` |
| `Icon` `arrow-up` | **있다** | `glyphs.tsx:333` (16그리드) |
| `Icon` `arrow-down` | **있다** | `glyphs.tsx:332` (16그리드) |
| `Icon` `check` | **있다** | `glyphs.tsx:162` |
| `Icon` `folder` | **있다** | `glyphs.tsx:341` (16그리드) |
| `Icon` 크기 12/14/24 | **있다** | `src/ds/icons/Icon.tsx:21` — `12|14|16|20|24` 전부 받는다. 24 쓰는 선례 `InboxRail.tsx:106` · `ScheduleRail.tsx:84` |
| 진행률 미터(track+fill) | **다르다** | `src/ds/ProgressBar.tsx:5-41` 존재하나 **API 가 `done`/`total` 이고 내부에서 %를 계산한다**(`ProgressBar.tsx:18`) — 시안은 `percent` 를 직접 받는다(`projects.v1.jsx:67,190`). 마크업도 `.progress-track`/`.progress-fill`(`ProgressBar.tsx:35,38`)이고 높이 6px 규격은 주석(`ProgressBar.tsx:2`)에만 있다. 시안은 `.scax-pj-summary__track/__fill` · `.scax-pj-side__track/__fill`(`projects.css:23-24,73-74`)로 **화면 전용 클래스**다. 소비처는 **한 곳뿐** — `src/features/work/WorkModals.tsx:1590` |
| **간트**(축·격자·행·바·twisty) | **없다** | `grep -rin "gantt" src/` → **0건**. 날짜 축 위에 막대를 그리는 화면이 저장소에 없다 (캘린더는 월/주 격자다 — `src/features/calendar/MonthGrid.tsx`·`WeekGrid.tsx`) |
| **의존선 SVG 오버레이** | **없다** | `pointer-events` 를 쓰는 SVG 오버레이 **0건**. 노드-엣지를 그리는 유일한 자리는 sigma/graphology 캔버스(`src/features/graph/GraphCanvas.tsx`)이고 **SVG 가 아니다** |

### 2-1. DS 토큰 — **시안이 쓰는 이름이 우리 코드에 전부 있다**

레일 폭 (시안 §1):

| 토큰 | 우리 정의 | 값 |
|---|---|---|
| `--scax-rail-left-width` | `src/styles/scax.css:119` → `var(--ax-inbox-w)` | `src/styles/product.css:79` = **380px** ✅ |
| `--scax-rail-right-width` | `src/styles/scax.css:120` → `var(--ax-calendar-w)` | `src/styles/product.css:80` = **342px** ✅ |
| 레일 테두리·그림자 | `src/styles/shell.css:137-138` — left `border-right`+`shadow-card`, right `border-left` | 시안 §1 과 동일 |

시안 `projects.css` 가 참조하는 토큰을 전수 확인했다 — **없는 것 0개**:

| 토큰 | 정의 |
|---|---|
| `--scax-color-accent` / `-05` / `-08` / `-20` | `scax.css:6,9,10,11` |
| `--scax-color-danger` / `-soft` | `scax.css:44,45` |
| `--scax-color-positive` | `scax.css:46` |
| `--scax-color-ink` / `-strong` / `-neutral` / `-assistive` / `-inverse` | `scax.css:17,16,18,20,22` |
| `--scax-color-line` / `-weak` / `-strong` | `scax.css:37,36,38` |
| `--scax-color-surface` · `--scax-color-fill-weak` | `scax.css:28,39` |
| `--scax-space-050/100/150/200/250/300/400/500/600` | `scax.css:51,52,53,54,55,56,57,58,59` |
| `--scax-radius-xs/sm/md/lg/xl/2xl/pill` | `scax.css:64,65,66,67,68,69,71` |
| `--scax-text-caption1-size` · `-caption2-size` · `-label1-size` · `-label2-size` | `scax.css:83,80,89,86` |
| `--scax-fw-regular/semibold/bold` | `scax.css:76,78,79` |
| `--scax-focus-ring` | `scax.css:128` (= `0 0 0 3px var(--scax-color-accent-20)`) |
| `--scax-shadow-card` · `--scax-control-height-sm`(32px) · `--scax-duration-fast`(120ms) | `scax.css:103,122,129` |

**`.design-sync/` 와 `src/ds` 중 정본은 `src/ds` + `src/styles` 다.**
- 사용자 결정이 문서에 박혀 있다: `.design-sync/NOTES.md:43-45` — 「지금은 정본이 우리 꺼야, 코드 기준」.
  Figma 정적 렌더러 199종과 `tokens/` 7벌을 **지우고 우리 35종으로 교체했다**고 적는다.
- `.design-sync/screens/_ds_bundle.css` 는 **우리 CSS 를 펼쳐 올린 산출물**이다 —
  `NOTES.md` 의 `flatten-css.mjs` 절이 「빌드 직전에 `src/styles/index.css` 를 한 벌로 펼친다」고 적고,
  실제로 `_ds_bundle.css:711-712,847-848,1025-1026` 이 `product.css:79-80`·`scax.css:119-120`·`shell.css:137-138`
  과 **같은 줄**이다. 즉 `.design-sync` 는 **거울이지 원본이 아니다.**
- 부품 ↔ 소스 매핑은 `.design-sync/config.json` 의 `componentSrcMap` 이 갖는다 (35종 전부 `src/ds/*` 를 가리킨다).

### 2-2. 우리 쪽 스타일 작성 방식 — 시안 CSS 를 그대로 옮길 수 있는가

- **CSS-in-JS 없음 · 유틸리티 클래스 없음 · Tailwind 없음.** `.design-sync/conventions.md` 머리가 명시한다.
- 구조: `src/styles/index.css` 한 장이 14개 파일을 `@import` 순서로 묶는다(`index.css:16-40`).
  토큰 층 = `fig-tokens.css` → `typography.css` → `product.css`(`--ax-*`) → `scax.css`(`--scax-*` 별칭) ,
  그 위에 `shell.css` · `components.css` · 화면별 `screens-a.css`/`screens-b.css`/`calendar.css`/`meetings.css` …
- **화면 전용 CSS 파일을 새로 두는 선례가 이미 있다** — `src/styles/calendar.css` · `meetings.css` · `workspace.css`.
- 컴포넌트에 임의 hex 를 두지 않는다(role rules). 실제로 `screens-a.css:18-46` 이 구 토큰 → `--scax-*` 대응표를 들고 있다.
- **결론**: 시안 `handoff/projects/css/projects.css`(13,510바이트, `.scax-pj-*` 전용 클래스)는
  **구조적으로 그대로 옮길 수 있다** — 참조하는 토큰이 전부 같은 이름으로 존재하고(§2-1),
  `index.css` 에 화면 CSS 한 장을 더 `@import` 하는 것이 기존 방식이다.
  ⚠ 단 `projects.css:2` 의 `.scax-page-header__title-row` 는 **셸 규칙**이라 화면 CSS 가 아니다 —
  우리 `AppHeader`(`AppShell.tsx:46-72`)에는 `titleEnd` 슬롯이 없다(시안 `scax-ui.jsx:264,276-281` 에는 있다).

---

## 3. 데이터가 프론트까지 어떻게 오나 (4-3)

### 3-1. 호출 전수 — `src/lib/api.ts` (총 144개 export 중 업무·프로젝트 관련)

컴포넌트에서 직접 `fetch` 하지 않는다 — 전부 `api.ts:126-143` 의 `request<T>()` 를 거친다.

**프로젝트 (6개)**

| 줄 | 함수 | 경로 |
|---|---|---|
| `api.ts:793` | `listProjects` | `GET /api/projects` |
| `api.ts:797` | `getProject` | `GET /api/projects/${projectId}` |
| `api.ts:801` | `getProjectParticipationHistory` | `GET /api/projects/${projectId}/participation-history` |
| `api.ts:805` | `createProject` | `POST /api/projects` |
| `api.ts:814` | `assignToProject` | `POST /api/projects/${projectId}/members` |
| `api.ts:818` | `releaseFromProject` | `DELETE /api/projects/${projectId}/members/${memberId}` |

**업무 — `/api/tasks*` (30개)**

| 줄 | 함수 | 경로 |
|---|---|---|
| `api.ts:154` | `getTasks` | `GET /api/tasks` · `GET /api/tasks?include_closed=true` |
| `api.ts:158` | `getTask` | `GET /api/tasks/${taskId}` |
| `api.ts:163` | `submitTaskCompletion` | `POST /api/tasks/${taskId}/completion-report` |
| `api.ts:174` | `addTaskReference` | `POST /api/tasks/${taskId}/references` |
| `api.ts:182` | `releaseTaskReference` | `DELETE /api/tasks/${taskId}/references/${referenceId}` |
| `api.ts:200` | `getTaskHistory` | `GET /api/tasks/${taskId}/history` |
| `api.ts:204` | `getTaskHistoryDiff` | `GET /api/tasks/${taskId}/history/diff?from=&to=` |
| `api.ts:219` | `createDirectTask` | `POST /api/tasks` |
| `api.ts:246` | `updateTask` | `PATCH /api/tasks/${taskId}` |
| `api.ts:269` | `getTaskMaterials` | `GET /api/tasks/${taskId}/materials` |
| `api.ts:273` | `uploadTaskMaterial` | `POST /api/tasks/${taskId}/materials` |
| `api.ts:285` | `taskMaterialContentUrl` | `/api/tasks/${taskId}/materials/${materialId}/content` |
| `api.ts:290` | `attachTaskMaterialLink` | `POST /api/tasks/${taskId}/materials/links` |
| `api.ts:302` | `attachTaskMaterialReference` | `POST /api/tasks/${taskId}/materials/references` |
| `api.ts:314` | `reassignTask` | `POST /api/tasks/${taskId}/reassign` |
| `api.ts:332` | `getTaskAssignments` | `GET /api/tasks/${taskId}/assignments` |
| `api.ts:337` | `getTaskChildren` | `GET /api/tasks/${taskId}/children` |
| `api.ts:347` | `reopenTask` | `POST /api/tasks/${taskId}/reopen` |
| `api.ts:355` | `getTaskProposals` | `GET /api/tasks/${taskId}/proposals` |
| `api.ts:364` | `createTaskProposal` | `POST /api/tasks/${taskId}/proposals` |
| `api.ts:376` | `respondTaskProposal` | `POST /api/tasks/${taskId}/proposals/${proposalId}/respond` |
| `api.ts:389` | `withdrawTaskProposal` | `POST /api/tasks/${taskId}/proposals/${proposalId}/withdraw` |
| `api.ts:396` | `detachTaskMaterial` | `POST /api/tasks/${taskId}/material-bindings/${bindingId}/detach` |
| `api.ts:400` | `transitionDirectTask` | `POST /api/tasks/${taskId}/${action}` (start·block·resume·complete·cancel) |
| `api.ts:976` | `assignTask` | `POST /api/tasks/assign` |
| `api.ts:1115` | `addChecklistItem` | `POST /api/tasks/${taskId}/checklist` |
| `api.ts:1119` | `updateChecklistItem` | `PATCH /api/tasks/${taskId}/checklist/${itemId}` |
| `api.ts:1128` | `removeChecklistItem` | `DELETE /api/tasks/${taskId}/checklist/${itemId}` |
| `api.ts:1134` | `reorderChecklist` | `POST /api/tasks/${taskId}/checklist/order` |
| `api.ts:1431` | `createTaskSchedule` | `POST /api/tasks/${taskId}/schedules` |

**업무 — 그 밖 (7개)**

| 줄 | 함수 | 경로 |
|---|---|---|
| `api.ts:150` | `getMyWork` | `GET /api/my-work` |
| `api.ts:971` | `getTaskAssignmentCandidates` | `GET /api/task-assignment-candidates` |
| `api.ts:989` | `getSentTaskAssignments` | `GET /api/task-assignments/sent` |
| `api.ts:993` | `acceptTaskAssignment` | `POST /api/task-assignments/${assignmentId}/accept` |
| `api.ts:997` | `declineTaskAssignment` | `POST /api/task-assignments/${assignmentId}/decline` |
| `api.ts:1447` | `updateTaskSchedule` | `PATCH /api/task-schedules/${scheduleId}` |
| `api.ts:1419` | `getCalendar` | `GET /api/calendar?from=&to=` |

**업무 요청 (23개)** — 시안 프로젝트 화면은 직접 쓰지 않지만 좌 레일 카드의 「분류」(D-8)가 여기에 걸린다:
`api.ts:474,479,483,491,504,559,564,581,592,596,609,613,625,641,655,944,948,956,1015,1030,1035,1048,1052`
(`getWorkRequests` `getWorkRequestInbox` `getWorkRequest` `getWorkRequestAssigneeCandidates` `createWorkRequest`
`getWorkRequestMaterials` `uploadWorkRequestMaterial` `attachWorkRequestMaterialLink` `workRequestMaterialContentUrl`
`detachWorkRequestMaterial` `markWorkRequestRead` `decideWorkRequest` `negotiateWorkRequest` `withdrawWorkRequest`
`hideWorkRequestListEntry` `getWorkRequestTimeline` `addWorkRequestComment` `resubmitWorkRequest`
`getWorkRequestCcCandidates` `uploadCommentAttachment` `amendWorkRequest` `uploadRequestEvidence` `requestAttachmentUrl`)

**AX 판단 (8개)**: `api.ts:487,696,1060,1064,1068,1086,1096,1111`
**관계 그래프 (3개)**: `api.ts:186,190,196`

> ⚠ **프로젝트 화면이 지금 쓰는 것은 위 중 7개뿐**이다 — `listProjects` · `getProject` ·
> `getProjectParticipationHistory` · `createProject` · `assignToProject` · `releaseFromProject` ·
> `getMemberDirectory`(`api.ts:146`). `ProjectPage.tsx:3-11` 의 import 가 그 전부다.
> **업무 상세(`getTask`)·체크리스트·선행업무·하위업무를 한 번도 부르지 않는다.**

### 3-2. envelope 모양과 권한 판단이 일어나는 자리

**두 갈래다. 프로젝트 화면은 그중 하나만 쓴다.**

1. **AX 판단 envelope** — `src/lib/viewModels.ts:691-710` `ActionItemEnvelope`:
   `allowed_commands`(`:698`) · `waiting_on`(`:701`) · `preview`(`:697`) · `expected_version`(`:703`),
   `requires_reason` 는 `ActionCommand`(`viewModels.ts:776`)에 있다.
   읽는 자리는 `src/features/action/*` 다. **프로젝트/업무 목록 화면은 이 봉투를 안 쓴다.**
2. **불린 한 개** — 프로젝트는 `ProjectDetail.may_manage`(`viewModels.ts:93`) 하나가 권한 전부다.
   화면은 그 값을 그대로 따른다 — `ProjectPage.tsx:216`(참여 종료 단추) · `:269`(붙이기 칸).
   「담당자에게만 업무가 보인다」는 **서버가 `tasks` 배열을 비워 보내는 것**이고, 화면은
   `iAmIn`(`ProjectPage.tsx:86`, 내 id 가 members 에 있나)으로 **안내 문구만** 고른다(`:312-316`).
3. **화면 수준 권한**은 세션 capabilities — `App.tsx:71,343` `has(capability)`.
   내비 필터(`App.tsx:345-351`)와 화면 prop(`App.tsx:356-357`)이 쓴다. **프로젝트는 여기서 안 걸린다.**
4. 업무 쪽 권한은 `derived`(`viewModels.ts:141-158`)를 읽는다 — `assignment`·`approval`·`proposal`·
   `blocking_children`·`overdue_days`. 판정 함수는 `src/features/work/workRows.ts:20,24,50,62,77`.

### 3-3. 변환 계층 — 화면이 쓰는 꼴로 바꾸는 자리

| 자리 | 무엇 | 줄 |
|---|---|---|
| `src/lib/viewModels.ts` | **타입만**이다. 함수가 아니다 (1,339줄 전부 `export type`) | — |
| `src/features/work/workRows.ts` | 업무 표 3벌의 «행» + 칩 조건. 순수 함수 | `workRows.ts:1-16` 머리 주석 |
| `src/features/calendar/calendarModel.ts` | 캘린더 격자/레일 카드(`RailCard`) 변환 | `ScheduleCard.tsx:5` 가 `RailCard` 를 받는다 |
| `src/features/work/requestInbox.ts` | 수신함 항목 변환 | `InboxRail.tsx:3` |
| `src/lib/labels.ts` | 한국어 카피·라벨·톤 표 (1,027줄) | — |
| **`src/features/project/`** | **변환 계층이 없다.** `ProjectPage.tsx` 가 서버 응답을 그대로 JSX 에 꽂는다 | `ProjectPage.tsx:132-133` (`done`/`total` 두 줄이 유일한 계산) |

### 3-4. D-1 ~ D-9 가 프론트까지 실제로 내려오는가

기준: **지금 프로젝트 화면이 받는 것**(`ProjectDetail`) / **업무 상세를 부르면 받을 수 있는 것**(`DirectTask`).

| # | 화면이 요구하는 사실 | `ProjectDetail.tasks` (`viewModels.ts:96-103`) | `DirectTask` (`viewModels.ts:186-255`) | 판정 |
|---|---|---|---|---|
| D-1 | 업무 ↔ 프로젝트 | — (프로젝트를 키로 조회하므로 암묵) | `project_id?: string \| null` (`:209`) | **온다** |
| D-2 | 시작일·종료일 | `start_date` · `due_date` (`:100-101`) | `start_date?` `due_date?` (`:194-195`) | **온다** (날짜 문자열. 시안의 「9월 N일」 정수 축은 시안 편의) |
| D-3 | 진행률 % | **없다** | **없다** — `grep progress` 결과 `child_progress`(`:247`) · `checklist_progress`(`:248`) 두 **건수** 뿐 | **안 온다** ⚠ |
| D-4 | 선행 → 후행 | **없다** | `preceding_task_ids?: string[]`(`:222`) · `predecessors?: [{task_id,title,state}]`(`:230`, **상세 조회에만**) | **부분** — 선행만. **후행(역방향)은 없다** ⚠ |
| D-5 | 상위–하위 | `parent_task_id`(`:102`) — 계층은 온다 | `parent?`(`:243`) · `children?: TaskChild[]`(`:245`) · `child_progress`(`:247`) | **온다** (시안은 1단계, 우리 타입은 깊이 제한 없음) |
| D-6 | 체크리스트(텍스트 + done) | **없다** | `checklist?: ChecklistItem[]`(`:237`, **상세 조회에만**) · `checklist_progress`(`:248`). 항목 타입 `viewModels.ts:375-390` (`text` `done` `position`) | **온다** — 단 업무마다 `getTask` 를 따로 불러야 한다 |
| D-7 | 상태 5종 | `state: string`(`:99` — **string 으로 느슨하다**) | `state: TaskState`(`:189`) = `open`·`in_progress`·`blocked`·`done`·`cancelled` (`:121`) | **온다** (§4 매핑 참조) |
| D-8 | 담당자 · 요청자 · 분류 | **없다** — 담당자도 없다 ⚠ | 담당 `assignee?`(`:207`)·`assignment?`(`:200`), 요청 `origin?`(`:203`)·`lineage?`(`:201`), 분류는 `isRequestTask()`(`workRows.ts:30`) 로 파생 | **부분** — 프로젝트 조회에는 **하나도 없고**, 업무 조회에는 있다 |
| D-9 | 프로젝트 목록(선택지) | `Project`(`viewModels.ts:58-69`) + `listProjects`(`api.ts:793`) | — | **온다** — 이미 Select 옵션으로 쓰는 선례가 있다: `WorkModals.tsx:4538` |

**요약**: 시안이 요구하는 9개 중 **D-3(진행률 %) 이 프론트 타입 어디에도 없다.** D-4 는 선행만 있고 후행이 없다.
D-6·D-8 은 있지만 **업무 목록 응답이 아니라 업무 «상세» 응답**에만 실린다 — 시안처럼 한 프로젝트의
모든 업무를 한 화면에 깔려면 **지금 계약으로는 N번 호출이 된다.** (백엔드 판단은 backend 워커 담당.)

### 3-5. 상태 표시(배지 라벨·색)는 어디서 결정되나

**상수표다. 서버가 라벨·색을 주지 않는다.**

| 무엇 | 자리 |
|---|---|
| 라벨 | `src/lib/labels.ts:3-9` `taskStateLabel` — open「시작 전」· in_progress「진행 중」· blocked「막힘」· done「완료」· cancelled「취소」 |
| 톤 | `src/lib/labels.ts:20-26` `taskStateTone` — open `neutral` · in_progress `accent` · blocked `danger` · done `positive` · cancelled `neutral` |
| 쓰는 곳 | `src/features/calendar/ScheduleCard.tsx:66` (`<Badge tone={taskStateTone[card.state]}>{taskStateLabel[card.state]}</Badge>`) |
| 프로젝트 화면 | `ProjectPage.tsx:321` — **배지가 아니라 `<span className="t-meta">` 맨 글자**로 상태를 낸다 |
| 파생 표시 | 상태와 **다른 표**다 — `labels.ts:29~` `derivedAssignmentLabel`·`derivedApprovalLabel`. 이유는 `labels.ts:28-32` 주석 |

**시안 5종 tone 매핑** (`handoff/projects/js/data.js:20-26` `PROJECT_STATUS_BADGE`) 과 대조:

| 시안 status | 시안 label / tone | 우리 `TaskState` | 우리 label / tone | 일치 |
|---|---|---|---|---|
| `progress` | 진행 중 / `accent` | `in_progress` | 진행 중 / `accent` | 라벨·톤 ✅ |
| `not-started` | 대기 / `neutral` | `open` | **시작 전** / `neutral` | 톤 ✅ · **라벨 다름** |
| `blocked` | 지연 / `danger` | `blocked` | **막힘** / `danger` | 톤 ✅ · **라벨 다름** |
| `done` | 완료 / `positive` | `done` | 완료 / `positive` | ✅ |
| `cancelled` | 취소 / `neutral` | `cancelled` | 취소 / `neutral` | ✅ |

→ **톤 5종은 한 칸도 안 틀린다.** 라벨 둘(`open`·`blocked`)만 말이 다르다.
⚠ 시안 간트 바 색도 같은 4상태를 쓴다(`projects.css:52-59`) — `progress`/`blocked`/`done`/`not-started`.
⚠ `cancelled` 는 **간트 바 색이 정의돼 있지 않다** (시안 CSS 에 `--cancelled` 없음).

---

## 4. 다시 그릴 때의 충돌 지점 (4-4)

### 4-1. 모달·드로어 — **프로젝트 화면은 이미 깨끗하다**

- `grep "Modal|Drawer" src/features/project/ProjectPage.tsx` → **0건**.
  지금 프로젝트 화면은 모달도 드로어도 안 쓴다. 참여 종료 사유 입력도 **인라인**이다(`ProjectPage.tsx:239-268`).
- **문제는 업무 쪽이다.** 시안 좌 레일 카드·우 레일 관계 줄·하위 업무 카드는 **누르면 그 업무로 이동**인데
  (`projects.v1.jsx:219,258`), 우리 업무 화면에서 업무를 여는 유일한 길은 **드로어**다:
  `src/features/work/MyWorkPage.tsx:1212` `TaskDetailDrawer` · `:1236` `ActionItemDrawer` ·
  `:1252` `WorkRequestDetailDrawer` · `:1285` `ConfirmModal` · `:1302` `CreateWorkModal` · `:1418` `CompletionReportModal`.
  캘린더 레일도 같은 길이다 — `ScheduleCard.tsx:49` `onOpen`.
  → **시안의 「선택」과 우리의 「연다」가 같은 제스처(카드 클릭)에 걸려 있다.** 프로젝트 화면이
  카드를 「선택」으로 쓰면 업무 화면과 **같은 부품이 다른 뜻**을 갖게 된다.

### 4-2. 상호작용 축 — 지금 상태 관리가 더 들고 있는 것

시안은 축이 둘이다: `project`(`projects.v1.jsx:280`) + `taskId`(`:281`). 그 밖은 간트 `open`(`:109`)과 내비 `collapsed`(`:279`).

`ProjectPage` 의 `useState` 는 **열 개**다 (`ProjectPage.tsx:28-41`):

| 상태 | 줄 | 시안에 대응 있나 |
|---|---|---|
| `projects` | `:28` | (셀렉터 options) — 대응 |
| `selected: ProjectDetail` | `:29` | `project` — 대응 (단 시안은 id 만, 우리는 detail 전체) |
| `history` | `:30` | **없다** (참여 이력이 시안에 없다) |
| `directory` | `:31` | **없다** |
| `opening` | `:32` | **없다** (새 프로젝트 열기 토글) |
| `name` | `:34` | **없다** |
| `joining` | `:34` | **없다** |
| `releasing` | `:35-39` | **없다** |
| `releaseReason` | `:40` | **없다** |
| `busy` | `:41` | **없다** |
| — | — | **`taskId` 가 없다** ⚠ 시안의 핵심 축이 지금 화면에 통째로 없다 |

또 셸 쪽에 축이 둘 더 있다: `navCollapsed`(`App.tsx:403` 의 토글) 와 `surface`(`App.tsx:73`).
`surfaceRails`(`App.tsx:130`) · `surfaceActions`(`:127`) · `surfaceRefresh`(`:135`) 는
**화면이 셸에 등록하는 seam** 이다 — 레일을 쓰려면 프로젝트 화면이 여기 붙어야 한다
(선례 `MyWorkPage.tsx:941-972` · `CalendarPage.tsx:460-477`).

### 4-3. 다시 그리면 같이 흔들리는 화면

**A. 프로젝트 화면만의 것 — 지워도 아무도 안 흔들린다**

| 자산 | 줄 | 다른 소비처 |
|---|---|---|
| `.project-page` `.project-layout` `.project-list` `.project-list-head` `.project-new` `.project-row` `.project-row-name` `.project-detail` `.project-members` `.project-tasks` `.project-join` | `src/styles/screens-a.css:231-260` | **0** (`grep` 확인) |
| `.project-layout` 반응형 | `src/styles/components.css:692-693` | `.dashboard-columns` · `.report-grid` 와 **같은 규칙에 묶여 있다** ⚠ — 이 줄만 손대면 홈·보고가 같이 움직인다 |

**B. 공유 자산 — 건드리면 다른 화면이 흔들린다**

| 자산 | 프로젝트가 쓰는 곳 | 같이 쓰는 화면 |
|---|---|---|
| `.screens-b-lead` | `ProjectPage.tsx:140-144` | **조직**(`OrgPage.tsx:352`) · **관계 탐색**(`RelationGraphPage.tsx:171`) · **보고**(`DailyReportPage.tsx:291`). 검사도 걸려 있다 — `OrgPage.test.tsx:249-251` |
| `ds/Select` | `ProjectPage.tsx:271` | `AccessDrawer.tsx:100,113` · `WorkModals.tsx:1500,1931,4327,4401,4496,4528` · `MyWorkPage.tsx:1383` · `MemoComposer.tsx:93` · `BookingModal.tsx:339` — **총 12자리** |
| `ds/Badge` | `ProjectPage.tsx:213,297` | 저장소 전역 |
| `ds/Button` | `ProjectPage.tsx:150,169,217,256,259,282,285` | 저장소 전역 |
| `lib/labels` (`formatDate` `personName` `taskStateLabel` `selectLabel` `emptyActionLabel`) | `ProjectPage.tsx:14` | 전역 |
| `api.listProjects` | `ProjectPage.tsx:57,76` | **`WorkModals.tsx:3672`** — 업무 만들기의 프로젝트 셀렉터(`WorkModals.tsx:4538`)가 같은 호출을 쓴다 |

**C. 새로 손대면 흔들릴 위험이 있는 공유 자산**

| 자산 | 위험 |
|---|---|
| `.scax-inbox-card` (`components.css:111-121`) | 시안이 hover/focus/selected 4규칙을 더한다(`projects.css:6-9`). **`[role="button"]` 선택자**라 — 우리 `InboxRail.tsx:59` 카드는 `role` 이 없고, `ScheduleCard.tsx:43` 도 없다. 지금 상태로는 **안 걸린다**. 다만 `.scax-inbox-card--selected` 를 무조건 규칙으로 쓰면 수신함·캘린더 카드에도 새 CSS 가 얹힌다 |
| `.scax-gutter-list` (`components.css:105-108`) | 수신함 레일 · 캘린더 레일이 같은 클래스를 쓴다. 프로젝트가 헤더에 `Select` 를 넣으려면 `.scax-gutter-list__header`(높이 `--scax-control-height-sm` 32px, `components.css:106`)가 그 트리거를 담아야 한다 — **시안은 `.scax-gutter-list__header--sub` 로 `min-height:auto` 를 더한다**(`projects.css:3`) |
| `ds/Empty` | `Empty.tsx:10` 이 「소비처 29곳을 고치지 않는다」고 적는다. 시안 24px 글리프를 쓰려면 `Empty.tsx:70` 하드코딩 20 을 건드려야 하고 그러면 **29곳이 같이 움직인다** |
| `ds/ProgressBar` | 소비처 1곳(`WorkModals.tsx:1590`). `percent` 직접 입력을 더하면 이 자리와 함께 움직인다 |
| `AppHeader` | 시안 `titleEnd` 슬롯(`scax-ui.jsx:276-281`)을 더하면 5개 화면이 공유하는 셸이 움직인다 |

---

## 5. 살아남는 것 / 버리는 것 / 새로 만들 것

### 살아남는 것 (그대로 쓴다)

| 항목 | 근거 |
|---|---|
| `AppShell` · `AppHeader` · `AppBody` 3레일 틀 | `src/shell/AppShell.tsx:37,46,74` — 시안 `scax-ui.jsx:207,264,288` 과 마크업 동일 |
| `SideNav` + `folder` 아이콘 + `activeId="project"` | `src/shell/SideNav.tsx:70` · `App.tsx:39,398` — 아이콘까지 시안과 같다 |
| 레일 폭 토큰 380/342 | `scax.css:119-120` → `product.css:79-80` — 시안 §1 과 값까지 같다 |
| `--scax-*` 토큰 전부 (색·간격·반경·타입·포커스링) | `scax.css:6-129` — 시안 `projects.css` 가 참조하는 이름 중 **없는 것 0개** (§2-1 표) |
| `scax-inbox-card` 마크업 + `ScheduleCard` 조립법 | `components.css:111-121` · `ScheduleCard.tsx:42-99` — 시안 `ProjectTaskCard`(`projects.v1.jsx:8-28`)와 사실상 같은 코드 |
| `.scax-gutter-list` 레일 껍데기 | `components.css:105-108` · 선례 `InboxRail.tsx:103-114` · `ScheduleRail.tsx:81-108` |
| `Badge` 5톤 + `variant="count"` | `ds/Badge.tsx:24,38` · `components.css:37-41` — 시안 `PROJECT_STATUS_BADGE`(`data.js:20-26`) 톤 5종과 **한 칸도 안 틀린다** |
| 글리프 7종 (`square-check` `chevron-down` `chevron-right` `arrow-up` `arrow-down` `check` `folder`) | `glyphs.tsx:289,163,164,333,332,162,341` |
| `Empty` + `icon` prop | `ds/Empty.tsx:39,53` — 크기 20/24 한 칸 차이만 남는다 |
| 상태 톤 표 `taskStateTone` | `labels.ts:20-26` — 시안 톤 매핑과 완전 일치 |
| 레일 등록 seam (`onRegisterRails`) | `App.tsx:130-131,477,488,505` · 선례 `MyWorkPage.tsx:941-972` — 새 배관이 필요 없다 |
| `Select` 알약 트리거 CSS + `trigger` prop 선례 | `components.css:44-49` · `Select.tsx:404-407` · **실사용 `MyWorkPage.tsx:1410`** |
| `listProjects` / `getProject` / `getTask` / 체크리스트 4종 | `api.ts:793,797,158,1115-1134` — 호출 자체는 이미 있다 |

### 버리는 것 (시안에 대응물이 없다)

| 항목 | 근거 |
|---|---|
| 2컬럼 `.project-layout` 레이아웃 | `ProjectPage.tsx:146` · `screens-a.css:232` — 시안은 3레일이다 |
| 프로젝트 «목록» 좌 칸 (`.project-list` + `.project-row`) | `ProjectPage.tsx:147-189` — 시안은 헤더 `Select` 하나다(`projects.v1.jsx:39`) |
| 「새 프로젝트」 열기 폼 | `ProjectPage.tsx:150-173` — 시안 화면에 생성 손잡이가 없다 |
| 「현재 참여자」 + 붙이기/떼기 + 사유 입력 | `ProjectPage.tsx:206-290` — 시안 우 레일은 **업무** 상자다 |
| 「참여 이력」 구획 | `ProjectPage.tsx:292-306` |
| 「이 프로젝트의 업무」 평평한 `<ul>` | `ProjectPage.tsx:308-327` — 시안은 좌 레일 카드 + 간트 두 벌로 나뉜다 |
| `.screens-b-lead` 설명 한 줄 | `ProjectPage.tsx:140-144` — 시안 본문 첫 줄은 요약 스트립이다 |
| 화면 전용 CSS `.project-*` 11종 | `screens-a.css:231-260` — 대체될 자리 |
| 테스트 7개 중 6개의 단언 | `ProjectPage.test.tsx:89-178` (§1-4 표) |
| 상태를 맨 글자로 내는 자리 | `ProjectPage.tsx:321` — 시안은 배지다 |

### 새로 만들 것

| 항목 | 근거 |
|---|---|
| **간트**(축 34px · 행 40px · 라벨 200px · 격자 · today 선 · twisty · 3높이 바) | `grep -rin "gantt" src/` → **0건**. 시안 기하는 `projects.v1.jsx:5,76-83,108-164` |
| **의존선 SVG 오버레이**(직각 3구간 + 화살표 marker + 선택 강조) | SVG 오버레이 **0건**. 시안 `projects.v1.jsx:85-106` · `projects.css:42-44` |
| **요약 스트립** 5칸 그리드 | 대응 컴포넌트 없음. 시안 `projects.v1.jsx:49-73` · `projects.css:16-25` |
| **우 레일 업무 상자** (메타 `dl` · 관계 선행/후행 · 체크리스트 읽기 전용 · 하위 업무 카드) | `ProjectPage.tsx` 에 대응 0. 시안 `projects.v1.jsx:167-276` · `projects.css:69-116` |
| **`taskId` 선택 축**(좌 레일·간트·의존선·우 레일 동시 연동) | 지금 `useState` 열 개 중 `taskId` **없음**(`ProjectPage.tsx:28-41`) |
| **카드 선택 상태 CSS** `.scax-inbox-card--selected` + hover/focus | `grep` **0건**. 시안 `projects.css:6-9` |
| **`percent` 를 직접 받는 6px 미터** | `ds/ProgressBar.tsx:18` 은 `done/total` 만 받는다 |
| **레일을 등록하는 `ProjectPage`** (`onRegisterRails` prop + `pageProps` 확장) | `App.tsx:352,515` — 프로젝트는 지금 이 seam 에 안 붙어 있다 |
| **프로젝트 `Select` 를 레일 헤더에 얹는 조립** + `.scax-gutter-list__header--sub` | `projects.css:3` — 우리 헤더는 32px 고정(`components.css:106`) |
| **한 프로젝트의 업무를 진행률·선행·체크리스트까지 한 번에 받는 화면 데이터 조립 자리** | `src/features/project/` 에 변환 계층 **없음**. 지금 계약으로는 `getProject` + 업무당 `getTask` N회 (§3-4) |
| **간트/의존선/우 레일 전용 CSS 한 장** | 선례는 `src/styles/calendar.css` · `meetings.css`. `index.css:16-40` 에 `@import` 한 줄 추가하는 방식 |

---

## 6. 눈에 띈 것 (고치지 않았다)

1. `App.tsx:34` 주석이 「표시 순서는 시안에 맞추고」라 적지만 실제 순서는 시안과 다르다 —
   시안은 업무 → **프로젝트** → 캘린더(`nav.js:15-17`), 우리는 업무 → 캘린더 → **프로젝트**(`App.tsx:37-39`).
2. `src/ds/GutterList.tsx` 는 **소비처가 0건**이다(`grep <GutterList` → 0). 시안·DS 의 `GutterList` 와
   이름만 같고 다른 부품이라, 시안을 옮길 때 이름 충돌이 난다.
3. `ProjectDetail.tasks[].state` 가 `string` 으로 느슨하다(`viewModels.ts:99`) — 같은 파일의
   `TaskState`(`:121`)·`TaskChild.state`(`:163`)는 유니온이다. `ProjectPage.tsx:321` 이
   `as keyof typeof taskStateLabel` 로 억지 캐스팅하고 `?? task.state` 로 원문을 흘린다.
4. `ProjectPage.tsx:325` — 업무가 0건이고 내가 안 붙어 있으면 **빈 `<li>`** 가 선다(`{iAmIn ? "..." : ""}`).
   빈 리스트 항목이 DOM 에 남는다.
5. `ProjectPage.tsx:54-73` `reload` 의 deps 에 `selected?.project_id` 가 들어 있어(`:72`)
   프로젝트를 고를 때마다 콜백이 새로 만들어진다. 주석(`:71`)은 「선택이 튀지 않게」라 적지만
   deps 가 그 반대로 작동할 소지가 있다 — **확인만 했고 재현은 안 했다.**
6. `.design-sync/report/01-현재화면-대-시안.md:160` 이 내비를 「10항목 vs 8항목」이라 적는데
   실측은 **9 vs 9**(+utility 2)다. 문서가 낡았다.
7. `src/ds/Empty.tsx:69` 주석이 「우리 Icon 은 12/14/16/20 만 받는다」고 적지만
   `src/ds/icons/Icon.tsx:21` 은 **24도 받는다**. 주석이 낡았다.
