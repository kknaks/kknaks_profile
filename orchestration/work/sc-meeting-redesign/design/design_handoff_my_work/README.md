# Handoff: 「내 업무」 화면 + SCAX 디자인 시스템 교체

## 개요
SCAX 업무 홈(「내 업무」) 화면의 구현 발주본이다. 좌측 전역 내비게이션, 페이지 헤더(브레드크럼·제목·액션), 3구획 본문(수신함 레일 · 업무 테이블 · 캘린더 레일), 우하단 AI 에이전트로 구성된다. **이 화면에서 확정한 페이지 틀은 이후 모든 SCAX 화면이 공통으로 쓴다.**

이 번들은 화면 하나만 담고 있지 않다. **디자인 시스템 쪽 변경(아이콘 세트 교체 + 토큰 별칭 계층)도 함께 반영해야 한다.** 아래 「디자인 시스템 변경」 절이 그 작업이다.

## 이 번들의 파일 성격
`design/` 안의 HTML·CSS·JSX 는 **디자인 레퍼런스**다. 의도한 모양과 동작을 보여주는 프로토타입이며, 그대로 제품에 올리는 코드가 아니다. 할 일은 이 디자인을 **대상 코드베이스(React 19 + Vite, 외부 UI 라이브러리 없음, CSS 변수 토큰 + 일반 CSS, 자체 컴포넌트)의 기존 패턴으로 재구현**하는 것이다.

다만 CSS 는 의도적으로 이식 가능하게 작성했다: 유틸리티 클래스·인라인 스타일·프레임워크 클래스명이 없고, 모든 값이 `--scax-*` CSS 변수를 참조하는 일반 CSS 클래스다. 클래스명(`scax-<블록>__<요소>--<변형>`)을 그대로 제품 CSS 클래스로 써도 된다.

프리뷰 런타임만 React 18 UMD + 브라우저 Babel 이다(단일 파일 로딩 제약 때문). 컴포넌트 코드 자체는 평범한 함수형 컴포넌트 + 훅이라 React 19 에서 수정 없이 동작한다.

## 충실도
**하이파이(hifi)** — 색·타이포·간격·라운드·그림자 값이 모두 디자인 시스템 원본에서 읽은 확정값이다. 픽셀 단위로 재현해야 한다. 아래 수치는 전부 실측값이며 임의 조정 금지.

---

## 디자인 시스템 변경

### 1) 아이콘 세트를 선(stroke) 글리프로 교체 — 필수
기존 아이콘 데이터는 선을 면으로 변환한(traced outline-as-fill, `fill-rule: evenodd`) 패스여서 20px 이하에서 형태가 뭉개졌다. 116개 글리프를 **24px 그리드 선 지오메트리**로 교체했다.

- 참조 파일: `ds/Icon.jsx.txt` (글리프 맵이 파일 안에 인라인되어 있다), `ds/Icon.d.ts.txt` — 이 프로젝트의 컴파일러가 참조본을 컴포넌트로 오인하지 않도록 `.txt` 를 붙였다. 코드베이스에 넣을 때 `.txt` 를 떼면 된다.
- 렌더 규약: `fill: none` / `stroke: currentColor` / `stroke-width: 1.5` / `stroke-linecap: round` / `stroke-linejoin: round` / `viewBox="0 0 24 24"`
- `*-fill` 이름은 같은 지오메트리를 `fill: currentColor` 로 칠한다.
- `*-thick` 이름은 같은 지오메트리에 `stroke-width + 0.5`.
- `strokeWidth` prop 으로 굵기를 올릴 수 있다(기본 1.5).
- 글리프 지오메트리 출처는 **Lucide (ISC 라이선스)** 이며 SCAX 아이콘 이름에 매핑했다. 코드베이스에 `lucide-react` 를 넣는 편이 낫다면, `ds/Icon.jsx.txt` 상단의 이름 매핑을 그대로 옮겨 `lucide-react` 를 감싸면 동일 결과가 나온다 — 단 **아이콘 이름표(`name` prop 값)는 SCAX 이름을 유지**해야 화면 코드가 안 바뀐다.
- 주의: 글리프 맵을 **별도 모듈로 분리하지 말 것**. 컴포넌트 파일 안에 두거나 `lucide-react` 를 감싸는 두 방식만 검증했다.

