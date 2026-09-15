# `DS-gaps.md` — 새 DS 에 없는 것 (사용자 컨펌용)

- **조사일** 2026-09-13 · **워커** designer(바퀴 0)
- 이 목록은 **§1-1 적용 사다리의 ④(발명 금지)로 떨어진 것 전부**다. 리포트 본문(`ds-token-report.md`)과 겹치는 설명은 걷어내고 판단에 필요한 것만 남겼다.
- **「네 제안」은 제안일 뿐이다. 결정은 사용자가 한다.**
- **사용처 수**는 `frontend/src` 에서 센 **프로덕션** 건수다(테스트 제외). 1곳짜리와 20곳짜리는 판단이 다르다.
- 사용자 방침이 「대부분 새 DS 에 추가하고 DS 를 갱신」이므로 **`폐기` 제안은 사용처 0인 항목에만** 달았다.

**항목 46건 — `DS 에 추가 요청` 36 · `대체 가능` 6 · `폐기` 2 · `그대로 두기 권함` 2.**

> ⚠ **G-03b 는 2026-09-13 정정됐다** — 「폐기 5종」 중 셋이 실제로는 살아 있었다(동적 `name={…}` 이라 grep 에 안 잡혔다). 진짜 0곳은 `ban`·`pending` 둘뿐이다.
(부품 10 · 토큰 11 · 클래스·패턴 3 · **바퀴 중 추가 22**)

> G-25~G-46 은 조사(바퀴 0) 뒤 **구현 바퀴를 돌면서 나온 것**이다. 코디가 워커 리포트에서 취합했고 출처 바퀴를 각 행에 적었다.

**사용처 5곳 이상인 항목 12건** — 이것부터 보면 된다:

| # | 항목 | 사용처 |
|---|---|---:|
| G-01 | 글꼴 가족이 다르다 (`Pretendard JP` ↔ `Pretendard Variable`) | 앱 전역 |
| G-02 | 폰트 파일이 프로젝트 안에 없다 (원격 CDN) | 앱 전역 |
| G-06 | 엔티티 색 팔레트 `--graph-*` 14종 | 관계 탐색 화면 전면 (런타임 참조) |
| G-14 | 칸반 뷰 · 타임라인 뷰 | 100 (칸반 30 · 타임라인 70) |
| G-15 | 시맨틱 `<table>` 스타일 | 26 |
| G-16 | `--progress-*` 3종 (진행 파랑) | 23 |
| G-13 | `Skeleton` 이 DS 부품이 아니다 | 16 |
| G-07 | `EmptyValue` (인라인 「—」) | 10 |
| G-17 | AX 팔레트 `--ai-*` 8종 + `--shadow-ai` | 10 |
| G-24 | 그림자 5종 → 새 DS 4종 | 10 |
| G-05 | `FieldMessage` 의 톤 구분 | 6 |
| G-10 | `Drawer` 폭 규약 (840 ↔ 520) | 6 |
| G-13 | `Popover` 가 DS 부품이 아니다 | 6 |

---

## 부품

