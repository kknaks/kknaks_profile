# 내 업무 — 구현 발주본

- 진입: `내 업무.html` (React 18 UMD + Babel 프리뷰). 소스는 React 19 + Vite 로 그대로 이식되는 평범한 JSX/CSS 다. 외부 UI 라이브러리 없음.
- 화면 하단 「상태」 스위처로 **기본 / 비어 있음 / 로딩 / 오류** 전환. 스위처(`StateSwitch`, `.scax-state-switch`)는 프리뷰 전용 — 구현 시 삭제.
- 문구는 현재 화면 그대로. 상태 전용 문구만 신규(아래 목록).

## 파일 → 이식 위치

| 발주본 | 이식 위치 |
|---|---|
| `css/tokens.css` | `src/styles/tokens.css` (`@import "…/styles.css"` 줄은 DS 패키지 경로로 교체) |
| `css/shell.css` | `src/styles/shell.css` |
| `css/components.css` | `src/styles/components.css` |
| `js/my-work.jsx` — `primitives.jsx` 구간 | `src/components/<Name>.jsx` 로 분해 |
| `js/my-work.jsx` — `shell.jsx` 구간 | `src/layout/` |
| `js/my-work.jsx` — `mywork.jsx`·`app.jsx` 구간, `js/data.js` | `src/pages/MyWork/` |

프리뷰는 브라우저 Babel 로 돌기 때문에 파일을 쪼개면 로딩 순서가 보장되지 않아 한 파일로 합쳐 두었다. 파일 안 `/* ===== <파일명> ===== */` 주석이 이식 단위다.

## 컴포넌트 트리

```
AppShell
├─ SideNav 「신규」                       (DS: Navigation/max)
└─ AppMain
   ├─ PageHeader 「신규」                 (breadcrumb + title + actions)
   │  └─ Button ×2                       일일보고 생성 / 업무 만들기
   └─ PageBody 「신규」
      ├─ rail-left  : InboxRail
      │   └─ GutterList
      │      ├─ SegmentedControl 「신규」  (DS: SegmentedControl/Solid)
      │      ├─ Badge (count)
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

기존 부품 그대로 사용: `Icon` `Button` `Badge` `Select` `Popover` `GutterList` `Empty` `StatusNote`.
이 화면에서 쓰지 않는 기존 부품: `Modal` `DateField` `DatePicker` `TimeField` `Composer` `DropZone` `FileList`.
신규 부품: `SideNav` `PageHeader` `PageBody` `AppShell` `SegmentedControl` `Tabs` `Chip` `InboxCard` `TaskTable` `CalendarRail` `AgentBubble` `Skeleton` `IconButton` `ButtonGroup`.

`Icon` 은 프리뷰에서만 DS 번들(`window.SCAX_DS.Icon`)을 읽는다. 시그니처 `<Icon name size />` 는 그대로이므로 앱에서는 기존 스프라이트 그대로 쓰면 된다. 글리프 이름은 DS 의 Icon/Normal 세트 이름을 사용했다.

## 토큰

`css/tokens.css` 가 DS 변수를 `--scax-*` 로 전부 내보낸다. 컴포넌트 CSS 는 `--scax-*` 만 참조한다 — DS 원본 변수 직접 참조 금지.
계열: `--scax-color-*`(accent·ink·surface·line·fill·status) · `--scax-space-*`(2·4·6·8·10·12·16·20·24·32·48px) · `--scax-radius-*`(xs 6 … 2xl 15, pill) · `--scax-text-*`(caption2·caption1·label2·label1·body1·headline·title / size·lh·ls) · `--scax-fw-*` · `--scax-shadow-*` · `--scax-ring*` · `--scax-state-*`(hover/focus/press 오버레이 불투명도) · 프레임 메트릭(`--scax-nav-width` 180 · `--scax-header-height` 72 · `--scax-rail-left-width` 380 · `--scax-rail-right-width` 342 · `--scax-control-height-*` · `--scax-row-height` 50).
유틸리티 클래스·인라인 스타일·프레임워크 클래스명 없음. 클래스명은 `scax-<블록>__<요소>--<변형>`.

## 상태

| 상태 | 좌측 수신함 | 본문 업무 목록 | 우측 캘린더 |
|---|---|---|---|
| 기본 | 카드 3 | 행 9 | 일정 3 |
| 비어 있음 | `Empty` | `Empty` | `Empty` |
| 로딩 | `Skeleton--card` ×3 | `skeleton-row` ×6 (헤더 유지) | `Skeleton--agenda` ×3 |
| 오류 | `StatusNote` + 다시 시도 | `StatusNote` + 다시 시도 | `StatusNote` + 다시 시도 |

상태 전용 신규 문구: 「새로운 수신 항목이 없습니다 / 업무·참고 알림이 도착하면 여기에 표시됩니다.」 「표시할 업무가 없습니다 / 새 업무를 만들거나 수신함에서 업무로 옮겨 보세요.」 「등록된 일정이 없습니다」 「…을 불러오지 못했습니다」 「다시 시도」. 그 외 모든 문구는 현재 화면과 동일.

## 동작 (프리뷰에 구현된 것만)

화면 내부에서 완결되는 것만 동작한다 — 별표 토글, 상태 `Select` 변경, 수신함 `확인완료` 제거, 행의 `확인/보완 요청/수락/거절`(결과 라벨로 치환), 탭·칩·세그먼티드·사이드 메뉴 선택.
화면 밖으로 나가는 버튼(`일일보고 생성` `업무 만들기` `답장` `원문 확인하기` `WBS 보기` `업무로 추가`)은 마크업·상태만 있고 핸들러는 비어 있다 — 라우팅은 개발 단계에서 연결.

## 페이지 틀 규칙 (이후 모든 화면 공통)

1. `AppShell` > `SideNav`(180px 고정) + `AppMain`.
2. `PageHeader` 72px: 좌측 `breadcrumb` → `h1` 2행, 우측 액션. 하단 1px `--scax-color-line`.
3. `PageBody` 3구획: 좌 레일(380px, 선택) · 본문(가변, `min-width:var(--scax-content-min-width)` = 640px) · 우 레일(342px, 선택). 레일 없는 화면은 본문만.
4. 스크롤은 각 구획 내부(`overflow-y:auto`)에서만. 페이지 전체 스크롤 없음.
5. 최소 폭 **1542px** = 180 + 380 + 640(`--scax-content-min-width`) + 342. 업무 테이블은 고정 트랙(44+120+140+120+200) + 좌우 24px 패딩 + 제목 트랙 때문에 `--scax-table-min-width:880px` 을 가진다 — 본문이 880 보다 좁아지면 테이블이 찌그러지지 않고 본문 구획이 가로 스크롤한다(`.scax-page-body__content{overflow:auto hidden}`). 1542 보다 좁아지면 페이지가 가로 스크롤한다.
