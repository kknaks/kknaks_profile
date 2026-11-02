# [frontend] REDRAW-02 — 앱 셸 + 내 업무(리스트·칸반)의 **시각만** 시안대로 고친다

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

---

## ⛔ 0. 이 work 의 성격 — 새로 만들지 않는다

**화면은 이미 완성되어 돌아간다.** 목록·필터·정렬·페이지네이션·칸반 DnD·상태 전이·컨텍스트 메뉴가 전부 구현돼 있다.
**동작을 하나도 건드리지 마라. 틀린 것은 시각뿐이다.**

앞선 work 은 끝났다 — **REDRAW-00**(토큰 3파일) · **REDRAW-01**(로그인). 그 파일들을 되돌리지 마라.

### 정본 — 세 층이고 위가 아래를 이긴다

| 순위 | 무엇 | 어디 |
|---|---|---|
| 1 | **사용자 승인 정정** | `orchestration/work/docs-v1/design-requests.md` §A |
| 2 | **시안 — 시각 정본** | `.dc.html` |
| 3 | **SPEC — 동작 정본** | `20-spec/spec-004-tasks-status-views.md` 등 |

### 🚫 시안이 낡은 자리 2곳 — **되돌리지 마라**

이 둘은 **코드가 맞다.** 시안이 정정 이전 그림이다. 「시안대로」 고치면 반려다.

| 무엇 | 시안(낡음) | 코드(맞음) | 근거 |
|---|---|---|---|
| **리스트 컬럼** | 시작일 · 종료일 **2개** | **기한 1개** | **A-4** — `startDate`/`endDate` 를 `due_date` 하나로 정리했다. 시작일 데이터가 없다 |
| **뷰 전환 활성색** | `#1E1E1E` (Ink) | 선택색 `#F4F5FF` + `#4B52A8` | **A-16** — 같은 화면 유형 탭 밑줄이 Ink 라 「검정은 위치, 화면당 하나」를 어긴다 |

**유형 배지도 마찬가지다** — 시안의 4색 고정 배지가 아니라 **동적 팔레트**(`data-color-token`)가 맞다(**A-1·A-2**). `TypeBadge` 의 색 결정 방식을 바꾸지 마라. 규격(높이·radius·글자)만 맞춰라.