| # | 없는 것 | 어디서 필요한가 (화면 · 사용처 수) | 구 DS 에선 무엇이었나 (파일:줄) | 새 DS 에서 가장 가까운 것 | 네 제안 |
|---|---|---|---|---|---|
| **G-04** | **`ProgressBar`** — 진행률 막대 | 업무 상세 모달의 체크리스트 진행률 · **1곳** (`WorkModals.tsx`) | `src/ProgressBar.tsx` + `styles.css:1390~1396` `.progress-chip` | `components/feedback/CircularCircular` — 무한 스피너라 **진행률을 못 그린다** | **DS 에 추가 요청** — 값 있는 선형 인디케이터 하나. readme 가 「Progress … 의도적으로 없다」고 적었으므로 디자이너 판단이 필요하다 |
| **G-05** | **`FieldMessage` 의 톤 구분** (error / warning / info) | 폼 검증 문구 · **6곳** (`WorkModals.tsx` 2 · `TimeField.tsx` 2 · `Select.tsx` 2) | `src/FormControls.tsx` + `styles.css:254~351` 폼 구획 | 핸드오프 `Field` 의 `.scax-field__hint` — **assistive 회색 한 톤뿐**. `SelectSelect` 에 `errorText` prop 은 있으나 정적 부품이라 못 쓴다 | **DS 에 추가 요청** — `.scax-field__hint--danger` / `--warning` 두 톤. 값은 이미 있는 `--scax-color-danger` / `--scax-color-warning` 을 쓰면 된다 |
| **G-07** | **`EmptyValue`** — 값이 비었을 때의 인라인 「—」 | 표·상세의 빈 셀 · **10곳** (`org/MemberAxesPanel.tsx` 6 · `WorkViews.tsx` 1 · `MyWorkPage.tsx` 1 · `meetings/AgendaBlock.tsx` · `meetings/MeetingListPage.tsx`) | `src/Empty.tsx` 안의 `EmptyValue` | **없음.** `Empty`/`EmptyPage` 는 블록 상태라 셀 안에 못 넣는다. 시안은 대신 리터럴 `—` 를 쓴다(`workspace.v1.jsx` `{row.place \|\| '—'}`) | **DS 에 추가 요청** — 한 줄짜리 토큰화된 표기(`color:var(--scax-color-ink-assistive)`). 없으면 10곳이 각자 `—` 를 하드코딩하게 된다 |
| **G-08** | **`TimeRangeField`** — 시작·끝 시각 한 쌍 | 회의 예약 · 일정 입력 · **2곳** (`ActionMeetingCard.tsx` · `meetings/BookingModal.tsx`) | `src/TimeField.tsx` + `styles.css:1330~1389` | `components/datetime/TimeField` — **단일 시각만.** 쌍을 다루는 부품이 없다 | **DS 에 추가 요청** — `TimeField` 두 개를 묶고 「끝 < 시작」을 막는 래퍼. DS 의 `TimeField` 가 이미 `from`/`to` 를 아니 결이 맞다 |
| **G-09** | **`MultiSelect`** — 다중 선택(칩 표시) | 참석자·참조자 고르기 · **1곳** (`ActionMeetingCard.tsx`) | `src/Select.tsx` 의 `MultiSelect` + `styles.css:1330~1389` | `SelectSelect` 에 `render:"chip"` variant 가 **있으나 정적**. CSS 는 `.scax-person-chips`/`.scax-person-chip` 이 이미 있는데 **그걸 움직이는 JS 부품이 없다** | **DS 에 추가 요청** — CSS 골격이 이미 있으므로 그 위에 얹는 부품 하나. 사다리 ②로 우리가 채울 수도 있으나, 참조자 UI 는 회의·업무 양쪽이 써서 DS 에 두는 편이 낫다 |
| **G-10** | **`Drawer` 폭 규약** — 우리 840px ↔ DS 골격 520px | 자료 미리보기 · 액션 센터 · 조직 접근권 · 업무 상세 · **6곳** (`ActionCenter.tsx` · `WorkModals.tsx` · `meetings/MaterialDrawer.tsx` · `org/AccessDrawer.tsx`) | `src/Modal.tsx` 의 `Drawer` + `styles.css:507~549` (840px, `--shadow-drawer`) | `workspace.css` `.scax-drawer`(**520px**) + `workspace.v1.jsx` `MaterialDrawer`. JS 부품으로는 DS 에 없다 | **새 DS 의 `.scax-drawer` 로 대체 가능** — 골격(오른쪽 슬라이드·head/body/foot·오버레이 32% 먹)은 그대로 쓰고 **폭만 사이즈 variant 로 연다**(`--sm` 520 / `--lg` 840). 업무 상세 드로어는 폼이 두 열이라 520 으로는 좁다 |
| **G-11** | **`ConfirmModal`** (JS 부품) | 삭제·이탈 확인 · **3곳** (`OrgPage.tsx` · `WorkModals.tsx`) | `src/Modal.tsx` 의 `ConfirmModal` + `styles.css:507~549` | `.scax-modal--sm`(420px, `role="alertdialog"`) **CSS 골격만.** `workspace.v1.jsx` 에 인라인으로 한 번 쓰였을 뿐 부품이 아니다 | **DS 에 추가 요청** — 사다리 ② 로 우리가 채울 수도 있으나, 「푸터에 위험 버튼 하나만 두고 취소는 X 로」라는 규약이 시안에 박혀 있어 DS 부품으로 굳히는 편이 안전하다 |
| **G-12** | **`TimeChip`** (JS 부품) | 회의록 줄의 근거 시각 · **1곳** (`meetings/AgendaBlock.tsx`) | `src/TimeChip.tsx` | `workspace.css` `.scax-time-chip` **CSS 만.** `workspace.v1.jsx` 은 `<button className="scax-time-chip">` 인라인 | **새 DS 의 `.scax-time-chip` 으로 대체 가능** — 사다리 ③. CSS 가 완전하고 우리 부품이 하는 일(누르면 스크립트 그 자리로)은 로직이라 우리 것이다 |
| **G-13** | **`Skeleton` · `Popover` · `Toast` 가 DS 부품이 아니다** | Skeleton **16곳** · Popover **6곳** · Toast **2곳** | `src/Skeleton.tsx` · `src/Popover.tsx` · `src/Modal.tsx` | 셋 다 **핸드오프에만 있다**(`scax-ui.jsx` · `work-modal.jsx` + CSS). readme 가 「Snackbar·Popover·Skeleton … 의도적으로 없다」고 적고, Toast 는 「발주본 CSS 에 두었고 DS 컴포넌트로는 아직 안 올렸다」고 적었다 | **DS 에 추가 요청** — 셋 다 이미 핸드오프에 구현·스타일이 다 있다. **DS 로 승격만 하면 된다.** 안 올리면 앱과 DS 의 부품 목록이 영구히 어긋난다 |
| **G-20** | **`MinWidthNotice`** | **0곳** (프로덕션 사용처 없음. 테스트에만 1건) | `src/MinWidthNotice.tsx` + `styles.css:826~910` 반응형 | **없음.** 새 DS 는 `min-width:1542px` 를 깔고 좁은 폭을 다루지 않는다 | **폐기** — 사용처가 0이다. 다만 §8 L-6(최소 폭·페이지 스크롤)이 열려 있어, 좁은 폭 대응을 하기로 하면 이 결정을 되돌려야 한다 |