사용 가능한 이름은 `ds/Icon.d.ts.txt` 의 `IconName` 유니온(120개)이 정본이다. 선 세트에 없는 4개 이름은 옛 데이터로 폴백한다.

### 2) 토큰 별칭 계층 `--scax-*` 추가 — 필수
DS 원본 변수(`--violet-50`, `--cool-neutral-99`, `--label-normal`, `--ax-*` …)를 화면 코드가 직접 참조하지 않는다. `design/css/tokens.css` 가 그 사이에 **의미 기반 별칭 한 겹**을 만든다. 컴포넌트 CSS 는 `--scax-*` 만 참조한다.

- `design/css/tokens.css` 를 `src/styles/tokens.css` 로 옮기고, 맨 위 `@import "../../../styles.css"` 를 사내 DS 패키지의 전역 스타일시트 경로로 바꾼다.
- DS 의 간격 토큰(`--space-*`, `--spacing-*`)은 Figma 에서 온 **단위 없는 숫자**여서 CSS 에서 바로 못 쓴다. `--scax-space-*` 가 px 로 변환한 계층이다(2·4·6·8·10·12·16·20·24·32·48px).
- 참조용 DS 원본: `ds/product.css`(제품 레벨 별칭), `ds/typography.css`(타입 램프 + `.ax-*` 클래스), `ds/fig-tokens.css`(원시 토큰 592개).

### 3) 토큰 목록
| 계열 | 이름 |
|---|---|
| 색 | `--scax-color-accent` `-accent-strong` `-accent-soft` `-accent-05/-08/-20` · `-ink-strong` `-ink` `-ink-neutral` `-ink-alt` `-ink-assistive` `-ink-disabled` `-ink-inverse` `-ink-nav-idle` `-ink-nav-active` · `-surface` `-surface-alt` `-surface-nav` `-surface-nav-active` `-surface-nav-hover` `-surface-inverse` · `-line-weak` `-line` `-line-strong` `-fill-weak` `-fill` `-fill-strong` · `-danger` `-danger-soft` `-positive` `-info` `-warning` |
| 간격 | `--scax-space-050`(2) `-100`(4) `-150`(6) `-200`(8) `-250`(10) `-300`(12) `-400`(16) `-500`(20) `-600`(24) `-800`(32) `-1200`(48) |
| 라운드 | `--scax-radius-xs`(6) `-sm`(8) `-md`(10) `-lg`(12) `-xl`(14) `-2xl`(15) `-pill`(999) |
| 타이포 | `--scax-font-ui`(Pretendard JP) `--scax-font-display`(Pretendard) · `--scax-fw-regular/medium/semibold/bold`(400/500/600/700) · `--scax-text-{caption2,caption1,label2,label1,body1,headline,title}-{size,lh,ls}` |
| 그림자 | `--scax-shadow-card` `-raised` `-panel` `-rail` · `--scax-ring` `-ring-weak` |
| 상태 오버레이 | `--scax-state-hover`(.05) `-focus`(.08) `-press`(.12) — 잉크는 항상 `--scax-color-ink` |
| 프레임 | `--scax-nav-width`(180) `-nav-width-collapsed`(65) `--scax-header-height`(72) `--scax-rail-left-width`(380) `--scax-rail-right-width`(342) `--scax-content-min-width`(640) `--scax-table-min-width`(880) `--scax-control-height-sm`(32) `-md`(39) `--scax-row-height`(50) `--scax-focus-ring` `--scax-duration-fast`(120ms) `--scax-easing` |

타입 램프 실측값: caption2 11/1.273/0.031em · caption1 12/1.334/0.025em · label2 13/1.385/0.019em · label1 14/1.467/0.010em · body1 15/1.5/0.006em · headline 17/1.412/0em · title 18/1.445/0em.

---

## 컴포넌트 트리

