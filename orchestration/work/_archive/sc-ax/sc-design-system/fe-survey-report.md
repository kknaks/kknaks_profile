# 디자인 시스템 v2 ↔ 프론트 대조 조사 (read-only)

- 조사일: 2026-09-07 · 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` · 브랜치 `kknaksss/sc-design-system`
- SoT: `docs/design/design-system-v2.dc.html` (1622줄 · 단일 아트보드 `.doc` · 섹션 00~16)
- 대상: `frontend/src/styles.css` (901줄) · `frontend/src/*.tsx` 25개 · `frontend/src/chat/`

---

## 요약 (5줄)

1. `:root` 토큰 41개는 v2 를 **거의 정확히 옮겨놨다** — 색 26개·그림자 6개·radius 4개 전부 일치. 토큰 층은 이미 끝난 일이다.
2. 진짜 구멍은 **토큰 아래**다. `--surface-default` 가 정의 없이 16곳에서 쓰이고(배경이 투명해진다), 6개 클래스가 CSS 규칙 없이 tsx 에 박혀 있다.
3. 스페이스 스케일이 새고 있다 — v2 가 **명시적으로 금지한** 10·14·18px 이 57회(10px만 44회). 타입 스케일은 3회만 샜다(9·10·12.5px).
4. 컴포넌트는 **버튼·상태·오버레이·테이블은 맞고**, 업무 유형 배지 4종·Popover/Dropdown·체크박스/라디오/토글·스켈레톤·에러 인풋·Empty 아이콘/CTA 가 통째로 없다.
5. 레이아웃·반응형이 v2 와 **구조적으로 다르다** — 홈 3열이 2열, 콘텐츠 max 1640 없음, 좌우 여백 240/80/48 규칙 없음, v2 가 지원하지 않는다고 못박은 1024·900 브레이크포인트가 있다.

---

## 디자인이 정의한 것 (축별)

### (a) 색 토큰 — **정의됨** (`01 — COLOR`, `02 — STATUS & TYPE TOKENS`)
Primitive + Semantic 2계층. 회색은 블루그레이 8단계(`gray-900 #1B1E25` ~ `gray-50 #F6F7FA`, hue 220 통일, 순수 무채색 폐기), 브랜드는 indigo 5단계(`#F1F2FE`/`#7181F8`/`#5467F7`/`#374DF6`/`#1E37F4`), 상태는 sky 3 + red 4. `Surface #FFFFFF` 는 스케일 밖. green 없음(완료 = indigo). Hero Gradient 는 2겹(가로 3스톱 `#DDE7FF→#D6DAFB 46%→#D7E2FF` + 세로 흰색 페이드) 높이 **120px**, 홈 상단과 로그인 좌측 패널에만. 상태 5종은 dot/텍스트/틴트 3값 세트, 업무 유형 배지는 **4개 고정**(미팅·회의 `#EEF1FE/#4A55B8`, 개인 업무 `#F1F2FE/#4B52A8`, 문서·보고 `#F4F7FF/#3F5F94`, 취소 `#F4F5F7/#6D7483`+border). 채널색(메일/카톡/슬랙)은 별개 축.

### (b) 타이포 — **정의됨** (`03 — TYPE`)
Pretendard Variable. **16단계 × 3굵기**(Display 1 56 ~ Caption 2 11), line-height **145%** · letter-spacing **−2%** 전 스타일 단일값, **예외 없음**(`16 RULES` 8번). Regular 400 / Medium 500 / Bold 700 — v1 의 600 은 전부 700 으로. Medium 은 **버튼 라벨과 상태 텍스트에만**. 역할 매핑 13행(Page Title = Title 2 28 Bold, Item = Label 1 14 Bold, Body = Body 2 15 Regular, Meta = Label 2 13 Regular, Field Label = Label 2 13 Bold, Badge = Caption 2 11 Bold …).

### (c) 간격·radius·shadow — **정의됨** (`04 — LAYOUT & SPACING`, `06 — SURFACE & ELEVATION`)
스페이스 스케일 8단계 **4·8·12·16·20·24·32·48**. "스케일에 없는 값(**10, 14, 18**)은 쓰지 않습니다." 예외는 레이블–필드 **7px** 하나. 필드–헬퍼 6. 패딩 규칙 11행(Card r8 = 16/gap 8, Panel r16 = 24/gap 16, Metric r16 = 20/gap 8, Drawer = 24/24, Modal = 24/16 푸터 gap 8, List Row h68 = `0 16`/gap 12, Table Cell = `0 16` 첫 열 좌 20, Toolbar = `0 24`). Radius: Card 8 · Panel 16 · Popover 12 · Modal 16 · Drawer 0 · Button/Input 8 · Badge/Chip 4 · Event Block 6. 그림자 **6개뿐**(sm/md/lg/xl/drawer/ai), 그 외 금지(`16 RULES` 9번).

### (d) 컴포넌트와 상태 — **정의됨** (`07`~`14`), 상태는 부분 정의
- **버튼** (`08`): 5변형(Primary/Secondary/Ghost/Danger/AI) × 3높이(h40/h34/h30), radius 8, 라벨 Medium. **각 변형의 기본·hover·active·disabled 4상태 값이 전부 명시**됨. 아이콘만 있는 버튼은 정사각형.
- **폼** (`09`): 인풋 h38(강조 h48) · 텍스트에어리어 min-h96/p12 · 셀렉트 h38 · 날짜 h38 · 체크박스 16×16 r4 · 라디오 16×16 · 토글 36×20 · 검색 h34 w260. 에러 시 헬퍼 → 에러 텍스트 **교체**. 필수 `*` `#DA3C2B`.
- **상태** (`10`): focus 링 `border #7181F8 + 0 0 0 3px rgba(113,129,248,0.14)`, `:focus-visible` 만. disabled 는 **opacity 금지**(배경 `#F6F7FA`/글자 `#979FAF`/보더 `#E8EAF0`). 스켈레톤 bar `#EFF1F6` r4 h14 gap 10, 실제 콘텐츠와 같은 개수. Empty(아이콘 20 + Headline 2 Bold + Label 1 Meta + gap 12 + CTA), Empty–필터(초기화 버튼), Error(다시 시도).
- **컴포넌트** (`11`): Avatar 5크기(20/24/32/40/80, 정원, `linear-gradient(140deg,#E8EAF0,#D4D8E0)`), Sidebar 200 Ink pill active, Task Card w360 r8 p16 gap8, List Row h68, Metric Card 395×91 r16 p20, Tabs h44 Label 2, Breadcrumb top38, Period Stepper h30, Segmented, Progress bar, Log Row.
- **테이블** (`12`): 헤더 Label 2 13 Bold `#6D7483`, 행 h56 border-bottom `#EFF1F6`, 본문 Label 1 14 **Regular** `#1B1E25`, 셀 패딩 좌우 16 첫 열 20, hover `#F6F7FA` / selected `#F8FAFF`, 외곽 r12 1px `#D4D8E0`.
- **캘린더** (`13`): 3뷰(일/주/월), 좌측 레일 260, 월간 셀 min-h 120, 블록 = 유형 틴트 + 좌측 3px, 오늘 = Ink 원 + `#F8FAFF`, 진입 시 08:00 최상단.
- **오버레이** (`14`): Drawer 840(스크림 `rgba(30,30,30,0.32)`, shadow-drawer, p24) / Modal 600(r16 shadow-xl) / Popover 200–400(스크림 없음, r12 shadow-lg, 8px 띄움). Status Dropdown(현재 값 배경 `#F4F5FF`, 지연 없음). Toast 400×56 하단 중앙 60px 위 **4초**, 되돌릴 수 있으면 **실행취소 함께**. Inline Add Row.

### (e) 레이아웃 — **정의됨** (`04`, `05 — GRID & PAGE ARCHETYPE`)
캔버스 1920×1080. 사이드바 **200**(border-right `#E8EAF0`), 콘텐츠 **1640**(left 240 / right 1880). 8컬럼 그리드(컬럼 184 · 거터 24). 세로 리듬 breadcrumb **38** → 타이틀 **66** → 툴바 **108**(h30) → 패널 **140**(h900, 하단 1040). **페이지 아키타입 5종**: Dashboard(3열 **392/600/600**, hero 120, 테이블 금지) · List(단일 8col 1640 × h900 r16) · Calendar(좌 레일 260 + 본문 1356, 8컬럼 예외) · Detail Drawer(840 고정) · Settings(좌 네비 1col 184 + 본문 4col 808 최대). 툴바 순서 규칙(좌: Period Stepper → 필터, 우: 검색 → 뷰 전환 → Primary 하나), 툴바 요소 전부 **h30**.

### (f) 반응형 — **정의됨** (`15 — RESPONSIVE`)
데스크톱 전용. **1280 미만은 지원하지 않고 최소 폭 안내를 띄운다.** 3단: 1920(본문 1640, 여백 240) / 1440(본문 1080, 여백 **80**) / 1280(본문 1184, 여백 **48**, 사이드바 숨김 + 좌상단 **햄버거 오버레이**, 드로어 전체화면 + 스크림 제거, 칸반 가로 스크롤, 캘린더 레일 팝오버). "아이콘만 남기는 축소형 사이드바는 만들지 않습니다." 테이블은 시작일 → 업무 유형 순으로 열이 숨고, 업무명·상태·종료일은 끝까지 남는다.

### (g) 다크모드 — **정의되지 않음 / 명시적으로 없음**
`01 — COLOR` BRAND note 원문: "**다크모드도 멀티 테마도 없는 제품**이라 9단계 스케일의 나머지는 영구 미사용으로 남습니다." → 다크모드는 미구현이 아니라 **의도적 부재**. 프론트도 `prefers-color-scheme` 규칙이 0개(`styles.css` 전체) — **일치**.

---

## 대조표

판정: **일치** / **값 다름** / **누락**(디자인에 있고 프론트에 없음) / **프론트 전용**(디자인 미정의)

### (a) 색 토큰

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| gray 8단계 | `01` gray-900~50 8값 | `styles.css:4-11` `--text-primary`~`--surface-sunken` 8개, 값 동일 | **일치** |
| indigo 5단계 | `01` `#F1F2FE/#7181F8/#5467F7/#374DF6/#1E37F4` | `styles.css:14-17` `--selected-bg`,`--accent`,`--action`,`--action-hover`,`--action-active` | **일치** |
| sky 3 / red 4 | `01` Progress 3 · Danger 4 | `styles.css:20-25` `--progress-*` 3, `--danger-*` 4 | **일치** |
| 상태 틴트 `#F4F5F7` | `02` 시작전·취소 틴트 | `styles.css:26` `--status-neutral-tint` | **일치** |
| selected row `#F8FAFF` | `12` 테이블 selected · `13` 오늘 | `styles.css:13` `--surface-selected-row` 정의됨 | **일치**(정의) |
| Hero Gradient 색 | `01` `#DDE7FF/#D6DAFB 46%/#D7E2FF` + 흰색 페이드 | `styles.css:205` `.hero::before`, `styles.css:456` `.login-brand` — **hex 리터럴** | **일치**(값) / 토큰화 안 됨 |
| Hero Gradient 높이 | `01` **120px** | `styles.css:205` `height: 200px` | **값 다름** |
| 업무 유형 배지 4종 | `02` 미팅·회의/개인 업무/문서·보고/취소 8색 | 대응 클래스·색 없음 | **누락** |
| 채널 색 3종 | `02` 메일/카톡/슬랙 타일+카운트 | 대응 없음 | **누락** |
| `--surface-default` | 디자인에 없음 (Surface = `#FFFFFF`) | `styles.css` 16곳 사용, **`:root` 에 정의 없음** → 배경 미적용 | **버그** |
| `--warning-surface` / `--warning-text` | 디자인에 warning 색 **없음** | `styles.css:474` 폴백 `#fff4e5`/`#8a5300` | **프론트 전용** |
| 그래프 노드 8색 | 디자인 미정의 | `GraphCanvas.tsx:19-26` (`#5a63c9`,`#9a78df`,`#4da885`,`#d89038`,`#d96f8b` 등) | **프론트 전용** |
| 그래프 보조 5색 | 디자인 미정의 | `GraphCanvas.tsx:78-80,173,185,220,223` | **프론트 전용** |
| `#2b303a` hover | 디자인 미정의 (Ink hover 규칙 없음) | `styles.css:215` `.ax-prompt button:hover`, `styles.css:384` `.ax-launcher:hover` | **프론트 전용** |
| `#c9d1ff`, `#e6e8fd` | AI 서페이스 보더/hover — 디자인 AI 버튼은 `#D5DAFB`/`#E9ECFD` | `styles.css:213` `.ax-prompt` border, `styles.css:126` `.btn.ai:hover` | **값 다름** |

### (b) 타이포

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 폰트 패밀리 | `03` Pretendard Variable | `styles.css:39` `"Pretendard Variable", Pretendard, -apple-system…` | **일치** |
| line-height 145% | `03`·`16 RULES 8` 예외 없음 | `styles.css:42` `1.45` (전역) | **일치** |
| letter-spacing −2% | `03`·`16 RULES 8` 예외 없음 | `styles.css:43` `-0.02em` (전역) | **일치** |
| line-height 지역 오버라이드 | **금지** (`RULES 8`) | `styles.css:356`(1), `631`(1.5), `700`(1.5), `707`(1.55), `711`(1.5), `716`(1.5), `832`(1) — **7곳** | **값 다름 (규칙 위반)** |
| letter-spacing 지역 오버라이드 | **금지** | `styles.css:63` `letter-spacing: 0`, `styles.css:659` `0.02em` — **2곳** | **값 다름 (규칙 위반)** |
| 타입 스케일 16단계 | `03` 56/40/36/32/28/24/22/20/18/17/16/15/14/13/12/11 | `styles.css` font-size 197회 중 **194회 스케일 안** | **거의 일치** |
| 스케일 밖 크기 | 없어야 함 | `9px`×1, `10px`×2(`styles.css:506` 등), `12.5px`×1(`styles.css:716`) — **4회** | **값 다름** |
| Page Title = Title 2(28) Bold | `03` 역할 매핑 | `styles.css:95` `.page-head h1 { font-size: 28px }` + `h1~h4 font-weight:700` | **일치** |
| Metric 숫자 = 28 Bold | `03` | `styles.css:230` `.metric-value { 28px / 700 }` | **일치** |
| Drawer Title = Heading 1(22) Bold | `03` | `styles.css:352` `.drawer-head h3 { 22px }` | **일치** |
| Panel Title = Body 1(16) Bold | `03` | `styles.css:104` `.card-title h2/h3 { 16px }` | **일치** |
| Section = Body 2(15) Bold | `03` | `styles.css:107` `.section-title { 15px / 700 }` | **일치** |
| Item/리스트 제목 = Label 1(14) Bold | `03` | `styles.css:57` `.t-item { 14px/700 }`, `styles.css:172` `.cell-main b { 14px/700 }` | **일치** |
| Meta = Label 2(13) Regular | `03` | `styles.css:58` `.t-meta { 13px }` (weight 미지정 = 400) | **일치** |
| Field Label = Label 2(13) Bold | `03` | `styles.css:200` `.field > label { 13px / 700 }` | **일치** |
| Badge = Caption 2(11) Bold | `03` | `styles.css:143` `.badge { 11px / 700 }` | **일치** |
| **테이블 본문 = Label 1(14) Regular** | `12` "본문 텍스트 … Regular" | `styles.css:172` `.cell-main b { font-weight: 700 }` | **값 다름** |
| **상태 텍스트 = Label 1(14) Medium** | `02` "dot 8px + Label 1(14)" | `styles.css:133` `.status { font-size: 13px }` | **값 다름** |
| Tabs = Label 2(13) | `11` TABS h44 Label 2(13) | `styles.css:257` `.page-tabs button { font-size: 15px }` | **값 다름** |

### (c) 간격·radius·shadow

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 그림자 6종 값 | `06` sm/md/lg/xl/drawer/ai | `styles.css:28-33` 6개 전부, 값 동일 | **일치** |
| shadow-lg 사용처 (Popover) | `06` 팝오버·드롭다운·툴팁 | `--shadow-lg` **정의만 되고 사용 0회** | **누락**(Popover 미구현) |
| 그림자 6개 외 금지 | `RULES 9` | `styles.css:512` `var(--shadow-md, 0 12px 36px rgba(35,43,74,.14))` 폴백, `styles.css:208`·`856` inset shadow 2곳 | **값 다름 (규칙 위반)** |
| radius Card 8 / Panel 16 / Chip 4 / Control 8 | `06` | `styles.css:34-37` `--radius-card:8px` 등 4개 | **일치** |
| radius Popover 12 | `06` r12 | 별도 토큰 없음 · `12px` 리터럴 9곳(`styles.css:156,266,…`) | **값 다름**(토큰 부재) |
| 스페이스 스케일 4·8·12·16·20·24·32·48 | `04` | `styles.css` 대부분 준수 | **거의 일치** |
| **금지값 10/14/18px** | `04` "쓰지 않습니다" | **10px ×44** (`styles.css:396,398,445,468,484,488,498,506,512,520,526,528,530,532,602,623,652,741,742` 등) · **14px ×8** · **18px ×5** = **57회** | **값 다름 (규칙 위반)** |
| 레이블–필드 7 | `04` 유일한 예외 | `styles.css:199` `.field { gap: 7px }`, `styles.css:427` `.ax-context { gap: 7px }` | **일치** |
| 필드–헬퍼 6 | `09` | 헬퍼 요소 자체 없음 | **누락** |
| Card 패딩 16 / gap 8 | `04` | `styles.css:239` `.task-card { padding:16px; gap: 4px }` | **값 다름**(gap) |
| Panel 패딩 24 / gap 16 | `04` | `styles.css:102` `.surface-card { padding: 24px }` | **일치** |
| Metric 패딩 20 / gap 8 | `04` | `styles.css:228` `.metric-card { padding:20px; gap:8px }` | **일치** |
| Drawer 패딩 24 | `04` | `styles.css:350-354` head `24 24 16` / body `24` / foot `16 24` | **일치** |
| Modal 패딩 24 / gap 16 / 푸터 gap 8 | `04` | `styles.css:359-364` `padding:24px`, body `gap:16px`, foot `gap:8px` | **일치** |
| List Row `0 16` / gap 12 | `04` "세로 패딩 없이 높이로 정렬" | `styles.css:250` `.task-row { padding: 12px 16px }` | **값 다름** |
| Table Cell `0 16`, 첫 열 좌 20 | `04`·`12` | `styles.css:161` `.work-table .progress-row { padding: 0 16px 0 20px }` ✓ / `styles.css:186` `.plain-table th,td { padding: 0 12px }`, first-child `8px` | **값 다름**(plain-table) |
| Toolbar `0 24` / gap 8 | `04` | `styles.css:99` `.toolbar { gap: 16px }` (좌우 패딩 없음, canvas 가 소유) | **값 다름** |
| 섹션 사이 24 | `04` | `styles.css:103` `.surface-card + .surface-card { margin-top: 24px }` | **일치** |
| 폼 필드 사이 16 | `04` | `styles.css:201` `.form-stack { gap: 16px }` | **일치** |

### (d) 컴포넌트와 상태

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 버튼 높이 h40/h34/h30 | `08` 패딩 18/14/12, 폰트 14/13/12 | `styles.css:113-117` `.btn`(34/14/13) `.h40`(40/18/14) `.h30`(30/12/12) | **일치** |
| Primary 기본/hover/active | `08` `#5467F7`/`#374DF6`/`#1E37F4` | `styles.css:118-120` `--action`/`--action-hover`/`--action-active` | **일치** |
| Secondary 기본/hover | `08` `#fff`/`#F6F7FA` border `#D4D8E0` | `styles.css:112,114` | **일치** |
| Secondary **active** | `08` border `#979FAF` + bg `#EFF1F6` | `styles.css:115` bg 만 `--border-subtle`, border 그대로 | **값 다름** |
| Ghost 기본/hover/active | `08` transparent/`#F6F7FA`/`#EFF1F6`+Ink | `styles.css:121-122` + `.btn:active` 상속 | **일치** |
| Danger 기본/hover | `08` `#DA3C2B`/`#C43222` | `styles.css:123-124` | **일치** |
| Danger **active** | `08` `#AE2C1E` | 없음 | **누락** |
| AI 버튼 | `08` bg `#F1F2FE` · **border `#D5DAFB`** · **글자 `#4B52A8`** · padding `0 12` | `styles.css:125` border **transparent** · 글자 `--action`(`#5467F7`) · padding `0 14` | **값 다름** |
| AI hover / active | `08` `#E9ECFD`+`#C3CBFB` / `#DDE2FC`+`#A6B0F7`+`#3A4194` | `styles.css:126` hover `#e6e8fd` 만, active 없음 | **값 다름 + 누락** |
| 아이콘 전용 버튼 = 정사각 | `07` h34→34×34, h30→30×30 | `styles.css:129` `.btn.icon { width: 30px }` (높이와 무관하게 30 고정) | **값 다름** |
| 상태 dot 8px + 5색 | `02` | `styles.css:134-141` dot 8px, 5상태 dot·텍스트 색 전부 일치 | **일치** |
| 상태 텍스트 크기 | `02` Label 1 (14) | `styles.css:133` `13px` | **값 다름** |
| Badge h20 r4 11px Bold | `02`·`06` | `styles.css:143` | **일치** |
| Badge 취소 = border `#E8EAF0` | `02`·`06` | `styles.css:148` `.badge.outline` border `--border-default` | **일치** |
| 업무 유형 배지 4종 | `02`·`RULES 5` | `.badge.ai/.neutral/.progress/.danger/.outline` — **다른 축** | **누락 + 프론트 전용** |
| Segmented h30, active Ink | `11`·`RULES 3` | `styles.css:149-151` h30, `aria-selected` Ink | **일치** |
| Avatar 20/24/32/40/80 | `11` 5크기 | `styles.css:72-75` xs20 · md32 · lg40 · xl80 — **sm 24 없음** | **누락**(1크기) |
| Avatar 기본 채움 gradient | `11` `linear-gradient(140deg,#E8EAF0,#D4D8E0)` | `styles.css:71` `linear-gradient(140deg, var(--border-default), var(--border-strong))` | **일치** |
| Avatar 이미지 안쪽 테두리 | `11` `1px rgba(27,30,37,0.06)` | `styles.css:208` `.hero-identity .avatar.xl` 만 | **부분 일치** |
| Avatar 비어 있음 (`#EFF1F6`+`#E8EAF0`) | `11` | 없음 | **누락** |
| Task Card r8 p16 border strong | `11` | `styles.css:239` | **일치** |
| List Row h68 | `11` | `styles.css:250` `.task-row { min-height: 68px }` | **일치** |
| Metric Card r16 p20 shadow-sm border `#E8EAF0` | `11` | `styles.css:228` | **일치** |
| Tabs h44 | `11` | `styles.css:257` `.page-tabs button { height: 40px }` | **값 다름** |
| Breadcrumb top 38 | `11`·`05` | `styles.css:84` `.canvas-topbar { height: 38px }` | **일치** |
| Period Stepper h30 | `11` | `styles.css:265` `.stepper` — 높이 미지정 | **값 다름** |
| Progress bar | `11` | 없음 | **누락** |
| Log Row (최신만 dot `#7181F8`) | `11` | `styles.css:594~` timeline/discussion 유사물 있으나 규격 다름 | **값 다름** |
| 테이블 외곽 r12 1px `#D4D8E0` | `12` | `styles.css:156` `.work-table` | **일치** |
| 테이블 행 h56 + `#EFF1F6` | `12` | `styles.css:161`, `styles.css:187` | **일치** |
| 테이블 헤더 13 Bold `#6D7483` | `12` | `styles.css:157`, `styles.css:185` | **일치** |
| 테이블 hover `#F6F7FA` | `12` | `styles.css:170`, `styles.css:191` | **일치** |
| 테이블 **selected `#F8FAFF`** | `12` | `--surface-selected-row` 는 캘린더/타임라인 today 에만 — 테이블 selected 규칙 없음 | **누락** |
| 정렬 가능 헤더 chevron | `12` | 없음 | **누락** |
| 빈 값 `—` `#6D7483` | `12` | 규칙 없음 | **누락** |
| 캘린더 월간 셀 min-h 120 | `13` (1280 이하 96) | `styles.css:274` `min-height: 96px` (항상) | **값 다름** |
| 캘린더 오늘 = Ink 원 + `#F8FAFF` | `13` | `styles.css:277-279` | **일치** |
| 캘린더 블록 = 틴트 + 좌 3px | `13`·`06` Event Block r6 | `styles.css:280` `.calendar-chip` 좌 3px ✓ / radius `--radius-chip`(4) | **값 다름**(radius) |
| 캘린더 일/주 뷰 · 좌측 레일 260 | `13`·`05` | 월간 + 타임라인 + 칸반. 일·주 뷰 없음, 좌측 레일 없음 | **누락** |
| Drawer 840 + 스크림 + shadow-drawer | `14` | `styles.css:348-349` `width: min(840px,100vw)`, `rgba(30,30,30,0.32)`, `--shadow-drawer` | **일치** |
| Modal 600 r16 shadow-xl | `14` | `styles.css:358-359` | **일치** |
| **Popover 200–400 r12 shadow-lg** | `14` | 없음 (`--shadow-lg` 미사용) | **누락** |
| Status Dropdown (현재값 `#F4F5FF`, 지연 제외) | `14` | 없음 — `<select>` 로 대체 | **누락** |
| Toast 400×56 하단 60 · 4초 | `14` | `styles.css:377` 400/56/bottom 60 ✓ · `Modal.tsx:96` `setTimeout(onClose, 4000)` ✓ | **일치** |
| Toast **실행취소** | `14` "되돌릴 수 있으면 함께" | `Modal.tsx:102-104` `×` 닫기만 | **누락** |
| Inline Add Row | `14` | `.inline-reason` 은 사유 입력 전용 | **누락** |
| focus `:focus-visible` + ring 0.14 | `10` | `styles.css:55` `:focus-visible { border-color: var(--accent); box-shadow: var(--focus-ring) }` | **일치** |
| disabled — opacity 금지 | `10` | `styles.css:127` `.btn:disabled` 색 3종 ✓ / `styles.css:307` `.kanban-card.dragging { opacity: 0.5 }` (drag 상태라 별건) | **일치** |
| 인풋 h38 r8 border strong | `09` | `styles.css:194` | **일치** |
| 인풋 강조 h48 · Headline 2(17) Bold | `09` | `styles.css:198` `.title-input { 48px / 17px / 700 }` | **일치** |
| Textarea min-h 96 / p 12 | `09` | `styles.css:197` | **일치** |
| **인풋 에러 상태** (border `#E2685B` + 에러 텍스트 `#C43222`) | `09` | 인풋 단위 에러 규칙 없음 (`error-banner` 는 페이지 배너) | **누락** |
| **필수 `*` `#DA3C2B`** | `09` | 없음 | **누락** |
| **Checkbox 16×16 r4** | `09` | `WorkModals.tsx` 3곳 네이티브 input, 스타일 규칙 없음 | **누락** |
| **Radio 16×16** | `09` | 사용처 0 | **누락** |
| **Toggle 36×20** | `09` | 사용처 0 | **누락** |
| **Search h34 w260** | `09` | `chat/ChatDrawer.tsx` 1곳 `type="search"`, 전용 스타일 없음 | **누락** |
| **Skeleton** (`#EFF1F6` r4 h14 gap10) | `10` | 클래스·컴포넌트 0 | **누락** |
| Empty 블록 | `10` 아이콘 20 + 제목 17 Bold + 설명 14 Meta + gap 12 + **CTA** | `styles.css:176` 제목 17 ✓ 설명 14 ✓ gap 12 ✓ / **아이콘·CTA 없음** (`MyWorkPage.tsx:301`, `OrgPage.tsx:375` 등 11곳 전부) | **부분 누락** |
| Empty — 필터 결과 없음 + 초기화 | `10` | 없음 | **누락** |
| Error — 다시 시도 | `10` | `error-banner` 는 다른 형태 | **누락** |
| 아이콘 규격 (16 그리드 · stroke 1.5 · round) | `07` | SVG 아이콘 시스템 없음 — 텍스트 글리프(`×`, `▾`, 이모지)로 대체 | **누락** |

### (e) 레이아웃

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 사이드바 200 + border-right `#E8EAF0` | `04`·`11` | `styles.css:61-62` `grid-template-columns: 200px …`, `border-right: 1px solid var(--border-default)` | **일치** |
| 사이드바 active = Ink pill | `11`·`RULES 3` | `styles.css:78` `.rail nav button.active { color:#fff; background: var(--text-primary) }` | **일치** |
| **콘텐츠 폭 1640 max** | `04`·`05` | `.canvas` 에 max-width 없음 (`styles.css:83`) | **누락** |
| **좌우 여백 240** (1920 기준) | `04`·`15` | `styles.css:83` `.canvas { padding: 0 48px 64px }` 고정 | **값 다름** |
| 8컬럼 그리드 (184 / 거터 24) | `05` | 그리드 시스템 없음 | **누락** |
| breadcrumb y=38 | `05` | `styles.css:84` height 38 ✓ | **일치** |
| 타이틀 y=66 · 툴바 y=108 · 패널 y=140 | `05` | `styles.css:94` `.page-head { min-height: 42px; margin-bottom: 24px }`, `styles.css:99` `.toolbar { min-height: 30px; margin-bottom: 16px }` — 리듬은 근사하나 좌표 규칙 아님 | **값 다름** |
| **Dashboard 3열 392/600/600** | `05` | `styles.css:233` `.home-columns { minmax(300px,392px) minmax(0,1fr) }` — **2열** | **값 다름 (구조)** |
| Dashboard hero 120 + AI 프롬프트 h52 | `05`·`01` | `styles.css:205` hero 200px / `styles.css:213` `.ax-prompt { height: 52px }` ✓ | **값 다름**(hero) |
| Dashboard 테이블 금지 | `05` | `TodayPage.tsx` 카드·리스트만 사용 | **일치** |
| **List = 단일 8col(1640) 패널** | `05` | `styles.css:255` `.work-layout { minmax(300px,360px) minmax(0,1fr) }` — 2열 | **값 다름 (구조)** |
| Calendar 좌측 레일 260 | `05`·`13` | 없음 | **누락** |
| Detail Drawer 840 · 내부 단일 컬럼 | `05` | `styles.css:348` 840 ✓ | **일치** |
| 드로어 위 모달 금지 | `05`·`RULES 4` | 확인 필요 (동시 렌더 경로 미확인) | **확인 필요** |
| **Settings 아키타입 (좌 184 + 본문 808)** | `05` | 설정 화면 자체가 없음 | **누락** |
| 툴바 요소 전부 h30 | `05` | `styles.css:99` `.toolbar { min-height: 30px }` / `styles.css:96` `.page-head-actions input[type=date] { height:34px }`, `styles.css:261` `.list-toolbar select { height:34px }`, `styles.css:490` `.graph-search { height:40px }` | **값 다름** |
| 툴바 Primary 는 맨 오른쪽 하나 | `05`·`RULES 12` | 확인 필요 (화면별 점검 필요) | **확인 필요** |

### (f) 반응형

| 축 | 디자인 값 (섹션) | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 브레이크포인트 1920 / 1440 / 1280 | `15` | `styles.css:429`(1280) · `435`(1024) · `440`(900) · `520`(1100) · `545`(900) · `587`(1024) · `662`(720) · `804`(900) — **7개 값** | **값 다름** |
| 1440 여백 80 | `15` | 없음 | **누락** |
| 1280 여백 48 | `15` | `styles.css:430` `padding: 0 24px 48px` | **값 다름** |
| **1280 미만 최소 폭 안내** | `15` "지원하지 않고 … 띄웁니다" | 없음. 대신 1024·900·720 에서 계속 레이아웃을 접는다 | **누락 + 프론트 전용** |
| 1280 사이드바 → 햄버거 오버레이 | `15` | `styles.css:441-446` **900** 에서 가로 스크롤 레일로 변환 (아이콘/축소형에 가까움 — `15` 가 금지) | **값 다름 (규칙 위반)** |
| 1280 드로어 전체화면 · 스크림 제거 | `15` | `styles.css:432` `.drawer { width: 100vw }` ✓ / 스크림 제거는 없음 | **부분 일치** |
| 칸반 4컬럼 · 최소 240 · 가로 스크롤 | `15` | `styles.css:299` `repeat(4, minmax(220px,1fr))` + `overflow-x:auto` | **값 다름**(220 vs 240) |
| 테이블 열 숨김 순서 (시작일 → 유형) | `15`·`12` | 없음 — `styles.css:449` `.plain-table { overflow-x: auto }` (가로 스크롤, `12` 는 "마지막 수단") | **값 다름** |
| 캘린더 월간 셀 120→96 | `15` | 항상 96 (`styles.css:274`) | **값 다름** |

### (g) 다크모드

| 축 | 디자인 값 (섹션) | 현재 값 | 판정 |
|---|---|---|---|
| 다크모드 | `01` note "다크모드도 멀티 테마도 없는 제품" — **없음이 정의** | `prefers-color-scheme` 규칙 0개 | **일치** |

### 위생 (스타일 계약 자체)

| 축 | 기대 | 현재 값 (파일:줄) | 판정 |
|---|---|---|---|
| 토큰 소유는 styles.css 한 곳 | `docs/design/README.md` | tsx 인라인 style 25개 — **색은 0개**(전부 spacing/grid). 단 `RelationGraphPage.tsx:269,277` 이 `KIND_COLOR` 주입 | **거의 일치** |
| tsx hex 리터럴 | 0 이어야 함 (`rules.md`) | **15개, 전부 `GraphCanvas.tsx`** (19–26, 78–80, 173, 185, 220, 223) | **값 다름** |
| styles.css hex 리터럴 (`:root` 밖) | 토큰만 써야 함 | **38개** = `#fff`×25 + `#2b303a`×2 + hero 3색×2 + `#c9d1ff`·`#e6e8fd`·`#f1f2fe`·`#fff4e5`·`#8a5300` | **값 다름** |
| 정의되지 않은 CSS 변수 | 0 | `--surface-default` **16회** (폴백 없음 → 배경 미적용), `--warning-surface`/`--warning-text`(폴백 있음) | **버그** |
| CSS 규칙 없는 className | 0 | `form-grid`(`ActionCenter.tsx:266,503`), `surface-card-list`, `round-basis`, `conflict`, `final`, `ax-rail-timings` — **6개** | **버그** |
| 정의만 되고 안 쓰이는 토큰 | — | `--shadow-lg` (Popover 미구현의 신호) | **누락 신호** |

---

## 바꿔야 할 것 — 우선순위

### A. CSS 토큰·값만 고치면 되는 것 (마크업 변경 없음)

| # | 항목 | 근거 (디자인) | 근거 (프론트) | 규모 |
|---|---|---|---|---|
| A1 | **`--surface-default` 를 `:root` 에 정의**(= `#fff`) 하거나 16곳을 `--surface` 로 교체 | `01` Surface = `#FFFFFF` | `styles.css` 16곳 (468, 490, 493, 498, 506, 512, 532 …) | 1줄 or 16곳 |
| A2 | **금지 스페이스 10 / 14 / 18px 제거** → 8·12·16·20 으로 | `04` "스케일에 없는 값(10, 14, 18)은 쓰지 않습니다" | 10px×44 · 14px×8 · 18px×5 = **57회** | 대 |
| A3 | **Hero Gradient 높이 200 → 120** | `01` "높이는 120px입니다" (v1 400 은 오기) | `styles.css:205` `height: 200px` | 1줄 |
| A4 | **AI 버튼 3상태 값 맞추기** (기본 border `#D5DAFB`·글자 `#4B52A8`·p12 / hover `#E9ECFD`+`#C3CBFB` / active `#DDE2FC`+`#A6B0F7`+`#3A4194`) | `08` BUTTON | `styles.css:125-126` | 3줄 |
| A5 | **Danger active `#AE2C1E`, Secondary active border `#979FAF`** 추가 | `08` | `styles.css:115,123` | 2줄 |
| A6 | **상태 텍스트 13 → 14px** (Label 1) | `02` "dot 8px + Label 1(14)" | `styles.css:133` | 1줄 |
| A7 | **테이블 본문 굵기 700 → 400** | `12` "본문 텍스트 Label 1(14) · Regular" | `styles.css:172` `.cell-main b` | 1줄 |
| A8 | **Tabs 높이 40 → 44, 폰트 15 → 13** | `11` "TABS · h44 · Label 2(13)" | `styles.css:257` | 1줄 |
| A9 | **line-height / letter-spacing 지역 오버라이드 9곳 제거** | `RULES 8` "행간과 자간은 손대지 않음 … 패딩으로 맞춥니다" | `styles.css:63,356,631,659,700,707,711,716,832` | 9줄 |
| A10 | **스케일 밖 font-size 4곳 정리** (9 → 11, 10 → 11, 12.5 → 12) | `03` 16단계 | `styles.css:506,716` 등 | 4줄 |
| A11 | **`.plain-table` 셀 패딩 12 → 16, 첫 열 8 → 20** | `04`·`12` | `styles.css:186,189` | 2줄 |
| A12 | **`.task-card` gap 4 → 8** | `04` "Card (r8) 패딩 16 · 내부 gap 8" | `styles.css:239` | 1줄 |
| A13 | **`.task-row` 패딩 `12px 16px` → `0 16px`** (h68 로 정렬) | `04` "세로 패딩 없이 높이로 정렬" | `styles.css:250` | 1줄 |
| A14 | **`--radius-popover: 12px` 토큰 추가** 후 리터럴 12px 9곳 치환 | `06` Popover r12 | `styles.css:156,266,…` | 1+9줄 |
| A15 | **`.btn.icon` 을 정사각형으로** (`width: 34px`, `.h30` 일 때 30) | `07` "h34면 34×34, h30이면 30×30" | `styles.css:129` | 2줄 |
| A16 | **`.avatar.sm` (24px) 추가** | `11` 5크기 | `styles.css:72-75` | 1줄 |
| A17 | **캘린더 월간 셀 min-h 96 → 120** (1280 이하만 96) | `13`·`15` | `styles.css:274` | 2줄 |
| A18 | **`.calendar-chip` radius 4 → 6** (Event Block) | `06` Event Block r6 | `styles.css:280` | 1줄 |
| A19 | **`shadow-md` 폴백 및 inset shadow 정리** | `RULES 9` "그림자는 6개뿐" | `styles.css:512,856` | 2줄 |
| A20 | **테이블 selected 행 `#F8FAFF`** 규칙 추가 | `12` | `--surface-selected-row` 이미 정의됨, 테이블에 미적용 | 2줄 |
| A21 | **툴바 요소 높이 h30 통일** (date/select 34, graph-search 40) | `05` "툴바 요소는 전부 h30" | `styles.css:96,261,490` | 3줄 |
| A22 | **칸반 컬럼 최소폭 220 → 240** | `15` | `styles.css:299` | 1줄 |

### B. 컴포넌트 구조를 바꿔야 하는 것 (마크업·새 컴포넌트)

| # | 항목 | 근거 (디자인) | 근거 (프론트) | 규모 |
|---|---|---|---|---|
| B1 | **CSS 규칙 없는 className 6개 해결** — 스타일을 쓰거나 마크업에서 제거 | 위생 | `form-grid`(`ActionCenter.tsx:266,503`) · `surface-card-list` · `round-basis` · `conflict` · `final` · `ax-rail-timings` | 중 |
| B2 | **Skeleton 컴포넌트** (bar `#EFF1F6` r4 h14 gap10 · 리스트 5행) | `10` STATE · `RULES 10` "정상만 그린 화면은 미완성" | 존재 0 | 중 |
| B3 | **Empty 블록에 아이콘 20 + CTA 슬롯** · 필터 variant(초기화) · Error variant(다시 시도) | `10` STATE | `styles.css:176` + 사용처 11곳(`MyWorkPage.tsx:301`, `OrgPage.tsx:231,375`, `CalendarPage.tsx:192` …) | 중 |
| B4 | **Popover / Dropdown 컴포넌트** (200–400 · r12 · shadow-lg · 스크림 없음 · 8px 띄움) + Status Dropdown | `14` OVERLAY | `--shadow-lg` 사용 0회, `<select>` 로 대체 중 | 대 |
| B5 | **폼 컨트롤 4종** — Checkbox(16 r4) · Radio(16) · Toggle(36×20) · Search(h34 w260) | `09` FORM | Checkbox 네이티브 3곳(`WorkModals.tsx`), 나머지 0 | 대 |
| B6 | **인풋 에러 상태 + 헬퍼/에러 텍스트 교체 + 필수 `*`** | `09` FORM | 인풋 단위 규칙 없음 | 중 |
| B7 | **아이콘 시스템** (viewBox 16 · stroke 1.5(≤14 는 1.3) · round · fill none · 12/14/16/20) | `07` ICON | 텍스트 글리프(`×`, `▾`, 이모지)로 대체 중 | 대 |
| B8 | **Dashboard 3열 392/600/600** 으로 (현재 2열) | `05` 아키타입 1 | `styles.css:233` `.home-columns` + `TodayPage.tsx` | 대 |
| B9 | **List 아키타입 = 단일 8col 패널** 로 (현재 2열 360+1fr) | `05` 아키타입 2 | `styles.css:255` `.work-layout` + `MyWorkPage.tsx` | 대 |
| B10 | **콘텐츠 max 1640 + 여백 240/80/48 3단** 적용 | `04`·`15` | `styles.css:83` 고정 48 | 중 |
| B11 | **1280 미만 최소 폭 안내 화면** + 1024·900·720 브레이크포인트 정리 | `15` "1280 미만은 지원하지 않고 … 최소 폭 안내를 띄웁니다" | `styles.css:435,440,520,545,587,662,804` | 중 |
| B12 | **1280 사이드바 → 햄버거 오버레이** (현재 900 에서 가로 레일 = `15` 가 금지한 축소형) | `15` | `styles.css:441-446` | 중 |
| B13 | **Toast 실행취소 액션** | `14` "되돌릴 수 있으면 실행취소를 함께" | `Modal.tsx:100-105` `×` 만 | 소 |
| B14 | **Progress bar · Log Row 규격** | `11` COMPONENTS | 유사물은 있으나 규격 다름 | 중 |
| B15 | **테이블 정렬 헤더 chevron · 빈 값 `—` · 반응형 열 숨김 순서** | `12`·`15` | 없음 | 중 |
| B16 | **GraphCanvas 색 15개를 토큰으로** (또는 디자인에 그래프 팔레트 등록 요청) | `rules.md` "임의 hex 리터럴 금지" | `GraphCanvas.tsx:19-26,78-80,173,185,220,223` | 중 |
| B17 | **캘린더 일/주 뷰 + 좌측 레일 260** | `05` 아키타입 3 · `13` | 월간·타임라인·칸반만 | 대 |
| B18 | **Settings 아키타입 화면** (좌 네비 184 + 본문 808) | `05` 아키타입 5 | 설정 화면 없음 | 대 |

---

## 디자인 미정의 · 프론트 전용

### 디자인에 있는데 프론트에 대응이 없는 것
- **화면**: 설정(아키타입 5) · 자료함 · 회의록 전용 화면(현재 `MeetingDrawer` 드로어만) · 캘린더 일/주 뷰 · 칸반 외 List 단일 패널
- **컴포넌트**: Popover/Dropdown · Status Dropdown · Skeleton · Toggle · Radio · Search 필드 · Progress bar · Inline Add Row · 아이콘 시스템 · Avatar sm(24)/비어 있음 variant
- **개념**: 업무 유형 배지 4종(미팅·회의 / 개인 업무 / 문서·보고 / 취소) · 채널 색(메일·카톡·슬랙) · 8컬럼 그리드 · 세로 리듬 좌표(38/66/108/140)

### 프론트에 있는데 디자인이 정의하지 않은 것
- **화면**: 보고(일일보고) · 프로젝트 · 조직 · **관계 탐색(그래프)** · AX 대화 드로어(`ax-drawer`, 440px) · 로그인 데모 계정 목록
- **개념**: 조직·권한·요청자·담당자·참조 (README `권한 — 조직이 정한다`, `업무 — 요청과 배정`) — 디자인은 이 개념들의 **부재**를 전제로 쓰였다 (아래 미결 1번)
- **색**: 그래프 노드/엣지 15색(`GraphCanvas.tsx`) · warning 2색(`--warning-surface #fff4e5` / `--warning-text #8a5300`) · Ink hover `#2b303a`
- **상태값**: `negotiating` · `accepted` · `rejected` · `pending` (`styles.css:136-141`) — 디자인 상태는 5종(시작전/진행중/완료/취소/지연)뿐
- **브레이크포인트**: 1100 · 1024 · 900 · 720 (디자인은 1280 이 하한)
- **뷰**: 칸반 · 타임라인(간트) — 디자인은 칸반을 `15`·`05` 에서 언급하나 규격은 미정의, 타임라인은 언급 없음

---

## 미결 · 확인 필요

1. **[중대] 제품 전제가 어긋난다.** 디자인 v2 는 헤더와 `11`·`12`·`RULES 1` 에서 "**개인 워크스페이스용 업무 기록 앱. 요청자·담당자·참조 개념이 없고, 모든 기록은 본인이 등록합니다**", "카드·리스트·테이블·캘린더·로그에 사람 표기를 넣지 않습니다"라고 못박는다. 그런데 sc-ax 는 `README.md` 「권한 — 조직이 정한다」·「업무 — 요청과 배정」이 보여주듯 **조직·요청자·담당자가 핵심**이고, `styles.css:243-245` `.task-card-people`·`.person-chip`·`.person-arrow` 가 카드 안에 사람을 그린다. → **디자인을 sc-ax 에 맞춰 확장할지, 프론트에서 사람 표기를 걷어낼지** 코디네이터/planner 판단 필요. 이 답에 따라 B8·B9 와 카드/리스트 구조가 통째로 달라진다.

2. **디자인 문서 내부 모순 — 홈 좌측 열 폭.** `05` 는 "홈 3열이 392/600/600 으로 바뀝니다"라고 하는데 `04` 카드는 여전히 `360 / 560 / 672 · 상단 히어로 400` 이라 적혀 있고, `11` TASK CARD 는 `w360`. 프론트는 392(`styles.css:233`)를 따르고 있다. **392 가 맞다고 보고 진행했으나 확정 필요.**

3. **디자인 문서 내부 모순 — Hero 높이.** `01` 과 `00` 은 "120px"(v1 의 400 은 오기)인데 `05` Dashboard 표는 "Hero Gradient 120", `RULES 7` 은 "홈 상단 **400px**". → **120 이 맞다고 보고 A3 을 제안했으나 확정 필요.**

4. **`styles.css:136-141` 의 상태값 4종**(`negotiating`/`accepted`/`rejected`/`pending`)이 디자인 5상태 중 무엇에 매핑되는지 미정의. 현재 `negotiating`·`accepted` 를 완료색(indigo), `pending` 을 진행중색으로 쓰는데 근거가 없다.

5. **`RULES 4` "드로어 위에 모달을 겹치지 않습니다"** 준수 여부를 확인하지 못했다 — `WorkModals.tsx`(107KB) 안에서 드로어와 모달이 동시에 열리는 경로가 있는지 정적으로 판별 불가. 다음 태스크에서 렌더 경로 추적 필요.

6. **`RULES 12` "툴바 Primary 는 맨 오른쪽 하나"** 를 화면별로 점검하지 못했다.

7. **칸반·타임라인(간트)** 은 디자인에 규격이 없다(`15` 가 칸반 반응형만 언급). 그대로 둘지, 디자인에 등록을 요청할지 결정 필요.

8. **스펙(`20-spec/`) 대조는 하지 못했다** — `21-screen/`·`21-html/` 이 비어 있어 화면 명세가 없다(브리프 §1 이 예고한 대로). 화면 골격 판단은 `README.md` 와 `App.tsx:18-25` 의 네비게이션 7개에 근거했다.

---

## 검증 (§8 자체 점검)

**(1) 디자인 축 (a)~(g) 전부에 「정의됨/미정의」가 적혀 있는가** — ✅
(a) 정의됨 · (b) 정의됨 · (c) 정의됨 · (d) 정의됨(상태는 버튼만 4상태 전부, 나머지 부분) · (e) 정의됨 · (f) 정의됨 · (g) **명시적으로 없음(= 부재가 정의)** — 7/7 기재.

**(2) 대조표의 모든 행에 파일:줄 또는 아트보드/섹션명이 있는가** — ✅
대조표 7개 표 · 총 **97행**. 전 행에 디자인 열은 섹션 번호(`01`~`16`), 프론트 열은 `styles.css:줄` / `파일.tsx:줄` 또는 "없음/사용처 0"(부재 근거)을 기재. 좌표를 못 준 2행(`드로어 위 모달`, `툴바 Primary`)은 판정을 **확인 필요**로 두고 미결 5·6번에 옮겼다.

**(3) hex 리터럴 전수 개수가 grep 결과와 일치하는가** — ✅
- 비테스트 `*.tsx`/`*.ts`(`chat/` 포함): **15개**, 전부 `GraphCanvas.tsx`(19,20,21,22,23,24,25,26,78,79,80,173,185,220,223).
  검증 명령: `grep -o '#[0-9a-fA-F]\{3,6\}' <비테스트 tsx/ts> | wc -l` → `15`. 파일별 집계도 `GraphCanvas.tsx: 15` 단일. 리포트 본문 수치와 일치.
- `styles.css` `:root` 밖(46–901줄): **38개** = `#fff`×25 + `#2b303a`×2 + `#dde7ff`×2 + `#d7e2ff`×2 + `#d6dafb`×2 + `#fff4e5`×1 + `#f1f2fe`×1 + `#e6e8fd`×1 + `#c9d1ff`×1 + `#8a5300`×1. 합 = 25+13 = 38. 일치.

**추가 자체 점검 (수치)**
- CSS 변수 교차검증: 사용됐으나 미정의 **5개**(`--surface-default` 16회 · `--warning-surface` · `--warning-text` · `--days`/`--columns`는 인라인 지역 변수라 정상), 정의됐으나 미사용 **1개**(`--shadow-lg`).
- className 교차검증: tsx 에서 쓰이나 `styles.css` 에 규칙 0인 클래스 **6개**.
- font-size 197회 중 스케일 밖 **4회**(9·10·10·12.5).
- spacing 값 중 v2 금지값 **57회**(10px×44 · 14px×8 · 18px×5).
- line-height/letter-spacing 지역 오버라이드 **9곳**.

**(4) git status 가 리포트 파일 외에 깨끗한가** — ✅
`git status --porcelain` → **빈 출력**. 워크트리 파일을 하나도 만들거나 고치지 않았다. 리포트는 워크트리 밖(코디 워크트리 `orchestration/work/sc-design-system/fe-survey-report.md`)에만 썼다.