## 토큰

| # | 없는 것 | 어디서 필요한가 (화면 · 사용처 수) | 구 DS 에선 무엇이었나 (파일:줄) | 새 DS 에서 가장 가까운 것 | 네 제안 |
|---|---|---|---|---|---|
| **G-01** | **글꼴 가족이 다르다** — DS 는 `Pretendard JP`, 앱은 `Pretendard Variable` | **앱 전역** (`styles.css:78` 한 줄이지만 모든 글자에 걸린다) | `styles.css:78` `"Pretendard Variable", Pretendard, -apple-system, …` | `tokens/typography.css` `--font-ui:"Pretendard JP", …` · `--font-display:"Pretendard", …` | **DS 에 추가 요청(확인)** — JP 는 일본어 자형을 포함한 별개 빌드라 한글 자형·폭이 미세하게 달라진다. 디자이너가 **정말 JP 를 의도했는지** 확인이 먼저다. 아니면 `--font-ui` 를 `Pretendard Variable` 로 고쳐 DS 를 갱신한다 |
| **G-02** | **폰트 파일이 프로젝트 안에 없다** | **앱 전역** | 앱은 시스템 설치 폰트에 기댄다. `.design-sync/fonts/PretendardVariable.woff2`(2,057,688 B)가 있으나 **claude.ai/design 렌더 전용**이라고 그 CSS 주석이 밝힌다 | `tokens/fonts.css` 가 **jsDelivr 원격 URL** 로 받는다. `_ds_manifest.json` `fonts[]` 가 `"files": [], "remoteSrc": true` | **DS 에 추가 요청** — DS 에 woff2 를 동봉하거나, 최소한 「앱은 로컬 파일로 바꿔 쓴다」를 규약으로 적어 달라. 그대로 두면 앱이 런타임에 외부 CDN 에 의존한다(사내망·오프라인에서 글꼴이 깨진다) |
| **G-03** | **아이콘 글리프 10종** — `arrow-up` `arrow-down` `sparkle` `paperclip` `folder` / `square` `circle` `ban` `pending` `empty` | 앞 5종은 **살아 있다**: `paperclip` 4 · `arrow-up` 2 · `arrow-down` 2 · `sparkle` 2 · `folder` 2 = **12곳**. 뒤 5종은 **0곳** | `src/Icon.tsx` (30 글리프, viewBox 16, stroke 1.5) | 새 세트 120 글리프. 매핑되는 것: `check-square`→`square-check` · `file`→`document` · `refresh`→`reset` · `alert`→`circle-exclamation` · `filter`→`tune` · `list`→`align-justify`/`list-category`. **위 10종은 대응이 없다** | **살아 있는 5종은 DS 에 추가 요청** — 같은 규칙(24 그리드 · stroke 1.5 · currentColor)으로 그려 달라. DS 는 이미 `play`/`play-fill`/`expand`/`collapse` 를 같은 방식으로 더한 전례가 있다. **`sparkle` 은 DS 의 `agent` 또는 `ai-review` 로 대체 가능한지 디자이너 확인**이 먼저다 |
| **G-03b** | 위 중 **`ban` `pending`** 둘만 | **0곳** | `src/Icon.tsx` | 없음 | **폐기** — 사용처 0. ~~`square`·`circle`·`empty` 도 0곳~~ → **2026-09-13 정정(바퀴 4)**: 셋은 **살아 있다.** `square`(`WorkViews.tsx:138` 체크 토글) · `circle`(`TodayPage.tsx:241` 메트릭) · `empty`(`Empty.tsx:42` 기본 변형)가 전부 **삼항·동적 `name={…}`** 자리라 문자열 검색에 안 잡혔다. 바퀴 4 에서 `square`→`blank` · `empty`→`inbox` 로 DS 이름을 얻었고 `circle` 만 구 글리프로 남았다. **이 셋을 지우면 화면이 깨진다** |
| **G-06** | **엔티티 색 팔레트 `--graph-*` 14종** — `node-person/team/project/work-request/task/material/meeting/report/fallback/dim` · `edge/edge-dim/edge-active/edge-label` · `label` | 관계 탐색 화면 **전면** — `GraphCanvas.tsx:29~36`·`54`·`105~107` 이 `getComputedStyle` 로 **런타임에 읽는다**. 토큰이 없으면 캔버스가 색을 잃는다 | `styles.css:43~56` | **없음.** 새 DS 는 「악센트 하나(violet), 나머지는 전부 중립」이 원칙이라 **범주형 팔레트가 아예 없다**(readme 「One accent … Everything else is neutral」) | **DS 에 추가 요청** — 8종(사람·팀·프로젝트·업무요청·업무·자료·회의·보고) + dim/fallback + 선 3종. DS 의 accent-foreground 계열 12색(`blue`·`cyan`·`green`·`lime`·`orange`·`pink`·`purple`·`red`·`violet`·`light-blue`)에서 고르면 새 값을 만들지 않고도 채울 수 있다 — **어느 종류에 어느 색인지는 디자이너가 정해야 한다** |
| **G-16** | **`--progress-accent` · `--progress-text` · `--progress-tint`** — 진행 상태의 파랑 3종 | 진행 배지·진행 행 · **`styles.css` 23곳** | `styles.css:40~42` (`#33aaff` / `#0079d0` / `#eaf4ff`) | `--scax-color-info`(`--cyan-40` `rgb(0,152,178)`) 하나. **tint(연한 바탕)와 text(진한 글자) 짝이 없다** | **DS 에 추가 요청** — 상태색마다 `soft`(바탕)·`strong`(글자) 짝. DS 는 `--scax-color-danger` 에만 `-soft` 를 뒀는데(`--scax-color-danger-soft`), positive·info·warning 에도 같은 짝이 필요하다 |
| **G-17** | **AX 팔레트 `--ai-*` 8종 + `--shadow-ai`** — `bg-active` `bg-hover` `border` `border-active` `border-hover` `text` `text-active` | AX 채팅 드로어·어시스턴트 · **10곳** (`styles.css` 9 · `org/MemberAxesPanel.tsx` 1) | `styles.css:8~15`, `59` | `--scax-color-accent-05/08/20` 3단 + `--scax-shadow-raised`. **경계선용 중간 단계(`#d5dafb`·`#c3cbfb`·`#a6b0f7`)와 글자용 어두운 단계(`#4b52a8`·`#3a4194`)가 없다** | **DS 에 추가 요청** — accent 의 경계선 2단·글자 2단. 지금 3단(05/08/20)은 바탕 전용이라 AX 표면을 그리면 경계선이 안 보인다 |
| **G-18** | **`--hero-sky-left` · `--hero-sky-right` · `--hero-violet`** | 로그인 화면 배경 · **6곳** (`styles.css:36~38`) | `styles.css:36~38` | 없음. 그라데이션은 DS 에 `--ax-agent-gradient` 하나뿐이고 readme 가 「그것 말고는 그라데이션 없음」이라고 못박는다 | **새 DS 의 `--scax-color-accent-soft` + `--scax-color-surface-alt` 로 대체 가능** — 로그인 배경을 그라데이션에서 단색 두 겹으로 낮춘다. DS 원칙(그라데이션 금지)에 맞추는 쪽이다. 다만 **로그인 인상이 바뀌므로 사용자 확인** 필요 |
| **G-19** | **`--warning-surface` · `--warning-text`** | 경고 배너 · **2곳** (`styles.css`) | `styles.css:62~63` (`#fff4e5` / `#8a5300`) | `--scax-color-warning`(`--orange-50` `rgb(255,146,0)`) 하나. 바탕·글자 짝 없음 | **DS 에 추가 요청** — G-16 과 같은 건이다. 상태색 4종(danger/positive/info/warning)에 `soft`/`strong` 짝을 한 번에 채우면 G-16·G-19 가 같이 닫힌다 |
| **G-24** | **그림자 5종 `--shadow-sm/md/lg/xl/drawer`** | **10곳** (`styles.css`) | `styles.css:57~61` | `--scax-shadow-card` · `-raised` · `-panel` · `-rail` **4종.** 대응은 되지만 값이 다르다(구 것은 `rgba(16,24,40,…)` 계열, 새 것은 `rgba(23,23,23,…)`·`rgba(0,0,0,…)`) | **새 DS 4종으로 대체 가능** — `sm`→`card` · `md`→`raised` · `lg`→`panel` · `xl`→`panel`(더 센 것이 없다) · `drawer`→`rail`. **`xl`(`0 16px 40px rgba(0,0,0,.16)`) 만 새 DS 에 더 센 짝이 없어 시각적으로 얕아진다** — 그것만 확인받는다 |
| **G-23** | **`--status-neutral-tint`** | 중립 상태 배지 바탕 · **3곳** (`styles.css`) | `styles.css:53` (`#f4f5f7`) | `--scax-color-fill-weak`(`rgba(112,115,124,.05)`) — 값이 사실상 같다 | **새 DS 의 `--scax-color-fill-weak` 로 대체 가능** — 그대로 갈아끼우면 된다. 확인만 받는다 |