```
AppShell
├─ SideNav 「신규」                       (DS: Navigation/max)
└─ AppMain
   ├─ PageHeader 「신규」                 breadcrumb + h1 + actions
   │  └─ Button ×2                       일일보고 생성(outlined) / 업무 만들기(solid)
   └─ PageBody 「신규」
      ├─ rail-left  : InboxRail
      │   └─ GutterList
      │      ├─ SegmentedControl 「신규」  전체 / 업무 / 참고
      │      ├─ Badge(count)
      │      └─ InboxCard 「신규」 ×N      (DS: InboxTask / InboxNotice)
      │         ├─ Badge, IconButton, ButtonGroup > Button ×2
      │         └─ Empty / Skeleton / StatusNote  ← 상태별 대체
      ├─ content    : TaskPanel
      │   ├─ Tabs 「신규」                 내 업무 / 보낸 업무 / 완료 업무
      │   ├─ Chip 「신규」 ×4 (DS: Category/Chip) + Button(WBS 보기)
      │   └─ TaskTable 「신규」            (DS: TaskTable)
      │      ├─ IconButton(star), Badge, Select(상태) > Popover, Button ×2
      │      └─ Empty / Skeleton ×6 / StatusNote  ← 상태별 대체
      └─ rail-right : CalendarRail 「신규」 (DS: WorkCalendar)
          ├─ SegmentedControl, Badge
          └─ Empty / Skeleton / StatusNote  ← 상태별 대체
AgentBubble 「신규」                      (DS: AI floating button)
```

기존 부품 그대로: `Icon` `Button` `Badge` `Select` `Popover` `GutterList` `Empty` `StatusNote`.
이 화면에서 안 쓰는 기존 부품: `Modal` `DateField` `DatePicker` `TimeField` `Composer` `DropZone` `FileList`.
신규 부품: `AppShell` `SideNav` `PageHeader` `PageBody` `SegmentedControl` `Tabs` `Chip` `InboxCard` `TaskTable` `CalendarRail` `AgentBubble` `Skeleton` `IconButton` `ButtonGroup`.

## 페이지 틀 규칙 (이후 모든 화면 공통)
1. `AppShell` = `SideNav`(180px 고정, 접으면 65px) + `AppMain`.
2. `PageHeader` 72px: 좌측 breadcrumb(12px, assistive) → `h1`(18px/600) 2행, 우측 액션. 하단 1px `--scax-color-line`.
3. `PageBody` 3구획: 좌 레일 380px(선택) · 본문 가변(`min-width: 640px`) · 우 레일 342px(선택). 레일 없는 화면은 본문만.
4. 스크롤은 각 구획 내부(`overflow-y: auto`)에서만. 페이지 전체 세로 스크롤 없음.
5. 최소 폭 **1542px** = 180 + 380 + 640 + 342. 업무 테이블은 고정 트랙(44+120+140+120+200) + 좌우 24px 패딩 때문에 `min-width: 880px` 을 가지며, 본문이 그보다 좁아지면 테이블이 찌그러지지 않고 본문 구획이 가로 스크롤한다.

## 화면 상세

### SideNav (180px / 접으면 65px)
- 패딩 16px 12px(접으면 좌우 8px), 배경 `--scax-color-surface-nav`, 우측 1px `--scax-color-line-weak`.
- 프로필: 아바타 40px 원형(접으면 32px) + 이름 `유하람님`(14px/600) + 역할 `기획자`(12px, assistive) + 접기 버튼(28px, `left-side` 아이콘).
- 메뉴 행: 높이 38px, 라운드 8px, 아이콘 20px + 라벨 14px/500, 간격 10px. idle `--scax-color-ink-nav-idle`(rgb(118,118,118)), hover 배경 `--scax-color-surface-nav-hover`(rgb(235,242,253)), active 배경 검정 + 흰 글자.
- 1그룹: 알림(`bell`) · 설정(`setting`). 구분선 1px. 2그룹: 홈(`home`) · 업무(`square-check`, active) · 캘린더(`calendar`) · 회의(`persons`) · 채팅(`chat`) · 수신함(`inbox`) · 진행 현황(`arrow-right`) · 자료(`document`).
- 하단: `LOGO`(17px/700, Pretendard) + `v1.0`(11px, assistive). 접으면 `L` 만.
- **접기 동작**: 상태 1개(`navCollapsed`). 접으면 라벨·역할·버전을 DOM 에서 제거하고(숨김이 아니라 제거) 폭을 `--scax-nav-w` 변수로 65px 로 전환, 메뉴 행은 아이콘 가운데 정렬, 아이콘에 `title` 툴팁. ⚠️ `width`/`flex-basis` 에 transition 을 걸면 var() 변경이 반영되지 않는다 — 트랜지션 금지.

