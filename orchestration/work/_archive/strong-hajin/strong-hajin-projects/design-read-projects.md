# 시안 정독 — 「프로젝트」 화면 (레이아웃·색·위치만)

**정본**: `reference/2026-09-10-sc-meeting/package 2/Projects.html`
+ `handoff/projects/{js/projects.v1.jsx, js/data.js, css/projects.css}`
+ 공용 `handoff/shell/{js/nav.js, js/scax-ui.jsx}` · `_ds_bundle.css`

**이 문서의 범위**: 화면이 **무엇을 어디에 어떤 색으로** 놓는가.
상태값·논리 구조는 **우리 코드가 정본**이다 — 시안의 목데이터 구조는 「이 화면이 무슨 사실을
요구하는가」의 목록으로만 읽는다.

## 1. 틀 — 3레일

```
┌ SideNav ─┬ 좌 레일 380px ─┬ 본문 (flex) ──────┬ 우 레일 342px ─┐
│ 9항목    │ 「업무」 헤더    │ ① 요약 스트립      │ 선택 업무 상자  │
│ activeId │  + count 배지   │ ② 진행 라인(간트)  │  (없으면 Empty) │
│ ='project'│ + 프로젝트 셀렉터│   + ③ 의존선      │                │
│          │ 업무 카드 목록   │                   │                │
└──────────┴────────────────┴───────────────────┴────────────────┘
AppHeader: title 「프로젝트」 (breadcrumb·actions 없음)
```

- 레일 폭은 DS 토큰: `--scax-rail-left-width = --ax-inbox-w = 380px` ·
  `--scax-rail-right-width = --ax-calendar-w = 342px`. **업무·캘린더 화면과 같은 폭**이다
- 좌 레일 `border-right` + `shadow-card`, 우 레일 `border-left`. 둘 다 바닥까지
- 내비에서 「프로젝트」는 `folder` 아이콘, 업무 다음·캘린더 앞 자리

## 2. 좌 레일 — 프로젝트 셀렉터 + 업무 카드

- 헤더 한 줄: `square-check` 24px 아이콘 + **「업무」** + `Badge variant="count"` (건수)
  그 아래 `Select`(ariaLabel 「프로젝트 선택」) — **프로젝트 전환이 헤더에 있다.** 별도 목록 화면 없음
- 카드는 **업무 탭 `scax-inbox-card` 를 그대로 재사용**. 새 부품 아님
  - 구성: 상태 배지 → 제목 → meta 한 줄(`when` · 담당 · 분류)
  - 이 화면이 더하는 것은 **선택 상태뿐**: hover `accent-20`/`accent-05`,
    selected `border accent` + `bg accent-08`, focus `--scax-focus-ring`

## 3. 본문 ① 요약 스트립

`grid-template-columns: repeat(4, minmax(96px,1fr)) minmax(180px,1.6fr)` — 5칸, 마지막이 넓다.

| 칸 | 라벨 | 값 색(tone) |
|---|---|---|
| 1 | 전체 업무 | `ink-strong` |
| 2 | 진행 중 | `accent` |
| 3 | 지연 | `danger` |
| 4 | 완료 | `positive` |
| 5 (wide) | 전체 진행률 | 6px 미터 바(`accent` fill) + % 텍스트 |

- 칸: `border line` · `radius-xl` · `surface`, 라벨 caption1 `ink-assistive`, 값 **24px/32px bold**, `tabular-nums`

## 4. 본문 ② 진행 라인 (간트) — 카드 하나

기하는 상수로 못 박혀 있다: `{ day: 34, row: 40, label: 200, days: 30, today: 17 }`

- 머리: 「진행 라인」(body1 semibold) + legend 「2026년 9월 · 화살표는 선행 → 후행」(caption1 assistive)
- 축: 1~30 일, 하루 34px, `today` 는 accent + semibold. 아래로 `line-weak` 경계
- 격자: 세로 34px · 가로 40px 의 `line-weak` 선. `now` 는 1px accent 세로선(opacity .5)
- 행(40px): `[twisty 16px][이름/담당 = label 200px][바]`
  - twisty 는 **하위 업무가 있을 때만**. `chevron-down/right`. 기본은 **모두 펼침**
  - 이름 2줄: 제목(label1 medium, ellipsis) / 담당·`하위 N`(caption2 assistive). 선택 시 accent semibold
  - 하위 행은 `padding-left: space-600` 들여쓰기, 이름 regular `ink-neutral`