## 클래스 · 패턴

| # | 없는 것 | 어디서 필요한가 (화면 · 사용처 수) | 구 DS 에선 무엇이었나 (파일:줄) | 새 DS 에서 가장 가까운 것 | 네 제안 |
|---|---|---|---|---|---|
| **G-14** | **칸반 뷰 · 타임라인 뷰** | 업무 화면의 「보기 방식」 · **칸반 30곳 · 타임라인 70곳** (`WorkViews.tsx` · `WorkModals.tsx` · `MyWorkPage.tsx` · `styles.css`) | `styles.css:407~486` 안의 `.kanban-*` 14줄 · `.timeline-*` 28줄 (+ `1049~1065` 요청 타임라인) | **없음.** 시안의 칩 바에는 「보기 방식」 세그먼티드가 들어갈 자리조차 없다 | **DS 에 추가 요청** — 두 뷰를 유지할 거라면 DS 에 자리가 필요하다. **유지 여부 자체가 사용자 결정**이다(§8 로직 항목 L-5). 사용처 100곳이라 조용히 없앨 수 있는 규모가 아니다 |
| **G-15** | **시맨틱 `<table>` 스타일** | 조직 변경 이력·업무 표 등 · **26곳** (`styles.css` 17 · `MyWorkPage.tsx` 4 · `org/ChangeLogPanel.tsx` 2 …) | `styles.css:213~239` 제네릭 표 · `240~253` `.plain-table`(th 44 / td 56) | `.scax-task-table` — **`<table>` 이 아니라 `div` + CSS grid** 이고 6열 트랙이 업무 표에 하드코딩되어 있다. 열 수가 다른 표에는 못 쓴다 | **DS 에 추가 요청** — 열 수에 안 묶인 일반 표 규약 하나(`.scax-table` th/td 높이·경계선·hover). 아니면 「모든 표는 `div` grid 로 다시 짠다」를 규약으로 못박아 달라 — 26곳이 걸리므로 **둘 중 하나는 정해져야 한다** |
| **G-21** | **`AppHeader` 의 breadcrumb 이 「쓰지 않는 것」으로 확정되어 있다** | 회의 상세 → 목록으로 돌아가는 유일한 경로 · **1곳이지만 이동 경로가 끊긴다** (`App.tsx:414~430`) | `styles.css:132~135` `.canvas-topbar` + `.breadcrumb` | `AppHeader` 는 `breadcrumb` prop 을 **받긴 하는데**, `tokens/scax.css` 주석이 「브레드크럼 줄은 두지 않는다 (디자이너 확정)」이라고 못박았고 시안 두 장 다 안 쓴다 | **DS 에 추가 요청(확인)** — 「안 쓴다」가 **모든 화면에 대한 확정인지**, 「업무·회의 화면에서만」인지 확인이 필요하다. 전자면 회의 상세에서 돌아갈 다른 길(§8 L-1·L-2)을 먼저 정해야 한다 |