### PageHeader (72px)
breadcrumb `업무 / 내 업무`, 제목 `업무`, 우측 `일일보고 생성`(outlined-primary, 39px) · `업무 만들기`(solid-primary, 39px). 버튼 라운드 10px, 14px/600.

### 수신함 레일 (380px)
- `GutterList`: 패딩 20px 24px, 헤더 32px(아이콘 24px + `수신함` 15px/500 + 카운트 배지 18px 원형 `--scax-color-danger` 흰 숫자 11px) + 우측 `SegmentedControl`.
- `SegmentedControl`: 배경 `--scax-color-fill-weak`, 패딩 2px, 항목 28px/라운드 6px, 선택 항목 흰 배경 + `--scax-shadow-card`.
- `InboxCard`: 패딩 **12px**, 라운드 14px, 1px `--scax-color-line`, `--scax-shadow-card`. 내부 세로 간격 — 본문 블록 **8px**, 본문↔버튼행 **16px**. 메타행 간격 6px.
  - 배지(업무=accent 08% 바탕/accent 글자, 참고=fill-weak/ink-alt) 22px, 라운드 6px, 12px/500.
  - 제목 15px/600, 본문 발췌 13px/1.62 assistive, 2줄 말줄임.
  - 메타: 아바타 20px 원형 · 이름(12px/500 neutral) · 1px 세로 구분선(높이 10px) · 날짜 · 출처 아이콘 16px + 라벨 + `external-link` 12px.
  - 버튼 2개 균등 분할(`ButtonGroup`, gap 8px), 39px, outlined.
- 카드 3장: ①업무 `8월 매출 자료 오늘까지 보내주세요.` / 내 업무로 · 답장 ②참고 `[9월 정산 자료 취합]에 참조로 걸렸습니다` / 원문 확인하기 · 확인완료 ③참고 `[사내 공지] 추석 연휴 근무 안내` / 원문 확인하기 · 확인완료.

### 업무 테이블 (본문)
- `Tabs`: 항목 높이 52px, 17px, 선택 시 600 + 하단 2px 검정 인디케이터, 하단 1px 라인.
- 칩 바: 패딩 16px 24px, 칩 32px/라운드 6px/13px, 선택 칩 검정 배경 + 흰 글자. 우측 끝 `WBS 보기`(outlined-neutral, sm).
- 그리드(헤더·행 공통): `44px minmax(0,1fr) 120px 140px 120px 200px`, 좌우 패딩 24px.
- 헤더: 높이 **35px**, 배경 `--scax-color-surface-alt`(rgb(247,247,248)), 상·하 1px `--scax-color-line-weak`, 13px/500 assistive. `제목/종류 · 요청자 · 기한 · 상태 · 액션`.
- 행: 최소 높이 **50px**, 흰 배경, 하단 1px `--scax-color-line-weak`, hover 배경 `--scax-color-accent-05`.
- 별: `IconButton` (`star` / `star-fill`), 켜짐 `--scax-color-accent`.
- 제목 14px/500 + 종류 배지. 미읽음 행은 제목 왼쪽에 4px 빨강 점.
- 기한 `09-10`, 초과분 `+1` 은 `--scax-color-danger` 12px/500.
- 상태 `Select`: 트리거 26px/라운드 6px, accent 08% 바탕 + accent 글자 + `caret-down` 12px. 옵션 `진행 중`(accent) · `막힘`(danger) · `완료`(positive). 메뉴는 `Popover`(라운드 8px, `--scax-shadow-raised`, 바깥 클릭·Esc 로 닫힘).
- 액션 칼럼: **2등분 고정 그리드**(`repeat(2, minmax(0,1fr))`, gap 8px) — 행마다 버튼 시작 위치가 동일해야 한다. 버튼 높이 36px, 라운드 8px, 14px/500. 첫 버튼 outlined-primary, 둘째 outlined-neutral.
- 행 데이터: ①`8월 정산 자료 정리`＋`완료 확인` / 홍길동 / 09-10 +1 / 확인·보완 요청 (별 켜짐) ②`8월 정산 자료 정리`＋`담당 변경` / 홍길동 / 09-10 / 수락·거절 (미읽음) ③`예외 승인 건`＋`결정 요청`(danger 배지) / 홍길동 / 09-10 / 수락·거절 ④~⑨ `Task name here` / `-` / 09-10 / 액션 없음.