- 바: 높이 **22px**(기본) / **14px 상위** / **18px 하위**, `radius-sm`, 안에 진행률 fill + % 텍스트
  (상위 바는 % 를 숨긴다). 선택 시 `box-shadow 0 0 0 2px accent`

| status | 바 배경 | fill |
|---|---|---|
| progress | `accent-20` | `accent` |
| blocked | `danger-soft` | `danger` |
| done | `fill-weak` | `positive` |
| not-started | `fill-weak` | `line-strong` |

## 5. 본문 ③ 의존선

- 간트 위에 겹치는 **SVG 오버레이**(`position:absolute; inset:0; pointer-events:none`)
- 경로는 직각 3구간: `M 선행끝 H 중간 V 후행행 H 후행시작-5` + 화살표 marker
- 평소 `line-strong` 1.2px, **선택된 업무에 닿는 선만** `accent` 1.6px

## 6. 우 레일 — 선택 업무 상자

선택 없으면 `Empty`(icon `square-check`, 「업무를 선택하세요」).

머리: 제목(body1 semibold) + 진행률 미터(6px) + %. 본문은 블록 4개:

1. **메타 정보** — `dl` 2열(키 64px): 상태(배지) · 기간 · 담당 · 요청 · 분류 · 상위 업무
2. **관계** — 선행(`arrow-up`) / 후행(`arrow-down`) 각각 건수 + 목록.
   줄마다 status dot(accent/danger/positive) + 제목 + `chevron-right`, **누르면 그 업무로 이동**
3. **체크리스트** — `done/total` 카운트. 완료 항목은 accent 체크박스 + 취소선
4. **하위 업무** — 카드 목록(제목 + 상태 배지 / `9월 N–M일 · 담당 · N%`), 누르면 이동

## 7. 상호작용 축 — 하나뿐이다

- `project` (셀렉터) = 화면 전체의 데이터 스코프
- `taskId` 하나가 **좌 레일 카드 · 간트 행/바 · 의존선 · 우 레일**을 동시에 묶는다.
  어디서 골라도 나머지 셋이 같이 반응한다
- 그 외 상태는 간트의 `open`(펼침 목록)과 내비 `collapsed` 뿐. **모달·드로어 없음**

## 8. 시안이 「사실」로 요구하는 것 — 우리 구조와 맞춰야 할 자리

시안 목데이터의 구조가 아니라, **화면을 그리려면 반드시 있어야 하는 사실**만 뽑았다.
괄호는 시안 주석이 적어 둔 가정(우리 것이 정본이므로 **확인 대상**).

| # | 화면이 요구하는 사실 | 시안의 가정 |
|---|---|---|
| D-1 | 업무가 어느 프로젝트에 속하는가 | `tasks.project_id` |
| D-2 | 업무의 시작일·종료일 | `from`/`to` (9월 정수일 — 시안 편의) |
| D-3 | 업무의 진행률 % | `tasks.progress` |
| D-4 | 업무 간 선행→후행 | `task_dependencies` |
| D-5 | 상위–하위 업무 (시안은 **1단계만**) | `tasks.parent_id` |
| D-6 | 업무 체크리스트(텍스트 + done) | `task_checklists` |
| D-7 | 상태 5종 | progress · not-started · blocked · done · cancelled |
| D-8 | 담당자 · 요청자 · 분류(내 업무/보낸 업무/완료) | `owner`·`requester`·`group` |
| D-9 | 프로젝트 목록(선택지) | `PROJECT_OPTIONS` |

**범위 밖**: `PROJECT_FILE_TREE`(자료 트리)는 data.js 에 있지만 **이 화면이 쓰지 않는다** —
시안 첫 줄 주석이 「자료함은 나중에 『자료』 탭으로 간다」고 명시한다.