---

## 바퀴 중 추가로 나온 것 (코디 추가)

| # | 없는 것 | 어디서 필요한가 (화면 · 사용처 수) | 구 DS 에선 무엇이었나 | 새 DS 에서 가장 가까운 것 | 제안 |
|---|---|---|---|---|---|
| **G-25** | **인라인 상태 한 줄** — `<span role="status">` 한 줄, tone `muted`\|`danger`. 회의 스트림 「연결하는 중」 같은 자리 | 회의 라이브·자료 상태 · **7곳** | `src/StatusNote.tsx` | 핸드오프 `StatusNote` 는 **가운데 정렬 오류 블록**(붉은 48px 원 + title/desc/action, `role="alert"`)이다. 겹치는 건 이름뿐이고 **`tone=muted` 에 대응이 없다** | **DS 에 추가 요청** — 블록형 옆에 「인라인 한 줄」 변형 하나. 조용한 진행 상태(muted)와 오류(danger)를 같은 크기로 쓰는 자리가 있다 |
| **G-26** | **2단 메타 목록** — 왼쪽 고정 메타칸 + 본문이 줄마다 짝을 이루는 목록 | 회의 원문·활동 기록 · **3곳** | `src/GutterList.tsx` | 핸드오프에 같은 이름 `GutterList` 가 있으나 **레일 목록**(머리 + 스크롤 본문 + inbox 아이콘)이라 다른 부품이다 | **DS 에 추가 요청** — 아니면 「원문·이력은 어떤 꼴로 세우나」를 규약으로 정해 달라. 핸드오프 쪽은 바퀴 6 의 회의 좌측 레일에 쓰인다(그건 별개로 필요) |
| **G-27** | **스켈레톤의 「0.4초 규칙」** — 짧은 로딩에는 아무것도 띄우지 않는 `animation-delay:0.4s` | 로딩 표시 전역 · **16곳** | `styles.css` 의 `.skeleton-bar{animation:skeleton-appear 0s linear .4s forwards}` | `.scax-skeleton` 은 **지연 없이 곧바로 맥동한다** | **DS 에 추가 요청(확인)** — 지연을 뺀 것이 의도인지 확인이 먼저다. 의도가 아니면 `.scax-skeleton` 에 지연을 넣어 달라. 깜빡임을 막던 규칙이라 16곳이 동시에 영향을 받는다 (바퀴 3a 에서 소실) |
| **G-28** | **인라인 텍스트 링크 버튼** — 문장 안에 들어가는 글자 단추 | 전 화면 · **22곳** | `styles.css` 의 `.btn.link` | `.scax-button--text-neutral` 은 **높이 39 + 좌우 여백**이라 문장 안에 못 들어간다 | **DS 에 추가 요청** — 높이·여백 없는 인라인 변형 하나. 22곳이라 **바퀴 9 에서 구 `styles.css` 를 못 지우는 가장 큰 덩어리**다 (바퀴 3c) |
| **G-29** | **테두리형 배지** — 흰 바탕 + 테두리 | 상태 표시 · **12곳** | `styles.css` 의 `.badge.outline` | `.scax-badge--neutral` 은 **회색 채움**이다. 접으면 이미 쓰는 채움형 neutral 7곳과 **화면에서 똑같아진다** | **DS 에 추가 요청** — 채움형과 **구분되어야 하는 상태**다. 시각 차이가 아니라 의미 차이 (바퀴 3c) |
| **G-30** | **클래스 기반 datetime 부품** — `DateField`·`DatePicker`·`TimeField` | 날짜·시각 입력 · **테스트 14건이 걸린 상호작용** | `src/DateField.tsx` · `DatePicker.tsx` · `TimeField.tsx` (`role="grid"` · 방향키 · min/max · 포커스 복귀 · 「지우기·오늘」 푸터) | DS `components/datetime/` 3종은 **`className` 이 하나도 없고 전부 인라인 스타일**이다. 리포트 §9 의 「1:1」은 **props 이야기**였고 구현 수준에서는 「껍데기만 갈기」가 성립하지 않는다 | **DS 에 추가 요청** — 클래스 기반으로 다시 내 달라. 지금 것을 통째로 쓰면 방향키·`role=grid`·min/max·포커스 복귀와 「지우기·오늘」 푸터를 잃고, 상호작용이 팝오버식에서 타이핑식으로 바뀌며, 167KB 아이콘 세트가 따라온다 (바퀴 3b) |