### 캘린더 레일 (342px)
- 패딩 20px 24px, 섹션 간격 **10px**. 헤더 `캘린더`(15px/500) + `SegmentedControl`(오늘 · 주 · 월).
- 날짜 블록 가운데 정렬: `9월 7일 월요일`(18px/600), 아래 `근무 시간`(아이콘 `clock` 16px + 라벨) ↔ `09:00 - 18:00` 간격 **32px**.
- `AgendaItem`: 패딩 **12px**, 라운드 14px, 1px line, 내부 간격 8px. 배지(회의=positive, 업무=accent) + 우측 시간(12px assistive) / 제목 14px/500 / 부제 12px assistive. hover 시 테두리 accent-20 + 배경 accent-05.
- 항목 3개: 회의 14:00-15:00 `거래처 미팅` / 업무 14:00-15:00 `8월 정산 마감` `2026.10.10 까지` ×2.

### AgentBubble
우하단 고정(right·bottom 24px). 말풍선: 최대 165px, 패딩 8px 16px, 라운드 15px, 검정 배경 + 흰 글자 14px, `--scax-shadow-raised`, 문구 `홍길동님  업무 시작 전\n일정을 정리해드릴까요?`(줄바꿈 유지). 아래 그라디언트 타원(120×70px, `--scax-gradient-agent`) + 오브 이미지 100px(`assets/ai-agent-orb.png`, `transform: scaleX(-1)`).

## 상태 (4종, 화면 하단 스위처로 전환 — 스위처는 프리뷰 전용이므로 구현 시 삭제)
| 상태 | 좌 레일 | 본문 | 우 레일 |
|---|---|---|---|
| 기본 | 카드 3 | 행 9 | 일정 3 |
| 비어 있음 | `Empty` | `Empty` | `Empty` |
| 로딩 | `Skeleton--card` ×3 | `skeleton-row` ×6 (헤더 유지) | `Skeleton--agenda` ×3 |
| 오류 | `StatusNote` + 다시 시도 | `StatusNote` + 다시 시도 | `StatusNote` + 다시 시도 |

- `Empty`: 48px 원형 아이콘(fill-weak 바탕) + 제목 14px/600 + 설명 13px assistive, 가운데 정렬.
- `StatusNote`: 같은 구조에 아이콘 바탕 `--scax-color-danger-soft` + `circle-exclamation`, `role="alert"`.
- `Skeleton`: `--scax-color-fill-weak`, 1.2s 펄스(opacity 1 ↔ .45).
- 상태 전용 신규 문구: 「새로운 수신 항목이 없습니다 / 업무·참고 알림이 도착하면 여기에 표시됩니다.」 「표시할 업무가 없습니다 / 새 업무를 만들거나 수신함에서 업무로 옮겨 보세요.」 「등록된 일정이 없습니다」 「…을 불러오지 못했습니다」 「다시 시도」. **그 외 모든 문구는 현재 화면과 동일하며 바꾸지 말 것.**