### 반드시 열 파일 (절대경로 · 읽기 전용)

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/업무 화면 정의서.dc.html
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/로그인 · 계정 · 프로필.dc.html
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/디자인 시스템.dc.html
```

| 무엇 | 어디 |
|---|---|
| 리스트 화면 | `업무 화면 정의서.dc.html` **24~220줄** |
| 칸반 화면 | 같은 파일 **222~410줄** |
| 1440 · 1280 | 같은 파일 **1074줄 · 1218줄 · 1323줄** |
| **사이드바 실측** | `로그인 · 계정 · 프로필.dc.html` **117~136줄** |
| 공통 컴포넌트 규격 | `디자인 시스템.dc.html` **06 COMPONENTS** |

**`00-design/*.md` 요약본은 열지 마라.** 그것이 이 사고의 원인이다.

> ⚠ **시안의 「설명 그림」과 「설명 문장」이 다르면 문장이 맞다.** 축소된 삽화의 그림자·크기를 값으로 읽지 마라.
> ⚠ **시안이 평평해 보여도 구조는 중첩이다.** 아래 표의 gap 값을 flat 하게 적용하지 말고, 시안의 묶음 구조를 그대로 따라라. 애매하면 물어라.

---

## 1. 범위

| 파일 | 무엇 |
|---|---|
| `src/components/shared/AppShell.tsx` | breadcrumb 자리 · 세로 리듬 |
| `src/components/shared/Sidebar.tsx` | 8건 |
| `src/features/tasks/components/TasksScreen.tsx` | 툴바 · 유형 탭 · 페이지네이션 |
| `src/features/tasks/components/TaskListView.tsx` | 표 4건 |
| `src/features/tasks/components/KanbanBoard.tsx` | 컬럼 · 카드 |
| `src/components/shared/UnderlineTabs.tsx` | 탭 규격 |
| `src/components/shared/PeriodStepper.tsx` · `StatusDot.tsx` · `TypeBadge.tsx` | 규격만 |
| `src/styles/tokens.css` · `tailwind.config.ts` | **필요한 토큰 추가만** |

**하지 않는 것**
- **동작·상태·조건·라우팅·쿼리를 바꾸지 마라**
- 다른 화면 파일(상세 드로어·설정)을 건드리지 마라 — 다음 work 이다
- 기존 토큰 값을 고치지 마라. **더하기만** 한다
- **hex 리터럴을 컴포넌트에 쓰지 마라**
- §2 에 없는 것을 고치지 마라. 이상해 보이면 **보고만** 해라

---

## 2. 고칠 것 — 22건

### AppShell.tsx — 2건

| # | 지금 | 시안 (24~51줄) |
|---|---|---|
| 1 | **breadcrumb 자리가 없다** | `left 240 / top 38` — 「홈 › 내 업무」 **13px `#9EA2AE`**, 현재 항목만 `#757575`, chevron 11px stroke `#B3B3B3`, `gap 7`. **AppShell 이 슬롯을 갖고 화면이 채운다** |
| 2 | `py-8` 균등 | breadcrumb **38** · 타이틀 **66** · 본문 **132**(리스트) / **140**(칸반). 좌측 `240` = 사이드바 200 + 40 |

> 1번은 **슬롯만 만든다.** 각 화면이 무엇을 넣을지는 이 work 에서 `/tasks` 만 채우고 나머지는 비운다.

### Sidebar.tsx — 8건

시안 `로그인 · 계정 · 프로필.dc.html` 117~136줄. **200 고정, 항목이 서로 붙어 있다.**

| # | 지금 | 시안 |
|---|---|---|
| 3 | 항목 `h-todo` (44px) | **35px** |
| 4 | 항목 `px-3` (12) | **14** |
| 5 | 항목 사이 `gap-1` (4) | **0 — 붙어 있다** |
| 6 | 항목 `text-body` (15) | **14** (활성만 700) |
| 7 | 프로필에 **아바타가 없다** | **32px 원** `linear-gradient(140deg,#C3CBFB,#98A6F0)` — 토큰으로. 이름과 `gap 8`, `top 80` |
| 8 | **알림 벨이 없다** | **30×30 · r8 · border `#EBEBEB`** · 벨 글리프 15px stroke `#1E1E1E` 1.3 · 프로필 행 **우측 끝** |
| 9 | 이름 `text-section` (15/700) | **14 / 700** |
| 10 | 소속 `text-caption` (12) | **11px** `#9EA2AE` |

**세로 리듬** — 로고 `top 23.5`(25px 마크) · 프로필 `top 80` · 메뉴 `top 143`. 지금은 `py-6` + `gap-6` 균등이다.

> **#8 알림 벨은 v1 에 도메인이 없다.** 시안대로 그리되 **누르면 아무 일도 없게** 두고, `V2Gate` 를 붙이지 마라(문구를 정한 적이 없다). 클릭 핸들러 없이 정적으로만 그려라.
> **사이드바 로고는 25px 이다** — 로그인 브랜드 패널의 32px 과 다르다. `BrandMark` 에 크기 prop 을 더해 두 곳을 갈라라. 로그인 쪽 값을 바꾸지 마라.

### ⚠ 예외 2건 — 이것만 **시각이 아니라 동작**이다

이 work 은 「시각만」이 원칙이지만 **아래 둘은 사용자가 확정한 교정**이라 함께 처리한다.
근거는 `10-decision/decision-002-my-tasks.md` §「2026-09-06 SPEC 오적용 교정」.

**E-1. 활성 필터 칩 「필터 n ✕」을 제거한다**

`TasksScreen.tsx` 타이틀 옆의 필터 칩(현재 `h-6 rounded-chip border-primary bg-secondary …`)을 **없앤다.**

- **내 업무 시안에 이 UI 가 없다** — `업무 화면 정의서.dc.html` 에서 「필터」 검색 결과 **0건**
- 출처는 **디자인 시스템 [11] CALENDAR** 의 「Type Filter · 범례 겸 필터」다. 캘린더는 유형 필터가 **별도 패널**이라 화면 위에서 뭐가 걸렸는지 안 보여서 칩이 필요했다
- 내 업무는 **유형 탭이 바로 아래에서 선택 상태를 밑줄+굵기로 보여준다.** 칩은 같은 정보를 두 번 말한다
- **칩만 지운다.** 필터 상태·쿼리·해제 동작은 유지한다 — 해제는 유형 탭의 「전체」로 돌아가는 것이다
- SPEC-004 U-12 는 이미 갱신됐다

**E-2. 헤더는 뷰와 무관하게 하나다 — 정렬·상태 필터를 칸반에도 그린다**

지금은 `params.view === "list"` 일 때만 정렬·상태를 그리고 **칸반이면 `null` 이라 툴바에 필터가 하나도 없다.**

- **정본 = 시안 리스트 헤더(24~88줄) 하나다.** 리스트든 칸반이든 이 구성이 그대로 있다:
  breadcrumb / 좌측 `내 업무 + ‹ 2026년 8월 ›` / 우측 `[리스트|칸반] · 정렬·종료일 · 상태 전체 · + 새 업무` / 그 아래 유형 탭
- **뷰 토글은 그 아래 본문만 바꾼다.** 헤더는 움직이지도 사라지지도 않는다
- `params.view` 분기를 **없애고** `SortPopover`·`StatusFilterPopover` 를 항상 그려라
- **「오늘」 버튼을 제거한다** — 시안 헤더에 없다(필터 칩과 같은 종류)
- **프로젝트 필터를 만들지 마라.** 이전 결정 A-17 「칸반 헤더 필터 = 프로젝트」는 **번복됐다**
- 근거: DEC-002 §「2026-09-06 SPEC 오적용 교정」 · SPEC-004 U-12
- 알려진 결과 — 칸반에 상태 필터를 걸면 해당 컬럼 하나만 남는다. **의도된 동작이다.** 막지 마라

**E-3. 기간 스테퍼 라벨을 누르면 날짜 범위를 고른다** (신설)

지금은 월 단위로만 움직인다. 사용자 확정으로 **날짜 범위**까지 다룬다.

- `‹` `›` 는 **기간 이동**이다. 기본(한 달)에서는 지금처럼 월 단위
- **라벨 클릭 → 달력 팝오버**에서 **시작일–종료일**을 고른다. 하단에 「이번 달」·「이번 주」 바로가기
- 범위를 고르면 라벨이 「**08.01 – 08.15**」로 바뀌고, `‹` `›` 는 **고른 범위와 같은 길이만큼** 이동
- 범위가 한 달 경계와 정확히 같으면 라벨은 「**2026년 8월**」로 되돌아간다
- **서버 계약은 그대로다** — `from`·`to` 는 이미 날짜다(SPEC-004 §4). 프론트가 달 경계로만 채워 보냈을 뿐이다. **새 파라미터를 만들지 마라**
- 팝오버 규격은 디자인 시스템 **[07] Popover** — 200~400 · 스크림 없음 · 트리거 아래 8px · 공간 없으면 위로. 항목·현재값 표현도 07 을 따른다
- 달력 UI 자체는 시안에 없다. **디자인 시스템 규격 안에서만** 만들고, 설명이 안 되는 자리가 나오면 **물어라**

**E-4. 「이전 달」 문구 4곳을 기간 표현으로 바꾼다** (E-3 의 파급)

기간이 월 고정이 아니게 되므로 「이전 달」이라는 말이 안 맞는다. 아래 4곳을 고쳐라.

| 파일:줄 | 지금 | 바꿀 말 |
|---|---|---|
| `KanbanBoard.tsx:192` | 「{월} 완료 {n}건 · **이전 달은 기간 이동으로 보기**」 | 「{기간} 완료 {n}건 · **이전 기간은 기간 이동으로 보기**」 |
| `TasksScreen.tsx:318` | 「새 업무를 만들거나 **이전 달을** 살펴보세요」 | 「새 업무를 만들거나 **다른 기간을** 살펴보세요」 |
| `TasksScreen.tsx:325` | 「**이전 달 보기**」 | 「**이전 기간 보기**」 |
| `PeriodStepper.tsx:32` | `aria-label="이전 달"` | `aria-label="이전 기간"` (다음 버튼도 같이) |

- `formatMonth(month)` 처럼 **월을 전제한 표시 함수**가 있으면 기간 범위를 받도록 넓혀라. 범위가 한 달 경계와 같으면 「2026년 8월」, 아니면 「08.01 – 08.15」다(E-3)
- 「n건 중 m건 표시」 요약(페이지네이션 좌측)도 같은 규칙으로 기간을 표시한다

> **E-1~E-4 는 시각이 아니라 동작·문구다.** 그 외 항목에서는 동작 코드를 건드리지 마라.
>
> **참고 — 시안이 없는 것이 정상인 자리**: 빈 상태 · 스켈레톤 · 검색 결과 없음 · 지연 뱃지 · 칸반 드래그 중 · 카드 컨텍스트 메뉴는
> `design-requests.md` §B-2 에 **미설계로 이미 인정**돼 있다. 이 자리들은 시안을 찾지 말고 **디자인 시스템 공통 규격**으로만 맞춰라.

### TasksScreen.tsx — 툴바 5건

| # | 지금 | 시안 (53~80줄) |
|---|---|---|
| 11 | 헤더가 `flex-wrap` 한 줄 + `flex-1` 스페이서 | **두 그룹** — 좌(타이틀 + 기간 스테퍼, `gap 16`) / 우(뷰토글·정렬·상태·새업무, `gap 10`), `justify-between` · `align-items: flex-end` |

> **#11 은 눈에 보이는 결함이다. 반드시 잡아라.**
> 지금은 툴바가 한 줄이고 타이틀 뒤에 `flex-1` 스페이서가 있어서, **기간 스테퍼가 우측 버튼 수에 따라 좌우로 움직인다** —
> 리스트(정렬·상태 있음)와 칸반(없음)에서 스테퍼 위치가 달라진다. 사용자가 지적한 자리다.
> 시안은 **스테퍼가 타이틀에 붙어 있는 좌측 그룹의 일부**라 뷰를 바꿔도 움직이지 않는다.
> `flex-1` 스페이서를 지우고 **좌/우 두 묶음 + `justify-between`** 으로 바꿔라.
| 12 | 뷰 토글 `bg-muted p-0.5` 필 | **h34 · r8 · border `#D9D9D9` · `overflow:hidden`** 세그먼트 2칸. 칸은 `padding 0 13` · 13px · 아이콘 13px · `gap 6`, 사이 `border-left #EBEBEB`. **활성 색은 A-16 대로 유지**(`#F4F5FF`+`#4B52A8`) |
| 13 | 정렬 · 상태 버튼 | **h34 · r8 · border `#D9D9D9` · 흰 배경 · 13px `#757575` · `padding 0 14` · `gap 8`** · chevron 11×7 |
| 14 | 「새 업무」 | **h34 · `#7181F8` · 13/600 · `padding 0 16` · `gap 7`** · 아이콘 14px · hover `#5F71F5` |
| 15 | 기간 스테퍼 | ‹ **30×30 r8 border `#D9D9D9`** / 라벨 **h30 r8 border `#D9D9D9` `padding 0 12` 14/600** / › 30×30. 셋 사이 `gap 6` |

> **#15 는 사용자가 이미지로 지목한 자리다. 시안 57~59줄을 그대로 옮겨라.**
> - `‹` `›` — **30×30** · r8 · **border 1px `#D9D9D9`** · 흰 배경 · 글리프 **7×11** stroke `#757575` 1.5 · hover 배경 `#F5F6F8`
> - 라벨 — **h30** · r8 · **border 1px `#D9D9D9`** · 흰 배경 · `padding 0 12` · **14 / 600** · `#1E1E1E`
> - 셋 사이 `gap 6`, 타이틀과는 `gap 16`
> - **세 요소가 모두 테두리를 가진 개별 버튼**이다. 하나로 이어붙인 세그먼트가 아니다
> - E-3 으로 라벨이 클릭 가능해지지만 **닫힌 상태의 모양은 위 그대로**다. 열렸을 때만 Selector 규격(border `#7181F8` + ring)을 얹는다

### UnderlineTabs.tsx — 유형 탭 2건

| # | 지금 | 시안 (82~88줄) |
|---|---|---|
| 16 | 탭 규격 | **h42 · 15px** · 활성 **700 + `border-bottom 2px #1E1E1E`** · 비활성 `#9EA2AE`(hover `#1E1E1E`) · 탭 간 `gap 22` · 컨테이너 `border-bottom 1px #D9D9D9` · `align-items: flex-end` |
| 17 | 색칩 없음 | 각 탭 라벨 앞 **8×8 · r2 색칩** + `gap 7`. 「전체」에는 칩이 없다. **색은 유형의 `colorToken` 에서 온다**(A-1) — 시안의 고정 4색을 하드코딩하지 마라 |

### TaskListView.tsx — 4건

**컬럼은 5개가 맞다**(A-4). 시안의 시작일/종료일 2컬럼으로 되돌리지 마라.

| # | 지금 | 시안 (92~208줄) |
|---|---|---|
| 18 | 헤더 `h-9`(36) · `text-caption`(12) · `#9EA2AE` · border `#EBEBEB` | **h44 · 13px · `#757575` · `border-bottom 1px #D9D9D9`**, 업무명 옆 **정렬 caret 8×6** |
| 19 | 모든 셀 좌측 정렬(`px-3`) | 업무명만 좌(`padding-left 10`), **유형·상태·기한·메모는 가운데** |
| 20 | 업무명 `text-body`(15) | **14 / 600** |
| 21 | 행 구분선 `border-row-divider`(`#F1F2F5`) · 메모 빈칸 `""` | **`#EBEBEB`** · 메모 없으면 **`—`** (`#9EA2AE`) |

행 높이 `h-row`(52) · hover `#FAFBFC` · 취소 행 제목 취소선+`#9EA2AE` 는 **맞다. 두어라.**
상태 셀은 팝오버 트리거지만 **표시는 dot 8px + 13px 상태색 텍스트**여야 한다 — 지금 텍스트가 `text-foreground` 라 상태색이 아니다.

### KanbanBoard.tsx — 1건 묶음

시안 276~410줄. 아래 규격으로 맞춰라.

- 보드 `grid-template-columns: repeat(4,1fr)` · `gap 20`
- 컬럼 — 배경 **`#F9FAFB`** · border **`#EBEBEB`** · **r16** · `padding 16` · `gap 12`
- 컬럼 헤더 — dot 8px + 이름 **14/700** + 카운트 **12px `#757575`**, `gap 8`
- 카드 — 흰 배경 · border **`#D9D9D9`** · **r8** · `padding 14` · `gap 8`
  - 유형 배지 `align-self: flex-start`
  - 제목 **14 / 600 / lh 1.4**
  - 하단 행 `justify-between` · **12px `#757575`**, D-day 는 `#7181F8` 600
- **진행중 컬럼의 현재 카드 1개만** border `#7181F8` + `box-shadow: 0 4px 12px rgba(113,129,248,0.14)`
- 컬럼 맨 아래 「업무 추가」 — **h38 · r8 · `border 1px dashed #D9D9D9`** · 13px `#9EA2AE` · 아이콘 13px · `gap 6` · hover 배경 흰색 + `#1E1E1E`

> 컬럼 배경 `#F9FAFB` 는 `--tm-column` 이다. REDRAW-00 에서 `--tm-canvas` 와 값이 같아졌지만 **의미가 다르다** — 여기서는 `--tm-column` 을 써라.

### 페이지네이션 — TasksScreen 하단

시안 210~218줄.
- 좌측 요약 **13px `#9EA2AE`** — 「2026년 8월 · 24건 중 12건 표시」
- 우측 버튼 — **30×30 · r8**, 이전/다음은 border `#D9D9D9`, **현재 페이지는 `#1E1E1E` 배경 + 흰 글씨 13/700**, 나머지 페이지는 border `#D9D9D9` + 13px `#757575`, `gap 6`
- 줄 전체 `justify-between`

**문구·계산·조건은 그대로 둔다.** 규격만 맞춘다.

---

## 3. 토큰

필요하면 `tokens.css` 에 **더하고** `tailwind.config.ts` 에 연결해라. **기존 값을 고치지 마라.**
- 사이드바 아바타 그라디언트 `linear-gradient(140deg,#C3CBFB,#98A6F0)`
- 칸반 활성 카드 그림자 `0 4px 12px rgba(113,129,248,0.14)`
- 없으면 `--tm-fg-placeholder: #b3b3b3`

---

## 4. 검증

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 전체 빌드 금지, 1회만
```

자기점검 — **컴포넌트 hex 리터럴 0개** · 동작 코드 diff 0줄 · `git status` 에 §1 파일만

**캡처 4장** (`npm run dev`)
1. **1920** `/tasks` 리스트 — 사이드바 + breadcrumb + 툴바 + 유형 탭 + 표 + 페이지네이션
2. **1920** `/tasks` 칸반
3. **1280** `/tasks` — 사이드바가 햄버거 오버레이로 바뀌고 메모 컬럼이 숨는다
4. **1920** 사이드바 확대 — 아바타 · 알림 벨 · 항목 35px

---

## 5. 지킹 것

1. **시각만 고친다.** 동작 코드를 한 줄도 바꾸지 마라
2. **§0 의 「시안이 낡은 자리 2곳」을 되돌리지 마라** — A-4 컬럼, A-16 뷰 토글 색
3. **§2 에 없는 것을 고치지 마라.** 이상해 보이면 **완료 보고에 적어라**
4. **막히면 물어라** — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다
5. **커밋·push 하지 마라**

## 6. Done Criteria

- [ ] 22건 전부 반영, 각 항목이 시안 값과 일치
- [ ] **A-4 컬럼 5개 · A-16 뷰 토글 색 유지** (되돌리지 않았음)
- [ ] 유형 배지·탭 색칩이 **동적 `colorToken`** 에서 온다 (고정 4색 하드코딩 0)
- [ ] 동작 코드 diff **0줄**
- [ ] 컴포넌트 hex 리터럴 0개
- [ ] `npx tsc --noEmit` 0 에러
- [ ] 캡처 4장

---

## 7. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] frontend: <질문>" --enter
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 / 22건 각각 반영 결과 / A-4·A-16 유지 근거 / 추가 토큰 / 동작 diff 0줄 근거 / tsc / 캡처 경로 / 눈에 띄었지만 안 고친 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