---

## 바퀴 7 (AX 드로어) — 9건

| # | 없는 것 | 어디서 (곳) | 구 DS | 새 DS 에서 가장 가까운 것 | 워커 제안 |
|---|---|---|---|---|---|
| **G-32** | **타입 램프에 16px 이 없다** | 3 — 드로어 머리 제목 · 답변 첫 강조 제목 · 시작 프롬프트 `＋` | `font-size:16px` | `body1`(15) 또는 `headline`(17) — **둘 다 1px 어긋난다** | `headline`(17)로 올렸다. 채팅 제목이 본문(14)과 구별돼야 해서 위쪽. DS 에 `--t-body2`(16) 한 칸 추가할지 결정 |
| **G-33** | **타입 램프에 9·10px 이 없다** (최소 `caption2`=11) | **12** — 실행 레일 단계 시간·도구 코드·요약 메타·「보기/접기」·근거 6종·후속 꼬리말·알림 시각·히스토리 부제 | `9px`·`10px` | `caption2`(11) | 전부 11로 올렸다 — 레일이 조금 커진다. 「조용한 부속」용 `caption3`(10)이 필요한지 결정. **급하지 않음** |
| **G-34** | **타입 램프에 20px 이 없다** (최대 `title`=18) | — | `20px` | `title`(18) | 18로 내렸다 |
| **G-35** | **`Badge` 에 경고(주황) 톤이 없다** | 2 — 업무 카드 「요청」 · 「답변 뒤 바뀜」 | 「요청」 `#ff5d00` on `#fff3eb` · `--warning-text`/`--warning-surface` | 톤 5종(accent·neutral·danger·positive·info) — **주황 없음** | 「요청」은 `accent`(보라)로 옮겼다 — **색 뜻이 바뀐다(주황=대기 → 보라=AX). 확인 필요.** 「답변 뒤 바뀜」은 구 토큰 그대로 남겼다. `Badge` 에 `warning` 톤을 열거나 `--scax-color-warning-surface` 를 올려 달라(`--scax-color-warning` 은 글자색 하나뿐이라 면색 짝이 없다) |
| **G-36** | **`Empty` 가 아이콘을 prop 으로 안 받는다** | 4 — 첨부 찾기 빈 상태 넷 | `.attachment-picker-empty` + `<Icon name="search">` | `Empty` 가 `variant` 로 아이콘을 **고른다**(default→inbox·filter→tune·error→circle-exclamation) | `variant="default"` 로 갔다 — **검색 판인데 받은편지함 아이콘이 뜬다.** `icon?: IconName` 하나 여는 게 가장 작은 수정 |
| **G-37** | **`Empty` 가 「불러오는 중」을 못 말한다** | 1 — 「검색 중…」 | 같은 컨테이너를 문구만 바꿔 재사용 | `Empty`(비었다)/`StatusNote`(못 불러왔다)/`Skeleton`(로딩) **셋 다 안 맞는다** — 판은 있고 안이 아직 안 찬 상태 | `Empty` 로 뒀다. `Skeleton` 으로 가면 「검색 중」이라는 말이 사라진다. `busy?: boolean` 이 필요한지 결정 |
| **G-38** | **간격 램프에 없는 값 9종** (`5·7·9·11·13·14·19·34·42`) | 14 | 램프 없이 리터럴 | `--scax-space-*` 11단(2/4/6/8/10/12/16/20/24/32/48) — 홀수 없음 | 간격은 램프에 스냅(5→6·7→6·9→8·11→10·13→12), **구조 치수**(레일 들여쓰기 19/20·검색칸 42·아이콘 34)는 리터럴로 뒀다. **그대로 두는 쪽 권함** |
| **G-39** | **화면에 「붙는」 드로어 변형이 없다** | 1 — AX 드로어 | `.ax-drawer{position:fixed;right:0}` | `.scax-drawer` 는 **스크림 있는 모달** 전제 | `.scax-drawer--chat` 4속성으로 해결. DS 에 「스크림 없는 상주 드로어」 변형이 필요한지 — **회의 워크스페이스도 같은 모양을 쓸 것 같다** |
| **G-40** | **작은 점 배지가 없다** | 1 — 알림 안 읽음 점(6px) | `.ax-notification-dot` | `.scax-badge--count` 는 숫자를 담는 18px 원이다. 「점」이 아니다 | 6px 점을 파일에 남겼다. **급하지 않음** |