## 상태 관리
- `screenState: 'default' | 'empty' | 'loading' | 'error'` — 실제로는 데이터 페치 상태에서 파생(프리뷰에서는 스위처로 강제).
- `navId`(활성 메뉴) · `navCollapsed`(사이드바 접힘) · `inboxFilter`(전체/업무/참고) · `inboxItems`(확인완료 시 제거) · `tab`(내 업무/보낸 업무/완료 업무) · `taskFilter`(칩) · `rows`(별·상태·수락/거절 결과) · `range`(오늘/주/월).
- 데이터 페치 3건이 독립적이다: 수신함 목록 · 업무 목록(탭·필터별) · 일정(범위별). 각 구획이 자기 로딩/오류를 따로 그린다.

## 동작 범위
화면 내부에서 완결되는 것만 구현되어 있다: 별 토글 · 상태 `Select` 변경 · 수신함 `확인완료` 제거 · 행의 `확인/보완 요청/수락/거절`(결과 라벨로 치환) · 탭·칩·세그먼티드·사이드 메뉴 선택 · 사이드바 접기.
화면 밖으로 나가는 버튼(`일일보고 생성` `업무 만들기` `답장` `원문 확인하기` `WBS 보기` `업무로 추가`)은 마크업만 있고 핸들러가 비어 있다 — **라우팅은 개발 단계에서 연결한다. 없는 기능을 새로 만들지 말 것.**

## 접근성
- 메뉴 행 `aria-current="page"`, 접기 버튼 `aria-expanded` + `aria-label`(접기/펴기 전환).
- 탭·세그먼티드 `role="tablist"/"tab"` + `aria-selected`, 칩 `aria-pressed`, 별 `aria-pressed` + `aria-label`.
- `Select` 트리거 `aria-haspopup="listbox"` + `aria-expanded`, 옵션 `role="option"` + `aria-selected`. `Popover` 는 바깥 클릭·Esc 로 닫힌다.
- 포커스 링 `--scax-focus-ring`(accent 20% 3px). 아이콘은 `aria-hidden`.
- 오류 영역 `role="alert"`, 스켈레톤 `aria-hidden`.

## 에셋
- `assets/avatar-person.png` — 프로필·수신함 발신자 아바타
- `assets/avatar-company.png` — 총무팀 아바타
- `assets/ai-agent-orb.png` — AI 에이전트 오브 (좌우 반전해서 사용)
- 아이콘은 별도 이미지 없음 — `ds/Icon.jsx.txt` 의 선 글리프.
- 폰트: Pretendard JP(본문) / Pretendard(로고). 사내에서 호스팅하는 웹폰트로 교체할 것.

## 파일
| 경로 | 내용 |
|---|---|
| `design/index.html` | 프로토타입 진입 파일 (브라우저에서 바로 열림) |
| `design/css/tokens.css` | `--scax-*` 토큰 별칭 → `src/styles/tokens.css` |
| `design/css/shell.css` | 리셋 + 페이지 틀 클래스 → `src/styles/shell.css` |
| `design/css/components.css` | 부품 클래스 → `src/styles/components.css` |
| `design/js/my-work.jsx` | 컴포넌트 전체. 파일 안 `/* ===== <파일명> ===== */` 주석이 이식 단위 (primitives → `src/components/`, shell → `src/layout/`, mywork·app → `src/pages/MyWork/`) |
| `design/js/data.js` | 화면 데이터·문구 → `src/pages/MyWork/data.ts` |
| `ds/Icon.jsx.txt`, `ds/Icon.d.ts.txt` | 교체할 아이콘 컴포넌트 + 선 글리프 116개 (`.txt` 떼고 사용) |
| `ds/product.css`, `ds/typography.css`, `ds/fig-tokens.css` | DS 원본 토큰(참조용) |

프리뷰는 `design/index.html` 을 열면 그대로 동작한다. 단 `_ds_bundle.js`·`styles.css` 경로가 원본 프로젝트를 가리키므로, 이 폴더만 따로 열면 아이콘과 DS 전역 스타일은 빠진 상태로 렌더된다(레이아웃·색·간격은 `--scax-*` 로 자립한다).