## 바퀴 8-A (로그인·홈·일일보고·프로젝트) — 1건 + 1건 부분 닫힘

| # | 없는 것 | 어디서 (곳) | 구 DS | 새 DS 에서 가장 가까운 것 | 워커 제안 |
|---|---|---|---|---|---|
| **G-41** | **18px 위의 제목 단이 없다** | 5 — 리터럴 px 로 남겼다 | 화면 제목들 | 타입 램프가 `title` 18 에서 끝난다 | 램프에 `page-title` 한 칸을 더할지 결정 (G-44 와 같은 건) |
| **G-16** | ~~진행 파랑 tint/text 짝 없음~~ | — | — | — | **배지 한정으로 닫힘** — `components.css:179` 의 `.scax-badge--info` 가 바탕 `rgba(0,116,204,.08)` + 글자 `--scax-color-info` 를 이미 갖고 있다. **배지 「밖」 자리에는 그대로 열려 있다** |

## 바퀴 8-B (조직·관계탐색·캘린더) — 6건

| # | 없는 것 | 어디서 (곳) | 구 DS | 새 DS 에서 가장 가까운 것 | 워커 제안 |
|---|---|---|---|---|---|
| **G-06** | **범주형 팔레트** (재확인) | 3 — `GraphCanvas` 노드 8색 + 필터칩·범례 색점 | `--graph-*` 14종 | **없다.** status 6색은 *상태*지 *범주*가 아니고 8종을 구별 못 한다. 「악센트 하나, 나머지 중립」과 정면 충돌 | 구 14종 **그대로 유지**. 셋 중 사용자가 골라야 한다 — (a) DS 에 범주 축 신설 (b) 그래프만 예외 팔레트로 공인 (c) 노드 색 버리고 모양·크기로 구별 |
| **G-42** | **status 의 soft 배경이 danger 하나뿐** | 1 — 캘린더 업무 막대 4상태, **앞으로 늘어난다** | `--progress-tint`·`--selected-bg`·`--danger-tint`·`--status-neutral-tint` 4벌 | `--scax-color-danger-soft` **하나뿐** | 없는 tint 를 지어내지 않았다. 바탕은 `fill-weak`/`accent-08`/`danger-soft` 셋으로만 말하고 뜻은 **왼쪽 3px 선 + 글자색**이 지게 했다. status 램프에 `-soft` 4종 신설 제안 |
| **G-43** | **글자 아바타(이니셜 원)** | `org/` **12** + 로그인·홈·업무·액션·회의 등 다수 | `.avatar` + `xs~xl` 5단 | `.scax-side-nav__avatar`·`.scax-person-chip__avatar` — 둘 다 **사진(`object-fit:cover`) 전제**. 글자 변형도, 크기 5단도 없다 | 구 `.avatar` 를 남기고 세 패널 안에서만 새 토큰으로 다시 칠했다. **바퀴 9 이전에 닫아야 한다** — 구 파일이 통째로 사라진다 |
| **G-44** | **28px 화면 제목이 램프 밖** | 3(제거함) + `ProjectPage`·`DailyReportPage` 잔여 | `.page-head h1{font-size:28px}` | 램프가 `title` 18 에서 끝난다 | 중복 h1 을 걷어내 이 바퀴에선 필요가 사라졌다. 남은 화면도 같은 처리가 맞는지, 램프에 `page-title` 한 칸을 더할지 결정 (G-41 과 같은 건) |
| **G-45** | **여러 줄 입력(textarea)** | 1 — `org/AccessDrawer` 사유 칸 | `.field textarea` | `.scax-textfield` 는 한 줄. `.scax-composer` 는 채팅 어휘(보내기·글자 수)라 폼 필드가 아니다 | 폼용 textarea 변형 신설 제안 |
| **G-46** | **값을 읽는 표(semantic `<table>`)** (G-15 재확인) | 1 + `.plain-table` 공유 4곳 | `.plain-table` | `.scax-task-table` 은 **업무 표 전용 div-grid**(`__row`·`__due`·`__resolved`). 5열 읽기 표를 못 담고, 테스트도 `querySelector("table")` 를 요구한다 | `<table>` 유지하고 자기 표 안에서만 다시 겨눴다. 범용 데이터 표 부품 신설 제안 |

---

## 사용자가 판단할 것 — 요약

| 묶음 | 항목 | 성격 |
|---|---|---|
| **먼저 닫혀야 바퀴 1 이 돈다** | G-01 · G-02 (폰트) | 바퀴 1 이 `tokens/fonts.css` 를 실을지 말지가 여기서 갈린다 |
| **바퀴 3(프리미티브) 전에** | G-04 · G-05 · G-07 · G-08 · G-09 · G-11 · G-13 · G-15 | 부품 한 벌을 만들 때 같이 채워야 두 번 안 만든다 |
| **바퀴 4(아이콘) 전에** | G-03 · G-03b | 글리프 이름 매핑표를 확정해야 한다 |
| **바퀴 5(업무 화면) 전에** | G-14 (칸반·타임라인 유지 여부) | §8 L-5 와 같은 건 |
| **바퀴 6(회의 화면) 전에** | G-21 (breadcrumb) | §8 L-1·L-2 와 같은 건 |
| **바퀴 7·8 전에** | G-06 · G-16 · G-17 · G-18 · G-19 · G-23 · G-24 (토큰) | 관계 탐색·AX 드로어·로그인이 이 토큰들 위에 서 있다 |
| **되돌릴 수 있음** | G-10 · G-12 · G-20 | 대체·폐기 제안이라 결정이 늦어도 바퀴가 막히지 않는다 |
| **바퀴 중 나온 것** | G-25~G-30 |
| **바퀴 9(은퇴) 전에 반드시** | **G-43 이니셜 아바타** — 구 `.avatar` 가 사라지면 12곳+ 이 깨진다. **가장 급하다** |
| **색 뜻이 바뀐 것 — 확인 필요** | **G-35** 업무 카드 「요청」이 주황(대기) → 보라(AX)로 바뀌었다 |
| **작은 부품 하나만 열면 닫히는 것** | G-36 `Empty.icon` · G-37 `Empty.busy` · G-35 `Badge warning` · G-39 상주 드로어 변형 |
| **그대로 두는 쪽 권함** | G-38 간격 리터럴 · G-40 점 배지 | G-27 은 이미 동작이 사라진 상태다(스켈레톤 깜빡임). 나머지 둘은 구 부품을 남겨 둬서 지금 깨진 건 없다 |
